# Lab 08 — Build a Multi-Agent System with the Gemini Agent SDK

**Topic:** 4 — Multi-Agent System Development with Gemini Agent SDK  |  **Objective:** Design collaborative agents with the Google Gemini Agent SDK (ADK)

## Goal

Express the same multi-agent pattern in Google's ecosystem. Building the equivalent system twice separates the portable concepts — agents, tools, routing — from one vendor's API surface.

## What you'll build

A Gemini-powered coordinator agent with two specialist sub-agents and working function tools.

**Tools:** Python 3.11+, google-adk, Google AI Studio API key

## Prerequisites

- Lab 06 completed — you are rebuilding that architecture in a second SDK.
- A Gemini API key from Google AI Studio: <https://aistudio.google.com/apikey>.
- Python 3.11+ with an activated virtual environment.
- Comfort with `async`/`await`, which ADK uses throughout.

## Step-by-step

### 1. Install the Google Agent Development Kit and set your Gemini API key in .env

```bash
mkdir lab-08-adk && cd lab-08-adk
uv venv && source .venv/bin/activate
uv pip install google-adk python-dotenv
```

Create `.env`. The second variable tells ADK to use the AI Studio API rather than Vertex AI — omit it and you will get confusing authentication errors:

```bash
cat > .env <<'EOF'
GOOGLE_API_KEY=your-key-here
GOOGLE_GENAI_USE_VERTEXAI=FALSE
EOF
echo -e '.env\n__pycache__/\n.venv' > .gitignore
```

### 2. Create an Agent with name, model, description and instruction

Create `gemini_team.py`:

```python
"""A Gemini coordinator agent with two specialist sub-agents."""

import asyncio

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

load_dotenv()

MODEL = "gemini-2.0-flash"
APP_NAME = "multi_agent_lab"
USER_ID = "learner-1"

weather_agent = Agent(
    name="weather_agent",
    model=MODEL,
    description="Answers questions about current weather conditions in a city.",
    instruction=(
        "You are a weather specialist. Use the get_weather tool to answer "
        "questions about conditions in a city. If the tool reports an error, "
        "tell the user plainly rather than guessing."
    ),
)
```

The `description` and `instruction` do different jobs, and confusing them is the most common ADK mistake. The **description** is read by a *coordinator* deciding whether to route here — it is the discoverability text. The **instruction** is read by *this agent* when it runs — it is the behaviour text. An agent with a vague description will never be routed to, no matter how good its instruction is.

`name` must be a valid Python identifier: lowercase with underscores, no spaces.

### 3. Write plain Python functions as tools

ADK reads the type hints and docstring to build the schema — no decorator is needed, unlike the OpenAI SDK's `@function_tool`:

```python
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
```

Returning a dict with an explicit `status` key is the ADK convention. It gives the model an unambiguous signal about success or failure instead of making it infer from prose.

Attach the tool:

```python
weather_agent = Agent(
    name="weather_agent",
    model=MODEL,
    description="Answers questions about current weather conditions in a city.",
    instruction=(
        "You are a weather specialist. Use the get_weather tool to answer "
        "questions about conditions in a city. If the tool returns status "
        "'error', relay the error_message to the user rather than guessing."
    ),
    tools=[get_weather],
)
```

### 4. Run the agent with a Runner and an in-memory session service

ADK separates the **runner** (executes the agent loop) from the **session service** (carries conversational state). Both `Runner(...)` and `run_async(...)` take keyword arguments only:

```python
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
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID
    )
    runner = Runner(
        agent=weather_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    answer, author = await ask(runner, session.id, "What is the weather in Singapore?")
    print(f"[{author}] {answer}")


if __name__ == "__main__":
    asyncio.run(main())
```

```bash
python gemini_team.py
```

Three details worth noting: the user message must be wrapped in a `types.Content`, `create_session` is a coroutine so it needs `await`, and `run_async` is an async generator you consume with `async for`.

### 5. Create two specialist sub-agents with distinct descriptions and non-overlapping tools

Add a second tool and a second specialist. Non-overlapping tools are what keep routing decisions unambiguous:

```python
def get_time(city: str) -> dict:
    """Return the current local time in a specified city.

    Args:
        city: The name of the city, for example "Singapore".

    Returns:
        A dict with a 'status' key and either a 'report' or 'error_message'.
    """
    from datetime import datetime
    from zoneinfo import ZoneInfo

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


time_agent = Agent(
    name="time_agent",
    model=MODEL,
    description="Answers questions about the current local time in a city.",
    instruction=(
        "You are a timekeeping specialist. Use the get_time tool to report the "
        "local time in a city. If the tool returns status 'error', relay the "
        "error_message rather than guessing."
    ),
    tools=[get_time],
)
```

### 6. Attach them to a coordinator agent via sub_agents

The coordinator holds no tools of its own — its job is routing, exactly like the triage agent in Lab 06:

```python
coordinator = Agent(
    name="coordinator",
    model=MODEL,
    description="Routes user requests to the correct specialist sub-agent.",
    instruction=(
        "You are a coordinator. You do not answer questions yourself. "
        "Delegate weather questions to weather_agent and time questions to "
        "time_agent. If a request covers both, handle them in turn. "
        "If neither applies, say the request is outside your scope."
    ),
    sub_agents=[weather_agent, time_agent],
)
```

ADK routes by matching the request against each sub-agent's `description`, which is why step 2 stressed that field. In `main()`, point the runner at the coordinator instead of the single agent:

```python
# In main(), replacing the earlier `agent=weather_agent` runner:
runner = Runner(
    agent=coordinator,
    app_name=APP_NAME,
    session_service=session_service,
)
```

An agent instance may have only one parent, so do not attach the same sub-agent object to two coordinators.

### 7. Run requests that should reach different specialists and confirm the routing

`event.author` carries the name of the agent that produced the response, which is the ADK equivalent of `result.last_agent.name`:

```python
async def main() -> None:
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID
    )
    runner = Runner(
        agent=coordinator,
        app_name=APP_NAME,
        session_service=session_service,
    )

    questions = [
        "What is the weather in Singapore?",
        "What time is it in Tokyo?",
        "What is the weather on Mars?",
    ]
    for question in questions:
        answer, author = await ask(runner, session.id, question)
        print(f"\nQ: {question}")
        print(f"   handled by: {author}")
        print(f"   {answer}")


if __name__ == "__main__":
    asyncio.run(main())
```

```bash
python gemini_team.py
```

Expect `weather_agent`, then `time_agent`, then a graceful error for Mars. Because all three questions share one `session.id`, the session service carries context between them — try a follow-up such as "and what time is it there?" to confirm.

ADK also ships a web inspector that visualises the routing. Run it from the parent folder of your agent package:

```bash
adk web
```

### 8. Note the API differences from the OpenAI SDK while the architecture stays identical

Record this comparison — you will extend it in Lab 09 and it is assessable material:

| Concept | OpenAI Agents SDK | Google ADK |
|---|---|---|
| Package / import | `openai-agents` / `from agents import ...` | `google-adk` / `from google.adk.agents import ...` |
| Define an agent | `Agent(name, instructions, model, tools)` | `Agent(name, model, description, instruction, tools)` |
| Declare a tool | `@function_tool` decorator | Plain function; schema from hints + docstring |
| Compose a team | `handoffs=[...]` | `sub_agents=[...]` |
| Routing signal | `handoff_description` | `description` |
| Execute | `Runner.run_sync(agent, "text")` | `runner.run_async(user_id=..., session_id=..., new_message=Content)` |
| Conversation state | Input list you pass in | `SessionService` holds it |
| Who answered | `result.last_agent.name` | `event.author` |
| Structured output | `output_type=PydanticModel` | `output_schema=PydanticModel` |

The architecture — a routing coordinator over narrow specialists with non-overlapping tools — is identical. Only the API surface changes, which is precisely the portable-concepts point of building it twice.

## Test it

Verify each of the following:

- [ ] "What is the weather in Singapore?" is handled by `weather_agent` — confirm via `event.author`.
- [ ] "What time is it in Tokyo?" is handled by `time_agent`.
- [ ] The tools return live computed results (the time really is the current Tokyo time), not fixed strings.
- [ ] An unknown city returns the `status: error` dict and the agent relays the message instead of inventing weather.
- [ ] A follow-up question in the same session resolves using earlier context, proving the session service is carrying state.
- [ ] The routing behaviour matches your Lab 06 OpenAI build for equivalent requests.
- [ ] `.env` is git-ignored and no key appears in the source.

## What you learned

- In ADK, `description` drives routing (discoverability) and `instruction` drives behaviour — conflating them breaks delegation.
- ADK tools are plain Python functions; the type hints and docstring generate the schema, and a `status` key makes success and failure unambiguous.
- The runner executes the loop while the session service carries conversational state — a cleaner separation than the OpenAI SDK's input list.
- `Runner(...)` and `run_async(...)` are keyword-only, and messages must be wrapped in `types.Content`.
- `sub_agents` on a coordinator is ADK's expression of the same supervisor-routing pattern as `handoffs`.
- The multi-agent architecture is portable across ecosystems; only the API surface differs.

## References

- Google ADK documentation — <https://google.github.io/adk-docs/>
- ADK quickstart — <https://google.github.io/adk-docs/get-started/quickstart/>
- Defining agents — <https://google.github.io/adk-docs/agents/llm-agents/>
- Function tools — <https://google.github.io/adk-docs/tools/function-tools/>
- Multi-agent systems — <https://google.github.io/adk-docs/agents/multi-agents/>
- Sessions and runners — <https://google.github.io/adk-docs/sessions/session/>
- Google AI Studio (API keys) — <https://aistudio.google.com/apikey>
