# software-development Plugin

Software development extension for Python, JavaScript, Go with testing and code quality.

## Installation

```bash
# Install core-workflow first (required dependency)
/plugin install core-workflow@agentops

# Then install software-development
/plugin install software-development@agentops
```

## What You Get

- **3 specialized agents** (software-engineer, code-reviewer, test-engineer)
- **3 slash commands** (/create-feature, /refactor-code, /add-tests)
- **3 skills** (python-testing, javascript-patterns, go-best-practices)
- **Token budget:** 4,000 tokens (2%)

## Quick Start

```bash
# Create new feature with TDD
/create-feature user-authentication

# Refactor existing code
/refactor-code src/auth/

# Add tests to improve coverage
/add-tests src/utils.py
```

## Components

### Agents

**software-engineer.md** - Research codebases
- Code discovery and analysis
- Dependency review
- Test coverage analysis

**code-reviewer.md** - Plan refactoring and improvements
- Identify code quality issues
- Design refactoring strategy
- Architecture review

**test-engineer.md** - Implement with TDD
- Test-driven development workflow
- Unit, integration, E2E tests
- Coverage tracking

### Commands

**/create-feature** - Build new feature with TDD
**/refactor-code** - Refactor safely with tests
**/add-tests** - Improve test coverage

### Skills (Progressive Disclosure)

**python-testing/** - pytest patterns and fixtures
**javascript-patterns/** - Modern ES6+, React, testing
**go-best-practices/** - Idiomatic Go, concurrency

## Integration with Core Workflow

Extends core-workflow's Research → Plan → Implement workflow with software development best practices.

## Tools Required

- Python: pytest, pylint, black, mypy
- JavaScript: npm/yarn, eslint, prettier
- Go: go test, golint, gofmt

## Token Budget

**Total:** ~4,000 tokens (2%)
- Agents: ~2,400 tokens
- Commands: ~300 tokens
- Skills: ~1,300 tokens (loaded on-demand)

**With core-workflow:** 12,000 tokens (6%)

## Documentation

Full documentation at [12-factor-agentops](https://github.com/boshu2/12-factor-agentops)

## License

Apache-2.0
