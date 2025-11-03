# 🔍 Git-Based Plugin Discovery Guide for Claude

## Overview

Claude supports flexible Git repository structures for plugin discovery. **You do NOT need to have the plugin at the repository root** - Claude can discover plugins in subdirectories, making it easy to maintain plugins alongside documentation, examples, and other resources.

## Supported Repository Structures

### 1. Plugin in Subdirectory (Recommended)

This is the most common and recommended structure, allowing you to include documentation, examples, and multiple plugins in one repository:

```
your-repository/
├── README.md                    # Repository documentation
├── LICENSE                      # Repository license
├── .claude-repository.json      # Repository discovery manifest
├── sample-plugin/               # ← Plugin is in subdirectory
│   ├── .claude-plugin/
│   │   └── plugin.json         # Plugin manifest
│   ├── commands/
│   ├── agents/
│   ├── skills/
│   └── ...
├── examples/                    # Usage examples
├── docs/                        # Additional documentation
└── tests/                       # Test files
```

### 2. Plugin at Repository Root

The plugin can also be at the repository root:

```
your-plugin-repository/
├── .claude-plugin/              # ← Plugin at root level
│   └── plugin.json
├── commands/
├── agents/
├── skills/
├── README.md
└── ...
```

### 3. Multiple Plugins in One Repository (Monorepo)

Claude can discover multiple plugins from a single repository:

```
claude-plugins-monorepo/
├── .claude-repository.json      # Repository manifest listing all plugins
├── plugins/
│   ├── devops-assistant/        # Plugin 1
│   │   └── .claude-plugin/
│   │       └── plugin.json
│   ├── security-scanner/        # Plugin 2
│   │   └── .claude-plugin/
│   │       └── plugin.json
│   └── data-processor/          # Plugin 3
│       └── .claude-plugin/
│           └── plugin.json
├── shared/                      # Shared utilities
└── docs/                        # Documentation
```

## Repository Discovery Manifest

To help Claude discover plugins in subdirectories, create a `.claude-repository.json` file at the repository root:

```json
{
  "version": "1.0.0",
  "type": "plugin-repository",
  "description": "Repository containing Claude plugin(s)",
  "plugins": [
    {
      "name": "devops-assistant",
      "path": "sample-plugin",
      "description": "Comprehensive DevOps automation plugin",
      "version": "1.0.0",
      "default": true
    }
  ],
  "repository": {
    "type": "git",
    "url": "https://github.com/example/swarm-claude-plugin"
  },
  "discovery": {
    "method": "manifest",
    "auto_detect": true,
    "search_paths": [
      "sample-plugin",
      "plugins/*",
      "packages/*"
    ]
  },
  "installation": {
    "script": "sample-plugin/install.sh",
    "requirements": {
      "claude": ">=1.0.0",
      "node": ">=16.0.0",
      "python": ">=3.8"
    }
  }
}
```

## How Claude Discovers Plugins in Git Repositories

### Discovery Algorithm

When Claude encounters a Git repository URL, it follows this discovery process:

```python
def discover_git_plugin(repo_url):
    """
    Discovers Claude plugins from a Git repository
    """
    
    # Step 1: Check for repository manifest
    manifest_url = f"{repo_url}/raw/main/.claude-repository.json"
    if exists(manifest_url):
        manifest = fetch(manifest_url)
        return discover_from_manifest(manifest)
    
    # Step 2: Check common locations for plugins
    search_locations = [
        "",                           # Root directory
        "sample-plugin",             # Common subdirectory names
        "plugin",
        "claude-plugin",
        "src",
        "dist",
        "packages/*",                # Monorepo patterns
        "plugins/*",
        "*/.claude-plugin"           # Any directory with .claude-plugin
    ]
    
    for location in search_locations:
        plugin_manifest = f"{repo_url}/raw/main/{location}/.claude-plugin/plugin.json"
        if exists(plugin_manifest):
            return {
                "found": True,
                "path": location,
                "manifest": fetch(plugin_manifest)
            }
    
    # Step 3: Check GitHub releases for packaged plugins
    if "github.com" in repo_url:
        return check_github_releases(repo_url)
    
    return {"found": False}
```

### Installation Commands for Different Structures

#### Installing from Subdirectory

```bash
# Method 1: Using repository URL with path hint
claude plugin install https://github.com/example/repo#path=sample-plugin

# Method 2: Using repository manifest (auto-detects path)
claude plugin install https://github.com/example/repo

# Method 3: Direct path to plugin.json
claude plugin install https://github.com/example/repo/sample-plugin

# Method 4: Using git clone with subdirectory
git clone https://github.com/example/repo.git
claude plugin install ./repo/sample-plugin
```

#### Installing Specific Plugin from Monorepo

```bash
# Install specific plugin by name
claude plugin install https://github.com/example/monorepo#plugin=devops-assistant

# Install all plugins from monorepo
claude plugin install https://github.com/example/monorepo#all

# Install default plugin (marked with "default": true)
claude plugin install https://github.com/example/monorepo
```

## Configuration Examples

### Example 1: Simple Subdirectory Structure

For your current structure (`sample-plugin` inside the repository):

Create `.claude-repository.json` at repository root:

```json
{
  "version": "1.0.0",
  "plugins": [
    {
      "name": "devops-assistant",
      "path": "sample-plugin",
      "default": true
    }
  ]
}
```

Installation:
```bash
# Claude will automatically find the plugin in sample-plugin/
claude plugin install https://github.com/yourusername/swarm-claude-plugin
```

### Example 2: Multiple Plugins with Shared Resources

```
repository/
├── .claude-repository.json
├── plugins/
│   ├── plugin-a/
│   │   └── .claude-plugin/plugin.json
│   └── plugin-b/
│       └── .claude-plugin/plugin.json
├── shared/
│   ├── utils.js
│   └── common.py
└── README.md
```

`.claude-repository.json`:
```json
{
  "version": "1.0.0",
  "plugins": [
    {
      "name": "plugin-a",
      "path": "plugins/plugin-a"
    },
    {
      "name": "plugin-b", 
      "path": "plugins/plugin-b"
    }
  ],
  "shared": {
    "paths": ["shared"],
    "copy_to_plugin": true
  }
}
```

### Example 3: Plugin with Build Step

```json
{
  "version": "1.0.0",
  "plugins": [
    {
      "name": "devops-assistant",
      "path": "dist",
      "source_path": "src",
      "build": {
        "required": true,
        "command": "npm run build",
        "output": "dist"
      }
    }
  ]
}
```

## GitHub-Specific Features

### Using GitHub Releases

Claude can install plugins from GitHub releases:

```yaml
# .github/workflows/release.yml
name: Release Plugin

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Package Plugin
        run: |
          cd sample-plugin
          tar -czf devops-assistant-${{ github.ref_name }}.claude-plugin *
      
      - name: Create Release
        uses: actions/create-release@v1
        with:
          files: sample-plugin/devops-assistant-*.claude-plugin
```

Installation from release:
```bash
# Install latest release
claude plugin install github:example/repo

# Install specific version
claude plugin install github:example/repo@v1.0.0
```

### Using Git Tags and Branches

```bash
# Install from specific branch
claude plugin install https://github.com/example/repo#branch=develop&path=sample-plugin

# Install from tag
claude plugin install https://github.com/example/repo#tag=v1.0.0&path=sample-plugin

# Install from commit
claude plugin install https://github.com/example/repo#commit=abc123&path=sample-plugin
```

## Best Practices

### 1. Always Include Repository Manifest

Even if your plugin is at the root, include `.claude-repository.json`:

```json
{
  "version": "1.0.0",
  "plugins": [
    {
      "name": "your-plugin",
      "path": ".",
      "default": true
    }
  ]
}
```

### 2. Use Semantic Versioning

Tag your releases properly:
```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

### 3. Include Installation Instructions

In your repository README:

```markdown
## Installation

### Via Claude CLI
```bash
# Install from this repository (plugin is in sample-plugin/)
claude plugin install https://github.com/username/repo

# Or specify the path explicitly
claude plugin install https://github.com/username/repo#path=sample-plugin
```

### Manual Installation
```bash
git clone https://github.com/username/repo.git
claude plugin install ./repo/sample-plugin
```
```

### 4. Support Multiple Installation Methods

```json
{
  "version": "1.0.0",
  "plugins": [
    {
      "name": "devops-assistant",
      "path": "sample-plugin"
    }
  ],
  "installation_methods": [
    {
      "type": "claude-cli",
      "command": "claude plugin install {{repo_url}}"
    },
    {
      "type": "npm",
      "command": "npm install -g @claude-plugins/devops-assistant"
    },
    {
      "type": "script",
      "command": "curl -sSL {{repo_url}}/raw/main/install.sh | bash"
    }
  ]
}
```

## Advantages of Subdirectory Structure

1. **Better Organization**: Keep documentation, examples, and tests separate from plugin code
2. **Multiple Plugins**: Host multiple related plugins in one repository
3. **Cleaner Repository Root**: Avoid cluttering the root with plugin-specific files
4. **Easier Maintenance**: Update documentation without touching plugin code
5. **CI/CD Friendly**: Better structure for automated testing and deployment
6. **Monorepo Support**: Manage multiple plugins with shared dependencies

## Migration Guide

If you want to support both root and subdirectory discovery:

```json
{
  "version": "1.0.0",
  "plugins": [
    {
      "name": "devops-assistant",
      "path": "sample-plugin",
      "default": true,
      "aliases": [
        ".",
        "plugin",
        "devops-assistant"
      ]
    }
  ],
  "compatibility": {
    "legacy_paths": [
      ".",
      "src"
    ],
    "redirect_to": "sample-plugin"
  }
}
```

## Troubleshooting

### Plugin Not Found in Subdirectory

1. Ensure `.claude-plugin/plugin.json` exists in the subdirectory
2. Add `.claude-repository.json` to repository root
3. Use explicit path: `claude plugin install repo#path=sample-plugin`

### Multiple Plugins Conflict

Use specific plugin name:
```bash
claude plugin install https://github.com/repo#plugin=specific-plugin-name
```

### Build Required Before Installation

Add build configuration to repository manifest:
```json
{
  "plugins": [{
    "name": "plugin",
    "path": "dist",
    "build": {
      "required": true,
      "command": "npm run build"
    }
  }]
}
```

---

## Summary

**Yes, Claude fully supports plugins in subdirectories!** Your current structure with `sample-plugin` as a subdirectory is perfectly valid and even recommended. Just add a `.claude-repository.json` manifest to help Claude discover it automatically, or users can specify the path explicitly during installation.

*Last Updated: January 2024 | Claude Plugin Discovery v1.0*