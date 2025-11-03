# DevOps Assistant Plugin - Installation & Discovery Guide

## 📚 Table of Contents
- [Overview](#overview)
- [Plugin Discovery](#plugin-discovery)
- [Installation Methods](#installation-methods)
- [Verification](#verification)
- [Configuration](#configuration)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Uninstallation](#uninstallation)

## Overview

The DevOps Assistant Plugin extends Claude's capabilities with advanced DevOps automation, security scanning, performance testing, and compliance checking features. This guide explains how Claude can discover and install this plugin in your environment.

## Plugin Discovery

Claude can discover plugins through multiple methods:

### 1. Local Directory Discovery

Claude automatically scans for plugins in these locations:

```
# User-level plugins
~/.claude/plugins/
~/.config/claude/plugins/

# System-level plugins
/usr/local/claude/plugins/
/opt/claude/plugins/

# Workspace-level plugins
./.claude-plugins/
./plugins/
```

To make your plugin discoverable locally:

```bash
# Option 1: Copy to user plugins directory
cp -r sample-plugin ~/.claude/plugins/devops-assistant

# Option 2: Create a symbolic link
ln -s /path/to/sample-plugin ~/.claude/plugins/devops-assistant

# Option 3: Add to workspace
cp -r sample-plugin ./.claude-plugins/devops-assistant
```

### 2. Registry Discovery

Claude can discover plugins from configured registries:

```json
// In Claude's configuration file (~/.claude/config.json)
{
  "plugin_registries": [
    {
      "name": "official",
      "url": "https://registry.claude.ai/plugins",
      "enabled": true
    },
    {
      "name": "enterprise",
      "url": "https://your-company.com/claude-plugins",
      "enabled": true,
      "auth": {
        "type": "bearer",
        "token_env": "CLAUDE_REGISTRY_TOKEN"
      }
    }
  ]
}
```

To publish to a registry:

```bash
# Package the plugin
cd sample-plugin
tar -czf devops-assistant-1.0.0.tar.gz *

# Upload to registry (example using curl)
curl -X POST https://registry.claude.ai/plugins/publish \
  -H "Authorization: Bearer $API_TOKEN" \
  -F "plugin=@devops-assistant-1.0.0.tar.gz" \
  -F "metadata=@.claude-plugin/plugin.json"
```

### 3. Git Repository Discovery

Claude can install plugins directly from Git repositories:

```bash
# Public repository
claude plugin install https://github.com/example/devops-assistant-plugin

# Private repository with authentication
claude plugin install git@github.com:company/devops-assistant-plugin.git

# Specific branch or tag
claude plugin install https://github.com/example/devops-assistant-plugin#v1.0.0
```

### 4. Manual Discovery via Command

Explicitly tell Claude about a plugin location:

```bash
# Register a local plugin
claude plugin discover /path/to/sample-plugin

# Register a remote plugin
claude plugin discover https://example.com/plugins/devops-assistant.json
```

## Installation Methods

### Method 1: Claude CLI Installation

```bash
# Install from local directory
claude plugin install ./sample-plugin

# Install from registry
claude plugin install devops-assistant

# Install specific version
claude plugin install devops-assistant@1.0.0

# Install with dependencies
claude plugin install devops-assistant --with-deps

# Dry run to see what would be installed
claude plugin install devops-assistant --dry-run
```

### Method 2: Interactive Installation

1. **Via Claude Interface**:
   ```
   User: Install the DevOps Assistant plugin
   Claude: I'll install the DevOps Assistant plugin for you...
   ```

2. **Via Command Palette**:
   ```
   Cmd/Ctrl + Shift + P → "Install Plugin" → Search "devops-assistant"
   ```

### Method 3: Package Manager Installation

```bash
# NPM (for Node.js components)
npm install -g @claude-plugins/devops-assistant

# Python (for Python components)
pip install claude-plugin-devops-assistant

# Homebrew (macOS)
brew install claude-plugin-devops-assistant
```

### Method 4: Docker Installation

```dockerfile
# In your Dockerfile
FROM claude:latest

# Install plugin
RUN claude plugin install devops-assistant

# Or copy plugin directly
COPY sample-plugin /opt/claude/plugins/devops-assistant
```

```bash
# Using Docker Compose
version: '3.8'
services:
  claude:
    image: claude:latest
    volumes:
      - ./sample-plugin:/opt/claude/plugins/devops-assistant:ro
    environment:
      - CLAUDE_PLUGIN_PATH=/opt/claude/plugins
```

### Method 5: Automated Installation Script

Create an installation script:

```bash
#!/bin/bash
# install-plugin.sh

set -e

PLUGIN_NAME="devops-assistant"
PLUGIN_VERSION="1.0.0"
CLAUDE_PLUGINS_DIR="${HOME}/.claude/plugins"

echo "Installing DevOps Assistant Plugin v${PLUGIN_VERSION}..."

# Create plugins directory if it doesn't exist
mkdir -p "${CLAUDE_PLUGINS_DIR}"

# Download or copy plugin
if [ -d "./sample-plugin" ]; then
    cp -r ./sample-plugin "${CLAUDE_PLUGINS_DIR}/${PLUGIN_NAME}"
else
    git clone https://github.com/example/devops-assistant-plugin \
        "${CLAUDE_PLUGINS_DIR}/${PLUGIN_NAME}"
fi

# Install dependencies
echo "Installing dependencies..."
cd "${CLAUDE_PLUGINS_DIR}/${PLUGIN_NAME}"

# Install Node.js dependencies if package.json exists
if [ -f "package.json" ]; then
    npm install --production
fi

# Install Python dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

# Set permissions
chmod +x scripts/*.sh
chmod +x scripts/*.py

# Verify installation
claude plugin verify "${PLUGIN_NAME}"

echo "✅ DevOps Assistant Plugin installed successfully!"
```

## Verification

### 1. Check Installation Status

```bash
# List all installed plugins
claude plugin list

# Check specific plugin
claude plugin info devops-assistant

# Verify plugin integrity
claude plugin verify devops-assistant

# Check plugin health
claude plugin health devops-assistant
```

### 2. Test Plugin Functionality

```bash
# Test commands
claude run @devops status
claude run @devops logs --service api-gateway

# Test agents
claude agent test security-reviewer
claude agent test performance-tester

# Test skills
claude skill test code-reviewer
claude skill test pdf-processor
```

### 3. Validation Output

Expected output from `claude plugin info devops-assistant`:

```
Plugin: DevOps Assistant
Version: 1.0.0
Status: ✅ Active
Location: /home/user/.claude/plugins/devops-assistant

Components:
  Commands: 2 (status, logs)
  Agents: 3 (security-reviewer, performance-tester, compliance-checker)
  Skills: 2 (code-reviewer, pdf-processor)
  Hooks: 13 configured, 13 active
  MCP Servers: 10 configured, 8 connected

Dependencies:
  ✅ Node.js 18.0.0 (required: >=16.0.0)
  ✅ Python 3.10.0 (required: >=3.8)
  ✅ Bash 5.1.0 (required: >=4.0)

Permissions:
  ✅ file:read
  ✅ file:write
  ✅ process:execute
  ✅ network:http
  ✅ system:env
```

## Configuration

### 1. Plugin Configuration

Edit plugin settings:

```bash
# Open configuration in editor
claude plugin config devops-assistant

# Set configuration via CLI
claude plugin config devops-assistant --set scanOnSave=true
claude plugin config devops-assistant --set securityLevel=high
```

Configuration file location: `~/.claude/plugins/devops-assistant/config.json`

```json
{
  "plugin": "devops-assistant",
  "enabled": true,
  "autoLoad": true,
  "settings": {
    "defaultBranch": "main",
    "scanOnSave": true,
    "autoFormat": false,
    "securityLevel": "standard",
    "environments": {
      "development": {
        "url": "http://localhost:3000",
        "monitoring": false
      },
      "production": {
        "url": "https://api.example.com",
        "monitoring": true,
        "alerts": true
      }
    }
  },
  "mcp_servers": {
    "kubernetes": {
      "enabled": true,
      "endpoint": "http://localhost:8001",
      "auth": "${K8S_TOKEN}"
    },
    "docker": {
      "enabled": true,
      "endpoint": "unix:///var/run/docker.sock"
    }
  }
}
```

### 2. Environment Variables

Set required environment variables:

```bash
# Create environment file
cat > ~/.claude/plugins/devops-assistant/.env << EOF
# API Keys
GITHUB_TOKEN=your_github_token
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret

# Database
DATABASE_URL=postgresql://user:pass@localhost/db

# Monitoring
PROMETHEUS_URL=http://localhost:9090
ELASTIC_URL=http://localhost:9200

# Notifications
SLACK_WEBHOOK=https://hooks.slack.com/services/xxx
PAGERDUTY_KEY=your_pagerduty_key

# Security
VAULT_TOKEN=your_vault_token
SONARQUBE_TOKEN=your_sonarqube_token
EOF

# Load environment variables
export $(cat ~/.claude/plugins/devops-assistant/.env | xargs)
```

### 3. Permissions Configuration

Configure plugin permissions:

```bash
# Grant all requested permissions
claude plugin permissions devops-assistant --grant-all

# Grant specific permissions
claude plugin permissions devops-assistant --grant file:read,file:write

# Review permissions
claude plugin permissions devops-assistant --list

# Revoke permissions
claude plugin permissions devops-assistant --revoke network:http
```

## Usage

### 1. Command Invocation

```bash
# Via Claude CLI
claude run @devops status
claude run @devops logs --service api-gateway --lines 100

# Via Claude Chat
"Check the status of our infrastructure"
"Show me the recent error logs from the API gateway"
```

### 2. Agent Activation

```bash
# Manual activation
claude agent activate security-reviewer
claude agent activate performance-tester

# Trigger-based (automatic)
# Agents activate based on configured triggers in plugin.json
```

### 3. Skill Usage

```python
# In Claude conversation
"Review this Python code for security issues"
"Extract text from this PDF document"

# Via API
from claude import skills

reviewer = skills.load('code-reviewer')
result = reviewer.analyze('app.py')

processor = skills.load('pdf-processor')
text = processor.extract_text('document.pdf')
```

### 4. Hook Integration

Hooks automatically integrate with your workflow:

```bash
# Git hooks are installed automatically
git commit  # Triggers pre-commit hooks
git push    # Triggers pre-push hooks

# Manual hook execution
claude hook run pre-deploy --env production
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Plugin Not Discovered

```bash
# Check plugin path
claude config get plugin_paths

# Add plugin path
claude config add-path ~/.my-plugins

# Refresh plugin cache
claude plugin refresh
```

#### 2. Installation Failures

```bash
# Check logs
claude plugin logs devops-assistant

# Clear cache and reinstall
claude plugin cache clear
claude plugin uninstall devops-assistant
claude plugin install devops-assistant --fresh
```

#### 3. Dependency Issues

```bash
# Check missing dependencies
claude plugin deps devops-assistant

# Install missing dependencies
claude plugin deps devops-assistant --install

# Use isolated environment
claude plugin install devops-assistant --isolated
```

#### 4. Permission Errors

```bash
# Check current permissions
claude plugin permissions devops-assistant --check

# Run with elevated permissions (temporary)
claude run @devops status --elevated

# Fix permission issues
sudo chown -R $(whoami) ~/.claude/plugins/devops-assistant
chmod -R 755 ~/.claude/plugins/devops-assistant
```

#### 5. MCP Server Connection Issues

```bash
# Test MCP connections
claude mcp test kubernetes-server
claude mcp test docker-server

# Restart MCP servers
claude mcp restart all

# Check MCP logs
claude mcp logs kubernetes-server
```

### Debug Mode

Enable debug mode for detailed troubleshooting:

```bash
# Enable debug mode
claude --debug plugin install devops-assistant

# Verbose output
claude -vvv plugin verify devops-assistant

# Trace mode
CLAUDE_TRACE=1 claude run @devops status
```

### Getting Help

```bash
# Plugin-specific help
claude help plugin devops-assistant
claude run @devops --help

# Documentation
claude docs devops-assistant

# Support channels
claude support --plugin devops-assistant
```

## Uninstallation

### Complete Removal

```bash
# Uninstall plugin and all dependencies
claude plugin uninstall devops-assistant --remove-deps

# Remove configuration
rm -rf ~/.claude/plugins/devops-assistant
rm -f ~/.claude/config/devops-assistant.json

# Remove environment variables
unset $(grep -v '^#' ~/.claude/plugins/devops-assistant/.env | sed -E 's/(.*)=.*/\1/' | xargs)
```

### Partial Removal

```bash
# Disable without uninstalling
claude plugin disable devops-assistant

# Remove specific components
claude plugin remove-component devops-assistant agents/security-reviewer
```

## Advanced Topics

### Custom Installation Locations

```bash
# Install to custom location
CLAUDE_PLUGIN_PATH=/opt/custom/plugins claude plugin install devops-assistant

# Multiple plugin paths
export CLAUDE_PLUGIN_PATH="/opt/plugins:/usr/local/claude/plugins:$HOME/.claude/plugins"
```

### Plugin Development Mode

```bash
# Link development version
claude plugin link /path/to/development/plugin

# Watch for changes
claude plugin watch devops-assistant

# Hot reload
claude plugin reload devops-assistant
```

### Enterprise Deployment

```yaml
# Kubernetes deployment
apiVersion: v1
kind: ConfigMap
metadata:
  name: claude-plugins
data:
  plugins.json: |
    {
      "devops-assistant": {
        "source": "registry://enterprise/devops-assistant",
        "version": "1.0.0",
        "autoInstall": true
      }
    }
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: claude
spec:
  template:
    spec:
      volumes:
        - name: plugins
          configMap:
            name: claude-plugins
      containers:
        - name: claude
          volumeMounts:
            - name: plugins
              mountPath: /etc/claude/plugins
```

## Support

- **Documentation**: https://docs.claude.ai/plugins/devops-assistant
- **Issues**: https://github.com/example/devops-assistant-plugin/issues
- **Community**: https://forum.claude.ai/c/plugins
- **Email**: plugins@claude.ai

---

*Last Updated: January 2024 | Version: 1.0.0*
