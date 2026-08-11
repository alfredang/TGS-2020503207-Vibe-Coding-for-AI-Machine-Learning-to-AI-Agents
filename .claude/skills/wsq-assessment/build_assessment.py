#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the WSQ assessment set for 'Application Integration with Docker and Kubernetes' (TGS-2021010366):
  - Written Assessment (SAQ)  — 5 open-ended KNOWLEDGE questions (K1–K5), aligned to the slides
  - Practical Performance (PP) — 4 PRACTICAL tasks (LO1–LO4), aligned to the in-class activities
Each instrument is produced as a Question Paper and a matching Answer Key (4 DOCX total),
all with the WSQ house cover page (same as the Lesson Plan / Learner Guide). Page 1 is the cover;
page 2 carries Trainee Information + Instructions + Grading; the questions/tasks begin on page 3.
Body: Arial 11.
"""
import os, sys
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# This script lives in the wsq-assessment skill (.claude/skills/wsq-assessment/) and runs in
# place — it detects the course repo root by walking up to the nearest dir that has a .git
# folder (or both courseware/ and assessment/). Override with env REPO=/path if needed.
def _find_repo():
    env = os.environ.get("REPO")
    if env and os.path.isdir(env):
        return os.path.abspath(env)
    d = os.path.dirname(os.path.abspath(__file__))
    while d != os.path.dirname(d):
        if os.path.isdir(os.path.join(d, ".git")) or \
           (os.path.isdir(os.path.join(d, "courseware")) and os.path.isdir(os.path.join(d, "assessment"))):
            return d
        d = os.path.dirname(d)
    return os.getcwd()

REPO = _find_repo()
# prodoc.py (WSQ cover page + version control + page numbers, same as LP/LG) ships with the
# tertiary-lesson-plan skill. Look for it at the project level first, then the user level.
for _cand in (os.path.join(REPO, ".claude/skills/tertiary-lesson-plan"),
              os.path.expanduser("~/.claude/skills/tertiary-lesson-plan")):
    if os.path.exists(os.path.join(_cand, "prodoc.py")):
        sys.path.insert(0, _cand); break
import prodoc  # cover page + version control + page numbers (same as LP/LG)

# ─── EDIT PER COURSE ────────────────────────────────────────────────────────
TITLE       = "AI Vibe Coding for Multi-Agents System"
COURSE_CODE = "TGS-2020503207"
# ────────────────────────────────────────────────────────────────────────────
# The cover page renders prodoc's module-level TGS constant. Override it so the
# assessment cover shows THIS course's ref (works with either prodoc version —
# the older project prodoc has no course_code kwarg).
prodoc.TGS = f"TGS Ref No: {COURSE_CODE}"
OUT   = os.path.join(REPO, "assessment")

# Logos: prefer the course's own courseware/assets, else fall back to the copies bundled
# in this skill (so the assessment builds even outside this project).
def _logo(name):
    here = os.path.dirname(os.path.abspath(__file__))
    for p in (os.path.join(REPO, "courseware/assets", name), os.path.join(here, "assets", name)):
        if os.path.exists(p):
            return p
    return None
ORG_LOGO    = _logo("tertiary-infotech-logo.png")
COURSE_LOGO = None   # Tertiary-only cover (as LP/LG)

Q_VER, A_VER = "v1", "v1"   # single standardised version across all four files
BRAND = RGBColor(0x1F, 0x6F, 0xEB); DARK = RGBColor(0x11, 0x18, 0x27); GREY = RGBColor(0x55, 0x5B, 0x66)
# Assessments carry the cover page only — no Document Version Control Record.

# Timings mirror the ORIGINAL papers pulled from the TMS:
#   WA (SAQ) = 50 minutes, 7 questions (K1–K7)
#   PP       = 75 minutes, 5 tasks (A1–A10)
WA_MINUTES = "50 minutes"
PP_MINUTES = "75 minutes"

# ---------------------------------------------------------------- WRITTEN (KNOWLEDGE)
# (criterion, context, question, [model-answer points]) — each traces to the course slides.
WRITTEN = [
 ("K1",
  "Organisations are moving from simple chatbots to AI agents. A chatbot returns an answer to a single prompt, "
  "whereas an agent is given a goal and works towards it by taking actions and checking the results.",
  "Explain what a modern AI agent is and describe the reasoning loop it follows. In your answer, identify the "
  "main components that make an agent different from a simple chatbot.",
  ["A modern AI agent is an LLM that reasons in a loop, calls tools, keeps memory and pursues a goal — it is "
   "not a single prompt-and-response exchange.",
   "The reasoning loop is GOAL → REASON → ACT → OBSERVE, repeated until the goal is met or a turn limit is "
   "reached: the model decides the next action, a tool is called and executed, and the result re-enters the "
   "context to inform the next decision.",
   "Key components: (a) tools — functions the agent may call to reach beyond the model, such as APIs, files, "
   "databases or the shell; (b) memory — short-term conversation context plus durable long-term facts; "
   "(c) instructions defining the agent's role and boundaries; (d) a turn limit so a confused agent cannot "
   "loop forever.",
   "A chatbot answers; an agent pursues a goal, takes actions and checks its own results. Autonomy is bounded: "
   "the agent chooses the path while the developer sets the boundaries, the budget and the review gate.",
   "(Slides: What is an AI Agent? / The Agent Reasoning Loop. Lab 1.)"]),
 ("K2",
  "As an agent's responsibilities grow, developers must decide whether to keep extending one agent or to split "
  "the work across several collaborating agents.",
  "Compare a single-agent design with a multi-agent system. Explain when each is appropriate and describe the "
  "benefits a multi-agent architecture provides.",
  ["A single agent is best when the task is narrow and well defined, a handful of tools is enough, and the "
   "context stays small.",
   "Its limits: too many tools confuse tool choice; one long context mixes unrelated work; and a single "
   "instruction set has to cover everything, which makes behaviour unpredictable.",
   "A multi-agent system is appropriate when the work splits into distinct specialities, each part needs its "
   "own tools and rules, or the parts can run in parallel.",
   "Benefits: focused instructions per agent, isolated context per agent, easier testing and replacement of "
   "one part, and parallel execution of independent work.",
   "The usual pattern is a supervisor/triage agent that classifies the request and routes it to the specialist "
   "best suited to it.",
   "(Slides: Single Agent vs Multi-Agent System / Multi-Agent Architecture Pattern.)"]),
 ("K3",
  "Agents need to remember information, and teams need to reuse capabilities across projects rather than "
  "rewriting them each time.",
  "Describe agent memory and agent skills. Explain the difference between short-term and long-term memory, and "
  "explain what makes a skill a modular, transferable capability.",
  ["Short-term memory is the conversation buffer — the messages list that lets the agent resolve follow-up "
   "questions such as 'and what about tomorrow?'. It lives only for the current run.",
   "Long-term memory is a persistent store (for example a JSON file exposed through remember_fact and "
   "recall_facts tools) that survives restarts; recalled facts are injected into the system prompt so memory "
   "actually influences behaviour.",
   "Older turns are summarised once the buffer grows past a threshold, keeping the context small and cheap.",
   "An agent skill is a modular, transferable capability — a documented procedure (name, when to use it, and "
   "the steps) packaged so an agent loads only what a task needs and can reuse it across projects.",
   "Skills make quality repeatable: the agent follows the documented procedure instead of improvising, without "
   "the developer re-explaining it every session.",
   "(Slides: Key Concepts — Modern Agent Foundations. Lab 2.)"]),
 ("K4",
  "Vibe coding means directing an AI coding agent in natural language to produce working software. Done "
  "casually it produces unreliable results; done with a disciplined process it is dependable.",
  "Describe the structured vibe coding workflow and explain what context engineering is and why it matters "
  "more than prompt wording.",
  ["The structured workflow is SPECIFY → SCAFFOLD → GENERATE → RUN & VERIFY → REFINE, a disciplined loop "
   "rather than one-shot prompting.",
   "Specify: write the goal, inputs/outputs, constraints and the acceptance test FIRST — the specification is "
   "the real deliverable. Scaffold: have the agent build project structure and dependencies before logic. "
   "Generate: implement one component at a time, reviewing each diff. Run & verify: execute the code and paste "
   "real error output back, which produces far better fixes than 'it does not work'. Refine: one improvement "
   "per iteration, committing the working state each time.",
   "Context engineering is deliberately curating exactly the files, specifications and constraints the agent "
   "sees. It drives reliability far more than prompt wording.",
   "In practice: curate rather than dump; keep a project context file (CLAUDE.md / GEMINI.md) stating the "
   "stack, conventions and prohibitions; reference precise file paths and line ranges instead of pasting large "
   "blocks; and package repeatable procedures as skills.",
   "The human stays the reviewer and architect — you own the specification, the review and the acceptance "
   "decision; the agent owns the typing.",
   "(Slides: The Structured Vibe Coding Workflow / Context Engineering. Labs 3 and 4.)"]),
 ("K5",
  "The OpenAI Agents SDK provides the building blocks for agents, tools and delegation in Python.",
  "Describe the main building blocks of the OpenAI Agents SDK and explain how structured outputs and "
  "supervisor routing make a multi-agent system more reliable.",
  ["Agent — a model plus instructions plus a tool set; the unit of specialisation. Runner — executes the agent "
   "loop, for example Runner.run_sync(agent, prompt).",
   "@function_tool — turns a plain Python function into a callable tool; the type hints and docstring become "
   "the schema the model sees, so the description determines when the model calls it.",
   "output_type — a Pydantic model that forces the agent to return validated, typed data instead of free "
   "prose, so downstream code can rely on the shape rather than parsing text.",
   "handoffs — the list of specialists a triage agent may delegate to. The triage agent classifies the request "
   "and routes it to the specialist best suited to it, with a default for ambiguous requests.",
   "Guardrails — input and output checks that reject out-of-scope or unsafe requests before any specialist "
   "work begins, saving cost and preventing bad output.",
   "Reliability improves because each specialist has narrow instructions and only the tools its own job needs, "
   "instead of one agent holding every tool.",
   "(Slides: OpenAI Agents SDK — Triage and Handoffs / The Building Blocks. Labs 5 and 6.)"]),
 ("K6",
  "The Model Context Protocol (MCP) is an open standard for connecting agents to tools and data.",
  "Explain what MCP is, what an MCP server exposes, and why the standard is valuable compared with writing a "
  "bespoke integration for each framework.",
  ["MCP (Model Context Protocol) is an open standard that lets an agent discover and call external tools and "
   "data sources through a uniform interface.",
   "An MCP server publishes typed tools, resources and prompts. Clients — your agent, or a coding agent such "
   "as Claude Code — discover those tools and invoke them over the protocol.",
   "Transport is stdio for local servers and HTTP/SSE for remote ones.",
   "The problem it solves: without a standard, every framework needed its own bespoke integration for the same "
   "tool, which multiplies work and maintenance.",
   "The payoff: write the capability once as a server and every MCP-aware agent can use it — no per-framework "
   "rewrite. A tool built with FastMCP and the @mcp.tool() decorator is immediately reusable.",
   "(Slides: Model Context Protocol (MCP) / How MCP Connects an Agent to Your Tools. Lab 10.)"]),
 ("K7",
  "Large agent systems are commonly organised as a hierarchy, with a parent agent delegating bounded tasks to "
  "child agents.",
  "Explain what a hierarchical sub-agent architecture is and describe why context isolation improves the "
  "reliability of a large multi-agent system.",
  ["In a hierarchical architecture a parent orchestrator decomposes the task and delegates a bounded piece of "
   "work to a child sub-agent, which has its own instructions, tools and context.",
   "The problem it solves: one agent doing everything fills its context with irrelevant working detail, which "
   "degrades its decisions.",
   "Context isolation means the sub-agent works in its own context and returns only a short structured "
   "conclusion, not its full transcript — so the orchestrator sees answers rather than working traces and its "
   "context stays small.",
   "Further benefits: independent sub-agents can run concurrently, cutting wall-clock time; a failing "
   "sub-agent degrades the result instead of killing the whole run; and each sub-agent has a narrow contract "
   "that can be tested on its own.",
   "A typical three-tier design is orchestrator → sub-agents → shared tools/MCP servers.",
   "(Slides: Hierarchical Sub-Agent Architecture / Why Context Isolation Matters. Lab 11.)"]),
]

# ---------------------------------------------------------------- PRACTICAL (ABILITY)
SCENARIO = (
 "You are an AI engineer at Vertex Analytics, a Singapore consultancy. The firm wants an internal AI assistant "
 "that its consultants can use for research, drafting and quick calculations. You have been asked to build it "
 "as a multi-agent system rather than one large agent, to prototype it on two different agent SDKs so the firm "
 "can choose an ecosystem, and to expose the firm's own internal tools through the Model Context Protocol so "
 "any future agent can reuse them. Complete the five tasks below. Each mirrors a hands-on lab you completed in "
 "class. For each task, paste your code and a screenshot of your working output as evidence.")

# (label, criterion, task prompt, box caption, model-answer build steps citing the lab)
BOX_CAP = "Paste your code and a screenshot of your output in the box below"
PRACTICAL = [
 ("Task 1", "A1, A4",
  "Build a tool-calling agent with memory (Labs 1 and 2). "
  "Part A — Write a Python agent that calls the model with two of your own tools: get_weather(city) and "
  "calculate(expression). Describe each function as a JSON tool schema with a name, a description and typed "
  "parameters, then write the agent loop so that when the reply contains tool_calls, your code executes the "
  "matching function and appends the result as a tool message. Cap the loop with a maximum number of turns. "
  "Part B — Add memory: keep a messages list as short-term memory, and add remember_fact(key, value) and "
  "recall_facts() tools that persist to memory.json, injecting the recalled facts into the system prompt. "
  "Run the agent with a question that needs BOTH tools and show the printed reasoning trace.",
  BOX_CAP,
  ["Create the project and virtual environment, then install the SDK: uv venv && source .venv/bin/activate; "
   "uv pip install openai python-dotenv. Store the key in .env (never hard-coded, never committed) and load it "
   "with python-dotenv.",
   "Write the two plain Python functions get_weather(city) and calculate(expression), each returning a "
   "JSON-serialisable result.",
   "Describe both as JSON tool schemas — name, description and typed parameters. The description is what the "
   "model uses to decide when to call the tool.",
   "Write the agent loop: send messages plus tools to the model; if the reply contains tool_calls, execute the "
   "matching function and append the result as a tool message; repeat until the model returns a final answer.",
   "Cap the loop with a maximum turn count so a confused agent cannot spin forever.",
   "Memory: keep the messages list as short-term memory; add remember_fact/recall_facts tools writing to "
   "memory.json; inject recalled facts into the system prompt at the start of each run; summarise older turns "
   "once the buffer passes a threshold.",
   "Evidence: the trace shows get_weather called once and calculate called once before the final answer, and a "
   "fact told to the agent is recalled from memory.json after restarting the process. (Labs 1 and 2.)"]),
 ("Task 2", "A2, A3",
  "Apply the structured vibe coding workflow with engineered context (Labs 3 and 4). "
  "Part A — Using an AI coding agent (Claude Code, Gemini CLI, Cursor or equivalent), build a small research-"
  "assistant agent WITHOUT hand-writing the implementation. Write SPEC.md FIRST, stating the goal, the inputs "
  "and outputs, the constraints and the acceptance test. Initialise Git, have the agent scaffold the structure, "
  "then implement one component at a time, reviewing each diff and committing the working state. "
  "Part B — Create a project context file (CLAUDE.md or GEMINI.md) stating the stack, conventions and what the "
  "agent must never do, and write one reusable skill file capturing a repeatable procedure. Demonstrate that "
  "the same prompt produces house-standard code with the context in place. "
  "Show your SPEC.md, your context file and your Git log as evidence.",
  BOX_CAP,
  ["Launch the coding agent in an empty folder and run git init so every AI change is reviewable as a diff.",
   "Write SPEC.md first — goal, inputs/outputs, constraints and the acceptance test. Be explicit about what "
   "'done' means; the specification is the deliverable, the agent produces the code.",
   "Ask the agent to scaffold ONLY the project structure and dependencies from SPEC.md — structure first, "
   "logic second.",
   "Implement one component at a time, reviewing the diff after each before moving on.",
   "Run the code and paste real error output back to the agent; concrete errors produce far better fixes than "
   "'it does not work'.",
   "Verify against the acceptance test in SPEC.md, then commit: git add -A && git commit -m 'Working research "
   "agent per SPEC.md'. Refine one improvement at a time, re-running the test after each change.",
   "Context engineering: create CLAUDE.md/GEMINI.md with the stack, conventions, folder layout and "
   "prohibitions; compare output against the vague-prompt baseline; write a skill file with the procedure "
   "steps and quality checks; reference precise files and line ranges rather than pasting whole files.",
   "Evidence: the generated agent passes the acceptance test written before any code existed, the Git history "
   "shows small reviewable commits, and the agent follows the skill instead of improvising. (Labs 3 and 4.)"]),
 ("Task 3", "A5, A8",
  "Build and deploy a supervisor-routed multi-agent system on the OpenAI Agents SDK (Labs 5, 6 and 7). "
  "Part A — Build three specialist agents (research, coding and writing), each with narrow instructions and "
  "only the tools its own job requires, plus at least one @function_tool and a Pydantic output_type that "
  "returns validated typed data. "
  "Part B — Build a triage agent that routes each request to the correct specialist via handoffs, and add a "
  "guardrail that rejects out-of-scope requests before any specialist runs. "
  "Part C — Deploy the system as a Streamlit chat application that keeps conversation history in "
  "st.session_state and displays which specialist handled each request. "
  "Show the routing for three different requests and a screenshot of the running app.",
  BOX_CAP,
  ["Install the SDK: uv pip install openai-agents pydantic python-dotenv.",
   "Create an Agent with a name, clear instructions and a model; run it with Runner.run_sync to confirm the "
   "setup, then set output_type to a Pydantic BaseModel so the result is validated typed data.",
   "Decorate a Python function with @function_tool — the docstring and type hints become the schema the model "
   "sees; add a second tool that calls a real public API so the agent works with live data.",
   "Define the three specialist agents with narrow instructions and non-overlapping tools, then define the "
   "triage agent passing the specialists in its handoffs list.",
   "Write triage instructions describing when to route to each specialist, with a default for ambiguous "
   "requests; add a guardrail rejecting out-of-scope requests before specialist work begins.",
   "Streamlit: build the chat UI with st.chat_message and st.chat_input; keep the conversation in "
   "st.session_state so history survives the re-run on every interaction; call the triage agent and render the "
   "final output; display which specialist handled the request; stream the response.",
   "Read the API key from the environment, never from source, and confirm .env is git-ignored.",
   "Evidence: result.final_output is an instance of the Pydantic model; a research question reaches the "
   "research agent and a coding request the coding agent; an out-of-scope request is refused by the guardrail; "
   "the app runs at localhost:8501 with history intact. (Labs 5, 6 and 7.)"]),
 ("Task 4", "A6, A7",
  "Build and deploy the equivalent multi-agent system on the Google Gemini Agent SDK (Labs 8 and 9). "
  "Part A — Using the Google Agent Development Kit (ADK), create a coordinator agent with at least two "
  "specialist sub-agents. Give each agent a name, model, description and instruction, and attach plain Python "
  "functions as tools. Attach the specialists via sub_agents so the coordinator routes by description. "
  "Part B — Run the system with a Runner and a session service, then deploy it as a Streamlit application that "
  "manages the ADK session and runner in st.session_state and shows which sub-agent handled each turn. "
  "Part C — Compare the two SDKs and record your comparison. "
  "Show the routing evidence, a screenshot of the running app and your written comparison.",
  BOX_CAP,
  ["Install the ADK: uv pip install google-adk, and set the Gemini API key in .env.",
   "Create an Agent with name, model, description and instruction — the description is what makes an agent "
   "discoverable by its coordinator.",
   "Write plain Python functions as tools; ADK reads the type hints and docstring to build the schema.",
   "Run the agent with a Runner and an InMemorySessionService to confirm single-agent behaviour before adding "
   "the hierarchy.",
   "Create two specialist sub-agents with distinct descriptions and non-overlapping tools, then attach them to "
   "the coordinator via sub_agents and let it route by description.",
   "Streamlit: import the coordinator, manage the ADK session and runner inside st.session_state so state "
   "survives re-runs, render the chat history, stream the reply and show which sub-agent handled each turn; "
   "add a sidebar control to switch Gemini model variants.",
   "Comparison: the same architecture in both ecosystems — OpenAI uses Agent/Runner.run_sync with "
   "handoffs=[...] and output_type; ADK uses Agent(name, model, description, instruction) with sub_agents=[...] "
   "and Runner + session service, routing driven by each agent's description. Record routing quality, latency "
   "and developer experience in README.md.",
   "Evidence: the coordinator routes each request to the correct sub-agent, tools return live results, the app "
   "holds conversation state, and README.md records a concrete comparison. (Labs 8 and 9.)"]),
 ("Task 5", "A9, A10",
  "Build an MCP server and a hierarchical sub-agent system (Labs 10 and 11). "
  "Part A — Write an MCP server with FastMCP exposing THREE typed tools (one reading local data and one "
  "calling an external API), run it over stdio, register it with an MCP client and confirm the client "
  "discovers all three tools. Return a clear error message from a tool on bad input. "
  "Part B — Build a hierarchical system: a parent orchestrator that decomposes a task and delegates to at "
  "least three specialist sub-agents, each with its own instructions, tools (including your MCP tools) and "
  "isolated context, returning only a short structured conclusion rather than a full transcript. Handle a "
  "failing sub-agent so one failure degrades the result instead of killing the run. "
  "Show the discovered tool list, the delegation trace and your error handling.",
  BOX_CAP,
  ["Install the MCP SDK: uv pip install \"mcp[cli]\" and create server.py.",
   "Instantiate FastMCP and define each tool with the @mcp.tool() decorator, using type hints and a clear "
   "docstring; add one tool reading local data and one calling an external API.",
   "Run the server over stdio (python server.py), then register it with the client: claude mcp add my-tools -- "
   "python /absolute/path/to/server.py, and confirm discovery with claude mcp list.",
   "Ask the agent a question that requires the tools and watch it select and call them; return a clear error "
   "message from a tool on bad input and confirm the agent handles it gracefully.",
   "Hierarchy: define the parent orchestrator whose only job is to decompose the task and delegate; expose "
   "each specialist sub-agent to the parent as a callable tool; give each sub-agent its own instructions and "
   "only the tools it needs, including the MCP tools.",
   "Ensure each sub-agent returns a short structured conclusion rather than its full transcript, keeping the "
   "parent's context small; run independent sub-agents concurrently and measure the time saved.",
   "Handle a failing sub-agent so one failure degrades the result instead of killing the run.",
   "Evidence: the MCP client lists all three tools; the agent completes a task impossible without them; the "
   "orchestrator delegates to at least three sub-agents; the parent context stays small because children "
   "return conclusions only; a deliberately failing sub-agent does not crash the run. (Labs 10 and 11.)"]),
]

# ---------------------------------------------------------------- doc helpers
def base_doc():
    doc = Document()
    n = doc.styles["Normal"]; n.font.name = "Arial"; n.font.size = Pt(11)
    return doc

def para(doc, text, size=11, bold=False, italic=False, color=None, after=6, before=0, align=None):
    p = doc.add_paragraph(); r = p.add_run(text)
    r.font.size = Pt(size); r.bold = bold; r.italic = italic
    if color: r.font.color.rgb = color
    p.paragraph_format.space_after = Pt(after); p.paragraph_format.space_before = Pt(before)
    if align is not None: p.alignment = align
    return p

def heading(doc, text, size=13):
    para(doc, text, size=size, bold=True, color=BRAND, after=6, before=8)

def answer_box(doc, lines=None, code=None, height_pt=90):
    """1x1 bordered box. `lines` → bullet-style model answer; `code` → monospace
    code/YAML/command block (indentation preserved); neither → empty answer space."""
    t = doc.add_table(rows=1, cols=1); t.style = "Table Grid"; t.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = t.rows[0].cells[0]
    cell.paragraphs[0].text = ""
    if code:
        run = cell.paragraphs[0].add_run("Suggestive answers (not exhaustive):")
        run.bold = True; run.font.size = Pt(10.5)
        for ln in code.split("\n"):
            b = cell.add_paragraph(style=None)
            b.paragraph_format.space_after = Pt(0); b.paragraph_format.space_before = Pt(0)
            rr = b.add_run(ln if ln else " ")
            rr.font.name = "Consolas"; rr.font.size = Pt(9)
            rr._element.rPr.rFonts.set(qn('w:cs'), "Consolas")
            wt = rr._element.find(qn('w:t'))
            if wt is not None: wt.set(qn('xml:space'), 'preserve')
    elif lines:
        run = cell.paragraphs[0].add_run("Suggestive answers (not exhaustive):")
        run.bold = True; run.font.size = Pt(10.5)
        for ln in lines:
            b = cell.add_paragraph(style=None); b.paragraph_format.left_indent = Inches(0.15)
            rr = b.add_run("•  " + ln); rr.font.size = Pt(10.5)
    else:
        # empty answer space
        tr = t.rows[0]._tr
        trPr = tr.get_or_add_trPr(); trh = OxmlElement('w:trHeight')
        trh.set(qn('w:val'), str(int(height_pt*20))); trh.set(qn('w:hRule'), 'atLeast'); trPr.append(trh)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

def page_break(doc):
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

FILL_GAP = 6    # extra space below each fill-in line (paired with double line spacing for writing room)

def candidate_block(doc):
    heading(doc, "Trainee Information")
    for label in ["Trainee Name (as per NRIC): ______________________________________",
                  "Last 3 digits and alphabet of NRIC/FIN: ____________________",
                  "Date: ____________________"]:
        p = para(doc, label, size=11, after=FILL_GAP)
        p.paragraph_format.line_spacing = 2.0

# Assessment briefing (from the course slides — "Briefing for Assessment").
BRIEFING = [
    "Place phones and other materials under the table or on the floor.",
    "No photos or recording of assessment scripts.",
    "No discussion during the assessment.",
    "Use a black/blue pen for hard-copy assessments.",
    "No liquid paper / correction tape.",
    "Scripts are collected when time is up.",
]

LMS_URL = "https://lms-tms.tertiaryinfotech.com/"

def add_hyperlink(p, url, text):
    """Add a real clickable Word hyperlink (blue, underlined) to paragraph p."""
    r_id = p.part.relate_to(
        url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True)
    link = OxmlElement("w:hyperlink"); link.set(qn("r:id"), r_id)
    run = OxmlElement("w:r"); rPr = OxmlElement("w:rPr")
    sz = OxmlElement("w:sz"); sz.set(qn("w:val"), "22"); rPr.append(sz)  # 11pt
    color = OxmlElement("w:color"); color.set(qn("w:val"), "0563C1"); rPr.append(color)
    u = OxmlElement("w:u"); u.set(qn("w:val"), "single"); rPr.append(u)
    run.append(rPr)
    t = OxmlElement("w:t"); t.text = text; run.append(t)
    link.append(run); p._p.append(link)
    return link

def instructions(doc, minutes_text):
    heading(doc, "Instructions to Candidate")
    # None marks the upload instruction, which carries a clickable LMS hyperlink.
    items = [
        "This is an individual exercise.",
        "This is an open-book assessment.",
        f"A total of {minutes_text} is given to complete this assessment.",
        None,
    ] + BRIEFING
    for i, s in enumerate(items, 1):
        p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(4)
        if s is None:
            p.add_run(f"{i}.  Complete your answers on the document provided and "
                      "upload the completed answers to the LMS at ").font.size = Pt(11)
            add_hyperlink(p, LMS_URL, LMS_URL)
            p.add_run(".").font.size = Pt(11)
        else:
            p.add_run(f"{i}.  {s}").font.size = Pt(11)

def grading(doc, what):
    heading(doc, "Grading")
    para(doc, what, size=11, after=12)
    for ln in ["Grade: _______  (C / NYC)",
               "Assessor Name: __________________________   Assessor NRIC: ________________",
               "Date: ________________________                    Signature: ____________________"]:
        p = para(doc, ln, size=11, after=FILL_GAP)
        p.paragraph_format.line_spacing = 2.0

def finish(doc, path):
    prodoc.add_page_numbers(doc); prodoc.enable_update_fields(doc)
    doc.save(path); print("  saved:", os.path.basename(path))

# ---------------------------------------------------------------- builders
def build_wa(answers):
    doc = base_doc()
    kind = "Written Assessment (SAQ) — Answer Key" if answers else "Written Assessment (SAQ)"
    prodoc.add_cover_page(doc, kind, TITLE, A_VER if answers else Q_VER,
                          org_logo=ORG_LOGO, course_logo=COURSE_LOGO)
    para(doc, TITLE, size=15, bold=True, color=DARK, align=WD_ALIGN_PARAGRAPH.CENTER, after=2)
    para(doc, "Answers to Written Assessment (SAQ)" if answers else "Written Assessment (SAQ)",
         size=13, bold=True, color=BRAND, align=WD_ALIGN_PARAGRAPH.CENTER, after=2)
    para(doc, f"Course Code: {COURSE_CODE}", size=11, color=GREY, align=WD_ALIGN_PARAGRAPH.CENTER, after=12)
    if not answers:
        # Page 2 — candidate information, instructions and grading; questions begin on the next page.
        candidate_block(doc); instructions(doc, WA_MINUTES)
        grading(doc, "Candidate has answered all written questions and demonstrated the underpinning "
                     "knowledge required for the course learning outcomes.")
        page_break(doc)
    para(doc, "Short-Answer Questions (Knowledge)", size=13, bold=True, color=BRAND, after=4)
    para(doc, "Answer all questions in your own words. Each question tests underpinning knowledge covered in the "
              "course slides.", size=10.5, italic=True, color=GREY, after=8)
    # In the ANSWER KEY this intro shares page 2 with the title block, so Question 1's tall
    # model-answer table would not fit in the remaining space and the renderer pushed it
    # onto the next page, leaving a blank page. Break here so every model answer in the key
    # starts on a clean page.
    if answers:
        page_break(doc)
    # Pagination is EXPLICIT — two questions to a page on the paper, one model answer to a
    # page in the key. Do not swap this for Word's keepNext/cantSplit: Word pushes an
    # oversized box to the next page, but Google Docs draws the border anyway and prints the
    # question text and the page footer straight THROUGH it. See SKILL.md → Pagination.
    per_page = 1 if answers else 2
    for i, (crit, ctx, q, pts) in enumerate(WRITTEN, 1):
        para(doc, f"Question {i}:", size=11.5, bold=True, after=2, before=6)
        para(doc, ctx, size=11, after=3)
        para(doc, f"{q}  ({crit})", size=11, bold=True, after=4)
        answer_box(doc, lines=pts if answers else None)
        if i % per_page == 0 and i < len(WRITTEN):
            page_break(doc)
    suffix = A_VER if answers else Q_VER
    name = (f"Answer to WA (SAQ) - {TITLE} - {suffix}.docx" if answers
            else f"WA (SAQ) - {TITLE} - {suffix}.docx")
    finish(doc, os.path.join(OUT, name))

def build_pp(answers):
    doc = base_doc()
    kind = "Practical Performance (PP) — Answer Key" if answers else "Practical Performance (PP)"
    prodoc.add_cover_page(doc, kind, TITLE, A_VER if answers else Q_VER,
                          org_logo=ORG_LOGO, course_logo=COURSE_LOGO)
    para(doc, TITLE, size=15, bold=True, color=DARK, align=WD_ALIGN_PARAGRAPH.CENTER, after=2)
    para(doc, "Answers to Practical Performance Assessment" if answers else "Practical Performance Assessment",
         size=13, bold=True, color=BRAND, align=WD_ALIGN_PARAGRAPH.CENTER, after=2)
    para(doc, f"Course Code: {COURSE_CODE}", size=11, color=GREY, align=WD_ALIGN_PARAGRAPH.CENTER, after=12)
    if not answers:
        # Page 2 — candidate information, instructions and grading; the problem begins on the next page.
        candidate_block(doc); instructions(doc, PP_MINUTES)
        grading(doc, "Candidate has successfully completed all PP tasks and can explain the overall "
                     "functions and features used to achieve them.")
        page_break(doc)
    para(doc, "Practical Problem", size=13, bold=True, color=BRAND, after=4)
    para(doc, "Scenario", size=11.5, bold=True, after=2)
    para(doc, SCENARIO, size=11, after=8)
    # In the ANSWER KEY the scenario shares page 2 with the title block, so Task 1's tall
    # model-answer table would not fit in the space left and the renderer pushed it to the
    # next page — leaving a blank page and Task 1 apparently missing. Break here so every
    # task in the key starts on a clean page, exactly as on the question paper.
    if answers:
        page_break(doc)
    # Practical tasks are long and their boxes are tall, so they get a page each — on the
    # paper AND in the key. Same rule as the WA: the page break is ours, not the renderer's.
    for i, (label, crit, prompt, cap, pts) in enumerate(PRACTICAL, 1):
        para(doc, f"{label} ({crit}):", size=11.5, bold=True, after=2, before=6)
        para(doc, prompt, size=11, after=3)
        para(doc, cap, size=10.5, italic=True, color=GREY, after=4)
        answer_box(doc, lines=pts if answers else None, height_pt=150)
        if i < len(PRACTICAL):
            page_break(doc)
    suffix = A_VER if answers else Q_VER
    name = (f"Answer to PP Assessment - {TITLE} - {suffix}.docx" if answers
            else f"PP Assessment - {TITLE} - {suffix}.docx")
    finish(doc, os.path.join(OUT, name))

if __name__ == "__main__":
    print("Building WSQ assessment set…")
    build_wa(answers=False); build_wa(answers=True)
    build_pp(answers=False); build_pp(answers=True)
    print(f"Done. WA: {len(WRITTEN)} questions · PP: {len(PRACTICAL)} tasks.")
