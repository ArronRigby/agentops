---
name: context-bundling
description: Create and load context bundles for session continuity. Use when starting/ending sessions, switching between phases, or when context approaches 40% threshold.
---

# context-bundling Skill

**Purpose:** Compress working context into portable bundles that survive session boundaries.

---

## When to Use

- Ending a session (save current state)
- Starting a session (load previous state)
- Switching RPI phases (research → plan → implement)
- Context approaching 40% threshold
- Handing off to another agent/session

---

## The 40% Rule

**Never exceed 40% context usage.** When approaching threshold:

1. **Stop new loading** - Don't read more files
2. **Synthesize findings** - Extract key insights
3. **Create bundle** - Compress to 2-5k tokens
4. **Save and reset** - Bundle preserves work

```
Context Zones:
🟢 <35%  - Continue working
⚡ 35-40% - Prepare bundle, stop loading
⚠️ 40-60% - Create bundle NOW, transition
🔴 >60%  - Reset immediately (context degraded)
```

---

## Bundle Creation Process

### Step 1: Identify What to Preserve

Essential:
- Key discoveries/decisions
- File references (path:line)
- Constraints identified
- Success criteria
- Next steps

Drop:
- Raw file contents (already in git)
- Exploration dead-ends
- Verbose explanations
- Intermediate reasoning

### Step 2: Compress Ruthlessly

**60k tokens → 2-3k tokens (20-30x compression)**

| Original | Compressed |
|----------|------------|
| Full file contents | File path + line numbers |
| Detailed analysis | 1-sentence summary |
| Multiple options explored | Recommended option + why |
| Step-by-step reasoning | Final conclusion |

### Step 3: Structure Bundle

```yaml
---
bundle_type: [research|plan|implementation|learning]
topic: [descriptive-name]
phase: [current-phase-status]
created: YYYY-MM-DD
context_tokens: [original]
compressed_tokens: [final]
---

## Executive Summary
[2-3 sentences capturing the essence]

## Key Findings
- [Most important insight 1]
- [Most important insight 2]
- [Most important insight 3]

## Constraints
- [Constraint 1]
- [Constraint 2]

## Success Criteria
- [Criterion 1]
- [Criterion 2]

## File References
- `src/path/file.ts:45-89` - [what's there]
- `tests/file.test.ts:12` - [what's there]

## Next Phase
[What to do when bundle is loaded]
```

### Step 4: Save to Filesystem

```bash
# Location
.agents/bundles/[topic]-[type]-YYYY-MM-DD.md

# Example
.agents/bundles/auth-research-2025-11-30.md
```

---

## Bundle Loading Process

### Step 1: Locate Bundle

```bash
# List available
ls .agents/bundles/

# Search by topic
ls .agents/bundles/ | grep -i "auth"
```

### Step 2: Load Selectively

Read bundle (~2-3k tokens), NOT original files.

Bundle contains enough to:
- Understand what was done
- Know what to do next
- Find original files if needed

### Step 3: Verify Context Budget

After loading:
```
Context: 🟢 3% loaded
Ready for: [next phase work]
```

---

## Bundle Chains

Bundles link to create work history:

```
research-bundle
    ↓ (references)
plan-bundle
    ↓ (references)
implementation-report
    ↓ (references)
learnings-bundle
```

Each bundle includes:
```yaml
previous_bundle: [name of prior phase bundle]
```

---

## Common Mistakes

### Loading Too Much

**Wrong:**
```bash
# Load bundle AND all original files
cat .agents/bundles/auth-research.md
cat src/auth/*.ts  # Redundant!
```

**Right:**
```bash
# Load bundle only
cat .agents/bundles/auth-research.md
# Read specific files ONLY when needed
```

### Not Compressing Enough

**Wrong:** 15k token "bundle" (just a copy of work)

**Right:** 2-3k token bundle with pointers to originals

### Skipping Bundle on Phase Transition

**Wrong:** Start planning without saving research bundle

**Right:** `/bundle-save` before `/plan`

---

## Integration

Works with:
- `/bundle-save` - Create bundle
- `/bundle-load` - Load bundle
- `/session-end` - Auto-offers bundle save
- `/session-resume` - Auto-searches bundles
