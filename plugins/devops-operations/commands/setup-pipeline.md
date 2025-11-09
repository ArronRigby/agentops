# /setup-pipeline - Configure CI/CD Pipeline

Create or update CI/CD pipeline for automated build, test, and deployment.

## Usage

```bash
/setup-pipeline <project-name> [options]

# Examples:
/setup-pipeline myapp
/setup-pipeline webapp --platform gitlab
/setup-pipeline api --tests unit,integration,e2e
```

## Workflow

### Phase 1: Research
- Review existing pipeline (if any)
- Identify build requirements
- Check test automation needs
- Review deployment targets

### Phase 2: Plan
- Design pipeline stages
- Define test strategy
- Select deployment approach
- Create security scanning steps

### Phase 3: Implement
- Create pipeline configuration (.gitlab-ci.yml or .github/workflows/)
- Set up build stage
- Configure test automation
- Add deployment stages
- Configure secrets/variables

### Phase 4: Validate
- Test pipeline on feature branch
- Verify all stages pass
- Check deployment to staging
- Review pipeline logs

## Pipeline Stages

**Build** - Compile code, build container images
**Test** - Run unit, integration, and e2e tests
**Security** - Scan for vulnerabilities
**Deploy-Staging** - Auto-deploy to staging environment
**Deploy-Production** - Manual approval, deploy to production

## Options

- `--platform <name>` - CI/CD platform (gitlab, github, default: detect)
- `--tests <types>` - Test types to include (unit,integration,e2e)
- `--deploy-strategy <type>` - Deployment strategy (rolling, blue-green, canary)

## See Also

- agents/cicd-specialist.md - Planning patterns
- skills/gitops-patterns/ - ArgoCD/Flux integration
