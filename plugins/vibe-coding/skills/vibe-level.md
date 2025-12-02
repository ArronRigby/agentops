---
name: vibe-level
description: Classify tasks by Vibe Level (0-5) based on risk, complexity, and AI reliability. Use before starting any implementation work to set appropriate verification strategy.
---

# vibe-level Skill

**Purpose:** Classify task difficulty and set verification strategy

---

## When to Use

- Before starting any implementation work
- When user describes a new task
- When planning a session
- When estimating effort

---

## The 6 Vibe Levels

| Level | Trust | Verify | Use For |
|-------|-------|--------|---------|
| **5** | 95% | Final only | Formatting, linting, typos |
| **4** | 80% | Spot check | Boilerplate, CRUD, simple tests |
| **3** | 60% | Key outputs | Features with known patterns |
| **2** | 40% | Every change | Integrations, auth, external APIs |
| **1** | 20% | Every line | Architecture, infrastructure, security |
| **0** | 0% | N/A | Research, novel problems, unknown domains |

---

## Classification Factors

Analyze each factor (1-5 scale, higher = more risk):

| Factor | Question |
|--------|----------|
| **Reversibility** | Can changes be easily undone? |
| **Blast Radius** | What breaks if this is wrong? |
| **Verification Cost** | How hard is it to verify correctness? |
| **Domain Complexity** | How much context is needed? |
| **AI Track Record** | Has AI succeeded with similar tasks? |

**Scoring:**
- Average score 1-2 → Level 4-5
- Average score 2-3 → Level 3
- Average score 3-4 → Level 1-2
- Average score 4-5 → Level 0-1

---

## Tracer Test Requirements

| Level | Tracer Tests |
|-------|-------------|
| 0 | N/A - research phase |
| 1 | REQUIRED - test every assumption |
| 2 | REQUIRED - test key assumptions |
| 3 | RECOMMENDED - test uncertain areas |
| 4 | OPTIONAL - spot check |
| 5 | SKIP - trust AI output |

---

## Common Tracer Patterns

| Risk Area | Tracer Test |
|-----------|-------------|
| Kubernetes API | `oc api-resources`, dry-run minimal CR |
| Secrets/Auth | Validate secret structure, test OAuth |
| SSL/TLS | Test SSL in container on target |
| Volumes | Deploy minimal pod with mount |
| Images | Test image pull before deployment |
| GitOps | Deploy, wait, diff for drift |

---

## Example Classifications

| Task | Level | Why |
|------|-------|-----|
| "Fix typo in README" | 5 | Reversible, no blast radius |
| "Add new REST endpoint" | 4 | Boilerplate, easy to test |
| "Implement user dashboard" | 3 | Known patterns, moderate complexity |
| "Integrate OAuth provider" | 2 | External dependency, auth is critical |
| "Design new microservice" | 1 | Architecture decisions, high blast radius |
| "Evaluate new AI framework" | 0 | Novel, need research first |

---

## Recording

Record the assigned level in `claude-progress.json`:
```json
{
  "current_state": {
    "vibe_level": 2,
    "vibe_level_reasoning": "OAuth integration with external provider"
  }
}
```
