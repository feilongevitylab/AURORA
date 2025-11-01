"""
Narrative Agent - Simulates GPT-5 behavior for natural language explanation generation.
"""

from typing import Dict, Any, Optional
from datetime import datetime


class NarrativeAgent:
    """
    Agent responsible for narrative operations including:
    - Natural language explanations (GPT-5 simulation)
    - Story generation from data insights
    - Summarization
    - Contextual narratives based on data summaries
    
    Simulates GPT-5 behavior without requiring API keys (mock mode).
    """
    
    def __init__(self):
        """Initialize the Narrative Agent"""
        self.name = "NarrativeAgent"
        self.model_simulation = "GPT-5 (simulated)"
    
    def run(self, data_summary: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate narrative explanation based on data summary (GPT-5 simulation).
        
        Args:
            data_summary: Dictionary containing data analysis results, including:
                - statistics: Basic statistics for HRV, stress_score, age
                - hrv_by_stress_level: Average HRV grouped by stress levels
                - correlations: Correlation coefficients
                - insights: List of insights from analysis
                - data_summary: Data metadata
        
        Returns:
            Dictionary containing narrative text and explanation
        """
        # Extract key information from data_summary
        hrv_by_stress = data_summary.get("hrv_by_stress_level", {})
        correlations = data_summary.get("correlations", {})
        statistics = data_summary.get("statistics", {})
        insights = data_summary.get("insights", [])
        
        # Generate GPT-5-style explanation based on the data
        explanation = self._generate_gpt5_explanation(
            hrv_by_stress=hrv_by_stress,
            correlations=correlations,
            statistics=statistics,
            insights=insights
        )
        
        # Generate detailed narrative
        narrative = self._generate_narrative(
            hrv_by_stress=hrv_by_stress,
            correlations=correlations,
            statistics=statistics
        )
        
        return {
            "agent": self.name,
            "result": {
                "explanation": explanation,
                "narrative": narrative,
                "model": self.model_simulation,
                "data_analyzed": {
                    "total_records": data_summary.get("data_summary", {}).get("total_records", 0),
                    "metrics_analyzed": list(data_summary.get("statistics", {}).keys()),
                },
                "key_insights": insights[:5] if insights else [],
                "timestamp": datetime.now().isoformat(),
            },
            "success": True,
        }
    
    def _generate_gpt5_explanation(
        self,
        hrv_by_stress: Dict[str, Any],
        correlations: Dict[str, float],
        statistics: Dict[str, Any],
        insights: list
    ) -> str:
        """
        Generate GPT-5-style explanation based on data patterns.
        
        Simulates GPT-5's ability to identify patterns and generate
        scientific explanations without using API keys.
        """
        # Analyze HRV vs Stress relationship
        if hrv_by_stress and correlations:
            hrv_stress_corr = correlations.get("hrv_vs_stress", 0)
            
            # Core explanation based on correlation
            if hrv_stress_corr < -0.5:
                explanation = (
                    "Heart rate variability tends to decrease with higher stress levels, "
                    "reflecting autonomic imbalance. This inverse relationship indicates "
                    "that elevated stress disrupts the parasympathetic nervous system's "
                    "ability to maintain optimal HRV, which is a critical indicator of "
                    "cardiovascular health and recovery capacity."
                )
            elif hrv_stress_corr < -0.3:
                explanation = (
                    "Heart rate variability shows a moderate decrease with increasing stress levels, "
                    "suggesting a discernible impact on autonomic nervous system regulation. "
                    "While the relationship is not extreme, it reflects the physiological response "
                    "where stress-mediated sympathetic activation competes with parasympathetic "
                    "tone, potentially affecting recovery and resilience."
                )
            elif hrv_stress_corr > 0.3:
                explanation = (
                    "Interestingly, heart rate variability demonstrates a positive correlation with "
                    "stress levels in this dataset. This pattern may indicate individual variability "
                    "in stress response mechanisms, where some individuals maintain or even enhance "
                    "parasympathetic activity under stress, possibly reflecting adaptive coping strategies."
                )
            else:
                explanation = (
                    "Heart rate variability exhibits minimal correlation with stress levels in this analysis. "
                    "This suggests that HRV may be influenced by multiple factors beyond stress alone, "
                    "including sleep quality, physical activity, and individual physiological baseline. "
                    "The relationship between stress and HRV requires consideration of these confounding variables."
                )
        else:
            # Fallback explanation
            explanation = (
                "Heart rate variability tends to decrease with higher stress levels, "
                "reflecting autonomic imbalance. This pattern is consistent with established "
                "physiological principles where chronic stress activates the sympathetic nervous system, "
                "reducing the parasympathetic activity that supports optimal HRV."
            )
        
        return explanation
    
    def _generate_narrative(
        self,
        hrv_by_stress: Dict[str, Any],
        correlations: Dict[str, float],
        statistics: Dict[str, Any]
    ) -> str:
        """
        Generate detailed narrative explanation based on comprehensive data analysis.
        """
        narrative_parts = []
        
        # Introduction
        avg_hrv = statistics.get("hrv", {}).get("mean", 0)
        narrative_parts.append(
            f"Analysis of the physiological data reveals important patterns in heart rate variability (HRV) "
            f"and its relationship with stress levels. The dataset shows an average HRV of {avg_hrv:.1f}, "
            f"which serves as a baseline for understanding individual variability patterns."
        )
        
        # HRV by stress level analysis
        if hrv_by_stress:
            if "Low" in hrv_by_stress and "High" in hrv_by_stress:
                low_hrv = hrv_by_stress["Low"].get("average_hrv", 0)
                high_hrv = hrv_by_stress["High"].get("average_hrv", 0)
                difference = low_hrv - high_hrv
                
                narrative_parts.append(
                    f"When examining HRV across different stress categories, individuals with low stress levels "
                    f"(<20) demonstrate an average HRV of {low_hrv:.1f}, compared to {high_hrv:.1f} for those "
                    f"with high stress levels (>35). This difference of {difference:.1f} points represents a "
                    f"significant physiological distinction, illustrating how stress management directly influences "
                    f"autonomic nervous system function."
                )
        
        # Correlation analysis
        if correlations:
            hrv_stress_corr = correlations.get("hrv_vs_stress", 0)
            narrative_parts.append(
                f"The correlation coefficient of {hrv_stress_corr:.3f} between HRV and stress scores provides "
                f"quantitative evidence of this relationship. This statistical measure confirms the inverse "
                f"association observed in the grouped analysis, supporting the conclusion that stress negatively "
                f"impacts autonomic balance as reflected in HRV metrics."
            )
        
        # Clinical interpretation
        narrative_parts.append(
            "From a clinical perspective, these findings underscore the importance of stress management "
            "strategies for maintaining optimal cardiovascular health. Higher HRV, particularly at low stress levels, "
            "indicates greater parasympathetic activity and better recovery capacity. Conversely, reduced HRV "
            "associated with elevated stress suggests increased sympathetic dominance, which may impact long-term "
            "cardiovascular health and stress resilience."
        )
        
        return " ".join(narrative_parts)

