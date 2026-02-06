# Council Brainstorm: Ways to Improve the AgentOps Plugin

**Date:** 2026-02-05
**Target:** AgentOps Claude Code plugin (v1.4.0) improvement ideas
**Judges:** 2 Claude (Opus 4.6) — Pragmatist + Skeptic

---

## Options Explored

| Idea | Pragmatist | Skeptic | Effort | Impact |
|------|-----------|---------|--------|--------|
| **Interactive onboarding (/quickstart)** | Top 3 — unlocks adoption | Top 1 — low effort, highest ROI | Low-Med | HIGH |
| **Consolidate skills (28 → 10-12)** | Top 1 — cheapest clarity win | Top concern — "28 skills is a liability" | Low | HIGH |
| **Graceful CLI degradation (ao/bd/codex)** | Top 3 — doubles addressable users | Top 3 — removes biggest adoption barrier | Med-High | HIGH |
| **Auto-spin the knowledge flywheel** | Priority — make it invisible | "5 manual steps is a conveyor belt, not a flywheel" | Medium | HIGH |
| **Council --quick mode (single-agent)** | Make validation a 10s habit | Council is becoming a kitchen sink | Low | Medium |
| **/status dashboard** | Users get lost between skills | N/A (not raised) | Low | Medium |
| **Fix npx distribution** | N/A | "If your update has a documented workaround, it's broken" | Medium | Medium |
| **Git-based JSONL merge conflicts** | N/A | Will break in teams — one-file-per-entity instead | High | Medium |
| **Prove value with /stats** | N/A | "Show the receipts" — no evidence the overhead pays off | Medium | Medium |
| **Standardize output format** | JSON envelope + markdown rendering | N/A | Low | Low |

---

## Shared Findings (Both Judges Agree)

1. **The #1 problem is adoption, not capability.** The plugin has powerful features buried under complexity. 28 skills + 3+ CLIs + a methodology creates a wall that stops most users before they experience value.

2. **Consolidate the skill surface area.** Library skills (standards, shared, beads) and background skills should be internal-only. Related skills should merge under parent commands. Target 10-12 user-facing skills max.

3. **External CLI dependencies must degrade gracefully.** If ao/bd/codex aren't installed, features should fall back to local alternatives (plain files, markdown, Claude-only), not show errors.

4. **The knowledge flywheel needs to be automatic.** A 5-step manual pipeline (extract → forge → knowledge → inject → flywheel) is not a flywheel. Auto-extract on session end, auto-inject on session start. Users should notice their agent getting smarter, not remember to run commands.

5. **An interactive onboarding experience is the highest-ROI investment.** No documentation replaces learning by doing. A /quickstart that walks through one real RPI cycle on the user's actual codebase would teach more in 10 minutes than any README.

## Disagreements

| Topic | Pragmatist | Skeptic |
|-------|-----------|---------|
| **Council expansion** | Keep it but add --quick for single-agent lightweight mode | Council has second-system effect — research/analyze are scope creep, lock to 3 task types |
| **Wrapper skills (vibe/pre-mortem/post-mortem)** | Consolidate under /validate parent command | Should be council presets, not separate skills at all |
| **Priority order** | Consolidate skills first (cheapest), then onboarding, then CLI degradation | Onboarding first (highest ROI), then auto-flywheel, then CLI degradation |

---

## Recommendation

**Top 5 improvements ranked by consensus ROI:**

1. **Consolidate to 10-12 user-facing skills** — Low effort, immediate clarity. Merge ao-related skills (6→1), validation skills (4→1), hide library/background internals. No functionality lost.

2. **Build /quickstart onboarding** — Medium effort, unlocks adoption. Guided RPI cycle on real code. 10 minutes to first value. Add "suggested next skill" hints after each skill completes.

3. **Auto-spin the knowledge flywheel** — Medium effort, delivers the core promise. Post-session hooks for extract+forge. Auto-inject on session start. Make it invisible.

4. **Graceful CLI degradation** — Medium-high effort, doubles user base. Every skill works with zero external deps. Progressive enhancement as CLIs are added.

5. **Add council --quick mode** — Low effort, makes validation a habit. Single structured self-review in <10s for routine checks. Reserve multi-agent for --deep/--mixed.

---

*Council completed. 2/2 judges responded.*
