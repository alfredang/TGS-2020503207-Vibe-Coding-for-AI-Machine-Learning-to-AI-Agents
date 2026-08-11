# SPEC — Research Assistant Agent

## Goal
A command-line agent that answers a research question by searching a local
document collection and citing which documents it used.

## Inputs
- `python research_agent.py "<question>"` — the question as one CLI argument.
- `documents/` — a folder of `.txt` files forming the searchable collection.

## Outputs
- A prose answer to stdout, under 200 words.
- A "Sources:" line listing the filenames actually used.
- Exit code 0 on success, 1 on any error.

## Constraints
- Python 3.11+, standard library plus `openai` and `python-dotenv` only.
- No web access — the agent may only read files under `documents/`.
- The API key is read from `OPENAI_API_KEY` via python-dotenv. Never hard-coded.
- The agent loop is capped at 5 turns.
- If no document is relevant, say so explicitly rather than inventing an answer.

## Acceptance test
Given `documents/mrt.txt` containing "The Thomson-East Coast Line opened in 2020":

    python research_agent.py "When did the Thomson-East Coast Line open?"

MUST print an answer containing "2020" and a "Sources:" line naming `mrt.txt`.

Given a question with no relevant document:

    python research_agent.py "What is the capital of Peru?"

MUST state that no relevant document was found, and MUST NOT answer "Lima".
