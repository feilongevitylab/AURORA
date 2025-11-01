"""
Data Agent - Handles data retrieval, processing, and analysis using pandas.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
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

