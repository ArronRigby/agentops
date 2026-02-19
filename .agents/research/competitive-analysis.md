# Competitive Analysis & Roadmap

> Relocated from PRODUCT.md on 2026-02-19. Reference material, not product spec.

## Competitive Landscape

Two layers matter here:
1. Approach-level alternatives (do you even need a workflow layer? where do you put validation?)
2. Named tools in the Claude Code / agent-workflow ecosystem (what users will compare us to in practice)

### Approach-Level Alternatives

| Alternative | Strength | Our Differentiation |
|-------------|----------|---------------------|
| Direct Agent Use (Claude Code, Cursor, Copilot) | Full autonomy; no overhead; simple to start | Adds multi-model councils, fresh-context waves, and knowledge compounding. A bare agent writes code once; ours extracts learnings and applies them next session. |
| Custom Prompt Engineering (.cursorrules, CLAUDE.md) | Flexible, version-controlled, lightweight | Static instructions don't compound. Our flywheel auto-extracts learnings and injects them back. `/post-mortem` proposes changes to the tools themselves. Progressive skill discovery shows 5 commands on day 1, not 27. |
| Agent Orchestrators (CrewAI, AutoGen, LangGraph) | Mature multi-language task scheduling | Those route work between agents but don't manage what's in each agent's context window. We treat context quality as the primary lever — fresh-context isolation per worker, phase-specific loading, knowledge quality gates. No external state backend — all learnings are git-tracked. |
| CI/CD Quality Gates (GitHub Actions, pre-commit) | Automated, enforced, industry standard | Gates run after code is written. Ours run before coding (`/pre-mortem`) and before push (`/vibe`). Failures retry with context, not human escalation. |
| Olympus (Mount Olympus) | Persistent daemon, context provenance, constraint injection (learnings become `*_test.go`), run ledger tracking every attempt | Complementary, not competing. AgentOps is the autonomous engine (skills, hooks, flywheel). Olympus is the power-user daemon layer that composes AgentOps for fully cross-session automation — nobody types `/rpi`, daemon polls and spawns. We stand alone; Olympus builds on top. |

### Named Tool Competitors

| Tool | What it does well | Where AgentOps differentiates |
|------|-------------------|------------------------------|
| [GSD (Get Shit Done)](https://github.com/glittercowboy/get-shit-done) | Lightweight meta-prompting and context practices that keep a single session moving | Persistence across sessions (curated learnings injected automatically), and more explicit validation gates around planning and shipping |
| [Compound Engineer](https://github.com/EveryInc/compound-engineering-plugin) | Structured "compound the work" loop and knowledge practices | Stronger multi-model review and gating (pre-mortem and vibe), plus repo-local, git-tracked knowledge artifacts |
| [Superpowers](https://github.com/obra/superpowers) | TDD-heavy workflows and disciplined implementation | Cross-session memory and compounding; broader lifecycle automation beyond implementation discipline |
| [Claude-Flow](https://github.com/ruvnet/claude-flow) | Swarm-style orchestration and high parallelism | Focus on context quality per worker and learning across time, not just routing and throughput |
| Spec-Driven Development (SDD) tools: [cc-sdd](https://github.com/gotalab/cc-sdd), GitHub Spec Kit, spec-kit, SDD_Flow | Spec-first process and templates as primary artifact | Adds "learnings as first-class artifacts" and failure simulation before building (pre-mortem), so the workflow improves over time, not just per spec |
| [Deep Trilogy / deep-plan](https://github.com/piercelamb/deep-plan) | Deep planning, checkpoint resumability, external review patterns | Wave-based parallel execution (`/crank`), cross-runtime orchestration, and systematic post-mortem extraction that feeds the next cycle |

## Roadmap

### Now (0-30 days)

| Initiative | Competitor driver | Why | Acceptance criteria |
|-----------|-------------------|-----|---------------------|
| Complexity-aware ceremony | GSD, BMAD-style workflows | Small tasks should not pay full RPI overhead; big tasks still need gates | `/rpi` auto-selects fast-path vs full lifecycle and logs the chosen mode |
| Scale without swarms guide | Claude-Flow | Provide an explicit alternative to "60+ agents": waves + isolation + gates | A short "scale story" doc exists and is referenced from `PRODUCT.md` and/or `docs/FAQ.md` |
| Test-first mode tightened | Superpowers | Make "TDD supported" credible with evidence, not just intent | "Test-first" runs produce artifacts showing failing tests existed before implementation and passed after |

### Next (30-90 days)

| Initiative | Competitor driver | Why | Acceptance criteria |
|-----------|-------------------|-----|---------------------|
| Council profiles (`budget/balanced/quality`) | GSD | Users need a knob for cost/latency vs rigor without editing internals | A profile flag exists and every council report logs the selected profile |
| Named personas for judges | Compound Engineer | Make reviews legible and persuasive by attaching critiques to stable expert roles | At least 5 named personas ship, each with a clear responsibility and stable output labeling |
| Technique-driven brainstorming | BMAD, Superpowers planning modes | Structured ideation improves plan quality and reduces retries | Brainstorm supports technique presets and documents each technique succinctly |
| Spec/plan interoperability | SDD tools | Meet expectations for spec templates and "spec as artifact" workflows | Plans include conformance checks by default; optional export to `.agents/specs/` exists |

### Later (6-12 months)

| Initiative | Competitor driver | Why | Acceptance criteria |
|-----------|-------------------|-----|---------------------|
| Provenance-first compounding | Trust gap vs "magic memory" | Make the knowledge flywheel auditable (origin, freshness, utility) | Injected artifacts include origin + last-used/utility metadata and can be traced back to commits/sessions |
| Checkpoint/resume as product surface | deep-plan | Long-running work needs safe resumability across phases | First-class "resume from phase" artifacts exist and the recovery path is documented |
| Optional local RAG for knowledge | Claude-Flow | Improve retrieval quality while staying local-first | A local-only semantic search path exists (opt-in) and integrates with `ao search` without cloud state |
