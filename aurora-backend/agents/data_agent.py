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
        # Reload data if needed
        if self.df is None:
            self._load_data()
        
        # Perform analysis based on query
        statistics = self._calculate_statistics()
        hrv_by_stress = self._calculate_hrv_by_stress()
        hrv_by_age_group = self._calculate_hrv_by_age_group()
        correlations = self._calculate_correlations()
        mode = (context or {}).get("mode")
        
        # Generate insights
        insights = self._generate_insights(statistics, hrv_by_stress, correlations)
        
        processed_data = {
            "query": query,
            "timestamp": datetime.now().isoformat(),
            "data_summary": {
                "total_records": len(self.df),
                "columns": list(self.df.columns),
                "shape": self.df.shape,
            },
            "statistics": statistics,
            "hrv_by_stress_level": hrv_by_stress,
            "hrv_by_age_group": hrv_by_age_group,
            "correlations": correlations,
            "insights": insights,
            "status": "processed",
        }

        if mode == "mirror":
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
    
    def _calculate_statistics(self) -> Dict[str, Any]:
        """Calculate basic statistics for HRV data"""
        return {
            "hrv": {
                "count": int(self.df["hrv"].count()),
                "mean": round(float(self.df["hrv"].mean()), 2),
                "std": round(float(self.df["hrv"].std()), 2),
                "min": round(float(self.df["hrv"].min()), 2),
                "max": round(float(self.df["hrv"].max()), 2),
                "median": round(float(self.df["hrv"].median()), 2),
            },
            "stress_score": {
                "count": int(self.df["stress_score"].count()),
                "mean": round(float(self.df["stress_score"].mean()), 2),
                "std": round(float(self.df["stress_score"].std()), 2),
                "min": round(float(self.df["stress_score"].min()), 2),
                "max": round(float(self.df["stress_score"].max()), 2),
                "median": round(float(self.df["stress_score"].median()), 2),
            },
            "age": {
                "count": int(self.df["age"].count()),
                "mean": round(float(self.df["age"].mean()), 2),
                "std": round(float(self.df["age"].std()), 2),
                "min": int(self.df["age"].min()),
                "max": int(self.df["age"].max()),
                "median": round(float(self.df["age"].median()), 2),
            },
        }
    
    def _calculate_hrv_by_stress(self) -> Dict[str, Any]:
        """
        Calculate average HRV grouped by stress level.
        Groups stress scores into categories: Low (<20), Medium (20-35), High (>35)
        """
        # Create stress categories
        def categorize_stress(score):
            if score < 20:
                return "Low"
            elif score <= 35:
                return "Medium"
            else:
                return "High"
        
        self.df["stress_category"] = self.df["stress_score"].apply(categorize_stress)
        
        # Group by stress category and calculate statistics
        grouped = self.df.groupby("stress_category")["hrv"].agg([
            "count", "mean", "std", "min", "max"
        ]).round(2)
        
        # Convert to dictionary format
        result = {}
        for category in grouped.index:
            result[category] = {
                "count": int(grouped.loc[category, "count"]),
                "average_hrv": round(float(grouped.loc[category, "mean"]), 2),
                "std": round(float(grouped.loc[category, "std"]), 2),
                "min": round(float(grouped.loc[category, "min"]), 2),
                "max": round(float(grouped.loc[category, "max"]), 2),
            }
        
        return result
    
    def _calculate_hrv_by_age_group(self) -> Dict[str, Any]:
        """
        Calculate average HRV grouped by age groups.
        Groups ages into: Young (<30), Middle (30-35), Senior (>35)
        """
        # Create age groups
        def categorize_age(age):
            if age < 30:
                return "Young"
            elif age <= 35:
                return "Middle"
            else:
                return "Senior"
        
        self.df["age_group"] = self.df["age"].apply(categorize_age)
        
        # Group by age group and calculate statistics
        grouped = self.df.groupby("age_group")["hrv"].agg([
            "count", "mean", "std"
        ]).round(2)
        
        # Convert to dictionary format
        result = {}
        for group in grouped.index:
            result[group] = {
                "count": int(grouped.loc[group, "count"]),
                "average_hrv": round(float(grouped.loc[group, "mean"]), 2),
                "std": round(float(grouped.loc[group, "std"]), 2),
            }
        
        return result
    
    def _calculate_correlations(self) -> Dict[str, float]:
        """Calculate correlation coefficients between numeric columns"""
        numeric_cols = ["hrv", "stress_score", "age"]
        corr_matrix = self.df[numeric_cols].corr()
        
        correlations = {
            "hrv_vs_stress": round(float(corr_matrix.loc["hrv", "stress_score"]), 3),
            "hrv_vs_age": round(float(corr_matrix.loc["hrv", "age"]), 3),
            "stress_vs_age": round(float(corr_matrix.loc["stress_score", "age"]), 3),
        }
        
        return correlations
    
    def _generate_insights(self, statistics: Dict, hrv_by_stress: Dict, 
                          correlations: Dict) -> List[str]:
        """Generate insights from the analysis"""
        insights = []
        
        # HRV insights
        avg_hrv = statistics["hrv"]["mean"]
        insights.append(f"Average HRV across all records: {avg_hrv}")
        
        # Stress level insights
        if "Low" in hrv_by_stress and "High" in hrv_by_stress:
            low_hrv = hrv_by_stress["Low"]["average_hrv"]
            high_hrv = hrv_by_stress["High"]["average_hrv"]
            insights.append(
                f"Average HRV for Low stress ({low_hrv}) is "
                f"{'higher' if low_hrv > high_hrv else 'lower'} than High stress ({high_hrv})"
            )
        
        # Correlation insights
        hrv_stress_corr = correlations["hrv_vs_stress"]
        if abs(hrv_stress_corr) > 0.3:
            direction = "negative" if hrv_stress_corr < 0 else "positive"
            insights.append(
                f"Strong {direction} correlation ({hrv_stress_corr}) between HRV and stress score"
            )
        
        # Data quality insights
        total_records = statistics["hrv"]["count"]
        insights.append(f"Analysis completed on {total_records} records")
        
        return insights

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

