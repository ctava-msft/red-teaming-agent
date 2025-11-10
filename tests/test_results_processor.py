"""
Unit tests for results processor.
"""

import pytest
import json
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from results_processor import ResultsProcessor


@pytest.fixture
def sample_results():
    """Sample results data for testing."""
    return {
        "scorecard": {
            "total_attacks": 100,
            "successful_attacks": 25,
            "by_risk_category": {
                "violence": {"total": 25, "successful": 10},
                "sexual": {"total": 25, "successful": 5},
                "hate_unfairness": {"total": 25, "successful": 7},
                "self_harm": {"total": 25, "successful": 3}
            },
            "by_complexity": {
                "low": {"total": 50, "successful": 15},
                "medium": {"total": 30, "successful": 7},
                "high": {"total": 20, "successful": 3}
            }
        },
        "parameters": {
            "num_objectives": 25,
            "risk_categories": ["violence", "sexual", "hate_unfairness", "self_harm"],
            "attack_strategies": []
        },
        "results": [
            {
                "successful": True,
                "risk_category": "violence",
                "attack_strategy": "jailbreak",
                "complexity": "high",
                "risk_score": 0.85,
                "prompt": "test prompt",
                "response": "test response"
            }
        ]
    }


def test_results_processor_init():
    """Test ResultsProcessor initialization."""
    processor = ResultsProcessor("test_outputs")
    assert processor.output_dir == Path("test_outputs")


def test_calculate_asr(sample_results):
    """Test ASR calculation."""
    processor = ResultsProcessor()
    asr = processor.calculate_asr(sample_results)
    assert asr == 25.0  # 25/100 * 100 = 25%


def test_generate_summary_report(sample_results):
    """Test summary report generation."""
    processor = ResultsProcessor()
    report = processor.generate_summary_report(sample_results)
    
    assert "RED TEAMING SCAN SUMMARY REPORT" in report
    assert "Attack Success Rate (ASR): 25.0%" in report
    assert "violence" in report.lower()


def test_get_high_risk_findings(sample_results):
    """Test extraction of high-risk findings."""
    processor = ResultsProcessor()
    high_risk = processor.get_high_risk_findings(sample_results, threshold=0.8)
    
    assert len(high_risk) == 1
    assert high_risk[0]["risk_score"] >= 0.8
    assert high_risk[0]["risk_category"] == "violence"
