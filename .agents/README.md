# .agents/ — Knowledge Artifact Store

Persistent context for AI-assisted development. Skills read and write artifacts here across sessions.

## Naming Convention

All artifact filenames follow: `YYYY-MM-DD-<slug>.md`

- Dates use `YYYY-MM-DD` (e.g., `2026-02-15-auth-refactor.md`)
- ISO 8601 timestamps (`date -Iseconds`) are used inside file content (JSON, logs), never in filenames
- Patterns use descriptive names without dates: `<pattern-name>.md`

## Directory Structure

### Core Knowledge (never pruned)

| Directory | Files | Purpose | Written By |
|-----------|-------|---------|------------|
| `learnings/` | 90 | Session insights, extracted knowledge | /retro, /extract |
| `patterns/` | 3 | Reusable solutions promoted from learnings | /forge, manual |
| `research/` | 79 | Deep codebase exploration reports | /research |
| `plans/` | 77 | Implementation roadmaps, epic decomposition | /plan |
| `retros/` | 26 | Retrospective summaries | /retro |

### Validation & Review

| Directory | Files | Purpose | Written By |
|-----------|-------|---------|------------|
| `council/` | 378 | Council reports (vibe, pre-mortem, post-mortem, quick) | /council, /vibe, /pre-mortem, /post-mortem |
| `vibe/` | 14 | Vibe-specific artifacts (complexity analysis) | /vibe |
| `specs/` | 9 | Contract specs for test-first mode | /crank (--test-first) |

### Workflow State

| Directory | Files | Purpose | Written By |
|-----------|-------|---------|------------|
| `rpi/` | 8 | RPI phase summaries, next-work.jsonl, schema | /rpi |
| `crank/` | 2 | Wave checkpoint files | /crank |
| `evolve/` | 12 | Fitness snapshots, cycle history, session summaries | /evolve |

### Session & Handoff

| Directory | Files | Purpose | Written By |
|-----------|-------|---------|------------|
| `handoff/` | 17 | Session handoff docs + continuation prompts | /handoff |
| `releases/` | 20 | Release notes + audit trails | /release |
| `doc/` | 6 | Generated documentation artifacts | /doc |

### Infrastructure (managed by ao CLI)

| Directory | Files | Purpose | Written By |
|-----------|-------|---------|------------|
| `ao/` | 828 | CLI state: chain.jsonl, sessions, index, provenance | ao CLI (automated) |
| `tooling/` | 4,665 | Scanner output (gitleaks, gosec, trivy, semgrep, etc.) | /vibe tooling scripts |
| `knowledge/` | 7 | Knowledge pipeline: pending/ for unprocessed learnings | /retro, /post-mortem fallback |
| `teams/` | 7 | Team coordination state | /swarm, /crank |
| `codex-team/` | 2 | Codex agent output files | /codex-team |

### Legacy (no active writer)

| Directory | Files | Purpose | Notes |
|-----------|-------|---------|-------|
| `pre-mortems/` | 18 | Early pre-mortem reports (Jan 2026) | Superseded by council/ path convention |
| `reports/` | 6 | Early validation reports (Dec 2025–Jan 2026) | Superseded by council/ |
| `assessments/` | 2 | One-off assessment artifacts | No skill writes here |
| `bundles/` | 1 | Context bundles (deprecated /bundle-load) | Legacy feature |
| `compaction-snapshots/` | 1 | Context compaction artifacts | Automated cleanup |
| `docs/` | 1 | Stray doc artifact | Not the same as doc/ |
| `execution/` | 1 | Legacy execution state | No skill writes here |
| `issues/` | 1 | Legacy issue artifact | Superseded by .beads/ |
| `mail/` | 1 | Legacy agent mail artifact | Superseded by gt mail |
| `patches/` | 1 | Legacy patch artifact | No skill writes here |
| `ralph/` | 1 | Legacy Ralph Wiggum test artifact | No skill writes here |

## Pruning

| Directory | Policy | Rationale |
|-----------|--------|-----------|
| `learnings/` | **Keep all** | Core knowledge assets, feed the flywheel |
| `patterns/` | **Keep all** | Promoted knowledge, highest value |
| `research/` | **Keep all** | Historical context, reasonable growth |
| `plans/` | **Keep all** | Implementation record |
| `retros/` | **Keep all** | Learning history |
| `council/` | **Keep last 30** | Reports are regenerable; 378 files is excessive |
| `tooling/` | **Keep last run only** | 1.1GB of regenerable scanner output. Already gitignored (only `.gitkeep` tracked) |
| `knowledge/pending/` | **Process or delete after 14 days** | Dead-end without ao CLI |
| `rpi/phase-*-summary-*` | **Prune after 30 days** | Phase summaries are session-scoped context |
| `ao/sessions/` | **Keep last 50** | ao CLI manages internally |
| `handoff/` | **Keep last 10** | Recent handoffs have value; old ones are stale |
| Legacy dirs | **Archive or delete** | No active writers; contents preserved in git history |

Run `scripts/prune-agents.sh --dry-run` to see what would be cleaned up.

## Frontmatter Schema

Documents may use YAML frontmatter:

```yaml
---
date: YYYY-MM-DD
type: Research | Plan | Pattern | Learning | Retro
topic: "Human-readable title"
tags: [type-tag, domain-tag]
status: DRAFT | COMPLETE | ACTIVE | DEPRECATED
---
```
