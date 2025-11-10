# Azure AI Foundry Setup Guide

This guide walks you through setting up Azure AI Foundry for use with the Red Teaming Agent.

## Prerequisites

- Azure subscription with appropriate permissions
- Azure CLI installed and configured

## Step 1: Create Azure AI Foundry Project

### Option A: Using Azure Portal (Recommended for First-Time Setup)

1. Navigate to [Azure AI Foundry](https://ai.azure.com)

2. Click **"+ New project"**

3. Fill in the details:
   - **Project name**: `humana-red-teaming-project`
   - **Subscription**: Select your subscription
   - **Resource group**: Create new or select existing
   - **Location**: Choose a supported region:
     - East US 2
     - Sweden Central
     - France Central
     - Switzerland West

4. Click **"Create"**

5. Wait for deployment to complete

### Option B: Using Azure CLI

```powershell
# Set variables
$subscriptionId = "your-subscription-id"
$resourceGroup = "humana-ai-rg"
$location = "eastus2"
$projectName = "humana-red-teaming-project"

# Set subscription
az account set --subscription $subscriptionId

# Create resource group
az group create --name $resourceGroup --location $location

# Create AI Foundry workspace (hub)
az ml workspace create `
  --name "$projectName-hub" `
  --resource-group $resourceGroup `
  --location $location `
  --kind project

# Get workspace details
az ml workspace show `
  --name "$projectName-hub" `
  --resource-group $resourceGroup
```

## Step 2: Create and Connect Storage Account

The Red Teaming Agent requires a storage account for logging results.

### Option A: Using Bicep Template (Automated)

Microsoft provides a Bicep template for this:

```powershell
# Download the template
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/azure-ai-foundry/foundry-samples/main/samples/microsoft/infrastructure-setup/01-connections/connection-storage-account.bicep" -OutFile "storage-connection.bicep"

# Deploy the template
az deployment group create `
  --resource-group $resourceGroup `
  --template-file storage-connection.bicep `
  --parameters projectName=$projectName
```

### Option B: Manual Setup

1. **Create Storage Account**:

```powershell
$storageAccountName = "humanaredteamstorage"  # must be globally unique

az storage account create `
  --name $storageAccountName `
  --resource-group $resourceGroup `
  --location $location `
  --sku Standard_LRS `
  --kind StorageV2 `
  --encryption-services blob `
  --https-only true
```

2. **Grant Permissions**:

```powershell
# Get your user principal ID
$userId = az ad signed-in-user show --query id -o tsv

# Get the workspace/project principal ID
$workspaceId = az ml workspace show `
  --name "$projectName-hub" `
  --resource-group $resourceGroup `
  --query identity.principalId -o tsv

# Grant Storage Blob Data Owner role to your user
az role assignment create `
  --assignee $userId `
  --role "Storage Blob Data Owner" `
  --scope "/subscriptions/$subscriptionId/resourceGroups/$resourceGroup/providers/Microsoft.Storage/storageAccounts/$storageAccountName"

# Grant Storage Blob Data Owner role to the workspace
az role assignment create `
  --assignee $workspaceId `
  --role "Storage Blob Data Owner" `
  --scope "/subscriptions/$subscriptionId/resourceGroups/$resourceGroup/providers/Microsoft.Storage/storageAccounts/$storageAccountName"
```

3. **Connect to AI Foundry Project**:

In the Azure Portal:
- Go to your AI Foundry project
- Navigate to **Settings** → **Connections**
- Click **+ New connection**
- Select **Azure Blob Storage**
- Enter your storage account details
- Save

## Step 3: Verify Setup

### Get Your Configuration Values

```powershell
# Get subscription ID
az account show --query id -o tsv

# Get resource group
echo $resourceGroup

# Get project name
echo $projectName

# Get storage account name
echo $storageAccountName
```

### Update Your .env File

Copy these values to your `.env` file:

```bash
AZURE_SUBSCRIPTION_ID=<from above>
AZURE_RESOURCE_GROUP=<from above>
AZURE_PROJECT_NAME=<from above>
AZURE_STORAGE_ACCOUNT_NAME=<from above>
```

### Test Authentication

```powershell
# Login to Azure
az login

# Verify subscription
az account show

# Test access to AI Foundry
az ml workspace show `
  --name "$projectName-hub" `
  --resource-group $resourceGroup
```

## Step 4: Optional - Deploy a Model (for Model Scanning)

If you want to scan a deployed model:

### Deploy Azure OpenAI Model

```powershell
# Create Azure OpenAI resource
$openaiName = "humana-red-team-openai"

az cognitiveservices account create `
  --name $openaiName `
  --resource-group $resourceGroup `
  --location $location `
  --kind OpenAI `
  --sku S0

# Deploy a model (e.g., GPT-4)
az cognitiveservices account deployment create `
  --name $openaiName `
  --resource-group $resourceGroup `
  --deployment-name gpt-4 `
  --model-name gpt-4 `
  --model-version 0613 `
  --model-format OpenAI `
  --scale-settings-scale-type Standard
```

### Get Model Configuration

```powershell
# Get endpoint
$endpoint = az cognitiveservices account show `
  --name $openaiName `
  --resource-group $resourceGroup `
  --query properties.endpoint -o tsv

echo "MODEL_ENDPOINT=$endpoint"
echo "MODEL_DEPLOYMENT_NAME=gpt-4"
echo "MODEL_API_VERSION=2024-08-01-preview"
```

Add these to your `.env` file.

## Troubleshooting

### "Subscription not registered for Microsoft.MachineLearningServices"

```powershell
az provider register --namespace Microsoft.MachineLearningServices
az provider register --namespace Microsoft.CognitiveServices
```

### "Storage account name already taken"

Storage account names must be globally unique. Try a different name:

```powershell
$storageAccountName = "humanaredteam$(Get-Random -Maximum 9999)"
```

### Permission Issues

Ensure you have:
- **Owner** or **Contributor** role on the subscription/resource group
- **Storage Blob Data Owner** on the storage account

### Region Issues

If you get "resource not available in region" errors, use one of the supported regions:
- East US 2 (`eastus2`)
- Sweden Central (`swedencentral`)
- France Central (`francecentral`)
- Switzerland West (`switzerlandwest`)

## Next Steps

1. Verify your configuration: [QUICKSTART.md](QUICKSTART.md)
2. Run your first scan: `python examples\simple_callback_example.py`
3. Review the results in the `outputs/` directory

## Additional Resources

- [Azure AI Foundry Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/)
- [Create an Azure AI Foundry Project](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/create-projects)
- [Configure Storage for Evaluations](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/evaluations-storage-account)
