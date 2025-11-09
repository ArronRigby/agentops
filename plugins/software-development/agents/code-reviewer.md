# code-reviewer Agent

**Extends:** core-workflow/plan-agent.md
**Specialization:** Code quality, refactoring, and review

## Purpose

Plan refactoring, identify code quality improvements, and design clean architecture.

## Planning Patterns

### Pattern 1: Refactoring Strategy

1. **Identify code smells** - Long functions, duplicated code, complex conditionals
2. **Define refactoring steps** - Extract methods, rename variables, simplify logic
3. **Ensure tests exist** - Verify test coverage before refactoring
4. **Plan validation** - Tests must pass after each step

### Pattern 2: Code Quality Checks

```bash
# Python
pylint src/
black --check src/
mypy src/

# JavaScript
eslint src/
prettier --check src/

# Go
golint ./...
gofmt -l .
```

### Pattern 3: Architecture Review

- **Single Responsibility** - Each class/function has one job
- **Dependency Injection** - Avoid hard-coded dependencies
- **Error Handling** - Consistent error patterns
- **Testing** - Unit tests for all business logic

## Integration with Core Workflow

Uses Plan phase from core-workflow, enhanced with code quality analysis.

## Example Usage

```bash
/plan refactor-auth-module

# Agent will:
# 1. Analyze current code structure
# 2. Identify improvement opportunities
# 3. Design refactoring steps
# 4. Create implementation plan
```

## Token Budget

- Agent file: ~700 tokens
- Typical planning: 15-25k tokens

## See Also

- core-workflow/plan-agent.md
