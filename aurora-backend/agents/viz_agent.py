"""
Visualization Agent - Handles chart generation using Plotly.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
import plotly.graph_objects as go
import json
import pandas as pd
import numpy as np

from data.mock_datasets import load_base_hrv_df


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
        dataset_label = None
        if data:
            dataset_label = (
                data.get("data_summary", {}).get("dataset")
                or data.get("metadata", {}).get("dataset")
            )

        alternate_views: List[Dict[str, Any]] = []

        if dataset_label == "longevity_hrv_stress":
            fig, alternate_views, recommendations = self._create_longevity_hrv_stress_views(data)
            chart_type = "longevity_hrv_stress_scatter"
        elif data and data.get("mirror_trend"):
            fig = self._create_mirror_trend_chart(data["mirror_trend"])
            chart_type = "mirror_trend"
            recommendations = [
                "Line chart showing HRV, Stress, and Focus trends over time",
                "Use legend to toggle individual layers",
                "Hover each point to inspect precise readings",
            ]
        else:
            fig = self._create_hrv_vs_stress_scatter()
            chart_type = "scatter"
            recommendations = [
                "Scatter plot showing HRV vs Stress relationship",
                "Interactive zoom and pan enabled",
                "Hover tooltips show individual data points",
            ]

        fig_json = json.loads(fig.to_json())

        return {
            "agent": self.name,
            "result": {
                "chart_type": chart_type,
                "plotly_json": fig_json,
                "alternate_views": [
                    {"id": view["id"], "label": view["label"], "plotly_json": view["plotly_json"]}
                    for view in alternate_views
                ],
                "query": query,
                "recommendations": recommendations,
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
    
    def _create_mirror_trend_chart(self, trend_data: list) -> go.Figure:
        fig = go.Figure()

        dates = [point["date"] for point in trend_data]
        hrv_values = [point["hrv"] for point in trend_data]
        stress_values = [point["stress"] for point in trend_data]
        focus_values = [point["focus"] for point in trend_data]

        fig.add_trace(go.Scatter(
            x=dates,
            y=hrv_values,
            mode='lines+markers',
            name='HRV',
            line=dict(color='#4F46E5', width=3),
            marker=dict(size=8, symbol='circle'),
        ))

        fig.add_trace(go.Scatter(
            x=dates,
            y=stress_values,
            mode='lines+markers',
            name='Stress',
            line=dict(color='#FB7185', width=3, dash='dash'),
            marker=dict(size=8, symbol='diamond'),
        ))

        fig.add_trace(go.Scatter(
            x=dates,
            y=focus_values,
            mode='lines+markers',
            name='Focus',
            line=dict(color='#22D3EE', width=3, dash='dot'),
            marker=dict(size=8, symbol='square'),
        ))

        fig.update_layout(
            title={
                'text': 'Mirror Trend · HRV / Stress / Focus',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20}
            },
            xaxis=dict(
                title='Date',
                showgrid=True,
                gridcolor='rgba(79,70,229,0.08)',
            ),
            yaxis=dict(
                title='Normalized Score',
                showgrid=True,
                gridcolor='rgba(79,70,229,0.08)',
                range=[0, 100],
            ),
            hovermode='x unified',
            template='plotly_white',
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1
            ),
            margin=dict(l=50, r=30, t=60, b=60),
            height=460,
        )

        return fig
    
    def _load_mock_data(self) -> pd.DataFrame:
        """
        Load mock HRV data from CSV or generate if not exists.
        
        Returns:
            DataFrame with columns: id, hrv, stress_score, age
        """
        return load_base_hrv_df()

    def _create_longevity_hrv_stress_views(
        self, data: Dict[str, Any]
    ) -> (go.Figure, List[Dict[str, Any]], List[str]):
        """
        Build the specialized visualisations for the longevity HRV-under-stress dataset.
        """
        trend_records = data.get("hrv_stress_trend", [])
        if not trend_records:
            fallback_fig = self._create_hrv_vs_stress_scatter()
            fallback_recs = [
                "Scatter plot showing HRV vs Stress relationship",
                "Interactive zoom and pan enabled",
                "Hover tooltips show individual data points",
            ]
            return fallback_fig, [], fallback_recs

        df = pd.DataFrame(trend_records)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["stress_bucket"] = df["stress_bucket"].astype(str)

        # Scatter plot with regression line showing overall relationship
        scatter_fig = go.Figure()
        scatter_fig.add_trace(
            go.Scatter(
                x=df["stress_score"],
                y=df["hrv"],
                mode="markers",
                name="Session",
                marker=dict(
                    size=10,
                    color=df["stress_score"],
                    colorscale="RdYlBu_r",
                    showscale=True,
                    colorbar=dict(title="Stress Score"),
                ),
                text=[
                    f"{row.day} • {row.session} • ΔHRV {row.hrv_delta_from_baseline} ms"
                    for row in df.itertuples()
                ],
                hovertemplate="<b>Stress:</b> %{x}<br><b>HRV:</b> %{y}<br>%{text}<extra></extra>",
            )
        )
        if df["stress_score"].nunique() >= 2:
            coeffs = np.polyfit(df["stress_score"], df["hrv"], 1)
            x_range = np.linspace(df["stress_score"].min(), df["stress_score"].max(), 50)
            y_fit = coeffs[0] * x_range + coeffs[1]
            scatter_fig.add_trace(
                go.Scatter(
                    x=x_range,
                    y=y_fit,
                    mode="lines",
                    name="Regression",
                    line=dict(color="#fb7185", width=3),
                    hoverinfo="skip",
                )
            )
        scatter_fig.update_layout(
            title=dict(
                text="HRV decreases as stress load increases",
                x=0.5,
                font=dict(size=20),
            ),
            xaxis=dict(title="Stress Score"),
            yaxis=dict(title="HRV (ms)"),
            template="plotly_white",
        )

        # Box plot comparing HRV distribution across stress buckets
        box_fig = go.Figure()
        for bucket in ["low", "moderate", "high"]:
            bucket_df = df[df["stress_bucket"] == bucket]
            if bucket_df.empty:
                continue
            box_fig.add_trace(
                go.Box(
                    y=bucket_df["hrv"],
                    name=bucket.capitalize(),
                    boxmean="sd",
                    marker_color=(
                        "#4ade80" if bucket == "low" else "#facc15" if bucket == "moderate" else "#f87171"
                    ),
                )
            )
        box_fig.update_layout(
            title=dict(text="HRV distribution by stress bucket", x=0.5),
            yaxis=dict(title="HRV (ms)"),
            template="plotly_white",
        )

        # Trend chart with dual y-axes to show HRV vs stress over time
        trend_fig = go.Figure()
        trend_fig.add_trace(
            go.Scatter(
                x=df["timestamp"],
                y=df["hrv"],
                mode="lines+markers",
                name="HRV",
                line=dict(color="#22d3ee", width=3),
                marker=dict(size=8),
            )
        )
        trend_fig.add_trace(
            go.Scatter(
                x=df["timestamp"],
                y=df["stress_score"],
                mode="lines+markers",
                name="Stress Score",
                line=dict(color="#f97316", width=3, dash="dash"),
                marker=dict(size=8),
                yaxis="y2",
            )
        )
        trend_fig.update_layout(
            title=dict(text="Session trend: stress climbs as HRV wanes", x=0.5),
            xaxis=dict(title="Session timeline"),
            yaxis=dict(title="HRV (ms)"),
            yaxis2=dict(
                title="Stress Score",
                overlaying="y",
                side="right",
                showgrid=False,
            ),
            template="plotly_white",
        )

        alternate_views = [
            {
                "id": "box_hrv_by_stress_bucket",
                "label": "HRV by Stress Bucket",
                "plotly_json": json.loads(box_fig.to_json()),
            },
            {
                "id": "trend_hrv_stress",
                "label": "Session Trend",
                "plotly_json": json.loads(trend_fig.to_json()),
            },
        ]

        recommendations = [
            "Use the regression overlay to explain the inverse HRV–stress trend.",
            "Switch to the stress bucket view to highlight recovery differences across buckets.",
            "Play the session timeline to narrate how sustained stress erodes HRV across the week.",
        ]

        return scatter_fig, alternate_views, recommendations

