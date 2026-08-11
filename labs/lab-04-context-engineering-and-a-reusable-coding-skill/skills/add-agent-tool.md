---
name: add-agent-tool
description: >
  Use when adding a new tool/function to the research agent. Covers the
  function, its JSON schema, registration and the verification step.
---

# Add an agent tool

Follow these steps in order. Do not skip the verification step.

## Steps

1. Write the Python function in `research_agent.py`, below the existing
   tool functions. Full type hints, one-line docstring stating *when* the
   agent should call it.
2. Return a JSON-serialisable `dict`. Catch exceptions and return
   `{"error": "<short reason>"}` — never let a tool raise into the loop.
3. Read any configuration from `os.getenv`, with a sensible default. Never
   hard-code a value that differs between machines.
4. Add the JSON schema to the `TOOLS` list. The `description` must say when
   to call the tool, not merely what it does — this is the routing signal.
5. Register the function in `TOOL_REGISTRY` under exactly the schema `name`.
6. Verify: run the acceptance test in `SPEC.md`, then run one question that
   should trigger the new tool and confirm from the trace that it fired.

## Quality checks

- [ ] Type hints on every parameter and the return value.
- [ ] Docstring says *when* to call, not just what it does.
- [ ] Failure path returns `{"error": ...}` rather than raising.
- [ ] Schema `name`, `TOOL_REGISTRY` key and function name all match.
- [ ] Existing acceptance test still passes.
