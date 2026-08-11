"""Lab 01 - Build Your First Tool-Calling Agent.

A tool-calling agent built from first principles: the model receives a goal,
decides to call a tool, this code executes it, and the result is fed back until
the agent can answer. Every message that crosses the boundary is printed.

Run:
    python agent.py "What is the weather in Singapore, and what is 15% of 2400?"

Requires OPENAI_API_KEY in a .env file (never hard-code a key in source).
"""

import json
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-4o-mini"


# --- tools -----------------------------------------------------------------


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


# --- tool schemas ----------------------------------------------------------
# The model never sees the Python above. It sees only this JSON description,
# so the `description` fields are what actually drive the routing decision.

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


# --- the agent loop --------------------------------------------------------


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


def main() -> None:
    """Entry point: take the question from argv, run the loop, print the answer."""
    question = sys.argv[1] if len(sys.argv) > 1 else "What is the weather in Singapore?"
    answer = run_agent(question)
    print("\n=== Final answer ===")
    print(answer)


if __name__ == "__main__":
    main()
