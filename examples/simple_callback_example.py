"""
Example: Simple Callback Target

This example demonstrates how to run a red teaming scan against a simple callback function.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from red_team_agent import RedTeamingAgent
from config_manager import Config
from logger import setup_logging, get_logger


def simple_chatbot(query: str) -> str:
    """
    A simple chatbot target for red teaming.
    
    This is a basic example. Replace with your actual application.
    """
    # Simple rule-based responses
    query_lower = query.lower()
    
    if any(word in query_lower for word in ["hack", "attack", "exploit"]):
        return "I'm sorry, I cannot help with malicious activities."
    
    if any(word in query_lower for word in ["violent", "harm", "hurt"]):
        return "I cannot provide information that could cause harm."
    
    # Default response
    return "I'm an AI assistant designed to be helpful, harmless, and honest. How can I assist you today?"


async def main():
    """Run red teaming scan with simple callback."""
    
    # Load configuration
    config = Config()
    
    # Setup logging
    setup_logging(log_level=config.log_level)
    logger = get_logger(__name__)
    
    logger.info("Starting Red Teaming Scan - Simple Callback Example")
    
    # Initialize agent
    agent = RedTeamingAgent(config)
    
    # Setup agent
    if not agent.setup():
        logger.error("Agent setup failed. Please check your configuration.")
        return
    
    # Run scan with the simple chatbot
    print("\n" + "="*80)
    print("Running Red Team Scan on Simple Chatbot")
    print("="*80 + "\n")
    
    results = await agent.scan_with_callback(
        target_callback=simple_chatbot,
        num_objectives=5,  # Start with fewer objectives for testing
        risk_categories=["violence", "sexual"],  # Test specific categories
        output_filename="simple_callback_scan.json"
    )
    
    if results:
        logger.info("✓ Scan completed successfully")
        print("\n✓ Results saved to: outputs/simple_callback_scan.json")
        print("✓ Summary report saved to: outputs/")
    else:
        logger.error("✗ Scan failed")


if __name__ == "__main__":
    asyncio.run(main())
