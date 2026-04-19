---
name: recall
description: Search team memory for past learnings, solutions, and decisions
allowed-tools:
  - Bash
---

# Recall Learnings

Search the persistent memory system for relevant past learnings.

## Usage

The user will provide a search query. Run the recall script with their query:

```bash
uv run python scripts/core/recall_learnings.py --query "<user's query>"
```

## How It Works

By default, searches git-native markdown files in `knowledge/learnings/` using text matching.
If `DATABASE_URL` is configured, also searches PostgreSQL with semantic vector search and merges results.

## Options

- `--k N`: Return N results (default 5)
- `--backend git|postgres|auto`: Force a specific backend (default: auto)
- `--text-only`: Fast text-only search (PostgreSQL mode)
- `--vector-only`: Pure semantic search (PostgreSQL mode)
- `--scope team|private|all`: Filter by scope (PostgreSQL mode)
- `--json`: Output as JSON for programmatic use

## Interpreting Results

- Git-native results show normalized text-match scores (0-1)
- Hybrid RRF scores of 0.01-0.03 are normal and indicate good PostgreSQL matches
- Each result shows its source (`[git]` or `[postgres]`)

## No Database? No Problem

Git-native search works out of the box with no infrastructure. Share learnings via `git push/pull`.
