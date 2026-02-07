# Conflict Resolution Algorithm for Multi-Agent Findings

**Date:** 2026-01-26
**Status:** TEMPERED
**Task:** #3 - Design conflict resolution algorithm

## Overview

When 6-12 agents analyze the same code in parallel, they produce findings that may conflict. This spec defines how to merge, deduplicate, and synthesize findings into a unified report with a single grade.

## Core Principles

1. **Severity Escalation** - Single veto: if ANY agent reports CRITICAL, output is CRITICAL
2. **Quorum Required** - 80% of agents must return for valid synthesis
3. **Deduplicate by Location** - Same file:line from multiple agents = one finding
4. **Provenance Tracked** - Record which agents contributed to each finding

---

## Algorithm

### Step 1: Collect Results

Wait for agents with per-agent timeout:

```
PER_AGENT_TIMEOUT = 180000  # 3 minutes in ms
QUORUM_PERCENT = 0.8

results = []
for agent in dispatched_agents:
    result = await agent with timeout PER_AGENT_TIMEOUT
    if result:
        results.append(result)
    else:
        log("TIMEOUT: {agent.name}")

if len(results) < len(dispatched_agents) * QUORUM_PERCENT:
    return {status: "INCOMPLETE", reason: "Insufficient agents returned"}
```

### Step 2: Severity Escalation

```
final_severity = "NONE"

for result in results:
    for finding in result.findings:
        if finding.severity == "CRITICAL":
            final_severity = "CRITICAL"
            break  # Can't get worse
        elif finding.severity == "HIGH" and final_severity != "CRITICAL":
            final_severity = "HIGH"
        elif finding.severity == "MEDIUM" and final_severity in ["NONE", "LOW"]:
            final_severity = "MEDIUM"
        elif finding.severity == "LOW" and final_severity == "NONE":
            final_severity = "LOW"
```

**Rule:** If ANY agent finds CRITICAL → final is CRITICAL (single veto)

### Step 3: Deduplicate Findings

```
def same_finding(f1, f2):
    return (
        f1.file_path == f2.file_path and
        abs(f1.line_number - f2.line_number) <= 5 and
        f1.category == f2.category  # security, quality, arch, etc.
    )

deduplicated = []
for result in results:
    for finding in result.findings:
        existing = find_match(deduplicated, finding, same_finding)
        if existing:
            existing.agents_found.append(result.agent_name)
            existing.agreement = f"{len(existing.agents_found)}/{len(results)}"
        else:
            finding.agents_found = [result.agent_name]
            finding.agreement = f"1/{len(results)}"
            deduplicated.append(finding)
```

### Step 4: Compute Grade

```
WEIGHTS = {
    "CRITICAL": 10,
    "HIGH": 5,
    "MEDIUM": 2,
    "LOW": 1
}

total_weight = sum(WEIGHTS[f.severity] for f in deduplicated)

# Grade thresholds (lower is better)
if any(f.severity == "CRITICAL" for f in deduplicated):
    grade = "D" if total_weight < 20 else "F"
elif total_weight == 0:
    grade = "A"
elif total_weight <= 5:
    grade = "A"
elif total_weight <= 15:
    grade = "B"
elif total_weight <= 30:
    grade = "C"
else:
    grade = "D"
```

### Step 5: Build Synthesis Report

```
report = {
    "grade": grade,
    "final_severity": final_severity,
    "agents_returned": len(results),
    "agents_dispatched": len(dispatched_agents),
    "quorum_met": len(results) >= len(dispatched_agents) * QUORUM_PERCENT,
    "findings": {
        "CRITICAL": [f for f in deduplicated if f.severity == "CRITICAL"],
        "HIGH": [f for f in deduplicated if f.severity == "HIGH"],
        "MEDIUM": [f for f in deduplicated if f.severity == "MEDIUM"],
        "LOW": [f for f in deduplicated if f.severity == "LOW"],
    },
    "timeouts": [a.name for a in dispatched_agents if a not in results],
    "synthesis_timestamp": now(),
}
```

---

## Finding Record Schema

```yaml
finding:
  id: "uuid"
  issue: "SQL injection vulnerability in user input"
  severity: "CRITICAL"
  file_path: "src/api/users.py"
  line_number: 42
  category: "security"
  agents_found: ["security-reviewer", "code-reviewer"]
  agreement: "2/6"
  confidence: 0.85  # Average of agent confidences
  first_agent: "security-reviewer"
  fix_suggestion: "Use parameterized queries"
  session_id: "abc123"
  timestamp: "2026-01-26T10:30:00Z"
```

---

## Quorum Rules

| Agents Dispatched | Minimum Required | Percentage |
|-------------------|------------------|------------|
| 6 | 5 | 83% |
| 8 | 7 | 88% |
| 10 | 8 | 80% |
| 12 | 10 | 83% |

**If quorum not met:**
- Mark report as "INCOMPLETE"
- Do NOT publish grade
- Escalate to human: "Only N/M agents returned"

---

## Timeout Handling

```
Per-agent timeout: 3 minutes (180000ms)

On timeout:
1. Cancel agent's remaining work
2. Log: "TIMEOUT: {agent_name}"
3. Continue with N-1 results if quorum still met
4. Add to report: "timeouts": ["agent_name"]
5. If quorum broken, escalate as INCOMPLETE
```

---

## Escalation Triggers

| Condition | Action |
|-----------|--------|
| All agents return "no findings" | Escalate: "Empty swarm - verify target has code" |
| CRITICAL + unanimous (6/6) | AUTO BLOCK - no human needed |
| CRITICAL + partial (3/6) | BLOCK + require human review |
| Quorum not met | INCOMPLETE - do not publish |
| Expected files not found | Escalate: "Target may be misconfigured" |

---

## Integration Points

### Vibe SKILL.md Step 9

Add after "Compute Grade":

```markdown
### Step 9a: Apply Conflict Resolution

If multiple agents dispatched:
1. Apply severity escalation (single veto rule)
2. Deduplicate findings by file:line
3. Compute weighted grade
4. Track agreement per finding

See: `.agents/specs/conflict-resolution-algorithm.md`
```

### Post-Mortem SKILL.md Step 4

Replace "Wait for all agents, then synthesize" with:

```markdown
### Step 4a: Synthesize Agent Results

Apply conflict resolution algorithm:
1. Check quorum (80% minimum)
2. Severity escalation (CRITICAL = veto)
3. Deduplicate findings
4. Compute final grade
5. Track provenance

If quorum not met, STOP and report INCOMPLETE.

See: `.agents/specs/conflict-resolution-algorithm.md`
```

---

## Test Cases

| Scenario | Input | Expected Output |
|----------|-------|-----------------|
| Unanimous CRITICAL | 6/6 agents: CRITICAL | Grade F, AUTO BLOCK |
| Split on HIGH | 3/6 HIGH, 3/6 MEDIUM | Grade B (escalate to HIGH) |
| Partial timeout | 5/6 return, 1 timeout | Grade computed, note timeout |
| Below quorum | 4/6 return | INCOMPLETE, no grade |
| Empty results | 6/6 return, 0 findings | Grade A, escalate "empty swarm?" |
| Duplicate finding | 3 agents same file:42 | 1 finding, agreement "3/6" |

---

## Verdict Computation

Uses council consensus rules to determine final verdict:

| Condition | Verdict |
|-----------|---------|
| All PASS | PASS |
| Any FAIL | FAIL |
| Mixed PASS/WARN | WARN |
| Cross-vendor disagree | DISAGREE (surface both, defer to human) |

## Contradiction Handling

When agents explicitly contradict (one says "secure", another says "vulnerable"):

1. Flag as **CONTESTED** finding
2. Include both positions with reasoning
3. Escalate to human review
4. Do NOT auto-resolve contradictions — they signal genuine uncertainty

Contested findings are surfaced prominently in the report with both agent positions side-by-side.

---

## Related

- Pre-mortem: `.agents/pre-mortems/2026-01-26-flatten-skill-nesting.md` (Finding #3)
- Vibe-coding: `skills/vibe/references/vibe-coding.md` (grade computation)
- Flywheel: `.agents/patterns/rpi-4-gates-flywheel.md` (gate decision)
