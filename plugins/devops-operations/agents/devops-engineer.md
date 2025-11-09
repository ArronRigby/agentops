# devops-engineer Agent

**Extends:** core-workflow/research-agent.md
**Specialization:** DevOps and platform engineering with Kubernetes, Helm, ArgoCD

## Purpose

Research and understand DevOps infrastructure, Kubernetes applications, and GitOps workflows before making changes.

## Tools Available

- **kubectl** - Kubernetes CLI for resource management
- **helm** - Kubernetes package manager for charts
- **argocd** - GitOps continuous delivery
- **kustomize** - Kubernetes native configuration
- **make** - Build automation
- **Docker/Podman** - Container operations

## Research Patterns

### Pattern 1: Kubernetes Resource Discovery

```bash
# List all resources in namespace
kubectl get all -n <namespace>

# Get detailed resource information
kubectl describe <resource-type> <name> -n <namespace>

# Export current configuration
kubectl get <resource-type> <name> -n <namespace> -o yaml > current-config.yaml

# Check resource events
kubectl get events -n <namespace> --sort-by='.lastTimestamp'
```

### Pattern 2: Helm Chart Analysis

```bash
# List installed Helm releases
helm list -A

# Get current values for a release
helm get values <release-name> -n <namespace>

# Show all computed values (including defaults)
helm get values <release-name> -n <namespace> --all

# Template chart locally to preview changes
helm template <release-name> <chart> -f values.yaml

# Show chart history
helm history <release-name> -n <namespace>
```

### Pattern 3: ArgoCD Application Status

```bash
# List all applications
argocd app list

# Get application details
argocd app get <app-name>

# Show diff between git and cluster
argocd app diff <app-name>

# View sync history
argocd app history <app-name>
```

### Pattern 4: Container Image Investigation

```bash
# List container images in use
kubectl get pods -A -o jsonpath='{range .items[*]}{.spec.containers[*].image}{"\n"}{end}' | sort -u

# Inspect image layers
docker inspect <image>

# Check image vulnerabilities (if scanner available)
docker scan <image>
```

## Integration with Core Workflow

This agent uses the Research → Plan → Implement workflow from core-workflow, enhanced with DevOps-specific context gathering.

### When to Use

Use `/research` with devops-engineer when:
- Deploying new applications to Kubernetes
- Upgrading existing Helm charts
- Investigating application failures
- Planning infrastructure changes
- Auditing current deployments

### Research Output

The agent creates research bundles containing:
- Current resource configurations (YAML)
- Helm chart values (current vs desired)
- ArgoCD application status
- Container image versions
- Resource utilization metrics
- Identified issues or gaps

### Example Usage

```bash
# Research deploying Redis cluster
/research deploy-redis-cluster

# Agent will:
# 1. Search for existing Redis deployments (kubectl)
# 2. Review available Helm charts
# 3. Check resource quotas and limits
# 4. Analyze storage requirements
# 5. Review network policies
# 6. Create research bundle with findings

# Output: redis-cluster-research.md (1.5k tokens)
```

## Factor Compliance

- **Factor II (JIT Context):** Loads only relevant manifests/charts
- **Factor VI (Session Continuity):** Creates research bundles for planning phase
- **Factor VII (Intelligent Routing):** Routes to kubectl/helm/argocd based on resource type
- **Factor XII (Domain Portability):** Patterns work across K8s distributions

## Best Practices

1. **Always check current state first** - Use kubectl/helm before making changes
2. **Export configurations** - Save current YAML for comparison
3. **Review resource limits** - Check quotas before deploying
4. **Check dependencies** - Identify ConfigMaps, Secrets, PVCs needed
5. **Document findings** - Create detailed research bundles

## Common Research Questions

**"What's deployed?"**
```bash
kubectl get deployments,statefulsets,daemonsets -A
```

**"How is it configured?"**
```bash
helm get values <release> -n <namespace> --all
```

**"Is it healthy?"**
```bash
kubectl get pods -n <namespace>
kubectl describe pod <name> -n <namespace>
kubectl logs <pod> -n <namespace>
```

**"What changed?"**
```bash
argocd app diff <app-name>
helm diff upgrade <release> <chart> -f values.yaml
```

## Token Budget

- **Agent file:** ~2.5k tokens
- **Typical research session:** 10-15k tokens
- **Research bundle output:** 1-2k tokens

Total cost per research session: ~12-17k tokens (6-8.5%)

## See Also

- core-workflow/research-agent.md - Base research patterns
- commands/deploy-app.md - Deployment workflows
- skills/kubernetes-manifests/ - Common K8s patterns
