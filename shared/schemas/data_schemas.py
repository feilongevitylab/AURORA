"""
Data schemas for API communication between frontend and backend.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class DataRequest(BaseModel):
    """Request schema for data operations"""
    query: str = Field(..., description="Natural language query or data request")
    dataset: Optional[str] = Field(None, description="Dataset identifier")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")


class DataResponse(BaseModel):
    """Response schema for data operations"""
    result: Any = Field(..., description="Result data")
    visualization: Optional[Dict[str, Any]] = Field(None, description="Visualization configuration")
    explanation: Optional[str] = Field(None, description="Explanation of the result")
    timestamp: datetime = Field(default_factory=datetime.now)


class AnalysisRequest(BaseModel):
    """Request schema for AI analysis operations"""
    prompt: str = Field(..., description="Analysis prompt for LangChain")
    data: Optional[Dict[str, Any]] = Field(None, description="Data to analyze")
    options: Optional[Dict[str, Any]] = Field(None, description="Analysis options")


class AnalysisResponse(BaseModel):
    """Response schema for AI analysis operations"""
    analysis: str = Field(..., description="Analysis result from LangChain")
    insights: Optional[List[str]] = Field(None, description="Key insights")
    confidence: Optional[float] = Field(None, description="Confidence score")
    timestamp: datetime = Field(default_factory=datetime.now)

