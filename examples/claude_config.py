#!/usr/bin/env python3
"""
Claude Plugin Configuration - API Key and Environment Setup
Handles Claude API key from environment variables and SDK initialization
"""

import os
import sys
import json
from typing import Dict, Optional, Any
from pathlib import Path


class ClaudeConfig:
    """Configuration manager for Claude API and plugin settings"""
    
    def __init__(self):
        self.api_key = None
        self.api_base_url = None
        self.plugin_mode = None
        self.plugin_path = None
        self.config_loaded = False
        self._load_configuration()
    
    def _load_configuration(self):
        """Load configuration from environment variables and config files"""
        
        # 1. Load Claude API Key from environment
        self.api_key = os.environ.get('CLAUDE_API_KEY')
        
        # Alternative environment variable names
        if not self.api_key:
            self.api_key = os.environ.get('ANTHROPIC_API_KEY')
        
        # 2. Load API base URL (optional, for custom endpoints)
        self.api_base_url = os.environ.get(
            'CLAUDE_API_BASE_URL',
            'https://api.anthropic.com'
        )
        
        # 3. Determine plugin mode (simulation or real)
        self.plugin_mode = os.environ.get('CLAUDE_PLUGIN_MODE', 'simulation')
        
        # 4. Plugin path configuration
        self.plugin_path = os.environ.get(
            'CLAUDE_PLUGIN_PATH',
            os.path.expanduser('~/.claude/plugins/devops-assistant')
        )
        
        # 5. Load additional settings from config file if exists
        config_file = os.environ.get('CLAUDE_CONFIG_FILE')
        if config_file and os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
                if 'api_key' in config and not self.api_key:
                    self.api_key = config['api_key']
                if 'plugin_settings' in config:
                    self.plugin_settings = config['plugin_settings']
        
        self.config_loaded = True
    
    def validate(self) -> tuple[bool, str]:
        """Validate configuration"""
        if self.plugin_mode == 'real' and not self.api_key:
            return False, "CLAUDE_API_KEY environment variable is required for real mode"
        
        if self.plugin_mode not in ['simulation', 'real']:
            return False, f"Invalid CLAUDE_PLUGIN_MODE: {self.plugin_mode}"
        
        return True, "Configuration valid"
    
    def get_client(self):
        """Get Claude client instance based on configuration"""
        if self.plugin_mode == 'real':
            return self._get_real_client()
        else:
            return self._get_simulated_client()
    
    def _get_real_client(self):
        """Initialize real Claude client with API key"""
        try:
            # Import the real Claude SDK
            from anthropic import Anthropic
            
            if not self.api_key:
                raise ValueError("API key required for real mode")
            
            # Initialize Claude/Anthropic client
            client = Anthropic(
                api_key=self.api_key,
                base_url=self.api_base_url
            )
            
            print(f"✅ Connected to Claude API (Real Mode)")
            print(f"   Base URL: {self.api_base_url}")
            
            return RealClaudeClient(client, self)
            
        except ImportError:
            print("❌ anthropic package not installed. Install with: pip install anthropic")
            print("   Falling back to simulation mode...")
            return self._get_simulated_client()
        except Exception as e:
            print(f"❌ Failed to initialize Claude client: {e}")
            print("   Falling back to simulation mode...")
            return self._get_simulated_client()
    
    def _get_simulated_client(self):
        """Get simulated client for testing"""
        print("🔧 Running in simulation mode (no API key required)")
        from claude_simulation import SimulatedClaudeClient
        return SimulatedClaudeClient(self)
    
    def display_config(self):
        """Display current configuration"""
        print("\n" + "="*60)
        print("CLAUDE PLUGIN CONFIGURATION")
        print("="*60)
        print(f"Mode: {self.plugin_mode}")
        print(f"API Key: {'***' + self.api_key[-4:] if self.api_key else 'Not set'}")
        print(f"API Base URL: {self.api_base_url}")
        print(f"Plugin Path: {self.plugin_path}")
        print("="*60 + "\n")


class RealClaudeClient:
    """Wrapper for real Claude API client with plugin support"""
    
    def __init__(self, anthropic_client, config: ClaudeConfig):
        self.client = anthropic_client
        self.config = config
        self.plugin = self._load_plugin()
    
    def _load_plugin(self):
        """Load the DevOps plugin"""
        # In real implementation, this would load the actual plugin
        # For now, we'll create a plugin interface
        return DevOpsPlugin(self.client, self.config)
    
    async def execute_command(self, command: str, params: Dict = None) -> Dict:
        """Execute a plugin command using real Claude API"""
        
        # Construct the prompt for Claude
        prompt = f"""
        Execute the following DevOps plugin command:
        Command: @devops {command}
        Parameters: {json.dumps(params or {}, indent=2)}
        
        Please provide the result in JSON format.
        """
        
        try:
            # Send to Claude API
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Parse response
            result = self._parse_response(response.content)
            return result
            
        except Exception as e:
            return {"error": str(e), "status": "failed"}
    
    async def execute_agent(self, agent_name: str, task: str, context: Dict = None) -> Dict:
        """Execute an agent task using real Claude API"""
        
        prompt = f"""
        As the {agent_name} agent, execute the following task:
        Task: {task}
        Context: {json.dumps(context or {}, indent=2)}
        
        Provide detailed results in JSON format including:
        - status (success/failed)
        - findings or results
        - recommendations if applicable
        """
        
        try:
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=2000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            result = self._parse_response(response.content)
            return result
            
        except Exception as e:
            return {"error": str(e), "status": "failed"}
    
    async def apply_skill(self, skill_name: str, target: Any, options: Dict = None) -> Dict:
        """Apply a skill using real Claude API"""
        
        prompt = f"""
        Apply the {skill_name} skill to the following target:
        Target: {str(target)}
        Options: {json.dumps(options or {}, indent=2)}
        
        Provide the results in JSON format.
        """
        
        try:
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            result = self._parse_response(response.content)
            return result
            
        except Exception as e:
            return {"error": str(e), "status": "failed"}
    
    def _parse_response(self, content: str) -> Dict:
        """Parse Claude's response to extract JSON"""
        try:
            # Try to extract JSON from the response
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # Return the content as a message if no JSON found
                return {"message": content, "status": "success"}
        except json.JSONDecodeError:
            return {"message": content, "status": "success"}


class DevOpsPlugin:
    """DevOps plugin interface for real Claude client"""
    
    def __init__(self, client, config: ClaudeConfig):
        self.client = client
        self.config = config
        
    def execute_command(self, command: str, params: Dict = None) -> Dict:
        """Execute a DevOps command"""
        # This would integrate with the actual plugin command system
        return {"command": command, "params": params, "status": "executed"}
    
    def get_agent(self, agent_name: str):
        """Get an agent instance"""
        # This would return the actual agent from the plugin
        return {"agent": agent_name, "ready": True}
    
    def get_skill(self, skill_name: str):
        """Get a skill instance"""
        # This would return the actual skill from the plugin
        return {"skill": skill_name, "ready": True}


# Utility functions
def setup_claude_environment():
    """Helper to set up Claude environment from .env file"""
    try:
        from dotenv import load_dotenv
        
        # Load from .env file
        env_path = Path('.env')
        if env_path.exists():
            load_dotenv(env_path)
            print("✅ Loaded environment from .env file")
        
        # Also check parent directories
        parent_env = Path('../.env')
        if parent_env.exists():
            load_dotenv(parent_env)
            print("✅ Loaded environment from parent .env file")
            
    except ImportError:
        print("ℹ️ python-dotenv not installed. Using system environment variables only.")
        print("   Install with: pip install python-dotenv")


def check_api_key():
    """Check if API key is configured"""
    api_key = os.environ.get('CLAUDE_API_KEY') or os.environ.get('ANTHROPIC_API_KEY')
    
    if api_key:
        print(f"✅ API Key found: ***{api_key[-4:]}")
        return True
    else:
        print("⚠️ No API key found in environment variables")
        print("\nTo use real Claude API, set one of these environment variables:")
        print("  export CLAUDE_API_KEY='your-api-key'")
        print("  export ANTHROPIC_API_KEY='your-api-key'")
        print("\nOr create a .env file with:")
        print("  CLAUDE_API_KEY=your-api-key")
        return False


def get_configured_client():
    """Get a configured Claude client ready for use"""
    # Set up environment
    setup_claude_environment()
    
    # Create config
    config = ClaudeConfig()
    
    # Validate
    valid, message = config.validate()
    if not valid and config.plugin_mode == 'real':
        print(f"❌ Configuration error: {message}")
        print("   Switching to simulation mode...")
        config.plugin_mode = 'simulation'
    
    # Display configuration
    config.display_config()
    
    # Get client
    return config.get_client(), config


# Example usage
if __name__ == "__main__":
    print("🔧 Claude Plugin Configuration Test")
    print("="*60)
    
    # Check for API key
    has_key = check_api_key()
    
    # Get configured client
    client, config = get_configured_client()
    
    if config.plugin_mode == 'real':
        print("\n✅ Ready to use real Claude API")
        print("   You can now execute plugin commands with the actual API")
    else:
        print("\n🔧 Running in simulation mode")
        print("   Set CLAUDE_API_KEY to use real API")
    
    # Example environment setup instructions
    print("\n" + "="*60)
    print("ENVIRONMENT SETUP INSTRUCTIONS")
    print("="*60)
    print("""
# Option 1: Export in terminal
export CLAUDE_API_KEY='your-api-key-here'
export CLAUDE_PLUGIN_MODE='real'  # or 'simulation'

# Option 2: Create .env file
cat > .env << EOF
CLAUDE_API_KEY=your-api-key-here
CLAUDE_PLUGIN_MODE=real
CLAUDE_API_BASE_URL=https://api.anthropic.com
CLAUDE_PLUGIN_PATH=/path/to/plugin
EOF

# Option 3: Use config file
export CLAUDE_CONFIG_FILE=/path/to/config.json

# Config file format:
{
  "api_key": "your-api-key",
  "plugin_settings": {
    "mode": "real",
    "auto_load": true
  }
}
    """)
