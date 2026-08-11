"""Lab 06 - Supervisor Routing and Sub-Agent Delegation (the runner).

Exercises the team defined in team.py:
  1. routes three requests and reports which specialist handled each,
  2. shows the guardrail refusing an out-of-scope (medical) request,
  3. compares the team against a single agent holding every tool.

Run:
    python main.py

Requires OPENAI_API_KEY in a .env file (never hard-code a key in source).
Open https://platform.openai.com/traces afterwards to see the handoff chain.
"""

from agents import InputGuardrailTripwireTriggered, Runner

from team import kitchen_sink_agent, triage_agent

REQUESTS = [
    "When did the Thomson-East Coast Line open?",
    "Write a Python function that reverses a linked list.",
    "Draft a 50-word update to my manager about project delays.",
]

OUT_OF_SCOPE = "Should I take ibuprofen for my headache?"


def show_routing() -> None:
    """Route each request and report the specialist that produced the answer."""
    print("=== Routing ===")
    for request in REQUESTS:
        result = Runner.run_sync(triage_agent, request)
        print(f"\nRequest:    {request}")
        print(f"Handled by: {result.last_agent.name}")
        print(f"Answer:     {result.final_output[:200]}")


def show_guardrail() -> None:
    """An out-of-scope request must be refused before any specialist runs."""
    print("\n\n=== Guardrail ===")
    for request in REQUESTS + [OUT_OF_SCOPE]:
        try:
            result = Runner.run_sync(triage_agent, request)
            print(f"\n{request}\n  -> {result.last_agent.name}")
        except InputGuardrailTripwireTriggered as exc:
            reason = exc.guardrail_result.output.output_info.reasoning
            print(f"\n{request}\n  -> REFUSED: {reason}")


def compare_with_single_agent() -> None:
    """Control case: one agent with every tool, versus the routed team."""
    print("\n\n=== Single agent vs team ===")
    for request in REQUESTS:
        single = Runner.run_sync(kitchen_sink_agent, request)
        team = Runner.run_sync(triage_agent, request)
        print(f"\nRequest: {request}")
        print(f"  single-agent tools used: "
              f"{sum(1 for i in single.new_items if 'ToolCall' in type(i).__name__)}")
        print(f"  team specialist:         {team.last_agent.name}")


def main() -> None:
    """Run all three demonstrations in order."""
    show_routing()
    show_guardrail()
    compare_with_single_agent()


if __name__ == "__main__":
    main()
