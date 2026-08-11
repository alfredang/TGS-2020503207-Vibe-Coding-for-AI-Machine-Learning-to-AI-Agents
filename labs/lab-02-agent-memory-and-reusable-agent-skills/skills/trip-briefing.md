---
name: trip-briefing
description: Use when the user asks for a travel or trip briefing for a city.
---

# Trip Briefing

Produce a briefing in exactly this structure:

1. **Weather** — current conditions and what to pack.
2. **Getting around** — the main public transport option.
3. **One local tip** — something a first-time visitor would miss.

Rules:
- Keep each section to two sentences or fewer.
- Call recall_facts first; if the user has a stored home_city, note the
  time-zone difference from it.
- If you do not know something, say so rather than inventing it.
