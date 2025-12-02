# /plan - Planning Phase (Middle Loop)

**Purpose:** Design solution and create implementation specification from research findings.

**Why this matters:** Plans prevent scope creep and enable review before execution. A well-structured plan catches architectural mistakes early when they're cheap to fix. Plans also create accountability - they're the contract between agent and human.

---

## Opus 4.5 Behavioral Standards

<avoid_overengineering>
Design the simplest solution that meets requirements. Do not add features, abstractions, or "improvements" beyond what was researched. The right complexity is the minimum needed for the current task.
</avoid_overengineering>

<explicit_decisions>
Document each architectural decision with rationale. Future sessions need to understand why choices were made, not just what was chosen.
</explicit_decisions>

<quantified_scope>
Express work in concrete terms: number of files, specific functions, estimated lines changed. Vague plans lead to vague implementations.
</quantified_scope>

---

## Usage

```bash
# Load research bundle and plan
/plan [research-bundle-name]

# Or plan from scratch (if research already known)
/plan
```

**Agent will:**
1. Load research findings
2. Evaluate option space from research
3. Design solution architecture
4. Break down into specific tasks with file:line targets
5. Specify acceptance criteria per task
6. Document decisions and risks
7. Create implementation specification

**Output:** Implementation plan ready for `/implement`

---

## Plan Structure

```markdown
# [Feature] Implementation Plan

**Type:** Plan
**Created:** YYYY-MM-DD
**Research:** [link to research bundle]
**Scope:** [Small/Medium/Large]

## Problem Statement
[What we're solving, from research]

## Recommended Approach
[Chosen option with rationale]

### Why Not [Alternative]?
[Brief rationale for rejected options]

## Tasks

### Task 1: [Name]
- **File:** src/path/file.ts:45-67
- **Change:** [Specific modification]
- **Acceptance:** [How to verify]

### Task 2: [Name]
...

## Risks
- [Risk]: [Mitigation]

## Out of Scope
[What we're explicitly not doing]
```

---

## Example

```
You: /plan user-auth-research-2025-11-30

Agent: Loading research bundle...

Based on research, I recommend:

**Approach:** Add refresh token rotation with Redis storage

**Why this approach:**
- Builds on existing Redis session infrastructure (src/services/session.ts)
- JWT library already supports refresh tokens
- Minimal changes to existing auth middleware

**Why not separate token service?**
- Over-engineers for current scale
- Adds deployment complexity
- No clear benefit until >10k users

**Tasks:**
1. Add refresh token model (src/models/token.ts) - new file ~50 lines
2. Update auth middleware (src/middleware/auth.ts:45-89) - add rotation logic
3. Add refresh endpoint (src/routes/auth.ts:23) - new route
4. Update Redis schema (src/services/session.ts:112-145) - add token fields
5. Add tests (tests/auth.test.ts) - 5-7 new tests

**Acceptance criteria:**
- Refresh tokens rotate on each use
- Old tokens invalidate immediately
- Tests cover rotation, expiry, and blacklist scenarios

Approve plan? (yes/no/modify)
```

---

## Vibe Level Guidance

| Vibe Level | Planning Depth | Verification |
|------------|----------------|--------------|
| 5 (Formatting) | Skip planning | N/A |
| 4 (Boilerplate) | Minimal outline | Spot check |
| 3 (CRUD) | Task list | Key outputs |
| 2 (Features) | Full spec | Every change |
| 1 (Architecture) | Detailed with ADRs | Every line |
| 0 (Research) | Return to /research | N/A |

---

## Completion Criteria

Plan is complete when you can answer:
- What specific files and lines change?
- How will each task be verified?
- What are we explicitly not doing?
- Why this approach over alternatives?

---

**Demonstrates:** Factor III (Single-Responsibility), Factor IX (Pattern Extraction), Factor XII (Domain Portability)
