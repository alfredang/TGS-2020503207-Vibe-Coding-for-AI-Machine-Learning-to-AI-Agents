"""Lab 07 - Deploy the Multi-Agent System with Streamlit.

A Streamlit chat front end for the Lab 06 agent team: conversation history in
st.session_state, the reply streamed token by token, and the specialist that
handled each turn shown in the UI.

Run (Streamlit apps execute top to bottom, so there is no main() guard):
    streamlit run app.py

The app opens at http://localhost:8501.

Requires OPENAI_API_KEY in a .env file (never hard-code a key in source). When
deploying to Streamlit Community Cloud do not upload .env at all — put the key
in the app's Settings > Secrets panel instead.

team.py must sit next to this file; it is the Lab 06 module exporting
triage_agent.
"""

import asyncio

import streamlit as st
from dotenv import load_dotenv
from openai.types.responses import ResponseTextDeltaEvent

from agents import InputGuardrailTripwireTriggered, Runner

from team import triage_agent

load_dotenv()

st.set_page_config(page_title="Multi-Agent Assistant", page_icon="AI")
st.title("Multi-Agent Assistant")
st.caption("Triage supervisor routing to research, coding and writing specialists.")


async def stream_reply(conversation, placeholder) -> tuple[str, str]:
    """Stream the team's reply into a Streamlit placeholder.

    `agent_updated_stream_event` fires the moment a handoff happens, so the
    handling specialist is known before the answer finishes.
    """
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


# --- session state ---------------------------------------------------------
# Streamlit re-runs the whole script on every interaction. A plain list would be
# reset each time, so history lives in st.session_state behind an `if not in`
# guard — assigning unconditionally is the classic Streamlit bug.

if "history" not in st.session_state:
    st.session_state.history = []   # [{"role", "content", "agent"}]

# --- sidebar ---------------------------------------------------------------

with st.sidebar:
    st.header("Session")
    if st.button("Clear conversation"):
        st.session_state.history = []
        st.rerun()
    st.metric("Turns", len(st.session_state.history) // 2)

# --- repaint the whole conversation on every re-run ------------------------

for message in st.session_state.history:
    with st.chat_message(message["role"]):
        if message.get("agent"):
            st.caption(f"Handled by: {message['agent']}")
        st.markdown(message["content"])

# --- handle a new submission ----------------------------------------------

prompt = st.chat_input("Ask the team something...")

if prompt:
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Pass the accumulated conversation, not just the latest prompt, so the
    # team has real multi-turn memory.
    conversation = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.history
    ]

    with st.chat_message("assistant"):
        placeholder = st.empty()
        try:
            # The Agents SDK is async and Streamlit scripts are synchronous,
            # so bridge them with asyncio.run.
            answer, handler = asyncio.run(stream_reply(conversation, placeholder))
        except InputGuardrailTripwireTriggered:
            answer = "That request is outside what this team handles."
            handler = "Guardrail"
            placeholder.markdown(answer)
        st.caption(f"Handled by: {handler}")

    st.session_state.history.append(
        {"role": "assistant", "content": answer, "agent": handler}
    )
