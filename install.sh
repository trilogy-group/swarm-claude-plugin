#!/bin/bash

# Claude Plugin Installation Script
# This script installs the devops-assistant plugin from the swarm-claude-plugin repository

set -e

REPO_OWNER="trilogy-group"
REPO_NAME="swarm-claude-plugin"
PLUGIN_NAME="devops-assistant"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🔧 Claude Plugin Installer"
echo "=========================="
echo ""

# Check if claude CLI is installed
if ! command -v claude &> /dev/null; then
    echo -e "${RED}❌ Error: Claude CLI is not installed${NC}"
    echo "Please install Claude CLI first: https://claude.ai/download"
    exit 1
fi

echo "📦 Installing $PLUGIN_NAME plugin..."
echo ""

# Method 1: Try GitHub format first (for public repos)
echo "→ Attempting to add GitHub repository as marketplace..."
if claude plugin marketplace add "$REPO_OWNER/$REPO_NAME" 2>/dev/null; then
    echo -e "${GREEN}✓ Marketplace added successfully${NC}"
    
    # Install the plugin
    echo "→ Installing plugin..."
    if claude plugin install "$PLUGIN_NAME" 2>/dev/null; then
        echo -e "${GREEN}✓ Plugin installed successfully${NC}"
    else
        echo -e "${YELLOW}⚠ Plugin may already be installed${NC}"
    fi
else
    # Method 2: Clone and install locally
    echo -e "${YELLOW}⚠ Direct GitHub installation failed (repository may be private)${NC}"
    echo "→ Attempting local installation method..."
    
    # Create temporary directory
    TEMP_DIR=$(mktemp -d)
    trap "rm -rf $TEMP_DIR" EXIT
    
    # Clone the repository
    echo "→ Cloning repository..."
    if git clone "https://github.com/$REPO_OWNER/$REPO_NAME.git" "$TEMP_DIR/plugin" 2>/dev/null; then
        echo -e "${GREEN}✓ Repository cloned${NC}"
        
        # Add as local marketplace
        echo "→ Adding local marketplace..."
        if claude plugin marketplace add "$TEMP_DIR/plugin"; then
            echo -e "${GREEN}✓ Local marketplace added${NC}"
            
            # Install the plugin
            echo "→ Installing plugin..."
            if claude plugin install "$PLUGIN_NAME"; then
                echo -e "${GREEN}✓ Plugin installed successfully${NC}"
            else
                echo -e "${RED}❌ Failed to install plugin${NC}"
                exit 1
            fi
        else
            echo -e "${RED}❌ Failed to add marketplace${NC}"
            echo ""
            echo "Possible issues:"
            echo "1. Missing .claude-plugin/marketplace.json file"
            echo "2. Invalid marketplace configuration"
            echo "3. Permission issues"
            exit 1
        fi
    else
        echo -e "${RED}❌ Failed to clone repository${NC}"
        echo ""
        echo "Possible issues:"
        echo "1. Repository is private - configure GitHub authentication"
        echo "2. Network connectivity issues"
        echo "3. Repository URL is incorrect"
        echo ""
        echo "For private repositories, try:"
        echo "  1. Configure SSH keys with GitHub"
        echo "  2. Use: git clone git@github.com:$REPO_OWNER/$REPO_NAME.git"
        echo "  3. Then: claude plugin marketplace add ./$REPO_NAME"
        echo "  4. Finally: claude plugin install $PLUGIN_NAME"
        exit 1
    fi
fi

echo ""
echo "🎉 Installation complete!"
echo ""
echo "Next steps:"
echo "  • Verify: claude plugin validate $PLUGIN_NAME"
echo "  • Enable: claude plugin enable $PLUGIN_NAME"
echo "  • Use: Check the plugin documentation for usage instructions"
echo ""

# Optional: Validate the installation
echo "→ Validating installation..."
if claude plugin validate "$PLUGIN_NAME" 2>/dev/null; then
    echo -e "${GREEN}✓ Plugin validation successful${NC}"
else
    echo -e "${YELLOW}⚠ Plugin validation command not available or plugin needs configuration${NC}"
fi

echo ""
echo "📚 For more information, see:"
echo "  • Repository: https://github.com/$REPO_OWNER/$REPO_NAME"
echo "  • Documentation: https://github.com/$REPO_OWNER/$REPO_NAME/blob/main/README.md"
echo ""
