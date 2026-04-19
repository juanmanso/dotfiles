---
name: status
description: Show memory system dashboard with learning stats and team activity
allowed-tools:
  - Bash
---

# Memory Status Dashboard

Show the current state of the memory system.

## Usage

```bash
uv run python scripts/sync/status.py
```

## What It Shows

- Total learning counts by scope (private, team, org)
- Recent learnings with timestamps
- Active sessions
- Team activity summary

## Additional Views

Browse learnings by scope:
```bash
uv run python scripts/sync/list_learnings.py                  # your private
uv run python scripts/sync/list_learnings.py --scope team      # team learnings
uv run python scripts/sync/list_learnings.py --scope all       # everything
```

Present the results in a clear, readable format.
