# /rollback - Rollback Kubernetes Deployment

Rollback failed deployment to previous stable version.

## Usage

```bash
/rollback <resource> [options]

# Examples:
/rollback myapp
/rollback webapp --namespace staging
/rollback redis --to-revision 5
```

## Workflow

### Phase 1: Identify Issue
- Check pod status
- Review error logs
- Analyze metrics (error rate, response time)
- Determine root cause

### Phase 2: Decide Rollback
- Severity assessment
- Impact analysis
- Rollback vs hotfix decision

### Phase 3: Execute Rollback
- Helm: `helm rollback <release>`
- Kubectl: `kubectl rollout undo deployment/<name>`
- ArgoCD: `argocd app rollback <app>`

### Phase 4: Verify
- Check pod health
- Verify application working
- Run smoke tests
- Document incident

## Rollback Methods

**Helm Rollback** - For Helm-managed applications
**Kubectl Rollback** - For kubectl-managed deployments
**ArgoCD Rollback** - For GitOps-managed applications

## Options

- `--namespace <ns>` - Target namespace (default: default)
- `--to-revision <n>` - Specific revision to rollback to
- `--dry-run` - Preview rollback without executing

## See Also

- agents/deployment-engineer.md - Rollback procedures
- commands/deploy-app.md - Deployment workflows
