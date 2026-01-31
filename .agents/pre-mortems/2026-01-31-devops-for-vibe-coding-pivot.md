# Pre-Mortem: DevOps for Vibe-Coding Strategic Pivot

**Date:** 2026-01-31
**Spec:** `.agents/plans/2026-01-31-devops-for-vibe-coding-pivot.md`
**Epic:** ag-xrd

## Summary

Strategic pivot from "12-Factor AgentOps: Operational principles for reliable AI agents" to "DevOps for Vibe-Coding: Shift-left validation for coding agents."

**Scope:** 12 tasks across 4 waves, touching 3 repos (12factor, agentops, personal_site), plugin marketplace, and 170KB+ of documentation.

**Simulation Method:** Parallel failure expert swarm (edge-case-hunter, integration-failure, ops-failure, data-failure)

---

## Simulation Findings

### CRITICAL (Must Fix Before Proceeding)

#### 1. Inbound Links & SEO Authority Destruction
**Why it will fail:** External links to "12-factor-agentops" from blog posts, Stack Overflow, academic papers, and the Vibe Coding book will break or point to mismatched content. Google search ranking for "12 factor agentops reliable agents" will plummet.

**Impact:** 6-12 months of SEO equity destroyed. Users land expecting general agent guidance, find coding-only focus.

**Recommended fix:**
- Add `MIGRATION.md` explaining old scope → new scope
- Keep repo name `12-factor-agentops` (DON'T rename)
- Add prominent notice: "Previously: Operational principles for *any* AI agent. Now: Specific patterns for coding agents."
- Create backward-compatible section for existing users

#### 2. Plugin Marketplace Cache Blindness
**Why it will fail:** Claude Code plugin marketplace caches metadata for 24-48+ hours. Users installing during transition see old description ("AI-assisted development") but get new behavior (coding-only scope).

**Impact:** User confusion, negative reviews, trust erosion.

**Recommended fix:**
- Coordinate with Anthropic on cache TTL before launch
- Delay marketing announcement by 48h after plugin.json update
- Test plugin propagation in staging environment first

#### 3. Cross-Repo Inconsistency Cascade
**Why it will fail:** 3 repos (12factor, agentops, personal_site) updated independently over days. During transition, user reads new tagline in agentops, old tagline in 12factor, no mention in personal_site.

**Impact:** Contradictory messaging destroys credibility. Users file confused issues.

**Recommended fix:**
- Atomic multi-repo rebrand: ALL repos updated within 2-hour window
- Create master checklist in `REBRAND-COORDINATION.md`
- Add CI check: grep for old taglines across all repos
- Staged rollout: 12factor first (source of truth), then agentops, then personal_site

#### 4. Archive Operation Underspecified - Data Loss Risk
**Why it will fail:** Plan says "archive general agent content" but doesn't specify:
- Which files exactly?
- Archive to directory, branch, or delete?
- What about `.agents/learnings/` that reference archived docs?

**Impact:** Silent knowledge loss. Flywheel decay spikes. Orphaned beads issues.

**Recommended fix:**
- Create explicit list of files to archive before executing
- Archive to `docs/_archived/` directory (NOT delete)
- Audit all `.agents/learnings/` for references to archived docs
- Create `git tag archive/v1.x-operational-principles` before rebrand

---

### HIGH (Should Fix)

#### 5. GitHub Social Proof Reset (Irreversible)
**Risk:** If repo is renamed, stars/forks don't transfer. Starting from 0 destroys credibility.

**Mitigation:** DON'T rename repo. Keep `12-factor-agentops`, change only description and content.

#### 6. Version Tag Orphaning
**Risk:** v2.0.0 was released Dec 2025 with old branding. Users cloning v2.0.0 get confused messaging.

**Mitigation:** Add CHANGELOG entry: "v2.0.0 marks pivot to vibe-coding focus." Create migration guide.

#### 7. Beads Issues Reference Old Terminology
**Risk:** 50-150 beads issues contain "12-factor", "operational principles" references. Links rot after archive.

**Mitigation:** Audit beads before rebrand: `bd list --json | jq '.[] | select(.title | contains("12-factor"))'`

#### 8. Agent Prompts Misaligned with New Scope
**Risk:** 20 agent prompts describe validation for "any AI agent." Post-rebrand, docs say "coding only" but agents validate broader scope.

**Mitigation:** Review all `agents/*.md` files. Update or mark as `[LEGACY]`.

#### 9. Stale Website Cache
**Risk:** 60-80% of returning users see old messaging for 24h due to CDN/browser cache.

**Mitigation:** Add cache-busting headers. Purge CDN on deploy. Warn users in announcement.

#### 10. Hardcoded External Links
**Risk:** 50+ hardcoded references to `https://github.com/boshu2/12-factor-agentops` and `12factoragentops.com` across repos.

**Mitigation:** Audit all repos: `grep -r "12-factor-agentops" . --include="*.md"`

---

### MEDIUM (Consider)

- **CLI help text** still says old tagline (Homebrew formula, `ao --help`)
- **GitHub repo description** (separate from README) may not update automatically
- **Issue templates** reference old scope - users file wrong issues
- **CHANGELOG historical entries** show old branding - mild confusion
- **LinkedIn/Twitter posts** with old messaging still circulating
- **Vibe Coding book** may reference old scope (coordinate with Gene Kim/Steve Yegge)
- **Knowledge flywheel poisoning** - old learnings reference deprecated docs
- **Markdown internal link rot** - renamed files break cross-references
- **Session hook context injection** - `using-agentops` skill auto-injected with old scope

---

## Ambiguities Found

1. **What exactly is "general agent content"?**
   - No explicit list of files to archive
   - Decision needed: Platform ops? DevOps? Infrastructure-as-code?

2. **What about ops-failure-expert, data-failure-expert agents?**
   - These are pre-mortem agents that aren't coding-specific
   - Delete? Relabel? Keep as-is?

3. **Does "coding agent" include web development, testing, architecture?**
   - Case studies describe "Web Development", "Platform Engineering"
   - New tagline implies ONLY code validation
   - Clarify scope definition before messaging

4. **What's the fallback for existing users who need general agents?**
   - No alternative framework offered
   - Consider: Link to HumanLayer 12-Factor Agents for general use?

5. **Will 12factoragentops.com domain change?**
   - Plan doesn't specify DNS changes
   - If domain stays, ensure redirects work

---

## Spec Enhancement Recommendations

1. **Add:** `REBRAND-COORDINATION.md` with atomic rollout checklist
2. **Add:** Explicit archive file list before Issue 10 executes
3. **Add:** Issue 0.5: "Define coding agent scope precisely" (before positioning doc)
4. **Clarify:** Which agent prompts are being updated vs deprecated
5. **Remove:** Any implication of repo renaming (keep `12-factor-agentops` name)
6. **Add:** Wave 0: Pre-flight audits (grep for old taglines, link validation)
7. **Add:** External coordination task: Notify Vibe Coding authors before launch

---

## Rollout Recommendations

### Pre-Launch (48h before)

1. Create `REBRAND-COORDINATION.md` source of truth
2. Audit all cross-references: `grep -r "operational principles\|12-factor-agentops" .`
3. List explicit archive targets
4. Create backup tag: `git tag archive/v1.x-pre-rebrand`
5. Test plugin.json propagation timing

### Launch Day (Atomic 2h Window)

1. 10:00 - Update 12factor README, docs, GitHub metadata
2. 10:30 - Update agentops plugin README, plugin.json
3. 11:00 - Update personal site article
4. 11:30 - Publish blog post explaining decision
5. 12:00 - Announce on social media (after 48h cache buffer)

### Post-Launch (2 weeks)

1. Monitor GitHub issues for confusion
2. Track SEO rankings for old vs new keywords
3. Audit inbound links, update where possible
4. Run `/retro` to capture learnings

---

## Verdict

**[ ] READY** - Proceed to implementation
**[X] NEEDS WORK** - Address critical/high issues first

### Required Before /crank:

1. **Create REBRAND-COORDINATION.md** with:
   - Old → new terminology mapping
   - Complete file list for all 3 repos
   - Atomic rollout sequence
   - Rollback plan

2. **Define scope explicitly:**
   - What IS a "coding agent"?
   - What IS NOT (and where do those users go)?

3. **Create archive plan:**
   - Explicit file list
   - Archive location (directory, not delete)
   - Backlink audit for learnings/beads

4. **Decide on repo name:**
   - Recommendation: KEEP `12-factor-agentops` (don't rename)
   - Change content, not infrastructure

---

## Gate 3 Decision Required

**Findings Summary:**
- 4 CRITICAL issues (must fix)
- 6 HIGH issues (should fix)
- 9 MEDIUM issues (consider)
- 5 ambiguities requiring clarification

**Recommendation:** Create coordination document addressing CRITICAL issues before proceeding to /crank.

---

*Pre-mortem complete. Awaiting human approval at Gate 3.*
