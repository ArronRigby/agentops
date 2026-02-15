# Vibe-Check Inner-Loop: Detectors & Metrics Research

Extracted from vibe-check TypeScript codebase. Source: /Users/fullerbt/workspaces/personal/vibe-check/

## Summary Table

| Component | File | LOC | Type | Key Thresholds |
|-----------|------|-----|------|----------------|
| context-amnesia | src/inner-loop/context-amnesia.ts | 319 | Detector | deletions>10, re-additions>50%, fixes≥3, similarity>0.7, 60min window |
| instruction-drift | src/inner-loop/instruction-drift.ts | 346 | Detector | 6+ files=refactor, max(3×avg,10)=scope creep, working set=3 commits |
| logging-only | src/inner-loop/logging-only.ts | 334 | Detector | 3 consecutive, >80% ratio, 46 patterns across 8 languages |
| tests-passing-lie | src/inner-loop/tests-passing-lie.ts | 260 | Detector | min 2 commits, 30min window, 13 success patterns, 9 tentative exclusions |
| flow | src/metrics/flow.ts | 99 | Metric | >90 elite, ≥75 high, ≥50 medium, <50 low |
| rework | src/metrics/rework.ts | 54 | Metric | <30 elite, <50 high, <70 medium, ≥70 low |
| spirals | src/metrics/spirals.ts | 182 | Metric | <15min elite, <30 high, <60 medium, ≥60 low; 6 pattern categories |
| trust | src/metrics/trust.ts | 191 | Metric | >95% elite, ≥80 high, ≥60 medium, <60 low; 81 stopwords |
| velocity | src/metrics/velocity.ts | 135 | Metric | >5 elite, ≥3 high, ≥1 medium, <1 low; 120min session gap |
| orchestrator | src/inner-loop/index.ts | 266 | Aggregator | 3+ critical=emergency protocol |
| metrics-index | src/metrics/index.ts | 183 | Aggregator | equal weight (1/5), ≥3.5 ELITE, ≥2.5 HIGH, ≥1.5 MEDIUM |

## Cross-References

**Detectors → Health Scoring:**
- tests-passing-lie + context-amnesia (≥3 incidents) → CRITICAL
- instruction-drift + logging-only → WARNING
- 3+ total critical issues → emergency protocol

**Metrics → Overall Rating:**
- All 5 metrics contribute equally (weight = 1/5)
- Scoring: elite=4, high=3, medium=2, low=1
- Average determines overall: ELITE/HIGH/MEDIUM/LOW

**Shared Data Flow:**
- `TimelineEvent` feeds both detectors and metrics
- `Commit` → `TimelineEvent` (via timeline builder, not in inner-loop)
- Fix chains (spirals detector) → flow metric (debugging minutes)
- File stats → context-amnesia (line counts), instruction-drift (file counts)

## Architecture: Data Flow

```
git log + git diff
    │
    ▼
TimelineEvent[] (commits with metadata)
    │
    ├──► Inner-Loop Detectors (parallel)
    │       ├── tests-passing-lie → LieResult[]
    │       ├── context-amnesia → IncidentResult[]
    │       ├── instruction-drift → DriftResult[]
    │       └── logging-only → LoggingResult[]
    │       │
    │       ▼
    │    index.ts aggregator
    │       ├── overallHealth: 'healthy' | 'warning' | 'critical'
    │       ├── recommendations[]
    │       └── emergencyProtocol (if 3+ critical)
    │
    └──► Metrics (parallel)
            ├── velocity (commits/hour)
            ├── rework (fix %)
            ├── trust (trusted commit %)
            ├── spirals (avg spiral duration)
            └── flow (productive time %)
            │
            ▼
         index.ts aggregator
            ├── individual ratings (elite/high/medium/low)
            └── overallRating (weighted average)
                │
                ▼
         VibeCheckResult / VibeCheckResultV2
            ├── metrics + ratings
            ├── innerLoop analysis
            └── output → terminal | json | markdown
```

## Shared Types and Interfaces

### src/types.ts

**Primitive Type Aliases** (L1-L3)
```typescript
export type Rating = 'elite' | 'high' | 'medium' | 'low';
export type OutputFormat = 'terminal' | 'json' | 'markdown';
export type OverallRating = 'ELITE' | 'HIGH' | 'MEDIUM' | 'LOW';
```

**Commit Interface** (L5-L12)
```typescript
export interface Commit {
  hash: string;
  date: Date;
  message: string;
  type: 'feat' | 'fix' | 'docs' | 'chore' | 'refactor' | 'test' | 'style' | 'tracer' | 'other';
  scope: string | null;
  author: string;
}
```

**MetricResult Interface** (L14-L19)
```typescript
export interface MetricResult {
  value: number;
  unit: string;
  rating: Rating;
  description: string;
}
```

**FixChain Interface** (L21-L29)
```typescript
export interface FixChain {
  component: string;
  commits: number;
  duration: number; // minutes
  isSpiral: boolean;
  pattern: string | null;
  firstCommit: Date;
  lastCommit: Date;
}
```

**PatternSummary Interface** (L31-L35)
```typescript
export interface PatternSummary {
  categories: Record<string, number>;
  total: number;
  tracerAvailable: number;
}
```

**VibeCheckResult Interface** (L37-L61)
```typescript
export interface VibeCheckResult {
  period: {
    from: Date;
    to: Date;
    activeHours: number;
  };
  commits: {
    total: number;
    feat: number;
    fix: number;
    docs: number;
    tracer: number;
    other: number;
  };
  metrics: {
    iterationVelocity: MetricResult;
    reworkRatio: MetricResult;
    trustPassRate: MetricResult;
    debugSpiralDuration: MetricResult;
    flowEfficiency: MetricResult;
  };
  fixChains: FixChain[];
  patterns: PatternSummary;
  overall: OverallRating;
}
```

**VibeCheckResultV2 Interface** (L66-L68)
```typescript
/**
 * Extended result with semantic metrics alias for output formatting
 */
export interface VibeCheckResultV2 extends VibeCheckResult {
  semanticMetrics: VibeCheckResult['metrics'];
}
```

**TimelineEvent Interface** (L73-L80)
```typescript
/**
 * Timeline event for inner-loop analysis
 */
export interface TimelineEvent {
  hash: string;
  timestamp: Date;
  author: string;
  subject: string;
  type: Commit['type'];
  scope: string | null;
}
```

**Re-exported Error Types** (L86-L103)
```typescript
export {
  ExitCode,
  ErrorCode,
  VibeCheckError,
  GitError,
  ValidationError,
  ConfigError,
  AnalysisError,
  isVibeCheckError,
  isGitError,
  isValidationError,
  isConfigError,
  isAnalysisError,
  getExitCode,
  getErrorCode,
  formatError,
  wrapError,
} from './errors.js';
```

---

### src/inner-loop/types.ts

**File Header Comment** (L1-L9)
```typescript
/**
 * Inner Loop Failure Pattern Types
 *
 * These detect the 4 "Inner Loop Disasters" from vibe coding:
 * 1. "Tests Passing" Lie - AI claims success but code doesn't work
 * 2. Context Amnesia - Forgets instructions, re-does work
 * 3. Instruction Drift - "Improves" things not asked for
 * 4. Debug Loop Spiral - Adds logging instead of fixing
 */
```

**Imports** (L11)
```typescript
import { Commit, TimelineEvent } from '../types.js';
```

#### Pattern 1: "Tests Passing" Lie

**TestsPassingLieResult Interface** (L17-L22)
```typescript
export interface TestsPassingLieResult {
  detected: boolean;
  lies: TestsPassingLie[];
  totalLies: number;
  message: string;
}
```

**TestsPassingLie Interface** (L24-L38)
```typescript
export interface TestsPassingLie {
  commitHash: string;
  commitMessage: string;
  timestamp: Date;
  claimedSuccess: boolean; // Commit message claims fix/pass/working
  /**
   * Actual verification result:
   * - 'build_failed': Build command failed
   * - 'tests_failed': Test command failed
   * - 'inferred': Detected from commit patterns (no actual verification)
   * - 'unknown': Verification attempted but result unclear
   */
  actualResult: 'build_failed' | 'tests_failed' | 'inferred' | 'unknown';
  verificationMethod: 'npm_test' | 'npm_build' | 'make_test' | 'inferred';
}
```

#### Pattern 2: Context Amnesia

**ContextAmnesiaResult Interface** (L44-L50)
```typescript
export interface ContextAmnesiaResult {
  detected: boolean;
  incidents: ContextAmnesiaIncident[];
  totalIncidents: number;
  totalTimeWasted: number; // minutes
  message: string;
}
```

**ContextAmnesiaIncident Interface** (L52-L68)
```typescript
export interface ContextAmnesiaIncident {
  type: 'revert' | 'reimplementation' | 'forgotten_change';
  originalCommit: {
    hash: string;
    message: string;
    timestamp: Date;
  };
  repeatCommit: {
    hash: string;
    message: string;
    timestamp: Date;
  };
  scope: string | null;
  filesAffected: string[];
  gapMinutes: number; // Time between original and repeat
  description: string;
}
```

#### Pattern 3: Instruction Drift

**InstructionDriftResult Interface** (L74-L80)
```typescript
export interface InstructionDriftResult {
  detected: boolean;
  drifts: InstructionDrift[];
  totalDriftCommits: number;
  totalUnauthorizedFiles: number;
  message: string;
}
```

**InstructionDrift Interface** (L82-L90)
```typescript
export interface InstructionDrift {
  commitHash: string;
  commitMessage: string;
  timestamp: Date;
  driftType: 'scope_creep' | 'unrequested_refactor' | 'unrequested_improvement' | 'style_change';
  unauthorizedFiles: string[];
  authorizedScope: string[]; // Expected files/dirs based on session intent
  description: string;
}
```

**SessionScope Interface** (L92-L97)
```typescript
export interface SessionScope {
  intendedFiles: string[];
  intendedDirs: string[];
  taskDescription?: string;
  startTime: Date;
}
```

#### Pattern 4: Debug Loop Spiral (Enhanced)

**LoggingOnlyResult Interface** (L103-L109)
```typescript
export interface LoggingOnlyResult {
  detected: boolean;
  loggingCommits: LoggingOnlyCommit[];
  consecutiveLoggingCount: number;
  totalLoggingCommits: number;
  message: string;
}
```

**LoggingOnlyCommit Interface** (L111-L125)
```typescript
export interface LoggingOnlyCommit {
  hash: string;
  message: string;
  timestamp: Date;
  loggingStatements: number; // Count of console.log, print, etc. added
  actualFixes: number; // Count of non-logging changes
  isLoggingOnly: boolean;
  loggingPatterns: string[]; // e.g., ['console.log', 'console.error']
  /**
   * How this commit was analyzed:
   * - 'inferred': Lightweight mode - loggingStatements/actualFixes are estimates from message patterns
   * - 'diff_analysis': Full mode - accurate counts from git diff inspection
   */
  detectionMode?: 'inferred' | 'diff_analysis';
}
```

#### Aggregated Results

**InnerLoopAnalysis Interface** (L131-L148)
```typescript
export interface InnerLoopAnalysis {
  // Individual pattern results
  testsPassingLie: TestsPassingLieResult;
  contextAmnesia: ContextAmnesiaResult;
  instructionDrift: InstructionDriftResult;
  loggingOnly: LoggingOnlyResult;

  // Aggregated metrics
  summary: {
    totalIssuesDetected: number;
    criticalIssues: number; // High severity
    warningIssues: number; // Medium severity
    overallHealth: 'healthy' | 'warning' | 'critical';
  };

  // Recommendations
  recommendations: string[];
}
```

#### Detection Configuration

**InnerLoopConfig Interface** (L154-L172)
```typescript
export interface InnerLoopConfig {
  // Tests Passing Lie
  runTestsAfterCommit: boolean;
  testCommand?: string; // e.g., 'npm test', 'make test'
  buildCommand?: string; // e.g., 'npm run build'

  // Context Amnesia
  amnesiaWindowMinutes: number; // How far back to look for repeats (default: 60)
  similarityThreshold: number; // 0-1, how similar commits must be to flag (default: 0.7)

  // Instruction Drift
  sessionScope?: SessionScope;
  allowedDriftFiles: string[]; // Files that are always OK to change (e.g., package.json)
  workingSetCommitCount: number; // How many initial commits define the working set (default: 3)

  // Logging Only
  maxConsecutiveLoggingCommits: number; // Flag after this many (default: 3)
  loggingPatterns: RegExp[]; // Patterns to detect logging statements
}
```

**DEFAULT_INNER_LOOP_CONFIG Constant** (L174-L190)
```typescript
export const DEFAULT_INNER_LOOP_CONFIG: InnerLoopConfig = {
  runTestsAfterCommit: false,
  amnesiaWindowMinutes: 60,
  similarityThreshold: 0.7,
  allowedDriftFiles: ['package.json', 'package-lock.json', 'tsconfig.json', '.gitignore'],
  workingSetCommitCount: 3, // First 3 commits define working set for drift detection
  maxConsecutiveLoggingCommits: 3,
  loggingPatterns: [
    /console\.(log|error|warn|debug|info)\(/,
    /print\s*\(/,
    /logger\.(log|error|warn|debug|info)\(/,
    /System\.out\.print/,
    /fmt\.Print/,
    /debug!\(/,
    /println!\(/,
  ],
};
```

---

## Type Hierarchy

### Core Data Flow

**Commit Processing Pipeline:**
```
Git History
    ↓
Commit[] (from src/types.ts L5-L12)
    ↓
TimelineEvent[] (from src/types.ts L73-L80) [used for inner-loop analysis]
    ↓
Inner Loop Detectors (src/inner-loop/types.ts)
    ├─→ TestsPassingLieResult
    ├─→ ContextAmnesiaResult
    ├─→ InstructionDriftResult
    └─→ LoggingOnlyResult
    ↓
InnerLoopAnalysis (aggregated)
```

**Metrics Pipeline:**
```
Commit[] + FixChain[]
    ↓
Metric Calculators
    ↓
MetricResult (src/types.ts L14-L19)
    ├─→ iterationVelocity
    ├─→ reworkRatio
    ├─→ trustPassRate
    ├─→ debugSpiralDuration
    └─→ flowEfficiency
    ↓
VibeCheckResult.metrics
```

### Rating Systems

**Two parallel rating systems:**

1. **MetricResult.rating** (src/types.ts L1, L17)
   - Type: `Rating = 'elite' | 'high' | 'medium' | 'low'`
   - Used for individual metrics (iteration velocity, rework ratio, etc.)
   - Lowercase

2. **VibeCheckResult.overall** (src/types.ts L3, L60)
   - Type: `OverallRating = 'ELITE' | 'HIGH' | 'MEDIUM' | 'LOW'`
   - Used for aggregate session health
   - Uppercase

3. **InnerLoopAnalysis.summary.overallHealth** (src/inner-loop/types.ts L143)
   - Type: `'healthy' | 'warning' | 'critical'`
   - Used for inner-loop pattern severity
   - Different scale from main ratings

### Detector Result Pattern

**All four inner-loop detectors follow this structure:**
```typescript
interface <Pattern>Result {
  detected: boolean;          // Boolean flag for presence
  <items>: <PatternType>[];   // Array of detected instances
  total<Items>: number;       // Count of instances
  message: string;            // Human-readable summary
}
```

Examples:
- `TestsPassingLieResult.lies: TestsPassingLie[]`
- `ContextAmnesiaResult.incidents: ContextAmnesiaIncident[]`
- `InstructionDriftResult.drifts: InstructionDrift[]`
- `LoggingOnlyResult.loggingCommits: LoggingOnlyCommit[]`

### Commit Metadata Reuse

**Commit-based pattern items share common fields:**
```typescript
{
  commitHash: string;      // OR hash: string (LoggingOnlyCommit)
  commitMessage: string;   // OR message: string (LoggingOnlyCommit)
  timestamp: Date;
  // ... pattern-specific fields
}
```

This consistency allows generic commit-to-pattern mappings.

### Configuration Hierarchy

**InnerLoopConfig** (src/inner-loop/types.ts L154-L172) groups settings by detector:
- **Tests Passing Lie:** `runTestsAfterCommit`, `testCommand`, `buildCommand`
- **Context Amnesia:** `amnesiaWindowMinutes`, `similarityThreshold`
- **Instruction Drift:** `sessionScope`, `allowedDriftFiles`, `workingSetCommitCount`
- **Logging Only:** `maxConsecutiveLoggingCommits`, `loggingPatterns`

Default configuration provided in `DEFAULT_INNER_LOOP_CONFIG` (L174-L190).

### Severity Classification

**InnerLoopAnalysis.summary** (src/inner-loop/types.ts L139-L143) distinguishes:
- `criticalIssues`: High severity patterns (e.g., tests passing lie, context amnesia)
- `warningIssues`: Medium severity patterns (e.g., instruction drift, single logging commit)
- `overallHealth`: Aggregate health status derived from critical/warning counts

### Optional Detection Modes

**Some pattern items include detection metadata:**

**TestsPassingLie.actualResult** (L36):
- `'build_failed' | 'tests_failed'` = actual verification performed
- `'inferred' | 'unknown'` = heuristic/pattern-based detection

**LoggingOnlyCommit.detectionMode** (L124):
- `'inferred'`: Lightweight (message pattern matching)
- `'diff_analysis'`: Full (git diff inspection)

This allows detectors to run in different modes (fast/approximate vs. slow/accurate).

### Time-Based Relationships

**Duration tracking across types:**

1. **FixChain.duration** (src/types.ts L24): Total time for a fix chain (minutes)
2. **ContextAmnesiaIncident.gapMinutes** (src/inner-loop/types.ts L66): Time between original and repeat commit
3. **VibeCheckResult.period.activeHours** (src/types.ts L41): Total session active time

All use different units (minutes vs. hours) — conversion required for comparisons.

### File Scope Tracking

**Two mechanisms for tracking file changes:**

1. **ContextAmnesiaIncident.filesAffected** (src/inner-loop/types.ts L65)
   - Array of file paths modified in amnesia incident

2. **InstructionDrift** (src/inner-loop/types.ts L82-L90)
   - `unauthorizedFiles`: Files changed outside scope
   - `authorizedScope`: Expected files/dirs from session intent
   - **SessionScope** (L92-L97): Defines intended working set

This enables drift detection by comparing actual vs. intended file changes.

---

## Inner-Loop Detectors

### context-amnesia

**File:** `src/inner-loop/context-amnesia.ts`

**Purpose:** Detects when AI forgets previous instructions and reverts intentional changes, re-implements code that was just deleted, or repeats the same fix multiple times.

**Regex Patterns:**

**Revert Detection Patterns** (L104-L110):
```typescript
const revertPatterns = [
  /revert/i,
  /undo/i,
  /rollback/i,
  /back\s*out/i,
  /restore\s+previous/i,
];
```

**Reimplementation Detection** (L206):
```typescript
/refactor/i  // Used to exclude intentional refactors from reimplementation detection
```

**Numeric Thresholds:**

- **Reimplementation Deletion Threshold** (L175): `commit.deletions > commit.additions && commit.deletions > 10`
  - Requires more deletions than additions
  - AND minimum 10 lines deleted

- **Reimplementation Re-addition Threshold** (L200): `commit.additions < deletion.linesDeleted * 0.5`
  - Re-additions must be at least 50% of deleted lines

- **Repeated Fix Minimum** (L257): `fixes.length < 3`
  - Requires at least 3 fixes in same scope to flag

- **Similarity Threshold** (L269): `similarity > config.similarityThreshold`
  - Default: 0.7 (from DEFAULT_INNER_LOOP_CONFIG)
  - Jaccard index for commit message similarity

**Scoring Formula:**

Total time wasted (L77):
```typescript
const totalTimeWasted = incidents.reduce((sum, i) => sum + i.gapMinutes, 0);
```

Message similarity (Jaccard index, L297-L318):
```typescript
function calculateSimilarity(msg1: string, msg2: string): number {
  const words1 = new Set(
    msg1
      .toLowerCase()
      .replace(/[^a-z0-9\s]/g, '')
      .split(/\s+/)
      .filter((w) => w.length > 2)
  );
  const words2 = new Set(
    msg2
      .toLowerCase()
      .replace(/[^a-z0-9\s]/g, '')
      .split(/\s+/)
      .filter((w) => w.length > 2)
  );

  if (words1.size === 0 || words2.size === 0) return 0;

  const intersection = new Set([...words1].filter((w) => words2.has(w)));
  const union = new Set([...words1, ...words2]);

  return intersection.size / union.size;
}
```

**Detection Logic:**

Three detection strategies (L70-L72):
1. **Reverts** (`detectReverts`): Finds commits with revert patterns in message, matches to previous commits touching same files within time window
2. **Reimplementation** (`detectReimplementation`): Tracks significant deletions, then finds later commits that re-add similar content to same files
3. **Repeated Fixes** (`detectRepeatedFixes`): Groups fix commits by scope, flags scopes with 3+ similar fixes in time window

**Time Window:** Uses `config.amnesiaWindowMinutes` (default 60 minutes from DEFAULT_INNER_LOOP_CONFIG)

**Aggregation Logic:**

- Returns top 10 incidents (L90)
- Calculates total time wasted across all incidents
- Detected if incidents.length > 0 (L80)
- Message includes incident types and total time wasted (L82-L86)

---

### instruction-drift

**File:** `src/inner-loop/instruction-drift.ts`

**Purpose:** Detects when AI changes files outside stated scope, does unrequested refactors, makes style changes to unrelated code, or "cleans up" working code.

**Regex Patterns:**

**Drift Pattern Categories** (L23-L50):
```typescript
const DRIFT_PATTERNS = {
  unrequested_refactor: [
    /\brefactor/i,
    /\bcleanup\b/i,
    /\bclean\s*up\b/i,
    /\breorganize/i,
    /\brestructure/i,
    /\bsimplify/i,
    /\bimprove\s+code/i,
  ],
  unrequested_improvement: [
    /\bimprove/i,
    /\benhance/i,
    /\boptimize/i,
    /\bbetter/i,
    /\bupgrade/i,
    /\bmodernize/i,
  ],
  style_change: [
    /\bformat/i,
    /\blint/i,
    /\bstyle\b/i,
    /\bprettier/i,
    /\bindent/i,
    /\bwhitespace/i,
    /\bspacing/i,
  ],
};
```

**Allowed Side-Effect Files** (L53-L63):
```typescript
const ALLOWED_SIDE_EFFECT_FILES = [
  /package\.json$/,
  /package-lock\.json$/,
  /yarn\.lock$/,
  /pnpm-lock\.yaml$/,
  /tsconfig\.json$/,
  /\.gitignore$/,
  /\.env\.example$/,
  /Cargo\.lock$/,
  /go\.sum$/,
];
```

**Numeric Thresholds:**

- **Working Set Commit Count** (L188): `Math.min(config.workingSetCommitCount, events.length)`
  - Default: 3 (from DEFAULT_INNER_LOOP_CONFIG L347)
  - First N commits define the "normal" working set

- **Large File Change Threshold** (L210): `files.length > 5`
  - Flag refactors touching more than 5 files

- **Scope Explosion - Average Multiplier** (L252): `Math.max(avgFiles * 3, 10)`
  - 3x average files per commit OR at least 10 files

- **Minimum Commits for Explosion Detection** (L238): `events.length < 3`
  - Requires at least 3 commits

**Scoring Formula:**

Total drift commits (L101):
```typescript
const totalDriftCommits = new Set(drifts.map((d) => d.commitHash)).size;
```

Total unauthorized files (L102):
```typescript
const totalUnauthorizedFiles = new Set(drifts.flatMap((d) => d.unauthorizedFiles)).size;
```

Average files per commit (L241-L251):
```typescript
let totalFiles = 0;
const fileCounts: number[] = [];

for (const event of events) {
  const files = filesPerCommit.get(event.hash) || [];
  const nonSideEffectFiles = files.filter((f) => !isAllowedSideEffect(f, config));
  fileCounts.push(nonSideEffectFiles.length);
  totalFiles += nonSideEffectFiles.length;
}

const avgFiles = totalFiles / events.length;
```

**Detection Logic:**

Three detection strategies (L88-L98):
1. **Scope Creep** (`detectScopeCreep`): If explicit session scope provided, check each commit's files against authorized files/dirs
2. **Unrequested Refactors** (`detectUnrequestedRefactors`): Match commit messages against drift patterns, check if touches files outside working set
3. **Scope Explosion** (`detectScopeExplosion`): Calculate average files per commit, flag commits touching 3x average or 10+ files

**File Authorization Check** (L144-L146):
```typescript
const isAuthorized =
  authorizedFiles.has(file) ||
  authorizedDirs.some((dir) => file.startsWith(dir + '/') || file === dir);
```

**Side-Effect File Check** (L281-L288):
```typescript
function isAllowedSideEffect(file: string, config: InnerLoopConfig): boolean {
  // Check config allowed files
  if (config.allowedDriftFiles.some((f) => file.endsWith(f))) {
    return true;
  }

  // Check default patterns
  return ALLOWED_SIDE_EFFECT_FILES.some((p) => p.test(file));
}
```

**Aggregation Logic:**

- Returns top 10 drifts (L113)
- Deduplicates commits and files via Set
- Detected if drifts.length > 0 (L104)
- Message includes drift types and counts (L106-L109)

**Helper Functions:**

- `createSessionScope` (L295-L305): Manual scope declaration
- `inferSessionScope` (L320-L346): Infer scope from first N commits (default 3)

---

### logging-only

**File:** `src/inner-loop/logging-only.ts`

**Purpose:** Detects "Debug Loop Spiral" where AI adds logging/print statements instead of fixing root cause.

**Two Detection Modes:**
1. **Lightweight Inference** (`detectLoggingOnlyCommits`): Fast, sync, infers from commit messages
2. **Full Diff Analysis** (`analyzeCommitsForLogging`): Async, inspects git diffs for accurate counts

**Regex Patterns:**

**Logging Patterns by Language** (L38-L97):
```typescript
const LOGGING_PATTERNS: Record<string, RegExp[]> = {
  javascript: [
    /console\.(log|error|warn|debug|info|trace|dir|table)\s*\(/,
    /console\.(time|timeEnd|timeLog|group|groupEnd)\s*\(/,
    /debugger;/,
  ],
  typescript: [
    /console\.(log|error|warn|debug|info|trace|dir|table)\s*\(/,
    /console\.(time|timeEnd|timeLog|group|groupEnd)\s*\(/,
    /debugger;/,
  ],
  python: [
    /print\s*\(/,
    /logging\.(debug|info|warning|error|critical)\s*\(/,
    /logger\.(debug|info|warning|error|critical)\s*\(/,
    /pprint\s*\(/,
    /breakpoint\s*\(/,
    /import\s+pdb/,
    /pdb\.set_trace\s*\(/,
  ],
  java: [
    /System\.out\.print(ln)?\s*\(/,
    /System\.err\.print(ln)?\s*\(/,
    /logger\.(debug|info|warn|error|trace)\s*\(/,
    /log\.(debug|info|warn|error|trace)\s*\(/,
    /LOG\.(debug|info|warn|error|trace)\s*\(/,
  ],
  go: [
    /fmt\.Print(ln|f)?\s*\(/,
    /log\.Print(ln|f)?\s*\(/,
    /log\.(Debug|Info|Warn|Error|Fatal)(f|ln)?\s*\(/,
  ],
  rust: [
    /println!\s*\(/,
    /eprintln!\s*\(/,
    /dbg!\s*\(/,
    /debug!\s*\(/,
    /info!\s*\(/,
    /warn!\s*\(/,
    /error!\s*\(/,
    /trace!\s*\(/,
  ],
  ruby: [
    /puts\s+/,
    /p\s+/,
    /pp\s+/,
    /Rails\.logger\.(debug|info|warn|error)\s*\(/,
    /logger\.(debug|info|warn|error)\s*\(/,
    /binding\.pry/,
    /byebug/,
  ],
  php: [
    /var_dump\s*\(/,
    /print_r\s*\(/,
    /echo\s+/,
    /error_log\s*\(/,
    /dd\s*\(/,
    /dump\s*\(/,
  ],
};
```

**Aggregated Pattern** (L100):
```typescript
const ALL_LOGGING_PATTERNS = Object.values(LOGGING_PATTERNS).flat();
```

**Debugging Activity Patterns (Inference Mode)** (L136-L148):
```typescript
const debuggingPatterns = [
  /\badd(ed|ing)?\s+(log|debug|print)/i,
  /\blog(ging)?\b/i,
  /\bdebug(ging)?\b/i,
  /\bprint\s+statement/i,
  /\btrace\b/i,
  /\bconsole\b/i,
  /\btemporary\b/i,
  /\btemp\b/i,
  /\bwip\b/i,
  /\binvestigat/i,
  /\bdiagnos/i,
];
```

**Numeric Thresholds:**

- **Max Consecutive Logging Commits** (L184): `maxConsecutive >= cfg.maxConsecutiveLoggingCommits`
  - Default: 3 (from DEFAULT_INNER_LOOP_CONFIG L348)

- **Logging-Only Ratio** (L246): `loggingStatements > 0 && (actualFixes === 0 || loggingStatements / addedLines.length > 0.8)`
  - Logging-only if: no other changes OR logging is >80% of added lines

- **Top Results Limit** (L194): Returns top 10 logging commits

**Scoring Formula:**

Consecutive logging count (L171-L182):
```typescript
let maxConsecutive = 0;
let currentConsecutive = 0;

for (const event of sorted) {
  const isLogging = loggingCommits.some((lc) => lc.hash === event.hash);
  if (isLogging) {
    currentConsecutive++;
    maxConsecutive = Math.max(maxConsecutive, currentConsecutive);
  } else {
    currentConsecutive = 0;
  }
}
```

Total logging statements (diff analysis, L321):
```typescript
const totalLogging = loggingCommits.reduce((sum, c) => sum + c.loggingStatements, 0);
```

Actual fixes count (L242):
```typescript
const actualFixes = addedLines.length - loggingStatements;
```

**Detection Logic:**

**Inference Mode** (`detectLoggingOnlyCommits`, L115-L199):
1. Filter commits matching debugging patterns
2. Mark as logging-only based on message patterns
3. Find longest consecutive run
4. Detected if maxConsecutive >= threshold

**Diff Analysis Mode** (`analyzeCommitsForLogging`, L278-L334):
1. For each commit, get diff with `git show [hash] --format= --unified=0`
2. Extract added lines (start with `+`, not `+++`)
3. Count lines matching logging patterns
4. Calculate actualFixes = addedLines - loggingStatements
5. Determine isLoggingOnly based on 80% ratio
6. Find consecutive runs across all commits

**Single Commit Analysis** (`analyzeCommitForLogging`, L205-L261):
```typescript
// Get diff
const diff = await git.show([commitHash, '--format=', '--unified=0']);

// Filter added lines
const addedLines = diff
  .split('\n')
  .filter((line) => line.startsWith('+') && !line.startsWith('+++'));

// Count logging patterns
let loggingStatements = 0;
for (const line of addedLines) {
  for (const pattern of ALL_LOGGING_PATTERNS) {
    if (pattern.test(line)) {
      loggingStatements++;
      break;
    }
  }
}

// Determine if logging-only
const isLoggingOnly =
  loggingStatements > 0 && (actualFixes === 0 || loggingStatements / addedLines.length > 0.8);
```

**Aggregation Logic:**

- Returns top 10 commits (L194, L329)
- Detected if consecutive count >= threshold (L184, L316)
- Message varies by severity (L186-L190, L320-L325)
- Results include `detectionMode: 'inferred' | 'diff_analysis'`

---

### tests-passing-lie

**File:** `src/inner-loop/tests-passing-lie.ts`

**Purpose:** Detects when AI claims "all tests passing" or "working" but code actually doesn't work. Detected through inferred patterns or actual test execution.

**Regex Patterns:**

**Success Claim Patterns** (L30-L45):
```typescript
const SUCCESS_CLAIM_PATTERNS = [
  // Explicit success claims (not bare "fix" which is just a commit type)
  /\bfixed\s+(it|the|this|that|bug|issue|problem)/i, // "fixed it", "fixed the bug"
  /\bworking\b/i, // "working" - explicit success claim
  /\bdone\b/i, // "done" - explicit completion
  /\bcomplete[ds]?\b/i, // "completed", "complete"
  /\b(bug|issue|problem)\s+resolved\b/i, // "issue resolved" (not bare "resolved")
  /\btests?\s+pass(es|ing)?\b/i, // "tests pass" (not bare "passing")
  /\bgreen\b/i, // "green" - test status
  /\bsuccessful(ly)?\b/i, // "successfully"
  /\ball\s+tests?\b/i, // "all tests"
  /\bready\b/i, // "ready"
  /\bshould\s+work/i, // "should work"
  /\bnow\s+works?\b/i, // "now works"
  /\bit\s+works?\b/i, // "it works"
];
```

**Tentative Patterns (Exclude from Lies)** (L48-L58):
```typescript
const TENTATIVE_PATTERNS = [
  /\btry\b/i,
  /\battempt/i,
  /\bmaybe\b/i,
  /\bwip\b/i,
  /\bwork\s*in\s*progress/i,
  /\bexperiment/i,
  /\btest(ing)?\b/i, // Just "testing" something
  /\bdebug/i,
  /\binvestigat/i,
];
```

**Numeric Thresholds:**

- **Minimum Commits** (L72): `events.length < 2` - requires at least 2 commits

- **Follow-up Window** (L93): 30 minutes
  - Look for fix commits within 30 minutes of success claim

- **Test Command Timeout** (L159): 120000ms (2 minutes)

- **Build Command Timeout** (L188): 300000ms (5 minutes)

- **Top Results Limit** (L133): Returns top 10 lies

**Scoring Formula:**

Lie rate (L127):
```typescript
const lieRate = Math.round((lies.length / events.length) * 100);
```

**Detection Logic:**

**Pattern-Based Detection** (`detectTestsPassingLie`, L64-L137):
1. Sort commits by timestamp
2. For each commit claiming success (not tentative):
   - Get following commits within 30-minute window
   - Filter for fix commits on same files or scope
   - If quick fixes found, flag as lie

**File/Scope Overlap Check** (L96-L108):
```typescript
const commitFiles = filesPerCommit.get(commit.hash) || [];
const quickFixes = followingCommits.filter((fc) => {
  if (fc.type !== 'fix') return false;

  // Check file overlap
  const fcFiles = filesPerCommit.get(fc.hash) || [];
  const hasOverlap = commitFiles.some((f) => fcFiles.includes(f));

  // Or same scope
  const sameScope = commit.scope && fc.scope === commit.scope;

  return hasOverlap || sameScope;
});
```

**Actual Verification** (optional):

`verifyCommit` (L143-L169): Runs test command at commit state
`verifyBuild` (L174-L198): Runs build command at commit state

Default commands (L237-L260):
- Test: `'npm test'`
- Build: `'npm run build'`

**Helper Functions:**

- `claimsToBeSuccessful` (L203-L204): Check message against SUCCESS_CLAIM_PATTERNS
- `isTentativeCommit` (L210-L211): Check message against TENTATIVE_PATTERNS
- `getFollowingCommitsInWindow` (L217-L232): Get commits within time window

**Aggregation Logic:**

- Returns top 10 lies (L133)
- Detected if lies.length > 0 (L124)
- Message includes lie count and lie rate percentage (L126-L129)

---

### Detector Orchestration (index.ts)

**File:** `src/inner-loop/index.ts`

**Purpose:** Aggregates all four detectors, calculates overall health, generates recommendations.

**Main Analysis Function** (`analyzeInnerLoop`, L39-L97):

**Detector Invocation** (L48-L51):
```typescript
const testsPassingLie = detectTestsPassingLie(events, filesPerCommit, cfg);
const contextAmnesia = detectContextAmnesia(events, filesPerCommit, lineStatsPerCommit, cfg);
const instructionDrift = detectInstructionDrift(events, filesPerCommit, cfg);
const loggingOnly = detectLoggingOnlyCommits(events, cfg);
```

**Aggregation Scoring:**

Total issues (L54-L58):
```typescript
const totalIssues =
  testsPassingLie.totalLies +
  contextAmnesia.totalIncidents +
  instructionDrift.totalDriftCommits +
  (loggingOnly.detected ? 1 : 0);
```

Critical issues (L61-L62):
```typescript
const criticalIssues =
  testsPassingLie.totalLies + (contextAmnesia.totalIncidents >= 3 ? 1 : 0);
```
- Tests Passing Lies always critical
- Context Amnesia critical if 3+ incidents

Warning issues (L65-L66):
```typescript
const warningIssues =
  (instructionDrift.detected ? 1 : 0) + (loggingOnly.detected ? 1 : 0);
```

**Overall Health Determination** (L69-L74):
```typescript
let overallHealth: 'healthy' | 'warning' | 'critical' = 'healthy';
if (criticalIssues > 0) {
  overallHealth = 'critical';
} else if (warningIssues > 0 || contextAmnesia.totalIncidents > 0) {
  overallHealth = 'warning';
}
```

**Recommendation Generation** (`generateRecommendations`, L102-L186):

**Per-Detector Recommendations:**

Tests Passing Lie (L111-L118):
- If detected: "STOP: AI claimed success but code needed fixes"
- Suggest running test command after each fix

Context Amnesia (L121-L137):
- Reverts: Check if changes were intentional
- Reimplementation: Break task into smaller pieces
- Forgotten changes: Restart with clear instructions

Instruction Drift (L140-L156):
- Scope creep: Be explicit about file scope
- Unrequested refactor: Add "Do NOT refactor" instruction
- Unrequested improvement: Be explicit about what NOT to do

Debug Loop (L159-L171):
- If detected: "STOP and think about root cause"
- Suggest: read errors, check docs, simplify
- Emergency (5+ consecutive): "git stash, take a break, start fresh"

**Emergency Protocol** (L174-L183):
```typescript
const totalCritical =
  testsPassingLie.totalLies +
  contextAmnesia.totalIncidents +
  (loggingOnly.consecutiveLoggingCount >= 3 ? 1 : 0);

if (totalCritical >= 3) {
  recommendations.unshift(
    '🚨 EMERGENCY PROTOCOL: Multiple inner loop failures detected. STOP → git status → backup → start simple'
  );
}
```

**Quick Check Function** (`quickInnerLoopCheck`, L191-L213):

Returns minimal summary:
```typescript
{
  hasIssues: boolean;
  issueCount: number;
  topIssue: string | null; // 'tests-passing-lie' | 'context-amnesia' | 'instruction-drift' | 'debug-loop'
}
```

**Formatting Function** (`formatInnerLoopAnalysis`, L218-L266):

Produces terminal output with:
- Health emoji (🚨 critical, ⚠️ warning, ✅ healthy)
- Individual pattern messages
- Summary counts (total issues, critical, warning)
- Top 5 recommendations

**Re-exports** (L28-L34):
- All types from `types.ts`
- All four detector functions
- Helper functions (`createSessionScope`, `inferSessionScope`)

---

## Metrics

### flow

**File:** `src/metrics/flow.ts`

**Purpose:** Calculate flow efficiency as percentage of productive time (building vs debugging).

**Formula** (L58):
```typescript
const efficiency = ((activeMinutes - debuggingMinutes) / activeMinutes) * 100;
```

**Input Parameters:**
- `activeMinutes: number` - Total active work time in minutes
- `spirals: FixChain[]` - Detected fix chains (may or may not be spirals)
- `totalFixCommits: number` - Total number of fix commits (optional, default 0)

**Constants:**

**ISOLATED_FIX_MINUTES** (L8):
```typescript
const ISOLATED_FIX_MINUTES = 5;
```
Estimated time per isolated fix commit (not part of spiral). Conservative estimate to avoid over-penalizing normal iteration.

**Debugging Time Calculation** (L42-L56):
```typescript
// Time in detected spirals (3+ consecutive fixes)
const spiralMinutes = spirals
  .filter((s) => s.isSpiral)
  .reduce((sum, s) => sum + s.duration, 0);

// Count fixes that are part of spirals (s.commits is already a count, not an array)
const fixesInSpirals = spirals
  .filter((s) => s.isSpiral)
  .reduce((sum, s) => sum + s.commits, 0);

// Isolated fixes = total fixes - fixes in spirals
const isolatedFixes = Math.max(0, totalFixCommits - fixesInSpirals);
const isolatedFixMinutes = isolatedFixes * ISOLATED_FIX_MINUTES;

// Total debugging time = spiral time + isolated fix time
const debuggingMinutes = spiralMinutes + isolatedFixMinutes;
```

**Normalization Logic** (L59):
```typescript
const clampedEfficiency = Math.max(0, Math.min(100, efficiency));
```
Clamps efficiency to [0, 100] range.

**Output Range:** 0-100% (clamped)

**Rating Thresholds** (L70-L75):
```typescript
function getRating(efficiency: number): Rating {
  if (efficiency > 90) return 'elite';
  if (efficiency >= 75) return 'high';
  if (efficiency >= 50) return 'medium';
  return 'low';
}
```

**Edge Cases:**
- `activeMinutes === 0` (L32-L38): Returns 0 value, 'medium' rating, "Insufficient data" description

**Feeds into aggregate:** Used as one of 5 metrics in overall rating calculation (see index.ts).

---

### rework

**File:** `src/metrics/rework.ts`

**Purpose:** Calculate rework ratio as percentage of fix commits vs total commits.

**Formula** (L23):
```typescript
const ratio = (fixCommits / commits.length) * 100;
```

**Input Parameters:**
- `commits: Commit[]` - Array of all commits

**Fix Commit Count** (L22):
```typescript
const fixCommits = commits.filter((c) => c.type === 'fix').length;
```

**Output Range:** 0-100%

**Rating Thresholds** (L34-L39):
```typescript
function getRating(ratio: number): Rating {
  if (ratio < 30) return 'elite';
  if (ratio < 50) return 'high';
  if (ratio < 70) return 'medium';
  return 'low';
}
```

**Interpretation:**
- Lower ratios = more forward progress
- Higher ratios = more time spent fixing

**Edge Cases:**
- `commits.length === 0` (L13-L19): Returns 0 value, 'medium' rating, "Insufficient data" description

**Feeds into aggregate:** Used as one of 5 metrics in overall rating calculation (see index.ts).

---

### spirals

**File:** `src/metrics/spirals.ts`

**Purpose:** Detect fix chains (consecutive fix commits on same component) and calculate average debug spiral duration.

**Constants:**

**SPIRAL_THRESHOLD** (L4):
```typescript
const SPIRAL_THRESHOLD = 3; // 3+ consecutive fixes = spiral
```

**Pattern Detection Regexes** (L7-L14):
```typescript
const PATTERNS: Record<string, RegExp> = {
  VOLUME_CONFIG: /volume|mount|path|permission|readonly|pvc|storage/i,
  SECRETS_AUTH: /secret|auth|oauth|token|credential|password|key/i,
  API_MISMATCH: /api|version|field|spec|schema|crd|resource/i,
  SSL_TLS: /ssl|tls|cert|fips|handshake|https/i,
  IMAGE_REGISTRY: /image|pull|registry|docker|tag/i,
  GITOPS_DRIFT: /drift|sync|argocd|reconcil|outof/i,
};
```

**Fix Chain Detection** (`detectFixChains`, L16-L57):
1. Sort commits by date ascending (L20)
2. Group consecutive fix commits by component (L26-L49)
3. Create fix chain if 3+ consecutive fixes (L35, L43, L52)
4. Non-fix commits break the chain (L42-L48)

**Component Extraction** (`getComponent`, L59-L72):
```typescript
// Use scope if available
if (commit.scope) {
  return commit.scope.toLowerCase();
}

// Extract first meaningful word from message
const words = commit.message
  .replace(/^fix\s*:?\s*/i, '')
  .split(/\s+/)
  .filter((w) => w.length > 2);

return words[0]?.toLowerCase() || 'unknown';
```

**Fix Chain Creation** (`createFixChain`, L74-L92):
```typescript
const firstCommit = commits[0].date;
const lastCommit = commits[commits.length - 1].date;
const duration = differenceInMinutes(lastCommit, firstCommit);

// Detect pattern from commit messages
const allMessages = commits.map((c) => c.message).join(' ');
const pattern = detectPattern(allMessages);

return {
  component,
  commits: commits.length,
  duration,
  isSpiral: commits.length >= SPIRAL_THRESHOLD,
  pattern,
  firstCommit,
  lastCommit,
};
```

**Average Spiral Duration Formula** (L124-L125):
```typescript
const totalDuration = spirals.reduce((sum, s) => sum + s.duration, 0);
const avgDuration = totalDuration / spirals.length;
```

**Output Range:** 0+ minutes (unbounded)

**Rating Thresholds** (L136-L141):
```typescript
function getRating(duration: number): Rating {
  if (duration < 15) return 'elite';
  if (duration < 30) return 'high';
  if (duration < 60) return 'medium';
  return 'low';
}
```

**Edge Cases:**
- `spirals.length === 0` (L115-L121): Returns 0 value, 'elite' rating, "No debug spirals detected"
  - Note: Unlike other metrics, this returns 'elite' for zero spirals because "no spirals" is a positive result, not "insufficient data"

**Pattern Summary** (`calculatePatternSummary`, L158-L182):
```typescript
const categories: Record<string, number> = {};
let total = 0;
let withTracer = 0;

for (const chain of chains) {
  const pattern = chain.pattern || 'OTHER';
  categories[pattern] = (categories[pattern] || 0) + chain.commits;
  total += chain.commits;

  if (chain.pattern) {
    withTracer += chain.commits;
  }
}

return {
  categories,
  total,
  tracerAvailable: total > 0 ? Math.round((withTracer / total) * 100) : 0,
};
```

**Feeds into aggregate:** Used as one of 5 metrics in overall rating calculation (see index.ts). Also feeds into flow efficiency calculation.

---

### trust

**File:** `src/metrics/trust.ts`

**Purpose:** Calculate trust pass rate as percentage of commits that don't need immediate follow-up fixes.

**Constants:**

**FOLLOWUP_WINDOW_MINUTES** (L4):
```typescript
const FOLLOWUP_WINDOW_MINUTES = 30;
```

**COMPONENT_STOPWORDS** (L10-L81):
```typescript
const COMPONENT_STOPWORDS = new Set([
  // Commit type words
  'fix', 'feat', 'chore', 'docs', 'style', 'test', 'tests', 'refactor',
  // Common verbs
  'add', 'adds', 'added', 'update', 'updates', 'updated',
  'change', 'changes', 'changed', 'remove', 'removes', 'removed',
  'delete', 'deletes', 'deleted', 'improve', 'improves', 'improved',
  'handle', 'handles', 'handling', 'use', 'uses', 'using',
  'make', 'makes', 'making', 'move', 'moves', 'moved',
  'rename', 'renames', 'renamed',
  // Common nouns
  'function', 'functions', 'method', 'methods', 'file', 'files',
  'module', 'modules', 'code', 'error', 'errors', 'issue', 'issues',
  'bug', 'bugs', 'type', 'types',
  // Articles/pronouns
  'the', 'this', 'that', 'for', 'and', 'with', 'from', 'into',
]);
```

**Formula** (L123):
```typescript
const rate = (trustedCommits / commits.length) * 100;
```

**Input Parameters:**
- `commits: Commit[]` - Array of all commits

**Trust Calculation Logic** (L107-L121):
```typescript
for (let i = 0; i < sorted.length; i++) {
  const commit = sorted[i];
  const nextCommit = sorted[i + 1];

  // Check if next commit is a fix to same component within 30 min
  const needsFollowup =
    nextCommit &&
    nextCommit.type === 'fix' &&
    sameComponent(commit, nextCommit) &&
    differenceInMinutes(nextCommit.date, commit.date) < FOLLOWUP_WINDOW_MINUTES;

  if (!needsFollowup) {
    trustedCommits++;
  }
}
```

**Component Matching Heuristics** (`sameComponent`, L146-L171):
1. **Scope match** (L147-L150): If both have scopes, compare them (most reliable)
2. **Scope difference** (L152-L155): If only one has scope, assume different components
3. **Message content** (L158-L170): Extract meaningful words (length > 4, not stopwords), require at least one overlap

```typescript
// Extract meaningful words (not stopwords, length > 4)
const extractMeaningfulWords = (msg: string): string[] =>
  msg
    .toLowerCase()
    .split(/\s+/)
    .slice(0, 5) // Look at first 5 words
    .filter((word) => word.length > 4 && !COMPONENT_STOPWORDS.has(word));

const aWords = new Set(extractMeaningfulWords(a.message));
const bWords = extractMeaningfulWords(b.message);

// Require at least one meaningful word overlap
return bWords.some((word) => aWords.has(word));
```

**Output Range:** 0-100%

**Rating Thresholds** (L173-L178):
```typescript
function getRating(rate: number): Rating {
  if (rate > 95) return 'elite';
  if (rate >= 80) return 'high';
  if (rate >= 60) return 'medium';
  return 'low';
}
```

**Edge Cases:**
- `commits.length === 0` (L93-L99): Returns 0 value, 'medium' rating, "Insufficient data" description

**Feeds into aggregate:** Used as one of 5 metrics in overall rating calculation (see index.ts).

---

### velocity

**File:** `src/metrics/velocity.ts`

**Purpose:** Calculate iteration velocity as commits per active hour.

**Constants:**

**SESSION_GAP_MINUTES** (L8):
```typescript
const SESSION_GAP_MINUTES = 120; // 2 hours = new session
```

**MIN_MINUTES_PER_COMMIT** (L21):
```typescript
const MIN_MINUTES_PER_COMMIT = 10;
```
Rationale: Commits represent visible checkpoints, but work happens between commits. A commit that appears instant (0 minutes from previous) still required time to write code, test, and review. This floor prevents unrealistically high velocities from rapid-fire commits.

**Formula** (L65):
```typescript
const velocity = commits.length / activeHours;
```

**Input Parameters:**
- `commits: Commit[]` - Array of all commits

**Active Hours Calculation** (`calculateActiveHours`, L86-L115):
```typescript
// Sort by date ascending
const sorted = [...commits].sort((a, b) => a.date.getTime() - b.date.getTime());

let totalMinutes = 0;
let sessionStart = sorted[0].date;

for (let i = 1; i < sorted.length; i++) {
  const gap = differenceInMinutes(sorted[i].date, sorted[i - 1].date);

  if (gap > SESSION_GAP_MINUTES) {
    // End current session, start new one
    totalMinutes += differenceInMinutes(sorted[i - 1].date, sessionStart);
    sessionStart = sorted[i].date;
  }
}

// Add final session
totalMinutes += differenceInMinutes(sorted[sorted.length - 1].date, sessionStart);

// Apply minimum time per commit to account for work between commits
const minMinutes = Math.max(totalMinutes, commits.length * MIN_MINUTES_PER_COMMIT);

return minMinutes / 60;
```

**Session Detection Logic:**
- Commits separated by gaps > 120 minutes are in different sessions
- Total active time = sum of session durations
- Floor applied: max(sessionTime, commits * 10 minutes)

**Output Range:** 0+ commits/hour (unbounded)

**Rating Thresholds** (L117-L122):
```typescript
function getRating(velocity: number): Rating {
  if (velocity > 5) return 'elite';
  if (velocity >= 3) return 'high';
  if (velocity >= 1) return 'medium';
  return 'low';
}
```

**Normalization** (L69):
```typescript
value: Math.round(velocity * 10) / 10,
```
Rounds to 1 decimal place.

**Edge Cases:**
- `commits.length === 0` (L35-L41): Returns 0 value, 'medium' rating, "Insufficient data" description
- `commits.length === 1` (L45-L51): Returns 0 value, 'medium' rating, "Single commit - velocity requires 2+ commits to measure"
- `activeHours === 0` (L56-L62): Returns commits.length value, 'high' rating, "All commits in rapid succession"
- `commits.length < 2` in calculateActiveHours (L87-L89): Returns 0.1 minimum to avoid division by zero

**Feeds into aggregate:** Used as one of 5 metrics in overall rating calculation (see index.ts).

---

### Metrics Aggregation (index.ts)

**File:** `src/metrics/index.ts`

**Purpose:** Orchestrate all metric calculations and produce final VibeCheckResult.

**Main Analysis Function** (`analyzeCommits`, L12-L70):

**Metric Invocation** (L30-L38):
```typescript
const iterationVelocity = calculateIterationVelocity(sorted);
const reworkRatio = calculateReworkRatio(sorted);
const trustPassRate = calculateTrustPassRate(sorted);
const debugSpiralDuration = calculateDebugSpiralDuration(fixChains);
const flowEfficiency = calculateFlowEfficiency(
  activeHours * 60,
  fixChains,
  commitCounts.fix
);
```

**Overall Rating Calculation** (`calculateOverallRating`, L104-L119):

**Scoring System** (L105-L110):
```typescript
const scores: Record<Rating, number> = {
  elite: 4,
  high: 3,
  medium: 2,
  low: 1,
};
```

**Average Score Formula** (L112-L113):
```typescript
const avgScore =
  ratings.reduce((sum, r) => sum + scores[r], 0) / ratings.length;
```

**Overall Rating Thresholds** (L115-L118):
```typescript
if (avgScore >= 3.5) return 'ELITE';
if (avgScore >= 2.5) return 'HIGH';
if (avgScore >= 1.5) return 'MEDIUM';
return 'LOW';
```

**Rating Aggregation Logic:**
- Convert each of 5 metric ratings to numeric score (elite=4, high=3, medium=2, low=1)
- Calculate arithmetic mean of scores
- Map average back to OverallRating (ELITE/HIGH/MEDIUM/LOW)

**Weighting:**
- All 5 metrics have equal weight (1/5 each)
- No prioritization or differential weighting

**Individual Metric Contributions** (L44-L50):
```typescript
const overall = calculateOverallRating([
  iterationVelocity.rating,
  reworkRatio.rating,
  trustPassRate.rating,
  debugSpiralDuration.rating,
  flowEfficiency.rating,
]);
```

**Empty Result** (`emptyResult`, L126-L181):
When `commits.length === 0`, all metrics return:
- `value: 0`
- `rating: 'medium'`
- `description: 'Insufficient data - no commits to analyze'`
- Overall rating: `'MEDIUM'`

Note: Exception is debugSpiralDuration in real analysis which returns 'elite' for zero spirals (positive result vs. insufficient data).

**Commit Type Counting** (`countCommitTypes`, L72-L102):
```typescript
const counts = {
  total: commits.length,
  feat: 0,
  fix: 0,
  docs: 0,
  tracer: 0,
  other: 0,
};

for (const commit of commits) {
  switch (commit.type) {
    case 'feat':
      counts.feat++;
      break;
    case 'fix':
      counts.fix++;
      break;
    case 'docs':
      counts.docs++;
      break;
    case 'tracer':
      counts.tracer++;
      break;
    default:
      counts.other++;
  }
}
```

**Re-exports** (L183):
```typescript
export { calculateActiveHours } from './velocity.js';
```

---

## Metric Interdependencies

**Flow Efficiency depends on:**
- Spiral detection (from spirals.ts)
- Total fix commit count (from commit type counting)
- Active hours calculation (from velocity.ts)

**Overall Rating depends on:**
- All 5 individual metric ratings (equal weight)

**Pattern Summary depends on:**
- Fix chains (from spiral detection)

**No circular dependencies** - metrics can be calculated in any order after fix chain detection.

## Test Cases and Fixtures

### Inner-Loop Tests (tests/inner-loop.test.ts)

#### Test Structure
5 describe blocks, 20 test cases total:
- `detectTestsPassingLie` (7 tests, L21-146)
- `detectContextAmnesia` (4 tests, L148-241)
- `detectInstructionDrift` (3 tests, L243-314)
- `detectLoggingOnlyCommits` (3 tests, L316-356)
- `analyzeInnerLoop` (3 tests, L358-440)

#### Mock Data Helper (L443-463)
```typescript
function makeEvent(hash, timestamp, type, scope, subject): TimelineEvent
```
Hardcoded: author="Test User", sessionId="test-session", gapMinutes=0, spiralDepth=0

#### Tests Passing Lie (7 tests)
| Test | Input | Expected | Edge Case |
|------|-------|----------|-----------|
| detects claim + immediate fix | 2 fix commits, same file, 15min apart, first says "working" | detected: true, totalLies > 0 | Core pattern |
| ignores tentative (WIP/try/experiment) | WIP commit + fix | NOT flagged | Tentative exemption |
| different files = no lie | 2 fix commits, different files | detected: false | File scope |
| bare "fix:" not flagged | 3 descriptive fix commits | detected: false, totalLies: 0 | Conventional != claim |
| flags "working", "done", "it works" | "auth done" + "forgot edge case" | detected: true | Success word list |
| "passing data" != "tests pass" | "passing data to handler" | detected: false | Verb vs noun |
| "fixed it"/"fixed the bug" | "fixed the bug" + "oops missed" | detected: true | Past-tense |

#### Context Amnesia (4 tests)
| Test | Input | Expected | Edge Case |
|------|-------|----------|-----------|
| detects explicit revert | feat(+50) → revert(-50) same file | detected: true, type: 'revert' | Revert keyword |
| detects reimplementation | chore(-50) → feat(+60) same file, 45min | detected: true, type: 'reimplementation' | Delete-recreate |
| detects repeated fixes | 3 fixes same scope, "null user", 20min intervals | totalIncidents >= 0 | Repetitive fix |
| healthy baseline | 2 feats, different files, 1hr apart | detected: false | No patterns |

#### Instruction Drift (3 tests)
| Test | Input | Expected | Edge Case |
|------|-------|----------|-----------|
| unrequested refactor | feat(1 file) → refactor(6 files) → feat(1 file) | detected: true, type: 'unrequested_refactor' | 6+ files threshold |
| scope explosion | 5×1-file commits → 1×30-file commit | detected: true, type: 'scope_creep' | max(3*avg, 10) |
| config exemption | feat(1 file) → chore(package.json + lock) | No drift | Config files OK |

#### Logging Only (3 tests)
| Test | Input | Expected | Edge Case |
|------|-------|----------|-----------|
| detects logging keywords | 3 fixes: "debug logging", "console.log", "temp debug" | detected: true, consecutive >= 3 | Core pattern |
| consecutive count | 3 logging + 1 feature | consecutive: 3, total: 3 | Count tracking |
| healthy baseline | feat, feat, test | detected: false | No logging |

#### analyzeInnerLoop (3 tests)
| Test | Input | Expected | Edge Case |
|------|-------|----------|-----------|
| multi-detector aggregation | "working" claim + fix + 2 logging commits | totalIssues > 0, recommendations.length > 0 | Aggregation |
| healthy session | feat, feat, test | overallHealth: 'healthy', issues: 0 | Baseline |
| critical health | repeated claims + immediate fixes | overallHealth in ['warning', 'critical'] | Threshold |

### CLI Integration Tests (tests/cli.integration.test.ts, 93 LOC)
- 8 test cases (4 FAILING due to stale `--since "1 month ago"` on Dec 2025 data)
- Tests: smoke, JSON output, markdown, file output, --simple, --help, --version, non-git error
- Self-testing pattern: runs against own repo with `node dist/cli.js`

### Boundary Gaps
- No multi-session detection tests
- No language-specific logging pattern tests (despite 9+ language support)
- No health scoring threshold transition tests
- No invalid input / conflicting flag tests
- 4 failing integration tests from stale date assumptions
