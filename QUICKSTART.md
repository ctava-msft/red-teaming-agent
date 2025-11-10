# Quick Start Guide

This guide will help you get started with the AI Red Teaming Agent in under 10 minutes.

## Step 1: Verify Prerequisites (2 minutes)

### Check Python Version
```powershell
python --version
```
**Required**: Python 3.10, 3.11, or 3.12 (NOT 3.9)

### Check Azure CLI
```powershell
az --version
az login
```

### Check Azure AI Foundry Project
- Visit https://ai.azure.com
- Ensure you have a project created
- Note down:
  - Subscription ID
  - Resource Group name
  - Project name

## Step 2: Install (3 minutes)

```powershell
# Navigate to project
cd red-teaming-agent

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies (Note: --pre flag is required)
pip install "azure-ai-evaluation[redteam]" azure-identity azure-ai-projects python-dotenv pyyaml --pre
```

## Step 3: Configure (2 minutes)

### Create .env file
```powershell
cp .env.example .env
```

### Edit .env and set these values:
```bash
AZURE_SUBSCRIPTION_ID=<your-subscription-id>
AZURE_RESOURCE_GROUP=<your-resource-group>
AZURE_PROJECT_NAME=<your-project-name>
AZURE_STORAGE_ACCOUNT_NAME=<your-storage-account>
```

**To find these values:**
```powershell
# Get subscription ID
az account show --query id -o tsv

# List your AI projects
az ml workspace list --query "[].{name:name, resourceGroup:resourceGroup}" -o table
```

## Step 4: Run Your First Scan (3 minutes)

```powershell
python examples\simple_callback_example.py
```

This will:
1. Authenticate with Azure
2. Run 5 attack objectives across 2 risk categories
3. Generate results in `outputs/simple_callback_scan.json`
4. Display a summary report

## Expected Output

```
================================================================================
RED TEAMING SCAN SUMMARY REPORT
================================================================================

Scan Configuration:
------------------
Risk Categories: violence, sexual
Attack Objectives per Category: 5

Overall Results:
---------------
Total Attacks: 10
Successful Attacks: 2
Attack Success Rate (ASR): 20.0%
...
```

## Next Steps

### Customize Your Scan

Edit the example to test different configurations:

```python
results = await agent.scan_with_callback(
    target_callback=your_chatbot,
    num_objectives=20,  # More objectives = more thorough testing
    risk_categories=["violence", "sexual", "hate_unfairness", "self_harm"],  # All categories
    output_filename="my_custom_scan.json"
)
```

### Test Your Own Application

Replace the example callback with your application:

```python
def my_chatbot(query: str) -> str:
    # Your actual chatbot/AI application logic
    response = your_application.get_response(query)
    return response
```

### Review Results

Results are saved in:
- `outputs/simple_callback_scan.json` - Complete scan data
- `outputs/red_team_report_*.txt` - Human-readable summary

## Common Issues

### "No module named 'azure'"
**Solution**: Activate virtual environment
```powershell
.\venv\Scripts\Activate.ps1
```

### "Authentication failed"
**Solution**: Login to Azure
```powershell
az login
az account set --subscription <your-subscription-id>
```

### "Region not supported"
**Solution**: Your Azure AI Foundry project must be in:
- East US 2
- Sweden Central
- France Central
- Switzerland West

## Getting Help

- Review the full [README.md](README.md)
- Check [Microsoft Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/ai-red-teaming-agent)
- Contact your AI Security team

## Security Reminder

🔐 **Important**: Never commit your `.env` file to version control. It's already in `.gitignore`.
