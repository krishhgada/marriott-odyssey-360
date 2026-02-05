"""
Marriott's Odyssey 360 AI - Main Backend Application
The world's first fully intelligent hospitality operating system
"""

from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security import HTTPBearer
from starlette.middleware.base import BaseHTTPMiddleware
import uvicorn
import os
import time
from contextlib import asynccontextmanager

from api import auth_simple as auth, concierge, emotion, hotel, wellness, local_discovery
from core.config import settings
from core.database import init_db
from core.security import get_current_user
from models.user import User

# Import new shared modules
from shared.telemetry import telemetry, get_metrics
from shared.config import flags

# Import new routers
from routers import privacy, culture, trustlens, intermodal, agentops, insights, analytics, hotel_iot, offers

# Global state management
app_state = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    # Startup
    print("🚀 Starting Marriott's Odyssey 360 AI...")
    await init_db()
    app_state["demo_mode"] = os.getenv("DEMO_MODE", "true").lower() == "true"
    print(f"📱 Demo Mode: {'Enabled' if app_state['demo_mode'] else 'Disabled'}")
    yield
    # Shutdown
    print("🛑 Shutting down Odyssey 360 AI...")

# Initialize FastAPI app
app = FastAPI(
    title="Marriott's Odyssey 360 AI",
    description="The world's first fully intelligent hospitality operating system",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if app_state.get("demo_mode", True) else None,
    redoc_url="/redoc" if app_state.get("demo_mode", True) else None
)

# Security middleware
security = HTTPBearer()

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "*.marriott.com"]
)


# Telemetry middleware
class TelemetryMiddleware(BaseHTTPMiddleware):
    """Middleware to log telemetry for all requests"""
    
    async def dispatch(self, request: Request, call_next):
        # Start timer
        start_time = time.time()
        
        # Process request
        response = await call_next(request)
        
        # Calculate latency
        latency_ms = (time.time() - start_time) * 1000
        
        # Log telemetry
        if flags.TELEMETRY_ENABLED:
            telemetry({
                "event_type": "api_request",
                "path": request.url.path,
                "method": request.method,
                "status": response.status_code,
                "latency_ms": round(latency_ms, 2),
                "user_agent": request.headers.get("user-agent", "unknown")
            })
        
        return response


# Add telemetry middleware
app.add_middleware(TelemetryMiddleware)

# Include API routers (existing)
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(concierge.router, prefix="/api/v1/concierge", tags=["AI Concierge"])
app.include_router(emotion.router, prefix="/api/v1/emotion", tags=["Emotion AI"])
app.include_router(hotel.router, prefix="/api/v1/hotel", tags=["Hotel Services"])
app.include_router(wellness.router, prefix="/api/v1/wellness", tags=["Wellness & Safety"])
app.include_router(local_discovery.router, prefix="/api/v1/local", tags=["Local Discovery"])

# Include new feature routers
app.include_router(privacy.router, prefix="/api/privacy", tags=["Privacy"])
app.include_router(culture.router, prefix="/api/culture", tags=["Culture & Accessibility"])
app.include_router(trustlens.router, prefix="/api/trust", tags=["TrustLens"])
app.include_router(intermodal.router, prefix="/api/intermodal", tags=["Intermodal Transport"])
app.include_router(agentops.router, prefix="/api/agentops", tags=["AgentOps"])
app.include_router(insights.router, prefix="/api/insights", tags=["Insights & Wellness"])
app.include_router(hotel_iot.router, prefix="/api/room", tags=["Room & IoT Control"])
app.include_router(offers.router, prefix="/api/offers", tags=["Offers"])
app.include_router(analytics.router, prefix="/api", tags=["Analytics"])

@app.get("/")
async def root():
    """Root endpoint with system status"""
    return {
        "message": "Welcome to Marriott's Odyssey 360 AI",
        "version": "1.0.0",
        "status": "operational",
        "demo_mode": app_state.get("demo_mode", True),
        "features": [
            "Emotion AI",
            "AI Concierge",
            "Immersive Local Discovery",
            "Contactless Everything",
            "Wellness & Safety",
            "Group Management",
            "Accessibility & Inclusion"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z",
        "services": {
            "ai_concierge": "operational",
            "emotion_ai": "operational",
            "hotel_services": "operational",
            "wellness_monitoring": "operational",
            "local_discovery": "operational"
        }
    }

@app.get("/api/v1/system/status")
async def system_status(current_user: User = Depends(get_current_user)):
    """System status for authenticated users"""
    return {
        "user_id": current_user.id,
        "demo_mode": app_state.get("demo_mode", True),
        "ai_personality": current_user.preferred_ai_personality,
        "language": current_user.preferred_language,
        "accessibility_features": current_user.accessibility_features,
        "privacy_level": current_user.privacy_level
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
