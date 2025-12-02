---
description: Single-command session resume with auto-detection
allowed-tools: Read, Glob, Bash(git*)
---

# /session-resume - Quick Resume

Single command to resume any previous session with automatic context detection.

## Usage

```bash
/session-resume                    # Auto-detect from progress file
/session-resume [topic]            # Search bundles for topic
/session-resume --bundle [name]    # Load specific bundle
```

## Protocol

### Auto-Detection (No Arguments)

1. **Check progress file:**
   ```bash
   [ -f "claude-progress.json" ] && cat claude-progress.json
   ```

2. **If found, display:**
   ```
   🔄 Resuming: [project name]

   Last session: [sessions[-1].date]
   Summary: [sessions[-1].summary]

   Currently: [current_state.working_on]
   Next steps:
   1. [next_steps[0]]
   2. [next_steps[1]]

   Blockers: [blockers or "None"]
   ```

3. **Load minimal context:**
   - Resume summary (~200 tokens)
   - Current working files if specified
   - Stay under 5% context

### Topic Search (With Argument)

1. **Search bundles:**
   ```bash
   ls -la .agents/bundles/ | grep -i "[topic]"
   ```

2. **If multiple matches:**
   ```
   Found 3 bundles matching "auth":
   1. auth-research-2025-11-28.md (2 days ago)
   2. auth-plan-2025-11-29.md (1 day ago)
   3. oauth-research-2025-11-30.md (today)

   Which to load? (1/2/3)
   ```

3. **Load selected bundle**

### Specific Bundle (--bundle)

```bash
/session-resume --bundle auth-plan-2025-11-29
```

Direct load, no search.

## Output

```
✅ Session resumed

📋 Project: [name]
🎯 Working on: [current task]
📊 Vibe Level: [level]
⏭️ Next: [immediate next step]

Context: 🟢 X% loaded
```

## Ready to Work

After resume, immediately ready for:
- `/plan` if research is complete
- `/implement` if plan is approved
- Direct work if resuming mid-task
