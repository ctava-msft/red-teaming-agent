"""
Example: Using Pre-configured Datasets

This example demonstrates how to use the pre-configured risk categories,
attack strategies, and scan profiles for red teaming.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from red_team_agent import RedTeamingAgent
from config_manager import Config
from logger import setup_logging, get_logger
from datasets import RiskCategories, AttackStrategies, ScanProfiles, ScanBuilder


def example_chatbot(query: str) -> str:
    """Example chatbot for testing."""
    return "I'm an AI assistant that follows ethical guidelines."


async def run_quick_scan(agent: RedTeamingAgent):
    """Run a quick scan using pre-configured profile."""
    print("\n" + "="*80)
    print("QUICK SCAN - Fast testing with basic coverage")
    print("="*80)
    
    profile = ScanProfiles.QUICK_SCAN
    
    results = await agent.scan_with_callback(
        target_callback=example_chatbot,
        num_objectives=profile["num_objectives"],
        risk_categories=profile["risk_categories"],
        attack_strategies=profile["attack_strategies"],
        output_filename="quick_scan_results.json"
    )
    
    return results


async def run_jailbreak_focused_scan(agent: RedTeamingAgent):
    """Run a jailbreak-focused scan."""
    print("\n" + "="*80)
    print("JAILBREAK FOCUSED SCAN - Testing prompt injection vulnerabilities")
    print("="*80)
    
    profile = ScanProfiles.JAILBREAK_FOCUSED
    
    results = await agent.scan_with_callback(
        target_callback=example_chatbot,
        num_objectives=profile["num_objectives"],
        risk_categories=profile["risk_categories"],
        attack_strategies=profile["attack_strategies"],
        output_filename="jailbreak_scan_results.json"
    )
    
    return results


async def run_custom_scan(agent: RedTeamingAgent):
    """Run a custom scan with specific categories and strategies."""
    print("\n" + "="*80)
    print("CUSTOM SCAN - Violence & Self-harm with encoding attacks")
    print("="*80)
    
    # Custom configuration
    custom_categories = [
        RiskCategories.VIOLENCE,
        RiskCategories.SELF_HARM
    ]
    
    custom_strategies = [
        AttackStrategies.BASE64,
        AttackStrategies.LEETSPEAK,
        AttackStrategies.CAESAR,
        AttackStrategies.ROT13,
        AttackStrategies.UNICODE_CONFUSABLE
    ]
    
    results = await agent.scan_with_callback(
        target_callback=example_chatbot,
        num_objectives=15,
        risk_categories=custom_categories,
        attack_strategies=custom_strategies,
        output_filename="custom_scan_results.json"
    )
    
    return results


async def run_comprehensive_scan(agent: RedTeamingAgent):
    """Run a comprehensive scan for production readiness."""
    print("\n" + "="*80)
    print("COMPREHENSIVE SCAN - Full coverage for production readiness")
    print("="*80)
    
    profile = ScanProfiles.PRODUCTION_READINESS
    
    # Estimate duration
    estimate = ScanBuilder.estimate_scan_duration(
        num_categories=len(profile["risk_categories"]),
        num_objectives=profile["num_objectives"],
        avg_response_time=2.0
    )
    
    print(f"\nEstimated duration: {estimate['estimated_minutes']} minutes")
    print(f"Total attacks: {estimate['total_attacks']}")
    
    user_input = input("\nThis is a long scan. Continue? (y/N): ")
    if user_input.lower() != 'y':
        print("Scan cancelled.")
        return None
    
    results = await agent.scan_with_callback(
        target_callback=example_chatbot,
        num_objectives=profile["num_objectives"],
        risk_categories=profile["risk_categories"],
        attack_strategies=profile["attack_strategies"],
        output_filename="comprehensive_scan_results.json"
    )
    
    return results


async def main():
    """Main entry point."""
    
    # Load configuration
    config = Config()
    setup_logging(log_level=config.log_level)
    logger = get_logger(__name__)
    
    logger.info("Starting Red Teaming with Pre-configured Datasets")
    
    # Initialize agent
    agent = RedTeamingAgent(config)
    
    if not agent.setup():
        logger.error("Agent setup failed")
        return
    
    # Display available options
    print("\n" + "="*80)
    print("RED TEAMING SCAN OPTIONS")
    print("="*80)
    
    print("\nAvailable Scan Profiles:")
    for name, profile in ScanProfiles.get_all_profiles().items():
        print(f"\n{name.upper()}: {profile['name']}")
        print(f"  {profile['description']}")
        print(f"  Objectives per category: {profile['num_objectives']}")
        print(f"  Risk categories: {len(profile['risk_categories'])}")
    
    print("\n" + "="*80)
    print("\nSelect a scan type:")
    print("1. Quick Scan (fast, 5 objectives)")
    print("2. Jailbreak Focused (20 objectives)")
    print("3. Custom Scan (15 objectives)")
    print("4. Comprehensive/Production (50 objectives)")
    print("0. Exit")
    
    choice = input("\nEnter choice (0-4): ")
    
    if choice == "1":
        await run_quick_scan(agent)
    elif choice == "2":
        await run_jailbreak_focused_scan(agent)
    elif choice == "3":
        await run_custom_scan(agent)
    elif choice == "4":
        await run_comprehensive_scan(agent)
    elif choice == "0":
        print("Exiting...")
    else:
        print("Invalid choice")
    
    print("\n" + "="*80)
    print("Scan complete! Check the outputs/ directory for results.")
    print("="*80)


if __name__ == "__main__":
    asyncio.run(main())
