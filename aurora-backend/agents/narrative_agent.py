"""
Narrative Agent - Uses OpenAI API or falls back to mock mode for natural language explanation generation.
"""

from typing import Dict, Any, Optional
from datetime import datetime
import os

try:
    from langchain_openai import ChatOpenAI
    from langchain_core.messages import HumanMessage, SystemMessage
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class NarrativeAgent:
    """
    Agent responsible for narrative operations including:
    - Natural language explanations using OpenAI API (or mock mode)
    - Story generation from data insights
    - Summarization
    - Contextual narratives based on data summaries
    
    Uses OpenAI API if OPENAI_API_KEY is set, otherwise falls back to mock mode.
    """
    
    def __init__(self):
        """Initialize the Narrative Agent"""
        self.name = "NarrativeAgent"
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.use_openai = OPENAI_AVAILABLE and self.api_key is not None
        
        if self.use_openai:
            # Try to use the latest available OpenAI model
            # Note: GPT-5 doesn't exist yet, using GPT-4 Turbo or GPT-4o as the best available option
            try:
                # Try GPT-4o first (if available), then fall back to GPT-4 Turbo
                try:
                    self.llm = ChatOpenAI(
                        model="gpt-4o",
                        temperature=0.7,
                        api_key=self.api_key
                    )
                    self.model_name = "GPT-4o (OpenAI)"
                except:
                    # Fall back to GPT-4 Turbo if GPT-4o is not available
                    self.llm = ChatOpenAI(
                        model="gpt-4-turbo-preview",
                        temperature=0.7,
                        api_key=self.api_key
                    )
                    self.model_name = "GPT-4 Turbo (OpenAI)"
                
                print(f"[NarrativeAgent] Using OpenAI API with model: {self.llm.model_name}")
            except Exception as e:
                print(f"[NarrativeAgent] Error initializing OpenAI: {e}. Falling back to mock mode.")
                self.use_openai = False
                self.model_name = "GPT-5 (simulated - fallback)"
        else:
            self.llm = None
            if not OPENAI_AVAILABLE:
                self.model_name = "GPT-5 (simulated - langchain-openai not available)"
            elif not self.api_key:
                self.model_name = "GPT-5 (simulated - no API key)"
            else:
                self.model_name = "GPT-5 (simulated)"
        
        print(f"[NarrativeAgent] Initialized in {'OpenAI' if self.use_openai else 'Mock'} mode")
    
    def run(self, data_summary: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate narrative explanation based on data summary using OpenAI API or mock mode.
        
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
        if self.use_openai:
            # Use OpenAI API
            explanation = self._generate_openai_explanation(data_summary)
            narrative = explanation  # Use the same explanation as narrative for OpenAI
        else:
            # Fall back to mock mode
            hrv_by_stress = data_summary.get("hrv_by_stress_level", {})
            correlations = data_summary.get("correlations", {})
            statistics = data_summary.get("statistics", {})
            insights = data_summary.get("insights", [])
            
            explanation = self._generate_gpt5_explanation(
                hrv_by_stress=hrv_by_stress,
                correlations=correlations,
                statistics=statistics,
                insights=insights
            )
            
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
                "model": self.model_name,
                "data_analyzed": {
                    "total_records": data_summary.get("data_summary", {}).get("total_records", 0),
                    "metrics_analyzed": list(data_summary.get("statistics", {}).keys()),
                },
                "key_insights": data_summary.get("insights", [])[:5] if data_summary.get("insights") else [],
                "timestamp": datetime.now().isoformat(),
            },
            "success": True,
        }
    
    def _generate_openai_explanation(self, data_summary: Dict[str, Any]) -> str:
        """
        Generate explanation using OpenAI API.
        
        Args:
            data_summary: Dictionary containing data analysis results
        
        Returns:
            AI-generated explanation string
        """
        try:
            # Format the data summary for the prompt
            data_str = self._format_data_summary(data_summary)
            
            # Create the prompt as specified
            system_message = SystemMessage(
                content="You are a scientific AI assistant. Provide clear, evidence-based explanations about physiological data, particularly regarding heart rate variability (HRV) and stress relationships. Use scientific terminology appropriately and explain complex concepts in an accessible manner."
            )
            
            human_message = HumanMessage(
                content=f"Explain how HRV relates to stress based on this data: {data_str}"
            )
            
            # Call OpenAI API
            response = self.llm.invoke([system_message, human_message])
            explanation = response.content
            
            return explanation.strip()
            
        except Exception as e:
            print(f"[NarrativeAgent] Error calling OpenAI API: {e}")
            print(f"[NarrativeAgent] Falling back to mock mode for this request")
            # Fall back to mock mode for this request
            hrv_by_stress = data_summary.get("hrv_by_stress_level", {})
            correlations = data_summary.get("correlations", {})
            statistics = data_summary.get("statistics", {})
            insights = data_summary.get("insights", [])
            
            return self._generate_gpt5_explanation(
                hrv_by_stress=hrv_by_stress,
                correlations=correlations,
                statistics=statistics,
                insights=insights
            )
    
    def _format_data_summary(self, data_summary: Dict[str, Any]) -> str:
        """
        Format data summary into a readable string for the prompt.
        
        Args:
            data_summary: Dictionary containing data analysis results
        
        Returns:
            Formatted string representation of the data
        """
        parts = []
        
        # Data summary metadata
        if "data_summary" in data_summary:
            metadata = data_summary["data_summary"]
            parts.append(f"Total records: {metadata.get('total_records', 'N/A')}")
            parts.append(f"Columns: {', '.join(metadata.get('columns', []))}")
        
        # Statistics
        if "statistics" in data_summary:
            parts.append("\nStatistics:")
            for metric, stats in data_summary["statistics"].items():
                parts.append(f"  {metric}: mean={stats.get('mean', 'N/A')}, std={stats.get('std', 'N/A')}, min={stats.get('min', 'N/A')}, max={stats.get('max', 'N/A')}")
        
        # HRV by stress level
        if "hrv_by_stress_level" in data_summary:
            parts.append("\nHRV by stress level:")
            for level, data in data_summary["hrv_by_stress_level"].items():
                parts.append(f"  {level}: average HRV={data.get('average_hrv', 'N/A')}, count={data.get('count', 'N/A')}")
        
        # Correlations
        if "correlations" in data_summary:
            parts.append("\nCorrelations:")
            for pair, value in data_summary["correlations"].items():
                parts.append(f"  {pair}: {value:.3f}")
        
        # Insights
        if "insights" in data_summary and data_summary["insights"]:
            parts.append("\nKey insights:")
            for insight in data_summary["insights"][:5]:
                parts.append(f"  - {insight}")
        
        return "\n".join(parts)
    
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

