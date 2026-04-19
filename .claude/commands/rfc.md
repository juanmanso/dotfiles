# RFC: Research, Design & Architecture

You are acting as a software architect. The user wants to design a solution for:

**$ARGUMENTS**

Follow this workflow strictly. Do not skip phases.

---

## Phase 1: Clarify

Before doing any work, ensure you understand the problem:

1. Restate the problem in your own words (1-2 sentences)
2. List **assumptions** you're making
3. Ask up to 3 clarifying questions if anything is ambiguous — then STOP and wait for answers

If the problem statement is clear enough, state your assumptions and proceed.

---

## Phase 2: Research

Gather context before proposing anything:

1. **Codebase** — Explore the current project structure, existing patterns, and relevant code using agents or tools
2. **Memory** — Check for prior learnings on this topic:
   ```bash
   cd $CLAUDE_OPC_DIR && PYTHONPATH=. uv run python scripts/core/recall_learnings.py --query "<topic keywords>" --k 5 --text-only
   ```
3. **External** (if needed) — Search the web for established patterns, libraries, or prior art relevant to the problem
4. **Constraints** — Identify technical constraints (existing stack, infrastructure, team size, timeline)

Present a **Research Summary** with key findings before moving on.

---

## Phase 3: Design

Propose 2-3 solution options. For each option:

### Option N: [Name]

- **Approach:** How it works (2-4 sentences)
- **Architecture:** Key components and how they interact
- **Pros:** What's good about this approach
- **Cons:** What's risky or costly
- **Effort:** Relative effort (low / medium / high)
- **Dependencies:** What this requires (libraries, infra, migrations)

Then provide a **Recommendation** with clear rationale for which option to pursue.

---

## Phase 4: Specification

Once the user approves a direction, produce the RFC document:

### RFC: [Title]

**Status:** Draft
**Author:** [User] + Claude
**Date:** [Today's date]

#### Problem Statement
What problem are we solving and why now?

#### Goals & Non-Goals
| Goals | Non-Goals |
|-------|-----------|
| ... | ... |

#### Proposed Solution
Detailed description of the chosen approach including:
- System architecture (describe components and data flow)
- Key interfaces / API contracts
- Data model changes (if any)
- Error handling strategy

#### Alternatives Considered
Brief summary of rejected options and why.

#### Trade-offs & Risks
| Trade-off / Risk | Mitigation |
|-------------------|------------|
| ... | ... |

#### Migration / Rollout Plan
How do we get from current state to the new design? Include:
- Breaking changes
- Migration steps
- Feature flags / rollback strategy

#### Open Questions
Anything unresolved that needs further discussion.

---

## Phase 5: Implementation Plan

Break the approved design into concrete tasks:

- [ ] Task 1: Description (estimated scope: S/M/L)
- [ ] Task 2: Description (estimated scope: S/M/L)
- ...

Order tasks by dependency. Flag which can be parallelized.

---

## Rules

- Do NOT jump to solutions. Research first.
- Present options before committing to one.
- Keep the RFC concise — prefer clarity over completeness.
- If the project uses React Native, consider mobile-specific constraints (navigation, native modules, platform differences) in your design.
- Store the final RFC as a markdown file in the project if the user approves.
