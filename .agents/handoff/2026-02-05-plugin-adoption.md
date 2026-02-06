# Handoff: Plugin Adoption Improvements

**Date:** 2026-02-05
**Session:** Council expansion (ag-zh0) + brainstorm + plan + pre-mortem for adoption epic (ag-iyl)
**Status:** Between tasks — plan created, council-validated, ready for spike + execution

---

## What We Accomplished This Session

### 1. Completed ag-zh0: Expand /council beyond code review

Cranked through 5 child issues in 2 waves (7 commits):

- **ag-zh0.1**: Added `research` and `analyze` task types (5 total now)
- **ag-zh0.2**: Added `--explorers=N` for judge sub-agent spawning (up to 24 parallel agents)
- **ag-zh0.3**: Added `--preset=<name>` (5 built-in: default, security-audit, architecture, research, ops) and `--perspectives-file=<path>` for custom persona definitions
- **ag-zh0.4**: Reframed council as general-purpose consensus tool, updated examples
- **ag-zh0.5**: Updated /vibe, /pre-mortem, /post-mortem wrappers for new council features
- Updated model defaults: gpt-5.2 → **gpt-5.3**, opus stays as friendly name (maps to **4.6**)

**Files changed:**
- `skills/council/SKILL.md` — major expansion (+394 lines)
- `skills/vibe/SKILL.md` — --preset and --explorers passthrough
- `skills/pre-mortem/SKILL.md` — --preset and --explorers passthrough
- `skills/post-mortem/SKILL.md` — --preset and --explorers passthrough

### 2. Ran council brainstorm on plugin improvements

2 Opus 4.6 judges (pragmatist + skeptic) brainstormed ways to improve the plugin. Both converged on: **"The #1 problem is adoption, not capability."** Top 5 consensus improvements identified.

**Artifact:** `.agents/council/2026-02-05-brainstorm-plugin-improvements.md`

### 3. Created plan for ag-iyl: Plugin Adoption Improvements

Decomposed brainstorm findings into 7 beads issues across 3 waves:

| Wave | Issues |
|------|--------|
| Wave 1 (parallel) | ag-iyl.1 (hide internal skills), ag-iyl.2 (council --quick), ag-iyl.3 (CLI degradation) |
| Wave 2 (after W1) | ag-iyl.4 (/quickstart), ag-iyl.5 (auto-flywheel), ag-iyl.6 (/status) |
| Wave 3 (after W2) | ag-iyl.7 (docs update) |

**Artifact:** `.agents/plans/2026-02-05-plugin-improvement-plan.md`

### 4. Council pre-mortem on the plan — Verdict: WARN

Both judges flagged critical feasibility issue:

| Finding | Impact |
|---------|--------|
| **ag-iyl.1**: `invocable: false` has no implementation path — skills CLI ignores frontmatter | Blocks Wave 2 |
| **ag-iyl.3**: Under-scoped (Medium→High) — split into detect+warn pass vs actual fallbacks | Risk to timeline |
| **ag-iyl.5**: No session-end hook exists — pivot to user-triggered extraction | Design change |
| **ag-iyl.4**: Missing dependency on ag-iyl.3 — new users most likely to lack CLIs | Fixed in beads |

All council findings annotated as comments on respective beads issues. Dependency ag-iyl.3→ag-iyl.4 added.

**Artifact:** `.agents/council/2026-02-05-validate-plugin-improvement-plan.md`

---

## Where We Paused

**Last action:** Council pre-mortem on ag-iyl plan, findings applied to beads
**Next action:** 30-minute spike on ag-iyl.1 to validate skill-hiding mechanism, then /crank ag-iyl
**Blockers:** ag-iyl.1 needs feasibility spike before Wave 1 can start

### Spike Required (30 min)

Validate how to hide internal skills from user-facing list. Options:
1. PR to skills CLI to support `invocable: false` frontmatter field
2. Underscore-prefix naming convention (`_shared/`, `_standards/`)
3. Move internals to non-scanned subdirectory
4. `.skillignore` file

Check: `~/.claude/plugins/marketplaces/agentops-marketplace/` and skills CLI source to understand loading mechanism.

---

## Context to Gather for Next Session

1. **Skills CLI source code** — how does it discover and load skills from a plugin? Does it scan directories, read manifests, or parse frontmatter?
2. **Claude Code plugin loader** — how does `system-reminder` skill list get populated? Is it from plugin.json, directory scan, or something else?
3. **Claude Code hooks API** — what lifecycle hooks exist? SessionStart exists (we use it). Does SessionEnd exist?

---

## Questions to Answer

1. Can the skills CLI be patched to support `invocable: false`, or is a workaround needed?
2. Should council --quick be named `/check` instead to avoid semantic confusion?
3. Is the existing `using-agentops` auto-inject hook a reliable model for auto-flywheel injection?

---

## Files to Read

```
# Priority files (read first)
.agents/plans/2026-02-05-plugin-improvement-plan.md
.agents/council/2026-02-05-validate-plugin-improvement-plan.md
.agents/council/2026-02-05-brainstorm-plugin-improvements.md

# Core skill files changed this session
skills/council/SKILL.md
skills/vibe/SKILL.md
skills/pre-mortem/SKILL.md
skills/post-mortem/SKILL.md

# Plugin structure
.claude-plugin/plugin.json
skills/SKILL-TIERS.md

# Memory
~/.claude/projects/-Users-fullerbt-gt-agentops-crew-nami/memory/MEMORY.md
```

---

## Beads State

```
Epic: ag-zh0 (CLOSED) — Council expansion, 5/5 issues done
Epic: ag-iyl (OPEN) — Plugin adoption improvements, 0/7 issues done
  Wave 1 ready: ag-iyl.1, ag-iyl.2, ag-iyl.3
  Wave 2 blocked: ag-iyl.4, ag-iyl.5, ag-iyl.6
  Wave 3 blocked: ag-iyl.7
```
