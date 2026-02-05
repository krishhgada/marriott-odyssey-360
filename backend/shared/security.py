"""
Enhanced security utilities for Marriott's Odyssey 360 AI
Includes PII redaction, allowlist, and JWT verification wrapper
"""

import re
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from core.security import verify_token
import os

security = HTTPBearer()

# Demo token for local testing
DEMO_TOKEN = os.getenv("DEMO_TOKEN", "demo-token-odyssey360")

# Allowlist for side-effecting actions
ALLOWED_ACTIONS = {
    "room.checkout",
    "room.environment",
    "offers.apply",
}


def redact(text: str) -> str:
    """
    Redact PII from text (emails and 12-16 digit sequences)
    
    Args:
        text: Input text potentially containing PII
        
    Returns:
        Text with PII redacted
        
    Examples:
        >>> redact("Contact user@example.com")
        'Contact us**@ex*****.com'
        >>> redact("Card: 1234567890123456")
        'Card: 1234********3456'
    """
    if not text:
        return text
    
    # Redact emails: show first 2 chars of username and first 2 of domain
    email_pattern = r'\b([a-zA-Z0-9._%+-]{2})[a-zA-Z0-9._%+-]*@([a-zA-Z0-9-]{2})[a-zA-Z0-9.-]*\.[a-zA-Z]{2,}\b'
    text = re.sub(email_pattern, r'\1**@\2*****.com', text)
    
    # Redact 12-16 digit sequences (credit cards, account numbers)
    # Show first 4 and last 4 digits
    digit_pattern = r'\b(\d{4})\d{4,8}(\d{4})\b'
    text = re.sub(digit_pattern, r'\1********\2', text)
    
    return text


def allowlist(action: str) -> bool:
    """
    Check if an action is in the allowlist
    
    Args:
        action: Action identifier (e.g., "room.checkout")
        
    Returns:
        True if action is allowed, False otherwise
    """
    return action in ALLOWED_ACTIONS


async def jwt_verify(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    FastAPI dependency for JWT verification
    Supports demo token for local testing
    
    Args:
        credentials: Bearer token from request header
        
    Returns:
        JWT payload dict
        
    Raises:
        HTTPException: If token is invalid or missing
    """
    # Check for demo token in development
    if credentials.credentials == DEMO_TOKEN:
        return {
            "sub": "demo-user",
            "email": "demo@marriott.com",
            "demo_mode": True
        }
    
    # Use existing JWT verification from core.security
    try:
        payload = verify_token(credentials)
        return payload
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token verification failed: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


def require_allowlist(action: str):
    """
    Decorator/dependency to require allowlist permission for an action
    
    Usage:
        @router.post("/checkout")
        async def checkout(allowed: bool = Depends(require_allowlist("room.checkout"))):
            if not allowed:
                raise HTTPException(403, "Action not permitted")
    """
    def _check():
        if not allowlist(action):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Action '{action}' is not in the allowlist"
            )
        return True
    return _check


