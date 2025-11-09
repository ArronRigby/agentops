# devops-operations Plugin

DevOps and platform engineering extension for Kubernetes, Helm, ArgoCD, and CI/CD automation.

## Installation

```bash
# Install core-workflow first (required dependency)
/plugin install core-workflow@agentops

# Then install devops-operations
/plugin install devops-operations@agentops
```

## What You Get

- **3 specialized agents** (devops-engineer, cicd-specialist, deployment-engineer)
- **3 slash commands** (/deploy-app, /setup-pipeline, /rollback)
- **3 skills** (kubernetes-manifests, helm-charts, gitops-patterns)
- **Token budget:** 7,000 tokens (3.5%)

## Quick Start

```bash
# Deploy application
/deploy-app myapp

# Setup CI/CD pipeline
/setup-pipeline myapp

# Rollback failed deployment
/rollback myapp
```

## Components

### Agents

**devops-engineer.md** - Research Kubernetes infrastructure
- Discover existing resources (kubectl, helm, argocd)
- Analyze current state
- Create research bundles

**cicd-specialist.md** - Plan CI/CD pipelines
- Design pipeline stages
- Define test strategy
- Select deployment approach

**deployment-engineer.md** - Execute Kubernetes deployments
- Deploy with validation gates
- Monitor rollout health
- Rollback on failure

### Commands

**/deploy-app** - Deploy application to Kubernetes
- Helm or kubectl deployment
- Validation gates
- Health checks

**/setup-pipeline** - Configure CI/CD pipeline
- GitLab CI or GitHub Actions
- Test automation
- Security scanning

**/rollback** - Rollback failed deployment
- Helm/kubectl/ArgoCD rollback
- Verify health after rollback
- Document incident

### Skills (Progressive Disclosure)

**kubernetes-manifests/** - Common K8s patterns
- Deployments, Services, ConfigMaps
- StatefulSets, Secrets
- Health checks and resource limits

**helm-charts/** - Helm chart templates
- Chart structure
- values.yaml patterns
- Template helpers

**gitops-patterns/** - ArgoCD/Flux patterns
- Application definitions
- Sync policies
- Progressive delivery

## Integration with Core Workflow

This plugin extends core-workflow's Research → Plan → Implement workflow with DevOps-specific tools and patterns.

**Example:** Deploying Redis Cluster
```bash
# Phase 1: Research
/research deploy-redis-cluster
# Uses: devops-engineer agent
# Outputs: Research bundle with current state

# Phase 2: Plan
/plan redis-cluster-research
# Uses: cicd-specialist agent
# Outputs: Deployment plan with validation strategy

# Phase 3: Implement
/implement redis-cluster-plan
# Uses: deployment-engineer agent
# Outputs: Deployed cluster with metrics

# Phase 4: Learn
/learn
# Extracts: Reusable Redis deployment pattern
```

## Tools Required

- kubectl - Kubernetes CLI
- helm - Kubernetes package manager
- argocd - GitOps CD (optional)
- make - Build automation
- Docker/Podman - Container operations

## Factor Compliance

- **Factor II (JIT Context):** Progressive disclosure skills
- **Factor III (Single-Responsibility):** Each agent has one job
- **Factor IV (Validation Gates):** Pre/during/post deployment validation
- **Factor V (Operational Telemetry):** Deployment metrics tracking
- **Factor XII (Domain Portability):** Works across K8s distributions

## Token Budget

**Total plugin:** ~7,000 tokens (3.5%)
- Agents: ~5,500 tokens
- Commands: ~1,000 tokens
- Skills: ~3,000 tokens (loaded on-demand)

**With core-workflow:** 15,000 tokens total (7.5%)
Leaves 92.5% headroom for actual work.

## Documentation

Full documentation at [12-factor-agentops](https://github.com/boshu2/12-factor-agentops)

## License

Apache-2.0
