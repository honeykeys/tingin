---
model: sonnet
---

You are continuing work from a previous session. A handoff prompt exists with everything you need.

$ARGUMENTS

## Pattern

1. **Read the handoff.** The first argument is a path to a handoff prompt file (in `geth/geth-memory/`). If no path is provided, find the most recent `*handoff*.md` or session log file in `geth/geth-memory/` (`ls -t geth/geth-memory/ | head -3`).

2. **Read the context files.** The handoff lists 3–5 files under "Context files." Read ALL of them. This is non-negotiable — these were selected as the minimum set for you to be effective.

3. **Read the active spec.** If a spec is referenced (e.g., `geth/specs/2026-04-25-hackathon-demo.md`), read it. Specs define the bar; without the bar, you cannot judge whether a deviation is improvement or drift.

4. **Verify state.** Check that reality matches the handoff:
   - `git branch --show-current` — does it match the handoff's branch?
   - `git status` — do uncommitted files match what the handoff claims?
   - `git log --oneline -3` — does the last commit match?
   - If state has DIVERGED from the handoff (someone else committed, branch was merged, files were changed): report the divergence before proceeding. Do not assume the handoff is current.

5. **Report ready.** Summarize in 3–4 lines:
   - What the previous session completed
   - What remains (from the handoff's "Pending" section)
   - What you will do first (from "Next steps")
   - Which program/skill is recommended

6. **Check background processes.** If the handoff mentions running dev servers (streamlit, jupyter), verify whether they are still running on the expected ports.

7. **Enter the recommended program's mode.** The handoff names a program under "Recommended program." Read `geth/programs/{name}/understanding.md`, `memory.md`, `relationships.md`. Adopt that program's patterns.

## If combined with another command

Karl may provide a program name alongside the handoff path. In that case:
- Read the handoff for state and context
- But enter the specified program's mode, not the handoff's recommendation

## Guardrails

- DO NOT start working before reading all context files. The previous session selected them for a reason.
- DO NOT trust the handoff blindly. Verify branch, uncommitted files, and last commit. Handoffs can be stale.
- If the handoff references files that do not exist: report it. Something was deleted or never committed.
- If there is no handoff file and no path provided: check `geth/geth-memory/` for the most recent session log and reconstruct context from there. This is the fallback, not the happy path.
