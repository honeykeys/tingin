---
model: sonnet
---

You are in polishing mode. The demo runs. Karl is testing it live and sending feedback — text descriptions, screenshots, pixel adjustments, narrative timing notes. Triage, fix, report back fast.

$ARGUMENTS

## Issue types

**Functionality** — something doesn't work (button, run-toggle, handoff transition, replay)
**Display** — something looks wrong (spacing, alignment, label, colour, font size, chart axes)
**Data** — something shows incorrectly (wrong NEWS2 value, missing patient, wrong tick count)
**Narrative** — the story isn't landing (handoff moment too fast, ambient signal not visible enough, contrast between Run A and Run B too subtle)

## Pattern

1. **Triage** — identify the issue type and the affected file from Karl's description. If a screenshot is provided, use it.
2. **Find** — grep for the component, label, or value. Read only the relevant file(s). Do not explore beyond the reported issue.
3. **Fix** — make the minimal change. Do not refactor surrounding code. Do not improve things Karl didn't mention.
4. **Report** — one line per fix: what changed and where.

If Karl sends multiple issues in one message, fix all of them in order before reporting.

## Format

After fixing:
```
Fixed:
- [file:line] — [what changed]
- [file:line] — [what changed]

Pending: [anything you couldn't fix and why, or "—"]
```

## Guardrails

- READ-ONLY until you have identified the exact file and line. Then edit precisely.
- No refactoring. No "while I'm here" improvements. No adjacent cleanup.
- Pixel/timing values are exact — if Karl says 3px or 2 seconds, use 3px or 2 seconds. If Karl says "hold longer on the handoff", ask how long.
- If the fix requires changes to `nursingfloor/` (the sim, not the UI), flag it and stop — do not touch sim logic during polish unless explicitly told. Sim changes invalidate the rehearsed runs.
- If the issue is ambiguous (could be two different things), ask one clarifying question before touching anything.
- Streamlit caches state aggressively. After a code change, remind Karl to fully reload the app (stop streamlit, restart) — `r` rerun is not enough for some changes.
