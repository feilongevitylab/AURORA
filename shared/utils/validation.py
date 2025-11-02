"""
Validation utilities for AURORA
"""

import re
from typing import Optional


def validate_query(query: str) -> bool:
    """Validate user query input"""
    if not query or not isinstance(query, str):
        return False
    if len(query.strip()) == 0:
        return False
    if len(query) > 10000:  # Reasonable limit
        return False
    return True


def sanitize_input(input_str: str) -> str:
    """Sanitize user input to prevent injection attacks"""
    if not input_str:
        return ""
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>"\']', '', input_str)
    return sanitized.strip()

