"""Lab 10 - Build and Connect an MCP Server.

An MCP server exposing three typed tools over stdio. The @mcp.tool() decorator
reads the type hints and docstring to build the schema the client sees - the
same principle as @function_tool in Lab 05, but exposed over a protocol rather
than inside one process, so any MCP-aware client can use it.

Run:
    python server.py          # waits silently for JSON-RPC on stdin
    mcp dev server.py         # opens the inspector UI to invoke tools by hand

Because the protocol occupies stdout, NEVER use print() in an MCP stdio server:
a stray print corrupts the JSON-RPC stream and the client will fail to connect.
Log to stderr or a file instead.

Version note: this uses the FastMCP class from the `mcp` 1.x line. In mcp 2.0.0
the class was renamed to MCPServer and FastMCP was removed, so requirements.txt
pins mcp[cli]>=1.9,<2. On 2.0.0 the code is identical apart from
`from mcp.server.mcpserver import MCPServer` and `MCPServer("toolbox")`.
"""

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


# Every tool above returns a descriptive error string rather than raising. A
# returned error is information the agent can act on; a raised exception is a
# protocol-level failure the agent cannot reason about. Do not do this:
#
#   @mcp.tool()
#   def fragile_time(timezone: str) -> str:
#       """Get the time in a timezone."""
#       return datetime.now(ZoneInfo(timezone)).isoformat()   # raises on bad input


if __name__ == "__main__":
    mcp.run(transport="stdio")
