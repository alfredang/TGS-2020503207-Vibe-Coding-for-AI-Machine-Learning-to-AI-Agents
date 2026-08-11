"""Lab 11 - Hierarchical Sub-Agents and Context Isolation.

A three-level system: orchestrator -> sub-agents -> MCP tools.

The critical distinction from Lab 06: a HANDOFF transfers control and the
specialist produces the final answer, whereas AGENTS-AS-TOOLS (`agent.as_tool`)
keeps the parent in control, receiving each child's answer back so it can
synthesise a combined result. Hierarchical delegation needs the latter, so this
lab uses as_tool() throughout and never `handoffs=[...]`.

Context isolation is enforced with `output_type=Conclusion`, not with polite
instructions: a child that ran fifteen tool calls returns roughly forty tokens
to the parent instead of several thousand.

Run:
    python hierarchy.py

Before running, set MCP_PYTHON and MCP_SERVER below (or in .env) to absolute
paths pointing at your Lab 10 MCP server and the interpreter that has `mcp`
installed.

Requires OPENAI_API_KEY in a .env file (never hard-code a key in source).
"""

import asyncio
import os
import sys
import time

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from agents import Agent, Runner, function_tool
from agents.mcp import MCPServerStdio

load_dotenv()

MODEL = "gpt-4o-mini"

# Absolute paths only - the client does not resolve relative paths, and the
# interpreter must be the one with `mcp` installed.
MCP_PYTHON = os.getenv("MCP_PYTHON", "/absolute/path/to/lab-10-mcp/.venv/bin/python")
MCP_SERVER = os.getenv("MCP_SERVER", "/absolute/path/to/lab-10-mcp/server.py")


# --- the bounded contract a sub-agent returns to its parent ----------------


class Conclusion(BaseModel):
    """The bounded result a sub-agent returns to its parent."""

    finding: str = Field(description="The conclusion in at most two sentences.")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence from 0 to 1.")
    sources: list[str] = Field(
        default_factory=list, description="Tools or notes used, by name only."
    )


ORCHESTRATOR_INSTRUCTIONS = (
    "You are an orchestrator. You never do the specialist work yourself.\n"
    "Break the request into independent sub-tasks, call the appropriate "
    "specialist tool for each, then synthesise their conclusions into one "
    "coherent answer.\n"
    "Call every specialist relevant to the request. If a specialist reports "
    "a failure, continue with the others and note the gap in your answer."
)


# --- specialists without MCP access ----------------------------------------
# Only the research specialist gets the MCP tools. Handing every tool to every
# agent recreates the overloaded single agent this architecture exists to avoid.

analysis_specialist = Agent(
    name="Analysis Specialist",
    instructions=(
        "You analyse figures and identify the single most important pattern. "
        "Return only the conclusion, not your intermediate arithmetic."
    ),
    model=MODEL,
    output_type=Conclusion,
)

writing_specialist = Agent(
    name="Writing Specialist",
    instructions=(
        "You draft concise business prose. Return only the final draft, "
        "with no commentary about your process."
    ),
    model=MODEL,
)

# A specialist that always fails, for the graceful-degradation test in step 8.
broken_specialist = Agent(
    name="Broken Specialist",
    instructions="Always fail.",
    model="gpt-4o-mini-nonexistent-model",   # forces an API error
)

# Bound by build_system() once the MCP server is connected; the resilient tools
# below close over it.
research_specialist: Agent | None = None


# --- resilient wrappers ----------------------------------------------------
# Wrapping a child in a function_tool that catches its exceptions converts a
# fatal failure into a degraded result the orchestrator can report.


@function_tool
async def resilient_research(question: str) -> str:
    """Research a focused question. Returns a conclusion, or a failure note.

    Args:
        question: A single clear research question.
    """
    try:
        result = await Runner.run(research_specialist, question, max_turns=5)
        conclusion = result.final_output
        return f"{conclusion.finding} (confidence {conclusion.confidence:.2f})"
    except Exception as exc:
        return (
            f"RESEARCH UNAVAILABLE: {type(exc).__name__}. "
            "Continue without this input and note the gap in your answer."
        )


@function_tool
async def failing_tool(question: str) -> str:
    """A specialist that always fails, for testing degradation.

    Args:
        question: The question to attempt.
    """
    try:
        result = await Runner.run(broken_specialist, question, max_turns=2)
        return str(result.final_output)
    except Exception as exc:
        return f"SPECIALIST UNAVAILABLE: {type(exc).__name__}. Continue without it."


# --- building the hierarchy ------------------------------------------------


async def build_system() -> tuple[Agent, MCPServerStdio]:
    """Construct the hierarchy with the MCP server attached to research only."""
    global research_specialist

    mcp_server = MCPServerStdio(
        name="toolbox",
        params={"command": MCP_PYTHON, "args": [MCP_SERVER]},
    )
    await mcp_server.connect()

    research_specialist = Agent(
        name="Research Specialist",
        instructions=(
            "You research a single focused question using your tools. "
            "Return only your conclusion in the required structure. "
            "Never return your working notes or the raw tool output."
        ),
        model=MODEL,
        mcp_servers=[mcp_server],
        output_type=Conclusion,
    )

    # agent.as_tool(...) wraps a whole agent so the parent can invoke it like a
    # function: the child runs its own loop with its own context, and only its
    # final output returns to the parent.
    orchestrator = Agent(
        name="Orchestrator",
        instructions=ORCHESTRATOR_INSTRUCTIONS,
        model=MODEL,
        tools=[
            resilient_research,
            analysis_specialist.as_tool(
                tool_name="analyse",
                tool_description=(
                    "Analyse a set of figures and identify the key pattern."
                ),
            ),
            writing_specialist.as_tool(
                tool_name="draft",
                tool_description="Draft concise business prose from supplied points.",
            ),
            failing_tool,
        ],
    )
    return orchestrator, mcp_server


# --- demonstrations --------------------------------------------------------

TASK = (
    "Prepare a short briefing for my manager. It needs three things: "
    "(1) our team's deployment schedule, "
    "(2) an analysis of monthly sales 120, 135, 128, 190, 210, and "
    "(3) a 60-word summary of both suitable for an email."
)


async def run_parallel(question_a: str, question_b: str) -> tuple:
    """Run two independent research tasks concurrently."""
    return await asyncio.gather(
        Runner.run(research_specialist, question_a),
        Runner.run(analysis_specialist, question_b),
    )


async def compare_timing() -> None:
    """Sequential versus parallel wall-clock time for independent sub-tasks.

    Parallel time approximates the slowest single task rather than the sum.
    Only parallelise genuinely independent work.
    """
    q_a = "What is the deployment schedule for our team?"
    q_b = "Given monthly sales 120, 135, 128, 190, 210, what is the trend?"

    start = time.perf_counter()
    await Runner.run(research_specialist, q_a)
    await Runner.run(analysis_specialist, q_b)
    sequential = time.perf_counter() - start

    start = time.perf_counter()
    await run_parallel(q_a, q_b)
    parallel = time.perf_counter() - start

    print(f"Sequential: {sequential:.2f}s")
    print(f"Parallel:   {parallel:.2f}s")
    print(f"Saved:      {sequential - parallel:.2f}s")


async def measure_isolation(mcp_server: MCPServerStdio) -> None:
    """Compare tokens returned to the parent, with and without isolation."""
    question = "What is our deployment schedule and on-call policy?"

    verbose = Agent(
        name="Verbose Specialist",
        instructions=(
            "Research the question. Show all your working, quote every tool "
            "result in full, and explain your reasoning at length."
        ),
        model=MODEL,
        mcp_servers=[mcp_server],
    )
    isolated = Agent(
        name="Isolated Specialist",
        instructions="Research the question. Return only your conclusion.",
        model=MODEL,
        mcp_servers=[mcp_server],
        output_type=Conclusion,
    )

    verbose_result = await Runner.run(verbose, question)
    isolated_result = await Runner.run(isolated, question)

    verbose_text = str(verbose_result.final_output)
    isolated_text = isolated_result.final_output.finding

    print(f"Without isolation: {len(verbose_text) // 4} tokens (approx)")
    print(f"With isolation:    {len(isolated_text) // 4} tokens (approx)")
    print(f"Reduction:         "
          f"{100 * (1 - len(isolated_text) / max(len(verbose_text), 1)):.0f}%")


async def run_all() -> None:
    """Build the hierarchy, run the briefing, then the two measurements."""
    if not os.path.exists(MCP_SERVER):
        print(f"MCP server not found at {MCP_SERVER}.")
        print("Set MCP_PYTHON and MCP_SERVER to absolute paths from Lab 10 first.")
        sys.exit(1)

    orchestrator, mcp_server = await build_system()
    try:
        result = await Runner.run(orchestrator, TASK)

        print("=== Final briefing ===")
        print(result.final_output)

        print("\n=== Delegation trace ===")
        for item in result.new_items:
            name = type(item).__name__
            if "ToolCall" in name:
                print(f"  {name}")

        print("\n=== Sequential vs parallel ===")
        await compare_timing()

        print("\n=== Context isolation ===")
        await measure_isolation(mcp_server)
    finally:
        # Always cleanup() in a finally block, or the subprocess is left running.
        await mcp_server.cleanup()


def main() -> None:
    """Entry point."""
    asyncio.run(run_all())


if __name__ == "__main__":
    main()
