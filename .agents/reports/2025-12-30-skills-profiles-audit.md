# Skills & Profiles Audit Report

**Date:** 2025-12-30
**Status:** SKILLS OK, PROFILES NEED UPDATE

---

## Executive Summary

| Directory | Status | Issue |
|-----------|--------|-------|
| **skills/** | ✅ OK | Well-structured, minor improvements possible |
| **profiles/** | ⚠️ STALE | References 20+ removed agents from old catalog |

---

## Skills Audit

### Structure

```
skills/
├── base/                    # 7 sub-skills (utilities)
│   ├── audit-diataxis/
│   ├── audit-onboarding/
│   ├── audit-workflow/
│   ├── cleanup-deprecated/
│   ├── cleanup-docs/
│   ├── cleanup-plans/
│   └── cleanup-repo/
├── brand-guidelines/        # Documentation styling
├── doc-curator/             # Doc quality management
├── git-workflow/            # Git best practices
├── skill-creator/           # Create new skills
├── test-gap-scanner/        # Test coverage analysis
└── testing/                 # Test patterns
```

### Validation Results

| Skill | SKILL.md | Frontmatter | Scripts/Refs |
|-------|----------|-------------|--------------|
| base/* (7) | ✅ All present | ✅ N/A (simple format) | ✅ impl.sh each |
| brand-guidelines | ✅ Present | ✅ Has description | - |
| doc-curator | ✅ Present | ✅ Has description | ✅ 3 references |
| git-workflow | ✅ Present | ✅ Has description | ✅ script + 2 refs |
| skill-creator | ✅ Present | ✅ Has description | ✅ 3 scripts + ref |
| test-gap-scanner | ✅ Present | ✅ Has description | ✅ 1 script |
| testing | ✅ Present | ✅ Has description | - |

### Skills Issues

1. **No INDEX.md** - No catalog file for skill discovery
2. **base/ has no SKILL.md** - Parent directory missing overview

### Skills Recommendations

- [ ] Create `skills/README.md` as skill catalog
- [ ] Add `skills/base/SKILL.md` overview for sub-skills

---

## Profiles Audit

### Structure

```
profiles/
├── README.md                # Main documentation (520 lines)
├── COMPARISON.md            # Comparison docs
├── META_PATTERNS.md         # Extracted patterns
├── schema/
│   └── role-profile.yaml    # Profile schema
├── shared/
│   ├── foundational.yaml    # Core system (always loaded)
│   ├── orchestration.yaml   # Workflow commands
│   └── context.yaml         # Bundle/memory systems
├── roles/
│   ├── software-dev.yaml    # Development profile
│   ├── platform-ops.yaml    # Operations profile
│   └── content-creation.yaml # Writing/research profile
└── examples/
    ├── software-dev-session.md
    ├── platform-ops-session.md
    └── content-creation-session.md
```

### Critical Issue: Stale Agent References

The profiles reference **20+ agents that no longer exist** (removed in catalog rebuild):

**In README.md:**
- `applications-create-app` ❌ REMOVED
- `services-crossplane-dev` ❌ REMOVED
- `services-edb-databases` ❌ REMOVED
- `pipelines-gitlab-ci` ❌ REMOVED
- `pipelines-troubleshooting` ❌ REMOVED
- `monitoring-slo-dashboards` ❌ REMOVED
- `deployments-progressive-delivery` ❌ REMOVED
- `argocd-debug-sync` ❌ REMOVED
- `sites-harmonize` ❌ REMOVED
- `harmonize-guide` ❌ REMOVED
- `playbooks-gitops-operations` ❌ REMOVED
- `playbooks-platform-upgrades` ❌ REMOVED

**In roles/software-dev.yaml:**
- References `work/gitops/.claude/agents/` paths ❌ WRONG REPO

**In roles/platform-ops.yaml:**
- References `work/gitops/.claude/agents/` paths ❌ WRONG REPO

**In examples/*.md:**
- All example sessions reference removed agents

### Root Cause

The profiles were designed for a **different workspace** (JREN platform at `work/gitops/`). They were copied to this agentops marketplace but never updated to reference the actual agents in `agents/`.

### Profiles Recommendations

**Option A: Update profiles to match actual agents** (Recommended)
- Rewrite YAML files to reference `agents/*.md`
- Update README.md with actual agent names
- Update examples with realistic sessions

**Option B: Remove profiles entirely**
- Delete profiles/ directory
- Simplify to agents + commands only

**Option C: Mark as "example/template"**
- Rename to `profiles-template/`
- Add disclaimer about customization needed

---

## Summary

| Component | Files | Status | Action |
|-----------|-------|--------|--------|
| skills/base/* | 7 | ✅ OK | None |
| skills/* (top-level) | 6 | ✅ OK | Add README.md |
| profiles/roles/* | 3 | ⚠️ STALE | Rewrite YAMLs |
| profiles/README.md | 1 | ⚠️ STALE | Update agent refs |
| profiles/examples/* | 3 | ⚠️ STALE | Rewrite examples |

---

## Recommended Actions

### Immediate (Low Effort)

1. Create `skills/README.md` catalog
2. Create `skills/base/SKILL.md` overview

### Required (Medium Effort)

3. Update `profiles/README.md` to reference actual agents
4. Update `profiles/roles/*.yaml` to use `agents/` paths
5. Update `profiles/examples/*.md` with valid agent names

### Optional (Higher Effort)

6. Rewrite example sessions for this marketplace context
7. Recalculate token budgets for actual agents
