"""Lab 09 - Deploy the Gemini Multi-Agent System with Streamlit.

A Streamlit chat front end for the Lab 08 Gemini team: the ADK runner and
session id cached in st.session_state, the coordinator's reply streamed into a
placeholder, the responding sub-agent shown per turn, and a sidebar that
switches Gemini model variants and reports latency.

Run (Streamlit apps execute top to bottom, so there is no main() guard):
    streamlit run gemini_app.py --server.port 8502

Run it on 8502 so the Lab 07 OpenAI app can stay open on 8501 for comparison.

Requires GOOGLE_API_KEY and GOOGLE_GENAI_USE_VERTEXAI=FALSE in a .env file
(never hard-code a key in source). gemini_team.py must sit next to this file.
"""

import asyncio
import time

import streamlit as st
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from gemini_team import APP_NAME, USER_ID, build_coordinator

load_dotenv()

st.set_page_config(page_title="Gemini Multi-Agent Assistant", page_icon="G")
st.title("Gemini Multi-Agent Assistant")
st.caption("Coordinator routing to weather and time specialists.")

MODELS = ["gemini-2.0-flash", "gemini-2.0-flash-lite", "gemini-2.5-flash"]


def init_backend(model: str) -> None:
    """Create the ADK session service, session and runner once per model."""
    session_service = InMemorySessionService()
    # create_session is async while the Streamlit script is synchronous.
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


async def stream_reply(placeholder, question: str) -> tuple[str, str]:
    """Stream the coordinator's reply, returning (text, responding_agent).

    The ADK session service already holds the transcript, so there is no need
    to re-send the conversation - a genuine convenience difference from the
    OpenAI SDK's input list.
    """
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


# --- session state ---------------------------------------------------------
# Without this guard every keystroke would rebuild the agents and wipe the
# conversation, because Streamlit re-runs the script on every interaction.

if "runner" not in st.session_state:
    init_backend(MODELS[0])

# --- sidebar ---------------------------------------------------------------
# Switching model means rebuilding the agents, which is exactly what the
# build_coordinator factory enables without parent-reassignment errors.

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

# --- repaint the conversation on every re-run ------------------------------

for message in st.session_state.history:
    with st.chat_message(message["role"]):
        if message.get("agent"):
            st.caption(f"Handled by: {message['agent']}")
        st.markdown(message["content"])

# --- handle a new submission ----------------------------------------------

prompt = st.chat_input("Ask about weather or time...")

if prompt:
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        try:
            start = time.perf_counter()
            answer, author = asyncio.run(stream_reply(placeholder, prompt))
            st.session_state.last_latency = time.perf_counter() - start
        except Exception as exc:
            answer, author = f"The agent failed: {exc}", "error"
            placeholder.markdown(answer)
        # Expect weather_agent or time_agent here. If the coordinator answers
        # directly, its instruction is not firm enough about delegating.
        st.caption(f"Handled by: {author}")

    st.session_state.history.append(
        {"role": "assistant", "content": answer, "agent": author}
    )
