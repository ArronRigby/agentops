---
name: progress-tracking
description: Manage claude-progress.json for session continuity and project state tracking. Use to maintain state across sessions and track work progress.
---

# progress-tracking Skill

**Purpose:** Maintain persistent state across sessions using claude-progress.json.

---

## When to Use

- Starting a session (read current state)
- Ending a session (write updated state)
- Completing a task (update working_on)
- Encountering a blocker (record it)
- Every 10+ messages (inline update)

---

## Progress File Schema

```json
{
  "project": "project-name",
  "created": "YYYY-MM-DD",
  "current_state": {
    "working_on": "Current task description",
    "vibe_level": 2,
    "phase": "implement",
    "next_steps": [
      "Step 1",
      "Step 2",
      "Step 3"
    ],
    "blockers": [
      {
        "description": "What's blocking",
        "severity": "high",
        "needs": "What's needed to unblock",
        "added": "YYYY-MM-DD"
      }
    ],
    "context_budget": "35%"
  },
  "sessions": [
    {
      "date": "YYYY-MM-DD",
      "summary": "One sentence summary",
      "commits": 3,
      "duration_minutes": 45,
      "vibe_level": 2,
      "patterns_used": ["JWT auth", "Redis caching"]
    }
  ],
  "resume_summary": "Concise summary for next session startup. Include immediate next action.",
  "related_bundles": [
    "auth-research-2025-11-30",
    "auth-plan-2025-11-30"
  ]
}
```

---

## Update Triggers

### Session Start

```json
// Read and display
{
  "resume_summary": "...",
  "current_state": { "working_on": "..." }
}
```

### Session End

```json
// Add new session entry
{
  "sessions": [
    // ... existing
    {
      "date": "YYYY-MM-DD",
      "summary": "[user provided]",
      "commits": N,
      "duration_minutes": M
    }
  ],
  "resume_summary": "[updated for next session]"
}
```

### Task Completion

```json
// Update current_state
{
  "current_state": {
    "working_on": "[next task or 'No active task']",
    "next_steps": ["[updated list]"]
  }
}
```

### Blocker Encountered

```json
// Add to blockers array
{
  "current_state": {
    "blockers": [
      // ... existing
      {
        "description": "[what's blocking]",
        "severity": "high",
        "needs": "[what's needed]",
        "added": "YYYY-MM-DD"
      }
    ]
  }
}
```

### Inline Update (Every 10 Messages)

```json
// Quick state save
{
  "current_state": {
    "working_on": "[current]",
    "next_steps": ["[updated]"],
    "context_budget": "[current %]"
  },
  "resume_summary": "[updated]"
}
```

---

## Resume Summary Best Practices

**Good resume summaries:**
```
"Research complete. JWT with Redis blacklist. Ready to plan refresh token rotation. Start with src/models/token.ts"

"Plan approved. 5 tasks. Starting task 3: Add refresh endpoint to src/routes/auth.ts:23"

"Blocked on Redis HA. Need DevOps input on cluster config. Can continue with task 4 (tests) in meantime."
```

**Bad resume summaries:**
```
"Working on auth stuff"  // Too vague
"See bundle for details"  // No immediate action
"Made progress today"  // No state information
```

---

## Feature List Integration

If `feature-list.json` exists, track feature completion:

```json
// feature-list.json
{
  "features": [
    {
      "id": "F001",
      "name": "User authentication",
      "description": "JWT-based auth with refresh tokens",
      "passes": false,
      "completed_date": null
    },
    {
      "id": "F002",
      "name": "Dashboard",
      "passes": true,
      "completed_date": "2025-11-29"
    }
  ]
}
```

**Rules:**
- ✅ Set `passes: true` when feature complete
- ✅ Add `completed_date`
- ❌ Never modify feature definitions
- ❌ Never delete features

---

## Git Workflow

Progress files should be committed:

```bash
# After significant updates
git add claude-progress.json feature-list.json
git commit -m "progress: [brief description]"
```

**Commit frequency:**
- End of session (always)
- After completing major task
- After encountering blocker
- Every 30-60 minutes of active work

---

## Common Patterns

### New Project

```bash
# Create initial progress file
/progress-update
> Project name: auth-refactor
> Initial task: Research authentication patterns
> Vibe level: 2
```

### Multi-Day Project

```
Day 1: Research → bundle-save → session-end
Day 2: session-resume → plan → bundle-save → session-end
Day 3: session-resume → implement → session-end
Day 4: session-resume → learn → project complete
```

### Parallel Workstreams

Use separate progress files or sections:
```json
{
  "workstreams": {
    "frontend": { "working_on": "..." },
    "backend": { "working_on": "..." }
  }
}
```
