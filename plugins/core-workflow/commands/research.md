# /research - Research Phase (Outer Loop)

**Purpose:** Explore problem space before committing to a solution.

**Why this matters:** Research prevents wasted effort. Without understanding context, agents build wrong solutions, miss existing patterns, or duplicate work. Research bundles preserve discoveries for future sessions.

---

## Opus 4.5 Behavioral Standards

<investigate_before_planning>
Before designing solutions, thoroughly explore the codebase and problem space. Read relevant files, understand existing patterns, and identify constraints. Do not speculate about code you have not opened.
</investigate_before_planning>

<use_parallel_tool_calls>
When gathering context, read multiple related files in parallel. If exploring authentication, read auth middleware, user model, and routes simultaneously rather than sequentially.
</use_parallel_tool_calls>

---

## Usage

```bash
/research
```

**Agent will:**
1. Clarify research question with you
2. Choose appropriate approach (codebase exploration, API analysis, requirements gathering, problem decomposition)
3. Gather context using JIT loading (stay under 40%)
4. Document findings with specific file references
5. Create research bundle for plan phase

**Output:** Research document + bundle ready for `/plan`

---

## Research Approaches

| Approach | When to Use | Key Activities |
|----------|-------------|----------------|
| Codebase Exploration | Understanding existing code | Glob for patterns, Grep for usage, Read key files |
| API Analysis | External integrations | WebFetch docs, analyze contracts, map dependencies |
| Requirements Gathering | Unclear scope | Questions to stakeholder, acceptance criteria |
| Problem Decomposition | Complex problems | Break into subproblems, identify option space |

---

## Example

```
You: /research

Agent: What topic should I explore?

You: How does user authentication work in this API?

Agent: I'll explore the codebase to understand the authentication system.
[Reads auth files, middleware, routes in parallel]
[Documents JWT flow, Redis blacklist, token lifecycle]

Research complete. Key findings:
- JWT-based authentication in src/middleware/auth.ts:45
- Redis blacklist for logout in src/services/session.ts:112
- No refresh tokens currently implemented
- Rate limiting on auth endpoints via express-rate-limit

Create bundle? (yes/no)

You: yes

Bundle saved: user-auth-research-2025-11-30.md
Ready for: /plan user-auth-research-2025-11-30
```

---

## Research Bundle Format

```markdown
# [Topic] Research

**Type:** Research
**Created:** YYYY-MM-DD
**Loop:** Outer
**Tags:** [relevant tags]

## Executive Summary
[2-3 sentences on what was discovered]

## Key Findings
[Specific discoveries with file:line references]

## Option Space
[If applicable, different approaches identified]

## Constraints Discovered
[Limitations, dependencies, risks]

## Next Steps
[Ready for /plan with specific recommendations]
```

---

## Completion Criteria

Research is complete when you can answer:
- What problem are we solving?
- What already exists that we can build on?
- What constraints limit our options?
- What approach should the plan phase evaluate?

---

**Demonstrates:** Factor II (JIT Context), Factor VI (Session Continuity), Factor VII (Intelligent Routing)
