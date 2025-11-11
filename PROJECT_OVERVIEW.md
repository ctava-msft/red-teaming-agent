# Project Overview: Humana Red Teaming Agent

## Summary

A comprehensive Python-based solution for automated AI red teaming using **PyRIT** (Python Risk Identification Tool) and **Azure AI Foundry**. This project enables security teams to proactively identify safety and security risks in generative AI systems.

**Project Components:**
1. **Red Teaming Agent** - Automated adversarial testing framework with PyRIT
2. **APIM-based MCP Agent** - Azure API Management gateway for Model Context Protocol (MCP) servers

## Key Features

### Red Teaming Agent

✅ **Automated Red Teaming Scans**
- Test AI systems against 100+ attack objectives per risk category
- Support for 20+ attack strategies (jailbreaks, encoding attacks, etc.)
- Coverage for violence, sexual content, hate/unfairness, and self-harm categories

✅ **Flexible Target Support**
- Simple callback functions
- OpenAI chat completion protocol
- Direct model configuration scanning
- PyRIT prompt targets

✅ **Comprehensive Reporting**
- Attack Success Rate (ASR) metrics
- Risk category breakdown
- Attack complexity analysis
- JSON and text report formats

✅ **Azure Integration**
- Secure authentication with Managed Identity or Azure CLI
- Results logging to Azure AI Foundry
- Storage account integration for compliance

✅ **Enterprise-Ready**
- Structured logging
- Configuration management
- Unit tests included
- Security best practices

### APIM-based MCP Agent

✅ **AI Gateway Architecture**
- Azure API Management as intelligent MCP server gateway
- OAuth 2.0 authentication following MCP Authorization specification
- Scalable infrastructure for multiple concurrent agent sessions

✅ **Custom Agent Tools**
- Extensible framework for building AI agent tools
- Pre-built tools: `hello_mcp`, `save_snippet`, `get_snippet`
- Azure Functions runtime for serverless execution

✅ **Enterprise Integration**
- Access to enterprise systems, databases, and APIs through MCP
- Secure agent interactions with proper authentication/authorization
- Azure Storage for agent data persistence

## Project Structure

```
humana-red-teaming-agent/
├── 📂 src/                          # Core application code
│   ├── red_team_agent.py            # Main Red Teaming Agent
│   ├── function_app.py              # ⭐ Integrated Azure Functions MCP tools
│   ├── config_manager.py            # Configuration management
│   ├── auth.py                      # Azure authentication
│   ├── logger.py                    # Logging utilities
│   ├── results_processor.py         # Results analysis
│   ├── datasets.py                  # Risk categories & attack strategies
│   ├── host.json                    # Azure Functions host configuration
│   ├── local.settings.json          # Local development settings
│   ├── .funcignore                  # Function deployment ignore rules
│   └── 📂 .vscode/                  # VS Code Azure Functions configuration
│       ├── extensions.json
│       ├── launch.json
│       ├── settings.json
│       └── tasks.json
│
├── 📂 infra/                        # Azure infrastructure (Bicep)
│   ├── main.bicep                   # Main infrastructure template
│   ├── 📂 app/                      # Application components
│   │   ├── 📂 apim-mcp/             # APIM MCP server configuration
│   │   │   ├── mcp-api.bicep        # MCP API definition
│   │   │   └── mcp-api.policy.xml   # APIM policies
│   │   └── 📂 apim-oauth/           # OAuth authentication
│   │       ├── oauth.bicep          # OAuth infrastructure
│   │       └── *.policy.xml         # OAuth policies
│   └── 📂 core/                     # Core Azure resources
│       ├── apim/                    # API Management
│       ├── storage/                 # Storage accounts
│       └── monitor/                 # Application Insights
│
├── 📂 examples/                     # Usage examples
│   ├── simple_callback_example.py   # Basic callback example
│   ├── advanced_callback_example.py # OpenAI protocol example
│   └── model_config_example.py      # Model scanning example
│
├── 📂 config/                       # Configuration files
│   └── config.yaml                  # Application settings
│
├── 📂 tests/                        # Unit tests
│   ├── test_config.py
│   ├── test_auth.py
│   └── test_results_processor.py
│
├── 📂 docs/                         # Documentation
│   ├── AZURE_SETUP.md               # Azure setup guide
│   └── DATASETS_REFERENCE.md        # Datasets reference
│
├── 📂 outputs/                      # Scan results (gitignored)
├── 📂 logs/                         # Log files (gitignored)
│
├── 📄 README.md                     # Main documentation
├── 📄 QUICKSTART.md                 # Quick start guide
├── 📄 PROJECT_OVERVIEW.md           # This file
├── 📄 INTEGRATION_SUMMARY.md        # Integration details
├── 📄 requirements.txt              # Python dependencies
├── 📄 requirements-dev.txt          # Development dependencies
├── 📄 pyproject.toml                # Project metadata
├── 📄 azure.yaml                    # Azure Developer CLI config
├── 📄 .env.example                  # Environment template
└── 📄 .gitignore                    # Git ignore rules
```

**Key Integration Points:**
- `src/function_app.py` - Integrated MCP tools that leverage `RedTeamingAgent` class
- All Azure Functions configuration files now in `src/` directory
- Deploy with `azd up` to provision APIM, Functions, and storage infrastructure

## Technology Stack

### Core Dependencies
- **azure-ai-evaluation[redteam]** - PyRIT integration for red teaming
- **azure-identity** - Azure authentication (Managed Identity/CLI)
- **azure-ai-projects** - Azure AI Foundry integration
- **python-dotenv** - Environment variable management
- **pyyaml** - Configuration file parsing

### Development Tools
- **pytest** - Unit testing framework
- **black** - Code formatting
- **flake8** - Linting
- **mypy** - Type checking

### Python Version
- **Required**: Python 3.10, 3.11, or 3.12
- **Not Supported**: Python 3.9 or earlier

## Workflow

```
1. Configure
   ├── Set up Azure AI Foundry project
   ├── Configure .env with credentials
   └── Customize config.yaml settings

2. Initialize Agent
   ├── Load configuration
   ├── Authenticate with Azure
   └── Initialize PyRIT agent

3. Define Target
   ├── Simple callback function, OR
   ├── OpenAI protocol callback, OR
   └── Model configuration

4. Run Scan
   ├── Generate attack objectives
   ├── Apply attack strategies
   ├── Probe target system
   └── Evaluate responses

5. Analyze Results
   ├── Calculate Attack Success Rate (ASR)
   ├── Generate summary reports
   ├── Identify high-risk findings
   └── Log to Azure AI Foundry
```

## Use Cases

### 1. Pre-Production Security Testing
Test AI applications before deployment to identify potential vulnerabilities.

### 2. Model Selection
Compare safety characteristics of different models during evaluation phase.

### 3. Continuous Monitoring
Run periodic scans to ensure ongoing compliance and safety.

### 4. Compliance Reporting
Generate detailed reports for security audits and compliance requirements.

### 5. Incident Investigation
Analyze specific scenarios or prompts that may have caused issues.

## Security & Compliance

### Authentication Methods
- ✅ **Managed Identity** (Recommended for production in Azure)
- ✅ **Azure CLI** (Recommended for local development)
- ✅ **Service Principal** (For CI/CD pipelines)
- ❌ **Never** hardcode credentials

### Data Protection
- All credentials stored in environment variables
- Results can be logged to Azure storage with encryption
- RBAC controls for access management
- Compliance with organization security policies

### Ethical Use
- ⚠️ Only test systems you own or have permission to test
- ⚠️ Human expert review required for high-risk findings
- ⚠️ Follow responsible AI practices

## Quick Start Commands

```powershell
# Setup
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your Azure credentials

# Run first scan (Python API)
python examples\simple_callback_example.py

# Run all examples
python examples\simple_callback_example.py
python examples\advanced_callback_example.py
python examples\model_config_example.py

# Deploy integrated MCP tools (Azure Functions)
azd up

# Test MCP tools
npx @modelcontextprotocol/inspector
# Connect to: https://<your-apim>.azure-api.net/mcp/sse

# Run tests
pytest tests/
```

## Integration Architecture

### Dual Interface Design

This project provides two ways to use red teaming capabilities:

**1. Python API (Direct)**
- Import and use `RedTeamingAgent` class directly
- Run scans programmatically in Python scripts
- Full control over configuration and callbacks
- Best for: Development, testing, custom integrations

**2. MCP Tools (Agent-Based)**
- Expose red teaming as tools via Azure Functions
- AI agents call tools through Azure APIM gateway
- Tools: `run_red_team_scan`, `get_scan_results`, etc.
- Best for: Agent workflows, automated testing, enterprise deployments

### Integration Flow

```
AI Agent → APIM Gateway → Azure Functions (src/function_app.py) 
                              ↓
                         RedTeamingAgent class
                              ↓
                         PyRIT + Azure AI Foundry
                              ↓
                         Azure Storage (results)
```

## Support & Resources

### Documentation
- [README.md](README.md) - Complete documentation
- [QUICKSTART.md](QUICKSTART.md) - Get started in 10 minutes
- [docs/AZURE_SETUP.md](docs/AZURE_SETUP.md) - Azure configuration guide

### Microsoft Resources
- [Azure AI Red Teaming Agent](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/ai-red-teaming-agent)
- [PyRIT on GitHub](https://github.com/Azure/PyRIT)
- [Azure AI Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/)

### Contact
- Humana AI Security Team
- Internal Slack: #ai-security
- Support Portal: [link]

## Roadmap

### Current (v0.1.0)
- ✅ Basic red teaming capabilities
- ✅ PyRIT integration
- ✅ Azure AI Foundry support
- ✅ Multiple target types
- ✅ Comprehensive reporting

### Planned (v0.2.0)
- 🔄 Web UI for results visualization
- 🔄 Custom attack strategy definitions
- 🔄 Automated remediation suggestions
- 🔄 Integration with CI/CD pipelines
- 🔄 Enhanced metrics and dashboards

### Future
- 📋 Multi-language support
- 📋 Additional risk categories
- 📋 Real-time monitoring
- 📋 Collaborative red teaming features

## Contributing

This is an internal Humana project. For contributions:
1. Create a feature branch
2. Follow code style guidelines (use `black` for formatting)
3. Add unit tests
4. Submit pull request for review

## License & Usage

- **Internal Use Only** - Humana proprietary
- Follow organization's security and compliance policies
- Do not share credentials or sensitive results externally

## Version History

### v0.1.0 (Current)
- Initial release
- Core red teaming functionality
- PyRIT and Azure AI Foundry integration
- Example applications
- Documentation and tests

---

**Last Updated**: November 10, 2025
**Maintained By**: Humana AI Security Team
**Status**: Active Development
