#!/bin/bash

# Claude Plugin Listing Script
# Lists all installed Claude plugins and their status

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

echo -e "${BOLD}📦 Claude Plugin Manager${NC}"
echo "=========================="
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if Claude CLI is installed
if ! command_exists claude; then
    echo -e "${RED}❌ Error: Claude CLI is not installed${NC}"
    echo "Please install Claude CLI first: https://claude.ai/download"
    exit 1
fi

# Settings file location
SETTINGS_FILE="$HOME/.claude/settings.json"

# List installed plugins
echo -e "${BOLD}Installed Plugins:${NC}"
echo "------------------"

if [ -f "$SETTINGS_FILE" ]; then
    if command_exists jq; then
        # Use jq for pretty formatting
        plugins=$(jq -r '.enabledPlugins | to_entries[] | "\(.key)"' "$SETTINGS_FILE" 2>/dev/null)
        
        if [ -n "$plugins" ]; then
            while IFS= read -r plugin; do
                # Extract plugin name and marketplace
                plugin_name=$(echo "$plugin" | cut -d'@' -f1)
                marketplace=$(echo "$plugin" | cut -d'@' -f2)
                
                # Check if enabled
                enabled=$(jq -r ".enabledPlugins[\"$plugin\"]" "$SETTINGS_FILE" 2>/dev/null)
                
                if [ "$enabled" = "true" ]; then
                    status="${GREEN}✅ Enabled${NC}"
                else
                    status="${RED}❌ Disabled${NC}"
                fi
                
                echo -e "  • ${BLUE}$plugin_name${NC} @ $marketplace - $status"
            done <<< "$plugins"
        else
            echo -e "  ${YELLOW}No plugins installed${NC}"
        fi
    else
        # Fallback without jq
        echo -e "  ${YELLOW}⚠ Install 'jq' for better formatting${NC}"
        echo ""
        grep -o '"[^"]*@[^"]*"' "$SETTINGS_FILE" 2>/dev/null | tr -d '"' | while read plugin; do
            echo "  • $plugin"
        done || echo -e "  ${YELLOW}No plugins installed${NC}"
    fi
else
    echo -e "  ${YELLOW}No plugins installed${NC}"
fi

echo ""

# List available marketplaces
echo -e "${BOLD}Configured Marketplaces:${NC}"
echo "------------------------"

# Capture marketplace output
marketplace_output=$(claude plugin marketplace list 2>&1)

if echo "$marketplace_output" | grep -q "Configured marketplaces:"; then
    echo "$marketplace_output" | tail -n +2 | sed 's/^/  /'
else
    echo -e "  ${YELLOW}No marketplaces configured${NC}"
fi

echo ""

# Show available commands
echo -e "${BOLD}Quick Commands:${NC}"
echo "---------------"
echo "  Install plugin:    claude plugin install <plugin-name>"
echo "  Enable plugin:     claude plugin enable <plugin-name>"
echo "  Disable plugin:    claude plugin disable <plugin-name>"
echo "  Uninstall plugin:  claude plugin uninstall <plugin-name>"
echo "  Add marketplace:   claude plugin marketplace add <source>"
echo ""

# Show plugin directory locations
echo -e "${BOLD}Plugin Locations:${NC}"
echo "-----------------"
echo "  Settings:     $SETTINGS_FILE"
echo "  Marketplaces: $HOME/.claude/plugins/marketplaces/"
echo ""

# Optional: Check for updates
echo -e "${BOLD}Tips:${NC}"
echo "------"
echo "  • To update marketplaces: claude plugin marketplace update"
echo "  • To validate a plugin:   claude plugin validate <path>"
echo "  • Plugin issues? Check:   $HOME/.claude/logs/"
echo ""
