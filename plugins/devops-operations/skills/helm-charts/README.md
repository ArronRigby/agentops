# Helm Charts - Best Practices

Progressive disclosure resource for Helm chart patterns and templates.

## Chart Structure

```
mychart/
├── Chart.yaml           # Chart metadata
├── values.yaml          # Default values
├── templates/
│   ├── deployment.yaml  # Deployment template
│   ├── service.yaml     # Service template
│   ├── _helpers.tpl     # Template helpers
│   └── NOTES.txt        # Post-install notes
└── charts/              # Subchart dependencies
```

## Chart.yaml

```yaml
apiVersion: v2
name: myapp
description: My application Helm chart
type: application
version: 1.0.0
appVersion: "1.0.0"
```

## values.yaml Structure

```yaml
replicaCount: 3

image:
  repository: myapp
  tag: "1.0.0"
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 80

resources:
  requests:
    memory: "128Mi"
    cpu: "100m"
  limits:
    memory: "256Mi"
    cpu: "200m"

config:
  database_host: "postgres"
  database_port: "5432"
```

## Template Patterns

### Deployment Template

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "mychart.fullname" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "mychart.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "mychart.selectorLabels" . | nindent 8 }}
    spec:
      containers:
      - name: {{ .Chart.Name }}
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
        ports:
        - containerPort: 8080
        resources:
          {{- toYaml .Values.resources | nindent 10 }}
```

### _helpers.tpl (Common Helpers)

```yaml
{{/*
Expand the name of the chart.
*/}}
{{- define "mychart.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "mychart.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "mychart.labels" -}}
helm.sh/chart: {{ include "mychart.chart" . }}
{{ include "mychart.selectorLabels" . }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}
```

## Deployment Commands

```bash
# Template chart locally
helm template myapp ./mychart -f values.yaml

# Dry-run install
helm install myapp ./mychart -f values.yaml --dry-run --debug

# Install chart
helm install myapp ./mychart -f values.yaml

# Upgrade chart
helm upgrade myapp ./mychart -f values.yaml

# Upgrade or install
helm upgrade --install myapp ./mychart -f values.yaml
```

## Best Practices

1. **Use _helpers.tpl** - Define common templates once
2. **Parameterize everything** - Use values.yaml for configuration
3. **Default values** - Provide sensible defaults in values.yaml
4. **Validate templates** - Use `helm template` before deploying
5. **Version charts** - Increment Chart.yaml version on changes

## Token Budget

This skill file: ~1k tokens
Load only when needed via progressive disclosure.
