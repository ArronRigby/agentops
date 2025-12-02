# core-workflow Plugin

Universal Research → Plan → Implement → Learn workflow demonstrating all 12 factors of AgentOps.

**Why this workflow exists:** Complex work fails without structure. Research prevents building wrong solutions. Planning prevents scope creep. Validation prevents cascading bugs. Learning captures institutional memory. This plugin enforces these practices automatically.

## Installation

```bash
/plugin marketplace add boshu2/agentops
/plugin install core-workflow@agentops
```

## What You Get

- **4 specialized agents** (research, plan, implement, learn)
- **5 slash commands** (/research, /plan, /implement, /learn, /workflow)
- Complete phase-based workflow with human gates
- **Token budget:** 8,000 tokens (4%)

## Quick Start

```bash
# Complete workflow (recommended for complex work)
/workflow add-feature

# Individual phases (when partial workflow needed)
/research [topic]
/plan [research-bundle]
/implement [plan]
/learn
```

## The 4-Phase Workflow

### Phase 1: Research (Outer Loop)

```bash
/research [topic]
```

**Purpose:** Explore problem space before committing to a solution.

**Opus 4.5 behaviors:**
- Investigate before planning - read files, understand patterns
- Use parallel tool calls when gathering context
- Document findings with file:line references

**Output:** Research bundle with options, constraints, and recommendations.

### Phase 2: Plan (Middle Loop)

```bash
/plan [research-bundle]
```

**Purpose:** Design solution and create implementation specification.

**Opus 4.5 behaviors:**
- Avoid overengineering - simplest solution that works
- Quantify scope - specific files, line ranges, task counts
- Document decisions with rationale

**Output:** Implementation spec with tasks, acceptance criteria, and risks.

### Phase 3: Implement (Inner Loop)

```bash
/implement [plan]
```

**Purpose:** Execute approved plan with continuous validation.

**Opus 4.5 behaviors:**
- Default to action - execute the plan, don't re-research
- Validate before proceeding - each task verified before next
- Communicate outcomes - brief summaries after each task

**Output:** Working solution + implementation report.

### Phase 4: Learn

```bash
/learn
```

**Purpose:** Extract patterns and identify improvements.

**Output:** Patterns documented, process improvements captured.

## 12-Factor Mapping

| Factor | Where Demonstrated |
|--------|-------------------|
| I. Git Memory | All phases commit with context |
| II. JIT Context | Research loads only what's needed |
| III. Single-Responsibility | One phase = one agent |
| IV. Validation Gates | Implement validates each task |
| V. Operational Telemetry | Track metrics throughout |
| VI. Session Continuity | Bundles between phases |
| VII. Intelligent Routing | Route to right research approach |
| VIII. Human Gate Reviews | Approval between phases |
| IX. Pattern Extraction | Learn phase captures reusables |
| X. Continuous Improvement | Identify process improvements |
| XI. Constitutional Guardrails | Enforce Laws automatically |
| XII. Domain Portability | Works in any domain |

## Vibe Level Integration

| Level | Workflow Recommendation |
|-------|------------------------|
| 5 (Format) | Skip workflow |
| 4 (Boilerplate) | Skip research, minimal plan |
| 3 (CRUD) | Light research, standard plan |
| 2 (Features) | Full workflow |
| 1 (Architecture) | Full workflow + extended research |
| 0 (Novel) | Extended research phase |

## When to Use

**Use full /workflow for:**
- New features with unclear scope
- Architectural changes
- Work spanning multiple sessions

**Use individual phases for:**
- Research already complete → `/plan` directly
- Plan already approved → `/implement` directly
- Extracting lessons from past work → `/learn` directly

**Skip workflow for:**
- Quick fixes with known solutions
- Formatting/linting tasks
- Simple bug fixes

## Documentation

Full documentation at [12-factor-agentops](https://github.com/boshu2/12-factor-agentops)

## License

Apache-2.0
