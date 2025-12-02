# /workflow - Complete RPI Cycle Orchestration

**Purpose:** Orchestrate complete Research → Plan → Implement → Learn cycle.

**Why this matters:** Complex work benefits from structured phases. Research prevents building the wrong thing. Planning prevents scope creep. Implementation with validation prevents cascading bugs. Learning captures patterns for next time. The workflow enforces these gates automatically.

---

## Opus 4.5 Behavioral Standards

<phase_discipline>
Complete each phase before advancing. Do not skip research for "obvious" problems. Do not skip planning for "small" features. Do not skip learning because the work is done. Each phase serves a purpose.
</phase_discipline>

<human_gates>
Require explicit approval between phases. The workflow pauses at Research→Plan and Plan→Implement transitions for human review. This is the quality gate.
</human_gates>

<bundle_continuity>
Each phase produces a bundle. Research creates research-bundle. Plan creates plan-bundle. Implement creates implementation-report. Learn creates learnings. These artifacts enable session continuity.
</bundle_continuity>

---

## Usage

```bash
/workflow [topic]
```

**Process:**

### Phase 1: Research (Outer Loop)
1. Invokes `/research [topic]`
2. Gathers context, explores options
3. Creates research bundle
4. **→ Human Review: Approve research direction?**

### Phase 2: Plan (Middle Loop)
1. Invokes `/plan [research-bundle]`
2. Designs solution from findings
3. Creates implementation specification
4. **→ Human Review: Approve plan?**

### Phase 3: Implement (Inner Loop)
1. Invokes `/implement [plan]`
2. Executes tasks with validation
3. Commits after each validated change
4. Creates implementation report
5. **→ Auto-transition on completion**

### Phase 4: Learn
1. Invokes `/learn`
2. Extracts patterns from implementation
3. Identifies process improvements
4. Documents for institutional memory
5. **→ Workflow complete**

---

## Example

```
You: /workflow add-refresh-tokens

== Phase 1: Research ==
Exploring authentication system...
[Reads auth files, discovers JWT + Redis pattern]

Research findings:
- Current: JWT with Redis blacklist
- Gap: No refresh tokens
- Options: Rotation vs sliding expiry

Research bundle saved: refresh-token-research-2025-11-30.md

Approve research direction? (yes/no/more)

You: yes

== Phase 2: Plan ==
Designing from research findings...
[Evaluates options, designs rotation approach]

Plan summary:
- 5 tasks, estimated 2 hours
- Builds on existing Redis infrastructure
- Full test coverage included

Plan saved: refresh-token-plan-2025-11-30.md

Approve plan? (yes/no/modify)

You: yes

== Phase 3: Implement ==
Executing plan...

Task 1/5: Add token model ✓
Task 2/5: Update middleware ✓
Task 3/5: Add endpoint ✓
Task 4/5: Update Redis schema ✓
Task 5/5: Add tests ✓

Implementation complete. 5 commits, 0 deviations.

== Phase 4: Learn ==
Extracting patterns...

Patterns captured:
- Redis schema extension pattern
- Token rotation implementation pattern

Improvements identified:
- Could use generic rotation for other tokens (API keys)

Learnings saved: refresh-token-learnings-2025-11-30.md

Workflow complete! ✓
```

---

## Phase Timing Guide

| Phase | Typical Time | Signal to Advance |
|-------|--------------|-------------------|
| Research | 15-60 min | Options understood, constraints identified |
| Plan | 30-90 min | Tasks specified, acceptance criteria defined |
| Implement | 1-4 hours | All tasks validated, committed |
| Learn | 15-30 min | Patterns documented |

**Total:** 2-6 hours for medium complexity features.

---

## When to Use /workflow vs Individual Commands

| Situation | Use |
|-----------|-----|
| New feature, unclear scope | `/workflow` |
| Research already done | `/plan` directly |
| Plan already approved | `/implement` directly |
| Quick fix, known solution | Skip workflow, just fix |
| Learning from past work | `/learn` directly |

---

## Abort and Resume

The workflow can be stopped at any phase gate. To resume:

```bash
# Resume from research
/plan [existing-research-bundle]

# Resume from plan
/implement [existing-plan-bundle]

# Resume mid-implementation
/implement [plan-bundle]  # auto-detects progress
```

---

## Vibe Level Integration

| Vibe Level | Workflow Recommendation |
|------------|------------------------|
| 5 (Format) | Skip workflow |
| 4 (Boilerplate) | Skip research, minimal plan |
| 3 (CRUD) | Light research, standard plan |
| 2 (Features) | Full workflow |
| 1 (Architecture) | Full workflow + extended research |
| 0 (Novel) | Extended research, may not reach implement |

---

**Demonstrates:** All 12 Factors working together through complete lifecycle
