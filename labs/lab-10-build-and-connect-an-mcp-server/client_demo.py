"""Lab 10 - MCP client demo: connect to server.py and call its tools.

A minimal MCP client that spawns server.py as a stdio subprocess, lists the
tools it discovers, and invokes each one - including a deliberate bad-input
call to show that a tool returns a descriptive error string rather than raising.

This is the same discovery-and-invoke handshake that Claude Code performs when
you run `claude mcp add`; doing it in code makes the protocol visible and lets
you verify the server without an agent or an API key.

Run (from this lab folder, with the same interpreter that has `mcp` installed):
    python client_demo.py

No API key is needed: only get_weather reaches the network, and it calls the
key-free Open-Meteo API.
"""

import asyncio
from pathlib import Path
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER = Path(__file__).parent / "server.py"


def render(result) -> str:
    """Flatten an MCP tool result into plain text for printing."""
    return "\n".join(
        block.text for block in result.content if getattr(block, "type", "") == "text"
    )


async def demo() -> None:
    """Spawn the server, list its tools, then call each one."""
    # An absolute path and the current interpreter: the client does not resolve
    # relative paths from your shell, and the interpreter must be the one with
    # `mcp` installed.
    params = StdioServerParameters(command=sys.executable, args=[str(SERVER)])

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("=== Tools discovered ===")
            for tool in tools.tools:
                first_line = (tool.description or "").strip().splitlines()[:1]
                print(f"  {tool.name}: {first_line[0] if first_line else ''}")

            print("\n=== current_time ===")
            result = await session.call_tool(
                "current_time", {"timezone": "Asia/Singapore"}
            )
            print(render(result))

            print("\n=== search_team_notes ===")
            result = await session.call_tool(
                "search_team_notes", {"query": "deployment schedule"}
            )
            print(render(result))

            print("\n=== get_weather (Singapore) ===")
            result = await session.call_tool(
                "get_weather", {"latitude": 1.29, "longitude": 103.85}
            )
            print(render(result))

            # The failure path: a returned error is information the agent can
            # act on, not a protocol-level crash.
            print("\n=== current_time with a bad timezone ===")
            result = await session.call_tool(
                "current_time", {"timezone": "Mars/Olympus_Mons"}
            )
            print(render(result))


def main() -> None:
    """Entry point."""
    asyncio.run(demo())


if __name__ == "__main__":
    main()
