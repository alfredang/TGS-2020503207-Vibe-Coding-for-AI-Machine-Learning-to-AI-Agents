"""Lab 02 - Agent Memory and Reusable Agent Skills.

An agent with short-term memory (a conversation buffer that is compacted once it
grows past a threshold) and long-term memory (a JSON file the agent reads and
writes through tools). It also loads a reusable skill from skills/*.md, but only
when the request matches that skill's description.

Run:
    python memory_agent.py

Requires OPENAI_API_KEY in a .env file (never hard-code a key in source).
memory.json is written next to this script and must stay out of Git.
"""

import json
import os
import re
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-4o-mini"
MEMORY_FILE = Path("memory.json")
SKILLS_DIR = Path("skills")
SUMMARY_THRESHOLD = 12  # messages before older turns are compacted


# --- short-term memory -----------------------------------------------------


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


# --- long-term memory, exposed to the agent as tools -----------------------


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


# --- injecting recalled facts into the system prompt -----------------------

BASE_PROMPT = (
    "You are a helpful personal assistant. Use the supplied tools rather than "
    "guessing. When the user states a durable preference or detail, call "
    "remember_fact so you still know it in a future session."
)


def build_system_prompt(skill_text: str = "") -> str:
    """Rebuild the system prompt from stored facts plus any selected skill."""
    facts = _load_memory()
    parts = [BASE_PROMPT]
    if facts:
        rendered = "\n".join(f"- {k}: {v}" for k, v in facts.items())
        parts.append(f"Known facts about the user:\n{rendered}")
    if skill_text:
        parts.append(f"Apply the following skill to this task:\n{skill_text}")
    return "\n\n".join(parts)


# --- compaction ------------------------------------------------------------


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


# --- the run loop (Lab 01's loop plus the memory pieces) -------------------


def run_turn(conversation: Conversation, user_input: str, max_turns: int = 5) -> str:
    """Run one user turn to completion, executing any tools the model requests."""
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


# --- skills: load on demand, not always ------------------------------------


def load_skills() -> list[dict]:
    """Read each skill file into {name, description, body}."""
    skills = []
    if not SKILLS_DIR.exists():
        return skills
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


def main() -> None:
    """Interactive REPL: memory persists across runs, skills load on demand."""
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


if __name__ == "__main__":
    main()
