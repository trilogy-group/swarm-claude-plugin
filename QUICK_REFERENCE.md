# 🚀 Claude DevOps Plugin - Quick Reference

## Installation
```bash
# One-line install
curl -sSL https://raw.githubusercontent.com/trilogy-group/swarm-claude-plugin/main/install.sh | bash

# Or manual
claude plugin marketplace add trilogy-group/swarm-claude-plugin
claude plugin install devops-assistant
```

## Essential Commands

### Plugin Management
```bash
# View installed plugins
cat ~/.claude/settings.json | jq '.enabledPlugins'

# List marketplaces
claude plugin marketplace list

# Uninstall plugin
claude plugin uninstall devops-assistant
```

### DevOps Commands
```bash
# In Claude CLI
claude
> @devops status                    # Check infrastructure status
> @devops status --service api       # Check specific service
> @devops logs                       # View logs
> @devops logs --filter error        # Filter logs
```

### Direct CLI Usage
```bash
# Execute commands directly
claude -p "@devops status --format json"
claude -p "@devops logs --tail 100"

# Natural language
claude -p "Check our infrastructure health"
claude -p "Show me recent deployment errors"
```

## Agents Quick Reference

| Agent | Trigger Phrase | Purpose |
|-------|---------------|---------|
| `security-reviewer` | "review security", "check vulnerabilities" | Code security analysis |
| `performance-tester` | "test performance", "check speed" | Performance analysis |
| `compliance-checker` | "check compliance", "verify standards" | Compliance validation |
| `repository-initializer` | "initialize repo", "create from boilerplate" | Repository setup from templates |

### Using Agents
```bash
# Natural activation
> Review this code for security issues

# Explicit activation
> @agent security-reviewer analyze ./src

# Via SDK
claude.agent('security-reviewer').analyze(code)
```

## Skills Quick Reference

| Skill | Usage | Output |
|-------|-------|--------|
| `code-reviewer` | Reviews code quality | Findings report |
| `pdf-processor` | Processes PDF docs | Extracted content |

## Common Workflows

### Daily Status Check
```bash
claude -p "@devops status" > daily-status.txt
```

### Security Review Before Deploy
```bash
claude -p "Review security of main branch" && \
claude -p "@devops deploy --env production"
```

### Error Investigation
```bash
claude -p "@devops logs --filter error --since '1 hour ago' | analyze these errors"
```

### Repository Initialization
```bash
# Initialize from boilerplate
claude -p "Initialize new service from https://github.com/your-org/boilerplate-api into payment-service repo"

# With specific requirements
claude -p "Fork boilerplate-api to create user-service with dev and stage branches"
```

## SDK Quick Start

### Python
```python
from claude import Claude, plugins

claude = Claude()
devops = plugins.load('devops-assistant')

# Command
status = devops.command('status')

# Agent
review = devops.agent('security-reviewer').analyze('./src')

# Repository initialization
init = devops.agent('repository-initializer').create({
    'source': 'https://github.com/org/boilerplate',
    'target': 'new-service',
    'branches': ['dev', 'stage']
})
```

### JavaScript
```javascript
const { Claude } = require('@claude/sdk');
const claude = new Claude({ plugins: ['devops-assistant'] });

// Command
const status = await claude.plugin('devops-assistant')
  .command('status')
  .execute();

// Agent
const review = await claude.plugin('devops-assistant')
  .agent('security-reviewer')
  .analyze('./src');

// Repository initialization
const init = await claude.plugin('devops-assistant')
  .agent('repository-initializer')
  .create({
    source: 'https://github.com/org/boilerplate',
    target: 'new-service',
    branches: ['dev', 'stage']
  });
```

## Environment Variables
```bash
# Set for plugin configuration
export CLAUDE_PLUGIN_ENV=production
export CLAUDE_DEVOPS_AUTO_DEPLOY=false
export CLAUDE_SECURITY_LEVEL=high
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Plugin not found | `claude plugin marketplace list` |
| Command not working | Check: `cat ~/.claude/settings.json` |
| Agent not activating | Use explicit: `@agent agent-name` |
| Permission denied | `claude plugin permissions devops-assistant --grant-all` |

## Debug Commands
```bash
claude --debug "@devops status"           # Debug mode
claude -vvv "@devops logs"                # Verbose
CLAUDE_TRACE=1 claude "@devops status"    # Trace mode
tail -f ~/.claude/logs/claude.log         # View logs
```

## File Locations
- Settings: `~/.claude/settings.json`
- Marketplaces: `~/.claude/plugins/marketplaces/`
- Logs: `~/.claude/logs/`
- Plugin: `~/.claude/plugins/marketplaces/swarm-claude-plugin/`

## Help & Support
```bash
claude help @devops                       # Plugin help
claude help @devops status                # Command help
claude docs devops-assistant              # Documentation
```

---
*Keep this handy for quick reference! Full docs: [USER_GUIDE.md](USER_GUIDE.md)*
