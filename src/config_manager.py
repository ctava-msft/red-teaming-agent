"""
Configuration Management for Red Teaming Agent.

This module handles loading and validating configuration from environment variables,
config files, and default values.
"""

import os
import yaml
from pathlib import Path
from typing import Optional, List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for Red Teaming Agent."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration.
        
        Args:
            config_path: Optional path to config.yaml file
        """
        # Load from config file if provided
        self.config_data = {}
        if config_path:
            self._load_config_file(config_path)
        else:
            # Try to find config.yaml in parent directory
            default_config = Path(__file__).parent.parent / "config" / "config.yaml"
            if default_config.exists():
                self._load_config_file(str(default_config))
        
        # Azure AI Foundry Configuration
        self.azure_subscription_id = os.getenv(
            'AZURE_SUBSCRIPTION_ID',
            self.config_data.get('azure', {}).get('subscription_id', '')
        )
        self.azure_resource_group = os.getenv(
            'AZURE_RESOURCE_GROUP',
            self.config_data.get('azure', {}).get('resource_group', '')
        )
        self.azure_project_name = os.getenv(
            'AZURE_PROJECT_NAME',
            self.config_data.get('azure', {}).get('project_name', '')
        )
        self.azure_tenant_id = os.getenv(
            'AZURE_TENANT_ID',
            self.config_data.get('azure', {}).get('tenant_id', '')
        )
        
        # Storage Configuration
        self.azure_storage_account_name = os.getenv(
            'AZURE_STORAGE_ACCOUNT_NAME',
            self.config_data.get('azure', {}).get('storage_account_name', '')
        )
        
        # Red Teaming Configuration
        red_team_config = self.config_data.get('red_teaming', {})
        self.num_objectives = int(os.getenv(
            'NUM_OBJECTIVES',
            str(red_team_config.get('num_objectives', 10))
        ))
        
        # Risk Categories
        risk_categories_env = os.getenv('RISK_CATEGORIES', '')
        if risk_categories_env:
            self.risk_categories = [cat.strip() for cat in risk_categories_env.split(',')]
        else:
            self.risk_categories = red_team_config.get('risk_categories', [
                'violence',
                'sexual',
                'hate_unfairness',
                'self_harm'
            ])
        
        # Attack Strategies
        attack_strategies_env = os.getenv('ATTACK_STRATEGIES', '')
        if attack_strategies_env:
            self.attack_strategies = [s.strip() for s in attack_strategies_env.split(',')]
        else:
            self.attack_strategies = red_team_config.get('attack_strategies', None)
        
        # ASR Threshold
        self.asr_threshold = float(os.getenv(
            'ASR_THRESHOLD',
            str(red_team_config.get('asr_threshold', 0.2))
        ))
        
        # Output Configuration
        output_config = self.config_data.get('output', {})
        self.output_dir = Path(os.getenv(
            'OUTPUT_DIR',
            output_config.get('directory', './outputs')
        ))
        self.output_format = os.getenv(
            'OUTPUT_FORMAT',
            output_config.get('format', 'json')
        )
        
        # Logging Configuration
        logging_config = self.config_data.get('logging', {})
        self.log_level = os.getenv(
            'LOG_LEVEL',
            logging_config.get('level', 'INFO')
        )
        self.log_to_file = os.getenv(
            'LOG_TO_FILE',
            str(logging_config.get('to_file', 'true'))
        ).lower() == 'true'
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def _load_config_file(self, config_path: str):
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r') as f:
                self.config_data = yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Warning: Could not load config file {config_path}: {e}")
            self.config_data = {}
    
    def validate(self) -> bool:
        """
        Validate required configuration values.
        
        Returns:
            bool: True if configuration is valid, False otherwise
        """
        required_fields = [
            ('azure_subscription_id', self.azure_subscription_id),
            ('azure_resource_group', self.azure_resource_group),
            ('azure_project_name', self.azure_project_name),
        ]
        
        missing_fields = []
        for field_name, field_value in required_fields:
            if not field_value:
                missing_fields.append(field_name)
        
        if missing_fields:
            print(f"Error: Missing required configuration fields: {', '.join(missing_fields)}")
            print("Please set these values in environment variables or config.yaml")
            return False
        
        return True
    
    def __repr__(self) -> str:
        """String representation of configuration."""
        return f"""Config(
    subscription_id={self.azure_subscription_id[:8]}... if {self.azure_subscription_id} else None,
    resource_group={self.azure_resource_group},
    project_name={self.azure_project_name},
    num_objectives={self.num_objectives},
    risk_categories={self.risk_categories},
    output_dir={self.output_dir}
)"""
