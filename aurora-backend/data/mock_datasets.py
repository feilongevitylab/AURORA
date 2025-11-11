"""
Centralized mock datasets used by the Aurora backend during development.

By storing the raw mock values here we keep `DataAgent` lean and make it
easier to iterate on the underlying numbers or swap them for real data in
the future.
"""

from __future__ import annotations

from typing import Dict

import pandas as pd


_BASE_HRV_DATA: Dict[str, list] = {
    "id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    "hrv": [
        45.2,
        52.8,
        38.5,
        61.3,
        49.7,
        55.1,
        42.9,
        58.6,
        48.3,
        53.7,
        40.1,
        56.4,
        47.2,
        59.8,
        44.6,
    ],
    "stress_score": [
        25,
        15,
        45,
        10,
        30,
        20,
        50,
        12,
        35,
        18,
        55,
        22,
        28,
        8,
        40,
    ],
    "age": [28, 32, 25, 35, 30, 27, 22, 38, 29, 33, 26, 31, 34, 40, 24],
}

_SCIENCE_CORTISOL_FOCUS_DATA: Dict[str, list] = {
    "id": list(range(1, 11)),
    "cortisol_morning": [18.5, 19.2, 17.8, 21.1, 16.9, 20.3, 18.7, 22.4, 19.8, 17.2],
    "cortisol_evening": [6.2, 5.9, 7.1, 5.4, 6.8, 5.7, 6.1, 5.2, 5.6, 6.4],
    "reaction_time_ms": [245, 232, 258, 225, 268, 238, 241, 222, 235, 252],
    "focus_index": [78, 82, 75, 88, 70, 85, 80, 90, 82, 76],
    "sleep_duration": [7.2, 7.5, 6.8, 7.9, 6.5, 7.3, 7.1, 8.1, 7.4, 6.9],
}

_SCIENCE_HRV_STRESS_DATA: Dict[str, list] = {
    "day": [
        "Mon",
        "Mon",
        "Tue",
        "Tue",
        "Wed",
        "Wed",
        "Thu",
        "Thu",
        "Fri",
        "Fri",
        "Sat",
        "Sat",
        "Sun",
        "Sun",
    ],
    "timestamp": [
        "2024-07-01T08:00:00",
        "2024-07-01T20:00:00",
        "2024-07-02T08:00:00",
        "2024-07-02T20:00:00",
        "2024-07-03T08:00:00",
        "2024-07-03T20:00:00",
        "2024-07-04T08:00:00",
        "2024-07-04T20:00:00",
        "2024-07-05T08:00:00",
        "2024-07-05T20:00:00",
        "2024-07-06T08:00:00",
        "2024-07-06T20:00:00",
        "2024-07-07T08:00:00",
        "2024-07-07T20:00:00",
    ],
    "session": [
        "Morning",
        "Evening",
        "Morning",
        "Evening",
        "Morning",
        "Evening",
        "Morning",
        "Evening",
        "Morning",
        "Evening",
        "Morning",
        "Evening",
        "Morning",
        "Evening",
    ],
    "hrv": [65, 62, 64, 60, 61, 57, 59, 54, 56, 51, 54, 49, 55, 50],
    "stress_score": [20, 24, 22, 28, 26, 33, 30, 37, 34, 40, 36, 42, 35, 39],
    "perceived_stress": [18, 22, 20, 26, 24, 30, 28, 34, 32, 38, 33, 40, 31, 37],
    "breathing_rate": [12, 13, 12, 14, 13, 15, 14, 16, 15, 17, 15, 18, 14, 17],
    "sleep_quality": [82, 78, 80, 76, 78, 73, 75, 70, 74, 68, 73, 66, 74, 67],
}


def load_base_hrv_df() -> pd.DataFrame:
    """Return the base HRV dataset used for default analysis."""
    return pd.DataFrame(_BASE_HRV_DATA).copy()


def load_longevity_cortisol_focus_df() -> pd.DataFrame:
    """Return the longevity-mode dataset exploring cortisol and focus."""
    df = pd.DataFrame(_SCIENCE_CORTISOL_FOCUS_DATA)
    df = df.copy()
    df["cortisol_ratio"] = (df["cortisol_morning"] / df["cortisol_evening"]).round(2)
    df["focus_per_sleep"] = (df["focus_index"] / df["sleep_duration"]).round(2)
    return df


def load_longevity_hrv_stress_df() -> pd.DataFrame:
    """Return a longevity-mode dataset that highlights HRV changes under stress."""
    df = pd.DataFrame(_SCIENCE_HRV_STRESS_DATA).copy()
    baseline = df.loc[0, "hrv"]
    df["hrv_delta_from_baseline"] = (df["hrv"] - baseline).round(2)
    df["day_index"] = list(range(1, len(df) + 1))
    df["stress_bucket"] = pd.cut(
        df["stress_score"],
        bins=[0, 25, 35, 100],
        labels=["low", "moderate", "high"],
        include_lowest=True,
        right=False,
    )
    df["hrv_variability"] = (
        df["hrv"].rolling(window=3, min_periods=1).std().fillna(0).round(2)
    )
    return df



