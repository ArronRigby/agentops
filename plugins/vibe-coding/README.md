# Vibe Coding Plugin

**Measure and improve AI-assisted development effectiveness.**

## Overview

The Vibe Coding plugin provides a complete framework for measuring, classifying, and improving AI-assisted development. It includes:

- **5 Core Metrics** - Quantify your vibe coding effectiveness
- **6 Vibe Levels** - Classify task difficulty (0-5)
- **12 Failure Patterns** - Identify and prevent common problems
- **6 Tracer Test Patterns** - Validate assumptions before coding

## Installation

```bash
# Install the npm tool
npm install -g @boshu2/vibe-check

# Or use directly
npx @boshu2/vibe-check
```

## Commands

| Command | Purpose |
|---------|---------|
| `/vibe-level` | Classify a task by difficulty (0-5) |
| `/vibe-check` | Run metrics analysis on repository |
| `/vibe-retro` | Run retrospective with failure pattern analysis |

## Skills

| Skill | Purpose |
|-------|---------|
| `vibe-check` | Run and interpret vibe-check results |
| `vibe-level` | Classify task difficulty |
| `tracer-test` | Create and run tracer tests |

## Agent

| Agent | Purpose |
|-------|---------|
| `vibe-assessor` | Comprehensive effectiveness assessment |

## The 5 Core Metrics

| Metric | Target | Elite | What It Measures |
|--------|--------|-------|------------------|
| **Iteration Velocity** | >3/hr | >5/hr | Commits per hour |
| **Flow Efficiency** | >75% | >90% | Time building vs debugging |
| **Debug Spiral Duration** | <30m | <15m | Avg time stuck in fix chains |
| **Rework Ratio** | <50% | <30% | Fix commits as % of total |
| **Trust Pass Rate** | >80% | >95% | AI code that ships without fix |

## The 6 Vibe Levels

| Level | Trust | Verify | Use For |
|-------|-------|--------|---------|
| 5 | 95% | Final only | Formatting, linting |
| 4 | 80% | Spot check | Boilerplate, CRUD |
| 3 | 60% | Key outputs | Features with known patterns |
| 2 | 40% | Every change | Integrations, auth |
| 1 | 20% | Every line | Architecture, infrastructure |
| 0 | 0% | N/A | Research, novel problems |

## The 6 Tracer Patterns

| Pattern | Risk Area | Tracer Test |
|---------|-----------|-------------|
| `API_MISMATCH` | K8s API versions | `oc api-resources`, dry-run CR |
| `SECRETS_AUTH` | Credentials, OAuth | Validate secret, test token |
| `SSL_TLS` | Certificates | Test SSL from cluster |
| `VOLUME_CONFIG` | PVC, mounts | Deploy minimal pod |
| `IMAGE_REGISTRY` | Image pull | Test pull before deploy |
| `GITOPS_DRIFT` | Operator changes | Deploy, wait, diff |

## Usage Example

```bash
# 1. Before starting work, classify the task
/vibe-level "implement OAuth integration"
# → Level 2: External dependency, auth is critical
# → Tracer tests REQUIRED

# 2. Run tracer tests for assumptions
# (use tracer-test skill)

# 3. Implement the feature

# 4. After work, check metrics
/vibe-check --since "today"

# 5. At end of week, run retrospective
/vibe-retro --since "1 week ago"
```

## Dependencies

- `core-workflow` plugin (required base)
- `@boshu2/vibe-check` npm package

## Links

- [npm: @boshu2/vibe-check](https://www.npmjs.com/package/@boshu2/vibe-check)
- [GitHub: boshu2/vibe-check](https://github.com/boshu2/vibe-check)
- [12-Factor AgentOps](https://github.com/boshu2/12-factor-agentops)
