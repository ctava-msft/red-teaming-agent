"""
Red Teaming Datasets - Risk Categories and Attack Strategies

This module provides curated datasets for configuring red teaming scans.
Based on Azure AI Foundry Red Teaming Agent and PyRIT capabilities.
"""

from typing import List, Dict, Any


# ============================================================================
# RISK CATEGORIES
# ============================================================================

class RiskCategories:
    """Risk categories supported by Azure AI Red Teaming Agent."""
    
    # Core risk categories (all supported)
    VIOLENCE = "violence"
    SEXUAL = "sexual"
    HATE_UNFAIRNESS = "hate_unfairness"
    SELF_HARM = "self_harm"
    
    # All supported categories
    ALL = [VIOLENCE, SEXUAL, HATE_UNFAIRNESS, SELF_HARM]
    
    # Common category groupings
    SAFETY_CRITICAL = [VIOLENCE, SEXUAL, SELF_HARM]
    ETHICAL = [HATE_UNFAIRNESS]
    HIGH_SEVERITY = [VIOLENCE, SELF_HARM]
    CONTENT_POLICY = [VIOLENCE, SEXUAL, HATE_UNFAIRNESS]
    
    @classmethod
    def get_category_description(cls, category: str) -> str:
        """Get description of a risk category."""
        descriptions = {
            cls.VIOLENCE: "Content promoting or describing violence, physical harm, or weapons",
            cls.SEXUAL: "Sexually explicit or suggestive content",
            cls.HATE_UNFAIRNESS: "Hateful, discriminatory, or unfair content targeting protected groups",
            cls.SELF_HARM: "Content promoting self-harm, suicide, or eating disorders"
        }
        return descriptions.get(category, "Unknown category")
    
    @classmethod
    def get_max_objectives(cls, category: str) -> int:
        """Get maximum number of attack objectives available per category."""
        # Each category supports up to 100 attack objectives
        return 100


# ============================================================================
# ATTACK STRATEGIES
# ============================================================================

class AttackStrategies:
    """Attack strategies supported by Azure AI Red Teaming Agent (PyRIT)."""
    
    # Encoding/Obfuscation Strategies
    ANSI_ATTACK = "AnsiAttack"
    ASCII_ART = "AsciiArt"
    ASCII_SMUGGLER = "AsciiSmuggler"
    ATBASH = "Atbash"
    BASE64 = "Base64"
    BINARY = "Binary"
    CAESAR = "Caesar"
    CHARACTER_SPACE = "CharacterSpace"
    CHAR_SWAP = "CharSwap"
    DIACRITIC = "Diacritic"
    FLIP = "Flip"
    LEETSPEAK = "Leetspeak"
    MORSE = "Morse"
    ROT13 = "ROT13"
    STRING_JOIN = "StringJoin"
    UNICODE_CONFUSABLE = "UnicodeConfusable"
    UNICODE_SUBSTITUTION = "UnicodeSubstitution"
    URL = "Url"
    
    # Prompt Manipulation Strategies
    JAILBREAK = "Jailbreak"
    SUFFIX_APPEND = "SuffixAppend"
    TENSE = "Tense"
    
    # Strategy categories
    ENCODING_STRATEGIES = [
        ANSI_ATTACK, ASCII_ART, ASCII_SMUGGLER, ATBASH, BASE64, 
        BINARY, CAESAR, CHARACTER_SPACE, CHAR_SWAP, DIACRITIC, 
        FLIP, LEETSPEAK, MORSE, ROT13, STRING_JOIN, 
        UNICODE_CONFUSABLE, UNICODE_SUBSTITUTION, URL
    ]
    
    MANIPULATION_STRATEGIES = [
        JAILBREAK, SUFFIX_APPEND, TENSE
    ]
    
    ALL = ENCODING_STRATEGIES + MANIPULATION_STRATEGIES
    
    # Complexity-based groupings
    LOW_COMPLEXITY = [BASE64, CAESAR, ROT13, LEETSPEAK, FLIP]
    MEDIUM_COMPLEXITY = [ATBASH, MORSE, CHAR_SWAP, DIACRITIC, TENSE]
    HIGH_COMPLEXITY = [JAILBREAK, ASCII_SMUGGLER, UNICODE_CONFUSABLE, SUFFIX_APPEND]
    
    @classmethod
    def get_strategy_description(cls, strategy: str) -> str:
        """Get description of an attack strategy."""
        descriptions = {
            cls.ANSI_ATTACK: "Utilizes ANSI escape sequences to manipulate text appearance and behavior",
            cls.ASCII_ART: "Generates visual art using ASCII characters for creative obfuscation",
            cls.ASCII_SMUGGLER: "Conceals data within ASCII characters to evade detection",
            cls.ATBASH: "Substitution cipher mapping each letter to its reverse in the alphabet",
            cls.BASE64: "Encodes binary data into Base64 text format",
            cls.BINARY: "Converts text into binary code (0s and 1s)",
            cls.CAESAR: "Shifts characters by a fixed number of positions in the alphabet",
            cls.CHARACTER_SPACE: "Adds spaces between characters for obfuscation",
            cls.CHAR_SWAP: "Swaps characters within text to create variations",
            cls.DIACRITIC: "Adds diacritical marks to change character appearance",
            cls.FLIP: "Flips characters from front to back (mirrored effect)",
            cls.LEETSPEAK: "Replaces letters with similar-looking numbers or symbols",
            cls.MORSE: "Encodes text into Morse code using dots and dashes",
            cls.ROT13: "Shifts characters by 13 positions in the alphabet",
            cls.SUFFIX_APPEND: "Appends an adversarial suffix to the prompt",
            cls.STRING_JOIN: "Joins multiple strings together for concatenation or obfuscation",
            cls.UNICODE_CONFUSABLE: "Uses Unicode characters that look similar to standard characters",
            cls.UNICODE_SUBSTITUTION: "Substitutes standard characters with Unicode equivalents",
            cls.URL: "Encodes text into URL format",
            cls.JAILBREAK: "Injects specially crafted prompts to bypass AI safeguards (UPIA)",
            cls.TENSE: "Changes the tense of text, converting to past tense"
        }
        return descriptions.get(strategy, "Unknown strategy")


# ============================================================================
# PRE-CONFIGURED SCAN PROFILES
# ============================================================================

class ScanProfiles:
    """Pre-configured scan profiles for different testing scenarios."""
    
    # Quick scan - fast testing with basic coverage
    QUICK_SCAN = {
        "name": "Quick Scan",
        "num_objectives": 5,
        "risk_categories": [RiskCategories.VIOLENCE, RiskCategories.SEXUAL],
        "attack_strategies": AttackStrategies.LOW_COMPLEXITY,
        "description": "Fast scan with basic coverage (10 total attacks)"
    }
    
    # Basic scan - standard testing
    BASIC_SCAN = {
        "name": "Basic Scan",
        "num_objectives": 10,
        "risk_categories": RiskCategories.ALL,
        "attack_strategies": AttackStrategies.LOW_COMPLEXITY + AttackStrategies.MEDIUM_COMPLEXITY,
        "description": "Standard scan with moderate coverage (40 total attacks)"
    }
    
    # Comprehensive scan - thorough testing
    COMPREHENSIVE_SCAN = {
        "name": "Comprehensive Scan",
        "num_objectives": 25,
        "risk_categories": RiskCategories.ALL,
        "attack_strategies": AttackStrategies.ALL,
        "description": "Thorough scan with full coverage (100 total attacks)"
    }
    
    # Jailbreak focused - test prompt injection vulnerabilities
    JAILBREAK_FOCUSED = {
        "name": "Jailbreak Focused",
        "num_objectives": 20,
        "risk_categories": RiskCategories.ALL,
        "attack_strategies": [AttackStrategies.JAILBREAK, AttackStrategies.SUFFIX_APPEND],
        "description": "Focus on jailbreak and prompt injection attacks"
    }
    
    # Encoding focused - test obfuscation techniques
    ENCODING_FOCUSED = {
        "name": "Encoding Focused",
        "num_objectives": 15,
        "risk_categories": RiskCategories.ALL,
        "attack_strategies": AttackStrategies.ENCODING_STRATEGIES,
        "description": "Focus on encoding and obfuscation techniques"
    }
    
    # Safety critical - high severity risks only
    SAFETY_CRITICAL_SCAN = {
        "name": "Safety Critical",
        "num_objectives": 30,
        "risk_categories": RiskCategories.SAFETY_CRITICAL,
        "attack_strategies": AttackStrategies.HIGH_COMPLEXITY,
        "description": "High-severity risks with complex attacks"
    }
    
    # Production readiness - comprehensive pre-deployment scan
    PRODUCTION_READINESS = {
        "name": "Production Readiness",
        "num_objectives": 50,
        "risk_categories": RiskCategories.ALL,
        "attack_strategies": AttackStrategies.ALL,
        "description": "Comprehensive pre-deployment scan (200 total attacks)"
    }
    
    # Compliance scan - minimal required testing
    COMPLIANCE_SCAN = {
        "name": "Compliance Scan",
        "num_objectives": 10,
        "risk_categories": RiskCategories.ALL,
        "attack_strategies": None,  # Use all strategies
        "description": "Minimal compliance testing across all categories"
    }
    
    @classmethod
    def get_all_profiles(cls) -> Dict[str, Dict[str, Any]]:
        """Get all available scan profiles."""
        return {
            "quick": cls.QUICK_SCAN,
            "basic": cls.BASIC_SCAN,
            "comprehensive": cls.COMPREHENSIVE_SCAN,
            "jailbreak": cls.JAILBREAK_FOCUSED,
            "encoding": cls.ENCODING_FOCUSED,
            "safety": cls.SAFETY_CRITICAL_SCAN,
            "production": cls.PRODUCTION_READINESS,
            "compliance": cls.COMPLIANCE_SCAN
        }
    
    @classmethod
    def get_profile(cls, profile_name: str) -> Dict[str, Any]:
        """Get a specific scan profile by name."""
        profiles = cls.get_all_profiles()
        return profiles.get(profile_name.lower(), cls.BASIC_SCAN)


# ============================================================================
# CUSTOM SCAN BUILDERS
# ============================================================================

class ScanBuilder:
    """Helper class to build custom scan configurations."""
    
    @staticmethod
    def build_scan_config(
        risk_categories: List[str] = None,
        attack_strategies: List[str] = None,
        num_objectives: int = 10
    ) -> Dict[str, Any]:
        """
        Build a custom scan configuration.
        
        Args:
            risk_categories: List of risk categories (default: all)
            attack_strategies: List of attack strategies (default: all)
            num_objectives: Number of objectives per category (default: 10)
            
        Returns:
            Dict with scan configuration
        """
        return {
            "risk_categories": risk_categories or RiskCategories.ALL,
            "attack_strategies": attack_strategies or AttackStrategies.ALL,
            "num_objectives": num_objectives
        }
    
    @staticmethod
    def estimate_scan_duration(
        num_categories: int,
        num_objectives: int,
        avg_response_time: float = 2.0
    ) -> Dict[str, Any]:
        """
        Estimate scan duration.
        
        Args:
            num_categories: Number of risk categories
            num_objectives: Number of objectives per category
            avg_response_time: Average response time per attack in seconds
            
        Returns:
            Dict with time estimates
        """
        total_attacks = num_categories * num_objectives
        estimated_seconds = total_attacks * avg_response_time
        estimated_minutes = estimated_seconds / 60
        
        return {
            "total_attacks": total_attacks,
            "estimated_seconds": estimated_seconds,
            "estimated_minutes": round(estimated_minutes, 2),
            "estimated_hours": round(estimated_minutes / 60, 2)
        }


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

def print_examples():
    """Print usage examples."""
    
    print("=" * 80)
    print("RED TEAMING DATASETS - USAGE EXAMPLES")
    print("=" * 80)
    
    print("\n1. Using Risk Categories:")
    print("-" * 40)
    print(f"All categories: {RiskCategories.ALL}")
    print(f"Safety critical: {RiskCategories.SAFETY_CRITICAL}")
    print(f"Violence description: {RiskCategories.get_category_description(RiskCategories.VIOLENCE)}")
    
    print("\n2. Using Attack Strategies:")
    print("-" * 40)
    print(f"All strategies: {len(AttackStrategies.ALL)} available")
    print(f"Low complexity: {AttackStrategies.LOW_COMPLEXITY}")
    print(f"High complexity: {AttackStrategies.HIGH_COMPLEXITY}")
    print(f"Jailbreak description: {AttackStrategies.get_strategy_description(AttackStrategies.JAILBREAK)}")
    
    print("\n3. Using Scan Profiles:")
    print("-" * 40)
    for name, profile in ScanProfiles.get_all_profiles().items():
        print(f"\n{profile['name']}:")
        print(f"  Description: {profile['description']}")
        print(f"  Objectives: {profile['num_objectives']}")
        print(f"  Categories: {len(profile['risk_categories'])}")
        print(f"  Strategies: {len(profile['attack_strategies']) if profile['attack_strategies'] else 'All'}")
    
    print("\n4. Estimating Scan Duration:")
    print("-" * 40)
    estimate = ScanBuilder.estimate_scan_duration(
        num_categories=4,
        num_objectives=25,
        avg_response_time=2.0
    )
    print(f"Total attacks: {estimate['total_attacks']}")
    print(f"Estimated time: {estimate['estimated_minutes']} minutes")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    print_examples()
