"""
User models for Marriott's Odyssey 360 AI
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

Base = declarative_base()

class PrivacyLevel(str, Enum):
    """Privacy level enumeration"""
    MINIMAL = "minimal"
    STANDARD = "standard"
    ENHANCED = "enhanced"
    FULL = "full"

class AccessibilityLevel(str, Enum):
    """Accessibility level enumeration"""
    NONE = "none"
    BASIC = "basic"
    ENHANCED = "enhanced"
    FULL = "full"

class User(Base):
    """User database model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    
    # AI and Personalization
    preferred_ai_personality = Column(String, default="professional")
    preferred_language = Column(String, default="en")
    accessibility_features = Column(JSON, default=list)
    privacy_level = Column(String, default=PrivacyLevel.STANDARD)
    
    # Guest Preferences
    dietary_restrictions = Column(JSON, default=list)
    room_preferences = Column(JSON, default=dict)
    service_preferences = Column(JSON, default=dict)
    wellness_goals = Column(JSON, default=list)
    
    # Biometric and Security
    biometric_enabled = Column(Boolean, default=False)
    voice_enabled = Column(Boolean, default=False)
    face_recognition_enabled = Column(Boolean, default=False)
    
    # Experience Memory
    visit_history = Column(JSON, default=list)
    preferences_learned = Column(JSON, default=dict)
    satisfaction_scores = Column(JSON, default=list)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

class UserCreate(BaseModel):
    """User creation model"""
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    preferred_ai_personality: str = "professional"
    preferred_language: str = "en"
    accessibility_features: List[str] = []
    privacy_level: PrivacyLevel = PrivacyLevel.STANDARD
    dietary_restrictions: List[str] = []
    room_preferences: Dict[str, Any] = {}
    service_preferences: Dict[str, Any] = {}
    wellness_goals: List[str] = []

class UserUpdate(BaseModel):
    """User update model"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    preferred_ai_personality: Optional[str] = None
    preferred_language: Optional[str] = None
    accessibility_features: Optional[List[str]] = None
    privacy_level: Optional[PrivacyLevel] = None
    dietary_restrictions: Optional[List[str]] = None
    room_preferences: Optional[Dict[str, Any]] = None
    service_preferences: Optional[Dict[str, Any]] = None
    wellness_goals: Optional[List[str]] = None

class UserResponse(BaseModel):
    """User response model"""
    id: int
    email: str
    first_name: str
    last_name: str
    phone_number: Optional[str]
    preferred_ai_personality: str
    preferred_language: str
    accessibility_features: List[str]
    privacy_level: str
    dietary_restrictions: List[str]
    room_preferences: Dict[str, Any]
    service_preferences: Dict[str, Any]
    wellness_goals: List[str]
    biometric_enabled: bool
    voice_enabled: bool
    face_recognition_enabled: bool
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: Optional[datetime]
    last_login: Optional[datetime]
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    """User login model"""
    email: EmailStr
    password: str
    biometric_data: Optional[Dict[str, Any]] = None
    device_info: Optional[Dict[str, Any]] = None

class Token(BaseModel):
    """Token model"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

class TokenData(BaseModel):
    """Token data model"""
    user_id: Optional[int] = None
    email: Optional[str] = None
