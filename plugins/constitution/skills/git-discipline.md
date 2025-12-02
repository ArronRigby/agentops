---
name: git-discipline
description: Semantic commits, Knowledge OS patterns, and git workflow discipline. Use to ensure commits capture knowledge for future agents.
---

# git-discipline Skill

**Purpose:** Use git as institutional memory through disciplined commits and workflows.

---

## Git as Knowledge OS

### Commits = Memory Writes

Every commit captures:
- **What** changed (the diff)
- **Why** it changed (commit message)
- **When** it changed (timestamp)
- **Who** changed it (author)

### Branches = Process Isolation

Parallel work without interference:
```bash
git checkout -b feature/auth-refresh
# Work independently
# Merge when ready
```

### Hooks = Kernel Interrupts

Enforce rules automatically:
- `pre-commit` - Validate before commit
- `commit-msg` - Ensure message format
- `post-commit` - Update state

### Logs = Audit Trail

Complete history:
```bash
git log                    # What happened
git blame src/auth.ts      # Who wrote what
git bisect                 # Find when bug introduced
```

---

## Semantic Commit Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

| Type | Use For | Example |
|------|---------|---------|
| `feat` | New feature | `feat(auth): add refresh tokens` |
| `fix` | Bug fix | `fix(api): handle null response` |
| `docs` | Documentation | `docs(readme): add setup instructions` |
| `refactor` | Code restructure | `refactor(auth): extract middleware` |
| `test` | Tests | `test(auth): add refresh token tests` |
| `chore` | Maintenance | `chore(deps): update dependencies` |

### Scopes

Common scopes:
- `auth`, `api`, `ui`, `db`
- `docs`, `tests`, `ci`
- File or module name

### Subject Line

- Imperative mood ("add" not "added")
- No period at end
- Max 72 characters
- Lowercase

---

## Full Commit Format (Law 3)

```
<type>(<scope>): <subject>

Context: [Why was this needed? What problem does it solve?]
Solution: [What was created/changed? How does it work?]
Learning: [What pattern was applied? What was discovered?]
Impact: [What value is delivered? Who benefits?]

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

### Example

```
feat(auth): add refresh token rotation

Context: Users were getting logged out every 24 hours due to JWT expiry.
This caused frustration and support tickets.

Solution: Implemented refresh token rotation using Redis for storage.
Tokens rotate on each use, old tokens are immediately invalidated.
TTL matches JWT expiry for automatic cleanup.

Learning: Redis TTL is perfect for token lifecycle management.
The pattern can be reused for other ephemeral tokens (password reset, etc).

Impact: Users stay logged in indefinitely while maintaining security.
Expected 90% reduction in auth-related support tickets.

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

---

## Branch Workflow

### Feature Branches

```bash
# Create from main
git checkout main
git pull
git checkout -b feature/description

# Work, commit frequently
git add .
git commit -m "feat(scope): description"

# Push when ready
git push -u origin feature/description
```

### Branch Naming

| Prefix | Use For |
|--------|---------|
| `feature/` | New features |
| `fix/` | Bug fixes |
| `docs/` | Documentation |
| `refactor/` | Code restructure |
| `experiment/` | Experimental work |

---

## Validation Before Commit

### Quick Validation

```bash
# Run before every commit (5 seconds)
make quick  # Or: npm run lint

# Catches:
# - Syntax errors
# - Linting issues
# - Type errors
```

### Full Validation

```bash
# Run before push (30 seconds)
make ci-all  # Or: npm test

# Catches:
# - Test failures
# - Integration issues
# - Build errors
```

---

## Commit Frequency

### Too Infrequent

```bash
# Bad: One massive commit
git commit -m "feat: add entire auth system"
# 50 files changed, 3000 insertions
```

**Problems:**
- Hard to review
- Hard to revert
- Loses intermediate context

### Just Right

```bash
# Good: Logical units
git commit -m "feat(auth): add user model"
git commit -m "feat(auth): add JWT middleware"
git commit -m "feat(auth): add login endpoint"
git commit -m "test(auth): add middleware tests"
```

**Benefits:**
- Easy to review
- Easy to revert
- Captures decision journey

### Guideline

Commit after each:
- Logical unit of work
- Passing test
- Working state

---

## Amending vs New Commit

### When to Amend

```bash
# Fixing typo in last commit
git commit --amend

# Adding forgotten file to last commit
git add forgotten-file.ts
git commit --amend --no-edit
```

**Only if:**
- Not yet pushed
- Same logical change
- You authored the commit

### When NOT to Amend

- After push
- Different logical change
- Someone else's commit
- Adding new functionality

---

## Hook Discipline (Law 4)

### Pre-Commit Hook

Runs before commit:
```bash
# .git/hooks/pre-commit
npm run lint
npm run type-check
```

### Post-Commit Hook

Runs after commit:
```bash
# .git/hooks/post-commit
# May generate session logs, metrics
```

### After Push

Check for hook modifications:
```bash
git status

# If modified files:
# ❌ Do NOT commit them
# ✅ They're auto-generated (normal)
```

---

## Git Safety

### Never Do

```bash
# Force push to main
git push --force origin main  # ❌

# Hard reset shared branch
git reset --hard HEAD~5       # ❌ if pushed

# Skip hooks without reason
git commit --no-verify        # ❌ generally
```

### Always Do

```bash
# Pull before push
git pull --rebase origin main

# Check status before commit
git status

# Review diff before commit
git diff --staged
```

---

## Searching History

### Find When Something Changed

```bash
# Search commit messages
git log --grep="auth"

# Search code changes
git log -p -S "refreshToken"

# Find who changed a line
git blame src/auth/middleware.ts
```

### Find When Bug Introduced

```bash
# Binary search through history
git bisect start
git bisect bad HEAD
git bisect good v1.0.0
# Git checks out commits, you test
git bisect good  # or bad
# Repeat until found
```
