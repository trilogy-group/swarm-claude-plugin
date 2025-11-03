#!/usr/bin/env python3
"""
Code Formatter Script for DevOps Assistant Plugin
Formats code according to project standards
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple

# ANSI color codes
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class CodeFormatter:
    """Main code formatter class"""
    
    def __init__(self, check_only: bool = False, fix: bool = False, verbose: bool = False):
        self.check_only = check_only
        self.fix = fix
        self.verbose = verbose
        self.issues_found = 0
        self.files_processed = 0
        self.files_fixed = 0
        
        # Language-specific configurations
        self.language_config = {
            '.js': self.format_javascript,
            '.jsx': self.format_javascript,
            '.ts': self.format_typescript,
            '.tsx': self.format_typescript,
            '.py': self.format_python,
            '.go': self.format_go,
            '.java': self.format_java,
            '.rs': self.format_rust,
            '.rb': self.format_ruby,
            '.sh': self.format_shell,
            '.yml': self.format_yaml,
            '.yaml': self.format_yaml,
            '.json': self.format_json,
            '.md': self.format_markdown
        }
    
    def log(self, message: str, level: str = 'info'):
        """Print formatted log message"""
        if level == 'error':
            print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")
        elif level == 'warning':
            print(f"{Colors.WARNING}⚠ {message}{Colors.ENDC}")
        elif level == 'success':
            print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")
        elif self.verbose:
            print(f"  {message}")
    
    def format_file(self, file_path: Path) -> Tuple[bool, List[str]]:
        """Format a single file based on its extension"""
        ext = file_path.suffix.lower()
        
        if ext not in self.language_config:
            return True, []
        
        self.files_processed += 1
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Call appropriate formatter
            formatted_content, issues = self.language_config[ext](content, file_path)
            
            if issues:
                self.issues_found += len(issues)
                
                if self.check_only:
                    self.log(f"{file_path}: {len(issues)} issue(s) found", 'warning')
                    for issue in issues:
                        print(f"    - {issue}")
                    return False, issues
                
                elif self.fix:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(formatted_content)
                    self.files_fixed += 1
                    self.log(f"{file_path}: Fixed {len(issues)} issue(s)", 'success')
                    return True, []
                else:
                    self.log(f"{file_path}: {len(issues)} issue(s) found (use --fix to correct)", 'warning')
                    return False, issues
            
            else:
                if self.verbose:
                    self.log(f"{file_path}: No issues found", 'success')
                return True, []
                
        except Exception as e:
            self.log(f"{file_path}: Error processing file - {e}", 'error')
            return False, [str(e)]
    
    def format_javascript(self, content: str, file_path: Path) -> Tuple[str, List[str]]:
        """Format JavaScript/JSX files"""
        issues = []
        formatted_content = content
        
        # Check for console.log statements
        if 'console.log' in content:
            issues.append("Contains console.log statements")
            if self.fix:
                formatted_content = re.sub(r'console\.log\([^)]*\);?\n?', '', formatted_content)
        
        # Check indentation (should be 2 spaces)
        lines = formatted_content.split('\n')
        for i, line in enumerate(lines):
            if line and not line.startswith(' ' * (len(line) - len(line.lstrip()))):
                if '\t' in line:
                    issues.append(f"Line {i+1}: Uses tabs instead of spaces")
                    if self.fix:
                        lines[i] = line.replace('\t', '  ')
        
        if self.fix:
            formatted_content = '\n'.join(lines)
        
        # Check for missing semicolons (simplified)
        if not content.strip().endswith(';') and content.strip() and not content.strip().endswith('}'):
            issues.append("Missing semicolon at end of file")
            if self.fix:
                formatted_content = formatted_content.rstrip() + ';\n'
        
        # Check line length
        for i, line in enumerate(lines):
            if len(line) > 100:
                issues.append(f"Line {i+1}: Exceeds 100 characters ({len(line)} chars)")
        
        return formatted_content, issues
    
    def format_typescript(self, content: str, file_path: Path) -> Tuple[str, List[str]]:
        """Format TypeScript/TSX files"""
        # Similar to JavaScript with additional TypeScript-specific checks
        formatted_content, issues = self.format_javascript(content, file_path)
        
        # Check for 'any' type usage
        if re.search(r':\s*any\b', content):
            issues.append("Uses 'any' type (consider using specific types)")
        
        return formatted_content, issues
    
    def format_python(self, content: str, file_path: Path) -> Tuple[str, List[str]]:
        """Format Python files according to PEP 8"""
        issues = []
        formatted_content = content
        lines = content.split('\n')
        
        # Check line length (PEP 8: 79 chars)
        for i, line in enumerate(lines):
            if len(line) > 120:  # Using 120 as a more practical limit
                issues.append(f"Line {i+1}: Exceeds 120 characters ({len(line)} chars)")
        
        # Check for trailing whitespace
        for i, line in enumerate(lines):
            if line.endswith(' ') or line.endswith('\t'):
                issues.append(f"Line {i+1}: Has trailing whitespace")
                if self.fix:
                    lines[i] = line.rstrip()
        
        # Check import order (simplified)
        import_lines = [i for i, line in enumerate(lines) if line.startswith('import ') or line.startswith('from ')]
        if import_lines and not all(import_lines[i] < import_lines[i+1] for i in range(len(import_lines)-1)):
            issues.append("Imports are not properly grouped")
        
        # Check for print statements (should use logging)
        if 'print(' in content:
            issues.append("Contains print statements (consider using logging)")
        
        # Check indentation (should be 4 spaces)
        for i, line in enumerate(lines):
            if '\t' in line:
                issues.append(f"Line {i+1}: Uses tabs instead of spaces")
                if self.fix:
                    lines[i] = line.replace('\t', '    ')
        
        if self.fix:
            formatted_content = '\n'.join(lines)
        
        return formatted_content, issues
    
    def format_go(self, content: str, file_path: Path) -> Tuple[str, List[str]]:
        """Format Go files"""
        issues = []
        formatted_content = content
        
        # Check for fmt.Println in production code
        if 'fmt.Println' in content:
            issues.append("Contains fmt.Println (use proper logging)")
        
        # Check for error handling
        if 'if err != nil {' not in content and 'error' in content:
            issues.append("May have unhandled errors")
        
        # Go uses tabs for indentation
        if '    ' in content:  # Four spaces
            issues.append("Uses spaces instead of tabs (Go convention is tabs)")
        
        return formatted_content, issues
    
    def format_java(self, content: str, file_path: Path) -> Tuple[str, List[str]]:
        """Format Java files"""
        issues = []
        
        # Check for System.out.println
        if 'System.out.println' in content:
            issues.append("Contains System.out.println (use proper logging)")
        
        # Check brace style
        if re.search(r'\n\s*{', content):
            issues.append("Opening brace on new line (should be on same line)")
        
        return content, issues
    
    def format_rust(self, content: str, file_path: Path) -> Tuple[str, List[str]]:
        """Format Rust files"""
        issues = []
        
        # Check for unwrap() usage
        if '.unwrap()' in content:
            issues.append("Uses .unwrap() (consider proper error handling)")
        
        # Check for println! in non-test code
        if 'println!' in content and '#[test]' not in content:
            issues.append("Contains println! macro (use proper logging)")
        
        return content, issues
    
    def format_ruby(self, content: str, file_path: Path) -> Tuple[str, List[str]]:
        """Format Ruby files"""
        issues = []
        
        # Check for puts/print
        if 'puts ' in content or 'print ' in content:
            issues.append("Contains puts/print (use proper logging)")
        
        # Check line length
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if len(line) > 120:
                issues.append(f"Line {i+1}: Exceeds 120 characters")
        
        return content, issues
    
    def format_shell(self, content: str, file_path: Path) -> Tuple[str, List[str]]:
        """Format shell scripts"""
        issues = []
        formatted_content = content
        
        # Check for shebang
        if not content.startswith('#!/'):
            issues.append("Missing shebang line")
            if self.fix:
                formatted_content = '#!/bin/bash\n' + formatted_content
        
        # Check for set -e
        if 'set -e' not in content:
            issues.append("Missing 'set -e' for error handling")
        
        # Check for unquoted variables
        if re.search(r'\$[A-Za-z_][A-Za-z0-9_]*(?!["\047])', content):
            issues.append("Contains unquoted variables")
        
        return formatted_content, issues
    
    def format_yaml(self, content: str, file_path: Path) -> Tuple[str, List[str]]:
        """Format YAML files"""
        issues = []
        lines = content.split('\n')
        
        # Check indentation (should be 2 spaces)
        for i, line in enumerate(lines):
            if '\t' in line:
                issues.append(f"Line {i+1}: Uses tabs (YAML requires spaces)")
        
        # Check for trailing spaces
        for i, line in enumerate(lines):
            if line.endswith(' '):
                issues.append(f"Line {i+1}: Has trailing whitespace")
        
        return content, issues
    
    def format_json(self, content: str, file_path: Path) -> Tuple[str, List[str]]:
        """Format JSON files"""
        issues = []
        formatted_content = content
        
        try:
            # Parse and pretty-print JSON
            data = json.loads(content)
            pretty_json = json.dumps(data, indent=2, sort_keys=True)
            
            if content != pretty_json:
                issues.append("JSON formatting inconsistent")
                if self.fix:
                    formatted_content = pretty_json + '\n'
                    
        except json.JSONDecodeError as e:
            issues.append(f"Invalid JSON: {e}")
        
        return formatted_content, issues
    
    def format_markdown(self, content: str, file_path: Path) -> Tuple[str, List[str]]:
        """Format Markdown files"""
        issues = []
        lines = content.split('\n')
        
        # Check for multiple blank lines
        blank_count = 0
        for i, line in enumerate(lines):
            if not line.strip():
                blank_count += 1
                if blank_count > 1:
                    issues.append(f"Line {i+1}: Multiple consecutive blank lines")
            else:
                blank_count = 0
        
        # Check heading style
        for i, line in enumerate(lines):
            if line.startswith('#') and not line.startswith('# '):
                if not re.match(r'^#{1,6} ', line):
                    issues.append(f"Line {i+1}: Missing space after # in heading")
        
        return content, issues
    
    def format_directory(self, directory: Path, extensions: List[str] = None):
        """Format all files in a directory"""
        if not directory.exists():
            self.log(f"Directory not found: {directory}", 'error')
            return False
        
        # Default extensions if not specified
        if not extensions:
            extensions = list(self.language_config.keys())
        
        # Find all files with specified extensions
        files = []
        for ext in extensions:
            files.extend(directory.rglob(f'*{ext}'))
        
        # Exclude common directories
        exclude_dirs = {'.git', 'node_modules', 'vendor', '.venv', 'dist', 'build', '__pycache__'}
        files = [f for f in files if not any(ex in str(f) for ex in exclude_dirs)]
        
        self.log(f"Found {len(files)} files to process", 'info')
        
        all_success = True
        for file_path in sorted(files):
            success, _ = self.format_file(file_path)
            if not success:
                all_success = False
        
        return all_success

def main():
    parser = argparse.ArgumentParser(
        description='Format code according to project standards'
    )
    parser.add_argument(
        'path',
        nargs='?',
        default='.',
        help='File or directory to format (default: current directory)'
    )
    parser.add_argument(
        '--check',
        action='store_true',
        help='Check for formatting issues without fixing'
    )
    parser.add_argument(
        '--fix',
        action='store_true',
        help='Automatically fix formatting issues'
    )
    parser.add_argument(
        '--extensions',
        nargs='+',
        help='File extensions to process (e.g., .js .py)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.check and args.fix:
        print(f"{Colors.FAIL}Error: Cannot use --check and --fix together{Colors.ENDC}")
        sys.exit(1)
    
    # Create formatter instance
    formatter = CodeFormatter(
        check_only=args.check,
        fix=args.fix,
        verbose=args.verbose
    )
    
    print(f"{Colors.HEADER}{'='*50}")
    print(f"🎨 Code Formatter")
    print(f"{'='*50}{Colors.ENDC}")
    
    path = Path(args.path)
    
    if path.is_file():
        success, _ = formatter.format_file(path)
    else:
        success = formatter.format_directory(path, args.extensions)
    
    # Print summary
    print(f"\n{Colors.HEADER}Summary:{Colors.ENDC}")
    print(f"  Files processed: {formatter.files_processed}")
    print(f"  Issues found: {formatter.issues_found}")
    print(f"  Files fixed: {formatter.files_fixed}")
    
    if formatter.issues_found > 0 and not args.fix:
        print(f"\n{Colors.WARNING}Run with --fix to automatically correct issues{Colors.ENDC}")
    
    # Exit with appropriate code
    if args.check:
        sys.exit(0 if formatter.issues_found == 0 else 1)
    else:
        sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
