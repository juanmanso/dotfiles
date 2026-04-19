---
name: claude-changelog
description: Fetch and display Claude Code changelog between versions. Stores the latest consulted version for future reference.
argument-hint: [from-version] [to-version] (e.g. "0.78 0.81", or blank for "since last checked")
---

# Claude Code Changelog

You are a research assistant that fetches Claude Code release notes and presents them clearly.

## Input

The user invoked `/claude-changelog $ARGUMENTS`.

**Arguments parsing:**
- Two versions given (e.g. `0.78 0.81`) — show changes between those versions (inclusive)
- One version given (e.g. `0.82`) — show changes from the last consulted version up to that version
- No arguments — check the tracker file for the last consulted version, then show everything from that version to the latest available

## Step 1: Check Last Consulted Version

Read the tracker file at `~/.claude/changelog-tracker.json`. It stores:
```json
{
  "last_consulted_version": "2.1.81",
  "last_consulted_at": "2026-03-23"
}
```

If the file doesn't exist, that's fine — the user hasn't used this skill before.

Use the tracker to fill in missing version bounds when the user provides fewer than two arguments.

## Step 2: Research Changelog

Use the `claude-code-guide` agent (or `WebSearch`/`WebFetch`) to find the Claude Code changelog entries for the requested version range. Search for:
- Claude Code official changelog
- Release notes on GitHub (anthropics/claude-code)
- Blog posts or announcements

For each version in the range, gather:
- Version number and release date
- New features
- Improvements
- Bug fixes (highlight critical ones)

## Step 3: Present Results

Format the output as:

```
## Claude Code Changelog: v{from} → v{to}

### v{X.Y.Z} (date)
**New Features:**
- Feature 1 — description
- Feature 2 — description

**Improvements:**
- Improvement 1

**Fixes:**
- Critical: fix description
- Fix description

---
(repeat per version)
```

Keep descriptions concise (one line each). Group by version, ordered chronologically.

## Step 4: Update Tracker

After displaying the changelog, update `~/.claude/changelog-tracker.json` with:
- `last_consulted_version`: the highest version number shown
- `last_consulted_at`: today's date

Write the file using the Write tool.

## Step 5: Summary

End with a brief one-line summary like:
> Tracked up to v2.1.83. Next time you run `/claude-changelog`, I'll show what's new since then.

## Rules

- Always present versions in chronological order
- If no new versions are found beyond the last consulted, say so clearly
- If the tracker file is missing, create it after the first run
- Don't include every minor fix — focus on features, notable improvements, and critical fixes
- When versions are ambiguous (e.g. user says "0.81"), interpret as "2.1.81"
