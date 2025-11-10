"""
Unit tests for authentication module.
"""

import pytest
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from auth import get_azure_credential


def test_get_default_credential():
    """Test getting default Azure credential."""
    credential = get_azure_credential()
    assert credential is not None


def test_get_cli_credential():
    """Test getting Azure CLI credential."""
    credential = get_azure_credential(use_cli=True)
    assert credential is not None


def test_get_managed_identity_credential():
    """Test getting Managed Identity credential."""
    # This will work in Azure environment
    credential = get_azure_credential(use_managed_identity=True)
    assert credential is not None
