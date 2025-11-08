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
        Orchestrate agent execution based on query keywords and mode context.
        
        Logic:
        1. If query includes "analyze" → call DataAgent
        2. If query includes "visualize" → call VizAgent
        3. If query includes "explain" → call NarrativeAgent
        4. Otherwise → run all and return combined results
        
        Mode-based behavior:
        - companion mode: Prioritize NarrativeAgent with warm tone
        - mirror mode: Combine DataAgent + VizAgent + NarrativeAgent with layered insights
        - science mode: Prioritize NarrativeAgent with professional tone
        
        Args:
            query: User's natural language query
            context: Optional context data (may contain mode information)
        
        Returns:
            Structured JSON with keys: data, chart, insight
        """
        query_lower = query.lower()
        mode = context.get("mode") if context else None
        
        # Initialize result structure
        result = {}
        
        # Mode-based routing
        if mode == "companion":
            # Companion mode: Prioritize narrative/insight
            if "data" not in result:
                data_result = self.data_agent.run(query, context)
                self._log_agent_execution(self.data_agent.name, data_result)
                result["data"] = data_result.get("result", {})
            
            narrative_result = self.narrative_agent.run(result["data"], mode=mode)
            self._log_agent_execution(self.narrative_agent.name, narrative_result)
            result["insight"] = narrative_result.get("result", {}).get("explanation", "")
            
        elif mode == "mirror":
            # Mirror mode: Combine layered data, visualization, and narrative
            data_result = self.data_agent.run(query, context)
            self._log_agent_execution(self.data_agent.name, data_result)
            result["data"] = data_result.get("result", {})
            
            viz_result = self.viz_agent.run(query, result["data"])
            self._log_agent_execution(self.viz_agent.name, viz_result)
            result["chart"] = viz_result.get("result", {}).get("plotly_json", {})
            
            # Also include narrative for context
            narrative_result = self.narrative_agent.run(result["data"], mode=mode)
            self._log_agent_execution(self.narrative_agent.name, narrative_result)
            narrative_payload = narrative_result.get("result", {})
            result["insight"] = narrative_payload.get("explanation", "")

            mirror_story = narrative_payload.get("mirror_story") or {}
            if result.get("data") is not None:
                hero_meta = result["data"].get("hero", {})
                hero_meta.setdefault("top_dialog", mirror_story.get("top_dialog"))
                hero_meta.setdefault("mirror_summary", mirror_story.get("summary"))
                result["data"]["hero"] = hero_meta
                if "energy_pattern" not in result["data"] and mirror_story.get("energy_pattern"):
                    result["data"]["energy_pattern"] = mirror_story["energy_pattern"]

            if result["data"].get("hero"):
                result["hero"] = result["data"]["hero"]
            if mirror_story.get("summary"):
                result["insight"] = mirror_story["summary"]
            
        elif mode == "science":
            # Science mode: Prioritize narrative with professional tone
            if "data" not in result:
                data_result = self.data_agent.run(query, context)
                self._log_agent_execution(self.data_agent.name, data_result)
                result["data"] = data_result.get("result", {})
            
            narrative_result = self.narrative_agent.run(result["data"], mode=mode)
            self._log_agent_execution(self.narrative_agent.name, narrative_result)
            result["insight"] = narrative_result.get("result", {}).get("explanation", "")
            
        else:
            # Default behavior: keyword-based routing
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
                
                narrative_result = self.narrative_agent.run(result["data"], mode=mode)
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
                
                narrative_result = self.narrative_agent.run(result["data"], mode=mode)
                self._log_agent_execution(self.narrative_agent.name, narrative_result)
                result["insight"] = narrative_result.get("result", {}).get("explanation", "")
        
        return result
    

