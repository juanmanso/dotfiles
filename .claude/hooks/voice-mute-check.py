#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""PreToolUse hook: blocks mcp__voice__speak when macOS audio is muted or volume is 0."""

import json
import subprocess
import sys


def check_audio_state() -> str | None:
    """Check macOS system audio state.

    Returns a reason string if audio should be blocked, or None if audio is fine.
    """
    try:
        result = subprocess.run(
            ["osascript", "-e", "get volume settings"],
            capture_output=True, text=True, timeout=5,
        )
        # Output: "output volume:50, input volume:75, alert volume:100, output muted:false"
        settings = result.stdout.strip()
        muted = "output muted:true" in settings
        volume = None
        for part in settings.split(","):
            if "output volume" in part:
                volume = int(part.split(":")[1].strip())
                break

        if volume is not None and volume == 0:
            return "System volume is at 0 — skipping speak."
        if muted:
            return "System audio is muted — skipping speak."
    except Exception:
        pass  # If we can't check, allow speech
    return None


def main() -> None:
    # Read hook input from stdin
    try:
        data = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, EOFError):
        data = {}

    tool_name = data.get("tool_name", "")

    # Only intercept voice speak calls
    if "speak" not in tool_name:
        sys.exit(0)

    reason = check_audio_state()
    if reason:
        # Exit code 2 = block the tool call
        print(reason, file=sys.stderr)
        sys.exit(2)

    # Allow the call
    sys.exit(0)


if __name__ == "__main__":
    main()
