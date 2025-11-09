# core-workflow Plugin

Universal Research → Plan → Implement → Learn workflow demonstrating all 12 factors of AgentOps.

## Installation

```bash
/plugin marketplace add boshu2/agentops
/plugin install core-workflow@agentops
```

## What You Get

- **4 specialized agents** (research, plan, implement, learn)
- **5 slash commands** (/research, /plan, /implement, /learn, /workflow)
- Complete phase-based workflow
- **Token budget:** 8,000 tokens (4%)

## Quick Start

```bash
# Complete workflow
/workflow add-feature

# Or individual phases
/research [topic]
/plan [research-bundle]
/implement [plan]
/learn
```

## The 4-Phase Workflow

### Phase 1: Research (Factor II, VI, VII)
```bash
/research [topic]
```
- Gather context, understand problem
- Use JIT loading (stay under 40%)
- Create research bundle for continuity

### Phase 2: Plan (Factor III, IX, XII)
```bash
/plan [research-bundle]
```
- Design solution, break down tasks
- Extract patterns, document decisions
- Create portable implementation spec

### Phase 3: Implement (Factor IV, V, XI)
```bash
/implement [plan]
```
- Execute with validation gates
- Track metrics, enforce Laws
- Commit with learnings

### Phase 4: Learn (Factor IX, X)
```bash
/learn
```
- Extract reusable patterns
- Identify improvements
- Document for future work

## 12-Factor Mapping

This plugin demonstrates all 12 factors of AgentOps:

| Factor | Demonstrated By |
|--------|-----------------|
| I. Git Memory | All phases commit learnings |
| II. JIT Context | Load only what's needed per phase |
| III. Single-Responsibility | One agent = one phase |
| IV. Validation Gates | Test before commit |
| V. Operational Telemetry | Track metrics |
| VI. Session Continuity | Bundles between phases |
| VII. Intelligent Routing | Route to right approach |
| VIII. Human Gate Reviews | Approval between phases |
| IX. Pattern Extraction | Capture reusable insights |
| X. Continuous Improvement | Identify improvements |
| XI. Constitutional Guardrails | Enforce Laws automatically |
| XII. Domain Portability | Works in any domain |

## Documentation

Full documentation at [12-factor-agentops](https://github.com/boshu2/12-factor-agentops)

## License

Apache-2.0
