---
name: context-engineering
description: The 40% Rule and JIT context loading patterns. Use to manage token budget effectively and prevent context collapse.
---

# context-engineering Skill

**Purpose:** Manage context efficiently to prevent collapse and maximize effectiveness.

---

## The 40% Rule

**Problem:** 200k token limit. Loading everything causes:
- 99% information loss
- Context collapse
- Forgetting recent instructions
- Contradicting earlier statements

**Solution:** Stay under 40% of token budget.

---

## Token Budget Zones

```
🟢 <35% (70k)      GREEN
   Continue working normally
   Load additional context as needed

⚡ 35-40% (70-80k)  YELLOW
   Prepare to bundle
   Stop loading new files
   Start synthesizing findings

⚠️ 40-60% (80-120k) RED
   Bundle NOW
   No more file loading
   Transition to next phase

🔴 >60% (120k+)    CRITICAL
   Context degrading
   Emergency bundle
   Reset session immediately
```

---

## JIT Loading Pattern

**Just-In-Time:** Load only what you need, when you need it.

### Bad (Upfront Loading)

```bash
# Load everything at start (90k tokens, exceeds 40%)
cat docs/**/*.md
cat .claude/agents/*.md
cat src/**/*.ts
```

**Result:** Context collapse, forgetting, hallucination

### Good (JIT Loading)

```bash
# Load baseline only
/prime                          # 2k tokens (constitution)

# User describes task

# Load ONLY relevant patterns
cat docs/patterns/auth.md      # 1-2k tokens

# Total: 3-4k (2% of budget)
```

**Result:** Sharp focus, full retention, no collapse

---

## Gather → Glean → Summarize

### Phase 1: Gather

Discover what exists:
```bash
# Don't read files, just find them
Glob: "**/*auth*.ts"
# Found: 8 files

Grep: "JWT" --glob="**/*.ts"
# Found: 12 matches in 5 files
```

**Context cost:** ~0 (file paths only)

### Phase 2: Glean

Read selectively:
```bash
# Read most relevant first
Read: src/auth/middleware.ts
# Extract: JWT validation, Redis blacklist

Read: src/auth/handlers.ts
# Extract: Login/logout flow
```

**Context cost:** ~5-10k per file

### Phase 3: Summarize

Synthesize findings:
```markdown
## Key Findings
- JWT auth with 24h expiry
- Redis blacklist for logout
- No refresh tokens
```

**Context cost:** ~500 tokens (summary replaces raw files)

---

## Context Estimation

### File Size Rules of Thumb

| File Type | Typical Size |
|-----------|--------------|
| Small config | 500-1k tokens |
| Medium module | 2-5k tokens |
| Large component | 5-15k tokens |
| Documentation | 1-5k tokens |

### Activity Costs

| Activity | Token Cost |
|----------|------------|
| Load primer | 2-5k |
| Read file | 1-10k per file |
| Search results | 500-2k |
| Bundle load | 2-5k |
| Tool output | 500-2k |

### Accumulation

Tokens accumulate across conversation:
- Message 1: 5k (primer)
- Message 3: 12k (read 2 files)
- Message 5: 20k (more files)
- Message 7: 30k (approaching 35%)
- **Message 9: 38k → BUNDLE NOW**

---

## Bundling at 40%

When approaching threshold:

### Step 1: Stop Loading

No more `Read` or `cat` commands.

### Step 2: Synthesize

Extract key insights from everything loaded:
```markdown
## Summary
[2-3 sentences of key findings]

## File References
[path:line for important locations]

## Next Steps
[what to do with fresh context]
```

### Step 3: Save Bundle

```bash
/bundle-save [topic]-[phase]-[date]
```

### Step 4: Continue or Reset

**If same phase:** Continue with bundle as reference
**If new phase:** Reset context, load bundle

---

## Signs of Context Collapse

Watch for these degradation signals:

| Signal | Severity | Action |
|--------|----------|--------|
| Forgetting recent instructions | High | Bundle and reset |
| Contradicting earlier statements | High | Bundle and reset |
| Asking same questions twice | Medium | Bundle soon |
| Losing track of task | High | Bundle and reset |
| Missing obvious file references | Medium | Synthesize |

---

## Recovery Protocol

If context has collapsed (>60%):

1. **Stop all file loading immediately**
2. **Extract most important findings**
3. **Create emergency bundle**
4. **Start fresh session**
5. **Load emergency bundle**

```bash
# Emergency bundle
/bundle-save emergency-[timestamp]

# Fresh session
# (start new conversation)

# Load bundle
/bundle-load emergency-[timestamp]
```

---

## Best Practices

### Do

- Estimate before loading
- Track cumulative usage
- Bundle proactively at 35%
- Use file paths instead of contents when possible
- Summarize instead of quoting

### Don't

- Load "just in case"
- Read entire directories
- Keep raw file contents in context
- Ignore the 40% threshold
- Wait for collapse to bundle
