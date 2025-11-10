"""
Utility module for Azure authentication.
Provides functions for authenticating with Azure services using DefaultAzureCredential.
"""

from azure.identity import DefaultAzureCredential, AzureCliCredential, ManagedIdentityCredential
from azure.core.credentials import TokenCredential
import logging

logger = logging.getLogger(__name__)


def get_azure_credential(use_cli: bool = False, use_managed_identity: bool = False) -> TokenCredential:
    """
    Get Azure credential for authentication.
    
    Uses DefaultAzureCredential by default, which tries multiple authentication methods:
    1. Environment variables
    2. Managed Identity (if running in Azure)
    3. Azure CLI (if logged in)
    4. Interactive browser (as fallback)
    
    Args:
        use_cli: Force use of Azure CLI credential
        use_managed_identity: Force use of Managed Identity credential
        
    Returns:
        TokenCredential: Azure credential object
    """
    try:
        if use_managed_identity:
            logger.info("Using Managed Identity authentication")
            return ManagedIdentityCredential()
        elif use_cli:
            logger.info("Using Azure CLI authentication")
            return AzureCliCredential()
        else:
            logger.info("Using DefaultAzureCredential (tries multiple auth methods)")
            return DefaultAzureCredential()
    except Exception as e:
        logger.error(f"Failed to get Azure credential: {str(e)}")
        raise


def verify_authentication(credential: TokenCredential) -> bool:
    """
    Verify that the credential can successfully authenticate.
    
    Args:
        credential: Azure credential to verify
        
    Returns:
        bool: True if authentication successful, False otherwise
    """
    try:
        # Try to get a token for Azure Resource Manager
        token = credential.get_token("https://management.azure.com/.default")
        if token and token.token:
            logger.info("Authentication verified successfully")
            return True
        return False
    except Exception as e:
        logger.error(f"Authentication verification failed: {str(e)}")
        return False
