# Claude DevOps Plugin - Python Examples

This directory contains comprehensive Python examples demonstrating all functionalities of the Claude DevOps Plugin, including agents, commands, scripts, and skills.

## 🔑 API Key Configuration

The examples support both **real Claude API** integration and **simulation mode**:

### Using Real Claude API

1. **Get your API key** from [Anthropic Console](https://console.anthropic.com/account/keys)

2. **Set up environment** (choose one method):

   ```bash
   # Method 1: Environment variable
   export CLAUDE_API_KEY='your-api-key-here'
   export CLAUDE_PLUGIN_MODE='real'
   
   # Method 2: Create .env file
   cp env.example .env
   # Edit .env and add your API key
   
   # Method 3: In your Python script
   import os
   os.environ['CLAUDE_API_KEY'] = 'your-api-key'
   ```

3. **Install dependencies**:
   ```bash
   pip install anthropic python-dotenv
   ```

### Using Simulation Mode

No API key required! The examples will run with simulated responses:

```bash
export CLAUDE_PLUGIN_MODE='simulation'
# Or just run without setting any environment variables
```

## 📁 Example Files

### 1. **01_main_demo.py** - Complete Plugin Demo
Comprehensive demonstration of all plugin capabilities in one file.
- **Features**: Commands, Agents, Skills, Workflows
- **Use Case**: Understanding the full plugin ecosystem
```bash
python 01_main_demo.py
```

### 2. **02_agent_examples.py** - All 11 Agents
Demonstrates each of the 11 specialized agents with realistic scenarios.
- **Agents Covered**:
  - Security Reviewer
  - Performance Tester
  - Compliance Checker
  - Repository Initializer
  - Spec System Prompt Loader
  - Spec Requirements Writer
  - Design Spec Writer
  - Spec Tasks Writer
  - Spec Implementer
  - Test Spec Writer
  - Spec Judge
```bash
python 02_agent_examples.py
```

### 3. **03_command_examples.py** - DevOps Commands
Shows usage of `@devops status` and `@devops logs` commands.
- **Examples**: Status monitoring, log filtering, CI/CD integration
```bash
python 03_command_examples.py
```

### 4. **04_script_integration.py** - Script & Hook Integration
Demonstrates integration with deployment scripts and Git hooks.
- **Scripts**: deploy.js, security-scan.sh, format-code.py
- **Git Hooks**: pre-commit, pre-push, post-merge
```bash
python 04_script_integration.py
```

### 5. **05_skills_demo.py** - Skills Demonstration
Shows the code-reviewer and pdf-processor skills in action.
- **Skills**: Code analysis, PDF processing
- **Features**: Security scanning, document extraction, report generation
```bash
python 05_skills_demo.py
```

### 6. **01_main_demo_with_api.py** - API Integration Demo
Enhanced version that demonstrates real Claude API integration.
- **Features**: Environment variable configuration, real vs simulation modes
- **API Support**: Works with actual Claude/Anthropic API
```bash
# With API key
export CLAUDE_API_KEY='your-key'
python 01_main_demo_with_api.py

# Without API key (simulation mode)
python 01_main_demo_with_api.py
```

### Configuration Files

- **claude_config.py** - Configuration management for API keys and settings
- **claude_simulation.py** - Simulation module for testing without API
- **env.example** - Template for environment variables

## 🚀 Quick Start

### Prerequisites

Install Python dependencies based on your needs:

```bash
# Option 1: Minimal installation (just essentials)
pip install -r requirements-minimal.txt
# Or directly:
pip install anthropic python-dotenv

# Option 2: Full installation (with all recommended packages)
pip install -r requirements.txt

# Option 3: Quick setup with interactive wizard
python setup.py  # Will check and install dependencies
```

📦 **See [REQUIREMENTS.md](REQUIREMENTS.md) for detailed dependency information**

### Run All Examples
```bash
# Run main comprehensive demo
python 01_main_demo.py

# Or run specific functionality demos
python 02_agent_examples.py     # For agents
python 03_command_examples.py   # For commands
python 04_script_integration.py # For scripts
python 05_skills_demo.py       # For skills
```

## 📚 Key Concepts Demonstrated

### Agents
Specialized AI agents that activate for specific tasks:
- **Security**: Vulnerability detection, dependency scanning
- **Performance**: Load testing, benchmark analysis
- **Compliance**: Standards validation, audit logging
- **Spec-Driven**: Requirements → Design → Tasks → Implementation → Testing

### Commands
DevOps operations via simple commands:
- `@devops status`: Infrastructure and service health
- `@devops logs`: Log retrieval and analysis

### Scripts
Integration with automation scripts:
- **Deployment**: Automated deployment pipelines
- **Security Scanning**: Vulnerability detection
- **Code Formatting**: Style enforcement

### Skills
Reusable capabilities for complex operations:
- **Code Reviewer**: Multi-language code analysis
- **PDF Processor**: Document extraction and processing

## 🔄 Workflow Examples

### 1. Security Review Workflow
```python
# From 02_agent_examples.py
async def example_security_workflow():
    # Code review → Dependency scan → Secret detection
```

### 2. Deployment Pipeline
```python
# From 04_script_integration.py
async def example_deployment_workflow():
    # Format → Security scan → Deploy to staging → Deploy to production
```

### 3. Spec-Driven Development
```python
# From 02_agent_examples.py
async def example_spec_development_workflow():
    # Requirements → Design → Tasks → Implementation → Testing → Evaluation
```

## 📊 Output Files

Each example generates a JSON results file:
- `demo_results.json` - Main demo results
- `agent_demo_results.json` - Agent execution results
- `command_demo_results.json` - Command execution logs
- `script_integration_results.json` - Script execution results
- `skills_demo_results.json` - Skills processing results

## 💰 API Usage & Costs

When using **real mode** with your Claude API key:

- **API Calls**: Each command, agent, and skill execution makes an API call
- **Token Usage**: Varies based on prompt complexity and response length
- **Costs**: Check [Anthropic Pricing](https://www.anthropic.com/pricing) for current rates
- **Monitoring**: Track usage in your [Anthropic Console](https://console.anthropic.com)

**Tips to minimize costs**:
- Use simulation mode for development and testing
- Test with smaller datasets first
- Implement caching for repeated operations
- Use the `CLAUDE_PLUGIN_MODE='simulation'` for demos

## 🎯 Use Cases

### For DevOps Engineers
- Automate deployment pipelines
- Monitor infrastructure health
- Implement security scanning

### For Development Teams
- Code quality assessment
- Automated testing workflows
- Documentation processing

### For Security Teams
- Vulnerability detection
- Compliance validation
- Security policy enforcement

## 🔧 Customization

### Modify Agent Behavior
Edit agent classes in `02_agent_examples.py`:
```python
class SecurityReviewerAgent(BaseAgent):
    async def execute(self, task: str, context: Dict) -> Dict:
        # Customize security checks
```

### Add New Commands
Extend `CommandExecutor` in `03_command_examples.py`:
```python
def execute(self, command: str, params: Dict = None) -> Dict:
    if command == "your-command":
        return self._execute_your_command(params)
```

### Create Custom Skills
Add new skill classes in `05_skills_demo.py`:
```python
class YourCustomSkill:
    async def apply(self, target: Any, options: Dict) -> Dict:
        # Implement your skill logic
```

## 📝 Integration with Real Claude Plugin

These examples use simulated SDK classes for demonstration. To integrate with the real Claude plugin:

1. Replace the simulated imports:
```python
# Instead of simulated classes
from claude import Claude, plugins, agents, skills
```

2. Use actual plugin paths:
```python
plugin = plugins.load('devops-assistant')
```

3. Connect to real services:
```python
# Real command execution
result = plugin.execute_command('status', {'environment': 'production'})
```

## 🤝 Contributing

Feel free to extend these examples with:
- Additional agent implementations
- New command variations
- More complex workflows
- Integration patterns

## 📖 Documentation

For complete documentation, see:
- [USER_GUIDE.md](../USER_GUIDE.md) - Full user guide
- [QUICK_REFERENCE.md](../QUICK_REFERENCE.md) - Quick command reference
- [Plugin README](../sample-plugin/README.md) - Plugin details

## 📄 License

These examples are provided as part of the Claude DevOps Plugin under the MIT License.

---

**Note**: These examples use simulated responses for demonstration purposes. In production, they would interact with real infrastructure and services.
