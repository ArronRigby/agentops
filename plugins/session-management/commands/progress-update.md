---
description: Interactively update progress files without manual JSON editing
allowed-tools: Read, Write, Edit
---

# /progress-update - Update Progress Interactively

Update `claude-progress.json` through guided prompts instead of manual editing.

## Usage

```bash
/progress-update                  # Interactive full update
/progress-update --working-on     # Update current task only
/progress-update --blocker        # Add a blocker
/progress-update --next-steps     # Update next steps
/progress-update --complete       # Mark current task complete
```

## Interactive Mode

```
📝 Progress Update

Current state:
  Working on: Add refresh token rotation
  Vibe Level: 2
  Next steps:
    1. Implement token rotation logic
    2. Add Redis storage
    3. Write tests

What would you like to update?
1. Working on (current task)
2. Vibe level
3. Next steps
4. Add blocker
5. Mark task complete
6. Add session note

> ___
```

## Update Types

### Working On

```bash
/progress-update --working-on
```

```
Current: Add refresh token rotation
New task: ___

Updated ✓
```

### Blocker

```bash
/progress-update --blocker
```

```
Add blocker:
Description: ___
Severity (low/medium/high): ___
Needs: ___

Added to blockers ✓
```

### Next Steps

```bash
/progress-update --next-steps
```

```
Current next steps:
1. Implement token rotation logic
2. Add Redis storage
3. Write tests

Actions:
1. Add step
2. Remove step
3. Reorder steps
4. Replace all

> ___
```

### Mark Complete

```bash
/progress-update --complete
```

```
Marking complete: Add refresh token rotation

Summary of completion: ___
New task (or "none"): ___

Updated ✓
Moving to: [new task or "no active task"]
```

## Progress File Schema

```json
{
  "project": "string - project name",
  "current_state": {
    "working_on": "string - current task",
    "vibe_level": "number 0-5",
    "next_steps": ["array of strings"],
    "blockers": [
      {
        "description": "string",
        "severity": "low|medium|high",
        "needs": "string - what's needed to unblock",
        "added": "YYYY-MM-DD"
      }
    ]
  },
  "sessions": [
    {
      "date": "YYYY-MM-DD",
      "summary": "string",
      "commits": "number",
      "duration_minutes": "number",
      "vibe_level": "number"
    }
  ],
  "resume_summary": "string - for next session startup"
}
```

## Auto-Commit

After update:
```bash
git add claude-progress.json
git commit -m "progress: [brief description of update]"
```
