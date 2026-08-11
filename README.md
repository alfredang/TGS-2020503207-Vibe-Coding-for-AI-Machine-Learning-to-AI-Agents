# WSQ AI Vibe Coding for Multi-Agents System

[![WSQ](https://img.shields.io/badge/WSQ-TGS--2020503207-1F6FEB)](https://www.tertiarycourses.com.sg/wsq-ai-vibe-coding-for-multi-agents-system.html)
[![Duration](https://img.shields.io/badge/Duration-2%20days%20%C2%B7%2016%20hours-10B981)](#lesson-plan)
[![Level](https://img.shields.io/badge/Level-Intermediate-7C3AED)](#prerequisites)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)

Course materials for the WSQ course **AI Vibe Coding for Multi-Agents System** (TGS-2020503207),
conducted by **Tertiary Infotech Academy Pte Ltd** (UEN 201200696W).

Build collaborative multi-agent AI systems — from a single tool-calling agent to hierarchical
sub-agents coordinated over the Model Context Protocol — using vibe coding as the build method.

---

## What you will build

| # | Lab | Topic | You build |
|---|-----|-------|-----------|
| 1 | [Build Your First Tool-Calling Agent](labs/lab-01-build-your-first-tool-calling-agent.md) | 1 | An agent loop with two of your own tools |
| 2 | [Agent Memory and Reusable Agent Skills](labs/lab-02-agent-memory-and-reusable-agent-skills.md) | 1 | Short-term + persistent memory, and a skill file |
| 3 | [Vibe Code an Agent with a Structured Workflow](labs/lab-03-vibe-code-an-agent-with-a-structured-workflow.md) | 2 | A research agent generated from your SPEC.md |
| 4 | [Context Engineering and a Reusable Coding Skill](labs/lab-04-context-engineering-and-a-reusable-coding-skill.md) | 2 | A project context file and a reusable skill |
| 5 | [First Agent with the OpenAI Agents SDK](labs/lab-05-first-agent-with-the-openai-agents-sdk.md) | 3 | An SDK agent with Pydantic structured output |
| 6 | [Supervisor Routing and Sub-Agent Delegation](labs/lab-06-supervisor-routing-and-sub-agent-delegation.md) | 3 | A triage supervisor over three specialists |
| 7 | [Deploy the Multi-Agent System with Streamlit](labs/lab-07-deploy-the-multi-agent-system-with-streamlit.md) | 3 | A Streamlit chat app with visible routing |
| 8 | [Build a Multi-Agent System with the Gemini Agent SDK](labs/lab-08-build-a-multi-agent-system-with-the-gemini-agent-sdk.md) | 4 | A Gemini coordinator with sub-agents |
| 9 | [Deploy the Gemini Multi-Agent System with Streamlit](labs/lab-09-deploy-the-gemini-multi-agent-system-with-streamlit.md) | 4 | The Gemini system deployed + an SDK comparison |
| 10 | [Build and Connect an MCP Server](labs/lab-10-build-and-connect-an-mcp-server.md) | 5 | An MCP server with three typed tools |
| 11 | [Hierarchical Sub-Agents and Context Isolation](labs/lab-11-hierarchical-sub-agents-and-context-isolation.md) | 5 | A three-tier orchestrator → sub-agents → MCP |

---

## Course outline

| Topic | Title | Focus |
|-------|-------|-------|
| 1 | **Modern Agent Foundations** | Agent anatomy, skills, memory, MCP, single-agent → multi-agent |
| 2 | **Vibe Coding for Multi-Agent Systems** | The structured workflow, context engineering, tooling |
| 3 | **Multi-Agent Development with OpenAI Agents SDK** | Structured outputs, tool calling, supervisor routing, Streamlit |
| 4 | **Multi-Agent Development with Gemini Agent SDK** | Google ADK agent design, collaboration, Streamlit |
| 5 | **MCP and Sub-Agents** | MCP servers, tool orchestration, hierarchical architecture |

## Learning outcomes

- **LO1** — Explain the components of a modern AI agent (skills, memory, tools, MCP) and the progression from single-agent to multi-agent collaboration.
- **LO2** — Apply a structured vibe coding workflow with context engineering to specify, generate and verify agent code reliably.
- **LO3** — Build a collaborative multi-agent system with the OpenAI Agents SDK using structured outputs, tool calling and supervisor routing, and deploy it with Streamlit.
- **LO4** — Build a collaborative multi-agent system with the Google Gemini Agent SDK and deploy it with Streamlit.
- **LO5** — Orchestrate tools through MCP and design hierarchical sub-agent architectures for delegated, specialised work.

---

## Getting started

```bash
git clone https://github.com/tertiarycourses/TGS-2020503207-AI-Vibe-Coding-for-Multi-Agents-System.git
cd TGS-2020503207-AI-Vibe-Coding-for-Multi-Agents-System

python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r labs/requirements.txt
```

Create a `.env` file in your working folder — **never commit it**:

```bash
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...
```

Verify the setup:

```bash
python3 -c "import openai, agents, pydantic, streamlit; print('OK')"
python3 -c "from google.adk.agents import Agent; print('ADK OK')"
python3 -c "from mcp.server.fastmcp import FastMCP; print('MCP OK')"
```

## Prerequisites

- Python 3.11 or later, and a terminal + code editor (VS Code recommended).
- An OpenAI API key (Topics 1, 3, 5) and a Google AI Studio key (Topic 4).
- An AI coding agent for the vibe coding labs — Claude Code, Gemini CLI, Codex CLI, Cursor or Windsurf.
- Basic Python: functions, type hints, virtual environments.

## Tech stack

`openai` · `openai-agents` · `google-adk` · `pydantic` · `streamlit` · `mcp[cli]` · `python-dotenv`

---

## Courseware

The slide deck, Lesson Plan and Learner Guide are distributed through the
[LMS/TMS portal](https://lms-tms.tertiaryinfotech.com) — sign in with your registered email and
open **My Courses**. The **Learner Guide** carries the full detailed step-by-step for every lab and
is your open-book reference during the assessment.

Current release — **v1.0** (11 August 2026):

| Artifact | File |
|---|---|
| Trainer Slides | `courseware/AI Vibe Coding for Multi-Agents System-v1.0.pptx` (+ `.pdf`) |
| Lesson Plan | `courseware/LP-AI Vibe Coding for Multi-Agents System.docx` (+ `.pdf`) |
| Learner Guide | `courseware/LG-AI Vibe Coding for Multi-Agents System.docx` (+ `.pdf`) |
| Learner Guide (Markdown) | [`LG-AI Vibe Coding for Multi-Agents System.md`](LG-AI%20Vibe%20Coding%20for%20Multi-Agents%20System.md) |

The deck is deliberately **visual** — architecture diagrams, workflow flows and tile grids. The
per-step instructions for each lab live in the **Learner Guide** and the [`labs/`](labs/) files,
not on the slides.

> Assessment papers are confidential and are **not** published in this repository.

## Assessment

| Instrument | Format | Duration |
|---|---|---|
| Written Assessment (WA) | Short-Answer Questions (SAQ) | 50 minutes |
| Practical Performance (PP) | Hands-on multi-agent build tasks | 75 minutes |

Open book. A minimum of **75% attendance** is required to be eligible for assessment and funding.

## Funding

WSQ-funded for eligible Singapore Citizens and PRs (baseline 50%, MCES/SME 70%), with SkillsFuture
Credit, SFEC, UTAP, PSEA and Absentee Payroll support. See the
[course page](https://www.tertiarycourses.com.sg/wsq-ai-vibe-coding-for-multi-agents-system.html)
for current rates and eligibility.

## Skills Framework

**TSC:** Analytics and Computational Modelling — `ICT-DIT-3001-1.1`

---

## About

**Tertiary Infotech Academy Pte Ltd** (UEN 201200696W) · [tertiarycourses.com.sg](https://www.tertiarycourses.com.sg)
Trainer: **Dr Alfred Ang**

© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved.
