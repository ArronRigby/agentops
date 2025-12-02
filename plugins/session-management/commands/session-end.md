---
description: End session gracefully with progress update and optional retrospective
allowed-tools: Read, Write, Bash(git*)
---

# /session-end - End Session Gracefully

Properly close a session with progress saving and optional retrospective.

## Usage

```bash
/session-end
```

## Protocol

### Step 1: Check Git Status

```bash
git status --short
```

If uncommitted changes exist:
```
⚠️ Uncommitted changes detected:
   M src/auth/middleware.ts
   M tests/auth.test.ts

Would you like to:
1. Commit these changes
2. Stash for later
3. Leave uncommitted (not recommended)
```

### Step 2: Session Summary

Ask:
```
One-sentence summary of this session:
> ___
```

### Step 3: Update Progress File

Update `claude-progress.json`:

```json
{
  "current_state": {
    "working_on": "[updated based on work]",
    "next_steps": ["[updated next steps]"],
    "blockers": ["[any blockers encountered]"]
  },
  "sessions": [
    // ... existing sessions
    {
      "date": "YYYY-MM-DD",
      "summary": "[user's summary]",
      "commits": N,
      "duration_minutes": M,
      "vibe_level": L
    }
  ],
  "resume_summary": "[Concise summary for next session startup]"
}
```

### Step 4: Check Feature Progress

If `feature-list.json` exists:
- Check if any features were completed
- Update `passes: true` and `completed_date` for finished features
- Never modify feature definitions, only mark completion

### Step 5: Offer Bundle Save

```
Would you like to save a context bundle for this work?
- Bundle name: [suggested-name]
- Size: ~Xk tokens compressed

(yes/no)
```

### Step 6: Suggest Retrospective

```
Would you like to run a retrospective?
/retro - Extract patterns and learnings

(yes/skip)
```

## Output

```
✅ Session ended gracefully

📊 Session Stats:
   Duration: X minutes
   Commits: N
   Vibe Level: L

📝 Progress saved to claude-progress.json
📦 Bundle saved: [name] (if created)

🔄 To resume: /session-resume
```

## Commit Progress

If progress files were updated:
```bash
git add claude-progress.json feature-list.json
git commit -m "progress: [brief summary]"
```
