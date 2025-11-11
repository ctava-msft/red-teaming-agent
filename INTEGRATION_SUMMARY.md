# Integration Summary: APIM Agent + Red Teaming Agent

## Overview

Successfully integrated the APIM-agent's MCP tools with the RedTeamingAgent class, creating a unified solution that exposes red teaming capabilities through the Model Context Protocol (MCP).

## Changes Made

### 1. Created Integrated Function App (`src/function_app.py`)

**New File:** `c:\Users\christava\Documents\src\github.com\ctava-msft\agents-top\red-teaming-agent\src\function_app.py`

**Features:**
- Imports and leverages the `RedTeamingAgent` class
- Combines original MCP tools (hello_mcp, save_snippet, get_snippet) with new red teaming tools
- New MCP tools added:
  - `run_red_team_scan` - Execute PyRIT security scans via MCP
  - `get_scan_results` - Retrieve detailed scan findings
  - `list_attack_strategies` - List available attack strategies
  - `get_risk_categories` - Get supported risk categories

**Integration Points:**
- Uses `RedTeamingAgent` class from `red_team_agent.py`
- Leverages `Config` class for configuration management
- Uses `logger` module for consistent logging
- Imports `datasets` module for attack strategies and risk categories

### 2. Copied Azure Functions Configuration Files

**Files copied to `src/`:**
- `host.json` - Azure Functions host configuration with experimental extension bundle
- `local.settings.json` - Local development settings
- `.vscode/` - VS Code configuration for Azure Functions debugging
- `.funcignore` - Files to ignore during Function deployment

### 3. Updated Dependencies (`requirements.txt`)

**Added:**
- `azure-functions>=1.18.0` - Azure Functions runtime support

**Now includes all dependencies for:**
- Red teaming (PyRIT, Azure AI Evaluation)
- Azure Functions (MCP tool hosting)
- Development tools (pytest, black, flake8, mypy)

### 4. Updated Documentation

**README.md:**
- Added "Integrated Components" section highlighting all three components
- Created "Available MCP Tools" table showing all 7 MCP tools
- Updated project structure to show `src/function_app.py` as integrated
- Added note about dual interface (Python API + MCP Tools)

**PROJECT_OVERVIEW.md:**
- Added APIM-based MCP Agent features section
- Updated project structure showing integrated `src/` directory
- Added "Integration Architecture" section explaining dual interface design
- Updated quick start commands to include MCP deployment

## Architecture

### Dual Interface Design

The solution now provides two ways to use red teaming:

1. **Python API (Direct)**
   ```python
   from src.red_team_agent import RedTeamingAgent
   agent = RedTeamingAgent(config)
   results = await agent.scan_with_callback(...)
   ```

2. **MCP Tools (Agent-Based)**
   ```json
   {
     "name": "run_red_team_scan",
     "arguments": {
       "target_description": "chatbot",
       "num_objectives": 10,
       "risk_categories": "violence,sexual"
     }
   }
   ```

### Integration Flow

```
AI Agent 
   ↓
Azure APIM Gateway (MCP endpoint)
   ↓
Azure Functions (src/function_app.py)
   ↓
RedTeamingAgent class
   ↓
PyRIT + Azure AI Foundry
   ↓
Azure Storage (scan results)
```

## MCP Tools Summary

### Utility Tools (Original)
1. **hello_mcp** - Test MCP connectivity
2. **save_snippet** - Store code/text snippets to Azure Storage
3. **get_snippet** - Retrieve stored snippets

### Red Teaming Tools (New - Integrated)
4. **run_red_team_scan** - Execute security scan using RedTeamingAgent
   - Parameters: target_description, num_objectives, risk_categories, scan_id
   - Returns: Scan summary with ASR metrics
   - Saves results to Azure Blob Storage

5. **get_scan_results** - Retrieve detailed scan findings
   - Parameters: scan_id
   - Returns: Full report with risk analysis using ResultsProcessor

6. **list_attack_strategies** - List all available attack strategies
   - Uses datasets.ATTACK_STRATEGIES
   - Returns: Formatted list with descriptions and complexity

7. **get_risk_categories** - Get supported risk categories
   - Uses datasets.RISK_CATEGORIES
   - Returns: Categories with descriptions

## Deployment

### Development
```powershell
# Install dependencies
pip install -r requirements.txt

# Run Azure Functions locally
cd src
func start
```

### Production
```powershell
# Deploy complete infrastructure
azd up
```

This provisions:
- Azure API Management (MCP gateway)
- Azure Functions (hosts src/function_app.py)
- Azure Storage (scan results + snippets)
- Azure AI Foundry (PyRIT backend)
- Authentication & monitoring

## Testing

### MCP Inspector
```powershell
npx @modelcontextprotocol/inspector
```

Connect to: `https://<your-apim>.azure-api.net/mcp/sse`

### Example Tool Call
```json
{
  "name": "run_red_team_scan",
  "arguments": {
    "target_description": "Customer service chatbot",
    "num_objectives": 10,
    "risk_categories": "violence,sexual,hate_unfairness",
    "scan_id": "test-scan-001"
  }
}
```

## Key Benefits of Integration

1. **Agent-Accessible Security Testing** - AI agents can now perform red teaming through MCP tools
2. **Reusable Core Logic** - RedTeamingAgent class used by both Python API and MCP tools
3. **Scalable Architecture** - Azure Functions + APIM provides enterprise-grade scalability
4. **Unified Codebase** - Single source of truth in `src/` directory
5. **Flexible Deployment** - Use as Python library OR as MCP service

## Original vs. Integrated

### Before
- `apim-agent/src/function_app.py` - Standalone MCP tools (snippets only)
- `src/red_team_agent.py` - Standalone red teaming agent (Python API only)
- Separate deployments and configurations

### After
- `src/function_app.py` - Integrated MCP tools + red teaming
- `src/red_team_agent.py` - Core agent class used by both interfaces
- Unified deployment with `azd up`
- Single requirements.txt with all dependencies

## Next Steps

1. **Test Integration** - Verify MCP tools work with RedTeamingAgent
2. **Update Bicep** - Ensure infrastructure deploys src/function_app.py
3. **Add Tests** - Unit tests for new MCP tools
4. **Document Examples** - Add MCP tool usage examples
5. **Production Hardening** - Error handling, retry logic, monitoring

## File Locations

```
src/
├── function_app.py          # ⭐ NEW - Integrated MCP tools
├── red_team_agent.py        # Core agent class
├── host.json                # ⭐ NEW - Functions config
├── local.settings.json      # ⭐ NEW - Local settings
├── .vscode/                 # ⭐ NEW - VS Code config
├── config_manager.py
├── auth.py
├── logger.py
├── results_processor.py
└── datasets.py

apim-agent/
└── src/
    └── function_app.py      # Original reference implementation
```

## Success Criteria

✅ RedTeamingAgent class integrated into function_app.py  
✅ All supporting files copied to src/  
✅ Dependencies updated in requirements.txt  
✅ Documentation updated (README + PROJECT_OVERVIEW)  
✅ Project structure reflects integration  
✅ Dual interface design documented  

## Integration Complete! 🎉
