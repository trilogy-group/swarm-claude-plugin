# 🚀 Quick Start Guide - DevOps Assistant Plugin

## 5-Minute Installation

### Option 1: One-Line Install (Recommended)

```bash
curl -sSL https://raw.githubusercontent.com/example/devops-assistant/main/install.sh | bash
```

### Option 2: Claude CLI

```bash
# Install latest version
claude plugin install devops-assistant

# Verify installation
claude plugin verify devops-assistant

# Test it works
claude run @devops status
```

### Option 3: Manual Install

```bash
# 1. Clone or download the plugin
git clone https://github.com/example/devops-assistant-plugin
cd devops-assistant-plugin

# 2. Copy to Claude plugins directory
cp -r sample-plugin ~/.claude/plugins/devops-assistant

# 3. Install dependencies
cd ~/.claude/plugins/devops-assistant
npm install && pip install -r requirements.txt

# 4. Activate the plugin
claude plugin enable devops-assistant
```

## 🔍 How Claude Discovers Plugins

### Automatic Discovery Locations

Claude automatically checks these directories on startup:

| Priority | Location | Type | Purpose |
|----------|----------|------|---------|
| 1 | `./.claude-plugins/` | Workspace | Project-specific plugins |
| 2 | `~/.claude/plugins/` | User | Personal plugins |
| 3 | `/opt/claude/plugins/` | System | Shared plugins |
| 4 | Registry URLs | Remote | Published plugins |

### Plugin Detection Criteria

Claude recognizes a valid plugin by checking for:

✅ **Required Files**:
- `.claude-plugin/plugin.json` - Plugin manifest
- At least one component (command, agent, or skill)

✅ **Valid Structure**:
```
your-plugin/
├── .claude-plugin/
│   └── plugin.json    ← REQUIRED: Plugin manifest
├── commands/          ← OPTIONAL: Custom commands
├── agents/            ← OPTIONAL: AI agents
├── skills/            ← OPTIONAL: Reusable skills
├── hooks/             ← OPTIONAL: Lifecycle hooks
└── scripts/           ← OPTIONAL: Utility scripts
```

## 🎯 First Steps After Installation

### 1. Check Installation

```bash
# Verify plugin is installed and active
claude plugin list | grep devops-assistant
```

Expected output:
```
✅ devops-assistant     1.0.0    Active    ~/.claude/plugins/devops-assistant
```

### 2. Test Basic Commands

```bash
# Test status command
claude run @devops status

# Test logs command
claude run @devops logs --service api-gateway --lines 50
```

### 3. Configure Essential Settings

```bash
# Set your environment
claude plugin config devops-assistant --set environment=development

# Configure monitoring endpoint
claude plugin config devops-assistant --set monitoring.url=http://localhost:9090

# Enable security scanning
claude plugin config devops-assistant --set security.enabled=true
```

### 4. Set Required Environment Variables

```bash
# Create .env file
cat > ~/.claude/plugins/devops-assistant/.env << EOF
GITHUB_TOKEN=your_token_here
DATABASE_URL=postgresql://localhost/mydb
SLACK_WEBHOOK=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
EOF

# Load variables
source ~/.claude/plugins/devops-assistant/.env
```

## 📝 Basic Usage Examples

### Using Commands

```bash
# In terminal
claude run @devops status
claude run @devops logs --service api-gateway

# In Claude chat
"Check the DevOps infrastructure status"
"Show me the API gateway logs from the last hour"
```

### Activating Agents

```bash
# Security scanning
"Review my code for security vulnerabilities"

# Performance testing
"Run performance tests on the API endpoints"

# Compliance checking
"Check GDPR compliance for user data handling"
```

### Using Skills

```python
# Code review
"Review this Python function for best practices"

# PDF processing
"Extract text from the uploaded PDF document"
```

## 🔧 Common Setup Tasks

### Enable Git Hooks

```bash
cd your-project
claude hook install pre-commit
claude hook install pre-push
```

### Connect to Services

```bash
# Connect to Kubernetes
kubectl proxy &
claude mcp connect kubernetes-server

# Connect to Docker
claude mcp connect docker-server

# Connect to monitoring
claude mcp connect monitoring-server --url http://prometheus:9090
```

### Configure Notifications

```bash
# Slack notifications
claude plugin config devops-assistant \
  --set notifications.slack.enabled=true \
  --set notifications.slack.webhook=$SLACK_WEBHOOK

# Email notifications
claude plugin config devops-assistant \
  --set notifications.email.enabled=true \
  --set notifications.email.smtp=smtp.gmail.com
```

## ❓ Troubleshooting Quick Fixes

### Plugin Not Found

```bash
# Refresh plugin discovery
claude plugin refresh

# Manually register plugin
claude plugin discover ~/.claude/plugins/devops-assistant
```

### Commands Not Working

```bash
# Check plugin status
claude plugin status devops-assistant

# Reload plugin
claude plugin reload devops-assistant

# Check logs
claude plugin logs devops-assistant --tail 50
```

### Permission Issues

```bash
# Grant all permissions (development)
claude plugin permissions devops-assistant --grant-all

# Fix file permissions
chmod -R 755 ~/.claude/plugins/devops-assistant
```

## 📊 Health Check

Run this command to verify everything is working:

```bash
claude plugin health devops-assistant --verbose
```

Expected output:
```
DevOps Assistant Plugin Health Check
====================================
✅ Plugin Status: Active
✅ Manifest Valid: Yes
✅ Dependencies Met: 5/5
✅ Commands Available: 2/2
✅ Agents Loaded: 3/3
✅ Skills Loaded: 2/2
✅ Hooks Configured: 13/13
✅ MCP Servers: 8/10 connected
✅ Permissions: All granted
✅ Environment Variables: 4/5 set

Overall Health: 95% - Excellent
```

## 🚪 Next Steps

1. **Read the full documentation**: `README.md`
2. **Explore available commands**: `claude help plugin devops-assistant`
3. **Configure for your environment**: Edit `~/.claude/plugins/devops-assistant/config.json`
4. **Join the community**: https://forum.claude.ai/c/plugins
5. **Report issues**: https://github.com/example/devops-assistant-plugin/issues

## 🆘 Get Help

```bash
# Plugin-specific help
claude help @devops

# Interactive tutorial
claude tutorial devops-assistant

# Support
claude support --plugin devops-assistant
```

---

**Need more help?** Ask Claude directly: "How do I use the DevOps Assistant plugin?"

*Version 1.0.0 | Last Updated: January 2024*
