# Documentation vs Reality Analysis

**Date:** 2026-02-07
**Scope:** Full comparison of documented claims vs actual repository state

---

## Executive Summary

The AgentOps repository has a **significant structural drift** between its documentation and its actual implementation. The codebase was restructured from a multi-plugin marketplace model to a single monolithic plugin with a flat `skills/` directory, but several key documentation files were never updated to reflect this change. Additionally, there are numeric discrepancies in skill and agent counts across different docs, and entire documented directories that don't exist.

---

## 1. The Biggest Gap: CLAUDE.md Describes a Phantom Architecture

### What CLAUDE.md claims:

```
plugins/           # Plugin packages (each installable independently)
  core-kit/        # Essential workflow skills (research, formulate, crank, etc.)
  vibe-kit/        # Code validation with domain expert agents
  general-kit/     # Zero-dependency portable version of vibe
  beads-kit/       # Git-based issue tracking integration
  docs-kit/        # Documentation generation and validation
  pr-kit/          # Pull request workflow skills
  dispatch-kit/    # Multi-agent coordination (mail, handoff, dispatch)
  gastown-kit/     # Gas Town orchestration skills
  domain-kit/      # Domain-specific skills (brand guidelines, etc.)
shared/            # Shared resources across plugins
  scripts/         # Common scripts (prescan.sh, etc.)
tests/             # Validation and smoke tests
templates/         # Plugin templates
```

### What actually exists:

| Documented Directory | Exists? | Notes |
|---|---|---|
| `plugins/` | **NO** | Does not exist at all |
| `plugins/core-kit/` | **NO** | None of the 9 `-kit` directories exist |
| `plugins/vibe-kit/` | **NO** | |
| `plugins/general-kit/` | **NO** | |
| `plugins/beads-kit/` | **NO** | |
| `plugins/docs-kit/` | **NO** | |
| `plugins/pr-kit/` | **NO** | |
| `plugins/dispatch-kit/` | **NO** | |
| `plugins/gastown-kit/` | **NO** | |
| `plugins/domain-kit/` | **NO** | |
| `shared/` | **NO** | Does not exist. `lib/` exists instead |
| `shared/scripts/` | **NO** | `lib/scripts/prescan.sh` exists instead |
| `templates/` | **NO** | Does not exist |
| `tests/` | **YES** | This one is correct |

**Actual structure** is a flat `skills/` directory at the repo root with 32 skill subdirectories, and a single `.claude-plugin/plugin.json` manifest. This is a monolithic single-plugin architecture, not a marketplace of independently installable plugin kits.

### Impact

CLAUDE.md is the primary file that Claude Code loads as project instructions. Any AI agent working on this repo gets a completely wrong mental model of the project structure from the start. Commands like:

```bash
./tests/skills/validate-skill.sh plugins/vibe-kit/skills/vibe  # DOESN'T WORK
cp -r templates/skill-template plugins/your-kit/skills/new-skill  # DOESN'T WORK
claude --plugin ./plugins/your-kit  # DOESN'T WORK
```

...all reference paths that don't exist.

---

## 2. CONTRIBUTING.md: Also Describes the Phantom Plugin Structure

CONTRIBUTING.md tells contributors to:

```bash
mkdir -p plugins/your-plugin-name/{.claude-plugin,agents,commands,skills}
```

And shows a plugin structure with per-plugin manifests, per-plugin agents, commands, etc. None of this matches reality. The actual contribution path would involve adding skills to `skills/` and possibly agents inline in SKILL.md files.

---

## 3. Skill Count Discrepancies

Different documents claim different numbers:

| Source | Claim | Actual |
|---|---|---|
| **ARCHITECTURE.md** | "All 21 skills" | **32 skill directories** exist |
| **SKILL-TIERS.md** | "21 user-facing + 11 internal = 32" | **32 total** (matches) |
| **marketplace.json** | "21 skills" in description | **32 skill directories** exist |
| **release-smoke-test.sh** | Validates "all 21 skills" | Only checks 21 of 32 |
| **smoke-test.sh** | Counts "33 skills" | Sees 32 dirs (was 33 at some point) |
| **plugin.json** | No skill count | N/A |

**Analysis:** SKILL-TIERS.md is the most accurate — it correctly accounts for all 32 skills by distinguishing 21 user-facing from 11 internal. ARCHITECTURE.md only shows the 21 user-facing skills and omits the internal ones from its tree diagram, which is misleading. The marketplace description saying "21 skills" undersells the actual count.

### Full Skill Inventory (32 actual):

**21 User-Facing:**
beads, bug-hunt, codex-team, complexity, council, crank, doc, handoff, implement, inbox, knowledge, plan, post-mortem, pre-mortem, quickstart, release, research, retro, status, swarm, trace, vibe

**11 Internal:**
beads, extract, flywheel, forge, inject, judge, provenance, ratchet, shared, standards, using-agentops

**Note:** `beads` appears in both lists in SKILL-TIERS.md — it's listed as user-facing (#skill tier: solo) but also as internal. This is a categorization inconsistency.

---

## 4. The "20 Agents" That Don't Exist as Files

### What ARCHITECTURE.md claims:

> "20 Subagent definitions" in an `agents/` directory

It lists 20 named agents:
- code-reviewer, security-reviewer, security-expert, architecture-expert
- code-quality-expert, ux-expert, plan-compliance-expert, goal-achievement-expert
- ratchet-validator, flywheel-feeder, technical-learnings-expert, process-learnings-expert
- integration-failure-expert, ops-failure-expert, data-failure-expert
- edge-case-hunter, coverage-expert, depth-expert, gap-identifier, assumption-challenger

### Reality:

- **No `agents/` directory exists** at the repo root
- `.agents/` exists but contains knowledge artifacts (plans, retros, pre-mortems), not agent definitions
- The 20 agent names are referenced in docs and some SKILL.md files as conceptual subagents, but there are no dedicated agent definition files
- Agent behaviors are defined inline within SKILL.md files (e.g., council, vibe, post-mortem spawn subagents as part of their instructions)

---

## 5. Test Path References

The test infrastructure has been partially updated:

| Test File | Path Style | Notes |
|---|---|---|
| `tests/run-all.sh` | `skills/*/` | Correct. Comment says "Updated for unified structure" |
| `tests/smoke-test.sh` | `skills/*/` | Correct |
| `tests/marketplace-e2e-test.sh` | `skills/*/` | Correct |
| `tests/skills/validate-skill.sh` | Takes path argument | Flexible |
| **CLAUDE.md examples** | `plugins/vibe-kit/skills/vibe` | **WRONG** — should be `skills/vibe` |

The tests themselves work with the actual structure. Only the documentation examples are wrong.

---

## 6. Shared Scripts: Copy, Not Symlink

CLAUDE.md claims:

> "Symlinks for shared code — Avoid duplication across plugins"
> "Symlink from plugin: `ln -s ../../../../../shared/scripts/script.sh script.sh`"

Reality:
- `lib/scripts/prescan.sh` exists (12,021 bytes)
- `skills/vibe/scripts/prescan.sh` exists (4,213 bytes) — a **separate copy**, not a symlink
- These are different sizes, so they're not even the same content
- No symlinks are used anywhere in the repo for shared scripts

---

## 7. Document-by-Document Consistency Matrix

| Document | Structure Model | Correct? |
|---|---|---|
| **CLAUDE.md** | `plugins/<kit>/skills/` marketplace | **WRONG** |
| **CONTRIBUTING.md** | `plugins/<name>/` marketplace | **WRONG** |
| **README.md** | `skills/` monolithic | Correct |
| **ARCHITECTURE.md** | `skills/` monolithic | Correct (but agent count issue) |
| **PLUGINS.md** | `skills/` references | Correct |
| **SKILL-TIERS.md** | `skills/` references | Correct (most accurate) |
| **CHANGELOG.md** | Mixed references | Historical, acceptable |
| **tests/run-all.sh** | `skills/` | Correct |
| **smoke-test.sh** | `skills/` | Correct |

**Two files are fundamentally wrong: CLAUDE.md and CONTRIBUTING.md.** These are arguably the two most important files for anyone (human or AI) trying to understand or contribute to the project.

---

## 8. Minor Discrepancies

### 8a. `docs/PLUGINS.md` filename is misleading
The file's actual heading is "# Skills Reference" — it documents skills, not plugins. The filename `PLUGINS.md` is a leftover from the old architecture.

### 8b. marketplace.json describes a marketplace with one entry
```json
"plugins": [{ "name": "agentops", "source": "./" }]
```
The marketplace infrastructure exists but contains only the monolithic plugin. The multi-kit marketplace vision was never realized.

### 8c. ARCHITECTURE.md lists 14 skills in tree, claims 21
The directory tree in ARCHITECTURE.md only shows 14 skill directories but says "All 21 skills." Seven skills are silently omitted from the tree view.

### 8d. `judge` skill is deprecated but still exists
SKILL-TIERS.md marks `judge` as deprecated (replaced by `/council`), but the skill directory still exists at `skills/judge/`.

---

## 9. Recommendations

### Critical (should fix immediately):

1. **Rewrite CLAUDE.md** to reflect the actual `skills/` structure. This is the file Claude Code reads first — it's giving AI agents completely wrong context.

2. **Rewrite CONTRIBUTING.md** plugin structure section to show the actual contribution path (`skills/<name>/SKILL.md`).

3. **Fix CLAUDE.md test examples:**
   - `./tests/skills/validate-skill.sh plugins/vibe-kit/skills/vibe` → `./tests/skills/validate-skill.sh skills/vibe`
   - `cp -r templates/skill-template plugins/your-kit/skills/new-skill` → remove or update
   - `claude --plugin ./plugins/your-kit` → `claude --plugin ./`

### Important:

4. **Update ARCHITECTURE.md** to show all 32 skills in the tree (or explicitly note which are omitted and why).

5. **Rename `docs/PLUGINS.md`** to `docs/SKILLS.md` or update its filename to match its content.

6. **Reconcile agent definitions** — either create the `agents/` directory with the 20 agent definitions, or update ARCHITECTURE.md to explain that agents are defined inline.

7. **Update marketplace.json** description from "21 skills" to "32 skills (21 user-facing, 11 internal)".

### Nice to have:

8. Remove the deprecated `skills/judge/` directory or add a clear deprecation notice in its SKILL.md.

9. Either implement the symlink pattern for `prescan.sh` or remove the symlink documentation from CLAUDE.md.

10. Clean up the discrepancy where `beads` appears in both user-facing and internal skill lists.

---

## Summary Table

| Category | Gaps Found | Severity |
|---|---|---|
| Directory structure (CLAUDE.md) | Entire `plugins/`, `shared/`, `templates/` don't exist | **Critical** |
| Directory structure (CONTRIBUTING.md) | Plugin creation instructions reference phantom paths | **Critical** |
| Skill counts | 21 vs 32 depending on document | Medium |
| Agent definitions | 20 agents documented, 0 agent files exist | Medium |
| Test examples in docs | Reference wrong paths | High |
| Shared script approach | Symlinks documented, copies used | Low |
| File naming | PLUGINS.md documents skills | Low |
