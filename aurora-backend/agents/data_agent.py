"""
Data Agent - Handles data retrieval, processing, and analysis using pandas.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import pandas as pd
import random
import os

from data.mock_datasets import (
    load_base_hrv_df,
    load_science_cortisol_focus_df,
    load_science_hrv_stress_df,
)

class DataAgent:
    """
    Agent responsible for data operations including:
    - Data retrieval from CSV files
    - Data processing and transformation using pandas
    - Statistical analysis
    - Data validation
    """
    
    def __init__(self, data_file: Optional[str] = None):
        """
        Initialize the Data Agent.
        
        Args:
            data_file: Optional path to CSV file. If None, uses mock data.
        """
        self.name = "DataAgent"
        self.data_file = data_file
        self.df = None
        self._load_data()
        self.mock_science_df = None
        self.mock_hrv_stress_df = None
    
    def _load_data(self) -> pd.DataFrame:
        """
        Load HRV data from CSV file or generate mock data.
        
        Returns:
            DataFrame with columns: id, hrv, stress_score, age
        """
        if self.data_file and os.path.exists(self.data_file):
            # Load from file if it exists
            self.df = pd.read_csv(self.data_file)
        else:
            # Generate mock data
            self.df = self._generate_mock_hrv_data()
        
        return self.df

    def _load_longevity_mock_data(self) -> pd.DataFrame:
        if self.mock_longevity_df is not None:
            return self.mock_longevity_df

        self.mock_longevity_df = load_longevity_cortisol_focus_df()
        return self.mock_longevity_df.copy()

    def _load_hrv_stress_mock_data(self) -> pd.DataFrame:
        if self.mock_hrv_stress_df is not None:
            return self.mock_hrv_stress_df.copy()
        self.mock_hrv_stress_df = load_longevity_hrv_stress_df()
        return self.mock_hrv_stress_df.copy()
    
    def _generate_mock_hrv_data(self) -> pd.DataFrame:
        """
        Generate mock HRV data with hardcoded sample for testing.
        
        Returns:
            DataFrame with columns: id, hrv, stress_score, age
        """
        # Hardcoded sample data for mock testing
        return load_base_hrv_df()
    
    def run(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute data analysis using pandas based on the query.
        
        Args:
            query: Natural language query or data request
            context: Optional context containing data or parameters
        
        Returns:
            Dictionary containing processed data and analysis results
        """
        context = context or {}
        mode = context.get("mode")
        query_lower = query.lower()

        dataset_label = "hrv"
        if mode == "longevity":
            cortisol_keywords = ["cortisol", "focus", "glucose", "neuro", "luteal", "hormone", "cognitive"]
            if any(keyword in query_lower for keyword in cortisol_keywords):
                df = self._load_longevity_mock_data()
                dataset_label = "longevity_cortisol_focus"
            elif ("hrv" in query_lower or "heart rate variability" in query_lower) and "stress" in query_lower:
                df = self._load_hrv_stress_mock_data()
                dataset_label = "longevity_hrv_stress"
            else:
                df = self._load_longevity_mock_data()
                dataset_label = "longevity_cortisol_focus"
        else:
            if self.df is None:
                self._load_data()
            df = self.df

        # Perform analysis based on chosen dataset
        statistics = self._calculate_statistics(df, dataset_label)
        grouped_summary = self._calculate_groupings(df, dataset_label)
        correlations = self._calculate_correlations(df, dataset_label)
        
        # Generate insights
        insights = self._generate_insights(statistics, grouped_summary, correlations, dataset_label)
        
        processed_data = {
            "query": query,
            "timestamp": datetime.now().isoformat(),
            "data_summary": {
                "total_records": len(df),
                "columns": list(df.columns),
                "shape": df.shape,
                "dataset": dataset_label,
            },
            "statistics": statistics,
            **grouped_summary,
            "correlations": correlations,
            "insights": insights,
            "status": "processed",
        }

        if mode == "energy" and dataset_label == "hrv":
            mirror_layers = self._generate_mirror_layers(statistics)
            mirror_trend = self._generate_mirror_trend()
            mirror_summary = self._generate_mirror_summary(statistics, correlations)
            coordination_score = self._estimate_coordination_score(statistics, correlations)
            energy_pattern = self._generate_energy_pattern(statistics, correlations, mirror_trend)
            hero_meta = self._generate_mirror_hero(mirror_summary, coordination_score)

            processed_data.update({
                "coordination_score": coordination_score,
                "insight_summary": mirror_summary,
                "mirror_layers": mirror_layers,
                "mirror_trend": mirror_trend,
                "energy_pattern": energy_pattern,
                "hero": hero_meta,
            })

        processed_data["metadata"] = self._build_dataset_metadata(
            dataset_label=dataset_label,
            statistics=statistics,
            grouped_summary=grouped_summary,
            correlations=correlations,
        )
        
        return {
            "agent": self.name,
            "result": processed_data,
            "success": True,
        }
    
    def _calculate_statistics(self, df: pd.DataFrame, dataset_label: str) -> Dict[str, Any]:
        if dataset_label == "longevity_cortisol_focus":
            return {
                "cortisol_morning": self._describe_series(df["cortisol_morning"]),
                "cortisol_evening": self._describe_series(df["cortisol_evening"]),
                "cortisol_ratio": self._describe_series(df["cortisol_ratio"]),
                "focus_index": self._describe_series(df["focus_index"]),
                "reaction_time_ms": self._describe_series(df["reaction_time_ms"]),
                "sleep_duration": self._describe_series(df["sleep_duration"]),
            }
        if dataset_label == "longevity_hrv_stress":
            return {
                "hrv": self._describe_series(df["hrv"]),
                "stress_score": self._describe_series(df["stress_score"]),
                "perceived_stress": self._describe_series(df["perceived_stress"]),
                "breathing_rate": self._describe_series(df["breathing_rate"]),
                "sleep_quality": self._describe_series(df["sleep_quality"]),
                "hrv_delta_from_baseline": self._describe_series(df["hrv_delta_from_baseline"]),
            }
        # default HRV dataset
        return {
            "hrv": self._describe_series(df["hrv"]),
            "stress_score": self._describe_series(df["stress_score"]),
            "age": self._describe_series(df["age"]),
        }
 
    def _calculate_groupings(self, df: pd.DataFrame, dataset_label: str) -> Dict[str, Any]:
        if dataset_label == "longevity_cortisol_focus":
            focus_bins = pd.cut(df["focus_index"], bins=[0, 70, 80, 100], labels=["Underloaded", "Optimal", "Peak"], include_lowest=True)
            grouped = df.groupby(focus_bins).agg({
                "cortisol_morning": "mean",
                "cortisol_evening": "mean",
                "cortisol_ratio": "mean",
                "reaction_time_ms": "mean"
            }).round(2)

            return {
                "focus_buckets": grouped.to_dict(orient="index"),
            }
        if dataset_label == "longevity_hrv_stress":
            stress_bucket_summary = (
                df.groupby("stress_bucket")
                .agg(
                    avg_hrv=("hrv", "mean"),
                    avg_stress=("stress_score", "mean"),
                    avg_hrv_delta=("hrv_delta_from_baseline", "mean"),
                    sessions=("hrv", "count"),
                )
                .round(2)
            )
            session_summary = (
                df.groupby("session")
                .agg(
                    avg_hrv=("hrv", "mean"),
                    avg_stress=("stress_score", "mean"),
                    avg_variability=("hrv_variability", "mean"),
                )
                .round(2)
            )
            day_summary = (
                df.groupby("day")
                .agg(
                    avg_hrv=("hrv", "mean"),
                    avg_stress=("stress_score", "mean"),
                    avg_delta=("hrv_delta_from_baseline", "mean"),
                )
                .round(2)
                .reset_index()
                .to_dict(orient="records")
            )
            trend_records = df[
                [
                    "timestamp",
                    "day",
                    "session",
                    "hrv",
                    "stress_score",
                    "perceived_stress",
                    "hrv_delta_from_baseline",
                    "hrv_variability",
                    "stress_bucket",
                ]
            ].to_dict(orient="records")

            return {
                "stress_bucket_summary": stress_bucket_summary.to_dict(orient="index"),
                "session_summary": session_summary.to_dict(orient="index"),
                "hrv_stress_trend": trend_records,
                "day_summary": day_summary,
            }

        # default HRV grouping
        def categorize_stress(score):
            if score < 20:
                return "Low"
            if score <= 35:
                return "Medium"
            return "High"

        df_copy = df.copy()
        df_copy["stress_category"] = df_copy["stress_score"].apply(categorize_stress)
        stress_grouped = df_copy.groupby("stress_category")["hrv"].agg([
            "count", "mean", "std", "min", "max"
        ]).round(2)

        def categorize_age(age):
            if age < 30:
                return "Young"
            if age <= 35:
                return "Middle"
            return "Senior"

        df_copy["age_group"] = df_copy["age"].apply(categorize_age)
        age_grouped = df_copy.groupby("age_group")["hrv"].agg([
            "count", "mean", "std"
        ]).round(2)

        return {
            "hrv_by_stress_level": stress_grouped.to_dict(orient="index"),
            "hrv_by_age_group": age_grouped.to_dict(orient="index"),
        }

    def _calculate_correlations(self, df: pd.DataFrame, dataset_label: str) -> Dict[str, float]:
        if dataset_label == "longevity_cortisol_focus":
            numeric_cols = ["cortisol_morning", "cortisol_evening", "cortisol_ratio", "focus_index", "reaction_time_ms", "sleep_duration"]
        elif dataset_label == "longevity_hrv_stress":
            numeric_cols = [
                "hrv",
                "stress_score",
                "perceived_stress",
                "breathing_rate",
                "sleep_quality",
                "hrv_delta_from_baseline",
            ]
        else:
            numeric_cols = ["hrv", "stress_score", "age"]

        corr_matrix = df[numeric_cols].corr()
        correlations = {}
        for i, col_i in enumerate(numeric_cols):
            for col_j in numeric_cols[i + 1:]:
                correlations[f"{col_i}_vs_{col_j}"] = round(float(corr_matrix.loc[col_i, col_j]), 3)

        return correlations

    def _generate_insights(self, statistics: Dict, grouped_summary: Dict, correlations: Dict, dataset_label: str) -> List[str]:
        insights = []

        if dataset_label == "longevity_cortisol_focus":
            morning = statistics["cortisol_morning"]["mean"]
            evening = statistics["cortisol_evening"]["mean"]
            ratio = statistics["cortisol_ratio"]["mean"]
            focus = statistics["focus_index"]["mean"]
            reaction = statistics["reaction_time_ms"]["mean"]
            insights.append(f"Average morning cortisol {morning} µg/dL with ratio {ratio}; evening baseline {evening} µg/dL.")
            insights.append(f"Focus index averages {focus} while reaction time sits near {reaction} ms, suggesting cognitive load trends.")
            if "focus_buckets" in grouped_summary:
                optimal = grouped_summary["focus_buckets"].get("Optimal", {})
                if optimal:
                    insights.append(
                        f"When focus is optimal, cortisol ratio averages {optimal.get('cortisol_ratio', 'N/A')} and reaction time {optimal.get('reaction_time_ms', 'N/A')} ms."
                    )
            for pair, value in correlations.items():
                if abs(value) >= 0.35:
                    insights.append(f"Notable correlation {pair}: {value}.")
            return insights

        if dataset_label == "longevity_hrv_stress":
            corr_value = correlations.get("hrv_vs_stress_score")
            if corr_value is not None:
                insights.append(
                    f"HRV and stress levels move in opposite directions (r={corr_value}), indicating autonomic load increases as stress climbs."
                )
            buckets = grouped_summary.get("stress_bucket_summary", {})
            low_bucket = buckets.get("low") or {}
            high_bucket = buckets.get("high") or {}
            if low_bucket and high_bucket:
                insights.append(
                    f"Low-stress sessions average HRV {low_bucket.get('avg_hrv')} ms vs {high_bucket.get('avg_hrv')} ms in high-stress periods."
                )
                insights.append(
                    f"HRV drops about {abs(high_bucket.get('avg_hrv_delta', 0))} ms below baseline under high stress, compared with {abs(low_bucket.get('avg_hrv_delta', 0))} ms when stress stays low."
                )
            session_summary = grouped_summary.get("session_summary", {})
            evening = session_summary.get("Evening") or {}
            morning = session_summary.get("Morning") or {}
            if evening and morning:
                insights.append(
                    f"Evenings show higher perceived stress ({evening.get('avg_stress')}) and lower HRV ({evening.get('avg_hrv')}) than mornings ({morning.get('avg_stress')} stress, {morning.get('avg_hrv')} HRV)."
                )
            return insights

        # default HRV insights
        avg_hrv = statistics["hrv"]["mean"]
        insights.append(f"Average HRV across all records: {avg_hrv}")
        stress_summary = grouped_summary.get("hrv_by_stress_level", {})
        if "Low" in stress_summary and "High" in stress_summary:
            low_hrv = stress_summary["Low"].get("mean") or stress_summary["Low"].get("average_hrv")
            high_hrv = stress_summary["High"].get("mean") or stress_summary["High"].get("average_hrv")
            insights.append(
                f"Average HRV for Low stress ({low_hrv}) is {'higher' if low_hrv and high_hrv and low_hrv > high_hrv else 'lower'} than High stress ({high_hrv})."
            )
        for pair, value in correlations.items():
            if "hrv" in pair and abs(value) > 0.3:
                direction = "negative" if value < 0 else "positive"
                insights.append(f"{pair.replace('_vs_', ' vs ')} shows a {direction} correlation of {value}.")
        total_records = statistics["hrv"]["count"]
        insights.append(f"Analysis completed on {total_records} records.")
        return insights

    @staticmethod
    def _describe_series(series: pd.Series) -> Dict[str, Any]:
        return {
            "count": int(series.count()),
            "mean": round(float(series.mean()), 2),
            "std": round(float(series.std()), 2),
            "min": round(float(series.min()), 2),
            "max": round(float(series.max()), 2),
            "median": round(float(series.median()), 2),
        }

    def _build_dataset_metadata(
        self,
        dataset_label: str,
        statistics: Dict[str, Any],
        grouped_summary: Dict[str, Any],
        correlations: Dict[str, float],
    ) -> Dict[str, Any]:
        if dataset_label == "longevity_hrv_stress":
        if dataset_label == "longevity_hrv_stress":
            corr_value = correlations.get("hrv_vs_stress_score")
            stress_views = [
                {
                    "id": "scatter_hrv_vs_stress",
                    "label": "HRV vs Stress Scatter",
                    "type": "scatter",
                    "bindings": {"x": "stress_score", "y": "hrv"},
                    "description": "Shows the inverse trend between stress load and HRV readings.",
                },
                {
                    "id": "box_hrv_by_stress_bucket",
                    "label": "HRV by Stress Bucket",
                    "type": "boxplot",
                    "bindings": {"group": "stress_bucket", "value": "hrv"},
                    "description": "Compares HRV distribution across low, moderate, and high stress buckets.",
                },
                {
                    "id": "trend_hrv_stress",
                    "label": "Day & Session Trend",
                    "type": "line",
                    "bindings": {"x": "timestamp", "y": "hrv", "color": "session"},
                    "description": "Tracks how HRV changes session-by-session as stress accumulates.",
                },
            ]
            metrics = {
                "average_hrv": statistics["hrv"]["mean"],
                "average_stress": statistics["stress_score"]["mean"],
                "hrv_stress_correlation": corr_value,
                "avg_hrv_delta": statistics["hrv_delta_from_baseline"]["mean"],
            }
            return {
                "dataset": dataset_label,
                "default_view": "scatter_hrv_vs_stress",
                "available_views": stress_views,
                "metrics": metrics,
            }

        # Generic metadata for other datasets
        sample_metric = next(iter(statistics.values())) if statistics else {}
        generic_metrics = {
            "average": sample_metric.get("mean") if isinstance(sample_metric, dict) else None,
            "total_records": sample_metric.get("count") if isinstance(sample_metric, dict) else None,
        }
        return {
            "dataset": dataset_label,
            "default_view": "summary",
            "available_views": [
                {
                    "id": "summary",
                    "label": "Summary",
                    "type": "summary",
                    "description": "High-level statistical overview.",
                }
            ],
            "metrics": generic_metrics,
        }

    def _generate_mirror_layers(self, statistics: Dict[str, Any]) -> Dict[str, Any]:
        avg_hrv = statistics["hrv"]["mean"]
        stress_mean = statistics["stress_score"]["mean"]

        sleep_quality = round(78 + random.uniform(-6, 6), 1)
        heart_coherence = round(70 + (50 - abs(stress_mean - 30)) / 2 + random.uniform(-5, 5), 1)
        stress_index = round(stress_mean * 2 + random.uniform(-5, 5), 1)
        mood_balance = round(80 - (stress_mean - 25) * 1.2 + random.uniform(-5, 5), 1)
        purpose = round(75 + random.uniform(-8, 8), 1)
        fulfillment = round(72 + random.uniform(-7, 7), 1)

        return {
            "physiology": {
                "title": "Physiology",
                "description": "HRV · Sleep Quality · Heart Coherence",
                "metrics": [
                    {"label": "HRV", "value": f"{avg_hrv:.1f}"},
                    {"label": "Sleep Quality", "value": f"{sleep_quality:.1f}"},
                    {"label": "Heart Coherence", "value": f"{heart_coherence:.1f}"},
                ],
            },
            "mind": {
                "title": "Mind",
                "description": "Stress Index · Mood Balance",
                "metrics": [
                    {"label": "Stress Index", "value": f"{stress_index:.1f}"},
                    {"label": "Mood Balance", "value": f"{mood_balance:.1f}"},
                ],
            },
            "meaning": {
                "title": "Meaning",
                "description": "Purpose · Fulfillment",
                "metrics": [
                    {"label": "Purpose", "value": f"{purpose:.1f}"},
                    {"label": "Fulfillment", "value": f"{fulfillment:.1f}"},
                ],
            },
        }

    def _generate_mirror_trend(self) -> list:
        base_date = datetime.now()
        trend = []
        baseline_hrv = 52 + random.uniform(-3, 3)
        focus_level = 65 + random.uniform(-5, 5)

        for offset in range(7):
            day = base_date - timedelta(days=6 - offset)
            hrv_value = baseline_hrv + random.uniform(-4, 4)
            stress_value = 60 - hrv_value * 0.5 + random.uniform(-4, 4)
            focus_value = focus_level + (offset - 3) * 1.2 + random.uniform(-3, 3)

            trend.append({
                "date": day.strftime("%m-%d"),
                "hrv": round(hrv_value, 1),
                "stress": round(max(20, min(95, stress_value)), 1),
                "focus": round(max(20, min(95, focus_value)), 1),
            })

        return trend

    def _estimate_coordination_score(self, statistics: Dict[str, Any], correlations: Dict[str, float]) -> int:
        hrv_mean = statistics["hrv"]["mean"]
        stress_mean = statistics["stress_score"]["mean"]
        correlation = correlations.get("hrv_vs_stress", 0)

        base = 75 + (hrv_mean - 50) * 0.4
        stress_adjustment = -(stress_mean - 25) * 0.3
        corr_adjustment = correlation * -20
        score = round(max(40, min(95, base + stress_adjustment + corr_adjustment)))
        return score

    def _generate_mirror_summary(self, statistics: Dict[str, Any], correlations: Dict[str, float]) -> str:
        correlation = correlations.get("hrv_vs_stress", 0)
        avg_hrv = statistics["hrv"]["mean"]

        if correlation < -0.4:
            return "Your sense of purpose moves in step with your recovery cycle, suggesting meaning is driving your nervous balance."
        if avg_hrv > 55:
            return "Your autonomic rhythm remains adaptable and your focus is aligning with recovery power."
        return "You are staying focused, though recovery velocity is slightly below average."

    def _generate_energy_pattern(self, statistics: Dict[str, Any], correlations: Dict[str, float], trend: list) -> str:
        hrv_trend = [point["hrv"] for point in trend]
        stress_trend = [point["stress"] for point in trend]

        if hrv_trend[-1] < hrv_trend[0] and stress_trend[-1] > stress_trend[0]:
            return "Over the past three days your HRV has dipped while focus climbed - your body is working to keep pace with your willpower."
        if hrv_trend[-1] > hrv_trend[0]:
            return "Your physiological rhythm is becoming more stable, with deeper breath and expansion in your resting state. Keep honoring this cadence."
        return "Your physiological and psychological tempos are searching for a new balance - leave room for integration and recovery."

    def _generate_mirror_hero(self, summary: str, coordination_score: int) -> Dict[str, Any]:
        now = datetime.now()
        hour = now.hour

        if hour < 12:
            greeting_prefix = "Good morning"
        elif hour < 18:
            greeting_prefix = "Good afternoon"
        else:
            greeting_prefix = "Good evening"

        greeting = f"{greeting_prefix}, your rhythm is quietly aligning. Coordination score {coordination_score}% - ready to explore today's mirror?"

        return {
            "greeting": greeting,
            "quick_prompts": [
                "I'm feeling a little tired today.",
                "I'm doing alright today.",
                "Show me today's mirror.",
            ],
            "top_dialog": f"{greeting_prefix}, traveler. Your system is waking with a gentle cadence - let's listen to the whispers of body and mind.",
            "mirror_summary": summary,
        }

