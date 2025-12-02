---
description: Initialize session with standardized get-bearings protocol
allowed-tools: Read, Bash(git*), Glob
---

# /session-start - Initialize Session

Start a new session with automatic context detection and minimal context loading.

## Usage

```bash
/session-start
```

## Protocol

### Step 1: Check for Existing Project

```bash
# Check for progress file
[ -f "claude-progress.json" ] && echo "Ongoing project detected"

# Check for feature list
[ -f "feature-list.json" ] && echo "Feature tracking active"
```

### Step 2: If Project Exists

Display:
```
📋 Ongoing project detected
   Project: [project name]
   Last session: [sessions[-1].summary]
   Working on: [current_state.working_on]
   Vibe Level: [current_state.vibe_level]
   Next: [current_state.next_steps[0]]
```

Load ONLY:
- `resume_summary` from progress file (~100-200 tokens)
- Current working files if specified
- Do NOT load full history

### Step 3: If No Project

Ask:
```
No existing project detected.
What are you working on today?
```

Options:
- Start fresh work
- Search for existing bundles: `/bundle-search`
- Load specific bundle: `/bundle-load [name]`

### Step 4: Establish Context Budget

Report current context estimate:
```
Context Status: 🟢 <5% loaded
Budget: 195k tokens remaining
```

## Output

Provide:
1. Project status (new or resuming)
2. Current state summary
3. Suggested next action
4. Context budget status

## Integration

This command sets up the session. End with `/session-end` for proper closure.
