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
        self.openai_clients: Dict[str, Any] = {}
        
        if self.use_openai:
            try:
                self.openai_clients["premium"] = ChatOpenAI(
                    model="gpt-4o",
                    temperature=0.7,
                    api_key=self.api_key
                )
                print("[NarrativeAgent] Using OpenAI API with model: gpt-4o for premium responses")
            except Exception as primary_error:
                print(f"[NarrativeAgent] Unable to initialize gpt-4o: {primary_error}. Trying gpt-4-turbo-preview.")
                try:
                    self.openai_clients["premium"] = ChatOpenAI(
                        model="gpt-4-turbo-preview",
                        temperature=0.7,
                        api_key=self.api_key
                    )
                    print("[NarrativeAgent] Using OpenAI API with model: gpt-4-turbo-preview for premium responses")
                except Exception as fallback_error:
                    print(f"[NarrativeAgent] Error initializing OpenAI premium model: {fallback_error}. Falling back to mock mode.")
                    self.use_openai = False
            
            if self.use_openai:
                try:
                    self.openai_clients["lite"] = ChatOpenAI(
                        model="gpt-4o-mini",
                        temperature=0.6,
                        api_key=self.api_key
                    )
                    print("[NarrativeAgent] Using OpenAI API with model: gpt-4o-mini for lite responses")
                except Exception as lite_error:
                    print(f"[NarrativeAgent] Unable to initialize gpt-4o-mini: {lite_error}. Falling back to premium model for lite tier.")
                    self.openai_clients["lite"] = self.openai_clients.get("premium")
            
            self.llm = self.openai_clients.get("premium")
            if not self.llm:
                self.use_openai = False
        else:
            self.llm = None
        
        if self.use_openai and self.llm:
            self.model_name = getattr(self.llm, "model_name", "OpenAI Chat")
        else:
            self.llm = None
            if not OPENAI_AVAILABLE:
                self.model_name = "GPT-5 (simulated - langchain-openai not available)"
            elif not self.api_key:
                self.model_name = "GPT-5 (simulated - no API key)"
            else:
                self.model_name = "GPT-5 (simulated)"
            self.use_openai = False
        
        print(f"[NarrativeAgent] Initialized in {'OpenAI' if self.use_openai else 'Mock'} mode")
    
    def run(self, data_summary: Dict[str, Any], mode: Optional[str] = None, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate narrative explanation based on data summary using OpenAI API or mock mode.
        
        Args:
            data_summary: Dictionary containing data analysis results, including:
                - statistics: Basic statistics for HRV, stress_score, age
                - hrv_by_stress_level: Average HRV grouped by stress levels
                - correlations: Correlation coefficients
                - insights: List of insights from analysis
                - data_summary: Data metadata
            mode: Optional mode parameter (companion, status, science)
        
        Returns:
            Dictionary containing narrative text and explanation
        """
        mirror_story = None
        context = context or {}
        model_tier = "premium" if context.get("is_registered") else "lite"

        if self.use_openai:
            # Use OpenAI API
            explanation = self._generate_openai_explanation(data_summary, mode, model_tier, context)
            narrative = explanation  # Use the same explanation as narrative for OpenAI
        else:
            # Fall back to mock mode
            hrv_by_stress = data_summary.get("hrv_by_stress_level", {})
            correlations = data_summary.get("correlations", {})
            statistics = data_summary.get("statistics", {})
            insights = data_summary.get("insights", [])
            
            if mode == "mirror":
                mirror_story = self._generate_mirror_story(
                    data_summary=data_summary,
                    statistics=statistics,
                    correlations=correlations,
                    insights=insights
                )
                explanation = mirror_story.get("summary", "")
                narrative = mirror_story.get("energy_pattern", explanation)
            else:
                explanation = self._generate_gpt5_explanation(
                    hrv_by_stress=hrv_by_stress,
                    correlations=correlations,
                    statistics=statistics,
                    insights=insights,
                    mode=mode
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
                "model_tier": model_tier if self.use_openai else "mock",
                "data_analyzed": {
                    "total_records": data_summary.get("data_summary", {}).get("total_records", 0),
                    "metrics_analyzed": list(data_summary.get("statistics", {}).keys()),
                },
                "key_insights": data_summary.get("insights", [])[:5] if data_summary.get("insights") else [],
                "timestamp": datetime.now().isoformat(),
                **({"mirror_story": mirror_story} if mirror_story else {}),
            },
            "success": True,
        }
    
    def _generate_openai_explanation(
        self,
        data_summary: Dict[str, Any],
        mode: Optional[str],
        model_tier: str,
        context: Dict[str, Any]
    ) -> str:
        """
        Generate explanation using OpenAI API.
        
        Args:
            data_summary: Dictionary containing data analysis results
        
        Returns:
            AI-generated explanation string
        """
        try:
            llm_client = self.openai_clients.get("premium" if model_tier == "premium" else "lite") or self.llm
            if llm_client is None:
                raise RuntimeError("OpenAI client is not initialized")

            self.model_name = getattr(llm_client, "model_name", getattr(llm_client, "model", "OpenAI Chat"))

            data_str = self._format_data_summary(data_summary)
            
            # Create the prompt as specified
            system_message = SystemMessage(
                content="You are a scientific AI assistant. Provide clear, evidence-based explanations about physiological data, particularly regarding heart rate variability (HRV) and stress relationships. Use scientific terminology appropriately and explain complex concepts in an accessible manner."
            )
            
            human_message = HumanMessage(
                content=f"Explain how HRV relates to stress based on this data: {data_str}"
            )
            
            # Call OpenAI API
            response = llm_client.invoke([system_message, human_message])
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
        insights: list,
        mode: Optional[str] = None
    ) -> str:
        """
        Generate GPT-5-style explanation based on data patterns and mode.
        
        Simulates GPT-5's ability to identify patterns and generate
        scientific explanations without using API keys.
        
        Args:
            mode: Optional mode parameter (companion, status, science)
        """
        # Mode-specific tone adjustment
        if mode == "companion":
            # Warm, supportive tone for companion mode
            if hrv_by_stress and correlations:
                hrv_stress_corr = correlations.get("hrv_vs_stress", 0)
                if hrv_stress_corr < -0.3:
                    explanation = (
                        "我注意到你的心率变异性（HRV）与压力水平之间存在一定的关联。"
                        "当压力较高时，HRV 往往会降低，这反映了自主神经系统的平衡状态。"
                        "这并不意味着有什么问题，而是提醒我们关注自己的压力管理。"
                        "记住，你的身体正在努力适应，给自己一些时间和空间来恢复是很重要的。"
                        "如果你感到压力过大，不妨尝试一些放松技巧，比如深呼吸或轻度运动。"
                    )
                else:
                    explanation = (
                        "从你的数据来看，你的生理指标整体保持在一个相对稳定的范围内。"
                        "这是很好的迹象，说明你的身体有良好的适应能力。"
                        "继续保持这种平衡很重要，同时也要记得关注自己的感受。"
                        "如果你有任何担忧或想要讨论的话题，我随时在这里倾听。"
                    )
            else:
                explanation = (
                    "我很高兴你愿意分享和探索自己的状态。"
                    "每个人的身体和心理都是独特的，重要的是找到适合自己的节奏。"
                    "如果你感到困惑或需要支持，请随时告诉我，我会尽力帮助你。"
                    "记住，寻求帮助和理解自己都是成长的一部分。"
                )
            return explanation
            
        elif mode == "science":
            # Professional, scientific tone for science mode
            if hrv_by_stress and correlations:
                hrv_stress_corr = correlations.get("hrv_vs_stress", 0)
                if hrv_stress_corr < -0.5:
                    explanation = (
                        "Heart rate variability (HRV) demonstrates a significant inverse correlation "
                        "with stress levels (r = {:.3f}), indicating autonomic nervous system (ANS) "
                        "dysregulation. This relationship reflects the physiological mechanism where "
                        "elevated stress activates the sympathetic nervous system (SNS), thereby "
                        "suppressing parasympathetic nervous system (PNS) activity. HRV serves as a "
                        "non-invasive biomarker of ANS function, with lower HRV values correlating "
                        "with reduced vagal tone and compromised cardiovascular resilience. "
                        "Research indicates that chronic stress-induced HRV reduction may be associated "
                        "with increased risk of cardiovascular events and reduced recovery capacity."
                    ).format(hrv_stress_corr)
                else:
                    explanation = (
                        "The relationship between heart rate variability and stress levels in this dataset "
                        "shows a correlation coefficient of {:.3f}. HRV is quantified through time-domain "
                        "and frequency-domain analyses, with common metrics including RMSSD (root mean square "
                        "of successive differences) and SDNN (standard deviation of NN intervals). "
                        "The autonomic nervous system regulates HRV through the interplay between "
                        "sympathetic and parasympathetic branches, with higher HRV generally indicating "
                        "greater physiological flexibility and adaptive capacity."
                    ).format(hrv_stress_corr)
            else:
                explanation = (
                    "Heart rate variability (HRV) is a measure of the variation in time between successive "
                    "heartbeats, controlled by the autonomic nervous system. HRV analysis provides insights "
                    "into cardiovascular health, stress response, and recovery capacity. Key HRV metrics "
                    "include time-domain parameters (RMSSD, SDNN, pNN50) and frequency-domain parameters "
                    "(LF, HF power). Higher HRV typically indicates better cardiovascular health and "
                    "autonomic balance, while lower HRV may suggest increased stress or reduced recovery capacity."
                )
            return explanation
        
        # Default behavior (status mode or no mode specified)
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

    def _generate_mirror_story(
        self,
        data_summary: Dict[str, Any],
        statistics: Dict[str, Any],
        correlations: Dict[str, Any],
        insights: list
    ) -> Dict[str, str]:
        trend = data_summary.get("mirror_trend", [])
        coordination_score = data_summary.get("coordination_score", 78)
        summary = data_summary.get("insight_summary") or (
            "你正在保持专注，但恢复速度略低于平均。"
        )
        energy_pattern = data_summary.get("energy_pattern")

        if not energy_pattern and trend:
            first = trend[0]
            last = trend[-1]
            if last["hrv"] < first["hrv"] and last["stress"] > first["stress"]:
                energy_pattern = "过去三天里，HRV 在收敛，但专注轨迹依旧上扬。意志力在前行，身体正追赶它的节拍。"
            elif last["hrv"] > first["hrv"]:
                energy_pattern = "你的生理节奏正在变柔和、灵活。每一次呼吸都像涟漪，向外扩散着恢复力。"
            else:
                energy_pattern = "你的系统维持在一个可持续的区间，张力与恢复在对话，需要一点点温柔的空间。"

        if not energy_pattern:
            energy_pattern = "你的生理节奏与心理波动正在互相靠近，意义感让系统慢慢同步。"

        hero_meta = data_summary.get("hero", {})
        top_dialog = hero_meta.get("top_dialog") or "你好，旅人。我们在这里照见你体内的流动，倾听那尚未被诉说的节奏。"

        if not summary and insights:
            summary = insights[0]

        coordination_phrase = f"当前协同指数为 {coordination_score}%，身体与心智正在寻找一条共同的轨迹。"

        energy_pattern_full = f"{energy_pattern} {coordination_phrase}"

        return {
            "summary": summary,
            "energy_pattern": energy_pattern_full,
            "top_dialog": top_dialog,
        }

