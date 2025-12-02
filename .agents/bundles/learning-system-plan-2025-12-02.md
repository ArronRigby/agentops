# Learning Extraction System Plan

**Created:** 2025-12-02
**Type:** Plan
**Status:** Ready for implementation
**Repo:** agentops
**Parent Plan:** workflow-improvements-plan-2025-12-02.md

---

## Goal

Create the `.agents/learnings/` infrastructure that enables patterns to compound across sessions. Every significant piece of work should produce:
- A retrospective (what happened, what worked, what didn't)
- Extracted patterns (reusable solutions)
- Evidence (metrics, session IDs, trust pass rates)

---

## Current State

agentops has:
- ✅ CLAUDE.md with methodology documentation
- ✅ Plugin architecture for workflows
- ✅ Command definitions

Missing:
- ❌ `.agents/learnings/` directory
- ❌ Pattern registry
- ❌ Retro storage
- ❌ Evidence tracking
- ❌ Pattern search/discovery

---

## Implementation

### Task 1: Create Directory Structure (15 min)

```
.agents/
├── bundles/                    # Already created
│   └── learning-system-plan-2025-12-02.md
└── learnings/
    ├── INDEX.md               # Pattern discovery index
    ├── patterns/
    │   ├── implementation/    # How to build things
    │   ├── debugging/         # How to fix things
    │   └── architecture/      # How to design things
    └── retros/
        └── YYYY-MM-DD-name.md # Session retrospectives
```

### Task 2: Create INDEX.md Template (30 min)

```markdown
# Learning Index

## Patterns by Category

### Implementation
- [Pattern Name](patterns/implementation/pattern-name.md) - Brief description

### Debugging
- [Pattern Name](patterns/debugging/pattern-name.md) - Brief description

### Architecture
- [Pattern Name](patterns/architecture/pattern-name.md) - Brief description

## Recent Retros
- [2025-12-02 Session Name](retros/2025-12-02-session-name.md)

## Pattern Statistics
- Total patterns: X
- Most used: [pattern-name] (N times)
- Highest trust: [pattern-name] (95%)
```

### Task 3: Create Pattern Schema (30 min)

Each pattern file follows this schema:

```markdown
# Pattern: [Name]

**Category:** implementation | debugging | architecture
**Created:** YYYY-MM-DD
**Last Validated:** YYYY-MM-DD
**Trust Level:** X% (based on evidence)

## Problem
What problem does this pattern solve?

## Solution
Step-by-step implementation.

## When to Use
- Scenario 1
- Scenario 2

## When NOT to Use
- Anti-pattern 1

## Evidence
| Session | Date | Trust Pass Rate | Outcome |
|---------|------|-----------------|---------|
| session-id | 2025-12-02 | 92% | Success |

## Related Patterns
- [Other Pattern](../category/other-pattern.md)
```

### Task 4: Create Retro Schema (30 min)

Each retro file follows this schema:

```markdown
# Retrospective: [Session Name]

**Date:** YYYY-MM-DD
**Session ID:** from claude-progress.json
**Vibe Level:** X
**Duration:** Xh Xm

## Summary
One paragraph of what was accomplished.

## Metrics
- Trust Pass Rate: X%
- Rework Ratio: X%
- Spirals: X

## What Worked
1. Thing that worked
2. Another thing

## What Didn't Work
1. Thing that failed
2. Another failure

## Failure Patterns Hit
- [Pattern Name] - How it manifested

## Failure Patterns Avoided
- [Pattern Name] - How we avoided it

## Learnings
1. Specific, actionable learning
2. Another learning

## Patterns Extracted
- [New Pattern](../patterns/category/new-pattern.md) - Created from this session
```

### Task 5: Create First Pattern (1 hour)

Extract a pattern from recent agentops work:

**Candidate: "Plugin Architecture Pattern"**
- How agentops plugins are structured
- Registration mechanism
- Command inheritance
- Evidence from actual usage

### Task 6: Integrate with /learn Command (1 hour)

Enhance workspace `/learn` command to:
1. Prompt for pattern details
2. Create pattern file from template
3. Update INDEX.md
4. Link to session retro

---

## Files to Create

| File | Purpose |
|------|---------|
| .agents/learnings/INDEX.md | Pattern discovery |
| .agents/learnings/patterns/implementation/.gitkeep | Category placeholder |
| .agents/learnings/patterns/debugging/.gitkeep | Category placeholder |
| .agents/learnings/patterns/architecture/.gitkeep | Category placeholder |
| .agents/learnings/retros/.gitkeep | Retro storage |

---

## Validation

- [ ] Directory structure created
- [ ] INDEX.md exists with template
- [ ] At least one pattern documented
- [ ] At least one retro documented
- [ ] /learn command updated to use new structure

---

## Success Metrics

After implementation:
- Patterns are discoverable via INDEX.md
- Each pattern has evidence (session, metrics)
- Retros link to extracted patterns
- Trust levels calculated from evidence
- /learn command creates properly formatted patterns

---

## Resume Command

```bash
/session-resume "learning system"
```
