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
        
        # Query type keywords
        self.analysis_keywords = [
            "analyze", "analysis", "analyze", "statistics", "stats",
            "calculate", "compute", "process", "data"
        ]
        self.viz_keywords = [
            "visualize", "visualization", "chart", "graph", "plot",
            "show", "display", "diagram", "visual"
        ]
        self.narrative_keywords = [
            "explain", "explanation", "describe", "story", "narrative",
            "tell", "summary", "summary", "interpret"
        ]
    
    def run(self, query: str, query_type: Optional[str] = None, 
            context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Orchestrate agent execution based on query type.
        
        Args:
            query: User's natural language query
            query_type: Explicit query type ("analysis", "visualization", "explanation", "combined")
                       If None, will be auto-detected
            context: Optional context data
        
        Returns:
            Dictionary containing results from all relevant agents
        """
        # Auto-detect query type if not provided
        if not query_type:
            query_type = self._detect_query_type(query)
        
        results = {
            "query": query,
            "query_type": query_type,
            "timestamp": datetime.now().isoformat(),
            "agents_executed": [],
        }
        
        # Execute agents based on query type
        if query_type == "analysis":
            results["analysis"] = self.data_agent.run(query, context)
            results["agents_executed"].append("DataAgent")
            
        elif query_type == "visualization":
            data_result = self.data_agent.run(query, context)
            results["analysis"] = data_result
            results["visualization"] = self.viz_agent.run(query, data_result.get("result"))
            results["agents_executed"].extend(["DataAgent", "VizAgent"])
            
        elif query_type == "explanation":
            data_result = self.data_agent.run(query, context)
            results["analysis"] = data_result
            insights = data_result.get("result", {}).get("insights", [])
            results["narrative"] = self.narrative_agent.run(query, data_result.get("result"), insights)
            results["agents_executed"].extend(["DataAgent", "NarrativeAgent"])
            
        elif query_type == "combined":
            # Execute all agents
            data_result = self.data_agent.run(query, context)
            results["analysis"] = data_result
            
            insights = data_result.get("result", {}).get("insights", [])
            results["visualization"] = self.viz_agent.run(query, data_result.get("result"))
            results["narrative"] = self.narrative_agent.run(query, data_result.get("result"), insights)
            results["agents_executed"].extend(["DataAgent", "VizAgent", "NarrativeAgent"])
            
        else:
            # Default: run all agents
            data_result = self.data_agent.run(query, context)
            results["analysis"] = data_result
            insights = data_result.get("result", {}).get("insights", [])
            results["visualization"] = self.viz_agent.run(query, data_result.get("result"))
            results["narrative"] = self.narrative_agent.run(query, data_result.get("result"), insights)
            results["agents_executed"].extend(["DataAgent", "VizAgent", "NarrativeAgent"])
        
        # Generate final response summary
        results["summary"] = self._generate_response_summary(query_type, results)
        results["success"] = True
        
        return {
            "agent": self.name,
            "result": results,
            "success": True,
        }
    
    def _detect_query_type(self, query: str) -> str:
        """
        Detect query type from natural language query.
        
        Returns:
            "analysis", "visualization", "explanation", or "combined"
        """
        query_lower = query.lower()
        
        has_analysis = any(keyword in query_lower for keyword in self.analysis_keywords)
        has_viz = any(keyword in query_lower for keyword in self.viz_keywords)
        has_narrative = any(keyword in query_lower for keyword in self.narrative_keywords)
        
        # Count matches to determine type
        match_count = sum([has_analysis, has_viz, has_narrative])
        
        if match_count == 0:
            # Default to combined if no keywords detected
            return "combined"
        elif match_count == 1:
            # Single intent
            if has_analysis and not has_viz and not has_narrative:
                return "analysis"
            elif has_viz:
                return "visualization"
            elif has_narrative:
                return "explanation"
        else:
            # Multiple intents - return combined
            return "combined"
    
    def _generate_response_summary(self, query_type: str, results: Dict[str, Any]) -> str:
        """Generate a summary of the agent execution"""
        agents_count = len(results.get("agents_executed", []))
        
        summary = f"""
Query processed successfully using {agents_count} agent(s).
Query type: {query_type}
Agents executed: {', '.join(results.get('agents_executed', []))}
        """.strip()
        
        return summary

