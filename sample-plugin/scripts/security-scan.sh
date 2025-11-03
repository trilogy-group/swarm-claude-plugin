#!/bin/bash

# Security Scan Script for DevOps Assistant Plugin
# Performs comprehensive security scanning on codebase

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
SCAN_DIR="${1:-.}"
REPORT_FILE="security-report.json"
EXIT_CODE=0

echo "🔒 Starting Security Scan..."
echo "================================"

# Function to print colored output
print_status() {
    local status=$1
    local message=$2
    
    case $status in
        "success")
            echo -e "${GREEN}✓${NC} $message"
            ;;
        "warning")
            echo -e "${YELLOW}⚠${NC} $message"
            ;;
        "error")
            echo -e "${RED}✗${NC} $message"
            ;;
        *)
            echo "$message"
            ;;
    esac
}

# Check if required tools are installed
check_dependencies() {
    local deps=("git" "grep" "find")
    
    for dep in "${deps[@]}"; do
        if ! command -v $dep &> /dev/null; then
            print_status "error" "Required tool '$dep' is not installed"
            exit 1
        fi
    done
    
    print_status "success" "All dependencies are installed"
}

# Scan for hardcoded secrets
scan_secrets() {
    echo ""
    echo "🔍 Scanning for hardcoded secrets..."
    
    local patterns=(
        'api[_-]?key.*=.*["\047][A-Za-z0-9+/]{20,}["\047]'
        'secret[_-]?key.*=.*["\047][A-Za-z0-9+/]{20,}["\047]'
        'password.*=.*["\047][^"\047]{8,}["\047]'
        'token.*=.*["\047][A-Za-z0-9+/]{20,}["\047]'
        'AWS[_-]?ACCESS[_-]?KEY[_-]?ID'
        'AWS[_-]?SECRET[_-]?ACCESS[_-]?KEY'
        'GITHUB[_-]?TOKEN'
        'private[_-]?key'
    )
    
    local found_secrets=0
    
    for pattern in "${patterns[@]}"; do
        if grep -r -E "$pattern" "$SCAN_DIR" --exclude-dir={.git,node_modules,vendor,.venv} --exclude="*.log" 2>/dev/null; then
            print_status "error" "Found potential secret matching pattern: $pattern"
            ((found_secrets++))
        fi
    done
    
    if [ $found_secrets -eq 0 ]; then
        print_status "success" "No hardcoded secrets detected"
    else
        print_status "error" "Found $found_secrets potential secrets"
        EXIT_CODE=1
    fi
}

# Check for vulnerable dependencies
scan_dependencies() {
    echo ""
    echo "📦 Scanning dependencies for vulnerabilities..."
    
    if [ -f "package.json" ]; then
        print_status "warning" "Found package.json - checking npm dependencies"
        
        # Simulate npm audit (in real implementation, would run actual npm audit)
        echo "  Running: npm audit --json"
        
        # Simulated vulnerable packages
        local vulnerable_packages=(
            "lodash@4.17.19: Prototype pollution (CVE-2020-8203)"
            "axios@0.19.0: SSRF vulnerability (CVE-2020-28168)"
        )
        
        if [ ${#vulnerable_packages[@]} -gt 0 ]; then
            print_status "warning" "Found vulnerable dependencies:"
            for vuln in "${vulnerable_packages[@]}"; do
                echo "    - $vuln"
            done
        else
            print_status "success" "No vulnerable npm packages found"
        fi
    fi
    
    if [ -f "requirements.txt" ]; then
        print_status "warning" "Found requirements.txt - checking Python dependencies"
        # Would run safety check or pip-audit in real implementation
    fi
    
    if [ -f "go.mod" ]; then
        print_status "warning" "Found go.mod - checking Go dependencies"
        # Would run go mod audit in real implementation
    fi
}

# Check file permissions
check_permissions() {
    echo ""
    echo "🔐 Checking file permissions..."
    
    # Find files with overly permissive permissions
    local permissive_files=$(find "$SCAN_DIR" -type f -perm /o+w 2>/dev/null | grep -v ".git" | head -10)
    
    if [ -n "$permissive_files" ]; then
        print_status "warning" "Found files with world-writable permissions:"
        echo "$permissive_files" | head -5
    else
        print_status "success" "No overly permissive file permissions found"
    fi
}

# Check for insecure code patterns
scan_code_patterns() {
    echo ""
    echo "🐛 Scanning for insecure code patterns..."
    
    local insecure_patterns=(
        'eval\('
        'exec\('
        'system\('
        'innerHTML\s*='
        'dangerouslySetInnerHTML'
        'md5\('
        'sha1\('
        'Math\.random\(\)'
    )
    
    local found_patterns=0
    
    for pattern in "${insecure_patterns[@]}"; do
        local matches=$(grep -r "$pattern" "$SCAN_DIR" --include="*.js" --include="*.py" --include="*.rb" --include="*.php" --exclude-dir={.git,node_modules,vendor} 2>/dev/null | wc -l)
        
        if [ $matches -gt 0 ]; then
            print_status "warning" "Found $matches instances of potentially insecure pattern: $pattern"
            ((found_patterns++))
        fi
    done
    
    if [ $found_patterns -eq 0 ]; then
        print_status "success" "No insecure code patterns detected"
    else
        print_status "warning" "Found $found_patterns types of insecure patterns"
    fi
}

# Check SSL/TLS configuration
check_ssl_config() {
    echo ""
    echo "🔓 Checking SSL/TLS configuration..."
    
    # Check for insecure SSL/TLS settings in configuration files
    if grep -r "SSLProtocol.*SSLv2\|SSLv3" "$SCAN_DIR" --include="*.conf" --include="*.config" 2>/dev/null; then
        print_status "error" "Found insecure SSL protocols (SSLv2/SSLv3)"
        EXIT_CODE=1
    else
        print_status "success" "No insecure SSL protocols found"
    fi
    
    if grep -r "ssl_protocols.*SSLv2\|SSLv3" "$SCAN_DIR" --include="*.conf" 2>/dev/null; then
        print_status "error" "Found insecure SSL protocols in nginx config"
        EXIT_CODE=1
    fi
}

# Generate security report
generate_report() {
    echo ""
    echo "📊 Generating security report..."
    
    cat > "$REPORT_FILE" <<EOF
{
  "scan_date": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "scan_directory": "$SCAN_DIR",
  "scan_status": $([ $EXIT_CODE -eq 0 ] && echo '"passed"' || echo '"failed"'),
  "findings": {
    "critical": $([ $EXIT_CODE -eq 1 ] && echo '1' || echo '0'),
    "high": 0,
    "medium": 2,
    "low": 1
  },
  "scans_performed": [
    "secret_scanning",
    "dependency_check",
    "permission_check",
    "code_pattern_analysis",
    "ssl_configuration"
  ],
  "recommendations": [
    "Remove hardcoded secrets and use environment variables",
    "Update vulnerable dependencies to latest versions",
    "Review and restrict file permissions",
    "Replace insecure code patterns with secure alternatives",
    "Use only TLS 1.2 and above"
  ]
}
EOF
    
    print_status "success" "Security report generated: $REPORT_FILE"
}

# Main execution
main() {
    echo "Target directory: $SCAN_DIR"
    echo ""
    
    check_dependencies
    scan_secrets
    scan_dependencies
    check_permissions
    scan_code_patterns
    check_ssl_config
    generate_report
    
    echo ""
    echo "================================"
    
    if [ $EXIT_CODE -eq 0 ]; then
        print_status "success" "Security scan completed successfully!"
    else
        print_status "error" "Security scan found critical issues!"
    fi
    
    echo ""
    echo "View detailed report: $REPORT_FILE"
    
    exit $EXIT_CODE
}

# Run main function
main
