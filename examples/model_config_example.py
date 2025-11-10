"""
Example: Model Configuration Target

This example demonstrates how to run a red teaming scan against a deployed model
using model configuration.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from red_team_agent import RedTeamingAgent
from config_manager import Config
from logger import setup_logging, get_logger


async def main():
    """Run red teaming scan with model configuration."""
    
    # Load configuration
    config = Config()
    
    # Setup logging
    setup_logging(log_level=config.log_level)
    logger = get_logger(__name__)
    
    logger.info("Starting Red Teaming Scan - Model Configuration Example")
    
    # Initialize agent
    agent = RedTeamingAgent(config)
    
    # Setup agent
    if not agent.setup():
        logger.error("Agent setup failed. Please check your configuration.")
        return
    
    # Define model configuration
    # This should point to your deployed Azure OpenAI or Azure AI Foundry model
    model_config = {
        "deployment_name": config.model_deployment_name,
        "endpoint": config.model_endpoint,
        "api_version": config.model_api_version,
        # API key or credential will be handled by Azure credential
    }
    
    # Verify model configuration is set
    if not model_config["deployment_name"] or not model_config["endpoint"]:
        logger.error("Model configuration not set. Please configure MODEL_DEPLOYMENT_NAME and MODEL_ENDPOINT in your .env file.")
        print("\n⚠️  Please set the following in your .env file:")
        print("   - MODEL_DEPLOYMENT_NAME=your-model-deployment-name")
        print("   - MODEL_ENDPOINT=https://your-endpoint.openai.azure.com/")
        return
    
    # Run scan with the model configuration
    print("\n" + "="*80)
    print(f"Running Red Team Scan on Model: {model_config['deployment_name']}")
    print("="*80 + "\n")
    
    results = await agent.scan_with_model_config(
        model_config=model_config,
        num_objectives=10,
        output_filename="model_config_scan.json"
    )
    
    if results:
        logger.info("✓ Scan completed successfully")
        print("\n✓ Results saved to: outputs/model_config_scan.json")
        print("✓ Summary report saved to: outputs/")
    else:
        logger.error("✗ Scan failed")


if __name__ == "__main__":
    asyncio.run(main())
