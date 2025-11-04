# 🌐 Remote Installation Guide - Installing from GitHub

This guide explains how to make the Claude plugin discoverable and installable from any machine using the GitHub URL.

## Prerequisites

1. **Public GitHub Repository**: The repository must be publicly accessible
2. **Marketplace Manifest**: The repository must contain `.claude-plugin/marketplace.json`
3. **Claude CLI**: Users must have Claude CLI installed

## For Repository Maintainers

### Step 1: Ensure Your Repository Structure

Your repository should have this structure:
```
swarm-claude-plugin/
├── .claude-plugin/
│   └── marketplace.json    # Required for marketplace discovery
├── sample-plugin/           # Plugin directory
│   ├── .claude-plugin/
│   │   └── plugin.json     # Plugin manifest
│   └── ...
└── README.md
```

### Step 2: Push to Public GitHub Repository

```bash
# Initialize git if not already done
git init

# Add your GitHub repository as remote
git remote add origin https://github.com/trilogy-group/swarm-claude-plugin.git

# Add all files
git add .

# Commit
git commit -m "Add Claude plugin with marketplace manifest"

# Push to GitHub (make sure repository is public)
git push -u origin main
```

### Step 3: Make Repository Public

1. Go to https://github.com/trilogy-group/swarm-claude-plugin/settings
2. Scroll to "Danger Zone"
3. Change visibility to Public (if not already)

## For Users - Installation Methods

### Method 1: GitHub Repository Format (Recommended)

```bash
# Add the repository as a marketplace
claude plugin marketplace add trilogy-group/swarm-claude-plugin

# Install the plugin
claude plugin install devops-assistant

# Or specify the marketplace explicitly
claude plugin install devops-assistant@swarm-claude-plugin
```

### Method 2: One-Line Installation Script

Create an installation script in your repository:

```bash
#!/bin/bash
# install.sh - Place this in your repository root

echo "Installing Claude Plugin from GitHub..."

# Clone the repository temporarily
TEMP_DIR=$(mktemp -d)
git clone https://github.com/trilogy-group/swarm-claude-plugin.git "$TEMP_DIR/plugin" || exit 1

# Add as marketplace
claude plugin marketplace add "$TEMP_DIR/plugin"

# Install the plugin
claude plugin install devops-assistant

# Cleanup
rm -rf "$TEMP_DIR"

echo "✅ Plugin installed successfully!"
```

Users can then run:
```bash
curl -sSL https://raw.githubusercontent.com/trilogy-group/swarm-claude-plugin/main/install.sh | bash
```

### Method 3: Manual Clone and Install

```bash
# Clone the repository
git clone https://github.com/trilogy-group/swarm-claude-plugin.git
cd swarm-claude-plugin

# Add as local marketplace
claude plugin marketplace add .

# Install the plugin
claude plugin install devops-assistant
```

### Method 4: Using SSH (for private repositories)

If the repository is private:

```bash
# Configure SSH key with GitHub first
# Then use SSH URL format
claude plugin marketplace add git@github.com:trilogy-group/swarm-claude-plugin.git

# Install the plugin
claude plugin install devops-assistant
```

## Troubleshooting

### Issue: "Failed to clone marketplace repository"

**Causes:**
1. Repository is private
2. Network issues
3. Authentication required

**Solutions:**
1. Make repository public OR
2. Use SSH URL with configured SSH keys OR
3. Clone locally first and add as local marketplace

### Issue: "Marketplace file not found"

**Cause:** Missing `.claude-plugin/marketplace.json`

**Solution:** Ensure the marketplace.json file exists in the repository:
```json
{
  "name": "swarm-claude-plugin",
  "version": "1.0.0",
  "description": "Claude Plugin Development Repository",
  "owner": {
    "name": "trilogy-group",
    "email": "devops@trilogy.com"
  },
  "plugins": [
    {
      "name": "devops-assistant",
      "version": "1.0.0",
      "description": "DevOps automation plugin",
      "author": {
        "name": "DevOps Team",
        "email": "devops@trilogy.com"
      },
      "source": "./sample-plugin",
      "tags": ["devops", "automation"]
    }
  ]
}
```

### Issue: "Plugin not found in marketplace"

**Cause:** Plugin name mismatch

**Solution:** Use the exact plugin name from marketplace.json:
```bash
claude plugin install devops-assistant  # Must match "name" in plugins array
```

## Alternative: Global Marketplace Registry

For broader distribution, consider registering with Claude's official marketplace:

```bash
# Future feature (when available)
claude plugin publish trilogy-group/swarm-claude-plugin

# Users can then install directly
claude plugin install devops-assistant@official
```

## Docker Installation

For containerized environments:

```dockerfile
FROM claude:latest

# Add marketplace and install plugin
RUN claude plugin marketplace add trilogy-group/swarm-claude-plugin && \
    claude plugin install devops-assistant

# Or use local copy
COPY . /tmp/plugin
RUN claude plugin marketplace add /tmp/plugin && \
    claude plugin install devops-assistant && \
    rm -rf /tmp/plugin
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Install Claude Plugin

on: [push, pull_request]

jobs:
  install-plugin:
    runs-on: ubuntu-latest
    steps:
      - name: Install Claude CLI
        run: |
          curl -sSL https://claude.ai/install.sh | bash
      
      - name: Add Marketplace
        run: |
          claude plugin marketplace add ${{ github.repository }}
      
      - name: Install Plugin
        run: |
          claude plugin install devops-assistant
      
      - name: Verify Installation
        run: |
          claude plugin validate devops-assistant
```

## Quick Start Commands

For users to copy and paste:

```bash
# Quick install from GitHub (public repository)
claude plugin marketplace add trilogy-group/swarm-claude-plugin && \
claude plugin install devops-assistant

# Verify installation
claude plugin validate devops-assistant
```

## Support

- **Repository Issues**: https://github.com/trilogy-group/swarm-claude-plugin/issues
- **Documentation**: See README.md and sample-plugin/README.md
- **Marketplace Schema**: See .claude-plugin/marketplace.json

---

*Note: The repository must be public for remote installation to work without authentication.*
