"""
SINGLE SOURCE OF TRUTH — WSQ AI Vibe Coding for Multi-Agents System (TGS-2020503207).

Every artifact (PPT, LP, LG, LG.md, labs index, assessment) is generated from this
file plus data_domain1.py … data_domain5.py, so they stay 100% aligned.

Guiding principle: the course material must be 100% aligned to the published course
outline and the hands-on labs, so learners can complete the assessment on what was
actually taught.

Content source: the published course outline at
https://www.tertiarycourses.com.sg/wsq-ai-vibe-coding-for-multi-agents-system.html
Admin/branding conventions carried over from the previous Master Trainer Slides.
"""

# ------------------------------------------------------------------ metadata
TITLE        = "AI Vibe Coding for Multi-Agents System"
SHORT_TITLE  = "AI Vibe Coding for Multi-Agents System"   # used in output filenames
COURSE_CODE  = "TGS-2020503207"
VERSION      = "v1.0"
VERSION_DATE = "11 August 2026"
ORG          = "Tertiary Infotech Academy Pte Ltd"
UEN          = "UEN: 201200696W"
TRAINER      = "Dr Alfred Ang"
DAYS         = 2

# Skills Framework alignment (from the published course record)
TSC_TITLE    = "Analytics and Computational Modelling"
TSC_CODE     = "ICT-DIT-3001-1.1"
TSC_ABILITIES = [
    "A1 - Identify appropriate statistical algorithms and data models to test hypotheses or theories",
    "A2 - Use appropriate analytics platforms and analytical tools given specific analytics and reporting requirements",
    "A3 - Utilise a range of statistical methods and analytics approaches to analyse data",
    "A4 - Evaluate the performance and suitability of models against business requirements",
]

COURSE_URL   = "https://www.tertiarycourses.com.sg/wsq-ai-vibe-coding-for-multi-agents-system.html"
REPO_URL     = "https://github.com/tertiarycourses/TGS-2020503207-AI-Vibe-Coding-for-Multi-Agents-System"
LMS_URL      = "https://lms-tms.tertiaryinfotech.com"

# ------------------------------------------------------------------ outcomes
# Aligned to the published multi-agent course outline (Topics 1-5).
LEARNING_OUTCOMES = [
    "LO1: Explain the components of a modern AI agent — skills, memory, tools and the Model Context Protocol (MCP) — and the progression from single-agent to multi-agent collaboration.",
    "LO2: Apply a structured vibe coding workflow with context engineering to specify, generate and verify agent code reliably.",
    "LO3: Build a collaborative multi-agent system with the OpenAI Agents SDK using structured outputs, tool calling and supervisor routing, and deploy it with Streamlit.",
    "LO4: Build a collaborative multi-agent system with the Google Gemini Agent SDK and deploy it with Streamlit.",
    "LO5: Orchestrate tools through MCP and design hierarchical sub-agent architectures for delegated, specialised work.",
]

# ------------------------------------------------------------------ topics (= course outline domains)
# num, code, title, subtitle, weighting, concept bullets for the section
TOPICS = [
    dict(num=1, code="01",
         title="Modern Agent Foundations",
         subtitle="Agent anatomy · Skills · Memory · MCP · Single-agent to multi-agent",
         weighting="20%",
         concepts=[
            ("What is a modern AI agent?", "An LLM that reasons in a loop, calls tools, keeps memory and pursues a goal — not a single prompt-and-response."),
            ("Agent skills", "Modular, transferable capabilities packaged so an agent can load only what a task needs, and reuse them across projects."),
            ("Agent memory", "Short-term context versus long-term stores; what to remember, what to summarise and what to discard."),
            ("Model Context Protocol (MCP)", "An open standard that lets an agent discover and call external tools and data sources through a uniform interface."),
            ("Tools and tool calling", "The agent chooses a function, the runtime executes it, and the result re-enters the reasoning loop."),
            ("Single-agent to multi-agent", "When one agent's context and responsibilities grow too large, split the work across specialised collaborating agents."),
         ]),
    dict(num=2, code="02",
         title="Vibe Coding for Multi-Agent Systems",
         subtitle="Vibe coding workflow · Context engineering · Tooling · Agent skills",
         weighting="20%",
         concepts=[
            ("What is vibe coding?", "Directing an AI coding agent in natural language to generate, run and refine working software, while you stay the reviewer and architect."),
            ("The structured workflow", "Specify, then scaffold, then generate, then run, then verify, then refine — a disciplined loop, not one-shot prompting."),
            ("Context engineering", "Curating exactly the files, specs and constraints the agent sees, which drives reliability far more than prompt wording."),
            ("Vibe coding tools", "Claude Code, Gemini CLI, Codex CLI, Cursor, Windsurf, Antigravity and Trae — terminal agents and agentic IDEs."),
            ("Agent skills integration", "Packaging repeatable procedures as skills the coding agent invokes, so quality does not depend on re-explaining each time."),
            ("Human in the loop", "You own the specification, the review and the acceptance test; the agent owns the typing."),
         ]),
    dict(num=3, code="03",
         title="Multi-Agent System Development with OpenAI Agents SDK",
         subtitle="Agent design · Structured outputs · Tool calling · Supervisor routing · Streamlit",
         weighting="25%",
         concepts=[
            ("The OpenAI Agents SDK", "A lightweight Python framework for agents, tools, handoffs and guardrails, with tracing built in."),
            ("Agents and instructions", "An agent is a model plus instructions plus a tool set; clear role boundaries make multi-agent behaviour predictable."),
            ("Structured outputs", "Pydantic output types force the model to return validated, typed data your code can rely on."),
            ("Function tools and API calls", "Decorate a Python function as a tool so the agent can call your own logic and external APIs."),
            ("Supervisor routing and handoffs", "A triage agent classifies the request and delegates to the specialist sub-agent best suited to it."),
            ("Streamlit deployment", "Wrap the multi-agent system in a simple web UI so non-developers can use it."),
         ]),
    dict(num=4, code="04",
         title="Multi-Agent System Development with Gemini Agent SDK",
         subtitle="Gemini agent design · Collaborative agents · Streamlit deployment",
         weighting="20%",
         concepts=[
            ("The Google Gemini Agent SDK", "Google's Agent Development Kit (ADK) for building, composing and running Gemini-powered agents in Python."),
            ("Defining a Gemini agent", "Model, instruction, description and tools — the description is what makes an agent discoverable by its coordinator."),
            ("Function tools in ADK", "Plain Python functions become tools; the docstring and type hints tell the model how and when to call them."),
            ("Multi-agent composition", "Sub-agents attached to a coordinator agent, which routes each request to the right specialist."),
            ("Sessions and runners", "The runner executes the agent loop while the session service carries conversational state."),
            ("Comparing the SDKs", "The same multi-agent pattern expressed in two ecosystems — portable concepts, different APIs."),
         ]),
    dict(num=5, code="05",
         title="MCP and Sub-Agents",
         subtitle="MCP servers · Tool orchestration · Hierarchical sub-agent architecture",
         weighting="15%",
         concepts=[
            ("MCP in depth", "Servers expose tools, resources and prompts; clients (your agent, Claude Code) discover and invoke them over a standard protocol."),
            ("Why MCP matters", "Write a capability once as a server, and every MCP-aware agent can use it — no bespoke integration per framework."),
            ("Building an MCP server", "Define typed tools with FastMCP and run them over stdio for local agents."),
            ("Tool orchestration", "Sequencing several tools to complete one goal, and handling partial failure sensibly."),
            ("Hierarchical sub-agents", "A parent delegates a bounded task to a child agent with its own context, tools and instructions."),
            ("Context isolation", "Sub-agents keep the parent's context clean by returning only the conclusion, not the whole working trace."),
         ]),
]

# ------------------------------------------------------------------ day themes (8 training hours/day)
DAY_THEMES = {
    1: "Agent Foundations & Vibe Coding for Multi-Agent Systems",
    2: "Agent SDKs, MCP, Sub-Agents & Assessment",
}

# ------------------------------------------------------------------ assessment
ASSESSMENT = dict(
    written="Written Assessment (WA) — Short-Answer Questions (SAQ), 1 hour, open book.",
    practical="Practical Performance (PP) — hands-on multi-agent build tasks, 1 hour, open book.",
    note="A minimum of 75% attendance is required to be eligible for assessment and funding.",
)

# ------------------------------------------------------------------ vibe coding tool landscape (Topic 2 visual)
VIBE_TOOLS_TERMINAL = [
    ("Claude Code", "https://claude.com/product/claude-code"),
    ("Gemini CLI", "https://geminicli.com/"),
    ("Codex CLI", "https://developers.openai.com/codex/cli/"),
    ("Grok CLI", "https://grokcli.io/"),
]
VIBE_TOOLS_IDE = [
    ("Cursor", "https://cursor.com/"),
    ("Windsurf", "https://windsurf.com/"),
    ("Google Antigravity", "https://antigravity.google/"),
    ("Trae", "https://www.trae.ai/"),
]
