"""
Humana Red Teaming Agent Package.

A Python package for running AI Red Teaming scans using PyRIT and Azure AI Foundry.
"""

__version__ = "0.1.0"

from .red_team_agent import RedTeamingAgent
from .config_manager import Config
from .results_processor import ResultsProcessor
from .auth import get_azure_credential, verify_authentication
from .logger import setup_logging, get_logger

__all__ = [
    "RedTeamingAgent",
    "Config",
    "ResultsProcessor",
    "get_azure_credential",
    "verify_authentication",
    "setup_logging",
    "get_logger",
]
