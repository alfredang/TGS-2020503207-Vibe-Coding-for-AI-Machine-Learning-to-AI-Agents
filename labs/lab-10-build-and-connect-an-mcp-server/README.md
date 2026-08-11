# Lab 10 — Build and Connect an MCP Server

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tertiarycourses/TGS-2020503207-AI-Vibe-Coding-for-Multi-Agents-System/blob/main/labs/lab-10-build-and-connect-an-mcp-server/lab-10-build-and-connect-an-mcp-server.ipynb)

**Topic:** 5 — MCP and Sub-Agents  |  **Objective:** Orchestrate tools through the Model Context Protocol

## Files in this lab

| File | What it is |
|---|---|
| `README.md` | This lab guide. |
| `server.py` | The MCP server: three typed `@mcp.tool()` tools over stdio. Run with `python server.py`, or `mcp dev server.py` for the inspector. |
| `team_notes.json` | The local data file `search_team_notes` reads. |
| `client_demo.py` | A minimal MCP client that spawns the server, lists its tools and calls each one — the same handshake Claude Code performs, so you can verify the server without an agent. Run with `python client_demo.py`. |
| `lab-10-build-and-connect-an-mcp-server.ipynb` | Colab notebook wrapper — writes the server, then verifies it with the client demo. |

## Goal

Write your own MCP server exposing typed tools, then connect it to a coding agent. Because MCP is an open standard, the same server works with any MCP-aware client — write the capability once, use it everywhere.

## What you'll build

A working MCP server with three typed tools, connected to and callable from your coding agent.

**Tools:** Python 3.11+, FastMCP (mcp package), Claude Code or another MCP client

## Prerequisites

- Python 3.11+ with an activated virtual environment.
- An MCP client installed — Claude Code (`npm install -g @anthropic-ai/claude-code`) or Claude Desktop.
- Labs 01-02 completed, so the idea of a tool schema is familiar.

> **Version note.** This lab uses the `FastMCP` class from the `mcp` 1.x line. In `mcp` 2.0.0 the class was renamed to `MCPServer` and `FastMCP` was removed, so pin the version as shown below. If you are working on 2.0.0, the code is identical apart from `from mcp.server.mcpserver import MCPServer` and `MCPServer("toolbox")`.

## Step-by-step

### 1. Install the MCP Python SDK and create server.py

```bash
mkdir lab-10-mcp && cd lab-10-mcp
uv venv && source .venv/bin/activate
uv pip install "mcp[cli]>=1.9,<2" requests
```

The `[cli]` extra installs the `mcp` command-line tool, which includes the inspector you use in step 4.

### 2. Instantiate FastMCP and define your first tool

Create `server.py`. The `@mcp.tool()` decorator reads the type hints and docstring to build the schema the client sees — the same principle as `@function_tool` in Lab 05, but exposed over a protocol rather than inside one process:

```python
"""An MCP server exposing three typed tools over stdio."""

import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("toolbox")

DATA_FILE = Path(__file__).parent / "team_notes.json"


@mcp.tool()
def current_time(timezone: str = "Asia/Singapore") -> str:
    """Get the current date and time in a given IANA timezone.

    Use this whenever the user asks what time it is, or needs today's date.

    Args:
        timezone: An IANA timezone name, e.g. "Asia/Singapore" or "Europe/London".
    """
    try:
        now = datetime.now(ZoneInfo(timezone))
    except Exception:
        return f"Error: '{timezone}' is not a valid IANA timezone name."
    return now.strftime("%Y-%m-%d %H:%M:%S %Z")
```

Write the docstring carefully. It is the only thing the agent reads when deciding whether this tool is relevant.

### 3. Add two more tools — one reading local data and one calling an external API

First create the local data file, `team_notes.json`:

```json
{
  "onboarding": "New joiners get a laptop on day 1 and complete security training in week 1.",
  "deployment": "Deploys run Tuesday and Thursday at 14:00 SGT. Fridays are frozen.",
  "oncall": "The on-call rotation changes Monday 09:00. Escalate to the lead after 30 minutes."
}
```

Then add both tools to `server.py`:

```python
@mcp.tool()
def search_team_notes(query: str) -> str:
    """Search the internal team handbook for a policy or process.

    Use this for questions about internal team practice such as onboarding,
    deployment schedules or the on-call rotation.

    Args:
        query: Keywords to search for, e.g. "deployment schedule".
    """
    if not DATA_FILE.exists():
        return "Error: the team notes file is missing."

    try:
        notes = json.loads(DATA_FILE.read_text())
    except json.JSONDecodeError as exc:
        return f"Error: the team notes file is malformed ({exc})."

    terms = query.lower().split()
    hits = [
        f"{topic}: {text}"
        for topic, text in notes.items()
        if any(term in topic.lower() or term in text.lower() for term in terms)
    ]
    return "\n".join(hits) if hits else f"No notes matched '{query}'."


@mcp.tool()
def get_weather(latitude: float, longitude: float) -> str:
    """Get the current temperature and wind speed for a location.

    Use this whenever the user asks about current weather conditions.

    Args:
        latitude: Latitude in decimal degrees, e.g. 1.29 for Singapore.
        longitude: Longitude in decimal degrees, e.g. 103.85 for Singapore.
    """
    try:
        response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,wind_speed_10m",
            },
            timeout=10,
        )
        response.raise_for_status()
        current = response.json()["current"]
    except requests.RequestException as exc:
        return f"Error: weather service unavailable ({exc})."
    except (KeyError, ValueError) as exc:
        return f"Error: unexpected response from weather service ({exc})."

    return (
        f"Temperature {current['temperature_2m']}degC, "
        f"wind {current['wind_speed_10m']} km/h."
    )
```

### 4. Run the server over stdio and confirm it starts without error

Add the entry point:

```python
if __name__ == "__main__":
    mcp.run(transport="stdio")
```

```bash
python server.py
```

A stdio server waits silently for JSON-RPC on standard input — no output means it started correctly. Press Ctrl+C to stop.

Because the protocol occupies stdout, **never use `print()` in an MCP stdio server**. A stray print corrupts the JSON-RPC stream and the client will fail to connect. Log to stderr or a file instead.

To interact with it properly, use the inspector:

```bash
mcp dev server.py
```

This opens a browser UI where you can list the tools and invoke each one by hand — the fastest way to debug before involving an agent.

### 5. Register the server with your MCP client

Use an **absolute** path — the client does not resolve relative paths from your shell's working directory:

```bash
claude mcp add my-tools -- python /absolute/path/to/server.py
```

If you installed into a virtual environment, point at that environment's interpreter so the `mcp` package is importable:

```bash
claude mcp add my-tools -- /absolute/path/to/lab-10-mcp/.venv/bin/python /absolute/path/to/lab-10-mcp/server.py
```

Get the absolute path with `pwd`.

### 6. List the available tools from the client to confirm discovery

```bash
claude mcp list
```

The server should appear as connected. Inside a `claude` session, `/mcp` shows the servers and their tools. You should see all three: `current_time`, `search_team_notes` and `get_weather`.

If the server shows as failed, the usual causes are a relative path, the wrong Python interpreter, a `print()` in the server, or an import error. Run `python server.py` directly to surface a traceback.

### 7. Ask the agent a question that requires your tools

Start `claude` in any folder and ask something the model cannot answer from its own knowledge:

```
When is our next deployment window, and what time is it now in Singapore?
```

The agent should call `search_team_notes` and `current_time`, then combine both results. Try a multi-tool question that requires sequencing:

```
What is the weather in Singapore right now (1.29, 103.85), and does that
affect our deployment schedule?
```

This is the payoff of MCP: you wrote these tools once, and any MCP-aware client — Claude Code, Claude Desktop, or an agent you build yourself — can use them without a bespoke integration.

### 8. Return a clear error message from a tool on bad input

Every tool above already returns a descriptive string instead of raising. Test each failure path deliberately:

```
What time is it in Mars/Olympus_Mons?
```

The tool returns `Error: 'Mars/Olympus_Mons' is not a valid IANA timezone name.`, and the agent should relay that and offer a valid alternative rather than crashing or inventing a time.

The rule is that a returned error is information the agent can act on, whereas a raised exception is a protocol-level failure that the agent cannot reason about. Compare with the deliberately fragile version:

```python
# Do not do this — an unhandled exception breaks the tool call.
@mcp.tool()
def fragile_time(timezone: str) -> str:
    """Get the time in a timezone."""
    return datetime.now(ZoneInfo(timezone)).isoformat()   # raises on bad input
```

## Test it

Verify each of the following:

- [ ] `mcp dev server.py` lists all three tools and each returns a sensible result when invoked by hand.
- [ ] `claude mcp list` shows `my-tools` as connected.
- [ ] `/mcp` inside a Claude Code session lists `current_time`, `search_team_notes` and `get_weather`.
- [ ] The agent answers a question about the deployment window that it could not possibly know without `search_team_notes`.
- [ ] A question needing two tools results in both being called in a sensible order.
- [ ] `get_weather` returns live data matching current conditions.
- [ ] An invalid timezone produces the descriptive error and the agent handles it gracefully.
- [ ] The server contains no `print()` calls.

## What you learned

- An MCP server exposes typed tools over a standard protocol, so one implementation serves every MCP-aware client — no per-framework integration.
- `@mcp.tool()` builds the schema from type hints and the docstring; the docstring is the discovery signal.
- stdio servers must keep stdout clean — a stray `print()` corrupts the JSON-RPC stream.
- Registration needs absolute paths, and the interpreter must be the one with `mcp` installed.
- `mcp dev` is the fastest debugging loop: verify the server by hand before involving an agent.
- Tools should return descriptive error strings, which the agent can reason about, rather than raising.

## References

- Model Context Protocol — <https://modelcontextprotocol.io/>
- MCP Python SDK — <https://github.com/modelcontextprotocol/python-sdk>
- Build an MCP server — <https://modelcontextprotocol.io/docs/develop/build-server>
- MCP Inspector — <https://modelcontextprotocol.io/docs/tools/inspector>
- Claude Code MCP configuration — <https://docs.claude.com/en/docs/claude-code/mcp>
- Open-Meteo API — <https://open-meteo.com/en/docs>
