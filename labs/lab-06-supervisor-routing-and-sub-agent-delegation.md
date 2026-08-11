# Lab 06 — Supervisor Routing and Sub-Agent Delegation

**Topic:** 3 — Multi-Agent System Development with OpenAI Agents SDK  |  **Objective:** Construct a collaborative multi-agent system with supervisor routing and handoffs

## Goal

Move from one overloaded agent to a team. Build three specialists and a triage supervisor that classifies each request and hands it to the right one — the core multi-agent pattern of the course.

## What you'll build

A four-agent system — a triage supervisor plus research, coding and writing specialists — that routes each request to the correct specialist.

**Tools:** Python, openai-agents SDK, Pydantic

## Prerequisites

- Lab 05 completed — `Agent`, `Runner`, `@function_tool` and `output_type` should be familiar.
- The same virtual environment with `openai-agents` and `pydantic` installed.
- `OPENAI_API_KEY` in `.env`.

## Step-by-step

### 1. Define three specialist agents, each with narrow instructions and only the tools its own job requires

Create `team.py`. The discipline here is *narrowness*: each agent's instructions describe one job, and it holds only the tools that job needs. An agent given every tool behaves like the overloaded single agent you are moving away from.

```python
"""A triage supervisor routing to three specialist agents."""

from dotenv import load_dotenv
from agents import Agent, Runner, function_tool

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
```

`handoff_description` is the field the triage agent reads when deciding where to route. It is to agents what a tool docstring is to tools — vague text here produces bad routing.

### 2. Define the triage agent and pass the specialists in its handoffs list

```python
triage_agent = Agent(
    name="Triage Agent",
    instructions=(
        "You are a supervisor. You do not answer questions yourself. "
        "Classify the user's request and hand off to exactly one specialist."
    ),
    model=MODEL,
    handoffs=[research_agent, coding_agent, writing_agent],
)
```

A handoff transfers the conversation: the specialist takes over and produces the final output. That differs from the sub-agents-as-tools pattern in Lab 11, where the parent stays in control and receives the child's answer back.

### 3. Write triage instructions describing when to route to each specialist, with a default

The one-line instruction above will misroute. Replace it with explicit rules and a stated default for ambiguity:

```python
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
)
```

### 4. Run three different requests and confirm each reaches the intended specialist

`result.last_agent` tells you which agent actually produced the answer:

```python
REQUESTS = [
    "When did the Thomson-East Coast Line open?",
    "Write a Python function that reverses a linked list.",
    "Draft a 50-word update to my manager about project delays.",
]

if __name__ == "__main__":
    for request in REQUESTS:
        result = Runner.run_sync(triage_agent, request)
        print(f"\nRequest:  {request}")
        print(f"Handled by: {result.last_agent.name}")
        print(f"Answer:   {result.final_output[:200]}")
```

```bash
python team.py
```

Expect Research, Coding and Writing respectively. If a request lands on the wrong specialist, fix the `handoff_description` and the routing rules — not the request.

### 5. Add a guardrail that rejects out-of-scope requests before any specialist work begins

A guardrail runs *before* the agent does its work, so an out-of-scope request costs one cheap classification instead of a full specialist run. The guardrail function returns a `GuardrailFunctionOutput`; setting `tripwire_triggered=True` halts the run by raising.

```python
from pydantic import BaseModel
from agents import (
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    input_guardrail,
)


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
```

Attach it to the triage agent and catch the exception at the call site:

```python
triage_agent.input_guardrails = [scope_guardrail]

if __name__ == "__main__":
    for request in REQUESTS + ["Should I take ibuprofen for my headache?"]:
        try:
            result = Runner.run_sync(triage_agent, request)
            print(f"\n{request}\n  -> {result.last_agent.name}")
        except InputGuardrailTripwireTriggered as exc:
            reason = exc.guardrail_result.output.output_info.reasoning
            print(f"\n{request}\n  -> REFUSED: {reason}")
```

The guardrail is declared with `input_guardrails=[...]` on the agent; the assignment above simply keeps the example readable after the fact.

### 6. Inspect the trace to see the handoff chain

Open <https://platform.openai.com/traces> and select the most recent run. The timeline shows the triage span, the handoff, the specialist span and each tool call nested underneath, with duration and token counts. This is how you find out that, for instance, the guardrail is costing more than the specialist it protects.

You can also read the handoff from the result in code:

```python
result = Runner.run_sync(triage_agent, "Write a Python function to sort a dict by value.")
print(f"Started at: Triage Agent")
print(f"Ended at:   {result.last_agent.name}")
for item in result.new_items:
    print(f"  {type(item).__name__}")
```

### 7. Compare against a single agent given all the tools

Build the control case and run the same requests through both:

```python
kitchen_sink_agent = Agent(
    name="Everything Agent",
    instructions=(
        "You handle research, Python coding and business writing. "
        "Use whichever tool is appropriate."
    ),
    model=MODEL,
    tools=[search_notes, run_linter, count_words],
)

if __name__ == "__main__":
    for request in REQUESTS:
        single = Runner.run_sync(kitchen_sink_agent, request)
        team = Runner.run_sync(triage_agent, request)
        print(f"\nRequest: {request}")
        print(f"  single-agent tools used: "
              f"{sum(1 for i in single.new_items if 'ToolCall' in type(i).__name__)}")
        print(f"  team specialist:         {team.last_agent.name}")
```

Watch for the single agent skipping `run_linter` on a coding request, or answering a factual question from its own weights instead of calling `search_notes`. With one narrow instruction set per specialist, that drift largely disappears — which is the reliability argument for multi-agent systems.

## Test it

Verify each of the following:

- [ ] A research question ("When did the Thomson-East Coast Line open?") reaches the **Research Agent** — confirm via `result.last_agent.name`.
- [ ] A coding request reaches the **Coding Agent**, and the trace shows `run_linter` was called.
- [ ] A writing request reaches the **Writing Agent**.
- [ ] An out-of-scope request (medical advice) raises `InputGuardrailTripwireTriggered` **before** any specialist runs — no specialist span appears in the trace.
- [ ] The trace at <https://platform.openai.com/traces> shows the handoff chain from triage to specialist.
- [ ] The single-agent control case shows at least one instance of skipped-tool or misapplied behaviour that the team handles correctly.

## What you learned

- Handoffs transfer the conversation to a specialist, which then produces the final output; `result.last_agent` reveals who answered.
- `handoff_description` is the routing signal — it is to agents what a docstring is to tools.
- Explicit routing rules plus a stated default beat a one-line "route appropriately" instruction.
- Input guardrails reject out-of-scope work before expensive specialist runs, raising `InputGuardrailTripwireTriggered`.
- Narrow instructions and narrow tool sets are what make a team more reliable than one agent holding every tool.

## References

- Handoffs — <https://openai.github.io/openai-agents-python/handoffs/>
- Guardrails — <https://openai.github.io/openai-agents-python/guardrails/>
- Multi-agent orchestration — <https://openai.github.io/openai-agents-python/multi_agent/>
- Tracing — <https://openai.github.io/openai-agents-python/tracing/>
- Agents SDK examples — <https://github.com/openai/openai-agents-python/tree/main/examples>
