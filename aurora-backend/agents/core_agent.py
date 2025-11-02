"""
Core Agent - Orchestrates all sub-agents based on query type.
"""

from typing import Dict, Any, Optional, List
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
    
    def __init__(self, enable_debug_logging: bool = False):
        """
        Initialize the Core Agent and sub-agents.
        
        Args:
            enable_debug_logging: If True, logs agent executions for debugging
        """
        self.name = "AuroraCoreAgent"
        self.data_agent = DataAgent()
        self.viz_agent = VizAgent()
        self.narrative_agent = NarrativeAgent()
        self.enable_debug_logging = enable_debug_logging
        self.execution_log: List[str] = []
        
        # Agent name mapping for debug output
        self.agent_name_map = {
            "DataAgent": "AuroraDataAnalystAgent",
            "VizAgent": "AuroraVizAgent",
            "NarrativeAgent": "AuroraNarrativeAgent"
        }
    
    def _log_agent_execution(self, agent_name: str, agent_result: Dict[str, Any]):
        """
        Log agent execution for debugging purposes.
        
        Args:
            agent_name: Name of the agent that was executed
            agent_result: Result dictionary from the agent
        """
        if self.enable_debug_logging:
            friendly_name = self.agent_name_map.get(agent_name, agent_name)
            log_entry = f"{friendly_name} executed"
            self.execution_log.append(log_entry)
            print(f"[Debug] {log_entry}")
            print(f"[Debug] Agent output keys: {list(agent_result.keys())}")
    
    def get_execution_log(self) -> List[str]:
        """
        Get the execution log of agents that have been executed.
        
        Returns:
            List of execution log entries like ["AuroraDataAnalystAgent executed", ...]
        """
        return self.execution_log.copy()
    
    def clear_execution_log(self):
        """Clear the execution log"""
        self.execution_log.clear()
    
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
            self._log_agent_execution(self.data_agent.name, data_result)
            result["data"] = data_result.get("result", {})
        
        # 2. If query includes "visualize" → call VizAgent
        if "visualize" in query_lower:
            # Need data for visualization, so run DataAgent first if not already done
            if "data" not in result:
                data_result = self.data_agent.run(query, context)
                self._log_agent_execution(self.data_agent.name, data_result)
                result["data"] = data_result.get("result", {})
            
            viz_result = self.viz_agent.run(query, result.get("data"))
            self._log_agent_execution(self.viz_agent.name, viz_result)
            result["chart"] = viz_result.get("result", {}).get("plotly_json", {})
        
        # 3. If query includes "explain" → call NarrativeAgent
        if "explain" in query_lower:
            # Need data for explanation, so run DataAgent first if not already done
            if "data" not in result:
                data_result = self.data_agent.run(query, context)
                self._log_agent_execution(self.data_agent.name, data_result)
                result["data"] = data_result.get("result", {})
            
            narrative_result = self.narrative_agent.run(result["data"])
            self._log_agent_execution(self.narrative_agent.name, narrative_result)
            # Extract explanation text
            result["insight"] = narrative_result.get("result", {}).get("explanation", "")
        
        # 4. Otherwise → run all and return combined results
        if not any(keyword in query_lower for keyword in ["analyze", "visualize", "explain"]):
            # Run all agents
            data_result = self.data_agent.run(query, context)
            self._log_agent_execution(self.data_agent.name, data_result)
            result["data"] = data_result.get("result", {})
            
            viz_result = self.viz_agent.run(query, result["data"])
            self._log_agent_execution(self.viz_agent.name, viz_result)
            result["chart"] = viz_result.get("result", {}).get("plotly_json", {})
            
            narrative_result = self.narrative_agent.run(result["data"])
            self._log_agent_execution(self.narrative_agent.name, narrative_result)
            result["insight"] = narrative_result.get("result", {}).get("explanation", "")
        
        return result
    

