"""
Simplified Emotion AI Core Module for Marriott's Odyssey 360 AI
Demo version without heavy ML dependencies
"""

import asyncio
import random
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

class EmotionType(str, Enum):
    """Emotion types enumeration"""
    JOY = "joy"
    SADNESS = "sadness"
    ANGER = "anger"
    FEAR = "fear"
    SURPRISE = "surprise"
    DISGUST = "disgust"
    NEUTRAL = "neutral"
    STRESS = "stress"
    EXCITEMENT = "excitement"
    CONTENTMENT = "contentment"
    ANXIETY = "anxiety"
    FRUSTRATION = "frustration"

class EmotionIntensity(str, Enum):
    """Emotion intensity levels"""
    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"

@dataclass
class EmotionResult:
    """Emotion detection result"""
    emotion: EmotionType
    intensity: EmotionIntensity
    confidence: float
    context: Optional[str] = None
    suggestions: List[str] = None
    timestamp: Optional[str] = None

class EmotionAI:
    """Simplified Emotion AI class for demo purposes"""
    
    def __init__(self):
        self.emotion_keywords = {
            EmotionType.JOY: ["happy", "excited", "great", "amazing", "wonderful", "fantastic", "love", "enjoy"],
            EmotionType.SADNESS: ["sad", "depressed", "down", "upset", "disappointed", "hurt", "lonely"],
            EmotionType.ANGER: ["angry", "mad", "furious", "annoyed", "irritated", "frustrated", "rage"],
            EmotionType.FEAR: ["scared", "afraid", "worried", "anxious", "nervous", "terrified", "panic"],
            EmotionType.STRESS: ["stressed", "overwhelmed", "pressure", "tense", "burned out", "exhausted"],
            EmotionType.EXCITEMENT: ["excited", "thrilled", "pumped", "energized", "enthusiastic", "eager"]
        }
    
    async def detect_text_emotion(self, text: str, context: Optional[str] = None) -> EmotionResult:
        """Detect emotion from text input (simplified demo version)"""
        try:
            text_lower = text.lower()
            
            # Simple keyword-based emotion detection
            emotion_scores = {}
            for emotion, keywords in self.emotion_keywords.items():
                score = sum(1 for keyword in keywords if keyword in text_lower)
                if score > 0:
                    emotion_scores[emotion] = score
            
            if emotion_scores:
                # Get emotion with highest score
                detected_emotion = max(emotion_scores, key=emotion_scores.get)
                confidence = min(0.9, 0.5 + (emotion_scores[detected_emotion] * 0.1))
            else:
                detected_emotion = EmotionType.NEUTRAL
                confidence = 0.5
            
            # Determine intensity based on confidence and text analysis
            intensity = self._determine_intensity(confidence, text)
            
            # Generate suggestions based on emotion
            suggestions = self._generate_emotion_suggestions(detected_emotion, intensity, context)
            
            return EmotionResult(
                emotion=detected_emotion,
                intensity=intensity,
                confidence=confidence,
                context=context,
                suggestions=suggestions,
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            print(f"Error in text emotion detection: {e}")
            return self._default_emotion_result()
    
    async def detect_audio_emotion(self, audio_data: bytes, sample_rate: int = 16000) -> EmotionResult:
        """Detect emotion from audio input (demo version)"""
        try:
            # For demo purposes, simulate emotion detection
            emotions = [EmotionType.JOY, EmotionType.NEUTRAL, EmotionType.STRESS, EmotionType.EXCITEMENT]
            detected_emotion = random.choice(emotions)
            confidence = random.uniform(0.6, 0.9)
            intensity = self._determine_intensity(confidence, None)
            
            suggestions = self._generate_emotion_suggestions(detected_emotion, intensity, "audio")
            
            return EmotionResult(
                emotion=detected_emotion,
                intensity=intensity,
                confidence=confidence,
                context="audio",
                suggestions=suggestions,
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            print(f"Error in audio emotion detection: {e}")
            return self._default_emotion_result()
    
    async def detect_vision_emotion(self, image_data: bytes) -> EmotionResult:
        """Detect emotion from image/video input (demo version)"""
        try:
            # For demo purposes, simulate emotion detection
            emotions = [EmotionType.JOY, EmotionType.NEUTRAL, EmotionType.SADNESS, EmotionType.SURPRISE]
            detected_emotion = random.choice(emotions)
            confidence = random.uniform(0.7, 0.95)
            intensity = self._determine_intensity(confidence, None)
            
            suggestions = self._generate_emotion_suggestions(detected_emotion, intensity, "vision")
            
            return EmotionResult(
                emotion=detected_emotion,
                intensity=intensity,
                confidence=confidence,
                context="vision",
                suggestions=suggestions,
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            print(f"Error in vision emotion detection: {e}")
            return self._default_emotion_result()
    
    def _determine_intensity(self, confidence: float, text: Optional[str] = None) -> EmotionIntensity:
        """Determine emotion intensity based on confidence and context"""
        if confidence >= 0.9:
            return EmotionIntensity.VERY_HIGH
        elif confidence >= 0.7:
            return EmotionIntensity.HIGH
        elif confidence >= 0.5:
            return EmotionIntensity.MEDIUM
        elif confidence >= 0.3:
            return EmotionIntensity.LOW
        else:
            return EmotionIntensity.VERY_LOW
    
    def _generate_emotion_suggestions(self, emotion: EmotionType, intensity: EmotionIntensity, context: Optional[str]) -> List[str]:
        """Generate proactive suggestions based on detected emotion"""
        suggestions = []
        
        if emotion == EmotionType.STRESS or emotion == EmotionType.ANXIETY:
            suggestions.extend([
                "Would you like me to dim the lights and play calming music?",
                "I can schedule a spa treatment or meditation session for you.",
                "Would you prefer a quiet room service meal in your room?",
                "I can adjust the room temperature to a more comfortable level."
            ])
        elif emotion == EmotionType.SADNESS:
            suggestions.extend([
                "Would you like me to suggest some uplifting activities?",
                "I can arrange for your favorite comfort food to be delivered.",
                "Would you like to connect with our concierge for local entertainment?",
                "I can adjust the room lighting to be more cheerful."
            ])
        elif emotion == EmotionType.JOY or emotion == EmotionType.EXCITEMENT:
            suggestions.extend([
                "Would you like me to suggest some exciting local activities?",
                "I can help you plan a special celebration dinner.",
                "Would you like to explore our premium amenities?",
                "I can arrange for a surprise upgrade or special treat."
            ])
        elif emotion == EmotionType.ANGER or emotion == EmotionType.FRUSTRATION:
            suggestions.extend([
                "I understand you're frustrated. How can I help resolve this?",
                "Would you like me to connect you with our manager?",
                "I can arrange for a quiet space or different room if needed.",
                "Would you like me to suggest some stress-relief activities?"
            ])
        
        return suggestions[:3]  # Return top 3 suggestions
    
    def _default_emotion_result(self) -> EmotionResult:
        """Return default emotion result when detection fails"""
        return EmotionResult(
            emotion=EmotionType.NEUTRAL,
            intensity=EmotionIntensity.MEDIUM,
            confidence=0.5,
            suggestions=["How can I assist you today?"],
            timestamp=datetime.now().isoformat()
        )

# Global emotion AI instance
emotion_ai = EmotionAI()
