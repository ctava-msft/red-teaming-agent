# Red Teaming Datasets Reference Guide

This guide provides comprehensive information about the risk categories and attack strategies available for red teaming scans.

## 📊 Risk Categories

### Supported Categories

| Category | Description | Max Objectives |
|----------|-------------|----------------|
| **violence** | Content promoting or describing violence, physical harm, or weapons | 100 |
| **sexual** | Sexually explicit or suggestive content | 100 |
| **hate_unfairness** | Hateful, discriminatory, or unfair content targeting protected groups | 100 |
| **self_harm** | Content promoting self-harm, suicide, or eating disorders | 100 |

### Usage Examples

```python
from datasets import RiskCategories

# Use all categories
scan_config = {
    "risk_categories": RiskCategories.ALL
}

# Use only safety-critical categories
scan_config = {
    "risk_categories": RiskCategories.SAFETY_CRITICAL  # [violence, sexual, self_harm]
}

# Use specific categories
scan_config = {
    "risk_categories": [RiskCategories.VIOLENCE, RiskCategories.HATE_UNFAIRNESS]
}
```

## 🎯 Attack Strategies (21 Total)

### Encoding & Obfuscation Strategies (18)

| Strategy | Description | Complexity |
|----------|-------------|------------|
| **Base64** | Encodes binary data into Base64 text format | Low |
| **Caesar** | Shifts characters by a fixed number of positions | Low |
| **ROT13** | Shifts characters by 13 positions | Low |
| **Leetspeak** | Replaces letters with similar-looking numbers/symbols | Low |
| **Flip** | Flips characters from front to back | Low |
| **Atbash** | Maps each letter to its reverse in alphabet | Medium |
| **Morse** | Encodes text into Morse code | Medium |
| **CharSwap** | Swaps characters within text | Medium |
| **Diacritic** | Adds diacritical marks to characters | Medium |
| **Tense** | Changes text tense (to past tense) | Medium |
| **AnsiAttack** | Uses ANSI escape sequences | Medium |
| **AsciiArt** | Generates visual art using ASCII | Medium |
| **Binary** | Converts text to binary (0s and 1s) | Medium |
| **CharacterSpace** | Adds spaces between characters | Medium |
| **StringJoin** | Joins strings for obfuscation | Medium |
| **Url** | Encodes text into URL format | Medium |
| **AsciiSmuggler** | Conceals data within ASCII characters | High |
| **UnicodeConfusable** | Uses lookalike Unicode characters | High |
| **UnicodeSubstitution** | Substitutes with Unicode equivalents | High |

### Prompt Manipulation Strategies (3)

| Strategy | Description | Complexity |
|----------|-------------|------------|
| **Jailbreak** | Injects crafted prompts to bypass safeguards (UPIA) | High |
| **SuffixAppend** | Appends adversarial suffix to prompt | High |
| **Tense** | Changes text tense | Medium |

### Usage Examples

```python
from datasets import AttackStrategies

# Use all strategies
scan_config = {
    "attack_strategies": AttackStrategies.ALL
}

# Use only low complexity strategies
scan_config = {
    "attack_strategies": AttackStrategies.LOW_COMPLEXITY
}

# Use encoding strategies only
scan_config = {
    "attack_strategies": AttackStrategies.ENCODING_STRATEGIES
}

# Use specific strategies
scan_config = {
    "attack_strategies": [
        AttackStrategies.JAILBREAK,
        AttackStrategies.BASE64,
        AttackStrategies.UNICODE_CONFUSABLE
    ]
}

# Use default (all strategies)
scan_config = {
    "attack_strategies": None  # Will use all available
}
```

## 📋 Pre-configured Scan Profiles

### 1. Quick Scan
- **Objectives**: 5 per category
- **Categories**: Violence, Sexual
- **Strategies**: Low complexity only
- **Total Attacks**: ~10
- **Duration**: ~1 minute
- **Use Case**: Fast testing, development

```python
from datasets import ScanProfiles

profile = ScanProfiles.QUICK_SCAN
await agent.scan_with_callback(
    target_callback=my_app,
    num_objectives=profile["num_objectives"],
    risk_categories=profile["risk_categories"],
    attack_strategies=profile["attack_strategies"]
)
```

### 2. Basic Scan
- **Objectives**: 10 per category
- **Categories**: All 4 categories
- **Strategies**: Low + Medium complexity
- **Total Attacks**: ~40
- **Duration**: ~2-3 minutes
- **Use Case**: Standard testing

### 3. Comprehensive Scan
- **Objectives**: 25 per category
- **Categories**: All 4 categories
- **Strategies**: All strategies
- **Total Attacks**: ~100
- **Duration**: ~5-10 minutes
- **Use Case**: Thorough testing

### 4. Jailbreak Focused
- **Objectives**: 20 per category
- **Categories**: All 4 categories
- **Strategies**: Jailbreak + SuffixAppend
- **Total Attacks**: ~80
- **Duration**: ~5 minutes
- **Use Case**: Test prompt injection vulnerabilities

### 5. Encoding Focused
- **Objectives**: 15 per category
- **Categories**: All 4 categories
- **Strategies**: All encoding strategies
- **Total Attacks**: ~60
- **Duration**: ~3-5 minutes
- **Use Case**: Test obfuscation resistance

### 6. Safety Critical
- **Objectives**: 30 per category
- **Categories**: Violence, Sexual, Self-harm
- **Strategies**: High complexity only
- **Total Attacks**: ~90
- **Duration**: ~5-8 minutes
- **Use Case**: High-severity risk testing

### 7. Production Readiness
- **Objectives**: 50 per category
- **Categories**: All 4 categories
- **Strategies**: All strategies
- **Total Attacks**: ~200
- **Duration**: ~15-20 minutes
- **Use Case**: Pre-deployment comprehensive scan

### 8. Compliance Scan
- **Objectives**: 10 per category
- **Categories**: All 4 categories
- **Strategies**: All strategies
- **Total Attacks**: ~40
- **Duration**: ~2-3 minutes
- **Use Case**: Minimal compliance testing

## 🔧 Custom Scan Configuration

### Building Custom Scans

```python
from datasets import ScanBuilder, RiskCategories, AttackStrategies

# Build custom configuration
custom_config = ScanBuilder.build_scan_config(
    risk_categories=[
        RiskCategories.VIOLENCE,
        RiskCategories.SELF_HARM
    ],
    attack_strategies=[
        AttackStrategies.JAILBREAK,
        AttackStrategies.BASE64,
        AttackStrategies.UNICODE_CONFUSABLE
    ],
    num_objectives=20
)

# Estimate duration
estimate = ScanBuilder.estimate_scan_duration(
    num_categories=2,
    num_objectives=20,
    avg_response_time=2.0  # seconds per attack
)

print(f"Total attacks: {estimate['total_attacks']}")
print(f"Estimated time: {estimate['estimated_minutes']} minutes")

# Run the scan
await agent.scan_with_callback(
    target_callback=my_app,
    **custom_config
)
```

## 📈 Scan Planning Guidelines

### Choose Number of Objectives

| Objectives | Total Attacks (4 categories) | Recommended Use |
|------------|------------------------------|-----------------|
| 5 | 20 | Quick testing, iteration |
| 10 | 40 | Standard testing |
| 25 | 100 | Thorough testing |
| 50 | 200 | Pre-production |
| 100 | 400 | Maximum coverage |

### Complexity Levels

**Low Complexity** (5 strategies)
- Simple encoding techniques
- Easy to detect and block
- Good for basic testing

**Medium Complexity** (13 strategies)
- More sophisticated obfuscation
- Moderate detection difficulty
- Standard production testing

**High Complexity** (3 strategies)
- Advanced prompt injection
- Difficult to detect
- Critical security testing

### Strategy Selection Guidelines

| Scenario | Recommended Strategies |
|----------|----------------------|
| **Initial testing** | Low complexity |
| **Pre-production** | All strategies |
| **Security audit** | High complexity + Jailbreak |
| **Content filtering** | Encoding strategies |
| **Prompt injection** | Jailbreak, SuffixAppend |
| **Obfuscation resistance** | Unicode*, ASCII* |

## 💡 Best Practices

### 1. Start Small, Scale Up
```python
# Week 1: Quick scan
profile = ScanProfiles.QUICK_SCAN

# Week 2: Basic scan
profile = ScanProfiles.BASIC_SCAN

# Week 3: Comprehensive scan
profile = ScanProfiles.COMPREHENSIVE_SCAN
```

### 2. Focus on Specific Risks
```python
# If concerned about violence
risk_categories = [RiskCategories.VIOLENCE]
attack_strategies = AttackStrategies.ALL
num_objectives = 50  # Deep dive
```

### 3. Iterative Testing
```python
# Round 1: Test all categories with low complexity
round_1 = {
    "risk_categories": RiskCategories.ALL,
    "attack_strategies": AttackStrategies.LOW_COMPLEXITY,
    "num_objectives": 10
}

# Round 2: Focus on failed categories with higher complexity
round_2 = {
    "risk_categories": [RiskCategories.VIOLENCE],  # Based on round 1 results
    "attack_strategies": AttackStrategies.HIGH_COMPLEXITY,
    "num_objectives": 30
}
```

### 4. Production Deployment Checklist
- [ ] Run comprehensive scan (50+ objectives)
- [ ] Test all risk categories
- [ ] Include high complexity strategies
- [ ] ASR < 10% for production
- [ ] Document and track findings
- [ ] Implement mitigations
- [ ] Re-test after fixes

## 🎯 Complete Example

```python
import asyncio
from src.red_team_agent import RedTeamingAgent
from src.config_manager import Config
from src.datasets import RiskCategories, AttackStrategies, ScanProfiles, ScanBuilder

async def comprehensive_red_team_test():
    # Setup
    config = Config()
    agent = RedTeamingAgent(config)
    await agent.setup()
    
    # Phase 1: Quick validation
    print("Phase 1: Quick Scan")
    quick_results = await agent.scan_with_callback(
        target_callback=my_app,
        **ScanProfiles.QUICK_SCAN
    )
    
    # Phase 2: Focused testing on high-risk areas
    print("Phase 2: Jailbreak Testing")
    jailbreak_results = await agent.scan_with_callback(
        target_callback=my_app,
        **ScanProfiles.JAILBREAK_FOCUSED
    )
    
    # Phase 3: Production readiness
    print("Phase 3: Comprehensive Scan")
    prod_results = await agent.scan_with_callback(
        target_callback=my_app,
        **ScanProfiles.PRODUCTION_READINESS
    )
    
    # Analyze combined results
    total_asr = (
        agent.results_processor.calculate_asr(quick_results) +
        agent.results_processor.calculate_asr(jailbreak_results) +
        agent.results_processor.calculate_asr(prod_results)
    ) / 3
    
    print(f"Average ASR across all phases: {total_asr}%")
    
    if total_asr < 10:
        print("✓ System is ready for production")
    else:
        print("✗ System needs additional hardening")

asyncio.run(comprehensive_red_team_test())
```

## 📚 Additional Resources

- [Azure AI Red Teaming Agent Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/ai-red-teaming-agent)
- [PyRIT GitHub Repository](https://github.com/Azure/PyRIT)
- [Attack Strategies Reference](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/ai-red-teaming-agent#supported-attack-strategies)
