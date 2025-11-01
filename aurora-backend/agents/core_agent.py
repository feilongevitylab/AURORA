"""
Core Agent - Orchestrates all sub-agents based on query type.
"""

from typing import Dict, Any, Optional
from datetime import datetime

from .data_agent import DataAgent
from .viz_agent import VizAgent
from .narrative_agent import NarrativeAgent


class AuroraCoreAgent:
    """
    Core orchestration agent that coordinates all sub-agents.
    Determines query type and delegates to appropriate agents:
    - analysis: DataAgent
    - visualization: VizAgent
    - explanation/narrative: NarrativeAgent
    - combined: All agents
    """
    
    def __init__(self):
        """Initialize the Core Agent and sub-agents"""
        self.name = "AuroraCoreAgent"
        self.data_agent = DataAgent()
        self.viz_agent = VizAgent()
        self.narrative_agent = NarrativeAgent()
    
    def run(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Orchestrate agent execution based on query keywords.
        
        Logic:
        1. If query includes "analyze" → call DataAgent
        2. If query includes "visualize" → call VizAgent
        3. If query includes "explain" → call NarrativeAgent
        4. Otherwise → run all and return combined results
        
        Args:
            query: User's natural language query
            context: Optional context data
        
        Returns:
            Structured JSON with keys: data, chart, insight
        """
        query_lower = query.lower()
        
        # Initialize result structure
        result = {}
        
        # 1. If query includes "analyze" → call DataAgent
        if "analyze" in query_lower:
            data_result = self.data_agent.run(query, context)
            result["data"] = data_result.get("result", {})
        
        # 2. If query includes "visualize" → call VizAgent
        if "visualize" in query_lower:
            # Need data for visualization, so run DataAgent first if not already done
            if "data" not in result:
                data_result = self.data_agent.run(query, context)
                result["data"] = data_result.get("result", {})
            
            viz_result = self.viz_agent.run(query, result.get("data"))
            result["chart"] = viz_result.get("result", {}).get("plotly_json", {})
        
        # 3. If query includes "explain" → call NarrativeAgent
        if "explain" in query_lower:
            # Need data for explanation, so run DataAgent first if not already done
            if "data" not in result:
                data_result = self.data_agent.run(query, context)
                result["data"] = data_result.get("result", {})
            
            narrative_result = self.narrative_agent.run(result["data"])
            # Extract explanation text
            result["insight"] = narrative_result.get("result", {}).get("explanation", "")
        
        # 4. Otherwise → run all and return combined results
        if not any(keyword in query_lower for keyword in ["analyze", "visualize", "explain"]):
            # Run all agents
            data_result = self.data_agent.run(query, context)
            result["data"] = data_result.get("result", {})
            
            viz_result = self.viz_agent.run(query, result["data"])
            result["chart"] = viz_result.get("result", {}).get("plotly_json", {})
            
            narrative_result = self.narrative_agent.run(result["data"])
            result["insight"] = narrative_result.get("result", {}).get("explanation", "")
        
        return result
    

