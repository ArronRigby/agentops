# Session Management Plugin

**Never lose context between sessions. Resume exactly where you left off.**

## The Problem

AI agents have goldfish memory. Each session starts fresh. Without session management:
- You re-explain context every time
- Work gets lost between sessions
- Multi-day projects become impossible
- Debugging history disappears

## The Solution

Session Management provides:
- **Progress Tracking** - `claude-progress.json` tracks state across sessions
- **Context Bundles** - Compressed snapshots for efficient resumption
- **Session Protocol** - Start/end rituals that preserve context
- **The 40% Rule** - Stay under 40% context to prevent collapse

## Installation

```bash
/plugin marketplace add boshu2/agentops
/plugin install session-management@agentops
```

## Commands

| Command | Purpose |
|---------|---------|
| `/session-start` | Initialize session with context detection |
| `/session-end` | Gracefully end with progress save |
| `/session-resume` | Single-command resume with auto-detection |
| `/bundle-save` | Save compressed context bundle |
| `/bundle-load` | Load context bundle |
| `/progress-update` | Update progress files interactively |

## Skills

| Skill | Purpose |
|-------|---------|
| `context-bundling` | Create and load context bundles |
| `progress-tracking` | Manage claude-progress.json |

## Agent

| Agent | Purpose |
|-------|---------|
| `context-manager` | Automated context and session management |

---

## The 40% Rule (Context Engineering)

**Problem:** 200k token limit. Loading everything = 99% information loss, context collapse.

**Solution:** Stay under 40% of token budget (80k of 200k).

```
Token Usage Zones:
🟢 <35% (70k)   - GREEN: Continue
⚡ 35-40% (70-80k) - YELLOW: Prepare to transition
⚠️ 40-60% (80-120k) - RED: Transition NOW
🔴 >60% (120k+) - CRITICAL: Reset immediately
```

**Pattern:** Gather → Glean → Summarize (JIT loading, not upfront loading)

---

## Progress Tracking (claude-progress.json)

Track state across sessions:

```json
{
  "project": "auth-refactor",
  "current_state": {
    "working_on": "Add refresh token rotation",
    "vibe_level": 2,
    "next_steps": [
      "Implement token rotation logic",
      "Add Redis storage",
      "Write tests"
    ],
    "blockers": []
  },
  "sessions": [
    {
      "date": "2025-11-30",
      "summary": "Research complete. JWT + Redis pattern identified.",
      "commits": 3,
      "duration_minutes": 45
    }
  ],
  "resume_summary": "Ready for implementation. Start with token model in src/models/token.ts"
}
```

---

## Context Bundles

Compress 60k tokens of research into 2-3k tokens:

```yaml
bundle_type: research
topic: user-authentication
phase: research-complete
created: 2025-11-30
findings_summary: |
  - JWT-based auth with Redis blacklist
  - No refresh tokens currently
  - Redis is SPOF (no HA)
constraints:
  - pyjwt 2.4.0 dependency
  - 24-hour token expiry
success_criteria:
  - Refresh token rotation working
  - Tests cover edge cases
next_phase: plan
```

**Bundle locations:**
- `.agents/bundles/` - Research and plan bundles
- `.agents/briefs/` - Worker briefs for multi-agent work

---

## Session Protocol

### Starting a Session

```bash
/session-start
```

1. Checks for `claude-progress.json`
2. Detects if ongoing project exists
3. Loads minimal context (resume_summary)
4. Suggests next actions

### Ending a Session

```bash
/session-end
```

1. Runs `git status` - warns if uncommitted changes
2. Asks for session summary (1 sentence)
3. Updates `claude-progress.json`
4. Offers to save bundle
5. Suggests `/retro` for learning extraction

### Resuming Mid-Project

```bash
/session-resume
```

Single command that:
1. Reads `claude-progress.json`
2. Finds matching bundle if exists
3. Loads context
4. Shows current state and next steps

---

## Usage Example

```bash
# Day 1: Start new work
/session-start
> No existing project. What are you working on?
> "Implement OAuth integration"

/research oauth-patterns
# ... research complete ...
/bundle-save oauth-research

/session-end
> Summary? "Research complete. Using OAuth 2.0 PKCE flow."

# Day 2: Resume
/session-resume
> Found: oauth-refactor project
> Last session: Research complete
> Next: Plan the implementation
> Loading bundle: oauth-research

/plan
# ... planning complete ...

/session-end
> Summary? "Plan approved. 5 tasks identified."
```

---

## Dependencies

- `core-workflow` plugin (required base)

## Links

- [12-Factor AgentOps](https://github.com/boshu2/12-factor-agentops)
- [Factor VI: Session Continuity](https://github.com/boshu2/12-factor-agentops)
