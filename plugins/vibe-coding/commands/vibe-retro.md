---
description: Run vibe coding retrospective with failure pattern analysis
allowed-tools: Bash(npx*), Read, Grep
argument-hint: "[--since 'time']"
---

# /vibe-retro - Vibe Coding Retrospective

Map completed work to the 12 vibe-coding failure patterns and identify tracer testing gaps.

## Usage

```bash
/vibe-retro                      # Current session
/vibe-retro --since "1 week ago" # Last week
```

## The 12 Failure Patterns

### Inner Loop (Seconds-Minutes)

| Pattern | Symptom | Prevention |
|---------|---------|------------|
| **Tests-Passing Lie** | AI claims tests pass but code doesn't work | Run tests yourself, don't trust claims |
| **Context Amnesia** | AI forgets instructions from minutes ago | Smaller context, explicit reminders |
| **Instruction Drift** | Gradual deviation from requirements | Checkpoint against original spec |
| **Debug Loop Spiral** | Adding logging instead of fixing root cause | Time-box debugging, escalate early |

### Middle Loop (Hours-Days)

| Pattern | Symptom | Prevention |
|---------|---------|------------|
| **Eldritch Code Horror** | Incomprehensible 3000+ line functions | Enforce file size limits, decompose |
| **Agent Workspace Collision** | Multiple agents modifying same files | Clear ownership, lock files |
| **Memory Tattoo Decay** | AI can't resume previous work | Bundle context, explicit handoffs |
| **Multi-Agent Deadlock** | Agents waiting on each other | Clear dependencies, timeout policies |

### Outer Loop (Weeks-Months)

| Pattern | Symptom | Prevention |
|---------|---------|------------|
| **Bridge Torching** | API changes break functionality | Version pinning, compatibility tests |
| **Repository Deletion** | AI deletes "unused" branches/files | Protected branches, backup policies |
| **Process Gridlock** | Approval processes negate productivity | Streamline reviews, async approval |
| **Stewnami Workspace Chaos** | Multiple conflicting states | Clear state management, cleanup |

## Analysis Steps

1. **Run vibe-check first:**
   ```bash
   npx @boshu2/vibe-check --since "<period>" --format json
   ```

2. **Review git history for patterns:**
   ```bash
   git log --oneline --since="<period>" | head -50
   ```

3. **Identify which patterns occurred**

4. **Calculate time lost:**
   - Estimate hours spent on each pattern
   - Total preventable time loss

5. **Recommend tracer tests:**
   - For each pattern hit, identify the tracer that would have prevented it

## Output

Provide:
1. **Patterns Hit** - Which of the 12 patterns occurred
2. **Time Lost** - Estimated hours per pattern
3. **Tracer Gaps** - What tracer tests were missing
4. **Recommendations** - Specific tracers to add for next cycle

## Integration

This command integrates with `/retro` for full session retrospectives.
