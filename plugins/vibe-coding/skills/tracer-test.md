---
name: tracer-test
description: Create and run tracer tests to validate assumptions before full implementation. Essential for Vibe Level 1-2 tasks. Prevents debug spirals by catching failures early.
---

# tracer-test Skill

**Purpose:** Validate critical assumptions before implementation

---

## When to Use

- Before any Level 1-2 task (REQUIRED)
- Before Level 3 tasks with uncertainty (RECOMMENDED)
- When previous similar work caused debug spirals
- When integrating with external systems
- When working in unfamiliar domain

---

## The 6 Tracer Patterns

### 1. API_MISMATCH
**Risk:** Kubernetes/API version incompatibility
**Tracer:**
```bash
# Check available APIs
oc api-resources | grep <resource>

# Dry-run minimal CR
cat <<EOF | oc apply --dry-run=server -f -
apiVersion: <version>
kind: <Kind>
metadata:
  name: tracer-test
spec:
  # minimal required fields only
EOF
```

### 2. SECRETS_AUTH
**Risk:** Secret format, OAuth flow, credential issues
**Tracer:**
```bash
# Validate secret structure
oc get secret <name> -o jsonpath='{.data}' | jq 'keys'

# Test OAuth token endpoint
curl -X POST <token-url> \
  -d "client_id=<id>&client_secret=<secret>&grant_type=client_credentials"
```

### 3. SSL_TLS
**Risk:** Certificate chain, trust store, TLS version
**Tracer:**
```bash
# Test SSL from inside cluster
oc run ssl-test --rm -it --image=curlimages/curl -- \
  curl -v https://<endpoint>

# Check certificate chain
openssl s_client -connect <host>:443 -showcerts
```

### 4. VOLUME_CONFIG
**Risk:** PVC binding, mount paths, permissions
**Tracer:**
```bash
# Deploy minimal pod with volume
cat <<EOF | oc apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: volume-tracer
spec:
  containers:
  - name: test
    image: busybox
    command: ['sh', '-c', 'ls -la /mnt && sleep 3600']
    volumeMounts:
    - name: test-vol
      mountPath: /mnt
  volumes:
  - name: test-vol
    persistentVolumeClaim:
      claimName: <pvc-name>
EOF

# Check mount
oc exec volume-tracer -- ls -la /mnt
```

### 5. IMAGE_REGISTRY
**Risk:** Image pull, registry auth, image existence
**Tracer:**
```bash
# Test image pull directly
oc run image-test --rm -it --image=<full-image-path> -- echo "pull successful"

# Check imagePullSecrets
oc get sa default -o jsonpath='{.imagePullSecrets}'
```

### 6. GITOPS_DRIFT
**Risk:** Operator modifications, webhook mutations, defaults
**Tracer:**
```bash
# Deploy resource
oc apply -f resource.yaml

# Wait for reconciliation
sleep 30

# Check for drift
oc get <resource> -o yaml > actual.yaml
diff resource.yaml actual.yaml
```

---

## Tracer Test Workflow

1. **Identify Risk Areas**
   - What external systems are involved?
   - What assumptions are we making?
   - Where have we seen failures before?

2. **Write Minimal Tracer**
   - Smallest possible test
   - Validates ONE assumption
   - Fast to run (<1 minute)

3. **Run Before Implementation**
   - If tracer fails, fix BEFORE coding
   - Document what was learned

4. **Keep Tracer for Regression**
   - Add to test suite
   - Run in CI/CD

---

## Time Investment

| Phase | Without Tracers | With Tracers |
|-------|-----------------|--------------|
| Research | 10% | 10% |
| Tracer Tests | 0% | 10-15% |
| Implementation | 30% | 30% |
| Debug Spirals | 40-50% | 5-10% |
| **Total** | 100% | 55-65% |

**Tracer tests typically save 25-50% of total time by preventing debug spirals.**

---

## Related Skills

- `vibe-level` - Classify task to know if tracers needed
- `vibe-check` - Measure if tracers are improving metrics
