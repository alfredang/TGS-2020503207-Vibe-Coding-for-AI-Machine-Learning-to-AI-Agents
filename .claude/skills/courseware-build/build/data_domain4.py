"""Topic 4 — Multi-Agent System Development with Gemini Agent SDK. Labs 8-9."""

DOMAIN4 = [
    dict(
        num=8, topic=4,
        title="Build a Multi-Agent System with the Gemini Agent SDK",
        objective="Design collaborative agents with the Google Gemini Agent SDK (ADK)",
        desc="Express the same multi-agent pattern in Google's ecosystem. Building the equivalent system twice "
             "separates the portable concepts — agents, tools, routing — from one vendor's API surface.",
        build="A Gemini-powered coordinator agent with two specialist sub-agents and working function tools.",
        services="Python 3.11+, google-adk, Google AI Studio API key",
        phases=[
            'Install the\nGoogle ADK',
            'Create a Gemini\nagent',
            'Add Python\nfunction tools',
            'Attach two\nsub-agents',
            'Confirm the\nrouting',
        ],
        steps=[
            ("Install the Google Agent Development Kit and set your Gemini API key in .env.",
             "uv pip install google-adk"),
            ("Create an Agent with name, model, description and instruction — the description is what makes it "
             "discoverable by a coordinator.", ""),
            ("Write plain Python functions as tools; ADK reads the type hints and docstring to build the schema.", ""),
            ("Run the agent with a Runner and an in-memory session service to confirm single-agent behaviour.", ""),
            ("Create two specialist sub-agents with distinct descriptions and non-overlapping tools.", ""),
            ("Attach them to a coordinator agent via sub_agents and let it route by description.", ""),
            ("Run requests that should reach different specialists and confirm the routing.", ""),
            ("Note the API differences from the OpenAI SDK while the architecture stays identical.", ""),
        ],
        test="The coordinator routes each request to the correct sub-agent, and the tools return live results — "
             "the same behaviour as the OpenAI build, in a different SDK.",
    ),
    dict(
        num=9, topic=4,
        title="Deploy the Gemini Multi-Agent System with Streamlit",
        objective="Deploy a Gemini-based collaborative multi-agent system with Streamlit",
        desc="Give the Gemini agent team the same web interface treatment, then compare the two deployments "
             "side by side and record which ecosystem fits which kind of work.",
        build="A deployed Streamlit application backed by the Gemini multi-agent system, plus a short written "
              "comparison of the two SDKs.",
        services="Python, Streamlit, google-adk",
        phases=[
            'Import the ADK\ncoordinator',
            'Manage session\nand runner state',
            'Render and stream\nthe chat',
            'Show the handling\nsub-agent',
            'Compare the\ntwo SDKs',
        ],
        steps=[
            ("Create a Streamlit app that imports your Gemini coordinator agent.", ""),
            ("Manage the ADK session and runner inside st.session_state so state survives re-runs.", ""),
            ("Render the chat history and stream the coordinator's reply.", ""),
            ("Show which sub-agent handled each turn.", ""),
            ("Add a sidebar control to switch Gemini model variants and observe the latency and quality "
             "trade-off.", ""),
            ("Run both the OpenAI and Gemini apps and compare routing quality, latency and developer "
             "experience.", ""),
            ("Record your comparison in README.md as evidence for the practical assessment.", ""),
        ],
        test="The Gemini app runs, routes correctly and holds conversation state, and your README records a "
             "concrete comparison of the two SDKs.",
    ),
]
