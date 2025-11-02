"""
AURORA Backend - FastAPI Application
Main entry point for the backend API server.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import random
from datetime import datetime, timedelta
from typing import List, Optional

from agents.core_agent import AuroraCoreAgent

load_dotenv()

app = FastAPI(
    title="AURORA API",
    description="Backend API for AURORA - AI-powered data analysis platform",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "AURORA Backend API", "status": "running"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# Pydantic models for request/response
class InsightRequest(BaseModel):
    """Request model for insight endpoint"""
    query: str


class HRVDataPoint(BaseModel):
    """HRV data point model"""
    timestamp: str
    rmssd: float  # Root Mean Square of Successive Differences
    sdnn: float   # Standard Deviation of NN intervals
    pnn50: float  # Percentage of NN50 intervals
    frequency_domain_lf: float  # Low frequency power
    frequency_domain_hf: float  # High frequency power


class StressDataPoint(BaseModel):
    """Stress data point model"""
    timestamp: str
    stress_level: float  # 0-100 scale
    heart_rate: float
    respiratory_rate: float
    skin_conductance: float


def generate_mock_hrv_data(days: int = 7) -> List[dict]:
    """Generate mock HRV data for the specified number of days"""
    data = []
    base_time = datetime.now()
    
    for day in range(days):
        for hour in range(0, 24, 2):  # Every 2 hours
            timestamp = base_time - timedelta(days=days - day, hours=24 - hour)
            data.append({
                "timestamp": timestamp.isoformat(),
                "rmssd": round(random.uniform(20.0, 80.0), 2),
                "sdnn": round(random.uniform(30.0, 120.0), 2),
                "pnn50": round(random.uniform(5.0, 40.0), 2),
                "frequency_domain_lf": round(random.uniform(100.0, 1000.0), 2),
                "frequency_domain_hf": round(random.uniform(50.0, 800.0), 2),
            })
    
    return sorted(data, key=lambda x: x["timestamp"])


def generate_mock_stress_data(days: int = 7) -> List[dict]:
    """Generate mock stress data for the specified number of days"""
    data = []
    base_time = datetime.now()
    
    for day in range(days):
        for hour in range(0, 24, 1):  # Every hour
            timestamp = base_time - timedelta(days=days - day, hours=24 - hour)
            data.append({
                "timestamp": timestamp.isoformat(),
                "stress_level": round(random.uniform(10.0, 90.0), 2),
                "heart_rate": round(random.uniform(60.0, 100.0), 2),
                "respiratory_rate": round(random.uniform(12.0, 20.0), 2),
                "skin_conductance": round(random.uniform(2.0, 15.0), 2),
            })
    
    return sorted(data, key=lambda x: x["timestamp"])


@app.get("/api/hrv")
async def get_hrv_data(days: int = 7):
    """
    Get HRV (Heart Rate Variability) physiological data.
    
    Args:
        days: Number of days of data to return (default: 7)
    
    Returns:
        List of HRV data points with timestamps and metrics
    """
    if days < 1 or days > 30:
        raise HTTPException(status_code=400, detail="Days must be between 1 and 30")
    
    data = generate_mock_hrv_data(days)
    return {
        "data": data,
        "count": len(data),
        "metrics": {
            "avg_rmssd": round(sum(d["rmssd"] for d in data) / len(data), 2),
            "avg_sdnn": round(sum(d["sdnn"] for d in data) / len(data), 2),
            "avg_pnn50": round(sum(d["pnn50"] for d in data) / len(data), 2),
        }
    }


@app.get("/api/stress")
async def get_stress_data(days: int = 7):
    """
    Get stress physiological data.
    
    Args:
        days: Number of days of data to return (default: 7)
    
    Returns:
        List of stress data points with timestamps and metrics
    """
    if days < 1 or days > 30:
        raise HTTPException(status_code=400, detail="Days must be between 1 and 30")
    
    data = generate_mock_stress_data(days)
    return {
        "data": data,
        "count": len(data),
        "metrics": {
            "avg_stress_level": round(sum(d["stress_level"] for d in data) / len(data), 2),
            "avg_heart_rate": round(sum(d["heart_rate"] for d in data) / len(data), 2),
            "avg_respiratory_rate": round(sum(d["respiratory_rate"] for d in data) / len(data), 2),
        }
    }


@app.post("/api/insight")
async def get_insight(request: InsightRequest):
    """
    Get AI-generated insight, data analysis, and visualization based on query.
    
    Args:
        request: InsightRequest containing query string
    
    Returns:
        Combined JSON with keys: data, chart, insight
    """
    try:
        # Initialize core agent
        core_agent = AuroraCoreAgent()
        
        # Process query through core agent
        result = core_agent.run(request.query)
        
        # Return the combined JSON (data, chart, insight)
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )


@app.post("/api/debug-flow")
async def debug_flow(request: InsightRequest):
    """
    Debug endpoint to trace agent execution flow.
    Logs each agent's name and output when called by Core Agent.
    
    Args:
        request: InsightRequest containing query string
    
    Returns:
        Array of executed agent names like: 
        ["AuroraDataAnalystAgent executed", "AuroraVizAgent executed", "AuroraNarrativeAgent executed"]
    """
    try:
        # Initialize core agent with debug logging enabled
        core_agent = AuroraCoreAgent(enable_debug_logging=True)
        
        # Clear any previous execution log
        core_agent.clear_execution_log()
        
        # Process query through core agent
        result = core_agent.run(request.query)
        
        # Get execution log
        execution_log = core_agent.get_execution_log()
        
        # Return array of executed agents
        return execution_log
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

