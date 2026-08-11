# Lab 11 — Hierarchical Sub-Agents and Context Isolation

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tertiarycourses/TGS-2020503207-AI-Vibe-Coding-for-Multi-Agents-System/blob/main/labs/lab-11-hierarchical-sub-agents-and-context-isolation/lab-11-hierarchical-sub-agents-and-context-isolation.ipynb)

**Topic:** 5 — MCP and Sub-Agents  |  **Objective:** Design a hierarchical sub-agent architecture with delegated, isolated context

## Files in this lab

| File | What it is |
|---|---|
| `README.md` | This lab guide. |
| `hierarchy.py` | The finished three-level system: orchestrator with `as_tool()` sub-agents, the `Conclusion` output type enforcing context isolation, the MCP server attached to research only, parallel execution and graceful degradation. Run with `python hierarchy.py`. |
| `lab-11-hierarchical-sub-agents-and-context-isolation.ipynb` | Colab notebook wrapper — the same code, one cell per step, re-creating the Lab 10 MCP server so it runs standalone. |

## Goal

Build the top of the architecture: a parent agent that delegates bounded tasks to specialised child agents, each with its own context and tools. The children return conclusions, not their whole working trace, which is what keeps a large system reliable.

## What you'll build

A three-level hierarchical system — orchestrator, sub-agents and MCP tools — that completes a multi-part task no single agent handles well.

**Tools:** Python, openai-agents SDK or google-adk, your MCP server from Lab 10

## Prerequisites

- Lab 06 completed — you understand handoffs and specialist agents.
- Lab 10 completed, with a working `server.py` MCP server.
- `openai-agents`, `pydantic` and `mcp[cli]` installed; `OPENAI_API_KEY` in `.env`.

This lab uses the OpenAI Agents SDK. The same architecture is achievable in ADK using `AgentTool`.

## Step-by-step

### 1. Define the parent orchestrator whose only job is to decompose the task and delegate

The critical distinction from Lab 06: a **handoff** transfers control and the specialist produces the final answer, whereas **agents-as-tools** keeps the parent in control, receiving each child's answer back so it can synthesise a combined result. Hierarchical delegation needs the latter.

Create `hierarchy.py`:

```python
"""A three-level hierarchy: orchestrator -> sub-agents -> MCP tools."""

import asyncio
import time

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from agents import Agent, Runner, function_tool

load_dotenv()

MODEL = "gpt-4o-mini"

orchestrator = Agent(
    name="Orchestrator",
    instructions=(
        "You are an orchestrator. You never do the specialist work yourself.\n"
        "Break the request into independent sub-tasks, call the appropriate "
        "specialist tool for each, then synthesise their conclusions into one "
        "coherent answer.\n"
        "Call every specialist relevant to the request. If a specialist reports "
        "a failure, continue with the others and note the gap in your answer."
    ),
    model=MODEL,
)
```

### 2. Expose each specialist sub-agent to the parent as a callable tool

`agent.as_tool(...)` wraps a whole agent so the parent can invoke it like a function. The child runs its own loop with its own context, and only its final output returns to the parent:

```python
research_specialist = Agent(
    name="Research Specialist",
    instructions=(
        "You research a single focused question. Return only your conclusion: "
        "the finding and your confidence. Never return your working notes."
    ),
    model=MODEL,
)

analysis_specialist = Agent(
    name="Analysis Specialist",
    instructions=(
        "You analyse figures and identify the single most important pattern. "
        "Return only the conclusion, not your intermediate arithmetic."
    ),
    model=MODEL,
)

writing_specialist = Agent(
    name="Writing Specialist",
    instructions=(
        "You draft concise business prose. Return only the final draft, "
        "with no commentary about your process."
    ),
    model=MODEL,
)

orchestrator = Agent(
    name="Orchestrator",
    instructions=orchestrator.instructions,
    model=MODEL,
    tools=[
        research_specialist.as_tool(
            tool_name="research",
            tool_description=(
                "Research one focused factual question. Pass a single clear "
                "question and receive a conclusion."
            ),
        ),
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
    ],
)
```

### 3. Give each sub-agent its own instructions and only the tools it needs

Attach the MCP server from Lab 10 so the research specialist — and only that specialist — gains your three MCP tools. `MCPServerStdio` spawns the server as a subprocess:

```python
from agents.mcp import MCPServerStdio

MCP_PYTHON = "/absolute/path/to/lab-10-mcp/.venv/bin/python"
MCP_SERVER = "/absolute/path/to/lab-10-mcp/server.py"


async def build_system() -> tuple[Agent, MCPServerStdio]:
    """Construct the hierarchy with the MCP server attached to research only."""
    mcp_server = MCPServerStdio(
        name="toolbox",
        params={"command": MCP_PYTHON, "args": [MCP_SERVER]},
    )
    await mcp_server.connect()

    research = Agent(
        name="Research Specialist",
        instructions=(
            "You research a single focused question using your tools. "
            "Return only your conclusion in the required structure. "
            "Never return your working notes or the raw tool output."
        ),
        model=MODEL,
        mcp_servers=[mcp_server],
    )
    # analysis_specialist and writing_specialist as defined above,
    # deliberately without MCP access.
    ...
    return orchestrator, mcp_server
```

Only the research specialist holds the MCP tools. Handing every tool to every agent recreates the overloaded single agent this architecture exists to avoid.

### 4. Ensure each sub-agent returns a short structured conclusion rather than its full transcript

Instructions alone are unreliable. Enforce the contract with an `output_type`:

```python
class Conclusion(BaseModel):
    """The bounded result a sub-agent returns to its parent."""

    finding: str = Field(description="The conclusion in at most two sentences.")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence from 0 to 1.")
    sources: list[str] = Field(
        default_factory=list, description="Tools or notes used, by name only."
    )
```

Set `output_type=Conclusion` on the research and analysis specialists. A child that ran fifteen tool calls now returns roughly forty tokens to the parent instead of several thousand — this is the mechanism behind context isolation.

### 5. Run sub-agents concurrently where their work is genuinely independent

Independent sub-tasks should not run sequentially. `asyncio.gather` runs them in parallel:

```python
async def run_parallel(question_a: str, question_b: str) -> tuple:
    """Run two independent research tasks concurrently."""
    return await asyncio.gather(
        Runner.run(research_specialist, question_a),
        Runner.run(analysis_specialist, question_b),
    )


async def compare_timing() -> None:
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
```

Parallel time approximates the slowest single task rather than the sum. Only parallelise genuinely independent work — if the analysis depends on the research result, it must wait.

### 6. Give the orchestrator a task requiring at least three sub-agents and trace the delegation

```python
TASK = (
    "Prepare a short briefing for my manager. It needs three things: "
    "(1) our team's deployment schedule, "
    "(2) an analysis of monthly sales 120, 135, 128, 190, 210, and "
    "(3) a 60-word summary of both suitable for an email."
)


async def main() -> None:
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
    finally:
        await mcp_server.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
```

```bash
python hierarchy.py
```

The trace should show three specialist tool calls. Always `cleanup()` the MCP server in a `finally` block, or the subprocess is left running.

### 7. Compare the parent's final context size with and without isolation

Make the benefit quantitative rather than assumed. Measure the tokens returned to the parent under each design:

```python
async def measure_isolation() -> None:
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
```

Expect a large reduction. Multiply that across a dozen sub-agent calls and it is the difference between a system that fits in context and one that does not.

### 8. Handle a failing sub-agent so one failure degrades the result

One broken child must not kill the run. Wrap the child in a `function_tool` that catches its exceptions and returns a message the orchestrator can act on:

```python
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
```

Test it with a deliberately broken specialist:

```python
broken_specialist = Agent(
    name="Broken Specialist",
    instructions="Always fail.",
    model="gpt-4o-mini-nonexistent-model",   # forces an API error
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
```

Add `failing_tool` to the orchestrator's tools and re-run the task from step 6. The orchestrator should complete the briefing using the specialists that worked, and state which part is missing — degradation, not collapse.

## Test it

Verify each of the following:

- [ ] The orchestrator completes the multi-part briefing by delegating to at least three sub-agents — confirm from the trace.
- [ ] The orchestrator itself performs no specialist work; every substantive result arrives from a sub-agent.
- [ ] Sub-agents return `Conclusion` objects, so the parent receives short structured findings rather than full transcripts.
- [ ] The measured context comparison shows a substantial reduction with isolation enabled.
- [ ] `asyncio.gather` measurably reduces wall-clock time for two independent sub-tasks.
- [ ] The research specialist can reach the Lab 10 MCP tools; the analysis and writing specialists cannot.
- [ ] With `failing_tool` attached, the run still completes and the final answer notes the missing input rather than crashing.
- [ ] `await mcp_server.cleanup()` runs in a `finally` block and no orphaned server process remains.

## What you learned

- Agents-as-tools keeps the parent in control and lets it synthesise several children's results, whereas a handoff transfers control entirely — hierarchy needs the former.
- Context isolation is enforced with `output_type`, not with polite instructions: a structured `Conclusion` is what keeps the parent's context small.
- Each sub-agent should hold only the tools its own job requires; MCP servers attach per agent, not globally.
- `asyncio.gather` parallelises genuinely independent sub-tasks, cutting wall-clock time to roughly the slowest one.
- Wrapping a child agent in a try/except tool converts a fatal failure into a degraded result the orchestrator can report.
- Measuring the context reduction turns an architectural claim into evidence.

## References

- Agents as tools — <https://openai.github.io/openai-agents-python/tools/#agents-as-tools>
- Multi-agent orchestration — <https://openai.github.io/openai-agents-python/multi_agent/>
- MCP with the Agents SDK — <https://openai.github.io/openai-agents-python/mcp/>
- Results and run items — <https://openai.github.io/openai-agents-python/results/>
- ADK AgentTool (the ADK equivalent) — <https://google.github.io/adk-docs/tools/function-tools/#agent-as-a-tool>
- Python asyncio.gather — <https://docs.python.org/3/library/asyncio-task.html#asyncio.gather>
- Effective context engineering for AI agents — <https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>
