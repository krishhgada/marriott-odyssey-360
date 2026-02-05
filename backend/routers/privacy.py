"""
Predictive Privacy Controller
Provides personalized privacy recommendations based on guest persona and preferences
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List, Literal
from shared.security import jwt_verify
from shared.telemetry import telemetry
from shared.config import flags

router = APIRouter()


class PrivacyRecommendRequest(BaseModel):
    """Request model for privacy recommendations"""
    persona: Literal["business", "family", "solo"] = Field(..., description="Guest persona type")
    trip_type: Literal["work", "leisure", "bleisure"] = Field(..., description="Type of trip")
    risk_tolerance: int = Field(..., ge=1, le=5, description="Privacy risk tolerance (1=paranoid, 5=open)")


class PrivacyToggles(BaseModel):
    """Privacy toggles configuration"""
    location_sharing: bool
    voice_history: bool
    personalization: bool


class PrivacyRecommendResponse(BaseModel):
    """Response model for privacy recommendations"""
    mode: Literal["strict", "balanced", "perks"]
    toggles: PrivacyToggles
    explanation: List[str]


def calculate_privacy_recommendation(
    persona: str, 
    trip_type: str, 
    risk_tolerance: int
) -> PrivacyRecommendResponse:
    """
    Deterministic privacy recommendation engine
    Based on persona, trip type, and risk tolerance
    """
    
    # Default to balanced
    mode = "balanced"
    location_sharing = True
    voice_history = False
    personalization = True
    explanation = []
    
    # Risk tolerance is the primary driver
    if risk_tolerance <= 2:
        # High privacy concern
        mode = "strict"
        location_sharing = False
        voice_history = False
        personalization = False
        explanation.append("Strict privacy mode recommended for low risk tolerance")
        explanation.append("All tracking disabled to maximize privacy")
        
    elif risk_tolerance >= 4:
        # Low privacy concern, maximize perks
        mode = "perks"
        location_sharing = True
        voice_history = True
        personalization = True
        explanation.append("Perks-optimized mode for better personalized experience")
        explanation.append("All features enabled to unlock maximum benefits")
        
    else:
        # Moderate - adjust based on persona and trip type
        mode = "balanced"
        
        if persona == "business":
            if trip_type == "work":
                location_sharing = True  # For meeting locations
                voice_history = False    # Professional privacy
                personalization = True   # For productivity
                explanation.append("Business traveler: location sharing for meetings")
                explanation.append("Voice history disabled for professional privacy")
            else:
                location_sharing = True
                voice_history = False
                personalization = True
                explanation.append("Business on leisure: balanced approach")
        
        elif persona == "family":
            location_sharing = True      # For family activities
            voice_history = True         # For convenience
            personalization = True       # For family recommendations
            explanation.append("Family mode: personalization for family activities")
            explanation.append("Voice enabled for hands-free convenience")
        
        elif persona == "solo":
            if trip_type == "leisure":
                location_sharing = True
                voice_history = False
                personalization = True
                explanation.append("Solo leisure: personalization with voice privacy")
            else:
                location_sharing = False
                voice_history = False
                personalization = True
                explanation.append("Solo work: minimal tracking, basic personalization")
    
    # Add mode-specific explanation
    if mode == "strict":
        explanation.append("⚠️ Note: Some features may be limited in strict mode")
    elif mode == "perks":
        explanation.append("✨ Unlock exclusive offers and personalized experiences")
    else:
        explanation.append("⚖️ Balanced privacy and personalization")
    
    return PrivacyRecommendResponse(
        mode=mode,
        toggles=PrivacyToggles(
            location_sharing=location_sharing,
            voice_history=voice_history,
            personalization=personalization
        ),
        explanation=explanation
    )


@router.post("/recommend", response_model=PrivacyRecommendResponse)
async def recommend_privacy_settings(
    request: PrivacyRecommendRequest,
    token_payload: dict = Depends(jwt_verify)
):
    """
    Get personalized privacy recommendations
    
    Based on guest persona, trip type, and risk tolerance,
    provides tailored privacy mode and toggle settings.
    """
    
    # Check feature flag
    if not flags.FEATURE_PRIVACY:
        raise HTTPException(status_code=501, detail="Privacy feature is not enabled")
    
    try:
        # Calculate recommendation
        recommendation = calculate_privacy_recommendation(
            persona=request.persona,
            trip_type=request.trip_type,
            risk_tolerance=request.risk_tolerance
        )
        
        # Log telemetry
        telemetry({
            "event_type": "privacy_recommend",
            "user_id": token_payload.get("sub", "unknown"),
            "persona": request.persona,
            "trip_type": request.trip_type,
            "risk_tolerance": request.risk_tolerance,
            "recommended_mode": recommendation.mode,
            "metadata": {"feature": "privacy"}
        })
        
        return recommendation
        
    except Exception as e:
        # Log error
        telemetry({
            "event_type": "privacy_error",
            "user_id": token_payload.get("sub", "unknown"),
            "error": str(e),
            "metadata": {"feature": "privacy"}
        })
        raise HTTPException(status_code=500, detail=f"Privacy recommendation failed: {str(e)}")


