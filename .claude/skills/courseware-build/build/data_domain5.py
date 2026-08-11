"""Topic 5 — MCP and Sub-Agents. Labs 10-11."""

DOMAIN5 = [
    dict(
        num=10, topic=5,
        title="Build and Connect an MCP Server",
        objective="Orchestrate tools through the Model Context Protocol",
        desc="Write your own MCP server exposing typed tools, then connect it to a coding agent. Because MCP is "
             "an open standard, the same server works with any MCP-aware client — write the capability once, "
             "use it everywhere.",
        build="A working MCP server with three typed tools, connected to and callable from your coding agent.",
        services="Python 3.11+, FastMCP (mcp package), Claude Code or another MCP client",
        phases=[
            'Install MCP and\ncreate server.py',
            'Define three\ntyped tools',
            'Run the server\nover stdio',
            'Register with the\nMCP client',
            'Call the tools\nfrom the agent',
        ],
        steps=[
            ("Install the MCP Python SDK and create server.py.",
             "uv pip install \"mcp[cli]\""),
            ("Instantiate FastMCP and define your first tool with the @mcp.tool() decorator, using type hints "
             "and a clear docstring.", ""),
            ("Add two more tools — one reading local data and one calling an external API.", ""),
            ("Run the server over stdio and confirm it starts without error.",
             "python server.py"),
            ("Register the server with your MCP client so the agent can discover it.",
             "claude mcp add my-tools -- python /absolute/path/to/server.py"),
            ("List the available tools from the client to confirm discovery.",
             "claude mcp list"),
            ("Ask the agent a question that requires your tools, and watch it select and call them.", ""),
            ("Return a clear error message from a tool on bad input and confirm the agent handles it "
             "gracefully.", ""),
        ],
        test="The MCP client lists all three tools, and the agent completes a task that is impossible without "
             "them, calling the tools in a sensible order.",
    ),
    dict(
        num=11, topic=5,
        title="Hierarchical Sub-Agents and Context Isolation",
        objective="Design a hierarchical sub-agent architecture with delegated, isolated context",
        desc="Build the top of the architecture: a parent agent that delegates bounded tasks to specialised "
             "child agents, each with its own context and tools. The children return conclusions, not their "
             "whole working trace, which is what keeps a large system reliable.",
        build="A three-level hierarchical system — orchestrator, sub-agents and MCP tools — that completes a "
              "multi-part task no single agent handles well.",
        services="Python, openai-agents SDK or google-adk, your MCP server from Lab 10",
        phases=[
            'Define the parent\norchestrator',
            'Expose sub-agents\nas tools',
            "Isolate each\nchild's context",
            'Run independent\nwork concurrently',
            'Handle a failing\nsub-agent',
        ],
        steps=[
            ("Define the parent orchestrator whose only job is to decompose the task and delegate.", ""),
            ("Expose each specialist sub-agent to the parent as a callable tool.", ""),
            ("Give each sub-agent its own instructions and only the tools it needs — including your MCP tools "
             "from Lab 10.", ""),
            ("Ensure each sub-agent returns a short structured conclusion rather than its full transcript.", ""),
            ("Run sub-agents concurrently where their work is genuinely independent, and measure the time "
             "saved.", ""),
            ("Give the orchestrator a task requiring at least three sub-agents and trace the delegation.", ""),
            ("Compare the parent's final context size with and without isolation to see the benefit "
             "quantitatively.", ""),
            ("Handle a failing sub-agent so one failure degrades the result instead of killing the run.", ""),
        ],
        test="The orchestrator completes the multi-part task by delegating to at least three sub-agents; the "
             "parent's context stays small because children return conclusions only, and one deliberately "
             "failing sub-agent does not crash the run.",
    ),
]
