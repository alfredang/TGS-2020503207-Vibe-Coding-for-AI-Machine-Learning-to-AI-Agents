#!/usr/bin/env python3
"""Generate the WSQ "AI Vibe Coding for Multi-Agents System" (TGS-2020503207) Lesson Plan (LP) DOCX.

Cover page + Document Version Control Record + auto TOC + Arial 11pt body +
colour-coded 2-day schedule tables (9:30am-6:30pm, 8 training hours/day, 1h lunch,
tea breaks within, final assessment on Day 2). Topics/labs come from course_data +
the domain data files so the LP stays aligned with the deck, guide and labs.
"""
import os, sys
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import course_data as C
from data_domain1 import DOMAIN1; from data_domain2 import DOMAIN2
from data_domain3 import DOMAIN3; from data_domain4 import DOMAIN4
from data_domain5 import DOMAIN5
ACT=DOMAIN1+DOMAIN2+DOMAIN3+DOMAIN4+DOMAIN5
import prodoc
def _find_repo(start):
    env=os.environ.get("COURSE_REPO")
    if env and os.path.isdir(env): return env
    d=start
    for _ in range(8):
        d=os.path.dirname(d)
        if os.path.isdir(os.path.join(d,"courseware")) and os.path.isdir(os.path.join(d,"labs")): return d
    return os.path.dirname(os.path.dirname(HERE))
REPO=_find_repo(HERE); ASSETS=os.path.join(os.path.dirname(HERE),"assets")

BRAND=RGBColor(0x1F,0x6F,0xEB); DARK=RGBColor(0x11,0x18,0x27); GREY=RGBColor(0x55,0x5B,0x66)
HEADER_FILL="1F6FEB"; TOPIC_FILL="E8F0FE"; BREAK_FILL="FFF4E5"; LUNCH_FILL="FDE9D9"; ASSESS_FILL="E8F7EE"

def lab_titles(nums):
    return "; ".join(f"Lab {a['num']}: {a['title']}" for a in ACT if a['num'] in nums)

# Slide-number index — the deck's page numbering, so the LP can cite slides.
# Regenerated alongside build_slides.py; verified by scripts/check_slide_refs.py.
SLIDE_REF = {}

# ------------------------------------------------ schedule (single source of truth for timing)
# (start, end, minutes, kind, activity_text)  kind: admin/topic/lab/break/lunch/assess/recap
SCHEDULE = {
 1: (C.DAY_THEMES[1], [
    ("9:30","10:00",30,"admin","Welcome, trainer and learner introductions, ground rules, learning outcomes, course outline and mandatory digital attendance (AM)"),
    ("10:00","11:00",60,"topic","Topic 1 — Modern Agent Foundations: what a modern AI agent is, the reason-act-observe loop, agent skills, memory, tools and the Model Context Protocol; the progression from single-agent to multi-agent collaboration (concepts + demonstration)"),
    ("11:00","11:15",15,"break","Tea break"),
    ("11:15","13:00",105,"lab","Hands-on: "+lab_titles([1,2])),
    ("13:00","14:00",60,"lunch","Lunch break"),
    ("14:00","15:00",60,"topic","Topic 2 — Vibe Coding for Multi-Agent Systems: the structured vibe coding workflow, context engineering, the vibe coding tool landscape and agent skills integration (concepts + demonstration). Digital attendance (PM)"),
    ("15:00","16:30",90,"lab","Hands-on: "+lab_titles([3,4])),
    ("16:30","16:45",15,"break","Tea break"),
    ("16:45","17:30",45,"topic","Topic 3 — Multi-Agent System Development with OpenAI Agents SDK: agents, runners, function tools and Pydantic structured outputs (concepts + demonstration)"),
    ("17:30","18:45",75,"lab","Hands-on: "+lab_titles([5])),
    ("18:45","19:00",15,"recap","Day 1 recap, Q&A and confirmation of digital attendance"),
 ]),
 2: (C.DAY_THEMES[2], [
    ("9:30","9:45",15,"recap","Day 1 recap and mandatory digital attendance (AM)"),
    ("9:45","10:15",30,"topic","Topic 3 continued — supervisor routing, sub-agent delegation, handoffs and guardrails (concepts + demonstration)"),
    ("10:15","11:15",60,"lab","Hands-on: "+lab_titles([6])),
    ("11:15","11:30",15,"break","Tea break"),
    ("11:30","12:30",60,"lab","Hands-on: "+lab_titles([7])),
    ("12:30","13:00",30,"topic","Topic 4 — Multi-Agent System Development with Gemini Agent SDK: agent design in the Google ADK and comparison with the OpenAI Agents SDK (concepts + demonstration)"),
    ("13:00","14:00",60,"lunch","Lunch break"),
    ("14:00","15:30",90,"lab","Hands-on: "+lab_titles([8,9])+". Digital attendance (PM)"),
    ("15:30","15:45",15,"break","Tea break"),
    ("15:45","16:15",30,"topic","Topic 5 — MCP and Sub-Agents: MCP servers and tool orchestration in depth, and hierarchical sub-agent architecture (concepts + demonstration)"),
    ("16:15","18:00",105,"lab","Hands-on: "+lab_titles([10,11])),
    ("18:00","18:30",30,"recap","Course revision and summary, course feedback and TRAQOM survey"),
    ("18:30","18:45",15,"assess","Briefing for Assessment and Assessment digital attendance"),
    ("18:45","19:00",15,"assess","Final Assessment administration — the Written Assessment (WA, SAQ, 50 minutes) and Practical Performance (PP, 75 minutes) are conducted as scheduled by the assessment centre"),
 ]),
}

# ------------------------------------------------ build document
doc=Document()
normal=doc.styles["Normal"]; normal.font.name="Arial"; normal.font.size=Pt(11)
prodoc.style_headings(doc)

prodoc.add_cover_page(doc,"LESSON PLAN",C.TITLE,C.VERSION.lstrip("v"),
                      org_logo=os.path.join(ASSETS,"tertiary-infotech-logo.png"),
                      course_logo=None, course_code=C.COURSE_CODE)
prodoc.add_version_control(doc,[
 ("1.0",C.VERSION_DATE,
  "Initial release — 2-day lesson plan for AI Vibe Coding for Multi-Agents System, aligned to the "
  "published course outline (Topics 1-5) and the 11 hands-on labs.",C.TRAINER),
])
prodoc.add_toc(doc)

def H(text,level=1):
    return doc.add_heading(text,level=level)

H("Course Information",1)
info=[("Course Title",C.TITLE),("WSQ Course Reference",C.COURSE_CODE),
      ("Training Provider",C.ORG+"  ("+C.UEN.replace('UEN: ','UEN ')+")"),
      ("Skills Framework",f"{C.TSC_TITLE}  ({C.TSC_CODE})"),
      ("Duration",f"{C.DAYS} days · 8 instructional hours per day (16 hours), plus assessment "
                  "(WA 50 minutes + PP 75 minutes)"),
      ("Daily Timing","9:30 am – 7:00 pm (8 instructional hours, plus a 1-hour lunch and two 15-minute tea breaks)"),
      ("Mode","Instructor-led, hands-on multi-agent development labs in Python"),
      ("Trainer",C.TRAINER)]
t=doc.add_table(rows=0,cols=2); t.style="Table Grid"
for k,v in info:
    c=t.add_row().cells; c[0].text=""; r=c[0].paragraphs[0].add_run(k); r.bold=True; r.font.size=Pt(10)
    prodoc._shade_cell(c[0],TOPIC_FILL)
    c[1].text=""; c[1].paragraphs[0].add_run(v).font.size=Pt(10)

H("Learning Outcomes",1)
doc.add_paragraph("On completion of this course, learners will be able to:")
for lo in C.LEARNING_OUTCOMES:
    p=doc.add_paragraph(style="List Bullet"); p.add_run(lo).font.size=Pt(10.5)

H("Skills Framework Alignment",1)
doc.add_paragraph(f"TSC Title: {C.TSC_TITLE}    |    TSC Code: {C.TSC_CODE}")
for ab in C.TSC_ABILITIES:
    p=doc.add_paragraph(style="List Bullet"); p.add_run(ab).font.size=Pt(10.5)

H("Assessment",1)
for a in [C.ASSESSMENT["written"],C.ASSESSMENT["practical"],
          "Format: Open Book — course slides, Learner Guide and approved materials only.",
          "The final assessment is conducted at the end of Day 2.",C.ASSESSMENT["note"]]:
    p=doc.add_paragraph(style="List Bullet"); p.add_run(a).font.size=Pt(10.5)

H("Training Resources",1)
for a in ["Course slide deck (Trainer Slides / Learner Slides) — downloadable from the LMS/TMS portal.",
          "Learner Guide — full detailed step-by-step instructions for all 11 hands-on labs.",
          f"Lab code repository: {C.REPO_URL}",
          "Learner laptop with Python 3.11 or later, an IDE or terminal, and internet access.",
          "API keys for the model providers used in the labs (OpenAI and Google AI Studio).",
          f"LMS/TMS portal: {C.LMS_URL}"]:
    p=doc.add_paragraph(style="List Bullet"); p.add_run(a).font.size=Pt(10.5)

def set_cell(cell,text,bold=False,size=9.5,color=None,fill=None,align=None):
    cell.text=""; p=cell.paragraphs[0]
    if align: p.alignment=align
    r=p.add_run(text); r.bold=bold; r.font.size=Pt(size); r.font.name="Arial"
    if color: r.font.color.rgb=color
    if fill: prodoc._shade_cell(cell,fill)

KIND_FILL={"topic":TOPIC_FILL,"break":BREAK_FILL,"lunch":LUNCH_FILL,"assess":ASSESS_FILL,
           "admin":"F3F5F8","recap":"F3F5F8","lab":None}

H("Course Schedule",1)
for day,(theme,rows) in SCHEDULE.items():
    H(f"Day {day} — {theme}",2)
    tbl=doc.add_table(rows=0,cols=3); tbl.style="Table Grid"; tbl.alignment=WD_TABLE_ALIGNMENT.CENTER
    hdr=tbl.add_row().cells
    for i,htext in enumerate(["Time","Duration","Topic / Activity"]):
        set_cell(hdr[i],htext,bold=True,size=10,color=RGBColor(0xFF,0xFF,0xFF),fill=HEADER_FILL)
    training=0
    for start,end,mins,kind,text in rows:
        cells=tbl.add_row().cells; fill=KIND_FILL.get(kind)
        set_cell(cells[0],f"{start}–{end}",bold=(kind in ("topic","assess")),size=9.5,fill=fill)
        set_cell(cells[1],f"{mins} min",size=9.5,fill=fill)
        set_cell(cells[2],text,bold=(kind in ("topic","assess")),size=9.5,fill=fill)
        # Instructional time excludes BOTH the lunch break and the tea breaks.
        if kind not in ("lunch","break"): training+=mins
    for row in tbl.rows:
        row.cells[0].width=Inches(1.15); row.cells[1].width=Inches(0.9); row.cells[2].width=Inches(4.75)
    p=doc.add_paragraph(); r=p.add_run(f"Total instructional time: {training} minutes ({training//60} hours), "
                                       "excluding the 1-hour lunch and two 15-minute tea breaks.")
    r.italic=True; r.font.size=Pt(9.5); r.font.color.rgb=GREY
    assert training==480, f"Day {day} instructional minutes = {training}, expected 480"

H("Lab Reference (aligned to the course outline)",1)
tt=doc.add_table(rows=0,cols=3); tt.style="Table Grid"
hdr=tt.add_row().cells
for i,htext in enumerate(["Topic","Weighting","Labs"]):
    set_cell(hdr[i],htext,bold=True,size=10,color=RGBColor(0xFF,0xFF,0xFF),fill=HEADER_FILL)
for tp in C.TOPICS:
    acts=[a for a in ACT if a["topic"]==tp["num"]]
    cells=tt.add_row().cells
    set_cell(cells[0],f"Topic {tp['code']}: {tp['title']}",bold=True,size=9.5,fill=TOPIC_FILL)
    set_cell(cells[1],tp["weighting"],size=9.5,fill=TOPIC_FILL)
    set_cell(cells[2],", ".join(f"Lab {a['num']}" for a in acts),size=9.5)

H("Learning Outcome to Lab Mapping",1)
lm=doc.add_table(rows=0,cols=3); lm.style="Table Grid"
hdr=lm.add_row().cells
for i,htext in enumerate(["Learning Outcome","Topic","Assessed by"]):
    set_cell(hdr[i],htext,bold=True,size=10,color=RGBColor(0xFF,0xFF,0xFF),fill=HEADER_FILL)
for i,lo in enumerate(C.LEARNING_OUTCOMES,1):
    tp=C.TOPICS[i-1]
    acts=[a for a in ACT if a["topic"]==tp["num"]]
    cells=lm.add_row().cells
    set_cell(cells[0],lo,size=9.5)
    set_cell(cells[1],f"Topic {tp['code']} ({', '.join('Lab '+str(a['num']) for a in acts)})",size=9.5,fill=TOPIC_FILL)
    set_cell(cells[2],"WA (SAQ) + PP",size=9.5)

prodoc.add_page_numbers(doc)
prodoc.enable_update_fields(doc)
OUT=os.path.join(REPO,"courseware",f"LP-{C.SHORT_TITLE}.docx")
doc.save(OUT)
print("Saved",OUT)
