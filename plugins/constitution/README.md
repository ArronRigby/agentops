# Constitution Plugin

**The foundational rules that govern all agent operations.**

## The Four Pillars

AgentOps is built on four foundational pillars:

1. **DevOps + SRE** - Apply the same practices you use for containers to agents
2. **Learning Science** - Research→Plan→Implement based on cognitive science
3. **Context Engineering** - Stay under 40% token budget, JIT load context
4. **Knowledge OS** - Git as institutional memory, commits as knowledge writes

**Key insight:** Agents ARE microservices. Apply the SAME controls.

## Installation

```bash
/plugin marketplace add boshu2/agentops
/plugin install constitution@agentops
```

## Skills

| Skill | Purpose |
|-------|---------|
| `laws-of-an-agent` | The Six Laws every agent must follow |
| `context-engineering` | The 40% Rule and JIT loading |
| `git-discipline` | Semantic commits and Knowledge OS |

## Agent

| Agent | Purpose |
|-------|---------|
| `guardian` | Enforce constitutional rules |

---

## The Six Laws of an Agent

### Law 1: ALWAYS Extract Learnings

Document patterns discovered during work:
- Capture decision rationale (why, not just what)
- Analyze failures to prevent recurrence
- Share insights for future sessions

### Law 2: ALWAYS Improve Self or System

Identify at least 1 improvement opportunity:
- Specify impact (time saved, quality improved)
- Propose implementation (effort, priority)
- Don't just identify - suggest solutions

### Law 3: ALWAYS Document Context for Future

Every commit must include:
- **Context:** Why this work was needed
- **Solution:** What was done and how
- **Learning:** Reusable insights
- **Impact:** Quantified value

### Law 4: ALWAYS Prevent Hook Loops

After git push, check for hook-modified files:
- DO NOT commit files modified by hooks
- Session logs are auto-generated (normal)
- Only commit hook files if explicitly requested

### Law 5: ALWAYS Guide with Workflow Suggestions

After context loads, suggest relevant workflows:
- Let user pick, never prescribe
- Point to documentation
- Respect user autonomy

### Law 6: ALWAYS Check Knowledge Graph First

Before modifying Memory MCP:
- Search for existing entities
- Update existing (don't duplicate)
- Only create if genuinely new

---

## The 40% Rule

**Problem:** 200k token limit. Loading everything = context collapse.

**Solution:** Stay under 40% of token budget (80k of 200k).

```
Token Usage Zones:
🟢 <35% (70k)   - GREEN: Continue working
⚡ 35-40% (70-80k) - YELLOW: Prepare to bundle
⚠️ 40-60% (80-120k) - RED: Bundle NOW
🔴 >60% (120k+) - CRITICAL: Context degraded
```

**Pattern:** Gather → Glean → Summarize

---

## Git as Knowledge OS

### Commits = Memory Writes

Every commit captures:
- What changed (the diff)
- Why it changed (commit message)
- When it changed (timestamp)
- Who changed it (author)

### Branches = Process Isolation

Parallel work streams without interference.

### Hooks = Kernel Interrupts

Enforce rules automatically:
- Pre-commit: Validate changes
- Commit-msg: Ensure format
- Post-commit: Update state

### Logs = Audit Trail

Every change traceable:
- `git log` for history
- `git blame` for responsibility
- `git bisect` for debugging

---

## Semantic Commits

Format: `<type>(<scope>): <subject>`

### Types

| Type | Use For |
|------|---------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `refactor` | Code restructure |
| `test` | Add/update tests |
| `chore` | Maintenance |

### Example

```
feat(auth): add refresh token rotation

Context: Users were getting logged out every 24h due to JWT expiry.
Solution: Implemented refresh token rotation with Redis storage.
Learning: Redis TTL can handle token lifecycle automatically.
Impact: Users stay logged in indefinitely with secure rotation.

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

---

## Validation Gates

### Gate 1: Pre-Commit (Local)
- Syntax validation
- Linting
- Basic tests

### Gate 2: Human Review (Plan Stage)
- Review approach before execution
- Catch architectural mistakes early

### Gate 3: CI/CD (Automated)
- Full test suite
- Security scanning
- Build verification

### Gate 4: Deployment
- Progressive rollout
- Health checks
- Rollback capability

---

## Dependencies

None - this is the foundational plugin.

## Links

- [12-Factor AgentOps](https://github.com/boshu2/12-factor-agentops)
- [Laws of an Agent](https://github.com/boshu2/12-factor-agentops)
