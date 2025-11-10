"""
Utility module for processing and analyzing red teaming results.
"""

import json
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ResultsProcessor:
    """Process and analyze red teaming scan results."""
    
    def __init__(self, output_dir: str = "outputs"):
        """
        Initialize results processor.
        
        Args:
            output_dir: Directory to save results
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def save_results(self, results: Dict[str, Any], filename: str = None) -> str:
        """
        Save scan results to JSON file.
        
        Args:
            results: Results dictionary from red teaming scan
            filename: Optional filename (if None, generates timestamp-based name)
            
        Returns:
            str: Path to saved results file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"red_team_results_{timestamp}.json"
        
        filepath = self.output_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Results saved to: {filepath}")
        return str(filepath)
    
    def load_results(self, filepath: str) -> Dict[str, Any]:
        """
        Load results from JSON file.
        
        Args:
            filepath: Path to results file
            
        Returns:
            Dict containing results
        """
        with open(filepath, 'r') as f:
            return json.load(f)
    
    def calculate_asr(self, results: Dict[str, Any]) -> float:
        """
        Calculate Attack Success Rate (ASR) from results.
        
        Args:
            results: Results dictionary
            
        Returns:
            float: ASR as a percentage (0-100)
        """
        try:
            scorecard = results.get("scorecard", {})
            total_attacks = scorecard.get("total_attacks", 0)
            successful_attacks = scorecard.get("successful_attacks", 0)
            
            if total_attacks == 0:
                return 0.0
            
            asr = (successful_attacks / total_attacks) * 100
            return round(asr, 2)
        except Exception as e:
            logger.error(f"Error calculating ASR: {str(e)}")
            return 0.0
    
    def generate_summary_report(self, results: Dict[str, Any]) -> str:
        """
        Generate a human-readable summary report from results.
        
        Args:
            results: Results dictionary
            
        Returns:
            str: Formatted summary report
        """
        try:
            scorecard = results.get("scorecard", {})
            parameters = results.get("parameters", {})
            
            asr = self.calculate_asr(results)
            
            report = f"""
{'='*80}
RED TEAMING SCAN SUMMARY REPORT
{'='*80}

Scan Configuration:
------------------
Risk Categories: {', '.join(parameters.get('risk_categories', []))}
Attack Objectives per Category: {parameters.get('num_objectives', 'N/A')}
Attack Strategies: {', '.join(parameters.get('attack_strategies', ['All'])) if parameters.get('attack_strategies') else 'All'}

Overall Results:
---------------
Total Attacks: {scorecard.get('total_attacks', 0)}
Successful Attacks: {scorecard.get('successful_attacks', 0)}
Attack Success Rate (ASR): {asr}%

Results by Risk Category:
------------------------
"""
            
            # Add risk category breakdown
            risk_breakdown = scorecard.get("by_risk_category", {})
            for category, stats in risk_breakdown.items():
                total = stats.get("total", 0)
                successful = stats.get("successful", 0)
                category_asr = (successful / total * 100) if total > 0 else 0
                
                report += f"\n{category.upper()}:\n"
                report += f"  Total Attacks: {total}\n"
                report += f"  Successful: {successful}\n"
                report += f"  ASR: {category_asr:.2f}%\n"
            
            # Add attack complexity breakdown
            report += "\nResults by Attack Complexity:\n"
            report += "----------------------------\n"
            
            complexity_breakdown = scorecard.get("by_complexity", {})
            for complexity, stats in complexity_breakdown.items():
                total = stats.get("total", 0)
                successful = stats.get("successful", 0)
                complexity_asr = (successful / total * 100) if total > 0 else 0
                
                report += f"\n{complexity.upper()}:\n"
                report += f"  Total Attacks: {total}\n"
                report += f"  Successful: {successful}\n"
                report += f"  ASR: {complexity_asr:.2f}%\n"
            
            report += f"\n{'='*80}\n"
            
            return report
        except Exception as e:
            logger.error(f"Error generating summary report: {str(e)}")
            return "Error generating summary report"
    
    def get_high_risk_findings(
        self, 
        results: Dict[str, Any], 
        threshold: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Extract high-risk findings from results.
        
        Args:
            results: Results dictionary
            threshold: Risk score threshold (0-1)
            
        Returns:
            List of high-risk findings
        """
        try:
            all_results = results.get("results", [])
            high_risk = []
            
            for result in all_results:
                if result.get("successful", False):
                    risk_score = result.get("risk_score", 0)
                    if risk_score >= threshold:
                        high_risk.append({
                            "risk_category": result.get("risk_category"),
                            "attack_strategy": result.get("attack_strategy"),
                            "complexity": result.get("complexity"),
                            "risk_score": risk_score,
                            "prompt": result.get("prompt"),
                            "response": result.get("response")
                        })
            
            return high_risk
        except Exception as e:
            logger.error(f"Error extracting high-risk findings: {str(e)}")
            return []
    
    def save_summary_report(self, results: Dict[str, Any], filename: str = None) -> str:
        """
        Save summary report to text file.
        
        Args:
            results: Results dictionary
            filename: Optional filename
            
        Returns:
            str: Path to saved report file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"red_team_report_{timestamp}.txt"
        
        filepath = self.output_dir / filename
        
        report = self.generate_summary_report(results)
        
        with open(filepath, 'w') as f:
            f.write(report)
        
        logger.info(f"Summary report saved to: {filepath}")
        return str(filepath)
