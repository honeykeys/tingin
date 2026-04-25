---
model: sonnet
---

You are generating a pre-demo manual test checklist for the Tingin Streamlit app. Karl needs to know exactly what to click and check before walking into the venue. Be specific — no generic advice.

$ARGUMENTS

## Pattern

**If $ARGUMENTS contains a feature description or recent change:**
- Use it as the primary source of truth for what to test extra-hard.

**If $ARGUMENTS is empty:**
- Run `git log --oneline -5` to identify what just shipped.
- Read the most recent file in `geth/geth-memory/` for context on what changed.
- Read `geth/specs/2026-04-25-hackathon-demo.md` Section 5 (App Flow) and Section 10 (Done = Shippable) as the test corpus.

Then:
1. Identify every surface the demo touches: sidebar, floor view, handoff view, finale view, MDP view.
2. For each surface, write test cases covering:
   - **Happy path** — feature works with seed=42 data
   - **Both runs** — Run A and Run B both produce the expected narrative
   - **Edge cases** — replay, speed slider, researcher mode toggle, navigation between views
3. Add a "Won't see yet" section for anything explicitly cut from the spec (CNA role, Charge nurse, live LLM rollouts, training integration).

## Format

Group by surface. Numbered list within each group. Keep each item to one sentence — what to do and what to expect.

```
[Surface name] (sidebar item or view)
1. [Action] — [expected result]
2. [Action] — [expected result]

[Next surface]
...

What you won't see yet (explicitly cut)
- [item and reason from spec Section 4]
```

## Tingin-specific must-checks

- **Seed determinism** — both runs produce the same NEWS2 trajectories every time. If a rerun produces different output, the seed isn't being applied.
- **Handoff red highlights** — in Run B, the ambient signal for P2 must show in red on the left panel (lost in compression). In Run A, no red.
- **NEWS2 axis labels** — y-axis "NEWS2 score 0–10", x-axis "tick (0–40)". No unitless numbers.
- **Three-panel hold time** — handoff screen should pause 2–3 seconds before allowing "Continue to shift 2." Too fast and judges miss the moment.
- **Tool-call feed** — every action timestamped, reward delta visible per call.
- **External display rendering** — fonts ≥ 14pt, charts not clipped, dark theme actually loaded (not light fallback).

## Guardrails

- READ-ONLY. Do not modify any files.
- No Geth vocabulary in the output. Plain English. Judges don't read CLAUDE.md.
- Be specific: name the UI elements, labels, and data as they appear in the app — not as they appear in code.
- If a test requires specific seed data, say so (e.g., "seed=42 must be set in `app.py`").
- Do not pad the list. If a surface only has two meaningful things to test, write two.
