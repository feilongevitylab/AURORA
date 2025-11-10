"""
Data Agent - Handles data retrieval, processing, and analysis using pandas.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import pandas as pd
import random
import os


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
        self.mock_companion_df = None
    
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

    def _load_science_mock_data(self) -> pd.DataFrame:
        if self.mock_science_df is not None:
            return self.mock_science_df

        mock_data = {
            "id": list(range(1, 11)),
            "cortisol_morning": [18.5, 19.2, 17.8, 21.1, 16.9, 20.3, 18.7, 22.4, 19.8, 17.2],
            "cortisol_evening": [6.2, 5.9, 7.1, 5.4, 6.8, 5.7, 6.1, 5.2, 5.6, 6.4],
            "reaction_time_ms": [245, 232, 258, 225, 268, 238, 241, 222, 235, 252],
            "focus_index": [78, 82, 75, 88, 70, 85, 80, 90, 82, 76],
            "sleep_duration": [7.2, 7.5, 6.8, 7.9, 6.5, 7.3, 7.1, 8.1, 7.4, 6.9],
        }

        df = pd.DataFrame(mock_data)

        df["cortisol_ratio"] = (df["cortisol_morning"] / df["cortisol_evening"]).round(2)
        df["focus_per_sleep"] = (df["focus_index"] / df["sleep_duration"]).round(2)

        self.mock_science_df = df
        return df

    def _load_companion_mock_data(self) -> pd.DataFrame:
        if self.mock_companion_df is not None:
            return self.mock_companion_df

        mock_data = {
            "id": list(range(1, 11)),
            "sleep_hours": [6.2, 7.4, 5.8, 7.9, 6.5, 7.1, 8.0, 6.8, 7.6, 6.3],
            "sleep_quality": [62, 78, 55, 82, 68, 75, 88, 70, 81, 60],
            "breath_rate": [17, 15, 18, 14, 16, 15, 13, 16, 14, 18],
            "anxiety_score": [62, 48, 70, 45, 58, 52, 40, 55, 49, 68],
            "relaxation_minutes": [12, 26, 8, 32, 18, 24, 36, 20, 28, 10],
        }

        df = pd.DataFrame(mock_data)

        df["sleep_efficiency"] = ((df["sleep_quality"] / df["sleep_hours"]).clip(0, 100)).round(1)
        df["relaxation_index"] = ((df["relaxation_minutes"] / (df["anxiety_score"] + 1)) * 100).round(1)

        self.mock_companion_df = df
        return df
    
    def _generate_mock_hrv_data(self) -> pd.DataFrame:
        """
        Generate mock HRV data with hardcoded sample for testing.
        
        Returns:
            DataFrame with columns: id, hrv, stress_score, age
        """
        # Hardcoded sample data for mock testing
        mock_data = {
            "id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
            "hrv": [45.2, 52.8, 38.5, 61.3, 49.7, 55.1, 42.9, 58.6, 48.3, 
                   53.7, 40.1, 56.4, 47.2, 59.8, 44.6],
            "stress_score": [25, 15, 45, 10, 30, 20, 50, 12, 35, 18, 55, 
                            22, 28, 8, 40],
            "age": [28, 32, 25, 35, 30, 27, 22, 38, 29, 33, 26, 31, 34, 40, 24]
        }
        
        df = pd.DataFrame(mock_data)
        
        # Optionally save to CSV for future reference
        if not os.path.exists("mock_hrv_data.csv"):
            df.to_csv("mock_hrv_data.csv", index=False)
        
        return df
    
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
        if mode == "science" and any(keyword in query_lower for keyword in ["cortisol", "focus", "glucose", "neuro", "luteal", "hormone", "cognitive"]):
            df = self._load_science_mock_data()
            dataset_label = "science_cortisol_focus"
        elif mode == "companion" and any(keyword in query_lower for keyword in ["sleep", "relax", "anxiety", "stress management", "breathing", "mindful"]):
            df = self._load_companion_mock_data()
            dataset_label = "companion_sleep_relaxation"
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

        if mode == "mirror" and dataset_label == "hrv":
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
        
        return {
            "agent": self.name,
            "result": processed_data,
            "success": True,
        }
    
    def _calculate_statistics(self, df: pd.DataFrame, dataset_label: str) -> Dict[str, Any]:
        if dataset_label == "science_cortisol_focus":
            return {
                "cortisol_morning": self._describe_series(df["cortisol_morning"]),
                "cortisol_evening": self._describe_series(df["cortisol_evening"]),
                "cortisol_ratio": self._describe_series(df["cortisol_ratio"]),
                "focus_index": self._describe_series(df["focus_index"]),
                "reaction_time_ms": self._describe_series(df["reaction_time_ms"]),
                "sleep_duration": self._describe_series(df["sleep_duration"]),
            }
        if dataset_label == "companion_sleep_relaxation":
            return {
                "sleep_hours": self._describe_series(df["sleep_hours"]),
                "sleep_quality": self._describe_series(df["sleep_quality"]),
                "sleep_efficiency": self._describe_series(df["sleep_efficiency"]),
                "anxiety_score": self._describe_series(df["anxiety_score"]),
                "relaxation_minutes": self._describe_series(df["relaxation_minutes"]),
                "relaxation_index": self._describe_series(df["relaxation_index"]),
            }
        # default HRV dataset
        return {
            "hrv": self._describe_series(df["hrv"]),
            "stress_score": self._describe_series(df["stress_score"]),
            "age": self._describe_series(df["age"]),
        }
 
    def _calculate_groupings(self, df: pd.DataFrame, dataset_label: str) -> Dict[str, Any]:
        if dataset_label == "science_cortisol_focus":
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

        if dataset_label == "companion_sleep_relaxation":
            sleep_bins = pd.cut(df["sleep_hours"], bins=[0, 6, 7.5, 10], labels=["Low", "Adequate", "Restorative"], include_lowest=True)
            grouped = df.groupby(sleep_bins).agg({
                "sleep_quality": "mean",
                "sleep_efficiency": "mean",
                "anxiety_score": "mean",
                "relaxation_minutes": "mean"
            }).round(1)

            return {
                "sleep_buckets": grouped.to_dict(orient="index"),
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
        if dataset_label == "science_cortisol_focus":
            numeric_cols = ["cortisol_morning", "cortisol_evening", "cortisol_ratio", "focus_index", "reaction_time_ms", "sleep_duration"]
        elif dataset_label == "companion_sleep_relaxation":
            numeric_cols = ["sleep_hours", "sleep_quality", "sleep_efficiency", "anxiety_score", "relaxation_minutes", "relaxation_index"]
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

        if dataset_label == "science_cortisol_focus":
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

        if dataset_label == "companion_sleep_relaxation":
            sleep_hours = statistics["sleep_hours"]["mean"]
            efficiency = statistics["sleep_efficiency"]["mean"]
            relaxation = statistics["relaxation_minutes"]["mean"]
            insights.append(f"Average sleep duration {sleep_hours} hours with efficiency {efficiency}%.")
            insights.append(f"Typical relaxation practice totals {relaxation} minutes daily alongside anxiety score {statistics['anxiety_score']['mean']}.")
            if "sleep_buckets" in grouped_summary:
                restorative = grouped_summary["sleep_buckets"].get("Restorative", {})
                if restorative:
                    insights.append(
                        f"Restorative sleep aligns with quality {restorative.get('sleep_quality', 'N/A')} and anxiety {restorative.get('anxiety_score', 'N/A')} levels."
                    )
            for pair, value in correlations.items():
                if abs(value) >= 0.35:
                    insights.append(f"Observing correlation {pair}: {value}.")
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

