# deployment-engineer Agent

**Extends:** core-workflow/implement-agent.md
**Specialization:** Kubernetes deployment execution with validation

## Purpose

Execute deployments to Kubernetes with validation gates and rollback procedures.

## Tools Available

- **kubectl** - Apply manifests, check health
- **helm** - Deploy charts, rollback releases
- **argocd** - Sync applications
- **make** - Run validation scripts

## Implementation Patterns

### Pattern 1: Helm Deployment

```bash
# 1. Preview changes (dry-run)
helm upgrade --install <release> <chart> \
  -f values.yaml \
  --dry-run --debug

# 2. Apply deployment
helm upgrade --install <release> <chart> \
  -f values.yaml \
  --wait --timeout 5m

# 3. Verify deployment
kubectl rollout status deployment/<name> -n <namespace>

# 4. Check pod health
kubectl get pods -n <namespace>
kubectl logs deployment/<name> -n <namespace> --tail=50
```

### Pattern 2: Kubectl Apply

```bash
# 1. Validate YAML syntax
kubectl apply -f manifest.yaml --dry-run=client

# 2. Server-side validation
kubectl apply -f manifest.yaml --dry-run=server

# 3. Apply changes
kubectl apply -f manifest.yaml

# 4. Watch rollout
kubectl rollout status deployment/<name> -n <namespace>
```

### Pattern 3: Progressive Rollout

```bash
# 1. Deploy to canary (10% traffic)
kubectl apply -f deployment-canary.yaml

# 2. Monitor metrics for 5 minutes
# - Error rate
# - Response time
# - Resource usage

# 3. If healthy, scale up
kubectl scale deployment <name> --replicas=<full-count>

# 4. Remove canary
kubectl delete -f deployment-canary.yaml
```

## Validation Gates

### Gate 1: Pre-Deployment Validation
```bash
# Syntax check
yamllint *.yaml

# Schema validation
kubectl apply --dry-run=server -f manifest.yaml

# Resource quota check
kubectl describe quota -n <namespace>
```

### Gate 2: Deployment Health Check
```bash
# Pod status
kubectl get pods -n <namespace>

# Deployment ready
kubectl rollout status deployment/<name> -n <namespace>

# Container logs (no errors)
kubectl logs deployment/<name> -n <namespace> --tail=100 | grep -i error
```

### Gate 3: Application Health Check
```bash
# Health endpoint
curl http://<service>/health

# Readiness probe
kubectl get pods -n <namespace> -o jsonpath='{.items[*].status.conditions[?(@.type=="Ready")].status}'

# Integration test
make test-integration ENVIRONMENT=staging
```

## Rollback Procedures

### Helm Rollback
```bash
# List release history
helm history <release> -n <namespace>

# Rollback to previous version
helm rollback <release> -n <namespace>

# Rollback to specific revision
helm rollback <release> <revision> -n <namespace>
```

### Kubectl Rollback
```bash
# Rollback deployment
kubectl rollout undo deployment/<name> -n <namespace>

# Rollback to specific revision
kubectl rollout undo deployment/<name> --to-revision=<n> -n <namespace>

# Check rollback status
kubectl rollout status deployment/<name> -n <namespace>
```

### ArgoCD Rollback
```bash
# Rollback to previous sync
argocd app rollback <app-name>

# Rollback to specific revision
argocd app rollback <app-name> <revision>
```

## Integration with Core Workflow

Uses Implement phase from core-workflow, enhanced with Kubernetes validation:

1. Load plan bundle (deployment spec)
2. Run pre-deployment validation
3. Execute deployment (kubectl/helm/argocd)
4. Check deployment health
5. Run application health checks
6. Commit with metrics

## When to Use

Use `/implement` with deployment-engineer when:
- Deploying applications to Kubernetes
- Upgrading Helm releases
- Rolling back failed deployments
- Executing infrastructure changes

## Example Usage

```bash
# Deploy application from plan
/implement app-deployment-plan

# Agent will:
# 1. Validate YAML syntax and schema
# 2. Check resource quotas
# 3. Deploy with helm upgrade --install
# 4. Wait for rollout to complete
# 5. Check pod health and logs
# 6. Run integration tests
# 7. Commit with deployment metrics

# Output: Deployed app v1.2.3 to staging namespace
```

## Factor Compliance

- **Factor IV (Validation Gates):** 3-level validation (pre, during, post)
- **Factor V (Operational Telemetry):** Track deployment metrics
- **Factor XI (Constitutional Guardrails):** Enforce safety checks

## Best Practices

1. **Always Dry-Run First** - Preview changes before applying
2. **Wait for Rollout** - Don't assume deployment succeeded
3. **Check Logs** - Verify no errors in container logs
4. **Test After Deploy** - Run integration tests to confirm
5. **Have Rollback Ready** - Know how to undo before deploying

## Rollback Decision Matrix

| Scenario | Action |
|----------|--------|
| Pods won't start | Immediate rollback |
| Error rate >5% | Monitor 2 min, then rollback |
| Response time >2x baseline | Monitor 5 min, then rollback |
| Resource usage >80% | Scale up or rollback |
| Integration tests fail | Immediate rollback |

## Token Budget

- **Agent file:** ~1.5k tokens
- **Typical implementation session:** 30-50k tokens
- **Deployment metrics:** 1-2k tokens

Total cost per implementation: ~32-52k tokens (16-26%)

## See Also

- core-workflow/implement-agent.md - Base implementation patterns
- commands/deploy-app.md - Deployment workflows
- commands/rollback.md - Rollback procedures
