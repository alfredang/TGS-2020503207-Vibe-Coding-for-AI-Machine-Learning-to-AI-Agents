"""Lab 08 - Build a Multi-Agent System with the Gemini Agent SDK (ADK).

The same architecture as Lab 06, expressed in Google's ecosystem: a coordinator
agent that holds no tools of its own routing to two specialist sub-agents via
`sub_agents`. ADK tools are plain Python functions - the type hints and
docstring generate the schema, no decorator needed.

The agents are built by a `build_coordinator(model)` factory rather than at
module level, because an ADK agent instance may have only one parent. Lab 09
imports this factory so it can rebuild the team when the model is switched.

Run:
    python gemini_team.py

Requires GOOGLE_API_KEY and GOOGLE_GENAI_USE_VERTEXAI=FALSE in a .env file.
Omit the second variable and ADK will try Vertex AI, producing confusing
authentication errors. Never hard-code a key in source.
"""

import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

load_dotenv()

MODEL = "gemini-2.0-flash"
APP_NAME = "multi_agent_lab"
USER_ID = "learner-1"


# --- tools -----------------------------------------------------------------
# Returning a dict with an explicit `status` key is the ADK convention: it gives
# the model an unambiguous success/failure signal instead of inferred prose.


def get_weather(city: str) -> dict:
    """Retrieve the current weather report for a specified city.

    Args:
        city: The name of the city, for example "Singapore".

    Returns:
        A dict with a 'status' key and either a 'report' or 'error_message'.
    """
    readings = {
        "singapore": "31degC with thundery showers and 84% humidity.",
        "london": "12degC and overcast.",
        "tokyo": "18degC and clear.",
    }
    report = readings.get(city.strip().lower())
    if report is None:
        return {
            "status": "error",
            "error_message": f"No weather data available for '{city}'.",
        }
    return {"status": "success", "report": f"The weather in {city} is {report}"}


def get_time(city: str) -> dict:
    """Return the current local time in a specified city.

    Args:
        city: The name of the city, for example "Singapore".

    Returns:
        A dict with a 'status' key and either a 'report' or 'error_message'.
    """
    zones = {
        "singapore": "Asia/Singapore",
        "london": "Europe/London",
        "tokyo": "Asia/Tokyo",
    }
    zone = zones.get(city.strip().lower())
    if zone is None:
        return {
            "status": "error",
            "error_message": f"No timezone information for '{city}'.",
        }
    now = datetime.now(ZoneInfo(zone))
    return {
        "status": "success",
        "report": f"The current time in {city} is {now:%Y-%m-%d %H:%M:%S %Z}.",
    }


# --- agents ----------------------------------------------------------------
# `description` is read by the coordinator when deciding whether to route here
# (discoverability). `instruction` is read by this agent when it runs
# (behaviour). Conflating the two is the most common ADK mistake, and an agent
# with a vague description will never be routed to.
#
# `name` must be a valid Python identifier: lowercase with underscores.


def build_coordinator(model: str = MODEL) -> Agent:
    """Construct the coordinator and its specialists for a given model."""
    weather = Agent(
        name="weather_agent",
        model=model,
        description="Answers questions about current weather conditions in a city.",
        instruction=(
            "You are a weather specialist. Use the get_weather tool to answer "
            "questions about conditions in a city. If the tool returns status "
            "'error', relay the error_message to the user rather than guessing."
        ),
        tools=[get_weather],
    )
    time_specialist = Agent(
        name="time_agent",
        model=model,
        description="Answers questions about the current local time in a city.",
        instruction=(
            "You are a timekeeping specialist. Use the get_time tool to report "
            "the local time in a city. If the tool returns status 'error', "
            "relay the error_message rather than guessing."
        ),
        tools=[get_time],
    )
    return Agent(
        name="coordinator",
        model=model,
        description="Routes user requests to the correct specialist sub-agent.",
        instruction=(
            "You are a coordinator. You do not answer questions yourself. "
            "Delegate weather questions to weather_agent and time questions to "
            "time_agent. If a request covers both, handle them in turn. "
            "If neither applies, say the request is outside your scope."
        ),
        sub_agents=[weather, time_specialist],
    )


# --- running the agent -----------------------------------------------------
# ADK separates the runner (executes the agent loop) from the session service
# (carries conversational state). Runner(...) and run_async(...) are
# keyword-only, and messages must be wrapped in types.Content.


async def ask(runner: Runner, session_id: str, question: str) -> tuple[str, str]:
    """Send one question and return (final_text, responding_agent_name)."""
    message = types.Content(role="user", parts=[types.Part(text=question)])

    final_text, author = "", ""
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session_id,
        new_message=message,
    ):
        if event.is_final_response() and event.content and event.content.parts:
            final_text = event.content.parts[0].text or ""
            author = event.author
    return final_text, author


async def main() -> None:
    """Route three questions through the coordinator and report who answered."""
    session_service = InMemorySessionService()
    # create_session is a coroutine, so it needs await.
    session = await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID
    )
    runner = Runner(
        agent=build_coordinator(MODEL),
        app_name=APP_NAME,
        session_service=session_service,
    )

    questions = [
        "What is the weather in Singapore?",
        "What time is it in Tokyo?",
        "What is the weather on Mars?",
    ]
    # All three share one session.id, so the session service carries context
    # between them - try a follow-up such as "and what time is it there?".
    for question in questions:
        answer, author = await ask(runner, session.id, question)
        print(f"\nQ: {question}")
        print(f"   handled by: {author}")
        print(f"   {answer}")


if __name__ == "__main__":
    asyncio.run(main())
