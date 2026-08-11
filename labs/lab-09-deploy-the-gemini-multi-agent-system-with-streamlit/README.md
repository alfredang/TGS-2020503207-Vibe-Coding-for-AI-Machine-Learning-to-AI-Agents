# Lab 09 — Deploy the Gemini Multi-Agent System with Streamlit

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tertiarycourses/TGS-2020503207-AI-Vibe-Coding-for-Multi-Agents-System/blob/main/labs/lab-09-deploy-the-gemini-multi-agent-system-with-streamlit/lab-09-deploy-the-gemini-multi-agent-system-with-streamlit.ipynb)

**Topic:** 4 — Multi-Agent System Development with Gemini Agent SDK  |  **Objective:** Deploy a Gemini-based collaborative multi-agent system with Streamlit

## Files in this lab

| File | What it is |
|---|---|
| `README.md` | This lab guide. |
| `gemini_app.py` | The Streamlit app: ADK runner and session id cached in `st.session_state`, streamed reply, responding sub-agent shown per turn, model switcher and latency metric. Run with `streamlit run gemini_app.py --server.port 8502`. |
| `gemini_team.py` | The Lab 08 Gemini team, copied here so the app runs standalone. Provides `build_coordinator`, `APP_NAME` and `USER_ID`. |
| `COMPARISON.md` | The step-7 SDK comparison template. Fill in every blank from your own runs and keep it as evidence for the practical assessment. |
| `lab-09-deploy-the-gemini-multi-agent-system-with-streamlit.ipynb` | Colab notebook wrapper. It writes the app files via `%%writefile` — Streamlit does not render inside Colab, so you run the app locally. |

## Goal

Give the Gemini agent team the same web interface treatment, then compare the two deployments side by side and record which ecosystem fits which kind of work.

## What you'll build

A deployed Streamlit application backed by the Gemini multi-agent system, plus a short written comparison of the two SDKs.

**Tools:** Python, Streamlit, google-adk

## Prerequisites

- Lab 08 completed, with a working `gemini_team.py` exporting `coordinator` and `ask`.
- Lab 07 completed — you will run both apps side by side to compare them.
- `GOOGLE_API_KEY` and `GOOGLE_GENAI_USE_VERTEXAI=FALSE` in `.env`.
- `streamlit` installed (`uv pip install streamlit`).

## Step-by-step

### 1. Create a Streamlit app that imports your Gemini coordinator agent

Create `gemini_app.py` next to `gemini_team.py`:

```python
"""Streamlit front end for the Lab 08 Gemini multi-agent team."""

import asyncio

import streamlit as st
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from gemini_team import build_coordinator, APP_NAME, USER_ID

load_dotenv()

st.set_page_config(page_title="Gemini Multi-Agent Assistant", page_icon="G")
st.title("Gemini Multi-Agent Assistant")
st.caption("Coordinator routing to weather and time specialists.")
```

Refactor `gemini_team.py` to expose a `build_coordinator(model)` factory rather than a module-level `coordinator` object. You need this for step 5, because switching model variants means rebuilding the agents:

```python
def build_coordinator(model: str = "gemini-2.0-flash") -> Agent:
    """Construct the coordinator and its specialists for a given model."""
    weather = Agent(
        name="weather_agent",
        model=model,
        description="Answers questions about current weather conditions in a city.",
        instruction=(
            "You are a weather specialist. Use the get_weather tool. If it "
            "returns status 'error', relay the error_message rather than guessing."
        ),
        tools=[get_weather],
    )
    time_specialist = Agent(
        name="time_agent",
        model=model,
        description="Answers questions about the current local time in a city.",
        instruction=(
            "You are a timekeeping specialist. Use the get_time tool. If it "
            "returns status 'error', relay the error_message rather than guessing."
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
            "time_agent. If neither applies, say the request is out of scope."
        ),
        sub_agents=[weather, time_specialist],
    )
```

The factory also avoids the "an agent can only have one parent" error you would otherwise hit when rebuilding.

### 2. Manage the ADK session and runner inside st.session_state

Streamlit re-runs the script on every interaction. Creating a fresh ADK session each time would silently reset the conversation, so both the runner and the session id must be cached in `st.session_state`.

Note that `create_session` is async while the Streamlit script is synchronous, so bridge with `asyncio.run`:

```python
def init_backend(model: str) -> None:
    """Create the ADK session service, session and runner once per model."""
    session_service = InMemorySessionService()
    session = asyncio.run(
        session_service.create_session(app_name=APP_NAME, user_id=USER_ID)
    )
    st.session_state.session_id = session.id
    st.session_state.runner = Runner(
        agent=build_coordinator(model),
        app_name=APP_NAME,
        session_service=session_service,
    )
    st.session_state.model = model
    st.session_state.history = []


if "runner" not in st.session_state:
    init_backend("gemini-2.0-flash")
```

The `if "runner" not in st.session_state` guard is essential — without it every keystroke would rebuild the agents and wipe the conversation.

### 3. Render the chat history and stream the coordinator's reply

Repaint history from state, then stream the new reply. ADK's `run_async` is an async generator, so accumulate partial events into a placeholder:

```python
async def stream_reply(placeholder, question: str) -> tuple[str, str]:
    """Stream the coordinator's reply, returning (text, responding_agent)."""
    message = types.Content(role="user", parts=[types.Part(text=question)])

    text, author = "", ""
    async for event in st.session_state.runner.run_async(
        user_id=USER_ID,
        session_id=st.session_state.session_id,
        new_message=message,
    ):
        if event.content and event.content.parts:
            chunk = event.content.parts[0].text or ""
            if chunk:
                if event.partial:
                    text += chunk
                else:
                    text = chunk
                placeholder.markdown(text)
        if event.is_final_response():
            author = event.author
    return text, author


# Repaint the conversation on every re-run.
for message in st.session_state.history:
    with st.chat_message(message["role"]):
        if message.get("agent"):
            st.caption(f"Handled by: {message['agent']}")
        st.markdown(message["content"])

prompt = st.chat_input("Ask about weather or time...")

if prompt:
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        try:
            answer, author = asyncio.run(stream_reply(placeholder, prompt))
        except Exception as exc:
            answer, author = f"The agent failed: {exc}", "error"
            placeholder.markdown(answer)
        st.caption(f"Handled by: {author}")

    st.session_state.history.append(
        {"role": "assistant", "content": answer, "agent": author}
    )
```

You do not need to re-send the conversation history: the ADK session service already holds it, because every call reuses the same `session_id`. This is a genuine convenience difference from the OpenAI SDK, where you pass the accumulated input list yourself — worth noting for step 6.

### 4. Show which sub-agent handled each turn

`event.author` gives the responding agent's name, and the code above already captures it, renders it live via `st.caption`, and stores it in the history so the repaint loop restores it. Requests should show `weather_agent` or `time_agent`, not `coordinator` — if you see `coordinator` answering directly, its instruction is not firm enough about delegating.

### 5. Add a sidebar control to switch Gemini model variants

Changing model means rebuilding the agents, which is exactly what the factory enables:

```python
MODELS = ["gemini-2.0-flash", "gemini-2.0-flash-lite", "gemini-2.5-flash"]

with st.sidebar:
    st.header("Configuration")
    chosen = st.selectbox(
        "Gemini model", MODELS, index=MODELS.index(st.session_state.model)
    )
    if chosen != st.session_state.model:
        init_backend(chosen)
        st.rerun()

    if st.button("Clear conversation"):
        init_backend(st.session_state.model)
        st.rerun()

    st.metric("Turns", len(st.session_state.history) // 2)
    if "last_latency" in st.session_state:
        st.metric("Last reply (s)", f"{st.session_state.last_latency:.2f}")
```

Record latency so the trade-off is measured rather than guessed. Add `import time` at the top of the file, then replace the timing-relevant line inside the `with st.chat_message("assistant"):` block from step 3:

```python
# Inside the `with st.chat_message("assistant"):` block, replacing the
# single `answer, author = asyncio.run(...)` line:
start = time.perf_counter()
answer, author = asyncio.run(stream_reply(placeholder, prompt))
st.session_state.last_latency = time.perf_counter() - start
```

Switching to the `-lite` variant should measurably reduce latency; check whether routing quality holds on ambiguous requests.

### 6. Run both the OpenAI and Gemini apps and compare

Run them on different ports so both are open at once:

```bash
streamlit run app.py --server.port 8501          # Lab 07, OpenAI
streamlit run gemini_app.py --server.port 8502   # this lab, Gemini
```

Send the identical set of requests to both and record what you observe:

- **Routing quality** — does each request reach the intended specialist? Test ambiguous requests that could plausibly go either way.
- **Latency** — time to first token, and time to complete reply.
- **Developer experience** — lines of setup code, how state is handled, how clear the errors were.
- **Failure behaviour** — what each does with an unknown city or an out-of-scope question.

### 7. Record your comparison in README.md as evidence for the practical assessment

Create `README.md` with your own measured findings — the numbers below are placeholders to replace:

```markdown
# Multi-Agent SDK Comparison

Same architecture (routing coordinator over narrow specialists) built twice.

## Test requests
1. "What is the weather in Singapore?"    (expect weather specialist)
2. "What time is it in Tokyo?"            (expect time specialist)
3. "What is the weather on Mars?"         (expect graceful error)
4. "Tell me about Singapore."             (ambiguous - observe routing)

## Results

| Criterion | OpenAI Agents SDK | Google ADK |
|---|---|---|
| Correct routing (of 4) | _/4 | _/4 |
| Median reply latency | _ s | _ s |
| Lines of setup code | _ | _ |
| Conversation state | Passed in as input list | Held by SessionService |
| Who answered | `result.last_agent.name` | `event.author` |
| Structured output | `output_type=` | `output_schema=` |
| Built-in tracing | Yes, hosted dashboard | Yes, via `adk web` |

## Findings
- Routing: ...
- Latency: ...
- Developer experience: ...
- Failure handling: ...

## Conclusion
Use the OpenAI Agents SDK when ...
Use Google ADK when ...
```

Fill in every row from your own runs. Fabricated numbers are not assessable evidence; a comparison with real measurements and an honest conclusion is.

## Test it

Verify each of the following:

- [ ] The Gemini app runs at <http://localhost:8502> and answers a question.
- [ ] Weather and time requests are routed to `weather_agent` and `time_agent` respectively, with the name shown in the UI.
- [ ] Conversation state holds: a follow-up such as "and what about London?" resolves using earlier context.
- [ ] History survives re-runs and is repainted with the handling agent shown for each turn.
- [ ] Switching model variant in the sidebar rebuilds the backend and changes the measured latency.
- [ ] "Clear conversation" resets the history and starts a fresh ADK session.
- [ ] `README.md` records a concrete comparison of the two SDKs with your own measured numbers.
- [ ] Neither app contains a hard-coded API key; `.env` is git-ignored in both projects.

## What you learned

- The ADK runner and session id must live in `st.session_state`, or Streamlit's re-run silently resets the conversation on every keystroke.
- ADK's session service holds conversation history server-side, so you do not re-send the transcript — a real difference from the OpenAI SDK's input list.
- Bridging ADK's async generator into synchronous Streamlit is done with `asyncio.run` around an async helper.
- A factory function for agent construction is what makes runtime model switching possible without parent-reassignment errors.
- Building the same architecture twice reveals which parts are portable concepts and which are vendor API details.
- An SDK comparison is only evidence if the numbers are measured from your own runs.

## References

- Google ADK documentation — <https://google.github.io/adk-docs/>
- ADK runtime and events — <https://google.github.io/adk-docs/runtime/>
- ADK sessions — <https://google.github.io/adk-docs/sessions/session/>
- Gemini models overview — <https://ai.google.dev/gemini-api/docs/models>
- Streamlit session state — <https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state>
- Streamlit chat elements — <https://docs.streamlit.io/develop/api-reference/chat>
- Deploy on Streamlit Community Cloud — <https://docs.streamlit.io/deploy/streamlit-community-cloud>
