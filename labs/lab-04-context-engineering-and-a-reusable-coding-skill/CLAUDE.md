# Project context — Research Assistant Agent

## Stack
- Python 3.11+, standard library plus `openai` and `python-dotenv` only.
- No new dependencies without asking first.

## Layout
- `research_agent.py` — the agent loop, tool functions and tool schemas.
- `documents/` — the searchable `.txt` collection. Data only, never code.
- `SPEC.md` — the specification. The acceptance test in it is authoritative.

## Conventions
- `snake_case` for functions and variables; `UPPER_SNAKE` for module constants.
- Every tool function has full type hints and a one-line docstring — these
  become the schema the model sees, so they must describe *when* to call it.
- Every tool returns a JSON-serialisable `dict`. On failure it returns
  `{"error": "..."}` rather than raising.
- Standard library imports first, then third-party, then local. One blank
  line between groups.

## Never do this
- Never hard-code an API key, URL or secret. Read them via `os.getenv`.
- Never edit `SPEC.md` to make a failing test pass.
- Never add a network call other than the OpenAI API — the spec forbids it.
- Never reformat or refactor a file you were not asked to change.
