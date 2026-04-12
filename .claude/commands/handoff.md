Write a session handoff to `geth/geth-memory/`. Read these first:

- The active program's `memory.md`
- Recent session logs in `geth/geth-memory/`

## Format

File: `geth/geth-memory/YYYY-MM-DD-{program}-{description}.md`

```markdown
## State
- Branch: {current branch}
- Uncommitted files: {list}
- Last commit: {hash + message}

## Done
{What was accomplished this session}

## Pending
{What still needs to happen}

## Corrections absorbed
{Any corrections Karl gave during this session}

## Context files (read these first)
{Files the next session needs to read to pick up where we left off}

## Next steps
{Specific, actionable next steps}
```

After writing the handoff:
1. Add a reference to the program's `memory.md`
2. If memory.md is approaching 100 lines, do a self-correction pass
