---
description: Run vibe-check analysis and display results
allowed-tools: Bash(npx*), Read
argument-hint: "[--since 'time'] [--format json|markdown]"
---

# /vibe-check - Measure Vibe Coding Effectiveness

Run vibe-check analysis on current repository using the published npm tool.

## Installation

```bash
npm install -g @boshu2/vibe-check
# or run directly
npx @boshu2/vibe-check
```

## Usage

```bash
/vibe-check                      # Basic analysis
/vibe-check --since "1 week ago" # Last week
/vibe-check --since "today"      # Today only
/vibe-check --format markdown    # Markdown output
/vibe-check --format json        # JSON for processing
```

## Execution

```bash
npx @boshu2/vibe-check $ARGUMENTS
```

## The 5 Core Metrics

| Metric | Target | Elite | Action if Below |
|--------|--------|-------|-----------------|
| **Iteration Velocity** | >3/hour | >5/hour | Smaller commits |
| **Rework Ratio** | <50% | <30% | Validate assumptions first |
| **Trust Pass Rate** | >80% | >95% | Use tracer tests |
| **Debug Spiral Duration** | <30m | <15m | Break into steps |
| **Flow Efficiency** | >75% | >90% | Reduce context switching |

## Interpretation

### Overall Rating

| Rating | Meaning | Action |
|--------|---------|--------|
| ELITE | Vibe coding working excellently | Maintain practices |
| HIGH | Good effectiveness | Minor improvements |
| MEDIUM | Room for improvement | Focus on weak metrics |
| LOW | Process issues | Stop and reassess approach |

### Debug Spiral Patterns

When spirals detected, check which pattern:

| Pattern | Tracer Test to Add |
|---------|-------------------|
| `VOLUME_CONFIG` | Deploy minimal pod with volume mount |
| `SECRETS_AUTH` | Validate secret structure, test OAuth |
| `API_MISMATCH` | `oc api-resources`, dry-run minimal CR |
| `SSL_TLS` | Test SSL in container on target cluster |
| `IMAGE_REGISTRY` | Test image pull before deployment |
| `GITOPS_DRIFT` | Deploy, wait, diff for operator changes |

## Next Steps

Based on results:
- **Trust Pass Rate <80%**: Add tracer tests before next implementation
- **Debug spirals detected**: Document patterns, create prevention tracers
- **Rework Ratio >50%**: Spend more time in research/plan phase
- **All metrics good**: Continue current practices, share learnings
