---
description: Determine appropriate Vibe Level for a task
allowed-tools: Read
argument-hint: "[task description]"
---

# /vibe-level - Task Level Classification

Classify a task by appropriate Vibe Level (0-5).

## Usage

```bash
/vibe-level "implement new API endpoint"
/vibe-level "fix typo in README"
/vibe-level "redesign authentication system"
```

## Classification

Analyze the task: **$ARGUMENTS**

Consider:
1. **Reversibility** - Can changes be easily undone?
2. **Blast Radius** - What breaks if wrong?
3. **Verification Cost** - How hard to check?
4. **Domain Complexity** - How much context needed?
5. **AI Track Record** - Previous success with similar tasks?

## Vibe Levels

| Level | Trust | Verify | Use For | Examples |
|-------|-------|--------|---------|----------|
| 5 | 95% | Final only | Format, lint | Fix whitespace, rename variable |
| 4 | 80% | Spot check | Boilerplate | Add CRUD endpoint, write tests |
| 3 | 60% | Key outputs | Features | New feature with known patterns |
| 2 | 40% | Every change | Integrations | API integration, auth flow |
| 1 | 20% | Every line | Architecture | New system design, infra changes |
| 0 | 0% | N/A | Research | Novel problem, unknown domain |

## Output

Provide:
- Recommended level (0-5)
- Reasoning (which factors drove the decision)
- Verification strategy for this level
- Whether tracer tests are recommended (Level 1-2 always, Level 3 if uncertain)

## Tracer Test Triggers

For Level 1-2 tasks, recommend tracer tests for:

| Risk Area | Tracer Test |
|-----------|-------------|
| API/Schema | `oc api-resources`, dry-run minimal CR |
| Secrets/Auth | Validate secret structure, test OAuth |
| SSL/TLS | Test SSL in container on target cluster |
| Volume/Config | Deploy minimal pod with volume mount |
| Image/Registry | Test image pull before deployment |
| GitOps/Drift | Deploy, wait, diff for operator changes |

## Recording

The vibe level should be recorded in `claude-progress.json` at session end via `/session-end`.
