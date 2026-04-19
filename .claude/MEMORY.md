# Personal Memory

## Active Projects

<!-- Add a subsection for each active project, detailing: the following sections for each -->

### Key Directories

<!-- Fill with important directories and their purposes for relevant repos -->

### Patterns

<!-- Fill with patterns I use for this specific project, e.g. for state management, API calls, error handling, etc.-->

## Personal Patterns

<!-- Fill with patterns I use across projects to maintain consistency and efficiency in my work. Examples include: -->

- Prefers concise, direct communication
  <!-- - Has extensive Postgres rules (RLS, locking, queries, schema, connections, maintenance) -->
  <!-- - Has Supabase workflow rules (MCP-first, SSR auth, Edge Functions) -->
  <!-- - Uses Company Claude memory system (recall/store learnings via scripts) -->
- No Claude co-authoring attribution in commits
- GPG signature of commits is a must. If failed, prompt user to sign themselves
- Use bun when possible

## Recall System

```bash
# Recall learnings
cd $CLAUDE_OPC_DIR && PYTHONPATH=. uv run python scripts/core/recall_learnings.py --query "topic"
# Store learnings
cd $CLAUDE_OPC_DIR && PYTHONPATH=. uv run python scripts/core/store_learning.py --session-id "id" --type TYPE --content "..." --confidence high
```
