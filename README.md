# AgentOps - Example Claude Code Marketplace

> A minimal example showing how to create your own Claude Code plugin marketplace

## Goals

1. **Showcase my plugins** - 3 example plugins demonstrating 12-Factor AgentOps patterns
2. **Show how to create your own** - Simple, clear structure for building marketplaces
3. **Link to better marketplaces** - Point to production-ready catalogs with 300+ plugins

---

## My Example Plugins

### Quick Install

```bash
/plugin marketplace add boshu2/agentops
/plugin install core-workflow@agentops
```

### What's Included

**core-workflow** - Universal Research → Plan → Implement → Learn workflow
- 4 agents for structured development phases
- 5 commands for workflow orchestration
- Base pattern for other plugins

**devops-operations** - Kubernetes, Helm, CI/CD automation
- 3 agents for DevOps tasks
- 3 commands for deployment workflows
- Skills for GitOps patterns

**software-development** - Python, JavaScript, Go development
- 3 agents for coding tasks
- 3 commands for code workflows
- Skills for testing patterns

All plugins follow [12-Factor AgentOps](https://github.com/boshu2/12-factor-agentops) principles.

---

## Create Your Own Marketplace

### 1. Repository Structure

```
your-marketplace/
├── .claude-plugin/
│   └── marketplace.json          # Required: marketplace definition
├── plugins/
│   └── your-plugin/
│       ├── .claude-plugin/
│       │   └── plugin.json       # Required: plugin manifest
│       ├── agents/               # Optional: AI specialists
│       ├── commands/             # Optional: slash commands
│       └── README.md             # Recommended: documentation
└── README.md                     # How to use your marketplace
```

### 2. Create marketplace.json

```json
{
  "name": "your-marketplace",
  "owner": {
    "name": "Your Name",
    "email": "you@example.com"
  },
  "plugins": [
    {
      "name": "your-plugin",
      "source": "./your-plugin",
      "description": "What your plugin does",
      "version": "1.0.0"
    }
  ]
}
```

### 3. Create plugin.json

```json
{
  "name": "your-plugin",
  "version": "1.0.0",
  "description": "Plugin description",
  "author": "Your Name",
  "license": "Apache-2.0",
  "components": {
    "agents": ["agents/your-agent.md"],
    "commands": ["commands/your-command.md"]
  }
}
```

### 4. Share It

```bash
# Users install with:
/plugin marketplace add your-github-username/your-repo
```

**Full documentation:** [Claude Code Plugin Marketplaces](https://docs.claude.com/en/docs/claude-code/plugin-marketplaces)

---

## Use Production Marketplaces Instead

My marketplace is a simple example. For real work, use these comprehensive catalogs:

### [AITMPL - AI Template Marketplace](https://www.aitmpl.com/plugins)
```bash
/plugin marketplace add https://www.aitmpl.com/agents
/plugin marketplace add https://www.aitmpl.com/plugins
```
**63+ plugins | 85+ agents** - Curated professional tools for all domains

### [Claude Code Templates](https://github.com/davila7/claude-code-templates)
```bash
/plugin marketplace add davila7/claude-code-templates
```
**100+ templates** - Complete component library with external integrations (GitHub, AWS, OpenAI)

### [wshobson/agents](https://github.com/wshobson/agents)
```bash
/plugin marketplace add wshobson/agents
```
**63 plugins | 85 agents | 47 skills** - Open source community collection

### [AgentOps Showcase](https://github.com/boshu2/agentops-showcase)
```bash
/plugin marketplace add boshu2/agentops-showcase
```
**92 agents** - Production-tested patterns from real GitOps operations

**Total ecosystem: 300+ plugins and agents** across these marketplaces.

---

## Resources

**Official Documentation:**
- [Claude Code Plugins](https://docs.claude.com/en/docs/claude-code/plugins)
- [Plugin Marketplaces](https://docs.claude.com/en/docs/claude-code/plugin-marketplaces)
- [Plugin Reference](https://docs.claude.com/en/docs/claude-code/plugins-reference)

**My Framework:**
- [12-Factor AgentOps](https://github.com/boshu2/12-factor-agentops) - Operational patterns
- [AgentOps Showcase](https://agentops-showcase.com) - Examples and tutorials

## License

Apache 2.0 - See [LICENSE](LICENSE)

---

**Created by:** Boden Fuller
**Purpose:** Minimal marketplace example + links to better alternatives
**Status:** Educational / Example
