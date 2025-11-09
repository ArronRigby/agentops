# /deploy-app - Deploy Application to Kubernetes

Deploy Kubernetes application using Helm or kubectl with validation gates.

## Usage

```bash
/deploy-app <app-name> [options]

# Examples:
/deploy-app redis-cluster
/deploy-app myapp --namespace staging
/deploy-app webapp --values custom-values.yaml
```

## Workflow

### Phase 1: Research
- Check current deployment state
- Review resource quotas
- Identify dependencies (ConfigMaps, Secrets, PVCs)

### Phase 2: Plan
- Design deployment strategy (rolling/blue-green/canary)
- Define validation gates
- Create rollback procedure

### Phase 3: Implement
- Validate YAML syntax and schema
- Apply deployment (helm/kubectl)
- Monitor rollout status
- Check pod health
- Run integration tests

### Phase 4: Verify
- Confirm pods running
- Check application health endpoint
- Verify no errors in logs
- Run smoke tests

## Options

- `--namespace <ns>` - Target namespace (default: default)
- `--values <file>` - Custom values file for Helm
- `--dry-run` - Preview changes without applying
- `--wait` - Wait for rollout to complete (default: true)
- `--timeout <duration>` - Rollout timeout (default: 5m)

## See Also

- agents/deployment-engineer.md - Implementation patterns
- commands/rollback.md - Rollback procedures
