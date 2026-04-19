#!/usr/bin/env python3
"""Knowledge Relay — PostToolUse hook for Edit/Write/MultiEdit operations.

Push-based knowledge discovery: after modifying a file, this hook automatically
surfaces relevant team and org learnings from the shared memory system.

Instead of developers having to remember to /recall before every change, the
system brings relevant knowledge TO them at the exact moment of code change.

Flow:
  1. Claude calls Edit/Write/MultiEdit
  2. This hook fires (PostToolUse)
  3. Extracts file context + changed content keywords
  4. Fast text-only search against team/org scope in archival_memory
  5. Filters out recently-seen learnings (cooldown cache)
  6. Outputs relevant learnings as context injection

Configuration:
  KNOWLEDGE_RELAY_COOLDOWN_SECONDS  - how long to suppress a seen learning (default: 120)
  KNOWLEDGE_RELAY_MIN_SCORE         - minimum relevance score to surface (default: 0.005)
  KNOWLEDGE_RELAY_MAX_RESULTS       - max learnings to surface per edit (default: 2)
  KNOWLEDGE_RELAY_DISABLED          - set to '1' to disable entirely

Cache: ~/.claude/knowledge_relay_seen.json
"""
from __future__ import annotations

import asyncio
import json
import os
import re
import sys
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

COOLDOWN_SECONDS = int(os.environ.get("KNOWLEDGE_RELAY_COOLDOWN_SECONDS", "120"))
MIN_SCORE = float(os.environ.get("KNOWLEDGE_RELAY_MIN_SCORE", "0.005"))
MAX_RESULTS = int(os.environ.get("KNOWLEDGE_RELAY_MAX_RESULTS", "2"))
DISABLED = os.environ.get("KNOWLEDGE_RELAY_DISABLED", "").lower() in ("1", "true", "yes")

SEEN_CACHE_PATH = Path.home() / ".claude" / "knowledge_relay_seen.json"

# ---------------------------------------------------------------------------
# Load environment
# ---------------------------------------------------------------------------

try:
    from dotenv import load_dotenv

    # Load project .env first, then global ~/.claude/.env
    claude_project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    if claude_project_dir:
        load_dotenv(Path(claude_project_dir) / ".env")
    load_dotenv(Path.home() / ".claude" / ".env")
    load_dotenv()
except ImportError:
    pass


# ---------------------------------------------------------------------------
# Seen cache helpers
# ---------------------------------------------------------------------------


def _load_seen_cache() -> dict[str, float]:
    """Load the seen-learning cooldown cache."""
    try:
        if SEEN_CACHE_PATH.exists():
            return json.loads(SEEN_CACHE_PATH.read_text())
    except Exception:
        pass
    return {}


def _save_seen_cache(cache: dict[str, float]) -> None:
    """Persist the seen-learning cooldown cache."""
    try:
        SEEN_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        SEEN_CACHE_PATH.write_text(json.dumps(cache))
    except Exception:
        pass


def _prune_seen_cache(cache: dict[str, float]) -> dict[str, float]:
    """Remove entries older than COOLDOWN_SECONDS."""
    cutoff = time.time() - COOLDOWN_SECONDS
    return {k: v for k, v in cache.items() if v > cutoff}


# ---------------------------------------------------------------------------
# Query extraction
# ---------------------------------------------------------------------------


def _extract_query(tool_name: str, tool_input: dict) -> str | None:
    """Build a search query from the tool input."""
    parts: list[str] = []

    file_path = tool_input.get("file_path") or tool_input.get("notebook_path", "")
    if file_path:
        # Use the filename (not full path) — more useful as a search signal
        basename = Path(str(file_path)).name
        # Strip extension for cleaner search
        stem = Path(basename).stem
        # Convert snake/kebab to spaces
        stem_words = re.sub(r"[_\-]", " ", stem)
        parts.append(stem_words)

    # Extract keywords from changed content
    changed_text = ""
    if tool_name in ("Edit", "MultiEdit"):
        changed_text = tool_input.get("new_string") or ""
    elif tool_name == "Write":
        changed_text = tool_input.get("content") or ""

    if changed_text:
        # Grab first 300 chars, collapse whitespace
        snippet = " ".join(changed_text[:300].split())
        # Extract identifiers (camelCase, snake_case, function names)
        identifiers = re.findall(r"\b[a-zA-Z_][a-zA-Z0-9_]{3,}\b", snippet)
        # Take the 8 most interesting (longest tends to be most specific)
        identifiers = sorted(set(identifiers), key=len, reverse=True)[:8]
        parts.extend(identifiers)

    query = " ".join(parts).strip()
    return query if len(query) >= 5 else None


# ---------------------------------------------------------------------------
# Database search
# ---------------------------------------------------------------------------


async def _search_team_knowledge(query: str) -> list[dict]:
    """Search team/org scope learnings using fast text search."""
    DATABASE_URL = (
        os.environ.get("CONTINUOUS_CLAUDE_DB_URL")
        or os.environ.get("DATABASE_URL")
        or os.environ.get("OPC_POSTGRES_URL")
    )

    if not DATABASE_URL:
        return []

    try:
        import asyncpg  # type: ignore
    except ImportError:
        return []

    try:
        conn = await asyncio.wait_for(
            asyncpg.connect(DATABASE_URL),
            timeout=2.0,
        )
    except Exception:
        return []

    try:
        # Text-based search (fast — no embedding generation needed)
        # Searches content using PostgreSQL full-text matching + simple LIKE fallback
        rows = await asyncio.wait_for(
            conn.fetch(
                """
                SELECT
                    id::text,
                    content,
                    metadata,
                    scope,
                    user_id,
                    -- Score: ts_rank on tsvector, fallback 0 if no match
                    COALESCE(
                        ts_rank(
                            to_tsvector('english', content),
                            plainto_tsquery('english', $1)
                        ),
                        0
                    ) AS score
                FROM archival_memory
                WHERE scope IN ('team', 'org')
                  AND (
                      to_tsvector('english', content) @@ plainto_tsquery('english', $1)
                      OR content ILIKE '%' || $2 || '%'
                  )
                ORDER BY score DESC, created_at DESC
                LIMIT $3
                """,
                query,
                query[:50],  # For LIKE fallback, use shorter query
                MAX_RESULTS * 3,  # Fetch extra, will filter by seen cache
            ),
            timeout=2.5,
        )
    except Exception:
        await conn.close()
        return []

    await conn.close()

    results = []
    for row in rows:
        metadata = row["metadata"] or {}
        if isinstance(metadata, str):
            try:
                metadata = json.loads(metadata)
            except Exception:
                metadata = {}
        results.append(
            {
                "id": row["id"],
                "content": row["content"] or "",
                "learning_type": metadata.get("learning_type", "LEARNING"),
                "tags": metadata.get("tags", []),
                "confidence": metadata.get("confidence", ""),
                "scope": row["scope"] or "team",
                "user_id": row["user_id"] or "team",
                "score": float(row["score"]),
            }
        )

    return results


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def _format_output(results: list[dict], query: str) -> str:
    """Format relay results for injection into Claude's context."""
    lines = [f"[Knowledge Relay] Relevant team knowledge for: {query[:60]}"]
    for i, r in enumerate(results, 1):
        ltype = r["learning_type"].replace("_", " ").title()
        scope_tag = f"[{r['scope']}]" if r["scope"] == "org" else ""
        content_preview = r["content"][:120].replace("\n", " ").strip()
        tags = ", ".join(r["tags"][:4]) if r["tags"] else ""
        line = f"  {i}. [{ltype}]{scope_tag} {content_preview}"
        if tags:
            line += f" ({tags})"
        lines.append(line)
    lines.append("  → Use /recall for full context on any of these.")
    return "\n".join(lines)


async def main() -> None:
    if DISABLED:
        return

    # Parse stdin (PostToolUse JSON payload)
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            return
        payload = json.loads(raw)
    except Exception:
        return

    tool_name = payload.get("tool_name", "")
    if tool_name not in ("Edit", "Write", "MultiEdit", "NotebookEdit"):
        return

    tool_input = payload.get("tool_input") or {}

    # Build search query from file context + changed content
    query = _extract_query(tool_name, tool_input)
    if not query:
        return

    # Load and prune cooldown cache
    seen_cache = _prune_seen_cache(_load_seen_cache())

    # Search team/org knowledge
    candidates = await _search_team_knowledge(query)

    # Filter by minimum score and cooldown
    fresh_results = []
    for r in candidates:
        if r["score"] < MIN_SCORE and r["score"] > 0:
            continue
        if r["id"] in seen_cache:
            continue
        fresh_results.append(r)
        if len(fresh_results) >= MAX_RESULTS:
            break

    if not fresh_results:
        return

    # Update seen cache with surfaced learnings
    now = time.time()
    for r in fresh_results:
        seen_cache[r["id"]] = now
    _save_seen_cache(seen_cache)

    # Output to stdout — Claude Code injects this as a system context block
    print(_format_output(fresh_results, query))


if __name__ == "__main__":
    asyncio.run(main())
