---
name: vibe-check
description: Run vibe-check analysis to measure AI-assisted coding effectiveness. Use after implementation, during retrospectives, or before planning. Triggers on mentions of metrics, retrospective, effectiveness, or development quality.
---

# vibe-check Skill

**Purpose:** Run vibe-check analysis and interpret results

**Tool:** `npx @boshu2/vibe-check`
- GitHub: [github.com/boshu2/vibe-check](https://github.com/boshu2/vibe-check)
- npm: [@boshu2/vibe-check](https://www.npmjs.com/package/@boshu2/vibe-check)

---

## When to Use

- After completing implementation work
- During retrospectives
- Before planning new work (baseline)
- When user asks about development effectiveness
- When debug spirals detected (3+ fix commits in a row)

---

## Quick Commands

```bash
# Basic analysis
npx @boshu2/vibe-check

# Last week
npx @boshu2/vibe-check --since "1 week ago"

# Session-specific
npx @boshu2/vibe-check --since "<session-start-time>"

# JSON for analysis
npx @boshu2/vibe-check --format json

# Markdown report
npx @boshu2/vibe-check --format markdown
```

---

## The 5 Core Metrics

| Metric | What It Measures | Target | Elite |
|--------|------------------|--------|-------|
| **Iteration Velocity** | Commits per hour | >3/hr | >5/hr |
| **Flow Efficiency** | % time building vs debugging | >75% | >90% |
| **Debug Spiral Duration** | Avg time stuck in fix chains | <30m | <15m |
| **Rework Ratio** | Fix commits as % of total | <50% | <30% |
| **Trust Pass Rate** | AI code that ships without fix | >80% | >95% |

---

## Overall Rating

| Rating | Meaning | Action |
|--------|---------|--------|
| ELITE | Vibe coding working excellently | Maintain practices |
| HIGH | Good effectiveness | Minor improvements |
| MEDIUM | Room for improvement | Focus on weak metrics |
| LOW | Process issues | Stop and reassess |

---

## Debug Spiral Patterns

When vibe-check detects spirals, identify the pattern:

| Pattern | Tracer Test |
|---------|-------------|
| `VOLUME_CONFIG` | Deploy minimal pod with volume mount |
| `SECRETS_AUTH` | Validate secret structure, test OAuth flow |
| `API_MISMATCH` | `oc api-resources`, dry-run minimal CR |
| `SSL_TLS` | Test SSL in container on target cluster |
| `IMAGE_REGISTRY` | Test image pull before deployment |
| `GITOPS_DRIFT` | Deploy, wait, diff for operator changes |

---

## Workflow Integration

### Before Implementation (Baseline)
```bash
npx @boshu2/vibe-check --since "1 month ago"
# Note trust pass rate - if <80%, plan tracer tests
```

### After Implementation
```bash
npx @boshu2/vibe-check --since "<session-start>"
# Check for new patterns, update pattern library
```

### Weekly Review
```bash
npx @boshu2/vibe-check --since "1 week ago" --format markdown
# Share with team, identify trends
```

---

## Related Skills

- `vibe-level` - Classify task difficulty (0-5)
- `tracer-test` - Validate assumptions before implementation
