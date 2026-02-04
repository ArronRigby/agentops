# Pre-Mortem: AO Skills Validation Framework

**Date:** 2026-02-03
**Spec:** `.agents/plans/2026-02-03-ao-skills-validation.md`

---

## Checklist Verification

| Category | Item | Present? | Location | Complete? |
|----------|------|----------|----------|-----------|
| Interface | Test acceptance criteria | yes | lines 18-23 | partial |
| Timing | Timeouts for tests | no | - | no |
| Error | Error handling for failures | partial | line 30 | partial |
| Safety | Rollback if tests break CI | no | - | no |
| Integration | Dependencies stated | yes | lines 284-305 | yes |
| State | Issue lifecycle transitions | partial | lines 286-305 | partial |
| Tooling | Prerequisites listed | no | - | no |

---

## Findings

### CRITICAL (Must Fix Before Implementation)

#### 1. Test acceptance criteria vague
- **Location:** lines 18-23 (Issue 1)
- **Why Critical:** "Tests verify parallel task execution" doesn't specify HOW to verify or what constitutes passing
- **Specific Fix:** Add to Issue 1: "Test verifies: 3 independent tasks spawn within 5s; TaskCreate returns task IDs; all tasks reach completed state"

#### 2. Gate commands state machine undefined
- **Location:** lines 90-107 (Issue 5)
- **Why Critical:** Plan says "Connect to chain.jsonl state machine" but no state diagram exists. Risk of implementing wrong transitions.
- **Specific Fix:** Add state diagram: `pending → [human reviews] → approved/rejected → [24h elapsed] → promoted`

#### 3. Knowledge decay specification incomplete
- **Location:** lines 131-147 (Issue 7)
- **Why Critical:** Code has TWO decay rates (knowledge=0.17, confidence=0.1) but plan only mentions one. Also, `--apply-decay` flag EXISTS in code (inject.go:112) but plan claims it's not implemented.
- **Specific Fix:** Clarify: "Freshness decay uses 0.17/week. Confidence decay uses 0.1/week. Flag is DEFINED but may not be WIRED to ranking logic - verify before implementing."

#### 4. Pool/gate implementation status contradicts code
- **Location:** lines 165-167
- **Why Critical:** Plan claims "5 TODO stubs" but code review found functional implementations in pool.go:51-88. Effort estimate may be 30% too high.
- **Specific Fix:** Re-audit gate.go and pool.go. Update plan with actual implementation status before starting work.

### HIGH (Should Clarify)

#### 1. No rollback procedure
- **Location:** Not found
- **Assumption Made:** If tests break CI, can simply revert commits
- **Specific Clarification:** Add to plan: "If tests break CI, revert to last green commit. Do not merge test PRs without CI passing."

#### 2. Toolchain-validate.sh location unverified
- **Location:** lines 161-162 (Issue 8)
- **Assumption Made:** Script exists at `./scripts/toolchain-validate.sh`
- **Specific Clarification:** Verify script exists. Document exit code semantics (0=pass, 2=critical, 3=high).

#### 3. E2E test assumption about programmatic skill invocation
- **Location:** lines 208-224 (Issue 11)
- **Assumption Made:** Skills can be invoked programmatically in tests
- **Specific Clarification:** Verify if /plan and /vibe can be called from shell scripts or require Claude session.

#### 4. Validation methodology audit may be stale
- **Location:** lines 159-162
- **Assumption Made:** 2026-01-31 audit still applies 3 days later
- **Specific Clarification:** Check if pre/post-mortem skills have been updated since audit. If tool integration added, audit conclusions invalid.

### MEDIUM

- **No timeout for bd CLI calls** (gate.go:186): Add 5s context timeout
- **No test file listing prerequisites** (all issues): Add "Requires: bash, test-helpers.sh"
- **BulkApprove zero duration edge case** (pool.go:506): Validate threshold >= 1h
- **Concurrent message writes race condition** (inbox.go:286-298): Add file locking

---

## Implicit Assumptions Found

| Location | Assumption | Risk | Clarification Needed |
|----------|------------|------|---------------------|
| line 27 | TaskCreate with run_in_background spawns parallel | HIGH | What if sequential? |
| line 106 | chain.jsonl format is undocumented | MEDIUM | Actually documented in code (chain.go:67-111) |
| line 143 | 0.17 constant comes from Darr et al. | MEDIUM | Verify citation |
| line 161 | toolchain-validate.sh exists | HIGH | Verify path |
| line 213 | Skills can be invoked from shell | HIGH | May require Claude session |

---

## Edge Cases Without Handling

| Location | Input | Boundary Missing | Suggested Handling |
|----------|-------|-----------------|-------------------|
| Issue 1 | 0 tasks ready | Empty wave handling | Return "No tasks ready for wave 1" |
| Issue 1 | All tasks blocked | Wave 1 empty | Error: "Cannot start - all tasks have blockers" |
| Issue 2 | 1000+ messages | Pagination | Add --limit flag, default 100 |
| Issue 5 | Gate already approved | Duplicate review | Error: "Already reviewed by X" |
| Issue 7 | Age = 0 weeks | Decay = 1.0 | Document: "Brand new = full score" |
| Issue 7 | Age = 52 weeks | Decay = 0.0001 | Add floor: min decay = 0.1 |
| Issue 14 | Empty message body | Parser handling | Return empty string, log warning |

---

## Verification Agents Summary

### Gap Identifier
- **10 gaps found:** 4 critical, 6 important
- **Key finding:** Pool commands may already be implemented (contradicts plan)

### Assumption Challenger
- **12 assumptions found:** 6 high-risk, 6 medium-risk
- **Key finding:** `--apply-decay` flag EXISTS but plan claims not implemented

### Edge Case Hunter
- **15 edge cases found:** 3 high risk, 6 medium risk
- **Key finding:** bd CLI timeout could block entire gate workflow

---

## Verdict

**[ ] READY** - 0 CRITICAL gaps, <=2 HIGH gaps

**[X] NEEDS WORK** - 4 CRITICAL gaps must be addressed:
1. Vague acceptance criteria (clarify test assertions)
2. Gate state machine undefined (add diagram)
3. Decay specification incomplete (clarify two rates)
4. Pool/gate status contradicts code (re-audit)

---

## Recommended Actions Before Implementation

1. **Re-audit pool.go and gate.go** - Verify TODO stub claim vs actual implementation
2. **Verify toolchain-validate.sh exists** - Check path and document interface
3. **Add state diagram for gate transitions** - Document bronze → silver → gold flow
4. **Clarify decay rates** - Distinguish knowledge freshness (0.17) from confidence decay (0.1)
5. **Add timeout to bd CLI calls** - Prevent workflow blocking
6. **Check if audit is stale** - Verify pre/post-mortem still theater

---

## Effort Adjustment

Based on assumption challenges:
- If pool/gate already implemented: **-3 days** from estimate
- If decay flag already wired: **-1 day** from estimate
- If audit stale and tools integrated: **-2 days** from estimate

**Revised estimate:** 10-15 days (down from 15-20) pending verification
