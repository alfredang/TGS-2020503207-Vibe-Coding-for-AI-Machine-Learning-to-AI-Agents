# Lab 07 — Deploy the Multi-Agent System with Streamlit

**Topic:** 3 — Multi-Agent System Development with OpenAI Agents SDK  |  **Objective:** Deploy a collaborative multi-agent system as a shareable Streamlit web application

## Goal

Put a web interface on the agent team from Lab 6 so a non-developer can use it, streaming the reply and showing which agent handled each request.

## What you'll build

A running Streamlit chat application backed by your multi-agent system, with visible routing and persistent conversation history.

**Tools:** Python, Streamlit, openai-agents SDK

## Prerequisites

- Lab 06 completed, with a working `team.py` exporting `triage_agent`.
- `OPENAI_API_KEY` in `.env`, and `.env` listed in `.gitignore`.
- Understanding that Streamlit re-runs your entire script top to bottom on every interaction — this is the single most important fact in this lab.

## Step-by-step

### 1. Install Streamlit and create app.py alongside your agents module

```bash
uv pip install streamlit
```

Place `app.py` in the same folder as `team.py` so you can `from team import triage_agent`. Once written, launch it with:

```bash
streamlit run app.py
```

The app opens at <http://localhost:8501>.

### 2. Build the chat UI with st.chat_message and st.chat_input

Create `app.py`:

```python
"""Streamlit front end for the Lab 06 multi-agent team."""

import asyncio

import streamlit as st
from dotenv import load_dotenv

from agents import Runner
from team import triage_agent

load_dotenv()

st.set_page_config(page_title="Multi-Agent Assistant", page_icon="AI")
st.title("Multi-Agent Assistant")
st.caption("Triage supervisor routing to research, coding and writing specialists.")

prompt = st.chat_input("Ask the team something...")
```

`st.chat_input` is pinned to the bottom of the page and returns the submitted string on the run triggered by submission, or `None` otherwise.

### 3. Keep the conversation in st.session_state so history survives the re-run

Every interaction re-executes the script from line 1. A plain Python list would be reset each time; `st.session_state` is the only thing that persists.

```python
if "history" not in st.session_state:
    st.session_state.history = []   # [{"role", "content", "agent"}]

# Repaint the whole conversation on every re-run.
for message in st.session_state.history:
    with st.chat_message(message["role"]):
        if message.get("agent"):
            st.caption(f"Handled by: {message['agent']}")
        st.markdown(message["content"])
```

Guard the initialisation with `if "history" not in st.session_state` — assigning unconditionally would wipe the history on every re-run, which is the classic Streamlit bug.

### 4. Call the triage agent from the UI and render the final output

The Agents SDK is async, and Streamlit scripts are synchronous, so bridge them with `asyncio.run`. Handle the guardrail exception from Lab 06 here too, so an out-of-scope question produces a polite refusal rather than a red traceback:

```python
from agents import InputGuardrailTripwireTriggered

if prompt:
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            result = asyncio.run(Runner.run(triage_agent, prompt))
            answer = result.final_output
            handler = result.last_agent.name
        except InputGuardrailTripwireTriggered:
            answer = "That request is outside what this team handles."
            handler = "Guardrail"

        st.markdown(answer)
        st.caption(f"Handled by: {handler}")

    st.session_state.history.append(
        {"role": "assistant", "content": answer, "agent": handler}
    )
```

Note this sends only the latest `prompt`, so each turn is independent. To give the team real multi-turn memory, build the accumulated input list and pass that instead:

```python
# Inside `if prompt:`, replacing the single-prompt Runner.run call above:
conversation = [
    {"role": m["role"], "content": m["content"]}
    for m in st.session_state.history
]
result = asyncio.run(Runner.run(triage_agent, conversation))
```

### 5. Display which specialist handled the request

The `st.caption(f"Handled by: {handler}")` line above already does this for the live turn, and the repaint loop in step 3 restores it for historical turns because the name is stored alongside the message. Making the routing visible is what turns the multi-agent architecture from an implementation detail into something the user can reason about — and it is what you will demonstrate in the assessment.

### 6. Stream the response so the user sees progress

`Runner.run_streamed` returns immediately and yields events as they arrive. Filter for raw response deltas to build the text incrementally, and watch for `agent_updated_stream_event` to catch the handoff the moment it happens:

```python
from openai.types.responses import ResponseTextDeltaEvent


async def stream_reply(conversation, placeholder) -> tuple[str, str]:
    """Stream the team's reply into a Streamlit placeholder."""
    result = Runner.run_streamed(triage_agent, conversation)
    text = ""
    handler = triage_agent.name

    async for event in result.stream_events():
        if event.type == "agent_updated_stream_event":
            handler = event.new_agent.name
        elif event.type == "raw_response_event" and isinstance(
            event.data, ResponseTextDeltaEvent
        ):
            text += event.data.delta
            placeholder.markdown(text)

    return text, handler
```

Wire it into the submit branch, replacing the blocking call from step 4:

```python
if prompt:
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    conversation = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.history
    ]

    with st.chat_message("assistant"):
        placeholder = st.empty()
        try:
            answer, handler = asyncio.run(stream_reply(conversation, placeholder))
        except InputGuardrailTripwireTriggered:
            answer = "That request is outside what this team handles."
            handler = "Guardrail"
            placeholder.markdown(answer)
        st.caption(f"Handled by: {handler}")

    st.session_state.history.append(
        {"role": "assistant", "content": answer, "agent": handler}
    )
```

`st.empty()` reserves one slot that gets overwritten with the growing text, rather than appending a new element per token.

### 7. Read the API key from the environment, never from the source

`load_dotenv()` at the top of the file already does this — the SDK picks up `OPENAI_API_KEY` from the environment automatically. Confirm nothing leaked:

```bash
git grep -nE "sk-[A-Za-z0-9]{20}"   # must return nothing
git check-ignore -v .env            # must confirm .env is ignored
git status --short                  # .env must not appear
```

If `.env` is not ignored, fix it before committing:

```bash
echo '.env' >> .gitignore
```

For deployment to Streamlit Community Cloud, do not upload `.env` at all — put the key in the app's **Settings > Secrets** panel, which exposes it to the process as an environment variable.

Add a sidebar control so you can clear the conversation while testing:

```python
with st.sidebar:
    st.header("Session")
    if st.button("Clear conversation"):
        st.session_state.history = []
        st.rerun()
    st.metric("Turns", len(st.session_state.history) // 2)
```

## Test it

Verify each of the following:

- [ ] The app runs at <http://localhost:8501> and accepts a question.
- [ ] A multi-turn conversation keeps its history intact — earlier messages remain on screen after each new question.
- [ ] A follow-up question that depends on the previous turn is answered correctly, confirming the conversation list is being passed.
- [ ] Each assistant message names the specialist that handled it, both live and after a re-run.
- [ ] The reply appears progressively rather than all at once after a frozen pause.
- [ ] An out-of-scope question produces a polite refusal, not a red traceback.
- [ ] "Clear conversation" empties the history.
- [ ] `git grep -nE "sk-[A-Za-z0-9]{20}"` returns nothing and `.env` does not appear in `git status`.

## What you learned

- Streamlit re-runs the whole script on every interaction, so all state that must survive belongs in `st.session_state`, guarded by an `if not in` initialisation.
- `st.chat_message` and `st.chat_input` provide the chat UI; the history must be repainted from state on every run.
- Bridging the async Agents SDK into a synchronous Streamlit script is done with `asyncio.run`.
- `Runner.run_streamed` plus `stream_events()` gives progressive output, and `agent_updated_stream_event` exposes the handoff as it happens.
- Surfacing which specialist answered turns routing into a visible, demonstrable feature.
- Secrets come from the environment locally and from the platform's secrets panel in deployment — never from source.

## References

- Streamlit chat elements — <https://docs.streamlit.io/develop/api-reference/chat>
- Streamlit session state — <https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state>
- Build a basic LLM chat app — <https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps>
- Streamlit secrets management — <https://docs.streamlit.io/develop/concepts/connections/secrets-management>
- Agents SDK streaming — <https://openai.github.io/openai-agents-python/streaming/>
- Running agents — <https://openai.github.io/openai-agents-python/running_agents/>
