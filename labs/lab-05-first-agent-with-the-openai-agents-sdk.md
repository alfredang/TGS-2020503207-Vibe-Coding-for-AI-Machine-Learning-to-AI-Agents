# Lab 05 — First Agent with the OpenAI Agents SDK

**Topic:** 3 — Multi-Agent System Development with OpenAI Agents SDK  |  **Objective:** Design an agent with the OpenAI Agents SDK using structured outputs and function tools

## Goal

Rebuild the hand-rolled agent from Lab 1 on the OpenAI Agents SDK and see how much the framework removes. Add a Pydantic output type so the agent returns validated typed data instead of prose, and expose your own Python functions as tools.

## What you'll build

An SDK-based agent that calls your function tools and returns a validated Pydantic object your code can use directly.

**Tools:** Python 3.11+, openai-agents SDK, Pydantic, .env

## Prerequisites

- Lab 01 completed — you will compare directly against the hand-rolled loop.
- Python 3.11+ and an activated virtual environment.
- `OPENAI_API_KEY` in `.env`.
- Familiarity with Python type hints and decorators.

## Step-by-step

### 1. Install the Agents SDK and Pydantic into your virtual environment

```bash
mkdir lab-05-agents-sdk && cd lab-05-agents-sdk
uv venv && source .venv/bin/activate
uv pip install openai-agents pydantic python-dotenv requests
```

Note the naming: the PyPI package is **`openai-agents`** but you import from **`agents`**. This trips people up constantly.

```bash
echo 'OPENAI_API_KEY=sk-...' > .env
echo -e '.env\n__pycache__/\n.venv' > .gitignore
```

### 2. Create an Agent and run it with Runner.run_sync

Create `sdk_agent.py`. Compare this against the roughly 90 lines of loop code you wrote in Lab 01 — the SDK's `Runner` handles the entire reason-act-observe cycle, the turn cap and the tool-result plumbing:

```python
"""A first agent on the OpenAI Agents SDK."""

from dotenv import load_dotenv
from agents import Agent, Runner

load_dotenv()

agent = Agent(
    name="Assistant",
    instructions=(
        "You are a concise research assistant. Use the tools available to you "
        "rather than guessing, and state clearly when you do not know something."
    ),
    model="gpt-4o-mini",
)

if __name__ == "__main__":
    result = Runner.run_sync(agent, "What are three benefits of unit testing?")
    print(result.final_output)
```

```bash
python sdk_agent.py
```

`Runner.run_sync` is the blocking convenience wrapper. In an async application — including the Streamlit app in Lab 07 — use `await Runner.run(agent, "...")` instead. There is also `Runner.run_streamed(...)` for token-by-token output.

### 3. Define a Pydantic BaseModel and set it as the agent's output_type

Prose is hard for code to consume. An `output_type` forces the model to return validated, typed data:

```python
from pydantic import BaseModel, Field


class ResearchBrief(BaseModel):
    """The structured answer shape the agent must return."""

    topic: str = Field(description="The subject of the question, in a few words.")
    summary: str = Field(description="A two-sentence answer.")
    key_points: list[str] = Field(description="Between three and five key points.")
    confidence: float = Field(
        ge=0.0, le=1.0, description="Confidence in the answer, from 0 to 1."
    )


agent = Agent(
    name="Research Assistant",
    instructions=(
        "You are a concise research assistant. Use the tools available to you "
        "rather than guessing. Always populate every field of the output."
    ),
    model="gpt-4o-mini",
    output_type=ResearchBrief,
)

if __name__ == "__main__":
    result = Runner.run_sync(agent, "What are the benefits of unit testing?")
    brief: ResearchBrief = result.final_output

    print(f"Topic:      {brief.topic}")
    print(f"Summary:    {brief.summary}")
    print(f"Confidence: {brief.confidence:.2f}")
    for point in brief.key_points:
        print(f"  - {point}")
```

`result.final_output` is now a real `ResearchBrief` instance, so `brief.confidence` is a `float` you can compare against a threshold. The `Field(description=...)` text is sent to the model, so it is worth writing properly.

### 4. Decorate a Python function with @function_tool

The docstring and type hints become the schema the model sees — you no longer hand-write the JSON you wrote in Lab 01:

```python
from agents import function_tool


@function_tool
def calculate(expression: str) -> str:
    """Evaluate an arithmetic expression such as '0.15 * 2400'.

    Use this for any arithmetic instead of computing the answer yourself.

    Args:
        expression: An arithmetic expression using digits and + - * / ( ) only.
    """
    allowed = set("0123456789.+-*/() ")
    if not set(expression) <= allowed:
        return "Error: expression contains unsupported characters."
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as exc:
        return f"Error: could not evaluate '{expression}': {exc}"
```

Attach it to the agent with `tools=[calculate]`.

### 5. Add a second tool that calls a real public API

So the agent works with live data rather than the stub from Lab 01. This uses the Open-Meteo forecast API, which needs no key:

```python
import requests


@function_tool
def get_weather(latitude: float, longitude: float) -> str:
    """Get the current temperature and wind speed for a location.

    Use this whenever the user asks about current weather conditions.

    Args:
        latitude: Latitude in decimal degrees, e.g. 1.29 for Singapore.
        longitude: Longitude in decimal degrees, e.g. 103.85 for Singapore.
    """
    try:
        response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,wind_speed_10m",
            },
            timeout=10,
        )
        response.raise_for_status()
        current = response.json()["current"]
    except requests.RequestException as exc:
        return f"Error: weather service unavailable ({exc})."
    except (KeyError, ValueError) as exc:
        return f"Error: unexpected response from weather service ({exc})."

    return (
        f"Temperature {current['temperature_2m']}degC, "
        f"wind {current['wind_speed_10m']} km/h."
    )


agent = Agent(
    name="Research Assistant",
    instructions=(
        "You are a concise research assistant. Use the tools available to you "
        "rather than guessing. Always populate every field of the output."
    ),
    model="gpt-4o-mini",
    tools=[calculate, get_weather],
    output_type=ResearchBrief,
)
```

### 6. Inspect the run result

The result object carries more than the final output — you can see which tools ran and in what order:

```python
from agents import Runner

if __name__ == "__main__":
    result = Runner.run_sync(
        agent,
        "What is the current weather in Singapore (1.29, 103.85), "
        "and what is 15% of 2400?",
    )

    brief: ResearchBrief = result.final_output
    print(f"Summary:    {brief.summary}")
    print(f"Confidence: {brief.confidence:.2f}")

    print("\n--- Run trace ---")
    for item in result.new_items:
        print(f"  {type(item).__name__}")

    print(f"\nLast agent: {result.last_agent.name}")
```

Runs are also traced automatically. Open <https://platform.openai.com/traces> to see the full timeline of model calls and tool invocations for the run you just executed — this becomes far more valuable in Lab 06 when several agents are involved.

### 7. Handle the failure path

A tool that raises should not crash the run. There are two layers of defence, and you want both.

First, return an error string rather than raising, as `get_weather` above does — the model reads the message and can retry with different arguments or tell the user.

Second, for exceptions you did not anticipate, supply a failure handler so the SDK converts them into a message for the model instead of propagating:

```python
from agents import function_tool


def tool_error(context, error: Exception) -> str:
    """Convert an unhandled tool exception into a message the model can read."""
    return f"The tool failed: {error}. Tell the user this data is unavailable."


@function_tool(failure_error_function=tool_error)
def lookup_population(city: str) -> str:
    """Get the population of a city. Raises if the city is unknown.

    Args:
        city: The city name.
    """
    populations = {"singapore": 5_920_000, "london": 8_900_000}
    return str(populations[city.strip().lower()])  # KeyError on unknown city
```

Test it deliberately:

```python
result = Runner.run_sync(agent, "What is the population of Atlantis?")
print(result.final_output.summary)
```

The run completes and reports the data is unavailable, rather than terminating with a `KeyError`.

## Test it

Verify each of the following:

- [ ] `result.final_output` is an instance of `ResearchBrief` — confirm with `isinstance(result.final_output, ResearchBrief)`.
- [ ] `brief.confidence` is a `float` between 0 and 1, and `brief.key_points` is a `list[str]` with three to five entries.
- [ ] Asking a combined weather-and-arithmetic question triggers both `get_weather` and `calculate`.
- [ ] `get_weather` returns live data that matches the current conditions, not a hard-coded stub.
- [ ] The trace at <https://platform.openai.com/traces> shows the expected tool calls in the expected order.
- [ ] Asking for the population of a non-existent city completes the run with an "unavailable" answer instead of raising `KeyError`.
- [ ] `sdk_agent.py` contains no API key, and `.env` is git-ignored.

## What you learned

- The SDK's `Runner` replaces the entire hand-rolled loop from Lab 01 — the message plumbing, the tool dispatch and the turn cap.
- The package is `openai-agents`, but the import is `from agents import ...`.
- `output_type=MyModel` turns the agent's answer into a validated Pydantic object your code can rely on.
- `@function_tool` derives the schema from type hints and the docstring, so the docstring is production code, not a comment.
- Tools should return error strings for expected failures and use `failure_error_function` for unexpected ones, so a broken tool degrades the answer instead of killing the run.

## References

- OpenAI Agents SDK documentation — <https://openai.github.io/openai-agents-python/>
- Agents — <https://openai.github.io/openai-agents-python/agents/>
- Tools — <https://openai.github.io/openai-agents-python/tools/>
- Running agents — <https://openai.github.io/openai-agents-python/running_agents/>
- Results — <https://openai.github.io/openai-agents-python/results/>
- Pydantic models — <https://docs.pydantic.dev/latest/concepts/models/>
- Open-Meteo API — <https://open-meteo.com/en/docs>
