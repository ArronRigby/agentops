---
name: laws-of-an-agent
description: The Six Laws that govern all agent operations. These are mandatory rules that must be followed in every session. Use this skill to understand and apply constitutional requirements.
---

# laws-of-an-agent Skill

**Purpose:** Define and enforce the mandatory rules for all agent operations.

---

## The Six Laws

These laws are **MANDATORY**. They are not optional guidelines - they are constitutional requirements enforced through automation.

---

### Law 1: ALWAYS Extract Learnings

**Requirement:** Document patterns and insights from every work session.

**Implementation:**
```markdown
## Learning
- [Pattern discovered]
- [Insight gained]
- [Failure analyzed]
```

**Include in:**
- Commit messages
- Session end summaries
- Bundle documents

**Why:** Institutional memory compounds. Today's learning is tomorrow's efficiency.

**Enforcement:** Pre-commit hooks check for Learning section.

---

### Law 2: ALWAYS Improve Self or System

**Requirement:** Identify at least 1 improvement opportunity per session.

**Implementation:**
```markdown
## Improvement Identified
- **What:** [description]
- **Impact:** [time saved / quality improved]
- **Effort:** [low/medium/high]
- **Priority:** [low/medium/high]
```

**Categories:**
- Process improvement (how we work)
- Tooling improvement (what we use)
- Documentation improvement (what we know)
- Code improvement (what we build)

**Why:** Continuous improvement is the difference between stagnation and excellence.

**Enforcement:** Session end checks for improvement identification.

---

### Law 3: ALWAYS Document Context for Future

**Requirement:** Every commit must include context for future agents.

**Commit Format:**
```
<type>(<scope>): <subject>

Context: [Why was this needed? What problem does it solve?]
Solution: [What was created/changed? How does it work?]
Learning: [What pattern was applied? What was discovered?]
Impact: [What value is delivered? Who benefits?]

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

**Why:** Future agents (including future you) need to understand why, not just what.

**Enforcement:** commit-msg hook validates format.

---

### Law 4: ALWAYS Prevent Hook Loops

**Requirement:** Never commit files modified by git hooks.

**Protocol:**
```bash
# After push, check for hook modifications
git status

# If hook-modified files exist:
# ❌ DO NOT commit them
# ✅ Report: "Post-commit hook created session log (normal)"
# ✅ STOP execution
```

**Common Hook Files:**
- Session logs
- Auto-generated timestamps
- Metrics files

**Exception:** Only commit if user explicitly says "commit the session log"

**Why:** Committing hook files creates infinite loops.

**Enforcement:** Post-push script checks and warns.

---

### Law 5: ALWAYS Guide with Workflow Suggestions

**Requirement:** After context loads, suggest relevant workflows.

**Protocol:**
1. Context loads (primer finishes)
2. Analyze what user is trying to do
3. Suggest 5-6 relevant workflows
4. User picks (or asks to see all)
5. Point to documentation

**Important:** Let user pick, NEVER prescribe.

**Example:**
```
Based on your task, you might want:
1. /research - Explore problem space first
2. /plan - Design solution if research done
3. /implement - Execute if plan approved

Which approach? (or ask for more options)
```

**Why:** Workflows ensure quality. Forcing them creates friction.

**Enforcement:** prepare-commit-msg hook adds workflow declaration.

---

### Law 6: ALWAYS Check Knowledge Graph First

**Requirement:** Search Memory MCP before creating new entities.

**Protocol:**
```typescript
// MANDATORY: Search first
mcp__memory__search_nodes({ query: "relevant topic" })

// Review existing entities

// THEN decide:
// - Update existing (add_observations) - PREFERRED
// - Create new (create_entities) - only if genuinely new
```

**Why:** Knowledge graph is shared institutional memory. Duplicates pollute data.

**Pattern:**
1. Search before creating
2. Update existing (don't duplicate)
3. Only create if truly new
4. Enrich, don't fragment

**Enforcement:** Agent framework validates search before create.

---

## Law Violations

### Detecting Violations

| Law | Violation Signal |
|-----|------------------|
| Law 1 | Commit without Learning section |
| Law 2 | Session end without improvement |
| Law 3 | Commit without context fields |
| Law 4 | Committing hook-modified files |
| Law 5 | Prescribing instead of suggesting |
| Law 6 | Creating duplicate entities |

### Remediation

| Violation | Fix |
|-----------|-----|
| Missing learning | Add to commit message before push |
| No improvement | Identify before session end |
| Missing context | Amend commit with full message |
| Hook file commit | Reset, don't commit hook files |
| Prescribing workflow | Rephrase as suggestion |
| Duplicate entity | Merge into existing, delete duplicate |

---

## Quick Reference

| Law | One-Line Summary |
|-----|------------------|
| 1 | Document what you learned |
| 2 | Suggest one improvement |
| 3 | Explain why, not just what |
| 4 | Don't commit hook files |
| 5 | Suggest, don't prescribe |
| 6 | Search before create |
