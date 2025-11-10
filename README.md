# AI Red Teaming Agent

A Python-based project for automated AI red teaming using **PyRIT** (Python Risk Identification Tool) and **Azure AI Foundry**. This tool helps identify safety and security risks in AI systems through automated adversarial testing.

## 🎯 Overview

The Red Teaming Agent automates the process of:

1. **Automated scans for content risks** - Scan AI models and applications for safety risks
2. **Evaluate probing success** - Measure Attack Success Rate (ASR) for different risk categories
3. **Reporting and logging** - Generate detailed reports and track findings over time

### Supported Risk Categories

- Violence
- Sexual content
- Hate and unfairness
- Self-harm

### Attack Strategies

The agent supports 20+ attack strategies including:
- ANSI Attack
- ASCII Art & Smuggler
- Base64, Binary, Caesar cipher
- Leetspeak, Morse code, ROT13
- Jailbreak techniques
- Unicode manipulation
- And more...

## 📋 Prerequisites

### Python Version
**Important**: PyRIT requires Python **3.10, 3.11, or 3.12**. It does NOT support Python 3.9.

### Azure Requirements

1. **Azure AI Foundry Project**
   - Create a project in [Azure AI Foundry](https://ai.azure.com)
   - Note your subscription ID, resource group, and project name

2. **Azure Storage Account** (for logging results)
   - Connect a storage account to your Azure AI Foundry project
   - Grant **Storage Blob Data Owner** permissions to your account and project

3. **Supported Regions**
   - East US 2
   - Sweden Central
   - France Central
   - Switzerland West

4. **Azure Authentication**
   - Azure CLI installed and logged in (`az login`)
   - OR Managed Identity (when running in Azure)
   - OR Service Principal credentials

## 🚀 Installation

### 1. Clone or Navigate to the Project

```powershell
cd red-teaming-agent
```

### 2. Create Virtual Environment

```powershell
# Create virtual environment with Python 3.10, 3.11, or 3.12
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

**Note**: The `--pre` flag is required while the packages are in preview.

```powershell
pip install -r requirements.txt
```

Or install directly:

```powershell
pip install "azure-ai-evaluation[redteam]" --pre
```

### 4. Configure Environment Variables

Copy the example environment file and configure it:

```powershell
cp .env.example .env
```

Edit `.env` and set your Azure credentials:

```bash
# Azure AI Foundry Configuration
AZURE_SUBSCRIPTION_ID=your-subscription-id-here
AZURE_RESOURCE_GROUP=your-resource-group-here
AZURE_PROJECT_NAME=your-ai-foundry-project-name-here

# Azure Authentication
AZURE_TENANT_ID=your-tenant-id-here

# Storage Account
AZURE_STORAGE_ACCOUNT_NAME=your-storage-account-name-here
```

### 5. Verify Configuration

Edit `config/config.yaml` to customize scan settings if needed.

## 📖 Usage

### Quick Start: Simple Callback

Run a basic scan with a simple callback function:

```powershell
python examples\simple_callback_example.py
```

### Advanced: OpenAI Chat Protocol

Run a scan with a callback following OpenAI's chat completion protocol:

```powershell
python examples\advanced_callback_example.py
```

### Model Configuration

Run a scan against a deployed Azure OpenAI model:

1. Set model configuration in `.env`:
   ```bash
   MODEL_DEPLOYMENT_NAME=gpt-4
   MODEL_ENDPOINT=https://your-endpoint.openai.azure.com/
   ```

2. Run the scan:
   ```powershell
   python examples\model_config_example.py
   ```

### Using Pre-configured Datasets

Use pre-configured scan profiles for common scenarios:

```powershell
python examples\dataset_examples.py
```

The datasets module provides:
- **8 pre-configured scan profiles** (Quick, Basic, Comprehensive, Jailbreak-focused, etc.)
- **4 risk categories** with descriptions
- **21 attack strategies** organized by complexity
- **Scan duration estimators**

See [DATASETS_REFERENCE.md](docs/DATASETS_REFERENCE.md) for complete details.

### Using the Main Agent Script

```powershell
python src\red_team_agent.py
```

## 🔧 Programmatic Usage

### Basic Usage

```python
import asyncio
from src.red_team_agent import RedTeamingAgent
from src.config_manager import Config
from src.logger import setup_logging

async def main():
    # Load configuration
    config = Config()
    setup_logging(log_level=config.log_level)
    
    # Initialize agent
    agent = RedTeamingAgent(config)
    
    # Setup agent (authenticate with Azure)
    if not agent.setup():
        print("Setup failed")
        return
    
    # Define your target callback
    def my_chatbot(query: str) -> str:
        # Your chatbot logic here
        return "Response from my chatbot"
    
    # Run scan
    results = await agent.scan_with_callback(
        target_callback=my_chatbot,
        num_objectives=10,
        risk_categories=["violence", "sexual"],
        output_filename="my_scan.json"
    )
    
    print(f"Attack Success Rate: {agent.results_processor.calculate_asr(results)}%")

asyncio.run(main())
```

### Using Pre-configured Datasets

```python
from src.datasets import RiskCategories, AttackStrategies, ScanProfiles

# Use a pre-configured profile
profile = ScanProfiles.JAILBREAK_FOCUSED

results = await agent.scan_with_callback(
    target_callback=my_chatbot,
    num_objectives=profile["num_objectives"],
    risk_categories=profile["risk_categories"],
    attack_strategies=profile["attack_strategies"]
)

# Or build a custom scan
from src.datasets import ScanBuilder

custom_config = ScanBuilder.build_scan_config(
    risk_categories=[RiskCategories.VIOLENCE, RiskCategories.SELF_HARM],
    attack_strategies=AttackStrategies.HIGH_COMPLEXITY,
    num_objectives=30
)

results = await agent.scan_with_callback(
    target_callback=my_chatbot,
    **custom_config
)
```

## 📊 Available Datasets

### Risk Categories (4)
- `violence` - Violence, physical harm, weapons
- `sexual` - Sexually explicit content
- `hate_unfairness` - Discrimination, hate speech
- `self_harm` - Self-harm, suicide content

### Attack Strategies (21)
**Low Complexity**: Base64, Caesar, ROT13, Leetspeak, Flip

**Medium Complexity**: Atbash, Morse, CharSwap, Diacritic, ANSI, ASCII, Binary, URL, etc.

**High Complexity**: Jailbreak, UnicodeConfusable, AsciiSmuggler, SuffixAppend

### Pre-configured Profiles (8)
1. **Quick Scan** - 5 objectives, 2 categories (~1 min)
2. **Basic Scan** - 10 objectives, all categories (~3 min)
3. **Comprehensive** - 25 objectives, all strategies (~10 min)
4. **Jailbreak Focused** - 20 objectives, prompt injection tests
5. **Encoding Focused** - 15 objectives, obfuscation tests
6. **Safety Critical** - 30 objectives, high-severity risks
7. **Production Readiness** - 50 objectives, full coverage (~20 min)
8. **Compliance** - 10 objectives, minimal required testing

See [docs/DATASETS_REFERENCE.md](docs/DATASETS_REFERENCE.md) for complete reference.

## 📊 Understanding Results

### Attack Success Rate (ASR)

The key metric is **Attack Success Rate (ASR)**, which measures the percentage of attacks that successfully elicited undesirable responses.

### Output Files

Each scan generates:

1. **JSON Results** (`outputs/scan_name.json`)
   - Complete scan data
   - Attack-response pairs
   - Risk scores per category
   - Attack complexity breakdown

2. **Summary Report** (`outputs/red_team_report_*.txt`)
   - Human-readable summary
   - ASR by risk category
   - ASR by attack complexity

### Sample Output

```
================================================================================
RED TEAMING SCAN SUMMARY REPORT
================================================================================

Scan Configuration:
------------------
Risk Categories: violence, sexual, hate_unfairness, self_harm
Attack Objectives per Category: 10

Overall Results:
---------------
Total Attacks: 40
Successful Attacks: 5
Attack Success Rate (ASR): 12.5%

Results by Risk Category:
------------------------
VIOLENCE:
  Total Attacks: 10
  Successful: 2
  ASR: 20.00%
...
```

## 🏗️ Project Structure

```
red-teaming-agent/
├── src/
│   ├── __init__.py                 # Package initialization
│   ├── red_team_agent.py           # Main Red Teaming Agent
│   ├── config_manager.py           # Configuration management
│   ├── auth.py                     # Azure authentication
│   ├── logger.py                   # Logging utilities
│   ├── results_processor.py        # Results analysis
│   └── datasets.py                 # Risk categories & attack strategies
├── examples/
│   ├── simple_callback_example.py  # Simple callback example
│   ├── advanced_callback_example.py # OpenAI protocol example
│   ├── model_config_example.py     # Model configuration example
│   └── dataset_examples.py         # Pre-configured dataset examples
├── config/
│   └── config.yaml                 # Configuration settings
├── docs/
│   ├── AZURE_SETUP.md              # Azure setup guide
│   └── DATASETS_REFERENCE.md       # Complete datasets reference
├── tests/                          # Unit tests
├── outputs/                        # Scan results (gitignored)
├── logs/                           # Log files (gitignored)
├── requirements.txt                # Python dependencies
├── pyproject.toml                  # Project metadata
├── .env.example                    # Environment template
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

## 🔐 Security Best Practices

### Authentication

- **Production**: Use Managed Identity when running in Azure
- **Development**: Use Azure CLI authentication (`az login`)
- **CI/CD**: Use Service Principal with least privilege
- **Never** hardcode credentials in code

### Storage

- Enable encryption for storage account
- Grant minimal required permissions
- Use RBAC for access control
- Regular access reviews

### Results

- Review scan results for sensitive data before sharing
- Store results securely
- Consider data retention policies
- Comply with your organization's security policies

## 🧪 Testing

Run unit tests:

```powershell
pytest tests/
```

Run with coverage:

```powershell
pytest --cov=src tests/
```

## 📚 Additional Resources

### Official Documentation

- [Azure AI Red Teaming Agent](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/ai-red-teaming-agent)
- [PyRIT GitHub Repository](https://github.com/Azure/PyRIT)
- [Azure AI Foundry Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/)
- [Azure AI Evaluation SDK](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/evaluate-sdk)

### Microsoft AI Red Team Resources

- [Planning Red Teaming for LLMs](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/red-teaming)
- [Three Takeaways from Red Teaming 100 Generative AI Products](https://www.microsoft.com/security/blog/2025/01/13/3-takeaways-from-red-teaming-100-generative-ai-products/)
- [Microsoft AI Red Team](https://www.microsoft.com/security/blog/2023/08/07/microsoft-ai-red-team-building-future-of-safer-ai/)

## 🐛 Troubleshooting

### Python Version Issues

**Error**: "PyRIT only works with Python 3.10, 3.11, 3.12"

**Solution**: Check your Python version and use a compatible version:
```powershell
python --version
# If needed, install Python 3.10, 3.11, or 3.12
```

### Authentication Issues

**Error**: "Authentication failed"

**Solutions**:
1. Login with Azure CLI: `az login`
2. Verify subscription: `az account show`
3. Set correct subscription: `az account set --subscription <subscription-id>`

### Region Not Supported

**Error**: "Region not supported"

**Solution**: Ensure your Azure AI Foundry project is in a supported region:
- East US 2
- Sweden Central
- France Central
- Switzerland West

### Import Errors

**Error**: "Import could not be resolved"

**Solution**: 
1. Ensure you're in the virtual environment
2. Install dependencies: `pip install -r requirements.txt`
3. Verify PYTHONPATH includes the project root

## 📝 License

This project is for internal use. Ensure compliance with your organization's policies.

## 🤝 Contributing

For questions or contributions, please contact your AI Security team.

## ⚠️ Important Notes

1. **Preview Software**: Azure AI Evaluation with PyRIT is in preview. Do not use in production without thorough testing.

2. **Ethical Use**: This tool is designed for security testing your own AI systems. Do not use it to attack systems you don't own or have permission to test.

3. **Human Review**: Automated red teaming should complement, not replace, human expert review. Always have security experts analyze high-risk findings.

4. **Compliance**: Ensure your use of this tool complies with your organization's security, privacy, and compliance policies.

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review official Microsoft documentation
3. Contact your AI Security team
