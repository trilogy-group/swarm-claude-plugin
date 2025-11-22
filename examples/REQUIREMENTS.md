# 📦 Python Requirements Guide

This directory contains multiple requirements files for different use cases:

## Requirements Files

### 1. `requirements-minimal.txt` 🎯
**For**: Basic functionality only
```bash
pip install -r requirements-minimal.txt
```
- ✅ Smallest footprint (2 packages)
- ✅ Essential for running examples
- ✅ Best for production deployments
- ❌ No enhanced features

**Contains**: 
- `anthropic` - Claude API client
- `python-dotenv` - Environment management

### 2. `requirements.txt` 📚
**For**: Recommended setup with enhanced features
```bash
pip install -r requirements.txt
```
- ✅ All recommended packages
- ✅ Better terminal output
- ✅ API reliability features
- ✅ Development tools included

**Adds**:
- Terminal formatting (rich, tabulate, colorama)
- API reliability (tenacity, httpx)
- Data validation (pydantic)
- Testing tools (pytest)

### 3. `requirements-dev.txt` 🛠️
**For**: Full development environment
```bash
pip install -r requirements-dev.txt
```
- ✅ Everything from requirements.txt
- ✅ All development tools
- ✅ Testing and coverage
- ✅ Documentation generation
- ❌ Large installation size

**Adds**:
- Code quality tools (black, flake8, mypy)
- Testing tools (pytest, coverage)
- Documentation (sphinx, mkdocs)
- Debugging (ipython, ipdb)

### 4. `requirements-lock.txt` 🔒
**For**: Reproducible installations
```bash
pip install -r requirements-lock.txt
```
- ✅ Exact version pinning
- ✅ Reproducible builds
- ✅ CI/CD pipelines
- ❌ May become outdated

## Quick Decision Guide

Choose your installation based on your needs:

| Use Case | Requirements File | Command |
|----------|------------------|---------|
| **Just run examples** | `requirements-minimal.txt` | `pip install anthropic python-dotenv` |
| **Normal usage** | `requirements.txt` | `pip install -r requirements.txt` |
| **Development** | `requirements-dev.txt` | `pip install -r requirements-dev.txt` |
| **CI/CD Pipeline** | `requirements-lock.txt` | `pip install -r requirements-lock.txt` |

## Installation Methods

### Method 1: Direct pip install (Quickest)
```bash
# Minimal
pip install anthropic python-dotenv

# With extras
pip install anthropic python-dotenv rich tabulate colorama tenacity
```

### Method 2: Using requirements files
```bash
# Navigate to examples directory
cd /opt/mycode/trilogy/swarm-claude-plugin/examples

# Install your chosen requirements
pip install -r requirements.txt
```

### Method 3: Interactive setup
```bash
# Run the setup wizard
python setup.py
# This will check and install dependencies automatically
```

### Method 4: Virtual environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

## Dependency Details

### Core Dependencies

| Package | Version | Purpose | Required |
|---------|---------|---------|----------|
| `anthropic` | >=0.18.0 | Claude API client | Yes (for real mode) |
| `python-dotenv` | >=1.0.0 | Load .env files | Yes |

### Optional Dependencies

| Package | Version | Purpose | Benefit |
|---------|---------|---------|---------|
| `rich` | >=13.3.0 | Terminal formatting | Better output |
| `tabulate` | >=0.9.0 | Table display | Status tables |
| `colorama` | >=0.4.6 | Colors on Windows | Cross-platform |
| `tenacity` | >=8.2.0 | Retry logic | API reliability |
| `pydantic` | >=2.0.0 | Data validation | Type safety |

## Python Version Requirements

- **Minimum**: Python 3.7
- **Recommended**: Python 3.8+
- **Tested**: Python 3.8, 3.9, 3.10, 3.11, 3.12

Check your Python version:
```bash
python --version
```

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'anthropic'`
**Solution**: Install the required packages
```bash
pip install anthropic python-dotenv
```

### Issue: `pip: command not found`
**Solution**: Install pip or use python -m pip
```bash
python -m pip install -r requirements.txt
```

### Issue: Permission denied
**Solution**: Use user installation or virtual environment
```bash
# User installation
pip install --user -r requirements.txt

# Or use virtual environment (recommended)
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: Version conflicts
**Solution**: Use a clean virtual environment
```bash
python -m venv fresh_env
source fresh_env/bin/activate
pip install -r requirements-lock.txt
```

## Updating Dependencies

### Update to latest versions
```bash
# Update all packages
pip install --upgrade -r requirements.txt

# Update specific package
pip install --upgrade anthropic
```

### Generate new lock file
```bash
# After testing with latest versions
pip freeze > requirements-lock.txt
```

## Notes

- The examples work in **simulation mode** without any dependencies except Python standard library
- Only `anthropic` and `python-dotenv` are truly required for **real API mode**
- All other dependencies enhance the experience but are optional
- Use virtual environments to avoid conflicts with system packages
- Consider using `requirements-lock.txt` for production deployments
