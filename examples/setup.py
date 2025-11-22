#!/usr/bin/env python3
"""
Quick setup script for Claude DevOps Plugin examples
Helps configure environment and test API connection
"""

import os
import sys
import subprocess
from pathlib import Path


def check_dependencies():
    """Check and install required dependencies"""
    print("🔍 Checking dependencies...")
    
    required_packages = {
        "anthropic": "Claude/Anthropic API client",
        "python-dotenv": "Environment variable management",
        "asyncio": "Async support (built-in)",
        "json": "JSON support (built-in)",
    }
    
    missing = []
    
    for package, description in required_packages.items():
        try:
            if package in ["asyncio", "json"]:
                # Built-in packages
                __import__(package)
                print(f"   ✅ {package}: {description}")
            else:
                __import__(package)
                print(f"   ✅ {package}: {description}")
        except ImportError:
            print(f"   ❌ {package}: {description} - NOT INSTALLED")
            if package not in ["asyncio", "json"]:
                missing.append(package)
    
    if missing:
        print(f"\n📦 Installing missing packages: {', '.join(missing)}")
        response = input("Install now? (y/n): ")
        if response.lower() == 'y':
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
                print("✅ Packages installed successfully!")
            except subprocess.CalledProcessError:
                print("❌ Failed to install packages. Please run manually:")
                print(f"   pip install {' '.join(missing)}")
                return False
    
    return True


def setup_env_file():
    """Set up .env file from template"""
    print("\n📄 Setting up environment file...")
    
    env_example = Path("env.example")
    env_file = Path(".env")
    
    if env_file.exists():
        print("   ✅ .env file already exists")
        response = input("   Overwrite? (y/n): ")
        if response.lower() != 'y':
            return True
    
    if not env_example.exists():
        print("   ❌ env.example not found")
        return False
    
    # Copy template
    env_file.write_text(env_example.read_text())
    print("   ✅ Created .env from template")
    
    # Prompt for API key
    print("\n🔑 API Key Configuration")
    print("   Get your key from: https://console.anthropic.com/account/keys")
    api_key = input("   Enter your Claude API key (or press Enter to skip): ").strip()
    
    if api_key:
        # Update .env file with API key
        content = env_file.read_text()
        content = content.replace("CLAUDE_API_KEY=your-api-key-here", f"CLAUDE_API_KEY={api_key}")
        
        # Ask for mode
        mode = input("   Use real API mode? (y/n, default=n): ").strip().lower()
        if mode == 'y':
            content = content.replace("CLAUDE_PLUGIN_MODE=simulation", "CLAUDE_PLUGIN_MODE=real")
        
        env_file.write_text(content)
        print("   ✅ API key configured")
        return True
    else:
        print("   ⚠️ No API key provided - will run in simulation mode")
        return True


def test_configuration():
    """Test the configuration"""
    print("\n🧪 Testing configuration...")
    
    try:
        # Import and test
        from claude_config import ClaudeConfig, check_api_key
        
        # Check API key
        has_key = check_api_key()
        
        # Create config
        config = ClaudeConfig()
        valid, message = config.validate()
        
        if valid:
            print(f"   ✅ Configuration valid: {message}")
            print(f"   Mode: {config.plugin_mode}")
            
            if config.plugin_mode == 'real':
                print("\n   🎉 Ready to use real Claude API!")
            else:
                print("\n   🎭 Running in simulation mode")
                print("      (Set API key to use real API)")
            
            return True
        else:
            print(f"   ❌ Configuration error: {message}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error testing configuration: {e}")
        return False


def run_test_demo():
    """Run a quick test demo"""
    print("\n🚀 Running test demo...")
    
    response = input("Run a quick test? (y/n): ")
    if response.lower() != 'y':
        return
    
    try:
        import asyncio
        from claude_config import get_configured_client
        
        async def quick_test():
            client, config = get_configured_client()
            
            print(f"\n   Testing in {config.plugin_mode} mode...")
            
            # Test command
            result = await client.execute_command("status", {"environment": "test"})
            print(f"   Command test: {result.get('status', 'unknown')}")
            
            # Test agent
            result = await client.execute_agent("security-reviewer", "Quick scan", {})
            print(f"   Agent test: {result.get('status', 'unknown')}")
            
            print("\n   ✅ Test completed successfully!")
        
        asyncio.run(quick_test())
        
    except Exception as e:
        print(f"   ❌ Test failed: {e}")


def show_next_steps():
    """Show next steps for the user"""
    print("\n" + "="*60)
    print("NEXT STEPS")
    print("="*60)
    
    print("""
✅ Setup complete! You can now:

1. Run the main demo:
   python 01_main_demo.py           # Original demo
   python 01_main_demo_with_api.py  # API-enabled demo

2. Test specific functionalities:
   python 02_agent_examples.py      # Test agents
   python 03_command_examples.py    # Test commands
   python 04_script_integration.py  # Test scripts
   python 05_skills_demo.py         # Test skills

3. Configure your environment:
   - Edit .env file for API settings
   - Set CLAUDE_PLUGIN_MODE='real' to use actual API
   - Set CLAUDE_PLUGIN_MODE='simulation' for testing

4. Monitor API usage:
   https://console.anthropic.com (when using real mode)

Need help? Check the README.md for detailed documentation.
    """)


def main():
    """Main setup function"""
    print("╔" + "="*58 + "╗")
    print("║" + " "*10 + "CLAUDE DEVOPS PLUGIN - SETUP WIZARD" + " "*12 + "║")
    print("╚" + "="*58 + "╝")
    
    steps = [
        ("Dependencies", check_dependencies),
        ("Environment File", setup_env_file),
        ("Configuration Test", test_configuration),
        ("Demo Test", run_test_demo)
    ]
    
    for step_name, step_func in steps:
        print(f"\n{'='*60}")
        print(f"STEP: {step_name}")
        print('='*60)
        
        success = step_func()
        if success is False:
            print(f"\n⚠️ Setup incomplete at step: {step_name}")
            print("   Please resolve issues and run setup again.")
            return
    
    show_next_steps()
    
    print("\n🎉 Setup completed successfully!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Setup cancelled by user")
    except Exception as e:
        print(f"\n❌ Setup error: {e}")
        sys.exit(1)
