# Lab 02 — Agent Memory and Reusable Agent Skills

**Topic:** 1 — Modern Agent Foundations  |  **Objective:** Implement short-term and long-term agent memory, and package a capability as a reusable skill

## Goal

Give the agent memory so it stops forgetting between turns, then extract a repeatable procedure into a skill file the agent loads on demand — the modular, transferable capability described in the course outline.

## What you'll build

An agent with a conversation buffer plus a persistent JSON memory store, and one reusable skill file that the agent loads only when the task calls for it.

**Tools:** Python, OpenAI SDK, JSON file store, Markdown skill definition

## Prerequisites

- Lab 01 completed — you will extend `agent.py` from that lab.
- The same virtual environment, activated, with `openai` and `python-dotenv` installed.
- `OPENAI_API_KEY` set in `.env`.

## Step-by-step

### 1. Add a messages list as short-term memory

In Lab 01 the `messages` list was rebuilt on every call, so the agent forgot everything between questions. Move it outside the function and it becomes a conversation buffer. Create `memory_agent.py`:

```python
"""An agent with short-term (buffer) and long-term (JSON file) memory."""

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-4o-mini"
MEMORY_FILE = Path("memory.json")
SUMMARY_THRESHOLD = 12  # messages before older turns are compacted


class Conversation:
    """Short-term memory: the running message buffer for this session."""

    def __init__(self, system_prompt: str) -> None:
        self.system_prompt = system_prompt
        self.messages: list[dict] = []

    def add(self, message) -> None:
        self.messages.append(message)

    def payload(self) -> list:
        """System prompt is rebuilt each turn so recalled facts stay fresh."""
        return [{"role": "system", "content": self.system_prompt}] + self.messages
```

Because the buffer survives across questions, a follow-up such as *"and what about tomorrow?"* now resolves — the earlier turns are still in the payload.

### 2. Add a long-term store exposed to the agent as tools

Short-term memory dies with the process. Long-term memory is a file the agent can read and write through tools.

```python
def _load_memory() -> dict:
    if MEMORY_FILE.exists():
        try:
            return json.loads(MEMORY_FILE.read_text())
        except json.JSONDecodeError:
            return {}
    return {}


def remember_fact(key: str, value: str) -> dict:
    """Store a durable fact about the user under a short key."""
    facts = _load_memory()
    facts[key] = value
    MEMORY_FILE.write_text(json.dumps(facts, indent=2))
    return {"stored": {key: value}, "total_facts": len(facts)}


def recall_facts() -> dict:
    """Return every durable fact stored about the user."""
    return {"facts": _load_memory()}


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "remember_fact",
            "description": (
                "Store a durable fact about the user, such as a preference, name "
                "or recurring detail. Call this whenever the user states something "
                "worth remembering for future sessions."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {"type": "string", "description": "Short label, e.g. 'home_city'."},
                    "value": {"type": "string", "description": "The fact to remember."},
                },
                "required": ["key", "value"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "recall_facts",
            "description": "Retrieve all durable facts previously stored about the user.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]

TOOL_REGISTRY = {"remember_fact": remember_fact, "recall_facts": recall_facts}
```

Add `memory.json` to `.gitignore` — it holds user data and does not belong in the repository.

```bash
echo 'memory.json' >> .gitignore
```

### 3. Inject the recalled facts into the system prompt at the start of each run

Storing facts is useless if nothing reads them. Build the system prompt from the memory file so recall is automatic rather than something the agent must remember to do.

```python
BASE_PROMPT = (
    "You are a helpful personal assistant. Use the supplied tools rather than "
    "guessing. When the user states a durable preference or detail, call "
    "remember_fact so you still know it in a future session."
)


def build_system_prompt(skill_text: str = "") -> str:
    facts = _load_memory()
    parts = [BASE_PROMPT]
    if facts:
        rendered = "\n".join(f"- {k}: {v}" for k, v in facts.items())
        parts.append(f"Known facts about the user:\n{rendered}")
    if skill_text:
        parts.append(f"Apply the following skill to this task:\n{skill_text}")
    return "\n\n".join(parts)
```

### 4. Summarise older turns once the buffer grows past a threshold

An unbounded buffer grows until it blows the context window and your budget. Compact the old turns into one summary message and keep the recent ones verbatim.

```python
def compact(conversation: Conversation) -> None:
    """Replace older turns with a single summary once the buffer is long."""
    if len(conversation.messages) <= SUMMARY_THRESHOLD:
        return

    keep = conversation.messages[-4:]      # recent turns stay verbatim
    older = conversation.messages[:-4]

    transcript = "\n".join(
        f"{m['role']}: {m.get('content', '')}"
        for m in older
        if isinstance(m, dict) and m.get("content")
    )
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "Summarise this conversation in under 100 words. "
                           "Keep decisions, names and numbers.",
            },
            {"role": "user", "content": transcript},
        ],
    )
    summary = response.choices[0].message.content
    conversation.messages = [
        {"role": "assistant", "content": f"[Summary of earlier conversation] {summary}"}
    ] + keep
```

Now add the run loop, which is Lab 01's loop plus the memory pieces:

```python
def run_turn(conversation: Conversation, user_input: str, max_turns: int = 5) -> str:
    conversation.add({"role": "user", "content": user_input})

    for _ in range(max_turns):
        response = client.chat.completions.create(
            model=MODEL,
            messages=conversation.payload(),
            tools=TOOLS,
        )
        message = response.choices[0].message

        if not message.tool_calls:
            conversation.add({"role": "assistant", "content": message.content})
            compact(conversation)
            return message.content

        conversation.add(message)
        for tool_call in message.tool_calls:
            name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"  Tool call: {name}({arguments})")
            try:
                result = TOOL_REGISTRY[name](**arguments)
            except Exception as exc:
                result = {"error": str(exc)}
            conversation.add(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result),
                }
            )

    return "Stopped: reached the maximum number of turns."
```

### 5. Write a skill as a Markdown file

A skill is a named, described procedure the agent follows. Create `skills/trip-briefing.md`:

```markdown
---
name: trip-briefing
description: Use when the user asks for a travel or trip briefing for a city.
---

# Trip Briefing

Produce a briefing in exactly this structure:

1. **Weather** — current conditions and what to pack.
2. **Getting around** — the main public transport option.
3. **One local tip** — something a first-time visitor would miss.

Rules:
- Keep each section to two sentences or fewer.
- Call recall_facts first; if the user has a stored home_city, note the
  time-zone difference from it.
- If you do not know something, say so rather than inventing it.
```

The front matter matters: `name` identifies the skill and `description` is what your loader matches on. This is the same shape used by the coding-agent skills in Lab 04.

### 6. Load the skill only when the request matches its description

Loading every skill on every request defeats the purpose — the point is to spend context only on what the task needs.

```python
import re

SKILLS_DIR = Path("skills")


def load_skills() -> list[dict]:
    """Read each skill file into {name, description, body}."""
    skills = []
    for path in sorted(SKILLS_DIR.glob("*.md")):
        text = path.read_text()
        match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
        if not match:
            continue
        front, body = match.groups()
        meta = {}
        for line in front.splitlines():
            if ":" in line:
                key, _, value = line.partition(":")
                meta[key.strip()] = value.strip()
        skills.append(
            {
                "name": meta.get("name", path.stem),
                "description": meta.get("description", ""),
                "body": body.strip(),
            }
        )
    return skills


def select_skill(user_input: str, skills: list[dict]) -> dict | None:
    """Ask the model which skill applies, if any."""
    if not skills:
        return None
    catalogue = "\n".join(f"- {s['name']}: {s['description']}" for s in skills)
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Choose the single most applicable skill for the user's request. "
                    f"Available skills:\n{catalogue}\n\n"
                    "Reply with the skill name only, or 'none'."
                ),
            },
            {"role": "user", "content": user_input},
        ],
    )
    choice = response.choices[0].message.content.strip().lower()
    return next((s for s in skills if s["name"].lower() == choice), None)


if __name__ == "__main__":
    skills = load_skills()
    conversation = Conversation(build_system_prompt())

    print("Memory agent ready. Type 'exit' to quit.\n")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            break

        skill = select_skill(user_input, skills)
        if skill:
            print(f"  [skill loaded: {skill['name']}]")
        conversation.system_prompt = build_system_prompt(skill["body"] if skill else "")

        print("Agent:", run_turn(conversation, user_input), "\n")
```

Run it and compare a trip request with and without the skill file present:

```bash
python memory_agent.py
```

## Test it

Verify each of the following:

- [ ] Tell the agent a fact ("I live in Singapore"); it calls `remember_fact` and `memory.json` appears on disk containing that fact.
- [ ] Exit the process, restart it, and ask "where do I live?" — the agent recalls the fact from `memory.json` without being told again.
- [ ] A follow-up question in the same session ("and what about tomorrow?") resolves correctly against the buffer.
- [ ] After more than 12 messages, the buffer is replaced by a summary message plus the last four turns.
- [ ] Asking for a trip briefing loads `trip-briefing` and the reply follows the documented three-section structure rather than improvising.
- [ ] `git status` lists neither `.env` nor `memory.json`.

## What you learned

- Short-term memory is the message buffer; long-term memory is durable storage the agent reaches through tools.
- Stored facts only influence behaviour if something injects them into the system prompt each run.
- Summarising older turns keeps context small and cost predictable as conversations grow.
- A skill is a named, described procedure — the description drives selection, the body drives behaviour.
- Loading skills on demand keeps the context focused; loading everything always is the anti-pattern.

## References

- OpenAI function calling guide — <https://platform.openai.com/docs/guides/function-calling>
- Agent Skills overview (Anthropic) — <https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview>
- Managing context for agents — <https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>
- Python `json` module — <https://docs.python.org/3/library/json.html>
- Python `pathlib` module — <https://docs.python.org/3/library/pathlib.html>
