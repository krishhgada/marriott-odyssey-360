"""
Simplified AI Concierge Core Module for Marriott's Odyssey 360 AI
Demo version without heavy ML dependencies
"""

import asyncio
import random
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from core.emotion_ai_simple import EmotionAI, EmotionResult, EmotionType
from models.user import User

class ConciergePersonality(str, Enum):
    """AI Concierge personality types"""
    PROFESSIONAL = "professional"
    FRIENDLY = "friendly"
    ENTHUSIASTIC = "enthusiastic"
    CALM = "calm"
    HUMOROUS = "humorous"
    FORMAL = "formal"
    CASUAL = "casual"
    EMPATHETIC = "empathetic"
    EFFICIENT = "efficient"
    CONVERSATIONAL = "conversational"

class ServiceType(str, Enum):
    """Service types the concierge can provide"""
    ROOM_SERVICE = "room_service"
    HOUSEKEEPING = "housekeeping"
    CONCIERGE = "concierge"
    DINING = "dining"
    WELLNESS = "wellness"
    TRANSPORTATION = "transportation"
    ENTERTAINMENT = "entertainment"
    BUSINESS = "business"
    EMERGENCY = "emergency"
    GENERAL = "general"

@dataclass
class ConciergeResponse:
    """AI Concierge response"""
    message: str
    personality: ConciergePersonality
    service_type: ServiceType
    suggestions: List[str]
    proactive_actions: List[Dict[str, Any]]
    emotion_detected: Optional[EmotionResult] = None
    follow_up_questions: List[str] = None
    requires_human: bool = False

class ConciergeAI:
    """Simplified AI Concierge class for demo purposes"""
    
    def __init__(self):
        self.emotion_ai = EmotionAI()
        self.conversation_memory = {}
        self.personality_prompts = self._initialize_personality_prompts()
        self.service_templates = self._initialize_service_templates()
        
    def _initialize_personality_prompts(self) -> Dict[ConciergePersonality, str]:
        """Initialize personality-specific prompts"""
        return {
            ConciergePersonality.PROFESSIONAL: "You are a professional, courteous, and efficient AI concierge.",
            ConciergePersonality.FRIENDLY: "You are a warm, approachable, and genuinely caring AI concierge.",
            ConciergePersonality.ENTHUSIASTIC: "You are an energetic, passionate, and exciting AI concierge.",
            ConciergePersonality.CALM: "You are a serene, composed, and soothing AI concierge.",
            ConciergePersonality.HUMOROUS: "You are a witty, charming, and light-hearted AI concierge.",
            ConciergePersonality.EMPATHETIC: "You are a deeply understanding, compassionate, and emotionally intelligent AI concierge."
        }
    
    def _initialize_service_templates(self) -> Dict[ServiceType, Dict[str, Any]]:
        """Initialize service-specific response templates"""
        return {
            ServiceType.ROOM_SERVICE: {
                "greeting": "I'd be happy to help with your room service needs!",
                "capabilities": ["Order food and beverages", "Schedule housekeeping", "Adjust room settings"]
            },
            ServiceType.DINING: {
                "greeting": "Let me help you discover amazing dining experiences!",
                "capabilities": ["Recommend restaurants", "Make reservations", "Suggest dietary options"]
            },
            ServiceType.WELLNESS: {
                "greeting": "I'm here to support your wellness and relaxation needs!",
                "capabilities": ["Schedule spa treatments", "Recommend fitness activities", "Arrange wellness services"]
            },
            ServiceType.CONCIERGE: {
                "greeting": "How can I make your stay more memorable today?",
                "capabilities": ["Recommend local attractions", "Arrange transportation", "Book experiences"]
            }
        }
    
    async def process_guest_message(
        self, 
        message: str, 
        user: User, 
        context: Optional[Dict[str, Any]] = None
    ) -> ConciergeResponse:
        """Process guest message and generate appropriate response"""
        
        # Detect emotion from the message
        emotion_result = await self.emotion_ai.detect_text_emotion(message, context.get("conversation_context") if context else None)
        
        # Determine service type
        service_type = self._classify_service_type(message)
        
        # Get personality-specific response
        personality = ConciergePersonality(user.preferred_ai_personality)
        response = await self._generate_response(
            message, user, personality, service_type, emotion_result, context
        )
        
        # Update conversation memory
        self._update_conversation_memory(user.id, message, response)
        
        return response
    
    def _classify_service_type(self, message: str) -> ServiceType:
        """Classify the type of service requested"""
        message_lower = message.lower()
        
        # Room service keywords
        if any(word in message_lower for word in ["room", "housekeeping", "cleaning", "amenities", "temperature", "lighting"]):
            return ServiceType.ROOM_SERVICE
        
        # Dining keywords
        elif any(word in message_lower for word in ["food", "dining", "restaurant", "menu", "dinner", "lunch", "breakfast", "eat"]):
            return ServiceType.DINING
        
        # Wellness keywords
        elif any(word in message_lower for word in ["spa", "wellness", "massage", "fitness", "gym", "relax", "meditation", "yoga"]):
            return ServiceType.WELLNESS
        
        # Transportation keywords
        elif any(word in message_lower for word in ["transport", "taxi", "uber", "airport", "shuttle", "car", "ride"]):
            return ServiceType.TRANSPORTATION
        
        # Entertainment keywords
        elif any(word in message_lower for word in ["entertainment", "show", "movie", "theater", "concert", "event", "fun"]):
            return ServiceType.ENTERTAINMENT
        
        # Business keywords
        elif any(word in message_lower for word in ["business", "meeting", "conference", "work", "office", "presentation"]):
            return ServiceType.BUSINESS
        
        # Emergency keywords
        elif any(word in message_lower for word in ["emergency", "help", "urgent", "problem", "issue", "assistance"]):
            return ServiceType.EMERGENCY
        
        else:
            return ServiceType.GENERAL
    
    async def _generate_response(
        self, 
        message: str, 
        user: User, 
        personality: ConciergePersonality,
        service_type: ServiceType,
        emotion_result: EmotionResult,
        context: Optional[Dict[str, Any]]
    ) -> ConciergeResponse:
        """Generate AI concierge response"""
        
        # Get personality prompt
        personality_prompt = self.personality_prompts.get(personality, self.personality_prompts[ConciergePersonality.PROFESSIONAL])
        
        # Get service template
        service_template = self.service_templates.get(service_type, {})
        
        # Generate response using template-based approach
        response_text = self._generate_template_response(message, personality, service_type, emotion_result, user)
        
        # Generate proactive actions based on emotion and context
        proactive_actions = self._generate_proactive_actions(emotion_result, service_type, user)
        
        # Generate follow-up questions
        follow_up_questions = self._generate_follow_up_questions(service_type, emotion_result)
        
        # Determine if human intervention is needed
        requires_human = self._requires_human_intervention(message, emotion_result, service_type)
        
        return ConciergeResponse(
            message=response_text,
            personality=personality,
            service_type=service_type,
            suggestions=emotion_result.suggestions if emotion_result else [],
            proactive_actions=proactive_actions,
            emotion_detected=emotion_result,
            follow_up_questions=follow_up_questions,
            requires_human=requires_human
        )
    
    def _generate_template_response(
        self, 
        message: str, 
        personality: ConciergePersonality,
        service_type: ServiceType,
        emotion_result: Optional[EmotionResult],
        user: User
    ) -> str:
        """Generate template-based response for demo purposes"""
        
        guest_name = user.first_name
        emotion = emotion_result.emotion.value if emotion_result else "neutral"
        
        # Base greeting based on personality
        if personality == ConciergePersonality.FRIENDLY:
            greeting = f"Hi {guest_name}! I'm so happy to help you today! 😊"
        elif personality == ConciergePersonality.PROFESSIONAL:
            greeting = f"Good day, {guest_name}. How may I assist you today?"
        elif personality == ConciergePersonality.ENTHUSIASTIC:
            greeting = f"Hello {guest_name}! I'm excited to help make your stay amazing! ✨"
        elif personality == ConciergePersonality.CALM:
            greeting = f"Hello {guest_name}. I'm here to help you feel comfortable and relaxed."
        elif personality == ConciergePersonality.HUMOROUS:
            greeting = f"Hey there, {guest_name}! Ready to have some fun? Let me know what you need! 😄"
        elif personality == ConciergePersonality.EMPATHETIC:
            greeting = f"Hello {guest_name}. I'm here to listen and help however I can."
        else:
            greeting = f"Hello {guest_name}. How can I assist you today?"
        
        # Service-specific response
        service_responses = {
            ServiceType.ROOM_SERVICE: "I'd be delighted to help with your room needs! I can assist with housekeeping, room service, temperature control, or any amenities you might need.",
            ServiceType.DINING: "I'd love to help you discover amazing dining experiences! I can recommend restaurants, make reservations, or help with special dietary needs.",
            ServiceType.WELLNESS: "I'm here to support your wellness journey! I can help with spa bookings, fitness activities, or any relaxation needs you have.",
            ServiceType.CONCIERGE: "I'm excited to help make your stay memorable! I can recommend local attractions, arrange transportation, or coordinate special experiences.",
            ServiceType.TRANSPORTATION: "I'd be happy to help with your transportation needs! I can arrange airport transfers, local rides, or provide transportation information.",
            ServiceType.ENTERTAINMENT: "Let me help you find some great entertainment! I can suggest shows, events, or activities that match your interests.",
            ServiceType.BUSINESS: "I'm here to support your business needs! I can help with meeting arrangements, business services, or work-related requests.",
            ServiceType.EMERGENCY: "I understand this is urgent. Let me help you immediately. What specific assistance do you need right now?",
            ServiceType.GENERAL: "I'm here to help with whatever you need! Feel free to ask me anything about your stay or our services."
        }
        
        service_response = service_responses.get(service_type, service_responses[ServiceType.GENERAL])
        
        # Emotion-aware response
        if emotion_result and emotion_result.emotion in [EmotionType.STRESS, EmotionType.ANXIETY]:
            emotion_response = " I can sense you might be feeling a bit stressed. Let me help make things easier for you."
        elif emotion_result and emotion_result.emotion in [EmotionType.SADNESS]:
            emotion_response = " I want to make sure you're comfortable and happy during your stay. How can I help brighten your day?"
        elif emotion_result and emotion_result.emotion in [EmotionType.JOY, EmotionType.EXCITEMENT]:
            emotion_response = " I love your positive energy! Let's make your stay even more amazing!"
        else:
            emotion_response = ""
        
        return f"{greeting} {service_response}{emotion_response}"
    
    def _generate_proactive_actions(
        self, 
        emotion_result: Optional[EmotionResult], 
        service_type: ServiceType,
        user: User
    ) -> List[Dict[str, Any]]:
        """Generate proactive actions based on emotion and context"""
        actions = []
        
        if emotion_result:
            if emotion_result.emotion in [EmotionType.STRESS, EmotionType.ANXIETY]:
                actions.extend([
                    {"action": "adjust_lighting", "value": "dim", "reason": "Create calming atmosphere"},
                    {"action": "suggest_wellness", "value": "spa_treatment", "reason": "Help reduce stress"},
                    {"action": "adjust_temperature", "value": "comfortable", "reason": "Optimize comfort"}
                ])
            elif emotion_result.emotion == EmotionType.SADNESS:
                actions.extend([
                    {"action": "suggest_entertainment", "value": "uplifting_activity", "reason": "Boost mood"},
                    {"action": "offer_comfort_food", "value": "favorite_dish", "reason": "Provide comfort"}
                ])
            elif emotion_result.emotion in [EmotionType.JOY, EmotionType.EXCITEMENT]:
                actions.extend([
                    {"action": "suggest_premium_services", "value": "upgrade_options", "reason": "Enhance positive experience"},
                    {"action": "recommend_activities", "value": "exciting_experiences", "reason": "Maintain positive energy"}
                ])
        
        return actions
    
    def _generate_follow_up_questions(self, service_type: ServiceType, emotion_result: Optional[EmotionResult]) -> List[str]:
        """Generate relevant follow-up questions"""
        questions = []
        
        if service_type == ServiceType.ROOM_SERVICE:
            questions.extend([
                "Would you like me to schedule housekeeping for a specific time?",
                "Is there anything specific you'd like me to arrange for your room?",
                "Would you like me to adjust any room settings for you?"
            ])
        elif service_type == ServiceType.DINING:
            questions.extend([
                "Do you have any dietary restrictions or preferences?",
                "What type of cuisine are you in the mood for?",
                "Would you like me to make a reservation for you?"
            ])
        elif service_type == ServiceType.WELLNESS:
            questions.extend([
                "What type of wellness experience are you looking for?",
                "Do you have any specific health goals or preferences?",
                "Would you like me to check availability for spa services?"
            ])
        
        return questions[:2]  # Return top 2 questions
    
    def _requires_human_intervention(self, message: str, emotion_result: Optional[EmotionResult], service_type: ServiceType) -> bool:
        """Determine if human intervention is required"""
        
        # Emergency situations always require human intervention
        if service_type == ServiceType.EMERGENCY:
            return True
        
        # High-intensity negative emotions might need human touch
        if emotion_result and emotion_result.intensity.value in ["high", "very_high"]:
            if emotion_result.emotion in [EmotionType.ANGER, EmotionType.FRUSTRATION]:
                return True
        
        # Complex requests that AI can't handle
        complex_keywords = ["complaint", "refund", "manager", "supervisor", "legal", "medical"]
        if any(keyword in message.lower() for keyword in complex_keywords):
            return True
        
        return False
    
    def _update_conversation_memory(self, user_id: int, message: str, response: ConciergeResponse):
        """Update conversation memory for context"""
        if user_id not in self.conversation_memory:
            self.conversation_memory[user_id] = []
        
        self.conversation_memory[user_id].append({
            "timestamp": datetime.now().isoformat(),
            "user_message": message,
            "ai_response": response.message,
            "emotion_detected": response.emotion_detected.emotion.value if response.emotion_detected else None,
            "service_type": response.service_type.value
        })
        
        # Keep only last 20 messages to prevent memory bloat
        if len(self.conversation_memory[user_id]) > 20:
            self.conversation_memory[user_id] = self.conversation_memory[user_id][-20:]

# Global concierge AI instance
concierge_ai = ConciergeAI()
