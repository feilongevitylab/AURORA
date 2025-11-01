"""
Formatting utilities for AURORA
"""

from datetime import datetime
from typing import Optional


def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format datetime to string"""
    return dt.strftime(format_str)


def format_number(number: float, decimals: int = 2) -> str:
    """Format number with specified decimal places"""
    return f"{number:,.{decimals}f}"

