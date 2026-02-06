# Council Consensus: WARN

**Target:** Plan for ag-iyl — Plugin Adoption Improvements (7 issues, 3 waves)
**Mode:** validate
**Judges:** 2 Claude (Opus 4.6) — Pragmatist + Skeptic

---

### Verdicts

| Judge | Verdict | Key Finding |
|-------|---------|-------------|
| Pragmatist | WARN | Issue 1 `invocable: false` has no implementation path — skills CLI ignores unknown frontmatter |
| Skeptic | WARN | Same critical concern + Issue 3 under-scoped + Issue 5 automation aspirational |

---

### Shared Findings (Both Judges Agree)

1. **CRITICAL: Issue 1 is unimplementable as written.** The plan adds `invocable: false` to frontmatter, but the skills CLI loads skills by directory presence, not frontmatter fields. This field will have zero effect. Issues 4, 6, 7 all depend on Issue 1.

2. **Issue 3 is underestimated.** "Audit all skills and add fallbacks" is High effort, not Medium. Each CLI×skill combination needs its own degradation design.

3. **Issue 5's "auto-extract on session end" has no triggering mechanism.** Claude Code has no reliable session-end hook. The plan needs a pragmatic alternative.

4. **Issue 4 (/quickstart) has a missing dependency on Issue 3.** A new user running /quickstart is the MOST likely person to lack bd/ao/gt — the onboarding skill MUST work without external CLIs.

### Disagreements

| Topic | Pragmatist | Skeptic |
|-------|-----------|---------|
| Issue 2 naming | Drop the <15s target, keep under /council | Consider renaming to /check or /lint — "single-agent council" is oxymoronic |

---

### Recommendations

**Before starting Wave 1 (30-minute spike):**
1. Validate whether the skills CLI can be patched to support `invocable: false`
2. If not, pivot to alternative: underscore-prefixed directories, `.skillignore`, or moving internals to a non-scanned subdirectory

**Plan amendments needed:**
1. **Issue 1:** Add concrete mechanism (not just frontmatter field)
2. **Issue 3:** Split into first-pass (detect+warn) and second-pass (actual fallbacks), or break into per-CLI sub-issues
3. **Issue 4:** Add Issue 3 as explicit dependency (quickstart must work without external CLIs)
4. **Issue 5:** Replace "auto-extract on session end" with user-triggered mechanism (/wrap, /retro auto-trigger, or prompt-based heuristic)
5. **Issue 2:** Drop the <15s time target (aspirational, not achievable for non-trivial targets)
6. **General:** Add per-wave validation step — run council --quick on changed skills after each wave

---

*Council completed. 2/2 judges responded.*
