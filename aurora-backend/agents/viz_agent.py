"""
Visualization Agent - Handles chart generation using Plotly.
"""

from typing import Dict, Any, Optional
from datetime import datetime
import plotly.graph_objects as go
import pandas as pd
import json
import os


class VizAgent:
    """
    Agent responsible for visualization operations including:
    - Chart generation using Plotly
    - HRV vs Stress scatter plot generation
    - Visual data representation
    """
    
    def __init__(self):
        """Initialize the Visualization Agent"""
        self.name = "VizAgent"
    
    def run(self, query: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate visualization using Plotly for HRV vs Stress scatter plot.
        
        Args:
            query: Natural language query for visualization
            data: Optional data to visualize (can contain DataAgent results)
        
        Returns:
            Dictionary containing Plotly figure as JSON
        """
        # Generate scatter plot of HRV vs Stress
        fig = self._create_hrv_vs_stress_scatter()
        
        # Convert figure to JSON using to_json() with default engine
        # This returns a JSON string that we parse to dict
        fig_json = json.loads(fig.to_json())
        
        return {
            "agent": self.name,
            "result": {
                "chart_type": "scatter",
                "plotly_json": fig_json,
                "query": query,
                "recommendations": [
                    "Scatter plot showing HRV vs Stress relationship",
                    "Interactive zoom and pan enabled",
                    "Hover tooltips show individual data points",
                ],
                "timestamp": datetime.now().isoformat(),
            },
            "success": True,
        }
    
    def _create_hrv_vs_stress_scatter(self) -> go.Figure:
        """
        Create a scatter plot of HRV vs Stress using Plotly.
        Uses mock data from CSV file or generates mock data.
        
        Returns:
            Plotly Figure object
        """
        # Load mock HRV data
        df = self._load_mock_data()
        
        # Create scatter plot
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df["stress_score"],
            y=df["hrv"],
            mode='markers',
            marker=dict(
                size=12,
                color=df["hrv"],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="HRV"),
                line=dict(width=1, color='white')
            ),
            text=[f"ID: {id}, Age: {age}" for id, age in zip(df["id"], df["age"])],
            hovertemplate='<b>Stress Score</b>: %{x}<br>' +
                         '<b>HRV</b>: %{y}<br>' +
                         '%{text}<br>' +
                         '<extra></extra>',
            name='HRV vs Stress'
        ))
        
        # Update layout
        fig.update_layout(
            title={
                'text': 'HRV vs Stress Score Scatter Plot',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20}
            },
            xaxis=dict(
                title='Stress Score',
                showgrid=True,
                gridcolor='lightgray',
                zeroline=True
            ),
            yaxis=dict(
                title='Heart Rate Variability (HRV)',
                showgrid=True,
                gridcolor='lightgray',
                zeroline=True
            ),
            hovermode='closest',
            template='plotly_white',
            width=800,
            height=600,
            showlegend=False
        )
        
        return fig
    
    def _load_mock_data(self) -> pd.DataFrame:
        """
        Load mock HRV data from CSV or generate if not exists.
        
        Returns:
            DataFrame with columns: id, hrv, stress_score, age
        """
        csv_path = "mock_hrv_data.csv"
        
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
        else:
            # Generate mock data if CSV doesn't exist
            mock_data = {
                "id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                "hrv": [45.2, 52.8, 38.5, 61.3, 49.7, 55.1, 42.9, 58.6, 48.3, 
                       53.7, 40.1, 56.4, 47.2, 59.8, 44.6],
                "stress_score": [25, 15, 45, 10, 30, 20, 50, 12, 35, 18, 55, 
                                22, 28, 8, 40],
                "age": [28, 32, 25, 35, 30, 27, 22, 38, 29, 33, 26, 31, 34, 40, 24]
            }
            df = pd.DataFrame(mock_data)
            # Save for future use
            df.to_csv(csv_path, index=False)
        
        return df

