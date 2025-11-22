#!/usr/bin/env python3
"""
Claude DevOps Plugin - Main Demo with API Key Support
Demonstrates using environment variables for Claude API integration
"""

import os
import sys
import json
import asyncio
from typing import Dict, List, Any
from datetime import datetime

# Import configuration modules
from claude_config import ClaudeConfig, get_configured_client, check_api_key, setup_claude_environment
from claude_simulation import SimulatedClaudeClient


class PluginDemo:
    """Main demo class with API key support"""
    
    def __init__(self):
        """Initialize demo with configured client"""
        print("\n" + "="*70)
        print("CLAUDE DEVOPS PLUGIN - API INTEGRATION DEMO")
        print("="*70)
        
        # Setup environment and get client
        self.client, self.config = get_configured_client()
        self.execution_log = []
        
        # Show operation mode
        if self.config.plugin_mode == 'real':
            print("✅ Using REAL Claude API")
            print(f"   API Key: ***{self.config.api_key[-4:]}")
        else:
            print("🎭 Using SIMULATION mode (no API calls)")
            print("   Set CLAUDE_API_KEY to use real API")
    
    async def demo_commands(self):
        """Demonstrate command functionality"""
        print("\n" + "="*70)
        print("DEMONSTRATING COMMANDS (with API)")
        print("="*70)
        
        # Status command
        print("\n📊 Executing Status Command...")
        status = await self.client.execute_command("status", {
            "environment": "production",
            "format": "json"
        })
        
        self._log_execution("command", "status", status)
        
        if self.config.plugin_mode == 'real':
            print("   [Real API Response]")
        else:
            print("   [Simulated Response]")
        
        print(f"   Status: {status.get('overall_health', status.get('status'))}")
        
        # Logs command
        print("\n📜 Executing Logs Command...")
        logs = await self.client.execute_command("logs", {
            "filter": "error",
            "tail": 20
        })
        
        self._log_execution("command", "logs", logs)
        print(f"   Found {logs.get('total', 0)} log entries")
        
        return {"status": status, "logs": logs}
    
    async def demo_agents(self):
        """Demonstrate agent functionality"""
        print("\n" + "="*70)
        print("DEMONSTRATING AGENTS (with API)")
        print("="*70)
        
        agents_to_test = [
            ("security-reviewer", "Scan code for vulnerabilities"),
            ("performance-tester", "Run performance benchmarks"),
            ("compliance-checker", "Verify SOC2 compliance")
        ]
        
        results = {}
        
        for agent_name, task in agents_to_test:
            print(f"\n🤖 Agent: {agent_name}")
            print(f"   Task: {task}")
            
            result = await self.client.execute_agent(
                agent_name,
                task,
                {"scope": "full", "environment": "production"}
            )
            
            self._log_execution("agent", agent_name, result)
            results[agent_name] = result
            
            # Display key metrics
            if "score" in result:
                print(f"   Score: {result['score']}")
            if "vulnerabilities" in result:
                print(f"   Vulnerabilities: {len(result['vulnerabilities'])}")
            
            print(f"   Status: {result.get('status', 'unknown')}")
        
        return results
    
    async def demo_skills(self):
        """Demonstrate skills functionality"""
        print("\n" + "="*70)
        print("DEMONSTRATING SKILLS (with API)")
        print("="*70)
        
        # Code reviewer skill
        print("\n💡 Code Reviewer Skill")
        code_review = await self.client.apply_skill(
            "code-reviewer",
            "main.py",
            {"language": "python", "checks": ["security", "complexity"]}
        )
        
        self._log_execution("skill", "code-reviewer", code_review)
        print(f"   Code Score: {code_review.get('score', 'N/A')}")
        
        # PDF processor skill
        print("\n📄 PDF Processor Skill")
        pdf_result = await self.client.apply_skill(
            "pdf-processor",
            "deployment_guide.pdf",
            {"operations": ["extract_text", "summarize"]}
        )
        
        self._log_execution("skill", "pdf-processor", pdf_result)
        print(f"   Pages Processed: {pdf_result.get('pages_processed', 'N/A')}")
        
        return {"code_review": code_review, "pdf_processing": pdf_result}
    
    async def demo_workflow(self):
        """Demonstrate complete workflow"""
        print("\n" + "="*70)
        print("COMPLETE WORKFLOW DEMO (with API)")
        print("="*70)
        
        print("\n🔄 CI/CD Pipeline Simulation")
        
        # Step 1: Check status
        print("\n→ Step 1: Pre-deployment status check")
        status = await self.client.execute_command("status", {"environment": "staging"})
        
        if status.get("overall_health") == "healthy" or status.get("status") == "success":
            print("   ✅ Environment healthy")
        else:
            print("   ⚠️ Environment issues detected")
        
        # Step 2: Security scan
        print("\n→ Step 2: Security scan")
        security = await self.client.execute_agent(
            "security-reviewer",
            "Scan deployment package",
            {"package": "v2.5.0"}
        )
        
        vulnerabilities = security.get("vulnerabilities", [])
        if not vulnerabilities or (isinstance(vulnerabilities, list) and len(vulnerabilities) == 0):
            print("   ✅ No critical vulnerabilities")
        else:
            print(f"   ⚠️ Found {len(vulnerabilities) if isinstance(vulnerabilities, list) else 'some'} vulnerabilities")
        
        # Step 3: Performance test
        print("\n→ Step 3: Performance validation")
        performance = await self.client.execute_agent(
            "performance-tester",
            "Run load tests",
            {"users": 1000, "duration": "5m"}
        )
        
        print(f"   Performance Status: {performance.get('status', 'unknown')}")
        
        # Step 4: Deploy decision
        print("\n→ Step 4: Deployment Decision")
        can_deploy = (
            (status.get("overall_health") == "healthy" or status.get("status") == "success") and
            len(vulnerabilities) == 0
        )
        
        if can_deploy:
            print("   ✅ DEPLOYMENT APPROVED")
        else:
            print("   ❌ DEPLOYMENT BLOCKED")
        
        return {
            "status": status,
            "security": security,
            "performance": performance,
            "can_deploy": can_deploy
        }
    
    def _log_execution(self, exec_type: str, name: str, result: Dict):
        """Log execution for tracking"""
        self.execution_log.append({
            "timestamp": datetime.now().isoformat(),
            "type": exec_type,
            "name": name,
            "mode": self.config.plugin_mode,
            "success": result.get("status") in ["success", "healthy", "operational"]
        })
    
    async def run_full_demo(self):
        """Run the complete demonstration"""
        try:
            # Run all demos
            command_results = await self.demo_commands()
            agent_results = await self.demo_agents()
            skill_results = await self.demo_skills()
            workflow_results = await self.demo_workflow()
            
            # Summary
            print("\n" + "="*70)
            print("DEMO SUMMARY")
            print("="*70)
            
            print(f"Mode: {'REAL API' if self.config.plugin_mode == 'real' else 'SIMULATION'}")
            print(f"Executions: {len(self.execution_log)}")
            
            successful = sum(1 for log in self.execution_log if log["success"])
            print(f"Successful: {successful}/{len(self.execution_log)}")
            
            if self.config.plugin_mode == 'real':
                print("\n💰 API Usage:")
                print("   Note: This demo made real API calls to Claude")
                print("   Check your Anthropic console for usage details")
            
            # Save results
            results = {
                "mode": self.config.plugin_mode,
                "timestamp": datetime.now().isoformat(),
                "api_key_configured": bool(self.config.api_key),
                "execution_log": self.execution_log,
                "results": {
                    "commands": command_results,
                    "agents": agent_results,
                    "skills": skill_results,
                    "workflow": workflow_results
                }
            }
            
            with open("demo_api_results.json", "w") as f:
                json.dump(results, f, indent=2, default=str)
            
            print("\n📁 Results saved to demo_api_results.json")
            
            return results
            
        except Exception as e:
            print(f"\n❌ Error during demo: {e}")
            if self.config.plugin_mode == 'real':
                print("   Check your API key and network connection")
            return {"error": str(e)}


def show_setup_instructions():
    """Show setup instructions for users"""
    print("\n" + "="*70)
    print("SETUP INSTRUCTIONS")
    print("="*70)
    
    print("""
To use this demo with the real Claude API:

1. Get your API key from Anthropic:
   https://console.anthropic.com/account/keys

2. Set up your environment (choose one method):

   Method A - Environment Variable:
   ┌──────────────────────────────────────┐
   │ export CLAUDE_API_KEY='your-key'    │
   │ export CLAUDE_PLUGIN_MODE='real'    │
   └──────────────────────────────────────┘

   Method B - .env File:
   ┌──────────────────────────────────────┐
   │ cp env.example .env                 │
   │ # Edit .env with your API key       │
   └──────────────────────────────────────┘

   Method C - Direct in Python:
   ┌──────────────────────────────────────┐
   │ import os                            │
   │ os.environ['CLAUDE_API_KEY'] = 'key'│
   │ os.environ['CLAUDE_PLUGIN_MODE'] = 'real'│
   └──────────────────────────────────────┘

3. Install required packages:
   pip install anthropic python-dotenv

4. Run the demo:
   python 01_main_demo_with_api.py

Without an API key, the demo runs in simulation mode.
    """)


async def main():
    """Main entry point"""
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "CLAUDE DEVOPS PLUGIN DEMO WITH API" + " "*18 + "║")
    print("║" + " "*10 + "Environment Variable Configuration Demo" + " "*18 + "║")
    print("╚" + "="*68 + "╝")
    
    # Check for API key
    has_key = check_api_key()
    
    if not has_key:
        show_setup_instructions()
        
        response = input("\nContinue in simulation mode? (y/n): ")
        if response.lower() != 'y':
            print("Exiting. Set up your API key and try again.")
            return
    
    # Run the demo
    demo = PluginDemo()
    results = await demo.run_full_demo()
    
    print("\n✅ Demo completed successfully!")
    
    return results


if __name__ == "__main__":
    # Set up environment from .env if available
    setup_claude_environment()
    
    # Run the async main function
    results = asyncio.run(main())
