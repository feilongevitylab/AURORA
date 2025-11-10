"""
AURORA Backend - FastAPI Application
Main entry point for the backend API server.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv
import os
import random
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
import bcrypt
from sqlalchemy.orm import Session

from agents.core_agent import AuroraCoreAgent
from database import Base, engine, get_db
from models import User

load_dotenv()

app = FastAPI(
    title="AURORA API",
    description="Backend API for AURORA - AI-powered data analysis platform",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:3002",
    ],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "AURORA Backend API", "status": "running"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# Pydantic models for request/response
class RegistrationRequest(BaseModel):
    email: EmailStr
    password: str
    nickname: str
    gender: str
    topics: List[str] = []
    other_topic: Optional[str] = None
    wearable_preference: str = "none"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class InsightRequest(BaseModel):
    """Request model for insight endpoint"""
    query: str
    raw_query: Optional[str] = None
    mode: Optional[str] = None  # companion, status, science
    user_id: Optional[str] = None
    is_registered: Optional[bool] = False
    data: Optional[Dict[str, Any]] = None


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


@app.post("/api/register")
async def register_user(request: RegistrationRequest, db: Session = Depends(get_db)):
    """
    Register or update a user profile for personalized insights.
    """
    email_key = request.email.lower().strip()

    normalized_gender = request.gender.lower().strip() if request.gender else "unspecified"
    if normalized_gender not in {"female", "male", "unspecified"}:
        normalized_gender = "unspecified"

    wearable_choice = request.wearable_preference.lower().strip() if request.wearable_preference else "none"
    if wearable_choice not in {"smartwatch", "ouraring", "none"}:
        wearable_choice = "none"

    trimmed_topics = [topic for topic in (request.topics or []) if topic != "other"]
    other_topic = request.other_topic.strip() if request.other_topic else None

    if "other" in (request.topics or []) and not other_topic:
        raise HTTPException(
            status_code=400,
            detail="Please share the additional topic you would like Aurora to focus on."
        )

    hashed_password = bcrypt.hashpw(
        request.password.encode("utf-8"),
        bcrypt.gensalt(),
    ).decode("utf-8")

    user = db.query(User).filter(User.email == email_key).first()

    if user:
        user.password_hash = hashed_password
        user.nickname = request.nickname.strip()
        user.gender = normalized_gender
        user.topics = trimmed_topics
        user.other_topic = other_topic
        user.wearable_preference = wearable_choice
        user.model_tier = "premium"
        user.is_registered = True
        user.updated_at = datetime.utcnow()
        if not user.created_at:
            user.created_at = datetime.utcnow()
    else:
        user = User(
            email=email_key,
            password_hash=hashed_password,
            nickname=request.nickname.strip(),
            gender=normalized_gender,
            topics=trimmed_topics,
            other_topic=other_topic,
            wearable_preference=wearable_choice,
            model_tier="premium",
            is_registered=True,
            last_sign_in_at=datetime.utcnow(),
        )
        db.add(user)

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"user": user.to_dict()}


@app.post("/api/login")
async def login_user(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate a returning user by email (password validation is simulated for prototype).
    """
    email_key = request.email.lower().strip()
    user = db.query(User).filter(User.email == email_key).first()

    if not user or not bcrypt.checkpw(
        request.password.encode("utf-8"),
        user.password_hash.encode("utf-8"),
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password. Please try again or sign up."
        )

    user.last_sign_in_at = datetime.utcnow()
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"user": user.to_dict()}


@app.post("/api/insight")
async def get_insight(request: InsightRequest, db: Session = Depends(get_db)):
    """
    Get AI-generated insight, data analysis, and visualization based on query and mode.
    
    Args:
        request: InsightRequest containing query string and optional mode
    
    Returns:
        Combined JSON with keys: data, chart, insight
    """
    try:
        # Initialize core agent
        core_agent = AuroraCoreAgent()
        
        # Prepare context based on mode and user data
        context: Dict[str, Any] = {
            "user_id": request.user_id,
            "is_registered": request.is_registered,
            "raw_query": (request.raw_query or request.query),
            "original_query": request.query,
            "payload_data": request.data,
        }

        if request.mode:
            context.update({
                "mode": request.mode,
                "tone": "warm" if request.mode == "companion" else "professional" if request.mode == "science" else "analytical",
                "supportive": request.mode == "companion",
                "include_topology": request.mode == "status",
                "include_references": request.mode == "science",
            })

        if request.user_id:
            user_profile = db.query(User).filter(User.id == request.user_id).first()
            if user_profile:
                user_dict = user_profile.to_dict()
                context["user_profile"] = user_dict
                context["is_registered"] = user_dict.get("is_registered", context.get("is_registered", False))
        
        # Process query through core agent with mode context
        result = core_agent.run(request.query, context)
        
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

