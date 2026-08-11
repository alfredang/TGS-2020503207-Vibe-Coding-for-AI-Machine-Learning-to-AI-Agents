"""Topic 3 — Multi-Agent System Development with OpenAI Agents SDK. Labs 5-7."""

DOMAIN3 = [
    dict(
        num=5, topic=3,
        title="First Agent with the OpenAI Agents SDK",
        objective="Design an agent with the OpenAI Agents SDK using structured outputs and function tools",
        desc="Rebuild the hand-rolled agent from Lab 1 on the OpenAI Agents SDK and see how much the framework "
             "removes. Add a Pydantic output type so the agent returns validated typed data instead of prose, "
             "and expose your own Python functions as tools.",
        build="An SDK-based agent that calls your function tools and returns a validated Pydantic object your "
              "code can use directly.",
        services="Python 3.11+, openai-agents SDK, Pydantic, .env",
        phases=[
            'Install the\nAgents SDK',
            'Create an Agent\nand Runner',
            'Add a Pydantic\noutput type',
            'Add @function_tool\ntools',
            'Inspect the\nrun result',
        ],
        steps=[
            ("Install the Agents SDK and Pydantic into your virtual environment.",
             "uv pip install openai-agents pydantic python-dotenv"),
            ("Create an Agent with a name, clear instructions and a model, then run it with Runner.run_sync to "
             "confirm the setup works.", ""),
            ("Define a Pydantic BaseModel for the answer shape you want, and set it as the agent's output_type.", ""),
            ("Decorate a Python function with @function_tool — the docstring and type hints become the schema "
             "the model sees.", ""),
            ("Add a second tool that calls a real public API so the agent works with live data rather than "
             "hard-coded values.", ""),
            ("Inspect the run result: the final validated output, plus which tools were called and in what order.", ""),
            ("Handle the failure path — a tool that raises should not crash the agent run.", ""),
        ],
        test="result.final_output is an instance of your Pydantic model with correctly typed fields, and the "
             "run trace shows the expected tool calls.",
    ),
    dict(
        num=6, topic=3,
        title="Supervisor Routing and Sub-Agent Delegation",
        objective="Construct a collaborative multi-agent system with supervisor routing and handoffs",
        desc="Move from one overloaded agent to a team. Build three specialists and a triage supervisor that "
             "classifies each request and hands it to the right one — the core multi-agent pattern of the course.",
        build="A four-agent system — a triage supervisor plus research, coding and writing specialists — that "
              "routes each request to the correct specialist.",
        services="Python, openai-agents SDK, Pydantic",
        phases=[
            'Define three\nspecialist agents',
            'Define the\ntriage agent',
            'Write the routing\ninstructions',
            'Add an input\nguardrail',
            'Trace the\nhandoff chain',
        ],
        steps=[
            ("Define three specialist agents, each with narrow instructions and only the tools its own job "
             "requires.", ""),
            ("Define the triage agent and pass the specialists in its handoffs list.", ""),
            ("Write triage instructions describing when to route to each specialist, with a default for "
             "ambiguous requests.", ""),
            ("Run three different requests and confirm each reaches the intended specialist.", ""),
            ("Add a guardrail that rejects out-of-scope requests before any specialist work begins.", ""),
            ("Inspect the trace to see the handoff chain and where the time and tokens were spent.", ""),
            ("Compare against a single agent given all the tools, and note the difference in reliability.", ""),
        ],
        test="A research question reaches the research agent, a coding request reaches the coding agent, and an "
             "out-of-scope request is refused by the guardrail before any specialist runs.",
    ),
    dict(
        num=7, topic=3,
        title="Deploy the Multi-Agent System with Streamlit",
        objective="Deploy a collaborative multi-agent system as a shareable Streamlit web application",
        desc="Put a web interface on the agent team from Lab 6 so a non-developer can use it, streaming the "
             "reply and showing which agent handled each request.",
        build="A running Streamlit chat application backed by your multi-agent system, with visible routing and "
              "persistent conversation history.",
        services="Python, Streamlit, openai-agents SDK",
        phases=[
            'Install Streamlit\nand create app.py',
            'Build the\nchat UI',
            'Hold history in\nsession_state',
            'Show the routing\nto the user',
            'Stream the\nresponse',
        ],
        steps=[
            ("Install Streamlit and create app.py alongside your agents module.",
             "uv pip install streamlit && streamlit run app.py"),
            ("Build the chat UI with st.chat_message and st.chat_input.", ""),
            ("Keep the conversation in st.session_state so history survives Streamlit's re-run on every "
             "interaction.", ""),
            ("Call the triage agent from the UI and render the final output.", ""),
            ("Display which specialist handled the request, so the routing is visible to the user.", ""),
            ("Stream the response so the user sees progress instead of a frozen page.", ""),
            ("Read the API key from the environment, never from the source, and confirm .env is git-ignored.", ""),
        ],
        test="The app runs at localhost:8501, answers a multi-turn conversation with history intact, names the "
             "specialist that handled each turn, and contains no hard-coded API key.",
    ),
]
