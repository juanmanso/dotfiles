---
name: store
description: Store a new learning from the current session into persistent memory
allowed-tools:
  - Bash
---

# Store Learning

Store a new learning into the persistent memory system.

## Usage

Extract what the user wants to remember, then run:

```bash
uv run python scripts/core/store_learning.py \
  --session-id "<short-identifier>" \
  --type <TYPE> \
  --content "<what was learned>" \
  --context "<what it relates to>" \
  --tags "tag1,tag2" \
  --confidence high|medium|low
```

## How It Works

Always writes a markdown file to `knowledge/learnings/` (git-native, works everywhere).
If `DATABASE_URL` is configured, also stores in PostgreSQL with pgvector embedding for semantic search.

## Learning Types

| Type | Use For |
|------|---------|
| `ARCHITECTURAL_DECISION` | Design choices, system structure |
| `WORKING_SOLUTION` | Fixes and solutions that worked |
| `CODEBASE_PATTERN` | Patterns discovered in code |
| `FAILED_APPROACH` | What didn't work (avoid repeating) |
| `ERROR_FIX` | How specific errors were resolved |
| `USER_PREFERENCE` | User's preferred approaches |

## Sharing

Learnings are shared via `git push/pull`. Run `uv run python scripts/sync/git_sync.py --sync` to sync with the team, or `--watch` for auto-sync.

## Guidelines

- Use descriptive session IDs (e.g., "auth-refactor", "hook-debugging")
- Include context so future searches can find this learning
- Use high confidence only when certain the learning is correct and broadly applicable
