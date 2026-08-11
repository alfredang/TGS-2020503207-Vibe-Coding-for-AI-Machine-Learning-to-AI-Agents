"""Topic 1 — Modern Agent Foundations. Labs 1-2."""

DOMAIN1 = [
    dict(
        num=1, topic=1,
        title="Build Your First Tool-Calling Agent",
        objective="Explain the components of a modern AI agent and implement a reasoning loop with tool calling",
        desc="Build a single agent from first principles so the loop is not a black box: the model receives a "
             "goal, decides to call a tool, your code executes it, and the result is fed back until the agent "
             "can answer. You will see every message that crosses the boundary.",
        build="A runnable Python agent that answers questions by calling two of your own tools, printing each "
              "reasoning step and tool result so the loop is visible.",
        services="Python 3.11+, OpenAI Python SDK, uv/pip, .env for API keys",
        phases=[
            'Set up the project\nand API key',
            'Write two Python\ntools',
            'Describe them as\nJSON schemas',
            'Write the\nagent loop',
            'Run and read\nthe trace',
        ],
        steps=[
            ("Create the project folder and a virtual environment, then install the OpenAI SDK and python-dotenv.",
             "uv venv && source .venv/bin/activate && uv pip install openai python-dotenv"),
            ("Store your API key in a .env file (never hard-code a key in source, and never commit .env).",
             "echo 'OPENAI_API_KEY=sk-...' > .env"),
            ("Write two plain Python functions the agent may call — get_weather(city) and calculate(expression) — "
             "each returning a JSON-serialisable result.", ""),
            ("Describe both functions as JSON tool schemas: name, description and typed parameters. The "
             "description is what the model uses to decide when to call it.", ""),
            ("Write the agent loop: send messages plus tools to the model, and if the reply contains tool_calls, "
             "execute the matching function and append the result as a tool message.", ""),
            ("Cap the loop with a maximum number of turns so a confused agent cannot spin forever.", ""),
            ("Run the agent and print each step to observe the reason-act-observe cycle end to end.",
             "python agent.py \"What is the weather in Singapore, and what is 15% of 2400?\""),
        ],
        test="The agent answers both parts of the question in one run, and the printed trace shows it called "
             "get_weather once and calculate once before producing the final answer.",
    ),
    dict(
        num=2, topic=1,
        title="Agent Memory and Reusable Agent Skills",
        objective="Implement short-term and long-term agent memory, and package a capability as a reusable skill",
        desc="Give the agent memory so it stops forgetting between turns, then extract a repeatable procedure "
             "into a skill file the agent loads on demand — the modular, transferable capability described in "
             "the course outline.",
        build="An agent with a conversation buffer plus a persistent JSON memory store, and one reusable skill "
              "file that the agent loads only when the task calls for it.",
        services="Python, OpenAI SDK, JSON file store, Markdown skill definition",
        phases=[
            'Add short-term\nmemory',
            'Add a persistent\nJSON store',
            'Inject recalled\nfacts',
            'Write a reusable\nskill file',
            'Load the skill\non demand',
        ],
        steps=[
            ("Add a messages list as short-term memory so the agent can resolve follow-up questions such as "
             "'and what about tomorrow?'.", ""),
            ("Add a long-term store: remember_fact(key, value) and recall_facts() writing to memory.json, both "
             "exposed to the agent as tools.", ""),
            ("Inject the recalled facts into the system prompt at the start of each run so memory actually "
             "influences behaviour.", ""),
            ("Summarise older turns once the buffer grows past a threshold, keeping the context small and cheap.", ""),
            ("Write a skill as a Markdown file with a name, a description of when to use it, and the procedure "
             "steps the agent should follow.", ""),
            ("Load the skill into the system prompt only when the user's request matches its description, and "
             "observe the difference in output quality.", ""),
        ],
        test="Tell the agent a fact, restart the process, ask about it again — the agent recalls it from "
             "memory.json. With the skill loaded, the agent follows the documented procedure instead of "
             "improvising.",
    ),
]
