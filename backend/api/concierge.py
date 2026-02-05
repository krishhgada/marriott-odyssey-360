"""
AI Concierge API endpoints for Marriott's Odyssey 360 AI
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from typing import Optional, Dict, Any, List
import json
from datetime import datetime

from core.concierge_ai_simple import concierge_ai, ConciergePersonality, ServiceType
from core.emotion_ai_simple import emotion_ai
from models.user import User
from core.security import get_current_user

router = APIRouter()

@router.post("/chat")
async def chat_with_concierge(
    message: str,
    context: Optional[Dict[str, Any]] = None,
    current_user: User = Depends(get_current_user)
):
    """Chat with the AI concierge"""
    try:
        response = await concierge_ai.process_guest_message(
            message=message,
            user=current_user,
            context=context or {}
        )
        
        return {
            "success": True,
            "response": {
                "message": response.message,
                "personality": response.personality.value,
                "service_type": response.service_type.value,
                "suggestions": response.suggestions,
                "proactive_actions": response.proactive_actions,
                "emotion_detected": {
                    "emotion": response.emotion_detected.emotion.value if response.emotion_detected else None,
                    "intensity": response.emotion_detected.intensity.value if response.emotion_detected else None,
                    "confidence": response.emotion_detected.confidence if response.emotion_detected else None
                } if response.emotion_detected else None,
                "follow_up_questions": response.follow_up_questions,
                "requires_human": response.requires_human,
                "timestamp": datetime.now().isoformat()
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing concierge request: {str(e)}"
        )

@router.post("/chat/voice")
async def chat_with_concierge_voice(
    audio_file: UploadFile = File(...),
    context: Optional[Dict[str, Any]] = None,
    current_user: User = Depends(get_current_user)
):
    """Chat with the AI concierge using voice input"""
    try:
        # Read audio file
        audio_data = await audio_file.read()
        
        # Detect emotion from audio
        emotion_result = await emotion_ai.detect_audio_emotion(audio_data)
        
        # For demo purposes, we'll simulate a voice-to-text conversion
        # In production, this would use a speech-to-text service
        simulated_message = "I'd like to order room service and get some recommendations for local dining."
        
        response = await concierge_ai.process_guest_message(
            message=simulated_message,
            user=current_user,
            context=context or {}
        )
        
        return {
            "success": True,
            "response": {
                "message": response.message,
                "personality": response.personality.value,
                "service_type": response.service_type.value,
                "suggestions": response.suggestions,
                "proactive_actions": response.proactive_actions,
                "emotion_detected": {
                    "emotion": emotion_result.emotion.value,
                    "intensity": emotion_result.intensity.value,
                    "confidence": emotion_result.confidence
                },
                "follow_up_questions": response.follow_up_questions,
                "requires_human": response.requires_human,
                "timestamp": datetime.now().isoformat()
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing voice request: {str(e)}"
        )

@router.post("/chat/video")
async def chat_with_concierge_video(
    video_file: UploadFile = File(...),
    context: Optional[Dict[str, Any]] = None,
    current_user: User = Depends(get_current_user)
):
    """Chat with the AI concierge using video input"""
    try:
        # Read video file
        video_data = await video_file.read()
        
        # Detect emotion from video
        emotion_result = await emotion_ai.detect_vision_emotion(video_data)
        
        # For demo purposes, we'll simulate a video analysis
        simulated_message = "I'm looking for some relaxation activities and wellness services."
        
        response = await concierge_ai.process_guest_message(
            message=simulated_message,
            user=current_user,
            context=context or {}
        )
        
        return {
            "success": True,
            "response": {
                "message": response.message,
                "personality": response.personality.value,
                "service_type": response.service_type.value,
                "suggestions": response.suggestions,
                "proactive_actions": response.proactive_actions,
                "emotion_detected": {
                    "emotion": emotion_result.emotion.value,
                    "intensity": emotion_result.intensity.value,
                    "confidence": emotion_result.confidence
                },
                "follow_up_questions": response.follow_up_questions,
                "requires_human": response.requires_human,
                "timestamp": datetime.now().isoformat()
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing video request: {str(e)}"
        )

@router.get("/personalities")
async def get_available_personalities():
    """Get available AI concierge personalities"""
    return {
        "success": True,
        "personalities": [
            {
                "id": personality.value,
                "name": personality.value.title(),
                "description": f"AI concierge with {personality.value} personality"
            }
            for personality in ConciergePersonality
        ]
    }

@router.get("/service-types")
async def get_available_service_types():
    """Get available service types"""
    return {
        "success": True,
        "service_types": [
            {
                "id": service_type.value,
                "name": service_type.value.replace("_", " ").title(),
                "description": f"Services related to {service_type.value.replace('_', ' ')}"
            }
            for service_type in ServiceType
        ]
    }

@router.post("/personality/update")
async def update_personality(
    personality: ConciergePersonality,
    current_user: User = Depends(get_current_user)
):
    """Update user's preferred AI personality"""
    try:
        # In a real implementation, this would update the user's preferences in the database
        # For demo purposes, we'll just return success
        return {
            "success": True,
            "message": f"AI personality updated to {personality.value}",
            "new_personality": personality.value
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating personality: {str(e)}"
        )

@router.get("/conversation/history")
async def get_conversation_history(
    limit: int = 10,
    current_user: User = Depends(get_current_user)
):
    """Get conversation history for the current user"""
    try:
        # Get conversation history from concierge AI
        history = concierge_ai.conversation_memory.get(current_user.id, [])
        
        # Return last N messages
        recent_history = history[-limit:] if len(history) > limit else history
        
        return {
            "success": True,
            "conversation_history": recent_history,
            "total_messages": len(history)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving conversation history: {str(e)}"
        )

@router.delete("/conversation/clear")
async def clear_conversation_history(
    current_user: User = Depends(get_current_user)
):
    """Clear conversation history for the current user"""
    try:
        # Clear conversation history
        if current_user.id in concierge_ai.conversation_memory:
            del concierge_ai.conversation_memory[current_user.id]
        
        return {
            "success": True,
            "message": "Conversation history cleared successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error clearing conversation history: {str(e)}"
        )

@router.get("/status")
async def get_concierge_status():
    """Get AI concierge system status"""
    return {
        "success": True,
        "status": "operational",
        "features": {
            "text_chat": True,
            "voice_chat": True,
            "video_chat": True,
            "emotion_detection": True,
            "personality_switching": True,
            "proactive_actions": True,
            "multilingual_support": True
        },
        "supported_languages": [
            "en", "es", "fr", "de", "it", "pt", "ru", "zh", "ja", "ko"
        ],
        "available_personalities": [p.value for p in ConciergePersonality],
        "timestamp": datetime.now().isoformat()
    }
