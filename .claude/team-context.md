# Quantinium Dev Team

_Team members receive updates automatically on `git pull`._
_Last updated: 2026-03-16_

## Tech Stack

- **Language**: Python 3.12+
- **Package Manager**: uv (not pip)
- **Storage**: Git-native markdown (default), PostgreSQL 16 + pgvector (optional)
- **Embeddings**: BGE-large-en-v1.5 (local, 1024-dim, via sentence-transformers)
- **Linting**: ruff (line-length 100)
- **Testing**: pytest + pytest-asyncio
- **Build**: hatchling

## Coding Standards

- Use `X | None` over `Optional[X]`, `list[T]` over `List[T]` (Python 3.12+ syntax)
- Use `TYPE_CHECKING` guard for type-only imports that cause circular deps
- All database columns use UUID PKs and TIMESTAMPTZ timestamps
- Use TEXT + CHECK constraints over ENUM types
- Enable RLS on all public tables, wrap `auth.uid()` in `(SELECT auth.uid())`
- Run `make verify` (lint + test) before committing

## Architecture Decisions

- Git-native storage as default — learnings stored as markdown in `knowledge/learnings/`, shared via git
- PostgreSQL + pgvector as optional enhancement for semantic search (when DATABASE_URL is set)
- Three-tier scoping: private → team → org with auto-promotion for high-confidence
- Fire-and-forget pattern for hooks that do heavy work (output `no_block`, spawn detached)
- Team sharing via `git push/pull` — works in AWS VPC/SSM without network access to shared DB

## Current Sprint Focus

Sprint: Infrastructure Hardening | Ends: 2026-03-30

- [x] Add comprehensive test suite (80+ tests)
- [x] Set up CI/CD pipeline
- [x] Create Claude Code plugin structure (skills, agents, rules)
- [x] Consolidate hooks (15 → 5) and rules (29 → 9)
- [x] Implement git-native learning storage (markdown + YAML frontmatter)
- [x] Add git sync for team sharing (push/pull)
- [ ] Convert remaining DB-only scripts (status.py, list_learnings.py) to git-native

## Team Members

| Name | COMPANY_USER_ID | Role           | Focus Area                  |
| ---- | --------------- | -------------- | --------------------------- |
| Juan | juam            | Lead Developer | Architecture, memory system |

## Useful Commands

```bash
make dev                           # Install all deps
make verify                        # Lint + test
make test-cov                      # Test with coverage
uv run python scripts/sync/status.py                              # Dashboard
uv run python scripts/core/recall_learnings.py --query "<topic>"  # Search memory
uv run python scripts/core/store_learning.py --session-id "id" --type WORKING_SOLUTION --content "..." --confidence high
uv run python scripts/sync/git_sync.py --sync                     # Sync learnings with team
```

## Shared Resources

- **Git repo**: company-claude-dev (private)
- **Learnings**: `knowledge/learnings/` (git-native markdown files)
- **Docs**: `knowledge/` directory + CLAUDE.md at project root
- **DB** (optional): `postgresql://company:company@localhost:5432/company_claude`
