#!/bin/bash

# DevOps Assistant Plugin Installer for Claude
# This script automates the installation of the DevOps Assistant Plugin

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
PLUGIN_NAME="devops-assistant"
PLUGIN_VERSION="1.0.0"
CLAUDE_HOME="${CLAUDE_HOME:-$HOME/.claude}"
PLUGIN_DIR="${CLAUDE_PLUGINS_DIR:-$CLAUDE_HOME/plugins}/$PLUGIN_NAME"
CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ASCII Art Banner
print_banner() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════╗"
    echo "║         DevOps Assistant Plugin Installer           ║"
    echo "║                  for Claude AI                      ║"
    echo "║                 Version $PLUGIN_VERSION                     ║"
    echo "╚══════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Logging functions
log_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

log_success() {
    echo -e "${GREEN}✓${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

log_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        log_warning "This script should not be run as root"
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

# Check system requirements
check_requirements() {
    log_info "Checking system requirements..."
    
    local missing_deps=()
    
    # Check for required commands
    local required_commands=("git" "curl" "python3" "node" "npm")
    
    for cmd in "${required_commands[@]}"; do
        if ! command -v "$cmd" &> /dev/null; then
            missing_deps+=("$cmd")
        else
            log_success "$cmd is installed"
        fi
    done
    
    # Check Python version
    if command -v python3 &> /dev/null; then
        python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        if (( $(echo "$python_version < 3.8" | bc -l) )); then
            log_warning "Python $python_version detected. Python 3.8+ is recommended"
        fi
    fi
    
    # Check Node.js version
    if command -v node &> /dev/null; then
        node_version=$(node --version | cut -d 'v' -f 2 | cut -d '.' -f 1)
        if (( node_version < 16 )); then
            log_warning "Node.js v$node_version detected. Node.js 16+ is recommended"
        fi
    fi
    
    if [ ${#missing_deps[@]} -gt 0 ]; then
        log_error "Missing required dependencies: ${missing_deps[*]}"
        echo ""
        echo "Please install the missing dependencies and try again."
        echo ""
        echo "Installation commands:"
        echo "  Ubuntu/Debian: sudo apt-get install ${missing_deps[*]}"
        echo "  macOS: brew install ${missing_deps[*]}"
        echo "  RHEL/CentOS: sudo yum install ${missing_deps[*]}"
        exit 1
    fi
    
    log_success "All requirements met"
}

# Check if Claude is installed
check_claude() {
    log_info "Checking Claude installation..."
    
    if command -v claude &> /dev/null; then
        claude_version=$(claude --version 2>/dev/null || echo "unknown")
        log_success "Claude is installed (version: $claude_version)"
        return 0
    else
        log_warning "Claude CLI not found in PATH"
        echo ""
        echo "The Claude CLI doesn't appear to be installed or is not in your PATH."
        echo "The plugin will be installed to: $PLUGIN_DIR"
        echo ""
        read -p "Continue with installation? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
        return 1
    fi
}

# Create necessary directories
create_directories() {
    log_info "Creating plugin directories..."
    
    mkdir -p "$CLAUDE_HOME"
    mkdir -p "$CLAUDE_HOME/plugins"
    mkdir -p "$CLAUDE_HOME/config"
    mkdir -p "$CLAUDE_HOME/cache"
    mkdir -p "$CLAUDE_HOME/logs"
    
    log_success "Directories created"
}

# Backup existing plugin if it exists
backup_existing() {
    if [ -d "$PLUGIN_DIR" ]; then
        log_warning "Existing plugin found at $PLUGIN_DIR"
        
        backup_name="${PLUGIN_NAME}-backup-$(date +%Y%m%d-%H%M%S)"
        backup_path="$CLAUDE_HOME/backups/$backup_name"
        
        log_info "Creating backup at $backup_path"
        mkdir -p "$CLAUDE_HOME/backups"
        cp -r "$PLUGIN_DIR" "$backup_path"
        
        log_success "Backup created"
        
        read -p "Remove existing plugin? (Y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Nn]$ ]]; then
            log_error "Installation aborted. Please remove or rename the existing plugin."
            exit 1
        fi
        
        rm -rf "$PLUGIN_DIR"
        log_success "Existing plugin removed"
    fi
}

# Install the plugin
install_plugin() {
    log_info "Installing DevOps Assistant Plugin..."
    
    # Copy plugin files
    log_info "Copying plugin files..."
    cp -r "$CURRENT_DIR" "$PLUGIN_DIR"
    
    # Remove the install script from the destination
    rm -f "$PLUGIN_DIR/install.sh"
    
    log_success "Plugin files copied to $PLUGIN_DIR"
    
    # Install Node.js dependencies
    if [ -f "$PLUGIN_DIR/package.json" ]; then
        log_info "Installing Node.js dependencies..."
        cd "$PLUGIN_DIR"
        npm install --production --silent
        cd - > /dev/null
        log_success "Node.js dependencies installed"
    fi
    
    # Install Python dependencies
    if [ -f "$PLUGIN_DIR/requirements.txt" ]; then
        log_info "Installing Python dependencies..."
        pip3 install -q -r "$PLUGIN_DIR/requirements.txt"
        log_success "Python dependencies installed"
    fi
    
    # Set executable permissions on scripts
    log_info "Setting permissions..."
    chmod +x "$PLUGIN_DIR/scripts/"*.sh 2>/dev/null || true
    chmod +x "$PLUGIN_DIR/scripts/"*.py 2>/dev/null || true
    chmod +x "$PLUGIN_DIR/scripts/"*.js 2>/dev/null || true
    
    log_success "Permissions set"
}

# Configure the plugin
configure_plugin() {
    log_info "Configuring plugin..."
    
    # Create default configuration
    config_file="$CLAUDE_HOME/config/${PLUGIN_NAME}.json"
    
    if [ ! -f "$config_file" ]; then
        cat > "$config_file" << EOF
{
  "enabled": true,
  "version": "$PLUGIN_VERSION",
  "installed_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "path": "$PLUGIN_DIR",
  "settings": {
    "environment": "development",
    "autoLoad": true,
    "scanOnSave": false,
    "securityLevel": "standard"
  }
}
EOF
        log_success "Configuration file created"
    else
        log_info "Configuration file already exists"
    fi
    
    # Create environment file template
    env_file="$PLUGIN_DIR/.env.example"
    cat > "$env_file" << 'EOF'
# DevOps Assistant Plugin Environment Variables
# Copy this file to .env and fill in your values

# API Keys
GITHUB_TOKEN=your_github_token_here
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Monitoring
PROMETHEUS_URL=http://localhost:9090
ELASTIC_URL=http://localhost:9200

# Notifications
SLACK_WEBHOOK=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASS=your_app_password

# Security
VAULT_TOKEN=your_vault_token_here
SONARQUBE_TOKEN=your_sonarqube_token_here

# Kubernetes
K8S_TOKEN=your_kubernetes_token_here
K8S_CLUSTER_URL=https://kubernetes.default.svc

# CI/CD
JENKINS_API_KEY=your_jenkins_api_key_here
JENKINS_URL=http://jenkins.local:8080
EOF
    
    log_success "Environment template created"
    log_info "Please configure your environment variables in $PLUGIN_DIR/.env"
}

# Register with Claude
register_with_claude() {
    log_info "Registering plugin with Claude..."
    
    if command -v claude &> /dev/null; then
        # Try to register the plugin
        if claude plugin register "$PLUGIN_DIR" 2>/dev/null; then
            log_success "Plugin registered with Claude"
        else
            log_warning "Could not register plugin automatically"
            echo ""
            echo "Please register manually with:"
            echo "  claude plugin register $PLUGIN_DIR"
        fi
        
        # Try to enable the plugin
        if claude plugin enable "$PLUGIN_NAME" 2>/dev/null; then
            log_success "Plugin enabled"
        else
            log_warning "Could not enable plugin automatically"
            echo ""
            echo "Please enable manually with:"
            echo "  claude plugin enable $PLUGIN_NAME"
        fi
    else
        log_info "Claude CLI not available - skipping registration"
    fi
}

# Verify installation
verify_installation() {
    log_info "Verifying installation..."
    
    local verification_passed=true
    
    # Check if plugin directory exists
    if [ -d "$PLUGIN_DIR" ]; then
        log_success "Plugin directory exists"
    else
        log_error "Plugin directory not found"
        verification_passed=false
    fi
    
    # Check if manifest exists
    if [ -f "$PLUGIN_DIR/.claude-plugin/plugin.json" ]; then
        log_success "Plugin manifest found"
    else
        log_error "Plugin manifest not found"
        verification_passed=false
    fi
    
    # Check if at least one component exists
    if [ -d "$PLUGIN_DIR/commands" ] || [ -d "$PLUGIN_DIR/agents" ] || [ -d "$PLUGIN_DIR/skills" ]; then
        log_success "Plugin components found"
    else
        log_error "No plugin components found"
        verification_passed=false
    fi
    
    # Try to run a test command if Claude is available
    if command -v claude &> /dev/null; then
        if claude plugin test "$PLUGIN_NAME" 2>/dev/null; then
            log_success "Plugin test passed"
        else
            log_warning "Plugin test failed or not available"
        fi
    fi
    
    if [ "$verification_passed" = true ]; then
        log_success "Installation verified successfully"
        return 0
    else
        log_error "Installation verification failed"
        return 1
    fi
}

# Print post-installation instructions
print_instructions() {
    echo ""
    echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}       Installation Complete! 🎉                       ${NC}"
    echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"
    echo ""
    echo "DevOps Assistant Plugin has been installed to:"
    echo "  $PLUGIN_DIR"
    echo ""
    echo "Next steps:"
    echo ""
    echo "1. Configure environment variables:"
    echo "   cp $PLUGIN_DIR/.env.example $PLUGIN_DIR/.env"
    echo "   nano $PLUGIN_DIR/.env"
    echo ""
    echo "2. Test the plugin:"
    echo "   claude plugin test $PLUGIN_NAME"
    echo "   claude run @devops status"
    echo ""
    echo "3. View available commands:"
    echo "   claude help @devops"
    echo ""
    echo "4. Read the documentation:"
    echo "   cat $PLUGIN_DIR/README.md"
    echo "   cat $PLUGIN_DIR/QUICK_START.md"
    echo ""
    echo "For support and updates:"
    echo "  GitHub: https://github.com/example/devops-assistant-plugin"
    echo "  Docs: https://docs.claude.ai/plugins/devops-assistant"
    echo ""
    echo -e "${CYAN}Thank you for installing DevOps Assistant Plugin!${NC}"
}

# Cleanup function
cleanup() {
    if [ $? -ne 0 ]; then
        log_error "Installation failed. Cleaning up..."
        # Add cleanup logic here if needed
    fi
}

# Main installation flow
main() {
    # Set trap for cleanup
    trap cleanup EXIT
    
    # Print banner
    print_banner
    
    # Run installation steps
    check_root
    check_requirements
    check_claude
    create_directories
    backup_existing
    install_plugin
    configure_plugin
    register_with_claude
    
    # Verify installation
    if verify_installation; then
        print_instructions
        exit 0
    else
        log_error "Installation completed with errors"
        echo "Please check the logs and try manual configuration"
        exit 1
    fi
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --help|-h)
            echo "DevOps Assistant Plugin Installer"
            echo ""
            echo "Usage: ./install.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  -h, --help          Show this help message"
            echo "  --plugin-dir DIR    Custom plugin installation directory"
            echo "  --claude-home DIR   Custom Claude home directory"
            echo "  --skip-deps         Skip dependency installation"
            echo "  --force             Force installation without prompts"
            echo ""
            exit 0
            ;;
        --plugin-dir)
            PLUGIN_DIR="$2"
            shift 2
            ;;
        --claude-home)
            CLAUDE_HOME="$2"
            shift 2
            ;;
        --skip-deps)
            SKIP_DEPS=true
            shift
            ;;
        --force)
            FORCE=true
            shift
            ;;
        *)
            log_error "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Run main installation
main
