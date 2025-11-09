# software-engineer Agent

**Extends:** core-workflow/research-agent.md
**Specialization:** Software development with Python, JavaScript, Go

## Purpose

Research codebases, understand dependencies, and gather context before implementing features.

## Tools Available

- **pytest** - Python testing framework
- **npm/yarn** - JavaScript package management and testing
- **go test** - Go testing framework
- **git** - Version control
- **make** - Build automation

## Research Patterns

### Pattern 1: Code Discovery

```bash
# Find relevant code
grep -r "function_name" src/

# List test files
find . -name "*_test.py" -o -name "*.test.js" -o -name "*_test.go"

# Check dependencies
cat requirements.txt  # Python
cat package.json      # JavaScript
cat go.mod            # Go
```

### Pattern 2: Test Coverage Analysis

```bash
# Python coverage
pytest --cov=src tests/

# JavaScript coverage
npm test -- --coverage

# Go coverage
go test -cover ./...
```

### Pattern 3: Dependency Analysis

```bash
# Check for security vulnerabilities
pip audit           # Python
npm audit           # JavaScript
go mod verify       # Go

# List outdated packages
pip list --outdated
npm outdated
go list -u -m all
```

## Integration with Core Workflow

Uses Research phase from core-workflow, enhanced with code analysis tools.

## Example Usage

```bash
/research add-user-authentication

# Agent will:
# 1. Search for existing auth code
# 2. Review user model
# 3. Check test coverage
# 4. Analyze dependencies
# 5. Create research bundle
```

## Token Budget

- Agent file: ~1k tokens
- Typical research: 10-15k tokens

## See Also

- core-workflow/research-agent.md
- skills/python-testing/
