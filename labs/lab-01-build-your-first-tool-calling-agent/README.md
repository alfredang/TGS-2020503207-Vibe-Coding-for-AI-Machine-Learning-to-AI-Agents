# Lab 01 — Build Your First Tool-Calling Agent

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tertiarycourses/TGS-2020503207-AI-Vibe-Coding-for-Multi-Agents-System/blob/main/labs/lab-01-build-your-first-tool-calling-agent/lab-01-build-your-first-tool-calling-agent.ipynb)

**Topic:** 1 — Modern Agent Foundations  |  **Objective:** Explain the components of a modern AI agent and implement a reasoning loop with tool calling

## Files in this lab

| File | What it is |
|---|---|
| `README.md` | This lab guide. |
| `agent.py` | The finished tool-calling agent: two tools, their JSON schemas, and the reason-act-observe loop. Run with `python agent.py "<question>"`. |
| `lab-01-build-your-first-tool-calling-agent.ipynb` | Colab notebook wrapper — the same code, one cell per step. |

## Goal

Build a single agent from first principles so the loop is not a black box: the model receives a goal, decides to call a tool, your code executes it, and the result is fed back until the agent can answer. You will see every message that crosses the boundary.

## What you'll build

A runnable Python agent that answers questions by calling two of your own tools, printing each reasoning step and tool result so the loop is visible.

**Tools:** Python 3.11+, OpenAI Python SDK, uv/pip, .env for API keys

## Prerequisites

- Python 3.11 or newer installed (`python3 --version`).
- An OpenAI API key from <https://platform.openai.com/api-keys>.
- `uv` installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`) or plain `pip`.
- Basic Python: functions, dictionaries, loops, `try`/`except`.

## Step-by-step

### 1. Create the project folder and a virtual environment, then install the OpenAI SDK and python-dotenv

```bash
mkdir lab-01-agent && cd lab-01-agent
uv venv && source .venv/bin/activate
uv pip install openai python-dotenv
```

On Windows PowerShell the activation line is `.venv\Scripts\activate`. If you prefer pip: `python3 -m venv .venv && source .venv/bin/activate && pip install openai python-dotenv`.

### 2. Store your API key in a .env file (never hard-code a key in source, and never commit .env)

```bash
echo 'OPENAI_API_KEY=sk-...' > .env
echo '.env' >> .gitignore
```

Replace `sk-...` with your real key. The `.gitignore` line is not optional — a key committed to Git is a leaked key, even if you delete it in the next commit.

### 3. Write two plain Python functions the agent may call

Create `agent.py`. These are ordinary Python functions with no AI in them at all — that is the point. The agent decides *when* to call them; your code decides *what they do*.

```python
"""A tool-calling agent built from first principles."""

import json
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-4o-mini"


def get_weather(city: str) -> dict:
    """Return the current weather for a city (stubbed for the lab)."""
    fake_readings = {
        "singapore": {"temp_c": 31, "condition": "Thundery showers", "humidity": 84},
        "london": {"temp_c": 12, "condition": "Overcast", "humidity": 71},
        "tokyo": {"temp_c": 18, "condition": "Clear", "humidity": 55},
    }
    reading = fake_readings.get(city.strip().lower())
    if reading is None:
        return {"error": f"No weather data for '{city}'."}
    return {"city": city, **reading}


def calculate(expression: str) -> dict:
    """Evaluate a simple arithmetic expression such as '0.15 * 2400'."""
    allowed = set("0123456789.+-*/() ")
    if not set(expression) <= allowed:
        return {"error": "Expression contains unsupported characters."}
    try:
        # Safe because the character set above permits arithmetic only.
        result = eval(expression, {"__builtins__": {}}, {})
    except Exception as exc:
        return {"error": f"Could not evaluate: {exc}"}
    return {"expression": expression, "result": result}
```

`get_weather` is stubbed so the lab runs without a second API key. Lab 05 replaces a stub like this with a live API call.

### 4. Describe both functions as JSON tool schemas

The model never sees your Python. It sees only this JSON description, so the `description` fields are what actually drive the routing decision. Vague descriptions produce a confused agent.

```python
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": (
                "Get the current weather for a named city. Use this whenever the "
                "user asks about weather, temperature or conditions."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name, for example 'Singapore'.",
                    }
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": (
                "Evaluate an arithmetic expression. Use this for any calculation "
                "instead of doing the arithmetic yourself."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Arithmetic expression, e.g. '0.15 * 2400'.",
                    }
                },
                "required": ["expression"],
            },
        },
    },
]

# Maps the schema name back to the real Python function.
TOOL_REGISTRY = {
    "get_weather": get_weather,
    "calculate": calculate,
}
```

### 5. Write the agent loop

This is the heart of the lab. Send the messages plus the tool schemas; if the reply contains `tool_calls`, execute each matching function and append the result as a `tool` message; then loop so the model can reason over what it just learned.

```python
def run_agent(user_question: str, max_turns: int = 5) -> str:
    """Run the reason-act-observe loop until the model produces a final answer."""
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant. Use the supplied tools rather than "
                "guessing. When you have everything you need, answer in plain prose."
            ),
        },
        {"role": "user", "content": user_question},
    ]

    for turn in range(1, max_turns + 1):
        print(f"\n--- Turn {turn} ---")
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
        )
        message = response.choices[0].message

        # No tool calls means the agent is ready to answer.
        if not message.tool_calls:
            print("Agent produced a final answer.")
            return message.content

        # Append the assistant turn that requested the tools, then each result.
        messages.append(message)

        for tool_call in message.tool_calls:
            name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"  Tool call: {name}({arguments})")

            function = TOOL_REGISTRY.get(name)
            if function is None:
                result = {"error": f"Unknown tool '{name}'."}
            else:
                try:
                    result = function(**arguments)
                except Exception as exc:
                    result = {"error": f"Tool raised: {exc}"}

            print(f"  Tool result: {result}")
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result),
                }
            )

    return "Stopped: reached the maximum number of turns without a final answer."
```

Note the ordering rule the API enforces: every `tool` message must follow the assistant message that requested it, and must carry the matching `tool_call_id`. Get this wrong and the API returns a 400.

### 6. Cap the loop with a maximum number of turns

The `max_turns` parameter above already does this, and the `for` loop falls through to the "Stopped" message. Without a cap, an agent that keeps re-calling the same tool will spin until it exhausts your credit. Every production agent runtime you will meet in this course — including the OpenAI Agents SDK in Lab 05 — has this same guard built in.

### 7. Run the agent and print each step

Add the entry point:

```python
if __name__ == "__main__":
    question = sys.argv[1] if len(sys.argv) > 1 else "What is the weather in Singapore?"
    answer = run_agent(question)
    print("\n=== Final answer ===")
    print(answer)
```

Then run it:

```bash
python agent.py "What is the weather in Singapore, and what is 15% of 2400?"
```

You should see two turns: the first requesting both tools, the second producing prose.

## Test it

Verify each of the following:

- [ ] The agent answers **both** parts of the question in a single run.
- [ ] The printed trace shows `get_weather` called exactly once.
- [ ] The printed trace shows `calculate` called exactly once.
- [ ] The final answer arrives before the turn cap is reached.
- [ ] Asking about an unknown city returns the tool's error dictionary and the agent reports it rather than crashing.
- [ ] `git status` does not list `.env` as a file to be committed.

## What you learned

- An agent is a loop, not a single call: the model reasons, requests an action, observes the result, and reasons again.
- The tool *description* is the routing signal — the model picks tools from the JSON schema, never from your Python source.
- Tool results re-enter the conversation as `tool` messages tied to a `tool_call_id`, which is what lets the model reason over what it just learned.
- A turn cap is a safety requirement, not a nicety.
- Secrets belong in `.env` and `.env` belongs in `.gitignore`.

## References

- OpenAI function calling guide — <https://platform.openai.com/docs/guides/function-calling>
- OpenAI Python SDK — <https://github.com/openai/openai-python>
- Chat Completions API reference — <https://platform.openai.com/docs/api-reference/chat>
- python-dotenv — <https://pypi.org/project/python-dotenv/>
- uv package manager — <https://docs.astral.sh/uv/>
