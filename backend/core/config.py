"""
Configuration settings for Marriott's Odyssey 360 AI
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    """Application settings"""
    
    # App Configuration
    app_name: str = "Marriott's Odyssey 360 AI"
    app_version: str = "1.0.0"
    debug: bool = False
    demo_mode: bool = True
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # Database
    database_url: str = "sqlite:///./odyssey360.db"
    mongodb_url: str = "mongodb://localhost:27017/odyssey360"
    redis_url: str = "redis://localhost:6379"
    
    # AI Services
    openai_api_key: Optional[str] = None
    emotion_ai_model: str = "emotion-bert-base"
    voice_ai_model: str = "whisper-1"
    vision_ai_model: str = "gpt-4-vision-preview"
    
    # Hotel Integration
    hotel_api_base_url: str = "https://api.marriott.com/v1"
    room_control_api_url: str = "https://iot.marriott.com/api"
    f_b_ordering_api_url: str = "https://fandb.marriott.com/api"
    
    # IoT and Sensors
    iot_mqtt_broker: str = "mqtt.marriott.com"
    iot_mqtt_port: int = 8883
    sensor_data_retention_hours: int = 24
    
    # Privacy and Ethics
    data_anonymization_enabled: bool = True
    raw_data_retention_seconds: int = 0  # Zero retention policy
    guest_consent_required: bool = True
    transparency_mode: bool = True
    
    # Supported Languages
    supported_languages: List[str] = [
        "en", "es", "fr", "de", "it", "pt", "ru", "zh", "ja", "ko",
        "ar", "hi", "th", "vi", "tr", "pl", "nl", "sv", "da", "no",
        "fi", "cs", "hu", "ro", "bg", "hr", "sk", "sl", "et", "lv", "lt"
    ]
    
    # Accessibility Features
    accessibility_features: List[str] = [
        "voice_control", "screen_reader", "high_contrast", "large_text",
        "haptic_feedback", "audio_descriptions", "sign_language", "braille"
    ]
    
    # AI Personalities
    ai_personalities: List[str] = [
        "professional", "friendly", "enthusiastic", "calm", "humorous",
        "formal", "casual", "empathetic", "efficient", "conversational"
    ]
    
    # Wellness Monitoring
    wellness_metrics: List[str] = [
        "stress_level", "sleep_quality", "mood", "energy_level",
        "social_interaction", "physical_activity", "nutrition_balance"
    ]
    
    # Local Discovery
    local_services: List[str] = [
        "restaurants", "attractions", "shopping", "transportation",
        "events", "wellness", "entertainment", "cultural_sites"
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Allow extra environment variables

# Global settings instance
settings = Settings()
