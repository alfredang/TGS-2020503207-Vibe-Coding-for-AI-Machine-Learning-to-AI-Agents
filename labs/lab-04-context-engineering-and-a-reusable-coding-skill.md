# Lab 04 — Context Engineering and a Reusable Coding Skill

**Topic:** 2 — Vibe Coding for Multi-Agent Systems  |  **Objective:** Engineer the agent's context and package a repeatable procedure as a project skill

## Goal

Improve reliability by controlling exactly what the coding agent sees, then capture your house conventions as a skill so the agent applies them automatically instead of you re-explaining them in every session.

## What you'll build

A project configured with a context file and a reusable skill, demonstrably producing house-standard code without repeated instructions.

**Tools:** Claude Code / Gemini CLI, Markdown, Git

## Prerequisites

- Lab 03 completed — you will work inside that same `lab-03-research-agent` project, which already has Git history and a working agent.
- Your vibe coding tool installed and authenticated (Claude Code or Gemini CLI).
- A clean working tree (`git status` shows nothing to commit) so each experiment produces a readable diff.

## Step-by-step

### 1. Take a deliberately vague prompt and note the weaknesses — this is your baseline

Start a fresh session in the Lab 03 project with **no** context file present, and give the agent an underspecified request:

> Add a tool that fetches a stock price.

Let it generate, then record what is wrong. You will typically see several of these:

- The wrong file, or a brand-new file that duplicates existing structure.
- A different naming convention from the rest of the project (`fetchStockPrice` vs `fetch_stock_price`).
- No type hints or docstring, so the tool schema the model sees is uninformative.
- A hard-coded API key or URL.
- No error handling on the network call.
- No registration in the existing tool list, so the tool is never actually callable.

Save this as your baseline, then discard the code so the comparison in step 3 is fair:

```bash
git diff > /tmp/baseline-no-context.diff
git checkout . && git clean -fd
```

### 2. Create a project context file stating the stack, conventions, folder layout and prohibitions

The context file is read automatically at the start of every session — `CLAUDE.md` for Claude Code, `GEMINI.md` for Gemini CLI. Create it at the project root:

```markdown
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
```

Commit it so the improvement is attributable:

```bash
git add CLAUDE.md && git commit -m "Add project context file"
```

### 3. Re-run the same vague prompt and compare against the baseline

Start a **new** session so the context file is loaded fresh, and give the identical prompt:

> Add a tool that fetches a stock price.

Compare the result against `/tmp/baseline-no-context.diff`. With the context file in place the same eight words typically now produce: the right file, `snake_case`, type hints and a docstring, `os.getenv` for configuration, an `{"error": ...}` path, and registration in the existing tool list — and a question about the new dependency, because the context file said to ask.

Nothing about the prompt changed. Only the context did. That is the point of the lab.

### 4. Write a skill file capturing a repeatable procedure

A context file states *what is true about the project*. A skill states *how to perform a specific procedure*. Create `.claude/skills/add-agent-tool/SKILL.md`:

```markdown
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
```

Gemini CLI users: place the same content at `.gemini/skills/add-agent-tool/SKILL.md`, or paste it into `GEMINI.md` under a clearly labelled heading.

### 5. Reference precise files and line ranges instead of pasting whole files

Context is a budget. Spending it on 400 lines the agent does not need makes it *less* reliable, not more — the relevant lines get diluted. Compare:

Wasteful — pastes the whole file:

> Here is my entire research_agent.py [400 lines pasted]. Add a currency conversion tool.

Precise — points at exactly the two places that matter:

> Add a currency conversion tool. Follow the same pattern as `search_documents`
> at `research_agent.py:34-58`, and register it in the `TOOLS` list at
> `research_agent.py:70-95`. Use the add-agent-tool skill.

The agent reads only what it needs. Find the line numbers quickly with:

```bash
grep -n "def search_documents\|^TOOLS\|^TOOL_REGISTRY" research_agent.py
```

### 6. Ask the agent to perform the procedure and confirm it follows the skill

Invoke the skill explicitly and check it against the skill's own quality checklist:

> Use the add-agent-tool skill to add `word_count(filename)`, which returns
> the number of words in a document under `documents/`.

Then verify the generated code satisfies every box in the skill's quality-checks list, and confirm the agent actually ran step 6 — it should have executed the acceptance test rather than merely claiming the tool works.

```bash
git diff
python research_agent.py "How many words are in mrt.txt?"
python research_agent.py "When did the Thomson-East Coast Line open?"
```

The second command re-runs the original acceptance test, confirming the new tool did not regress the existing behaviour.

## Test it

Verify each of the following:

- [ ] You have a recorded baseline of what the vague prompt produced **without** the context file.
- [ ] The identical prompt **with** the context file produces code matching your stated conventions, without you restating them.
- [ ] The generated code uses `snake_case`, type hints, a docstring, and `os.getenv` — none of which were mentioned in the prompt.
- [ ] The agent asked before adding a new dependency, as the context file requires.
- [ ] Invoking the `add-agent-tool` skill produces a tool that satisfies every item in the skill's quality checklist.
- [ ] The agent ran the acceptance test as part of the procedure rather than only asserting the tool works.
- [ ] `git grep -i "sk-"` still returns nothing.

## What you learned

- Context engineering moves reliability more than prompt wording — the same prompt produces different quality depending on what the agent can see.
- A context file (`CLAUDE.md` / `GEMINI.md`) encodes what is permanently true about the project, including explicit prohibitions.
- A skill encodes a repeatable procedure with its own quality checks, so consistency does not depend on you remembering to ask.
- Precise file and line references beat pasting whole files: context is a budget, and dilution costs accuracy.
- Baseline-then-compare is how you demonstrate a context improvement rather than assume it.

## References

- Manage Claude's memory (CLAUDE.md) — <https://docs.claude.com/en/docs/claude-code/memory>
- Agent Skills — <https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview>
- Effective context engineering for AI agents — <https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>
- Gemini CLI configuration — <https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/configuration.md>
- Claude Code best practices — <https://www.anthropic.com/engineering/claude-code-best-practices>
