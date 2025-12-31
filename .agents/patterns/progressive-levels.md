---
date: 2025-12-30
type: Pattern
category: "Documentation"
tags: [pattern, education, documentation, progressive-disclosure]
status: ACTIVE
---

# Pattern: Progressive Levels

## When to Use

- Teaching a complex system with multiple concepts
- Documentation is too dense for beginners
- Users have varying skill levels
- You want self-service onboarding

## The Pattern

### Structure

```
levels/
├── README.md              # Overview and progression path
├── L1-basics/             # Minimal, just works
│   ├── README.md          # What you'll learn
│   ├── command.md         # 50 lines max
│   └── demo/              # Real transcripts
├── L2-{concept}/          # Adds ONE concept
│   ├── README.md
│   ├── command.md         # Can reference L1
│   └── demo/
├── L3-{concept}/          # Adds ONE more concept
│   ...
└── L5-{concept}/          # Full capability
```

### Rules

1. **L1 is sacred**: Maximum 50 lines per command file
2. **One concept per level**: L2 adds persistence, not persistence+tracking+auth
3. **Each level builds on previous**: L3 assumes L1+L2 mastery
4. **Demo transcripts required**: Show, don't tell
5. **Reference for frameworks**: Extract theory to `/reference/`

### Level Naming Convention

```
L1-basics         # No adjectives, just "basics"
L2-persistence    # The ONE concept this level adds
L3-state          # Noun form of the concept
L4-parallelization
L5-orchestration
```

### Command File Template (L1)

```markdown
---
description: One line
---

# /command

[2-3 sentences: what it does, when to use it]

## Usage

```
/command "input"
```

## Steps

1. [What happens]
2. [What happens]
3. [What happens]

## Output

[Where output goes]

## Example

```
You: /command "input"
Claude: [Brief transcript]
```

## Next

[What to run next]
```

### Demo Transcript Template

```markdown
# Demo: /command Session

## Before
- [Starting state]

## Session
```
You: /command "input"

Claude: [Full transcript with tool calls]
```

## After
- [What changed]

## What You Learned
- [Takeaway 1]
- [Takeaway 2]
```

## Why It Works

1. **Reduces cognitive load**: Users process one concept at a time
2. **Self-selecting**: Advanced users skip to L3+, beginners stay at L1
3. **Progressive commitment**: Users invest more as they see value
4. **Maintainable**: Each level is isolated, can update independently

## Examples

### From agentops

```
levels/
├── L1-basics/
│   ├── research.md        # 42 lines - explore codebase
│   ├── implement.md       # 49 lines - make changes
│   └── demo/              # 2 transcripts
├── L2-persistence/
│   ├── research.md        # 55 lines - saves to .agents/
│   ├── retro.md           # 60 lines - extract learnings
│   └── demo/              # 2 transcripts
├── L3-state-management/
│   ├── plan.md            # 69 lines - create issues
│   ├── implement.md       # 79 lines - issue-driven
│   └── demo/              # 2 transcripts
├── L4-parallelization/
│   ├── implement-wave.md  # 92 lines - parallel execution
│   └── demo/              # 1 transcript
└── L5-orchestration/
    ├── autopilot.md       # 94 lines - full automation
    └── demo/              # 1 transcript
```

### Progression

| Level | Concept Added | Line Count |
|-------|---------------|------------|
| L1 | None (baseline) | ~45 |
| L2 | .agents/ persistence | ~55 |
| L3 | Issue tracking | ~75 |
| L4 | Parallelization | ~90 |
| L5 | Automation | ~95 |

## Anti-Patterns

- **Level inflation**: Adding concepts that aren't core to the tool
- **Skipping L1**: Every system needs a "just works" entry point
- **Framework in L1**: Theory belongs in reference docs
- **Synthetic demos**: Use real captured sessions when possible

## Related

- Source: [Kubernetes the Hard Way](https://github.com/kelseyhightower/kubernetes-the-hard-way)
- Learning: `.agents/learnings/2025-12-30-progressive-documentation.md`
