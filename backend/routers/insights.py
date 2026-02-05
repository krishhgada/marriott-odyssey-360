"""
Insights - Bio-Haptic Mood to Proactive Suggestions
Analyzes guest mood and context to provide personalized recommendations
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List, Literal, Optional
from shared.security import jwt_verify
from shared.telemetry import telemetry
from shared.config import flags

router = APIRouter()


class MoodData(BaseModel):
    """Mood/biometric data"""
    stress_level: float = Field(..., ge=0, le=1, description="Stress level (0=calm, 1=very stressed)")
    energy_level: float = Field(..., ge=0, le=1, description="Energy level (0=exhausted, 1=energetic)")
    local_weather: str = Field(..., description="Current weather condition")


class ContextData(BaseModel):
    """Contextual information"""
    time_of_day: str = Field(..., description="Time in HH:MM format")
    occupancy_pct: float = Field(..., ge=0, le=100, description="Hotel occupancy percentage")


class PreferencesData(BaseModel):
    """Guest preferences"""
    likes_quiet: bool = Field(default=True, description="Prefers quiet environments")
    preferred_cuisine: str = Field(default="Italian", description="Preferred cuisine type")


class InsightsPredictRequest(BaseModel):
    """Request for mood-based prediction"""
    guest_id: str
    mood: MoodData
    context: ContextData
    preferences: PreferencesData


class Suggestion(BaseModel):
    """Actionable suggestion"""
    text: str
    action_id: str
    evidence: List[str]


class InsightsPredictResponse(BaseModel):
    """Response with predicted state and suggestion"""
    state: Literal["STRESSED", "FATIGUED", "CURIOUS", "CELEBRATORY", "NEUTRAL"]
    suggestion: Suggestion


def classify_guest_state(mood: MoodData, context: ContextData, preferences: PreferencesData) -> tuple:
    """
    Deterministic classifier for guest state
    Returns (state, suggestion, evidence)
    """
    
    # Parse time
    hour = int(context.time_of_day.split(':')[0])
    
    # Decision tree classification
    
    # STRESSED: High stress, any time, especially if rainy
    if mood.stress_level > 0.7:
        if preferences.likes_quiet:
            suggestion_text = "We recommend our quiet spa lounge with complimentary aromatherapy"
            action_id = "SPA_QUIET_LOUNGE"
            evidence = [
                f"Elevated stress level detected ({mood.stress_level:.1f})",
                "Guest preference: quiet environments",
                "Spa lounge currently at 30% capacity"
            ]
        else:
            suggestion_text = "Join our rooftop social hour with live jazz and light refreshments"
            action_id = "SOCIAL_ROOFTOP"
            evidence = [
                f"Elevated stress level detected ({mood.stress_level:.1f})",
                "Social activities help reduce stress",
                "Live music available now"
            ]
        return ("STRESSED", suggestion_text, action_id, evidence)
    
    # FATIGUED: Low energy, any time
    if mood.energy_level < 0.3:
        if hour < 12:
            suggestion_text = "Order our energizing breakfast with coffee to your room"
            action_id = "BREAKFAST_DELIVERY"
            evidence = [
                f"Low energy detected ({mood.energy_level:.1f})",
                "Morning time - nutritious meal recommended",
                "Room service available immediately"
            ]
        elif 12 <= hour < 17:
            suggestion_text = "Try our power nap pod with guided meditation (30 min)"
            action_id = "POWER_NAP_POD"
            evidence = [
                f"Low energy detected ({mood.energy_level:.1f})",
                "Afternoon energy dip is common",
                "Power nap can boost productivity"
            ]
        else:
            suggestion_text = "Early turndown service with sleep-inducing aromatherapy"
            action_id = "EARLY_TURNDOWN"
            evidence = [
                f"Low energy detected ({mood.energy_level:.1f})",
                "Evening - prepare for restful sleep",
                "Aromatherapy proven to improve sleep quality"
            ]
        return ("FATIGUED", suggestion_text, action_id, evidence)
    
    # CURIOUS: Moderate energy, moderate stress, daytime
    if 0.4 <= mood.energy_level <= 0.7 and mood.stress_level < 0.5 and 9 <= hour < 18:
        suggestion_text = f"Explore nearby {preferences.preferred_cuisine} restaurant (15 min walk)"
        action_id = "LOCAL_DINING"
        evidence = [
            "Balanced mood - perfect for exploration",
            f"Your preferred cuisine: {preferences.preferred_cuisine}",
            f"Weather: {mood.local_weather} - good for walking"
        ]
        return ("CURIOUS", suggestion_text, action_id, evidence)
    
    # CELEBRATORY: High energy, low stress
    if mood.energy_level > 0.7 and mood.stress_level < 0.3:
        if context.occupancy_pct < 70:
            suggestion_text = "Suite upgrade available with complimentary champagne 🎉"
            action_id = "SUITE_UPGRADE_WINE"
            evidence = [
                f"Positive energy detected ({mood.energy_level:.1f})",
                f"Hotel at {context.occupancy_pct:.0f}% occupancy - upgrades available",
                "Celebrate your stay with us!"
            ]
        else:
            suggestion_text = "Join our lobby celebration with live music and cocktails"
            action_id = "LOBBY_CELEBRATION"
            evidence = [
                f"Positive energy detected ({mood.energy_level:.1f})",
                "Social celebration happening now",
                "Complimentary welcome drink"
            ]
        return ("CELEBRATORY", suggestion_text, action_id, evidence)
    
    # NEUTRAL: Default case
    suggestion_text = "Enjoy our complimentary fitness center and pool area"
    action_id = "FITNESS_POOL"
    evidence = [
        "Balanced mood detected",
        "Physical activity enhances well-being",
        f"Current weather: {mood.local_weather}"
    ]
    return ("NEUTRAL", suggestion_text, action_id, evidence)


@router.post("/predict", response_model=InsightsPredictResponse)
async def predict_and_suggest(
    request: InsightsPredictRequest,
    token_payload: dict = Depends(jwt_verify)
):
    """
    Predict guest state from mood/context and provide suggestion
    """
    
    if not flags.FEATURE_INSIGHTS:
        raise HTTPException(status_code=501, detail="Insights feature is not enabled")
    
    try:
        state, suggestion_text, action_id, evidence = classify_guest_state(
            mood=request.mood,
            context=request.context,
            preferences=request.preferences
        )
        
        telemetry({
            "event_type": "insights_predict",
            "user_id": token_payload.get("sub", "unknown"),
            "guest_id": request.guest_id,
            "predicted_state": state,
            "action_id": action_id,
            "stress_level": request.mood.stress_level,
            "energy_level": request.mood.energy_level,
            "metadata": {"feature": "insights"}
        })
        
        return InsightsPredictResponse(
            state=state,
            suggestion=Suggestion(
                text=suggestion_text,
                action_id=action_id,
                evidence=evidence
            )
        )
        
    except Exception as e:
        telemetry({
            "event_type": "insights_error",
            "user_id": token_payload.get("sub", "unknown"),
            "error": str(e),
            "metadata": {"feature": "insights"}
        })
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


