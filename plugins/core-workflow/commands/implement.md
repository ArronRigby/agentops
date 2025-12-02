# /implement - Implementation Phase (Inner Loop)

**Purpose:** Execute approved plan with continuous validation.

**Why this matters:** Implementation is where plans meet reality. By following the plan mechanically and validating after each change, we catch deviations early. The inner loop is tight - make change, verify, commit. This prevents cascading errors and ensures each step is solid before proceeding.

---

## Opus 4.5 Behavioral Standards

<default_to_action>
Execute the plan. Do not re-research or re-plan unless blocked. If the plan says "modify auth.ts:45", open that file and make the change.
</default_to_action>

<avoid_overengineering>
Implement exactly what the plan specifies. Do not add error handling for impossible scenarios, create abstractions for one-time operations, or "improve" surrounding code. The plan defines scope.
</avoid_overengineering>

<validate_before_proceeding>
After each task, run the specified acceptance check. Do not proceed to task N+1 until task N passes validation. If validation fails, fix before continuing.
</validate_before_proceeding>

<communication_style>
After completing each task, briefly summarize what changed and the validation result. Keep updates concise - focus on outcomes, not narration.
</communication_style>

---

## Usage

```bash
# Load plan and implement
/implement [plan-name]
```

**Agent will:**
1. Load implementation plan
2. Execute tasks sequentially per plan
3. Validate after each change using plan's acceptance criteria
4. Track progress and metrics
5. Document any deviations with rationale
6. Commit after each validated task

**Output:** Working solution + implementation report

---

## Implementation Loop

```
For each task in plan:
  1. Read target file(s)
  2. Make specified change
  3. Run acceptance check
  4. If pass → commit and proceed
  5. If fail → fix and re-validate (max 3 attempts)
  6. If stuck → flag for human review
```

---

## Example

```
You: /implement refresh-token-plan-2025-11-30

Agent: Loading plan... 5 tasks identified.

**Task 1/5: Add refresh token model**
- Created src/models/token.ts (48 lines)
- Acceptance: TypeScript compiles ✓
- Committed: "feat(auth): add refresh token model"

**Task 2/5: Update auth middleware**
- Modified src/middleware/auth.ts:45-89
- Added rotation logic, token validation
- Acceptance: Existing tests pass ✓
- Committed: "feat(auth): add token rotation to middleware"

**Task 3/5: Add refresh endpoint**
- Added POST /auth/refresh to src/routes/auth.ts
- Acceptance: curl test returns new tokens ✓
- Committed: "feat(auth): add refresh token endpoint"

**Task 4/5: Update Redis schema**
- Modified src/services/session.ts:112-145
- Added token fields, TTL handling
- Acceptance: Redis integration test passes ✓
- Committed: "feat(auth): extend Redis schema for tokens"

**Task 5/5: Add tests**
- Created 6 tests in tests/auth.test.ts
- Covers: rotation, expiry, blacklist, concurrent refresh
- Acceptance: All tests pass ✓
- Committed: "test(auth): add refresh token test coverage"

**Implementation complete.**
- Tasks: 5/5 ✓
- Deviations: 0
- Total commits: 5
- Ready for /learn
```

---

## Deviation Handling

When reality doesn't match the plan:

| Situation | Action |
|-----------|--------|
| Minor adjustment needed | Make change, document in commit |
| Task blocked by unforeseen issue | Stop, flag for review |
| Plan assumption was wrong | Document finding, return to /plan |
| Better approach discovered | Complete current task, note for /learn |

Do not silently deviate. Explicit deviation documentation enables learning.

---

## Debug Spiral Detection

Watch for these patterns during implementation:

| Signal | Threshold | Action |
|--------|-----------|--------|
| Fix commits | >3 in a row | Pause, add tracer test |
| Same file edited | >4 times | Review approach |
| Test failures | >5 consecutive | Step back, re-read plan |
| Time on single task | >30 minutes | Flag for review |

If spiral detected: Stop implementing. Document what's failing. Ask for human guidance.

---

## Commit Standards

Each task gets one commit:

```
<type>(<scope>): <description>

[Brief rationale if deviation from plan]

Acceptance: [what was verified]
Task: [N]/[total]
```

Types: `feat`, `fix`, `refactor`, `test`, `docs`

---

## Completion Criteria

Implementation is complete when:
- All plan tasks executed
- All acceptance criteria verified
- Deviations documented
- Clean commit history

---

**Demonstrates:** Factor IV (Validation Gates), Factor V (Operational Telemetry), Factor XI (Constitutional Guardrails)
