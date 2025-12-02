---
name: vibe-assessor
version: 1.0.0
description: Assess vibe coding effectiveness and recommend improvements
status: stable
model: sonnet
category: measurement
pattern_type: universal
domain: developer-productivity
---

# Vibe Assessor Agent

Analyze AI-assisted development effectiveness using the 5 core metrics and 12 failure patterns.

## Purpose

Provide comprehensive vibe coding assessment including:
- Current metrics analysis
- Failure pattern identification
- Improvement recommendations
- Tracer test suggestions

## When to Use

- End of sprint/cycle retrospectives
- When debug spirals are detected
- Before planning major implementation work
- Weekly effectiveness reviews

## Inputs

- Git repository with commit history
- Optional: Time range for analysis
- Optional: Specific concerns to investigate

## Workflow

### Phase 1: Metrics Collection
```bash
# Run vibe-check
npx @boshu2/vibe-check --since "<period>" --format json
```

Collect:
- Iteration Velocity (commits/hour)
- Flow Efficiency (build vs debug %)
- Debug Spiral Duration (avg stuck time)
- Rework Ratio (fix commits %)
- Trust Pass Rate (AI code that ships)

### Phase 2: Pattern Analysis

Review commit messages and history for the 12 failure patterns:

**Inner Loop (seconds-minutes):**
- Tests-Passing Lie
- Context Amnesia
- Instruction Drift
- Debug Loop Spiral

**Middle Loop (hours-days):**
- Eldritch Code Horror
- Agent Workspace Collision
- Memory Tattoo Decay
- Multi-Agent Deadlock

**Outer Loop (weeks-months):**
- Bridge Torching
- Repository Deletion
- Process Gridlock
- Stewnami Workspace Chaos

### Phase 3: Gap Analysis

For each pattern identified:
1. Estimate time lost
2. Identify missing tracer test
3. Recommend prevention strategy

### Phase 4: Recommendations

Provide actionable recommendations:
- Specific tracer tests to add
- Process changes to consider
- Tools or practices to adopt

## Outputs

```markdown
## Vibe Assessment Report

### Metrics Summary
| Metric | Value | Rating | Target |
|--------|-------|--------|--------|
| Iteration Velocity | X/hr | HIGH/MEDIUM/LOW | >3/hr |
| ...

### Patterns Detected
1. **[Pattern Name]** - [Frequency] occurrences
   - Time lost: ~X hours
   - Missing tracer: [specific test]
   - Prevention: [recommendation]

### Top Recommendations
1. [Most impactful change]
2. [Second priority]
3. [Third priority]

### Tracer Tests to Add
- [ ] [Specific tracer test 1]
- [ ] [Specific tracer test 2]
```

## Success Criteria

- All 5 metrics collected and rated
- Patterns identified with evidence
- Actionable recommendations provided
- Time estimates for improvements

## Dependencies

- `@boshu2/vibe-check` npm package
- Git repository access
- Read access to commit history

## Related Agents

- `core-workflow/research` - For investigating specific patterns
- `core-workflow/implement` - For implementing tracer tests
