#!/usr/bin/env python3
"""
Claude DevOps Plugin - Script Integration Examples
Demonstrates integration with deployment, security, and formatting scripts
"""

import os
import json
import subprocess
import asyncio
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import tempfile


class ScriptIntegration:
    """Integration layer for plugin scripts"""
    
    def __init__(self, scripts_dir: str = "./scripts"):
        self.scripts_dir = Path(scripts_dir)
        self.execution_log = []
        self.available_scripts = {
            "deploy": "deploy.js",
            "security-scan": "security-scan.sh",
            "format-code": "format-code.py"
        }
    
    async def execute_script(self, script_name: str, args: List[str] = None, env: Dict = None) -> Dict:
        """Execute a script with given arguments"""
        if script_name not in self.available_scripts:
            return {"error": f"Unknown script: {script_name}"}
        
        script_path = self.scripts_dir / self.available_scripts[script_name]
        
        # Log execution
        execution_record = {
            "timestamp": datetime.now().isoformat(),
            "script": script_name,
            "args": args or [],
            "env": env or {}
        }
        
        print(f"\n🚀 Executing Script: {script_name}")
        print(f"   Path: {script_path}")
        if args:
            print(f"   Arguments: {' '.join(args)}")
        
        # Simulate script execution
        if script_name == "deploy":
            result = await self._execute_deploy_script(args, env)
        elif script_name == "security-scan":
            result = await self._execute_security_scan(args, env)
        elif script_name == "format-code":
            result = await self._execute_format_code(args, env)
        else:
            result = {"error": "Script execution not implemented"}
        
        execution_record["result"] = result
        self.execution_log.append(execution_record)
        
        return result
    
    async def _execute_deploy_script(self, args: List[str], env: Dict) -> Dict:
        """Simulate deployment script execution"""
        await asyncio.sleep(1)  # Simulate execution time
        
        # Parse deployment arguments
        environment = "production"
        version = "latest"
        rollback = False
        
        if args:
            for i, arg in enumerate(args):
                if arg == "--env" and i + 1 < len(args):
                    environment = args[i + 1]
                elif arg == "--version" and i + 1 < len(args):
                    version = args[i + 1]
                elif arg == "--rollback":
                    rollback = True
        
        # Simulate deployment process
        print("\n📦 Deployment Process:")
        print(f"   1. Validating configuration...")
        await asyncio.sleep(0.5)
        print(f"   2. Running pre-deployment checks...")
        await asyncio.sleep(0.5)
        print(f"   3. Backing up current state...")
        await asyncio.sleep(0.5)
        
        if rollback:
            print(f"   4. Rolling back to previous version...")
            deployment_status = "rolled_back"
        else:
            print(f"   4. Deploying version {version} to {environment}...")
            deployment_status = "deployed"
        
        await asyncio.sleep(0.5)
        print(f"   5. Running health checks...")
        await asyncio.sleep(0.5)
        print(f"   6. Updating monitoring...")
        
        return {
            "status": "success",
            "deployment": {
                "environment": environment,
                "version": version,
                "status": deployment_status,
                "timestamp": datetime.now().isoformat(),
                "duration": "2m 34s"
            },
            "validation": {
                "config_valid": True,
                "dependencies_met": True,
                "resources_available": True
            },
            "health_check": {
                "status": "passed",
                "services_healthy": 12,
                "response_time": "145ms"
            },
            "rollback_available": True,
            "deployment_url": f"https://{environment}.example.com"
        }
    
    async def _execute_security_scan(self, args: List[str], env: Dict) -> Dict:
        """Simulate security scanning script"""
        await asyncio.sleep(1)
        
        # Parse scan arguments
        scan_type = "full"
        target = "."
        output_format = "json"
        
        if args:
            for i, arg in enumerate(args):
                if arg == "--type" and i + 1 < len(args):
                    scan_type = args[i + 1]
                elif arg == "--target" and i + 1 < len(args):
                    target = args[i + 1]
                elif arg == "--format" and i + 1 < len(args):
                    output_format = args[i + 1]
        
        print("\n🔍 Security Scan Process:")
        print(f"   Scan Type: {scan_type}")
        print(f"   Target: {target}")
        
        # Simulate different scan phases
        vulnerabilities = []
        
        print("\n   Phase 1: Static Code Analysis")
        await asyncio.sleep(0.5)
        vulnerabilities.extend([
            {
                "type": "SQL_INJECTION",
                "severity": "HIGH",
                "file": "api/db_handler.py",
                "line": 42,
                "description": "Unsanitized user input in SQL query"
            },
            {
                "type": "XSS",
                "severity": "MEDIUM",
                "file": "frontend/user_profile.js",
                "line": 156,
                "description": "Unescaped user content in HTML"
            }
        ])
        
        print("   Phase 2: Dependency Scanning")
        await asyncio.sleep(0.5)
        vulnerabilities.extend([
            {
                "type": "VULNERABLE_DEPENDENCY",
                "severity": "HIGH",
                "package": "requests==2.25.0",
                "cve": "CVE-2023-12345",
                "description": "Known vulnerability in HTTP library"
            }
        ])
        
        print("   Phase 3: Secret Detection")
        await asyncio.sleep(0.5)
        vulnerabilities.extend([
            {
                "type": "HARDCODED_SECRET",
                "severity": "CRITICAL",
                "file": "config/settings.py",
                "line": 23,
                "description": "API key found in source code"
            }
        ])
        
        print("   Phase 4: Configuration Analysis")
        await asyncio.sleep(0.5)
        
        # Calculate summary
        severity_count = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for vuln in vulnerabilities:
            severity_count[vuln["severity"]] = severity_count.get(vuln["severity"], 0) + 1
        
        return {
            "status": "completed",
            "scan_type": scan_type,
            "target": target,
            "timestamp": datetime.now().isoformat(),
            "duration": "45s",
            "vulnerabilities": vulnerabilities,
            "summary": {
                "total": len(vulnerabilities),
                "critical": severity_count["CRITICAL"],
                "high": severity_count["HIGH"],
                "medium": severity_count["MEDIUM"],
                "low": severity_count["LOW"]
            },
            "recommendations": [
                "Update vulnerable dependencies",
                "Remove hardcoded secrets",
                "Implement input validation",
                "Enable security headers"
            ]
        }
    
    async def _execute_format_code(self, args: List[str], env: Dict) -> Dict:
        """Simulate code formatting script"""
        await asyncio.sleep(0.5)
        
        # Parse formatting arguments
        check_only = False
        fix = True
        target_path = "."
        languages = ["python", "javascript", "typescript"]
        
        if args:
            for arg in args:
                if arg == "--check":
                    check_only = True
                    fix = False
                elif arg == "--fix":
                    fix = True
                    check_only = False
                elif arg.startswith("--path="):
                    target_path = arg.split("=")[1]
        
        print("\n✨ Code Formatting Process:")
        print(f"   Mode: {'Check Only' if check_only else 'Fix Issues'}")
        print(f"   Target: {target_path}")
        print(f"   Languages: {', '.join(languages)}")
        
        files_processed = {}
        issues_found = {}
        issues_fixed = {}
        
        # Simulate processing different file types
        for lang in languages:
            await asyncio.sleep(0.3)
            print(f"\n   Processing {lang} files...")
            
            if lang == "python":
                files_processed[lang] = 45
                issues_found[lang] = 123
                issues_fixed[lang] = 120 if fix else 0
            elif lang == "javascript":
                files_processed[lang] = 32
                issues_found[lang] = 89
                issues_fixed[lang] = 85 if fix else 0
            elif lang == "typescript":
                files_processed[lang] = 28
                issues_found[lang] = 67
                issues_fixed[lang] = 65 if fix else 0
        
        return {
            "status": "success",
            "mode": "check" if check_only else "fix",
            "target_path": target_path,
            "timestamp": datetime.now().isoformat(),
            "files_processed": sum(files_processed.values()),
            "by_language": files_processed,
            "issues": {
                "found": sum(issues_found.values()),
                "fixed": sum(issues_fixed.values()),
                "remaining": sum(issues_found.values()) - sum(issues_fixed.values())
            },
            "details": {
                "python": {
                    "files": files_processed.get("python", 0),
                    "issues_found": issues_found.get("python", 0),
                    "issues_fixed": issues_fixed.get("python", 0),
                    "formatters": ["black", "isort", "autopep8"]
                },
                "javascript": {
                    "files": files_processed.get("javascript", 0),
                    "issues_found": issues_found.get("javascript", 0),
                    "issues_fixed": issues_fixed.get("javascript", 0),
                    "formatters": ["prettier", "eslint"]
                },
                "typescript": {
                    "files": files_processed.get("typescript", 0),
                    "issues_found": issues_found.get("typescript", 0),
                    "issues_fixed": issues_fixed.get("typescript", 0),
                    "formatters": ["prettier", "tslint"]
                }
            }
        }


class GitHooksIntegration:
    """Integration with Git hooks"""
    
    def __init__(self):
        self.hooks = {
            "pre-commit": self._pre_commit_hook,
            "pre-push": self._pre_push_hook,
            "post-merge": self._post_merge_hook,
            "prepare-commit-msg": self._prepare_commit_msg_hook
        }
    
    async def trigger_hook(self, hook_name: str, context: Dict = None) -> Dict:
        """Trigger a Git hook"""
        if hook_name not in self.hooks:
            return {"error": f"Unknown hook: {hook_name}"}
        
        print(f"\n🪝 Triggering Git Hook: {hook_name}")
        return await self.hooks[hook_name](context or {})
    
    async def _pre_commit_hook(self, context: Dict) -> Dict:
        """Pre-commit hook logic"""
        print("   Running pre-commit checks...")
        
        checks_passed = True
        messages = []
        
        # 1. Format code
        print("   ✓ Formatting code...")
        await asyncio.sleep(0.3)
        messages.append("Code formatted successfully")
        
        # 2. Run linters
        print("   ✓ Running linters...")
        await asyncio.sleep(0.3)
        linter_issues = 3
        if linter_issues > 0:
            messages.append(f"Found {linter_issues} linter issues (auto-fixed)")
        
        # 3. Security scan
        print("   ✓ Quick security scan...")
        await asyncio.sleep(0.3)
        security_issues = 0
        if security_issues > 0:
            checks_passed = False
            messages.append(f"BLOCKED: {security_issues} security issues found")
        
        # 4. Check for large files
        print("   ✓ Checking file sizes...")
        await asyncio.sleep(0.2)
        
        return {
            "hook": "pre-commit",
            "status": "passed" if checks_passed else "failed",
            "checks": {
                "formatting": "passed",
                "linting": "passed",
                "security": "passed" if security_issues == 0 else "failed",
                "file_size": "passed"
            },
            "messages": messages,
            "allow_commit": checks_passed
        }
    
    async def _pre_push_hook(self, context: Dict) -> Dict:
        """Pre-push hook logic"""
        print("   Running pre-push validation...")
        
        # Run comprehensive tests
        print("   ✓ Running test suite...")
        await asyncio.sleep(1)
        
        print("   ✓ Checking branch protection...")
        await asyncio.sleep(0.3)
        
        print("   ✓ Validating commit messages...")
        await asyncio.sleep(0.3)
        
        return {
            "hook": "pre-push",
            "status": "passed",
            "checks": {
                "tests": {"passed": 156, "failed": 0, "skipped": 3},
                "coverage": "92%",
                "branch_protection": "compliant",
                "commit_messages": "valid"
            },
            "allow_push": True
        }
    
    async def _post_merge_hook(self, context: Dict) -> Dict:
        """Post-merge hook logic"""
        print("   Running post-merge tasks...")
        
        tasks = []
        
        # 1. Install dependencies
        print("   ✓ Checking for dependency updates...")
        await asyncio.sleep(0.3)
        tasks.append("Dependencies updated")
        
        # 2. Run migrations
        print("   ✓ Checking for database migrations...")
        await asyncio.sleep(0.3)
        tasks.append("No migrations needed")
        
        # 3. Clear caches
        print("   ✓ Clearing caches...")
        await asyncio.sleep(0.2)
        tasks.append("Caches cleared")
        
        return {
            "hook": "post-merge",
            "status": "completed",
            "tasks_executed": tasks,
            "recommendations": [
                "Run full test suite",
                "Review merged changes",
                "Update documentation if needed"
            ]
        }
    
    async def _prepare_commit_msg_hook(self, context: Dict) -> Dict:
        """Prepare commit message hook"""
        original_msg = context.get("message", "")
        
        # Add ticket number if missing
        ticket_pattern = r"[A-Z]+-\d+"
        branch_name = context.get("branch", "feature/ABC-123-new-feature")
        
        import re
        ticket_match = re.search(ticket_pattern, branch_name)
        
        enhanced_msg = original_msg
        if ticket_match and ticket_match.group() not in original_msg:
            ticket = ticket_match.group()
            enhanced_msg = f"[{ticket}] {original_msg}"
        
        return {
            "hook": "prepare-commit-msg",
            "original_message": original_msg,
            "enhanced_message": enhanced_msg,
            "modifications": [
                f"Added ticket number: {ticket}" if ticket_match else "No modifications"
            ]
        }


# Workflow Examples
async def example_deployment_workflow():
    """Complete deployment workflow with scripts"""
    print("\n" + "="*70)
    print("DEPLOYMENT WORKFLOW EXAMPLE")
    print("="*70)
    
    integrator = ScriptIntegration()
    
    # Step 1: Format code before deployment
    print("\n📍 Step 1: Format and validate code")
    format_result = await integrator.execute_script(
        "format-code",
        ["--fix", "--path=./src"]
    )
    
    if format_result["issues"]["remaining"] > 0:
        print(f"   ⚠️ {format_result['issues']['remaining']} formatting issues remain")
    
    # Step 2: Security scan
    print("\n📍 Step 2: Security scan")
    security_result = await integrator.execute_script(
        "security-scan",
        ["--type", "pre-deployment", "--target", "./"]
    )
    
    if security_result["summary"]["critical"] > 0:
        print("   ❌ Critical security issues found - Deployment blocked!")
        return {"status": "blocked", "reason": "security"}
    
    # Step 3: Deploy to staging
    print("\n📍 Step 3: Deploy to staging")
    staging_result = await integrator.execute_script(
        "deploy",
        ["--env", "staging", "--version", "v2.5.0-rc1"]
    )
    
    # Step 4: Run smoke tests
    print("\n📍 Step 4: Running smoke tests on staging...")
    await asyncio.sleep(1)
    print("   ✅ Smoke tests passed")
    
    # Step 5: Deploy to production
    print("\n📍 Step 5: Deploy to production")
    prod_result = await integrator.execute_script(
        "deploy",
        ["--env", "production", "--version", "v2.5.0"],
        {"DEPLOYMENT_KEY": "prod-key-123"}
    )
    
    print("\n✅ Deployment workflow completed successfully")
    
    return {
        "workflow": "deployment",
        "status": "success",
        "steps": {
            "formatting": format_result,
            "security": security_result,
            "staging": staging_result,
            "production": prod_result
        }
    }


async def example_git_workflow():
    """Git hooks workflow example"""
    print("\n" + "="*70)
    print("GIT HOOKS WORKFLOW EXAMPLE")
    print("="*70)
    
    hooks = GitHooksIntegration()
    
    # Simulate git commit
    print("\n📝 Simulating: git commit -m 'Add new feature'")
    
    # Trigger pre-commit hook
    pre_commit_result = await hooks.trigger_hook("pre-commit", {
        "files": ["src/feature.py", "tests/test_feature.py"]
    })
    
    if not pre_commit_result["allow_commit"]:
        print("\n❌ Commit blocked by pre-commit hook")
        return {"status": "blocked", "hook": "pre-commit"}
    
    # Prepare commit message
    commit_msg_result = await hooks.trigger_hook("prepare-commit-msg", {
        "message": "Add new feature",
        "branch": "feature/JIRA-456-new-feature"
    })
    print(f"\n📝 Commit message: {commit_msg_result['enhanced_message']}")
    
    # Simulate git push
    print("\n📤 Simulating: git push origin feature-branch")
    
    # Trigger pre-push hook
    pre_push_result = await hooks.trigger_hook("pre-push", {
        "branch": "feature-branch",
        "remote": "origin"
    })
    
    if not pre_push_result["allow_push"]:
        print("\n❌ Push blocked by pre-push hook")
        return {"status": "blocked", "hook": "pre-push"}
    
    print("\n✅ Git workflow completed successfully")
    
    # Simulate merge
    print("\n🔀 Simulating: git merge feature-branch")
    
    # Trigger post-merge hook
    post_merge_result = await hooks.trigger_hook("post-merge", {
        "merged_branch": "feature-branch",
        "target_branch": "main"
    })
    
    return {
        "workflow": "git",
        "status": "success",
        "hooks_triggered": {
            "pre-commit": pre_commit_result,
            "prepare-commit-msg": commit_msg_result,
            "pre-push": pre_push_result,
            "post-merge": post_merge_result
        }
    }


async def example_security_pipeline():
    """Security-focused script pipeline"""
    print("\n" + "="*70)
    print("SECURITY PIPELINE EXAMPLE")
    print("="*70)
    
    integrator = ScriptIntegration()
    security_score = 100
    issues = []
    
    # Multiple security scans
    scan_types = [
        ("dependency", ["--type", "dependencies", "--format", "json"]),
        ("static", ["--type", "static-analysis", "--target", "./src"]),
        ("secrets", ["--type", "secrets", "--target", "./"]),
        ("configuration", ["--type", "config", "--target", "./config"])
    ]
    
    for scan_name, scan_args in scan_types:
        print(f"\n🔍 Running {scan_name} security scan...")
        result = await integrator.execute_script("security-scan", scan_args)
        
        # Deduct points based on findings
        deduction = (
            result["summary"]["critical"] * 20 +
            result["summary"]["high"] * 10 +
            result["summary"]["medium"] * 5 +
            result["summary"]["low"] * 2
        )
        security_score -= deduction
        
        if result["vulnerabilities"]:
            issues.extend(result["vulnerabilities"])
        
        print(f"   Found: {result['summary']['total']} issues")
        print(f"   Security Score: {max(security_score, 0)}/100")
    
    # Generate security report
    print("\n📊 Security Pipeline Summary:")
    print(f"   Final Security Score: {max(security_score, 0)}/100")
    print(f"   Total Issues: {len(issues)}")
    
    # Determine action based on score
    if security_score >= 80:
        print("   ✅ Security check PASSED - Deployment allowed")
        action = "deploy"
    elif security_score >= 60:
        print("   ⚠️ Security check WARNING - Manual review required")
        action = "review"
    else:
        print("   ❌ Security check FAILED - Deployment blocked")
        action = "block"
    
    return {
        "pipeline": "security",
        "security_score": max(security_score, 0),
        "total_issues": len(issues),
        "action": action,
        "scans_performed": len(scan_types)
    }


async def example_automated_maintenance():
    """Automated maintenance script workflow"""
    print("\n" + "="*70)
    print("AUTOMATED MAINTENANCE WORKFLOW")
    print("="*70)
    
    integrator = ScriptIntegration()
    tasks_completed = []
    
    # 1. Code formatting
    print("\n🧹 Task 1: Code Formatting")
    format_result = await integrator.execute_script(
        "format-code",
        ["--fix", "--path=./"]
    )
    tasks_completed.append({
        "task": "Code Formatting",
        "status": "completed",
        "files_processed": format_result["files_processed"],
        "issues_fixed": format_result["issues"]["fixed"]
    })
    
    # 2. Security patches
    print("\n🔒 Task 2: Applying Security Patches")
    await asyncio.sleep(0.5)
    print("   ✓ 3 security patches applied")
    tasks_completed.append({
        "task": "Security Patches",
        "status": "completed",
        "patches_applied": 3
    })
    
    # 3. Dependency updates
    print("\n📦 Task 3: Updating Dependencies")
    await asyncio.sleep(0.5)
    print("   ✓ 12 dependencies updated")
    tasks_completed.append({
        "task": "Dependency Updates",
        "status": "completed",
        "dependencies_updated": 12
    })
    
    # 4. Database optimization
    print("\n🗄️ Task 4: Database Optimization")
    await asyncio.sleep(0.5)
    print("   ✓ Indexes rebuilt, statistics updated")
    tasks_completed.append({
        "task": "Database Optimization",
        "status": "completed",
        "optimizations": ["indexes_rebuilt", "statistics_updated", "vacuum_completed"]
    })
    
    # 5. Cache cleanup
    print("\n🧹 Task 5: Cache Cleanup")
    await asyncio.sleep(0.5)
    print("   ✓ 2.3GB of cache cleared")
    tasks_completed.append({
        "task": "Cache Cleanup",
        "status": "completed",
        "space_freed": "2.3GB"
    })
    
    print("\n✅ Automated Maintenance Completed")
    print(f"   Tasks Completed: {len(tasks_completed)}")
    
    return {
        "workflow": "maintenance",
        "status": "success",
        "tasks": tasks_completed,
        "timestamp": datetime.now().isoformat(),
        "next_scheduled": (datetime.now().replace(hour=3, minute=0)).isoformat()
    }


async def main():
    """Main function to run all script integration examples"""
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "CLAUDE SCRIPT INTEGRATION EXAMPLES" + " "*18 + "║")
    print("║" + " "*10 + "Demonstrating Script and Hook Integrations" + " "*15 + "║")
    print("╚" + "="*68 + "╝")
    
    # Run examples
    deployment = await example_deployment_workflow()
    git_workflow = await example_git_workflow()
    security = await example_security_pipeline()
    maintenance = await example_automated_maintenance()
    
    # Summary
    print("\n" + "="*70)
    print("EXECUTION SUMMARY")
    print("="*70)
    print("✅ All script integration examples completed successfully")
    
    print("\nScripts demonstrated:")
    print("  • deploy.js - Deployment automation")
    print("  • security-scan.sh - Security scanning")
    print("  • format-code.py - Code formatting")
    
    print("\nGit hooks demonstrated:")
    print("  • pre-commit - Code quality checks")
    print("  • pre-push - Test validation")
    print("  • post-merge - Post-merge tasks")
    print("  • prepare-commit-msg - Message enhancement")
    
    print("\nWorkflows covered:")
    print("  • Complete deployment pipeline")
    print("  • Git workflow with hooks")
    print("  • Security scanning pipeline")
    print("  • Automated maintenance")
    
    # Save results
    results = {
        "deployment_workflow": deployment,
        "git_workflow": git_workflow,
        "security_pipeline": security,
        "maintenance_workflow": maintenance
    }
    
    with open("script_integration_results.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    
    print("\n📁 Results saved to script_integration_results.json")
    
    return results


if __name__ == "__main__":
    asyncio.run(main())
