"""
Emotion AI API endpoints for Marriott's Odyssey 360 AI
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from typing import Optional, Dict, Any
from datetime import datetime

from core.emotion_ai_simple import emotion_ai, EmotionType, EmotionIntensity
from models.user import User
from core.security import get_current_user

router = APIRouter()

@router.post("/detect/text")
async def detect_text_emotion(
    text: str,
    context: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """Detect emotion from text input"""
    try:
        result = await emotion_ai.detect_text_emotion(text, context)
        
        return {
            "success": True,
            "emotion_detection": {
                "emotion": result.emotion.value,
                "intensity": result.intensity.value,
                "confidence": result.confidence,
                "context": result.context,
                "suggestions": result.suggestions,
                "timestamp": result.timestamp or datetime.now().isoformat()
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error detecting text emotion: {str(e)}"
        )

@router.post("/detect/audio")
async def detect_audio_emotion(
    audio_file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """Detect emotion from audio input"""
    try:
        audio_data = await audio_file.read()
        result = await emotion_ai.detect_audio_emotion(audio_data)
        
        return {
            "success": True,
            "emotion_detection": {
                "emotion": result.emotion.value,
                "intensity": result.intensity.value,
                "confidence": result.confidence,
                "context": result.context,
                "suggestions": result.suggestions,
                "timestamp": result.timestamp or datetime.now().isoformat()
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error detecting audio emotion: {str(e)}"
        )

@router.post("/detect/video")
async def detect_video_emotion(
    video_file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """Detect emotion from video input"""
    try:
        video_data = await video_file.read()
        result = await emotion_ai.detect_vision_emotion(video_data)
        
        return {
            "success": True,
            "emotion_detection": {
                "emotion": result.emotion.value,
                "intensity": result.intensity.value,
                "confidence": result.confidence,
                "context": result.context,
                "suggestions": result.suggestions,
                "timestamp": result.timestamp or datetime.now().isoformat()
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error detecting video emotion: {str(e)}"
        )

@router.get("/emotions")
async def get_available_emotions():
    """Get available emotion types"""
    return {
        "success": True,
        "emotions": [
            {
                "id": emotion.value,
                "name": emotion.value.title(),
                "description": f"Emotion type: {emotion.value}"
            }
            for emotion in EmotionType
        ]
    }

@router.get("/intensities")
async def get_available_intensities():
    """Get available intensity levels"""
    return {
        "success": True,
        "intensities": [
            {
                "id": intensity.value,
                "name": intensity.value.replace("_", " ").title(),
                "description": f"Intensity level: {intensity.value}"
            }
            for intensity in EmotionIntensity
        ]
    }

@router.get("/status")
async def get_emotion_ai_status():
    """Get Emotion AI system status"""
    return {
        "success": True,
        "status": "operational",
        "features": {
            "text_emotion_detection": emotion_ai.text_emotion_pipeline is not None,
            "audio_emotion_detection": emotion_ai.audio_emotion_pipeline is not None,
            "vision_emotion_detection": emotion_ai.vision_emotion_pipeline is not None,
            "proactive_suggestions": True,
            "real_time_processing": True
        },
        "supported_formats": {
            "text": ["plain text", "markdown"],
            "audio": ["wav", "mp3", "m4a", "flac"],
            "video": ["mp4", "avi", "mov", "webm"]
        },
        "timestamp": datetime.now().isoformat()
    }
