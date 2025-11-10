"""
Example: Advanced Callback Target (OpenAI Chat Protocol)

This example demonstrates how to run a red teaming scan against a callback
that follows the OpenAI chat completion protocol.
"""

import asyncio
import sys
from pathlib import Path
from typing import List, Dict, Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from red_team_agent import RedTeamingAgent
from config_manager import Config
from logger import setup_logging, get_logger


def advanced_chatbot(messages: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    An advanced chatbot following OpenAI chat completion protocol.
    
    Args:
        messages: List of message dictionaries with 'role' and 'content'
        
    Returns:
        Dict with response following OpenAI format
    """
    # Extract the last user message
    user_message = ""
    for msg in reversed(messages):
        if msg.get("role") == "user":
            user_message = msg.get("content", "")
            break
    
    # Simple content filtering
    user_message_lower = user_message.lower()
    
    blocked_topics = {
        "violence": ["kill", "murder", "attack", "assault", "violent"],
        "sexual": ["explicit", "nsfw", "sexual"],
        "hate": ["racist", "sexist", "discrimination"],
        "self_harm": ["suicide", "self-harm", "hurt myself"]
    }
    
    for category, keywords in blocked_topics.items():
        if any(keyword in user_message_lower for keyword in keywords):
            response_text = f"I cannot provide information related to {category}. Please ask about something else."
            return {
                "choices": [{
                    "message": {
                        "role": "assistant",
                        "content": response_text
                    }
                }]
            }
    
    # Default helpful response
    response_text = (
        "I'm an AI assistant designed to be helpful, harmless, and honest. "
        "I'm here to assist you with information and tasks while following ethical guidelines."
    )
    
    return {
        "choices": [{
            "message": {
                "role": "assistant",
                "content": response_text
            }
        }]
    }


async def main():
    """Run red teaming scan with advanced callback."""
    
    # Load configuration
    config = Config()
    
    # Setup logging
    setup_logging(log_level=config.log_level)
    logger = get_logger(__name__)
    
    logger.info("Starting Red Teaming Scan - Advanced Callback Example")
    
    # Initialize agent
    agent = RedTeamingAgent(config)
    
    # Setup agent
    if not agent.setup():
        logger.error("Agent setup failed. Please check your configuration.")
        return
    
    # Run scan with the advanced chatbot
    print("\n" + "="*80)
    print("Running Red Team Scan on Advanced Chatbot (OpenAI Protocol)")
    print("="*80 + "\n")
    
    results = await agent.scan_with_callback(
        target_callback=advanced_chatbot,
        num_objectives=10,  # Test with 10 objectives per category
        output_filename="advanced_callback_scan.json"
    )
    
    if results:
        logger.info("✓ Scan completed successfully")
        print("\n✓ Results saved to: outputs/advanced_callback_scan.json")
        print("✓ Summary report saved to: outputs/")
    else:
        logger.error("✗ Scan failed")


if __name__ == "__main__":
    asyncio.run(main())
