"""Lab 06 - Supervisor Routing and Sub-Agent Delegation (the agent definitions).

Three narrow specialists, a triage supervisor that routes to exactly one of
them via `handoffs`, an input guardrail that rejects out-of-scope requests
before any specialist runs, and a deliberately overloaded control agent used
for the single-agent comparison.

This module only defines the agents. Run `main.py` to exercise them; Lab 07
imports `triage_agent` from here for the Streamlit front end.

NOTE ON THE FILENAME: this file must NOT be called `agents.py`. The OpenAI
Agents SDK is imported as `from agents import ...`, so a local `agents.py`
would shadow the installed package and break every import in the lab.

Requires OPENAI_API_KEY in a .env file (never hard-code a key in source).
"""

from dotenv import load_dotenv
from pydantic import BaseModel

from agents import (
    Agent,
    GuardrailFunctionOutput,
    RunContextWrapper,
    Runner,
    function_tool,
    input_guardrail,
)

load_dotenv()

MODEL = "gpt-4o-mini"


# --- tools -----------------------------------------------------------------

@function_tool
def search_notes(query: str) -> str:
    """Search the internal knowledge base for background on a topic.

    Use this when answering a factual or research question.

    Args:
        query: The search terms.
    """
    notes = {
        "mrt": "The Thomson-East Coast Line opened in stages from 2020.",
        "python": "Python 3.11 introduced significant interpreter speedups.",
        "agents": "Multi-agent systems split work across specialised agents.",
    }
    hits = [text for key, text in notes.items() if key in query.lower()]
    return "\n".join(hits) if hits else "No relevant notes found."


@function_tool
def run_linter(code: str) -> str:
    """Check a Python snippet for syntax errors before returning it.

    Use this to verify any code you are about to give the user.

    Args:
        code: The Python source to check.
    """
    try:
        compile(code, "<submitted>", "exec")
    except SyntaxError as exc:
        return f"Syntax error on line {exc.lineno}: {exc.msg}"
    return "Syntax OK."


@function_tool
def count_words(text: str) -> str:
    """Count the words in a draft, to check it meets a length requirement.

    Args:
        text: The draft text.
    """
    return f"{len(text.split())} words."


# --- specialists -----------------------------------------------------------
# `handoff_description` is the field the triage agent reads when deciding where
# to route. It is to agents what a tool docstring is to tools.

research_agent = Agent(
    name="Research Agent",
    handoff_description="Answers factual and research questions using the knowledge base.",
    instructions=(
        "You are a research specialist. Answer factual questions using the "
        "search_notes tool. Cite what the notes said. If the notes contain "
        "nothing relevant, say so plainly rather than inventing an answer."
    ),
    model=MODEL,
    tools=[search_notes],
)

coding_agent = Agent(
    name="Coding Agent",
    handoff_description="Writes, explains and debugs Python code.",
    instructions=(
        "You are a Python specialist. Write clear, correct code with type hints. "
        "Always check your code with the run_linter tool before returning it, "
        "and fix anything it reports."
    ),
    model=MODEL,
    tools=[run_linter],
)

writing_agent = Agent(
    name="Writing Agent",
    handoff_description="Drafts, edits and summarises prose for a business audience.",
    instructions=(
        "You are a writing specialist. Produce clear, concise prose for a "
        "business audience. Use count_words to confirm you have met any length "
        "requirement the user stated."
    ),
    model=MODEL,
    tools=[count_words],
)


# --- guardrail -------------------------------------------------------------
# A guardrail runs *before* the agent does its work, so an out-of-scope request
# costs one cheap classification instead of a full specialist run.


class ScopeCheck(BaseModel):
    is_out_of_scope: bool
    reasoning: str


scope_agent = Agent(
    name="Scope Check",
    instructions=(
        "Decide whether the request is within scope for a team that handles "
        "research, Python coding and business writing. Medical, legal and "
        "financial advice are out of scope. Set is_out_of_scope accordingly."
    ),
    model=MODEL,
    output_type=ScopeCheck,
)


@input_guardrail
async def scope_guardrail(
    ctx: RunContextWrapper[None], agent: Agent, user_input
) -> GuardrailFunctionOutput:
    """Reject out-of-scope requests before any specialist runs."""
    result = await Runner.run(scope_agent, user_input, context=ctx.context)
    check = result.final_output
    return GuardrailFunctionOutput(
        output_info=check,
        tripwire_triggered=check.is_out_of_scope,
    )


# --- the triage supervisor -------------------------------------------------
# Explicit routing rules plus a stated default beat a one-line
# "route appropriately" instruction, which misroutes.

triage_agent = Agent(
    name="Triage Agent",
    instructions=(
        "You are a supervisor agent. You never answer the question yourself; "
        "your only job is to route it to exactly one specialist.\n\n"
        "Routing rules:\n"
        "- Facts, background, 'what is', 'when did', research questions "
        "  -> Research Agent.\n"
        "- Anything involving code, programming, debugging, or a library "
        "  -> Coding Agent.\n"
        "- Drafting, editing, summarising, emails, reports "
        "  -> Writing Agent.\n\n"
        "If the request is ambiguous or spans several areas, route to the "
        "Research Agent as the default."
    ),
    model=MODEL,
    handoffs=[research_agent, coding_agent, writing_agent],
    input_guardrails=[scope_guardrail],
)


# --- the single-agent control case -----------------------------------------
# One agent holding every tool: the design the team architecture replaces.

kitchen_sink_agent = Agent(
    name="Everything Agent",
    instructions=(
        "You handle research, Python coding and business writing. "
        "Use whichever tool is appropriate."
    ),
    model=MODEL,
    tools=[search_notes, run_linter, count_words],
)
