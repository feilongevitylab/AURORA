"""
Narrative Agent - Handles natural language explanation and story generation.
"""

from typing import Dict, Any, Optional
from datetime import datetime
import random


class NarrativeAgent:
    """
    Agent responsible for narrative operations including:
    - Natural language explanations
    - Story generation from data insights
    - Summarization
    - Contextual narratives
    """
    
    def __init__(self):
        """Initialize the Narrative Agent"""
        self.name = "NarrativeAgent"
    
    def run(self, query: str, data: Optional[Dict[str, Any]] = None, 
            insights: Optional[list] = None) -> Dict[str, Any]:
        """
        Generate narrative explanation based on query and data insights.
        
        Args:
            query: Original user query
            data: Optional processed data
            insights: Optional list of insights from analysis
        
        Returns:
            Dictionary containing narrative text and summary
        """
        # Generate mock narrative
        narrative_templates = [
            "Based on the analysis of your physiological data, we observed {trend} patterns over the selected time period.",
            "The data indicates {key_finding}, which suggests {interpretation}.",
            "Our analysis reveals {insight}, showing {implication} for your overall health metrics.",
            "Examining the temporal patterns, we found {pattern} that correlates with {factor}.",
        ]
        
        mock_insights = insights or [
            "Average HRV increased by 15% over the past week",
            "Stress levels peaked during afternoon hours",
            "Sleep quality correlates with morning recovery metrics",
        ]
        
        # Generate narrative text
        narrative = self._generate_narrative(query, mock_insights)
        
        # Generate summary
        summary = self._generate_summary(mock_insights)
        
        # Generate key takeaways
        takeaways = [
            f"Takeaway 1: {mock_insights[0] if mock_insights else 'Significant pattern detected'}",
            f"Takeaway 2: {mock_insights[1] if len(mock_insights) > 1 else 'Trend analysis completed'}",
            f"Takeaway 3: {mock_insights[2] if len(mock_insights) > 2 else 'Recommendations available'}",
        ]
        
        return {
            "agent": self.name,
            "result": {
                "narrative": narrative,
                "summary": summary,
                "key_takeaways": takeaways,
                "insights_used": mock_insights,
                "tone": "professional",
                "length": "medium",
                "timestamp": datetime.now().isoformat(),
            },
            "success": True,
        }
    
    def _generate_narrative(self, query: str, insights: list) -> str:
        """Generate narrative text from query and insights"""
        if not insights:
            insights = ["baseline measurements", "normal ranges", "standard patterns"]
        
        narrative = f"""
Based on your query: "{query}", here's what the data tells us:

The analysis of your physiological measurements reveals several interesting patterns. 
First, we observed that {insights[0] if insights else 'the data follows expected trends'}. 
This suggests that your baseline metrics are within normal operational ranges.

Additionally, {insights[1] if len(insights) > 1 else 'temporal analysis shows consistent patterns'} 
indicating stable physiological responses. These findings align with established 
medical research on typical biometric variations.

In conclusion, the comprehensive review of your data demonstrates {insights[2] if len(insights) > 2 else 'a healthy profile'} 
with recommendations for continued monitoring and proactive health management.
        """.strip()
        
        return narrative
    
    def _generate_summary(self, insights: list) -> str:
        """Generate concise summary"""
        if not insights:
            return "Data analysis completed successfully with no significant anomalies detected."
        
        summary = f"Analysis identified {len(insights)} key insights: "
        summary += "; ".join(insights[:3])  # First 3 insights
        if len(insights) > 3:
            summary += f", and {len(insights) - 3} additional findings."
        
        return summary

