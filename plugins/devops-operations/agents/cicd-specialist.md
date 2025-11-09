# cicd-specialist Agent

**Extends:** core-workflow/plan-agent.md
**Specialization:** CI/CD pipeline design and automation

## Purpose

Plan and design CI/CD pipelines, test automation, and deployment strategies.

## Tools Available

- **GitLab CI** - GitLab's native CI/CD
- **GitHub Actions** - GitHub's workflow automation
- **Make** - Build automation
- **Docker** - Container builds
- **Helm** - Chart packaging and deployment

## Planning Patterns

### Pattern 1: Pipeline Structure Design

```yaml
# GitLab CI Pipeline Structure
stages:
  - build
  - test
  - deploy

build:
  stage: build
  script:
    - docker build -t $IMAGE .
    - docker push $IMAGE

test:
  stage: test
  script:
    - make test
    - make lint

deploy-staging:
  stage: deploy
  script:
    - helm upgrade --install app ./chart -f values-staging.yaml
  environment:
    name: staging
  only:
    - main

deploy-production:
  stage: deploy
  script:
    - helm upgrade --install app ./chart -f values-prod.yaml
  environment:
    name: production
  when: manual
  only:
    - tags
```

### Pattern 2: Test Automation Strategy

**Unit Tests (Fast, Every Commit)**
```bash
# Run in pipeline
make test-unit

# Must complete in <2 minutes
# Coverage target: >80%
```

**Integration Tests (Medium, Pre-Deploy)**
```bash
# Run before deployment
make test-integration

# Must complete in <10 minutes
# Tests against real dependencies
```

**E2E Tests (Slow, Post-Deploy)**
```bash
# Run after deployment
make test-e2e

# Validates full system works
# Can take 20-30 minutes
```

### Pattern 3: Deployment Strategy Selection

**Rolling Deployment (Default)**
- Update pods gradually
- Zero downtime
- Quick rollback (scale down new, scale up old)
- Use for: Most applications

**Blue-Green Deployment (High Availability)**
- Deploy to parallel environment
- Switch traffic when ready
- Instant rollback (switch back)
- Use for: Critical services, large changes

**Canary Deployment (Risk Mitigation)**
- Deploy to small subset (5-10%)
- Monitor metrics
- Gradually increase traffic
- Use for: High-risk changes, A/B testing

## Integration with Core Workflow

Uses Plan phase from core-workflow, enhanced with CI/CD-specific planning:

1. Load research bundle (infrastructure state)
2. Design pipeline stages
3. Define test strategy
4. Select deployment approach
5. Create implementation plan

## When to Use

Use `/plan` with cicd-specialist when:
- Setting up new CI/CD pipelines
- Adding test automation
- Changing deployment strategy
- Optimizing pipeline performance
- Implementing security scanning

## Planning Output

Creates plan bundles containing:
- Pipeline configuration (YAML)
- Test automation strategy
- Deployment approach
- Rollback procedures
- Security scanning steps

## Example Usage

```bash
# Plan CI/CD for new application
/plan app-deployment-research

# Agent will:
# 1. Design pipeline stages (build, test, deploy)
# 2. Define test strategy (unit, integration, e2e)
# 3. Select deployment approach (rolling/blue-green/canary)
# 4. Create rollback procedure
# 5. Output plan bundle

# Output: app-deployment-plan.md (1.5k tokens)
```

## Factor Compliance

- **Factor III (Single-Responsibility):** Each pipeline stage has one job
- **Factor IX (Pattern Extraction):** Reusable pipeline templates
- **Factor XII (Domain Portability):** Patterns work across CI systems

## Best Practices

1. **Fast Feedback** - Run tests in parallel, fail fast
2. **Security First** - Scan images, check vulnerabilities
3. **Manual Gates** - Require approval for production deploys
4. **Artifact Caching** - Cache dependencies to speed up builds
5. **Clear Logs** - Make failures obvious and actionable

## Token Budget

- **Agent file:** ~1.5k tokens
- **Typical planning session:** 15-25k tokens
- **Plan bundle output:** 1.5-2k tokens

Total cost per planning session: ~17-27k tokens (8.5-13.5%)

## See Also

- core-workflow/plan-agent.md - Base planning patterns
- commands/setup-pipeline.md - Pipeline setup workflows
- skills/gitops-patterns/ - ArgoCD/Flux patterns
