---
description: Load saved research/plan bundles from filesystem (search first with /bundle-search)
allowed-tools: Read, Glob
---

# /bundle-load - Load Context Bundle

Load a previously saved context bundle to resume work.

## Usage

```bash
/bundle-load [bundle-name]        # Load specific bundle
/bundle-load --latest             # Load most recent bundle
/bundle-load --search [topic]     # Search and select
```

## Protocol

### Direct Load

```bash
/bundle-load auth-research-2025-11-30
```

1. Read bundle from `.agents/bundles/`
2. Parse YAML frontmatter
3. Display summary
4. Ready to continue from `next_phase`

### Latest Bundle

```bash
/bundle-load --latest
```

Loads most recently modified bundle in `.agents/bundles/`

### Search and Select

```bash
/bundle-load --search auth
```

1. Search bundles matching topic
2. Display options with dates
3. User selects
4. Load selected bundle

## Output

```
📦 Bundle loaded: auth-research-2025-11-30

Type: research
Phase: research-complete
Created: 2025-11-30

📋 Summary:
JWT-based auth with Redis blacklist. No refresh tokens.
Redis is SPOF. Need HA strategy.

🎯 Success Criteria:
- Refresh token rotation working
- Tests cover edge cases
- Redis HA configured

⏭️ Next Phase: plan

Context: 🟢 3% loaded (2.4k tokens)

Ready for: /plan auth-research-2025-11-30
```

## Bundle Chaining

Bundles reference previous phases:

```
research-bundle → plan-bundle → implementation-report → learnings
```

When loading a plan bundle, it includes reference to its research bundle:

```yaml
---
bundle_type: plan
research_bundle: auth-research-2025-11-30
---
```

## Context Budget

Loading a bundle typically uses 1-3% of context budget:

| Bundle Type | Typical Size | Context % |
|-------------|--------------|-----------|
| Research | 2-3k tokens | 1-1.5% |
| Plan | 3-5k tokens | 1.5-2.5% |
| Implementation | 2-4k tokens | 1-2% |
| Learning | 1-2k tokens | 0.5-1% |

**Total for full chain:** ~5-7% (leaves 93-95% for work)
