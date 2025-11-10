"""
Main Red Teaming Agent module using PyRIT and Azure AI Foundry.

This module provides the core functionality for running automated red teaming scans
against AI systems to identify safety and security risks.
"""

import asyncio
from typing import Optional, List, Dict, Any, Callable
from pathlib import Path
import logging

from azure.identity import DefaultAzureCredential
from azure.ai.evaluation import RedTeam

from config_manager import Config
from auth import get_azure_credential, verify_authentication
from logger import setup_logging, get_logger
from results_processor import ResultsProcessor

logger = get_logger(__name__)


class RedTeamingAgent:
    """
    AI Red Teaming Agent using PyRIT and Azure AI Foundry.
    
    This agent automates the process of:
    1. Scanning AI systems for safety risks
    2. Simulating adversarial attacks
    3. Evaluating responses for harmful content
    4. Generating detailed reports with Attack Success Rate (ASR)
    """
    
    def __init__(self, config: Config):
        """
        Initialize the Red Teaming Agent.
        
        Args:
            config: Configuration object with Azure and red teaming settings
        """
        self.config = config
        self.credential = None
        self.red_team_agent = None
        self.results_processor = ResultsProcessor(self.config.output_dir)
        
        logger.info("Red Teaming Agent initialized")
    
    def setup(self) -> bool:
        """
        Set up authentication and initialize the Red Team agent.
        
        Returns:
            bool: True if setup successful, False otherwise
        """
        try:
            # Validate configuration
            if not self.config.validate():
                logger.error("Configuration validation failed")
                return False
            
            # Get Azure credentials (using Managed Identity in Azure, DefaultAzureCredential locally)
            logger.info("Setting up Azure authentication...")
            self.credential = get_azure_credential()
            
            # Verify authentication
            if not verify_authentication(self.credential):
                logger.error("Azure authentication verification failed")
                return False
            
            # Initialize Red Team agent
            logger.info("Initializing Red Team agent...")
            self.red_team_agent = RedTeam(
                subscription_id=self.config.azure_subscription_id,
                resource_group_name=self.config.azure_resource_group,
                project_name=self.config.azure_project_name,
                credential=self.credential
            )
            
            logger.info("Red Team agent setup completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Setup failed: {str(e)}", exc_info=True)
            return False
    
    async def scan_with_callback(
        self,
        target_callback: Callable[[str], str],
        num_objectives: Optional[int] = None,
        risk_categories: Optional[List[str]] = None,
        attack_strategies: Optional[List[str]] = None,
        output_filename: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Run red teaming scan with a simple callback function.
        
        Args:
            target_callback: Function that takes a prompt string and returns response string
            num_objectives: Number of attack objectives per risk category (default from config)
            risk_categories: List of risk categories to test (default from config)
            attack_strategies: List of attack strategies to use (default: all)
            output_filename: Custom output filename for results
            
        Returns:
            Dict with scan results, or None if scan failed
        """
        try:
            num_objectives = num_objectives or self.config.num_objectives
            risk_categories = risk_categories or self.config.risk_categories
            attack_strategies = attack_strategies or self.config.attack_strategies or None
            
            logger.info(f"Starting red team scan with {num_objectives} objectives per category")
            logger.info(f"Risk categories: {', '.join(risk_categories)}")
            
            # Run the scan
            result = await self.red_team_agent.scan(
                target=target_callback,
                num_objectives=num_objectives,
                risk_categories=risk_categories,
                attack_strategies=attack_strategies,
                output_path=output_filename
            )
            
            logger.info("Red team scan completed")
            
            # Process and save results
            if output_filename:
                logger.info(f"Results saved to: {output_filename}")
            
            # Generate and display summary
            self._display_results_summary(result)
            
            return result
            
        except Exception as e:
            logger.error(f"Scan failed: {str(e)}", exc_info=True)
            return None
    
    async def scan_with_model_config(
        self,
        model_config: Dict[str, str],
        num_objectives: Optional[int] = None,
        risk_categories: Optional[List[str]] = None,
        attack_strategies: Optional[List[str]] = None,
        output_filename: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Run red teaming scan against a base model configuration.
        
        Args:
            model_config: Dictionary with model configuration
                         (e.g., {"deployment_name": "gpt-4", "endpoint": "...", "api_version": "..."})
            num_objectives: Number of attack objectives per risk category
            risk_categories: List of risk categories to test
            attack_strategies: List of attack strategies to use
            output_filename: Custom output filename for results
            
        Returns:
            Dict with scan results, or None if scan failed
        """
        try:
            num_objectives = num_objectives or self.config.num_objectives
            risk_categories = risk_categories or self.config.risk_categories
            attack_strategies = attack_strategies or self.config.attack_strategies or None
            
            logger.info(f"Starting red team scan on model: {model_config.get('deployment_name')}")
            logger.info(f"Risk categories: {', '.join(risk_categories)}")
            
            # Run the scan
            result = await self.red_team_agent.scan(
                target=model_config,
                num_objectives=num_objectives,
                risk_categories=risk_categories,
                attack_strategies=attack_strategies,
                output_path=output_filename
            )
            
            logger.info("Red team scan completed")
            
            # Process and save results
            if output_filename:
                logger.info(f"Results saved to: {output_filename}")
            
            # Generate and display summary
            self._display_results_summary(result)
            
            return result
            
        except Exception as e:
            logger.error(f"Scan failed: {str(e)}", exc_info=True)
            return None
    
    def _display_results_summary(self, results: Dict[str, Any]) -> None:
        """
        Display summary of scan results.
        
        Args:
            results: Results dictionary from scan
        """
        try:
            # Generate summary report
            summary = self.results_processor.generate_summary_report(results)
            print(summary)
            
            # Save summary to file
            self.results_processor.save_summary_report(results)
            
            # Check ASR threshold
            asr = self.results_processor.calculate_asr(results)
            if asr > (self.config.asr_threshold * 100):
                logger.warning(
                    f"Attack Success Rate ({asr}%) exceeds threshold "
                    f"({self.config.asr_threshold * 100}%)"
                )
                print(f"\n⚠️  WARNING: ASR ({asr}%) exceeds threshold!")
            
        except Exception as e:
            logger.error(f"Error displaying results summary: {str(e)}")
    
    def analyze_results(self, results_path: str) -> None:
        """
        Analyze previously saved results.
        
        Args:
            results_path: Path to saved results JSON file
        """
        try:
            logger.info(f"Loading results from: {results_path}")
            results = self.results_processor.load_results(results_path)
            
            # Display summary
            self._display_results_summary(results)
            
            # Extract high-risk findings
            high_risk = self.results_processor.get_high_risk_findings(results)
            
            if high_risk:
                print(f"\n🔴 Found {len(high_risk)} high-risk findings:")
                for i, finding in enumerate(high_risk[:5], 1):  # Show top 5
                    print(f"\n{i}. {finding['risk_category']} - {finding['attack_strategy']}")
                    print(f"   Risk Score: {finding['risk_score']:.2f}")
                    print(f"   Complexity: {finding['complexity']}")
            
        except Exception as e:
            logger.error(f"Error analyzing results: {str(e)}", exc_info=True)


async def main():
    """Main entry point for running red teaming scans."""
    
    # Load configuration
    config = Config()
    
    # Setup logging
    setup_logging(log_level=config.log_level)
    logger = get_logger(__name__)
    
    logger.info("Starting Red Teaming Agent")
    
    # Initialize agent
    agent = RedTeamingAgent(config)
    
    # Setup agent
    if not agent.setup():
        logger.error("Agent setup failed. Exiting.")
        return
    
    # Example: Define a simple target callback
    def example_target(query: str) -> str:
        """
        Example target application callback.
        Replace this with your actual application logic.
        """
        # This is a placeholder - replace with your actual chatbot/application
        return "I'm an AI assistant that follows ethical guidelines. I cannot provide harmful content."
    
    # Run scan
    results = await agent.scan_with_callback(
        target_callback=example_target,
        output_filename="my_first_red_team_scan.json"
    )
    
    if results:
        logger.info("Red teaming scan completed successfully")
    else:
        logger.error("Red teaming scan failed")


if __name__ == "__main__":
    asyncio.run(main())
