"""Lab 05 - First Agent with the OpenAI Agents SDK.

The hand-rolled loop from Lab 01 rebuilt on the OpenAI Agents SDK: the Runner
handles the whole reason-act-observe cycle, `@function_tool` derives each tool
schema from type hints and the docstring, and `output_type` forces a validated
Pydantic object instead of prose.

Note the naming: the PyPI package is `openai-agents` but you import from `agents`.

Run:
    python sdk_agent.py

Requires OPENAI_API_KEY in a .env file (never hard-code a key in source).
"""

import requests
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from agents import Agent, Runner, function_tool

load_dotenv()

MODEL = "gpt-4o-mini"


# --- structured output -----------------------------------------------------


class ResearchBrief(BaseModel):
    """The structured answer shape the agent must return."""

    topic: str = Field(description="The subject of the question, in a few words.")
    summary: str = Field(description="A two-sentence answer.")
    key_points: list[str] = Field(description="Between three and five key points.")
    confidence: float = Field(
        ge=0.0, le=1.0, description="Confidence in the answer, from 0 to 1."
    )


# --- tools -----------------------------------------------------------------


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


# --- the agent -------------------------------------------------------------

agent = Agent(
    name="Research Assistant",
    instructions=(
        "You are a concise research assistant. Use the tools available to you "
        "rather than guessing. Always populate every field of the output."
    ),
    model=MODEL,
    tools=[calculate, get_weather, lookup_population],
    output_type=ResearchBrief,
)


def print_brief(brief: ResearchBrief) -> None:
    """Print a ResearchBrief field by field, proving it is typed data."""
    print(f"Topic:      {brief.topic}")
    print(f"Summary:    {brief.summary}")
    print(f"Confidence: {brief.confidence:.2f}")
    for point in brief.key_points:
        print(f"  - {point}")


def main() -> None:
    """Run a combined tool question, then deliberately exercise the failure path."""
    result = Runner.run_sync(
        agent,
        "What is the current weather in Singapore (1.29, 103.85), "
        "and what is 15% of 2400?",
    )

    brief: ResearchBrief = result.final_output
    print("=== Structured output ===")
    print_brief(brief)
    print(f"\nisinstance(result.final_output, ResearchBrief): "
          f"{isinstance(result.final_output, ResearchBrief)}")

    # The result object carries more than the final output: you can see which
    # tools ran and in what order. Runs are also traced automatically at
    # https://platform.openai.com/traces
    print("\n=== Run trace ===")
    for item in result.new_items:
        print(f"  {type(item).__name__}")
    print(f"\nLast agent: {result.last_agent.name}")

    # A tool that raises must not crash the run: failure_error_function turns
    # the KeyError into a message the model can report.
    print("\n=== Failure path ===")
    failure = Runner.run_sync(agent, "What is the population of Atlantis?")
    print(failure.final_output.summary)


if __name__ == "__main__":
    main()
