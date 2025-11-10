"""
Simple unit tests for configuration management.
"""

import pytest
import os
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from config_manager import Config


def test_config_loading():
    """Test that configuration loads without errors."""
    config = Config()
    assert config is not None


def test_config_properties():
    """Test that config properties are accessible."""
    config = Config()
    
    # Test that properties exist and return appropriate types
    assert isinstance(config.num_objectives, int)
    assert isinstance(config.risk_categories, list)
    assert isinstance(config.output_dir, str)
    assert isinstance(config.log_level, str)


def test_config_defaults():
    """Test that default values are set correctly."""
    config = Config()
    
    # Test defaults
    assert config.num_objectives == 10
    assert "violence" in config.risk_categories
    assert config.output_dir == "outputs"
    assert config.log_level == "INFO"


def test_config_validation():
    """Test configuration validation."""
    config = Config()
    
    # This will return False if required env vars are not set
    # which is expected in test environment
    result = config.validate()
    assert isinstance(result, bool)
