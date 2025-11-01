"""
Visualization Agent - Handles chart generation and visualization configuration.
"""

from typing import Dict, Any, Optional
from datetime import datetime
import random


class VizAgent:
    """
    Agent responsible for visualization operations including:
    - Chart type selection
    - Visualization configuration
    - Plotly.js chart specs generation
    - Visual data representation
    """
    
    def __init__(self):
        """Initialize the Visualization Agent"""
        self.name = "VizAgent"
        self.chart_types = ["line", "bar", "scatter", "pie", "heatmap", "box"]
    
    def run(self, query: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate visualization configuration based on the query and data.
        
        Args:
            query: Natural language query for visualization
            data: Optional data to visualize
        
        Returns:
            Dictionary containing Plotly.js configuration
        """
        # Determine appropriate chart type based on query
        chart_type = self._determine_chart_type(query)
        
        # Mock Plotly.js configuration
        plotly_config = {
            "data": [
                {
                    "x": list(range(10)),
                    "y": [random.uniform(0, 100) for _ in range(10)],
                    "type": chart_type,
                    "name": "Dataset 1",
                    "marker": {
                        "color": self._get_color_for_type(chart_type),
                    },
                }
            ],
            "layout": {
                "title": {
                    "text": self._generate_title(query),
                    "font": {"size": 18},
                },
                "xaxis": {
                    "title": "Time",
                    "showgrid": True,
                },
                "yaxis": {
                    "title": "Value",
                    "showgrid": True,
                },
                "hovermode": "closest",
                "template": "plotly_white",
            },
            "config": {
                "responsive": True,
                "displayModeBar": True,
            },
        }
        
        return {
            "agent": self.name,
            "result": {
                "chart_type": chart_type,
                "plotly_config": plotly_config,
                "recommendations": [
                    f"Recommended chart type: {chart_type}",
                    "Interactive zoom and pan enabled",
                    "Hover tooltips configured",
                ],
                "timestamp": datetime.now().isoformat(),
            },
            "success": True,
        }
    
    def _determine_chart_type(self, query: str) -> str:
        """Determine the best chart type based on query keywords"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["trend", "over time", "timeline"]):
            return "line"
        elif any(word in query_lower for word in ["compare", "category", "bar"]):
            return "bar"
        elif any(word in query_lower for word in ["correlation", "scatter", "relationship"]):
            return "scatter"
        elif any(word in query_lower for word in ["distribution", "box", "whisker"]):
            return "box"
        elif any(word in query_lower for word in ["heatmap", "correlation matrix"]):
            return "heatmap"
        elif any(word in query_lower for word in ["pie", "proportion", "percentage"]):
            return "pie"
        else:
            return random.choice(self.chart_types)
    
    def _get_color_for_type(self, chart_type: str) -> str:
        """Get color scheme for chart type"""
        color_map = {
            "line": "rgb(59, 130, 246)",
            "bar": "rgb(139, 92, 246)",
            "scatter": "rgb(236, 72, 153)",
            "pie": "rgb(251, 191, 36)",
            "heatmap": "rgb(34, 197, 94)",
            "box": "rgb(249, 115, 22)",
        }
        return color_map.get(chart_type, "rgb(59, 130, 246)")
    
    def _generate_title(self, query: str) -> str:
        """Generate a title for the visualization"""
        # Extract key terms or use query as title
        if len(query) > 60:
            return query[:57] + "..."
        return query or "Data Visualization"

