# Continuation Prompt for New Session

Copy/paste this to start the next session:

---

## Context

We completed ag-zh0 (council expansion to 5 task types + explorers + presets) and then ran a full brainstorm→plan→pre-mortem cycle for ag-iyl (Plugin Adoption Improvements — 7 issues, 3 waves). Council pre-mortem returned WARN: ag-iyl.1 needs a feasibility spike before Wave 1 can start because `invocable: false` frontmatter isn't supported by the skills CLI.

## Read First

1. `.agents/handoff/2026-02-05-plugin-adoption.md` — full session handoff
2. `.agents/plans/2026-02-05-plugin-improvement-plan.md` — the plan
3. `.agents/council/2026-02-05-validate-plugin-improvement-plan.md` — council findings

## What I Need Help With

1. **Spike ag-iyl.1:** Investigate the skills CLI loading mechanism. Check how `npx skills` and Claude Code discover skills in a plugin. Determine the right mechanism to hide internal skills (frontmatter field, naming convention, subdirectory, or .skillignore). 30-minute timebox.
2. **Amend ag-iyl.1** based on spike findings.
3. **Execute ag-iyl** via `/crank ag-iyl` — autonomous execution of all 7 issues across 3 waves.

## Key Files

```
.agents/plans/2026-02-05-plugin-improvement-plan.md
.agents/council/2026-02-05-validate-plugin-improvement-plan.md
skills/council/SKILL.md
skills/SKILL-TIERS.md
.claude-plugin/plugin.json
```

## Open Questions

1. How does the skills CLI discover skills? Directory scan? Manifest? Frontmatter?
2. Can we hide skills without upstream CLI changes?
3. Should council --quick be renamed to /check?

---

Start with: spike ag-iyl.1 (validate skill-hiding mechanism), then `/crank ag-iyl`
