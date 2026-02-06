# Plan: AgentOps Plugin Improvements

**Date:** 2026-02-05
**Source:** `.agents/council/2026-02-05-brainstorm-plugin-improvements.md`

## Overview

Address the top 5 consensus improvements from the council brainstorm. The core problem is adoption, not capability — 28 user-visible skills + external CLI dependencies create a wall that stops users before they experience value.

## Issues

### Epic: ag-yl0 — Plugin Adoption Improvements

---

### Issue 1: Hide library/background skills from user-facing skill list
**Wave:** 1
**Dependencies:** None
**Effort:** Low
**Acceptance:** Only 12-15 skills appear in slash-command suggestions. Library (shared, standards, beads), background (inject, extract, forge, provenance, ratchet, flywheel), meta (using-agentops), and deprecated (judge) skills are marked non-invocable.
**Description:**
Add `invocable: false` to frontmatter of skills that should be internal-only:
- Library: shared, standards, beads
- Background: inject, extract, forge, provenance, ratchet, flywheel
- Meta: using-agentops (auto-injected, not user-invoked)
- Deprecated: judge

Verify that the skills CLI / Claude Code plugin loader respects this field. If not, determine the correct mechanism to hide skills (may need marketplace manifest changes).

Update SKILL-TIERS.md to reflect the new visibility rules.

---

### Issue 2: Add council --quick flag for single-agent lightweight validation
**Wave:** 1
**Dependencies:** None
**Effort:** Low
**Acceptance:** `/council --quick validate recent` runs a single structured self-review in <15s without spawning background agents. Uses the same JSON output schema. Report written to .agents/council/.
**Description:**
Add a `--quick` flag to the council skill that:
1. Skips multi-agent spawning
2. Runs a single structured self-review inline (no Task tool)
3. Uses the same output_schema (verdict/confidence/findings/recommendation)
4. Writes report to .agents/council/ with same naming convention
5. Completes in under 15 seconds

This makes validation cheap enough to run constantly, not just before big commits.

---

### Issue 3: Add graceful CLI degradation to all skills
**Wave:** 1
**Dependencies:** None
**Effort:** Medium
**Acceptance:** Every skill that references bd/ao/gt/codex works when those CLIs are absent. Fallback behavior documented. No skill crashes or shows raw error output when a CLI is missing.
**Description:**
Audit all 28 skills for external CLI dependencies. For each:

| CLI | Fallback when missing |
|-----|----------------------|
| bd | Skip beads references, use TaskList for tracking, note "install bd for persistent tracking" |
| ao | Write knowledge to .agents/knowledge/ directly, skip flywheel metrics |
| gt | Skip workspace management, work in current directory |
| codex | Fall back to Claude-only (already handled in council, verify in swarm/crank) |

Add a shared utility pattern (in skills/shared/) for CLI availability checking:
```bash
if command -v bd &>/dev/null; then
  # full behavior
else
  echo "Note: Install bd for persistent issue tracking"
  # fallback behavior
fi
```

---

### Issue 4: Build /quickstart onboarding skill
**Wave:** 2
**Dependencies:** Issue 1 (skill count must be reduced first so quickstart shows a manageable list)
**Effort:** Medium
**Acceptance:** New user runs /quickstart and completes a guided RPI cycle on their actual codebase in under 10 minutes. Skill detects project type, suggests a real task, walks through research→plan→vibe.
**Description:**
Create a new `/quickstart` skill that:
1. Detects project (language, framework, git state, existing .agents/)
2. Shows "You have N skills available. Here are the 3 that matter most: /research, /plan, /vibe"
3. Runs a mini guided RPI cycle:
   - `/research` on a specific area of their codebase
   - Suggests running `/plan` on a real task
   - Runs `/vibe --quick` on their most recent commit
4. Explains what each step did and what value it added
5. Shows "next steps" for deeper usage

Also add "suggested next skill" hints to existing skills:
- After /research: "Consider /plan to decompose into tasks"
- After /plan: "Run /pre-mortem to validate, or /crank to execute"
- After /vibe: "PASS? Ship it. FAIL? Fix and re-run."

---

### Issue 5: Auto-spin the knowledge flywheel
**Wave:** 2
**Dependencies:** Issue 3 (CLI degradation must work first so auto-flywheel doesn't crash without ao)
**Effort:** Medium
**Acceptance:** Knowledge is automatically extracted at session end and injected at session start without manual commands. ao flywheel status shows automatic activity. Works with or without ao CLI.
**Description:**
Make the flywheel truly automatic:

1. **Auto-extract on session end:** Add a post-session hook (or make /retro and /post-mortem auto-trigger extract+forge)
2. **Auto-inject on session start:** The existing inject hook should work, but verify it fires reliably
3. **Fallback without ao:** Write learnings to `.agents/knowledge/pending/` as markdown files. When ao becomes available, import them.
4. **Single command for manual trigger:** `ao auto` or `/flywheel spin` that does extract+forge+inject in one shot

The user should notice their agent getting smarter without remembering to run 5 commands.

---

### Issue 6: Add /status dashboard skill
**Wave:** 2
**Dependencies:** Issue 1 (needs reduced skill list to show clean dashboard)
**Effort:** Low
**Acceptance:** `/status` shows a single-screen summary: current task, recent council verdicts, flywheel health, pending inbox, suggested next action.
**Description:**
Create a `/status` skill that aggregates:
1. Current bead on hook (gt hook or bd show current)
2. Recent council verdicts (ls .agents/council/ | tail -3)
3. Flywheel health (ao flywheel status or "ao not installed")
4. Pending inbox (gt mail inbox or "no messages")
5. Suggested next action based on context

All with graceful degradation — show what's available, skip what isn't.

---

### Issue 7: Update SKILL-TIERS.md and model defaults
**Wave:** 3
**Dependencies:** Issues 1-6 (reflect final state after all changes)
**Effort:** Low
**Acceptance:** SKILL-TIERS.md accurately reflects new skill visibility, tier assignments, and model defaults (gpt-5.3, opus 4.6). Dependency graph updated.
**Description:**
Update SKILL-TIERS.md with:
1. New visibility column (public/internal/deprecated)
2. Updated skill count (user-facing vs internal)
3. Updated model defaults (gpt-5.3, opus 4.6)
4. New skills (/quickstart, /status) added to tables
5. Updated dependency graph
6. Document the consolidation rationale

---

## Execution Order

**Wave 1** (parallel): Issue 1, Issue 2, Issue 3
- Hide internal skills, add --quick council, CLI degradation

**Wave 2** (after Wave 1): Issue 4, Issue 5, Issue 6
- Onboarding, auto-flywheel, dashboard

**Wave 3** (after Wave 2): Issue 7
- Documentation cleanup

## Scope Notes

**Deferred (not in this plan):**
- Full skill merging (e.g., /ao as parent command) — requires skills CLI support for subcommands, bigger lift
- Fix npx distribution — upstream dependency on skills.sh, out of scope
- Git-based JSONL merge conflicts — bd CLI concern, not plugin skill
- /stats telemetry skill — nice-to-have, defer to v1.6
- Standardize output format — low impact, defer

## Next Steps
- Run `/pre-mortem` to validate this plan
- Then `/crank` for autonomous execution
