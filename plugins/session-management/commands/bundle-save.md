---
description: Save compressed research/plan bundles to filesystem
allowed-tools: Write, Read, Bash(mkdir*)
---

# /bundle-save - Save Context Bundle

Compress current session context into a portable bundle for future sessions.

## Usage

```bash
/bundle-save                      # Auto-name based on topic
/bundle-save [name]               # Custom name
/bundle-save --type research      # Specify bundle type
/bundle-save --type plan
```

## Bundle Types

| Type | Contents | Size Target |
|------|----------|-------------|
| `research` | Findings, constraints, options | 2-3k tokens |
| `plan` | Tasks, acceptance criteria, risks | 3-5k tokens |
| `implementation` | Progress, commits, deviations | 2-4k tokens |
| `learning` | Patterns, improvements, failures | 1-2k tokens |

## Bundle Format

```yaml
# .agents/bundles/[name]-[type]-YYYY-MM-DD.md

---
bundle_type: [type]
topic: [topic]
phase: [current phase]
created: YYYY-MM-DD
context_tokens: [original size]
compressed_tokens: [bundle size]
compression_ratio: [X:1]
---

## Executive Summary
[2-3 sentences capturing the essence]

## Key Findings / Tasks / Progress
[Bullet points of most important items]

## Constraints
[What limits our options]

## Success Criteria
[How we know it's done]

## Open Questions
[What still needs answers]

## Next Phase
[What comes next]

## File References
[Key files with line numbers for quick navigation]
```

## Compression Strategy

**From 60k tokens → 2-3k tokens:**

1. **Extract insights, not raw data**
   - "JWT auth with Redis blacklist" not the full code

2. **Preserve file references**
   - `src/auth/middleware.ts:45-89` for quick lookup

3. **Keep decision rationale**
   - "Chose rotation over sliding expiry because..."

4. **Drop intermediate work**
   - Remove exploration dead-ends
   - Keep only successful paths

## Output

```
📦 Bundle saved

Name: auth-research-2025-11-30.md
Type: research
Location: .agents/bundles/
Size: 2.4k tokens (compressed from 58k)
Ratio: 24:1

To load: /bundle-load auth-research-2025-11-30
```

## Directory Structure

```
.agents/
├── bundles/           # Saved bundles
│   ├── auth-research-2025-11-30.md
│   ├── auth-plan-2025-11-30.md
│   └── feature-x-implementation-2025-11-29.md
└── briefs/            # Worker briefs (multi-agent)
    ├── worker-1-backend.md
    └── worker-2-frontend.md
```
