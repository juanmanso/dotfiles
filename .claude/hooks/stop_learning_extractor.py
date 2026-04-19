#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Stop hook: Extract and store learnings from transcript.

Fire-and-forget design:
1. Parses transcript JSONL for completed todos, error-fix pairs, files modified
2. Outputs {"decision": "no_block"} immediately (never blocks session exit)
3. Spawns detached background processes to store each learning

Input (stdin): {session_id, transcript_path, stop_hook_active, ...}
Output: {"decision": "no_block"} or {} on skip/error
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class TodoItem:
    id: str
    content: str
    status: str


@dataclass
class ToolCall:
    name: str
    input: dict[str, Any] | None = None
    success: bool = True


@dataclass
class TranscriptSummary:
    completed_todos: list[TodoItem] = field(default_factory=list)
    error_fix_pairs: list[tuple[str, str]] = field(default_factory=list)
    files_modified: list[str] = field(default_factory=list)
    errors_encountered: list[str] = field(default_factory=list)


def parse_transcript(transcript_path: Path) -> TranscriptSummary:
    """Parse JSONL transcript and extract high-signal learning data."""
    summary = TranscriptSummary()

    if not transcript_path.exists():
        return summary

    try:
        content = transcript_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return summary

    all_tool_calls: list[ToolCall] = []
    modified_files: set[str] = set()
    errors: list[str] = []
    last_todo_state: list[TodoItem] = []

    for line in content.split('\n'):
        line = line.strip()
        if not line:
            continue

        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue

        # Extract tool calls (two common transcript formats)
        tool_name = entry.get("tool_name") or (
            entry.get("name") if entry.get("type") == "tool_use" else None
        )

        # Also check nested message content for assistant turns
        if not tool_name and entry.get("type") == "assistant":
            msg_content = entry.get("message", {}).get("content", [])
            if isinstance(msg_content, list):
                for block in msg_content:
                    if isinstance(block, dict) and block.get("type") == "tool_use":
                        inner_name = block.get("name", "")
                        inner_input = block.get("input", {})
                        tc = ToolCall(name=inner_name, input=inner_input, success=True)

                        if inner_name.lower() == "todowrite":
                            todos = inner_input.get("todos", [])
                            last_todo_state = [
                                TodoItem(
                                    id=t.get("id", f"todo-{i}"),
                                    content=t.get("content", ""),
                                    status=t.get("status", "pending")
                                )
                                for i, t in enumerate(todos)
                            ]

                        if inner_name.lower() in ("edit", "write"):
                            fp = inner_input.get("file_path") or inner_input.get("path")
                            if fp and isinstance(fp, str):
                                modified_files.add(fp)

                        all_tool_calls.append(tc)

        if tool_name:
            tool_call = ToolCall(name=tool_name, input=entry.get("tool_input"), success=True)

            if tool_name.lower() == "todowrite":
                tool_input = entry.get("tool_input", {})
                todos = tool_input.get("todos", [])
                last_todo_state = [
                    TodoItem(
                        id=t.get("id", f"todo-{i}"),
                        content=t.get("content", ""),
                        status=t.get("status", "pending")
                    )
                    for i, t in enumerate(todos)
                ]

            if tool_name.lower() in ("edit", "write"):
                tool_input = entry.get("tool_input", {})
                fp = tool_input.get("file_path") or tool_input.get("path")
                if fp and isinstance(fp, str):
                    modified_files.add(fp)

            all_tool_calls.append(tool_call)

        # Extract tool failures from tool_result entries
        if entry.get("type") == "tool_result" or entry.get("tool_result") is not None:
            result = entry.get("tool_result", {})
            if isinstance(result, dict):
                exit_code = result.get("exit_code") or result.get("exitCode")
                if exit_code is not None and exit_code != 0:
                    if all_tool_calls:
                        all_tool_calls[-1].success = False
                    error_msg = result.get("stderr") or result.get("error") or "Command failed"
                    last_tool = all_tool_calls[-1] if all_tool_calls else None
                    command = (last_tool.input or {}).get("command", "unknown") if last_tool else "unknown"
                    errors.append(f"{str(command)[:80]}: {str(error_msg)[:150]}")

            if entry.get("error"):
                errors.append(str(entry["error"])[:200])
                if all_tool_calls:
                    all_tool_calls[-1].success = False

        # Also check user messages for tool_result blocks
        if entry.get("type") == "user":
            msg_content = entry.get("message", {}).get("content", [])
            if isinstance(msg_content, list):
                for block in msg_content:
                    if isinstance(block, dict) and block.get("type") == "tool_result":
                        inner_content = block.get("content", "")
                        if isinstance(inner_content, str) and "error" in inner_content.lower():
                            errors.append(inner_content[:200])

    # Build error-fix pairs: failed tool followed by successful Bash/Edit/Write
    error_fix_pairs: list[tuple[str, str]] = []
    for i, tc in enumerate(all_tool_calls):
        if not tc.success and i + 1 < len(all_tool_calls):
            next_tc = all_tool_calls[i + 1]
            if next_tc.success and next_tc.name.lower() in ("bash", "edit", "write"):
                fix_desc = ""
                if next_tc.input:
                    fix_desc = (
                        next_tc.input.get("command")
                        or next_tc.input.get("file_path")
                        or ""
                    )
                    fix_desc = str(fix_desc)[:100]
                if errors:
                    err = errors[-1][:150]
                    error_fix_pairs.append((err, f"Fixed via {next_tc.name}: {fix_desc}"))

    summary.completed_todos = [t for t in last_todo_state if t.status == "completed"]
    summary.files_modified = list(modified_files)
    summary.errors_encountered = errors[-5:]
    summary.error_fix_pairs = error_fix_pairs[:3]

    return summary


def meets_threshold(summary: TranscriptSummary) -> bool:
    """Return True if there's enough signal worth storing as learnings."""
    return (
        len(summary.completed_todos) > 0
        or len(summary.files_modified) >= 3
        or len(summary.error_fix_pairs) > 0
    )


def spawn_store(
    opc_dir: Path,
    session_id: str,
    learning_type: str,
    content: str,
    context: str,
    tags: str,
) -> None:
    """Spawn a detached store_learning.py subprocess (fire-and-forget)."""
    store_script = opc_dir / "scripts" / "core" / "store_learning.py"
    if not store_script.exists():
        return

    env = {**os.environ, "PYTHONPATH": str(opc_dir)}
    cmd = [
        "uv", "run", "python", str(store_script),
        "--session-id", session_id,
        "--type", learning_type,
        "--content", content[:500],
        "--context", context[:200],
        "--tags", tags,
        "--confidence", "medium",
    ]

    try:
        subprocess.Popen(
            cmd,
            cwd=str(opc_dir),
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
    except Exception:
        pass  # Fire and forget - never block on subprocess failures


def main() -> None:
    # Read stdin
    try:
        data = json.load(sys.stdin)
    except Exception:
        print("{}")
        return

    # Avoid recursion if stop hook triggers itself
    if data.get("stop_hook_active"):
        print("{}")
        return

    session_id = data.get("session_id", "auto-stop")
    transcript_path_str = data.get("transcript_path", "")

    # Resolve OPC directory
    opc_dir = Path(
        os.environ.get("CLAUDE_OPC_DIR")
        or os.path.join(
            os.environ.get("USERPROFILE", os.path.expanduser("~")),
            "Desktop", "Continuous-Claude-v3", "opc"
        )
    )

    # Output no_block IMMEDIATELY before any work (never stall session exit)
    print(json.dumps({"decision": "no_block"}))
    sys.stdout.flush()

    # No transcript path → nothing to extract
    if not transcript_path_str:
        return

    transcript_path = Path(transcript_path_str)
    summary = parse_transcript(transcript_path)

    # Check threshold before spawning anything
    if not meets_threshold(summary):
        return

    # Short session label for store_learning tagging
    session_label = session_id[:16] if session_id else "auto-stop"

    # Store completed todos as WORKING_SOLUTION
    file_context = ", ".join(summary.files_modified[:3]) if summary.files_modified else "session"
    for todo in summary.completed_todos[:5]:
        spawn_store(
            opc_dir=opc_dir,
            session_id=session_label,
            learning_type="WORKING_SOLUTION",
            content=f"Completed task: {todo.content}",
            context=f"Files involved: {file_context}",
            tags="auto_extracted,session_stop,todo_completed",
        )

    # Store error-fix pairs as ERROR_FIX
    for err, fix in summary.error_fix_pairs[:3]:
        spawn_store(
            opc_dir=opc_dir,
            session_id=session_label,
            learning_type="ERROR_FIX",
            content=f"Error: {err} | Fix: {fix}",
            context="Error resolved during session",
            tags="auto_extracted,session_stop,error_fix",
        )

    # Store multi-file change summary as CODEBASE_PATTERN (3+ files)
    if len(summary.files_modified) >= 3:
        file_list = ", ".join(summary.files_modified[:10])
        if len(summary.files_modified) > 10:
            file_list += f" (+{len(summary.files_modified) - 10} more)"
        spawn_store(
            opc_dir=opc_dir,
            session_id=session_label,
            learning_type="CODEBASE_PATTERN",
            content=f"Modified {len(summary.files_modified)} files: {file_list}",
            context="Multi-file session change",
            tags="auto_extracted,session_stop,files_modified",
        )


if __name__ == "__main__":
    main()
