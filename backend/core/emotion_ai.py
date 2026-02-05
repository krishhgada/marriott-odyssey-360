"""
Emotion AI Core Module for Marriott's Odyssey 360 AI
Real-time emotion detection and analysis from text, audio, and video
"""

import asyncio
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import cv2
import librosa
import torch
from transformers import pipeline, AutoTokenizer, AutoModel
import openai
from core.config import settings

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
    """Core Emotion AI class for real-time emotion detection"""
    
    def __init__(self):
        self.text_emotion_pipeline = None
        self.audio_emotion_pipeline = None
        self.vision_emotion_pipeline = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize AI models for emotion detection"""
        try:
            # Text emotion detection
            self.text_emotion_pipeline = pipeline(
                "text-classification",
                model="j-hartmann/emotion-english-distilroberta-base",
                device=self.device
            )
            
            # Audio emotion detection (using a pre-trained model)
            self.audio_emotion_pipeline = pipeline(
                "audio-classification",
                model="superb/hubert-large-superb-er",
                device=self.device
            )
            
            # Vision emotion detection (using OpenCV + custom model)
            self.vision_emotion_pipeline = self._load_vision_model()
            
        except Exception as e:
            print(f"Warning: Could not initialize some emotion models: {e}")
    
    def _load_vision_model(self):
        """Load vision-based emotion detection model"""
        try:
            # Load pre-trained facial emotion recognition model
            # This would typically be a more sophisticated model in production
            return cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        except Exception as e:
            print(f"Warning: Could not load vision model: {e}")
            return None
    
    async def detect_text_emotion(self, text: str, context: Optional[str] = None) -> EmotionResult:
        """Detect emotion from text input"""
        try:
            if not self.text_emotion_pipeline:
                return self._default_emotion_result()
            
            # Analyze text emotion
            result = self.text_emotion_pipeline(text)
            
            # Map to our emotion types
            emotion_mapping = {
                "joy": EmotionType.JOY,
                "sadness": EmotionType.SADNESS,
                "anger": EmotionType.ANGER,
                "fear": EmotionType.FEAR,
                "surprise": EmotionType.SURPRISE,
                "disgust": EmotionType.DISGUST,
                "neutral": EmotionType.NEUTRAL
            }
            
            emotion_label = result[0]["label"].lower()
            confidence = result[0]["score"]
            emotion = emotion_mapping.get(emotion_label, EmotionType.NEUTRAL)
            
            # Determine intensity based on confidence and text analysis
            intensity = self._determine_intensity(confidence, text)
            
            # Generate suggestions based on emotion
            suggestions = self._generate_emotion_suggestions(emotion, intensity, context)
            
            return EmotionResult(
                emotion=emotion,
                intensity=intensity,
                confidence=confidence,
                context=context,
                suggestions=suggestions
            )
            
        except Exception as e:
            print(f"Error in text emotion detection: {e}")
            return self._default_emotion_result()
    
    async def detect_audio_emotion(self, audio_data: bytes, sample_rate: int = 16000) -> EmotionResult:
        """Detect emotion from audio input"""
        try:
            if not self.audio_emotion_pipeline:
                return self._default_emotion_result()
            
            # Convert audio data to numpy array
            audio_array = np.frombuffer(audio_data, dtype=np.float32)
            
            # Analyze audio emotion
            result = self.audio_emotion_pipeline(audio_array)
            
            # Map to our emotion types
            emotion_mapping = {
                "happy": EmotionType.JOY,
                "sad": EmotionType.SADNESS,
                "angry": EmotionType.ANGER,
                "fearful": EmotionType.FEAR,
                "surprised": EmotionType.SURPRISE,
                "disgusted": EmotionType.DISGUST,
                "neutral": EmotionType.NEUTRAL
            }
            
            emotion_label = result[0]["label"].lower()
            confidence = result[0]["score"]
            emotion = emotion_mapping.get(emotion_label, EmotionType.NEUTRAL)
            
            # Determine intensity
            intensity = self._determine_intensity(confidence, None)
            
            # Generate suggestions
            suggestions = self._generate_emotion_suggestions(emotion, intensity, "audio")
            
            return EmotionResult(
                emotion=emotion,
                intensity=intensity,
                confidence=confidence,
                context="audio",
                suggestions=suggestions
            )
            
        except Exception as e:
            print(f"Error in audio emotion detection: {e}")
            return self._default_emotion_result()
    
    async def detect_vision_emotion(self, image_data: bytes) -> EmotionResult:
        """Detect emotion from image/video input"""
        try:
            if not self.vision_emotion_pipeline:
                return self._default_emotion_result()
            
            # Convert image data to OpenCV format
            nparr = np.frombuffer(image_data, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            # Convert to grayscale for face detection
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.vision_emotion_pipeline.detectMultiScale(gray, 1.1, 4)
            
            if len(faces) == 0:
                return self._default_emotion_result()
            
            # For demo purposes, we'll use a simplified emotion detection
            # In production, this would use a more sophisticated facial emotion model
            emotion = EmotionType.NEUTRAL
            confidence = 0.7
            intensity = EmotionIntensity.MEDIUM
            
            # Generate suggestions
            suggestions = self._generate_emotion_suggestions(emotion, intensity, "vision")
            
            return EmotionResult(
                emotion=emotion,
                intensity=intensity,
                confidence=confidence,
                context="vision",
                suggestions=suggestions
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
            suggestions=["How can I assist you today?"]
        )

# Global emotion AI instance
emotion_ai = EmotionAI()
