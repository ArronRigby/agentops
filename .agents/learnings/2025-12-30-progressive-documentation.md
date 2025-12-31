---
date: 2025-12-30
type: Learning
topic: "Progressive Documentation for AI Tools"
source: "agentops-3eo"
tags: [learning, education, documentation, kelsey-hightower]
status: COMPLETE
---

# Learning: Progressive Documentation for AI Tools

## Context

Agentops had 28 commands averaging 400+ lines each, with 80% framework content (PDC, FAAFO, Three Loops) and 20% actionable procedure. New users faced a wall of concepts before they could run anything.

## What We Learned

### 1. Gateway Commands Must Be Tiny
**Type:** Pattern

Large command files overwhelm new users. The first command they encounter should be ~50 lines max.

**Evidence:** Original `commands/implement.md` was 516 lines. New `levels/L1-basics/implement.md` is 49 lines. Same functionality for beginners, just without the framework baggage.

**Application:** For any AI tool documentation:
- L1/beginner docs: 50 lines max
- Intermediate docs: 100 lines max
- Advanced docs: No limit, but users opt-in

---

### 2. One Concept Per Level
**Type:** Pattern

Kelsey Hightower's approach: each level adds exactly ONE new concept. Don't bundle.

**Evidence:** L1→L5 progression:
- L1: Commands exist (no persistence)
- L2: +persistence (.agents/)
- L3: +issue tracking (beads)
- L4: +parallelization (waves)
- L5: +automation (autopilot)

**Application:** When teaching complex systems:
1. Identify the 3-5 core concepts
2. Order them by dependency
3. Create one level per concept
4. Each level's docs assume previous levels mastered

---

### 3. Demo Transcripts Beat Descriptions
**Type:** Technical

Showing a real session transcript is more valuable than describing what happens. Users can pattern-match against real output.

**Evidence:** Each level has a `demo/` directory with session transcripts showing:
- What the user types
- What Claude outputs (including tool calls)
- What files are created/modified
- What the user learned

**Application:** For any AI tool:
- Record actual sessions (not synthetic)
- Show tool calls in brackets: `[Read] src/auth.ts`
- Include the "After" state (what changed)
- Add "What You Learned" section

---

### 4. Extract Frameworks to Reference
**Type:** Process

Framework content (PDC, FAAFO) is valuable but shouldn't block action. Extract to `/reference/`, link when needed.

**Evidence:** Created:
- `reference/pdc-framework.md` (195 lines)
- `reference/faafo-alignment.md` (181 lines)
- `reference/failure-patterns.md` (394 lines)

Commands now say "See reference/pdc-framework.md for details" instead of embedding 100 lines of framework explanation.

**Application:**
- Ask: "Does the user need this to run the command?"
- If no, extract to reference
- If yes, keep inline but minimal

---

### 5. Wave Execution Works for Docs Too
**Type:** Process

The same wave-based parallelization used for code implementation works for documentation writing.

**Evidence:** Wave 2 executed 4 issues in parallel (different directories):
- agentops-1ca: levels/ structure
- agentops-eaw: reference/pdc-framework.md
- agentops-bo0: reference/faafo-alignment.md
- agentops-j9e: reference/failure-patterns.md

All 4 sub-agents ran simultaneously, single commit captured results.

**Application:** When creating documentation:
1. Identify independent doc sections (different files)
2. Create beads issues with "Files affected" comments
3. Run `/implement-wave` to parallelize
4. Batch commit

---

### 6. Additive Over Destructive
**Type:** Gotcha

Don't delete existing documentation when restructuring. Keep `commands/` intact, add `levels/`.

**Evidence:** Original plan considered replacing `commands/`. Final approach was additive:
- `commands/` → Full reference versions (unchanged)
- `levels/` → Progressive learning versions (new)

This preserves existing users' bookmarks and mental models.

**Application:** When restructuring docs:
- Add new structure alongside old
- Deprecate old only after new is proven
- Redirect, don't delete

---

## Summary

Progressive documentation = minimal entry + layered depth. Kelsey Hightower's "Hard Way" approach works for AI tools too: show users what to type, what happens, then explain why.

## Related

- Plan: `.agents/plans/2025-12-30-kelsey-style-restructure.md`
- Research: `.agents/research/2025-12-30-kelsey-style-restructure.md`
- Retro: `.agents/retros/2025-12-30-kelsey-style-restructure.md`
