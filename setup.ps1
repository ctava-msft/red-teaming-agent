# Setup Script for Humana Red Teaming Agent
# This script automates the initial setup process

Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "Humana Red Teaming Agent - Setup Script" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check Python version
Write-Host "Step 1: Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
Write-Host "Found: $pythonVersion" -ForegroundColor Green

if ($pythonVersion -match "Python 3\.(10|11|12)") {
    Write-Host "✓ Python version is compatible" -ForegroundColor Green
} else {
    Write-Host "✗ ERROR: Python 3.10, 3.11, or 3.12 is required" -ForegroundColor Red
    Write-Host "  Your version: $pythonVersion" -ForegroundColor Red
    Write-Host "  Please install a compatible Python version" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Step 2: Check if virtual environment exists
Write-Host "Step 2: Setting up virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "✓ Virtual environment already exists" -ForegroundColor Green
    $createVenv = Read-Host "Do you want to recreate it? (y/N)"
    if ($createVenv -eq "y" -or $createVenv -eq "Y") {
        Remove-Item -Recurse -Force venv
        python -m venv venv
        Write-Host "✓ Virtual environment recreated" -ForegroundColor Green
    }
} else {
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}
Write-Host ""

# Step 3: Activate virtual environment and install dependencies
Write-Host "Step 3: Installing dependencies..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..." -ForegroundColor Gray

& .\venv\Scripts\Activate.ps1

# Upgrade pip
pip install --upgrade pip | Out-Null

# Install dependencies with --pre flag (required for preview packages)
pip install -r requirements.txt --pre

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Error installing dependencies" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Step 4: Setup .env file
Write-Host "Step 4: Configuring environment variables..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "✓ .env file already exists" -ForegroundColor Green
    $recreateEnv = Read-Host "Do you want to reconfigure it? (y/N)"
    if ($recreateEnv -ne "y" -and $recreateEnv -ne "Y") {
        Write-Host "Keeping existing .env file" -ForegroundColor Gray
    } else {
        Copy-Item .env.example .env -Force
        Write-Host "✓ .env file reset from template" -ForegroundColor Green
    }
} else {
    Copy-Item .env.example .env
    Write-Host "✓ .env file created from template" -ForegroundColor Green
}
Write-Host ""

# Step 5: Check Azure CLI
Write-Host "Step 5: Checking Azure CLI..." -ForegroundColor Yellow
try {
    $azVersion = az --version 2>&1 | Select-String "azure-cli"
    Write-Host "✓ Azure CLI is installed: $azVersion" -ForegroundColor Green
    
    # Check if logged in
    $account = az account show 2>&1
    if ($LASTEXITCODE -eq 0) {
        $accountInfo = $account | ConvertFrom-Json
        Write-Host "✓ Logged in as: $($accountInfo.user.name)" -ForegroundColor Green
        Write-Host "  Subscription: $($accountInfo.name)" -ForegroundColor Gray
    } else {
        Write-Host "⚠ Not logged in to Azure" -ForegroundColor Yellow
        $login = Read-Host "Do you want to login now? (Y/n)"
        if ($login -ne "n" -and $login -ne "N") {
            az login
        }
    }
} catch {
    Write-Host "✗ Azure CLI is not installed" -ForegroundColor Red
    Write-Host "  Please install from: https://aka.ms/azure-cli" -ForegroundColor Yellow
}
Write-Host ""

# Step 6: Provide next steps
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Configure your .env file with Azure credentials:" -ForegroundColor White
Write-Host "   notepad .env" -ForegroundColor Gray
Write-Host ""
Write-Host "   Required values:" -ForegroundColor White
Write-Host "   - AZURE_SUBSCRIPTION_ID" -ForegroundColor Gray
Write-Host "   - AZURE_RESOURCE_GROUP" -ForegroundColor Gray
Write-Host "   - AZURE_PROJECT_NAME" -ForegroundColor Gray
Write-Host "   - AZURE_STORAGE_ACCOUNT_NAME" -ForegroundColor Gray
Write-Host ""
Write-Host "2. If you don't have an Azure AI Foundry project:" -ForegroundColor White
Write-Host "   See: docs\AZURE_SETUP.md" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Run your first red teaming scan:" -ForegroundColor White
Write-Host "   python examples\simple_callback_example.py" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Review the documentation:" -ForegroundColor White
Write-Host "   - README.md - Full documentation" -ForegroundColor Gray
Write-Host "   - QUICKSTART.md - Quick start guide" -ForegroundColor Gray
Write-Host "   - PROJECT_OVERVIEW.md - Project overview" -ForegroundColor Gray
Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "For help, contact the Humana AI Security Team" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
