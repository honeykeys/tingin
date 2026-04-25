---
model: sonnet
---

You are the program winding down. The session has a shape.

Context: $ARGUMENTS

## Pattern

1. **Write session log** to `geth/geth-memory/YYYY-MM-DD-kn-{program}-{description}.md`:
   - **Context**: what was the task
   - **What was done**: files changed, decisions made, findings (especially API quirks discovered, e.g., OpenReward `RunToolOutput.root.output` shape)
   - **What the next session needs to know**: critical handoff — the quality of this block determines whether the next runtime can continue without re-investigation
   - **Corrections absorbed**: any feedback from Karl this session
2. **Update the absorbing program's `memory.md`**: ONE-LINE index entry pointing to the session log. Distilled learnings only. Not a journal.
3. **Update `relationships.md`** proactively. If you coordinated with another program this session (even via the orchestrator), update. Relationships.md drifts fastest.
4. **Check for uncommitted code**: `git status`. List any modified files at risk of being stranded.
5. **Check for unstaged geth-memory files**: session logs from earlier today that were not added to the index.
6. **If code is uncommitted**: recommend commit or stash before closing. Name the files at risk.
7. **If a spec was followed**: note any deviations from the spec for the next session — and whether they should be folded back into the spec or left as one-off pragmatism.

## Handoff Block

Before ending, write a handoff block at the top of the session log so the next `/takeoff` has a clear entry point:

```
## HANDOFF
**Branch:** [name]
**Last commit:** [sha + msg]
**Pending:** [1-3 bullets of what remains]
**Next steps:** [first action the next session takes]
**Context files:** [3-5 file paths the next session must read]
**Recommended program:** [program name]
```

## Guardrails

- DO NOT skip under velocity pressure. The handoff IS the product. A session without a handoff is a session the next runtime must reconstruct from scratch.
- `memory.md` is an INDEX. One-line entries. Distilled learnings. NOT journal entries.
- Session logs go in their own files in `geth/geth-memory/`, not inline in `memory.md`.
- The uncommitted-code check is non-negotiable even on quick wind-downs — that is where sessions strand work.
- Convert relative dates to absolute dates in session logs ("tomorrow" → "2026-04-26") so they remain interpretable.
- For hackathon/deadline work, surface time-pressure decisions explicitly: "cut X to ship Y" so the next session knows what was traded.
