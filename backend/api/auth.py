"""
Authentication API endpoints for Marriott's Odyssey 360 AI
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

from models.user import User, UserCreate, UserLogin, Token, UserResponse
from core.config import settings

router = APIRouter()
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Mock user database for demo purposes
demo_users = {
    "demo@marriott.com": {
        "id": 1,
        "email": "demo@marriott.com",
        "hashed_password": pwd_context.hash("demo123"),
        "first_name": "John",
        "last_name": "Doe",
        "preferred_ai_personality": "friendly",
        "preferred_language": "en",
        "accessibility_features": ["voice_control", "high_contrast"],
        "privacy_level": "standard",
        "is_active": True,
        "is_verified": True
    }
}

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Verify JWT token"""
    try:
        payload = jwt.decode(credentials.credentials, settings.secret_key, algorithms=[settings.algorithm])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Get current authenticated user"""
    payload = verify_token(credentials)
    user_id = payload.get("sub")
    
    # Find user in demo database
    for email, user_data in demo_users.items():
        if user_data["id"] == user_id:
            return User(**user_data)
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User not found",
        headers={"WWW-Authenticate": "Bearer"},
    )

@router.post("/register", response_model=UserResponse)
async def register_user(user_data: UserCreate):
    """Register a new user"""
    try:
        # Check if user already exists
        if user_data.email in demo_users:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        user_id = max([u["id"] for u in demo_users.values()]) + 1
        hashed_password = get_password_hash(user_data.password)
        
        new_user = {
            "id": user_id,
            "email": user_data.email,
            "hashed_password": hashed_password,
            "first_name": user_data.first_name,
            "last_name": user_data.last_name,
            "phone_number": user_data.phone_number,
            "preferred_ai_personality": user_data.preferred_ai_personality,
            "preferred_language": user_data.preferred_language,
            "accessibility_features": user_data.accessibility_features,
            "privacy_level": user_data.privacy_level.value,
            "dietary_restrictions": user_data.dietary_restrictions,
            "room_preferences": user_data.room_preferences,
            "service_preferences": user_data.service_preferences,
            "wellness_goals": user_data.wellness_goals,
            "biometric_enabled": False,
            "voice_enabled": False,
            "face_recognition_enabled": False,
            "is_active": True,
            "is_verified": True,  # Auto-verify for demo
            "created_at": datetime.now(),
            "updated_at": None,
            "last_login": None
        }
        
        demo_users[user_data.email] = new_user
        
        return UserResponse(**new_user)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error registering user: {str(e)}"
        )

@router.post("/login", response_model=Token)
async def login_user(login_data: UserLogin):
    """Login user and return access token"""
    try:
        # Check if user exists
        if login_data.email not in demo_users:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        user_data = demo_users[login_data.email]
        
        # Verify password
        if not verify_password(login_data.password, user_data["hashed_password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Check if user is active
        if not user_data["is_active"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Account is deactivated"
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": user_data["id"]}, expires_delta=access_token_expires
        )
        
        # Create refresh token
        refresh_token_expires = timedelta(days=settings.refresh_token_expire_days)
        refresh_token = create_access_token(
            data={"sub": user_data["id"], "type": "refresh"}, expires_delta=refresh_token_expires
        )
        
        # Update last login
        demo_users[login_data.email]["last_login"] = datetime.now()
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.access_token_expire_minutes * 60
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during login: {str(e)}"
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return current_user

@router.post("/refresh", response_model=Token)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Refresh access token"""
    try:
        payload = verify_token(credentials)
        user_id = payload.get("sub")
        token_type = payload.get("type")
        
        if token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        
        # Find user
        user_data = None
        for email, data in demo_users.items():
            if data["id"] == user_id:
                user_data = data
                break
        
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        # Create new access token
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": user_data["id"]}, expires_delta=access_token_expires
        )
        
        return Token(
            access_token=access_token,
            refresh_token=credentials.credentials,  # Keep same refresh token
            token_type="bearer",
            expires_in=settings.access_token_expire_minutes * 60
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error refreshing token: {str(e)}"
        )

@router.post("/logout")
async def logout_user(current_user: User = Depends(get_current_user)):
    """Logout user (invalidate token)"""
    # In a real implementation, you would add the token to a blacklist
    # For demo purposes, we'll just return success
    return {
        "success": True,
        "message": "Successfully logged out"
    }
