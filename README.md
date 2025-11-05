# Swarm Claude Plugin Repository

This repository demonstrates best practices for structuring and distributing Claude plugins. It includes a complete sample plugin (`devops-assistant`) located in the `sample-plugin` subdirectory.

## 📁 Repository Structure

```
swarm-claude-plugin/                # Repository root
├── .claude-plugin/
│   └── marketplace.json            # Marketplace manifest for discovery
├── .claude-repository.json         # Repository manifest for plugin discovery  
├── sample-plugin/                  # Plugin in subdirectory (recommended structure)
│   ├── .claude-plugin/
│   │   └── plugin.json             # Plugin manifest
│   ├── commands/                   # Plugin commands
│   ├── agents/                     # AI agents
│   ├── skills/                     # Reusable skills
│   ├── hooks/                      # Lifecycle hooks
│   ├── scripts/                    # Utility scripts
│   ├── README.md                   # Plugin documentation
│   ├── QUICK_START.md              # Quick start guide
│   ├── install.sh                  # Installation script
│   └── ...
├── scripts/
│   └── list-plugins.sh             # Helper script to list installed plugins
├── install.sh                      # Main installation script
├── USER_GUIDE.md                   # Comprehensive user guide for using the plugin
├── QUICK_REFERENCE.md              # Quick reference card / cheat sheet
├── REMOTE_INSTALLATION_GUIDE.md    # Guide for remote installation
├── GIT_DISCOVERY_GUIDE.md          # Guide for Git-based discovery
├── examples/                       # Usage examples (future)
├── docs/                           # Additional documentation (future)
└── README.md                       # This file
```

## 🚀 Quick Installation

### Method 1: One-Line Installation (Recommended)
```bash
# Install directly using our installation script
curl -sSL https://raw.githubusercontent.com/trilogy-group/swarm-claude-plugin/main/install.sh | bash
```

### Method 2: GitHub Marketplace Format
```bash
# Add the repository as a marketplace (for public repos)
claude plugin marketplace add trilogy-group/swarm-claude-plugin

# Install the plugin
claude plugin install devops-assistant
```

### Method 3: Clone and Install Locally
```bash
# Clone the repository
git clone https://github.com/trilogy-group/swarm-claude-plugin.git
cd swarm-claude-plugin

# Add as local marketplace
claude plugin marketplace add .

# Install the plugin
claude plugin install devops-assistant
```

### Method 4: Private Repository Installation
```bash
# For private repositories, use SSH
git clone git@github.com:trilogy-group/swarm-claude-plugin.git
cd swarm-claude-plugin

# Add as local marketplace
claude plugin marketplace add .

# Install the plugin
claude plugin install devops-assistant
```

### ⚠️ Important Notes:
- The plugin requires `.claude-plugin/marketplace.json` for marketplace discovery
- Repository must be **public** for direct GitHub installation
- For private repos, clone locally first or use SSH authentication

## 🎯 Quick Usage

Once installed, you can use the plugin in multiple ways:

### In Claude CLI Interactive Mode
```bash
# Start Claude CLI
claude

# Use plugin commands
> @devops status
> @devops logs --service api-gateway

# Natural language requests
> Check the health of our infrastructure
> Review this code for security issues
```

### Via Command Line
```bash
# Direct execution
claude -p "@devops status --format json"

# Natural language
claude -p "Analyze our deployment logs for errors"
```

### In Your Code (SDK)
```python
from claude import Claude, plugins

claude = Claude()
devops = plugins.load('devops-assistant')

# Execute commands
status = devops.command('status', {'environment': 'prod'})

# Use agents
security_review = devops.agent('security-reviewer').analyze('./src')
```

📚 **Full Documentation**: See [USER_GUIDE.md](USER_GUIDE.md) for comprehensive usage instructions


### Manage Plugins
```bash
# Install a plugin
claude plugin install devops-assistant

# Install from specific marketplace
claude plugin install devops-assistant@swarm-claude-plugin

# Enable a plugin (use full name with marketplace)
claude plugin enable devops-assistant@swarm-claude-plugin

# Disable a plugin (use full name with marketplace)
claude plugin disable devops-assistant@swarm-claude-plugin

# Uninstall a plugin
claude plugin uninstall devops-assistant

# Validate a plugin (checks manifest structure)
claude plugin validate /path/to/plugin
```

**Note:** The plugin name format for enable/disable commands may require the full `plugin@marketplace` format.

### Manage Marketplaces
```bash
# Add a marketplace
claude plugin marketplace add trilogy-group/swarm-claude-plugin  # GitHub format
claude plugin marketplace add /path/to/local/plugin              # Local path

# List marketplaces
claude plugin marketplace list

# Remove a marketplace
claude plugin marketplace remove swarm-claude-plugin

# Update marketplace
claude plugin marketplace update swarm-claude-plugin
```

## 🔍 How Discovery Works

Claude discovers the plugin in this repository through multiple mechanisms:

1. **Repository Manifest** (`.claude-repository.json`): Explicitly declares where plugins are located
2. **Automatic Search**: Claude searches common paths like `sample-plugin/`, `plugins/`, `packages/`
3. **Direct Path**: Users can specify the exact path to the plugin

The plugin does **NOT** need to be at the repository root. Having it in a subdirectory is actually recommended because it:
- Keeps the repository organized
- Allows for documentation and examples at the root
- Supports multiple plugins in one repository
- Makes CI/CD pipelines cleaner

## 📋 What's Included

### DevOps Assistant Plugin (`sample-plugin/`)

A comprehensive DevOps automation plugin featuring:

- **🔧 Commands**: Infrastructure status monitoring, log analysis
- **🤖 Agents**: Security reviewer, performance tester, compliance checker
- **💡 Skills**: Code reviewer, PDF processor
- **🔄 Hooks**: Git hooks, deployment hooks, security hooks
- **📜 Scripts**: Security scanning, code formatting, deployment orchestration
- **🔌 Integrations**: Kubernetes, Docker, Prometheus, Jenkins, AWS/Azure/GCP

## 📚 Documentation

### Core Documentation
- [**User Guide**](USER_GUIDE.md) - Complete guide on using the plugin with Claude CLI and SDK
- [**Quick Reference**](QUICK_REFERENCE.md) - Cheat sheet for common commands and usage
- [Plugin README](sample-plugin/README.md) - Complete plugin documentation
- [Quick Start Guide](sample-plugin/QUICK_START.md) - Get started in 5 minutes

### Installation & Setup
- [Remote Installation Guide](REMOTE_INSTALLATION_GUIDE.md) - Install from GitHub
- [Git Discovery Guide](GIT_DISCOVERY_GUIDE.md) - How Claude discovers plugins in Git repos
- [Plugin Discovery Spec](sample-plugin/PLUGIN_DISCOVERY.md) - Technical discovery details

### Plugin Components
- [Commands Documentation](sample-plugin/commands/) - Available commands
- [Agents Documentation](sample-plugin/agents/) - AI agents and their capabilities
- [Skills Documentation](sample-plugin/skills/) - Reusable skills
- [Hooks Documentation](sample-plugin/hooks/) - Automation hooks

## 🎯 Key Points About Subdirectory Structure

### ✅ Advantages
1. **Plugin can be in any subdirectory** - Not limited to repository root
2. **Cleaner repository organization** - Separate plugin from docs/examples
3. **Multiple plugins supported** - Can have multiple plugins in one repo
4. **Better for monorepos** - Natural fit for monorepo structures
5. **CI/CD friendly** - Easier to manage build and test pipelines

### 🔧 How It Works
- The `.claude-repository.json` file at the root tells Claude where to find plugins
- Claude automatically searches common subdirectory patterns
- Users can specify explicit paths if needed
- All installation methods work with subdirectory structures


## 🔄 Development Workflow

For plugin developers:

```bash
# Clone the repository
git clone https://github.com/yourusername/swarm-claude-plugin.git
cd swarm-claude-plugin

# Make changes to the plugin
cd sample-plugin
# ... edit files ...

# Test locally
claude plugin install ./sample-plugin --dev

# Watch for changes (development mode)
claude plugin watch devops-assistant

# Commit and push
git add .
git commit -m "Update plugin"
git push

# Users can now install the updated plugin
claude plugin update devops-assistant
```

## 📦 Repository as a Template

This repository structure can serve as a template for your own Claude plugins:

1. Fork or clone this repository
2. Modify `sample-plugin/` with your plugin code
3. Update `.claude-repository.json` with your plugin details
4. Push to your repository
5. Share the repository URL for others to install

## 🤝 Contributing

Contributions are welcome! This repository demonstrates best practices for Claude plugin development and distribution.

## 📄 License

MIT License - See [LICENSE](sample-plugin/LICENSE) for details

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/swarm-claude-plugin/issues)
- **Documentation**: See the various guide files in this repository
- **Plugin Docs**: [sample-plugin/README.md](sample-plugin/README.md)

---

**Remember**: The plugin being in `sample-plugin/` subdirectory is intentional and recommended. Claude fully supports this structure!
