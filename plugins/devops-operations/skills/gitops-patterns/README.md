# GitOps Patterns - ArgoCD & Flux

Progressive disclosure resource for GitOps continuous delivery patterns.

## ArgoCD Application Pattern

### Basic Application

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/repo
    targetRevision: main
    path: k8s/overlays/staging
  destination:
    server: https://kubernetes.default.svc
    namespace: myapp-staging
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### Helm-Based Application

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
spec:
  source:
    repoURL: https://github.com/org/charts
    targetRevision: main
    path: charts/myapp
    helm:
      values: |
        replicaCount: 3
        image:
          tag: "1.2.3"
```

## Flux Kustomization Pattern

### Basic Kustomization

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: myapp-staging
  namespace: flux-system
spec:
  interval: 5m
  path: ./k8s/overlays/staging
  prune: true
  sourceRef:
    kind: GitRepository
    name: myapp
```

### Git Repository Source

```yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: myapp
  namespace: flux-system
spec:
  interval: 1m
  url: https://github.com/org/repo
  ref:
    branch: main
```

## Progressive Delivery Patterns

### Canary Deployment (ArgoCD + Argo Rollouts)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: myapp
spec:
  replicas: 10
  strategy:
    canary:
      steps:
      - setWeight: 10
      - pause: {duration: 2m}
      - setWeight: 50
      - pause: {duration: 5m}
      - setWeight: 100
```

### Blue-Green Deployment

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: myapp
spec:
  strategy:
    blueGreen:
      activeService: myapp
      previewService: myapp-preview
      autoPromotionEnabled: false
```

## Sync Policies

### Auto-Sync

```yaml
syncPolicy:
  automated:
    prune: true        # Delete resources removed from git
    selfHeal: true     # Sync when cluster state drifts
```

### Manual Sync

```yaml
syncPolicy:
  syncOptions:
  - CreateNamespace=true
```

## ArgoCD CLI Commands

```bash
# List applications
argocd app list

# Get application details
argocd app get myapp

# Sync application
argocd app sync myapp

# Rollback application
argocd app rollback myapp

# Show application diff
argocd app diff myapp
```

## Flux CLI Commands

```bash
# Check Flux components
flux check

# List kustomizations
flux get kustomizations

# Reconcile kustomization
flux reconcile kustomization myapp-staging

# Suspend kustomization
flux suspend kustomization myapp-staging
```

## Best Practices

1. **Git as source of truth** - All changes via git commits
2. **Automated sync** - Let GitOps handle deployments
3. **Health checks** - Define resource health in ArgoCD/Flux
4. **Progressive delivery** - Use canary/blue-green for risk mitigation
5. **Separation of environments** - Different branches or repos per env

## Token Budget

This skill file: ~1k tokens
Load only when needed via progressive disclosure.
