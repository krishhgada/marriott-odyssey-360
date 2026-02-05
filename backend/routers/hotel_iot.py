"""
Hotel & IoT Control Extensions
Extended room control and housekeeping features
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Literal, Optional
from shared.security import jwt_verify, allowlist
from shared.telemetry import telemetry
from shared.config import flags

router = APIRouter()


class RoomEnvironmentRequest(BaseModel):
    """Request to control room environment"""
    room: str
    lights: Optional[Literal["on", "off", "dim"]] = None
    ac_temp: Optional[int] = Field(None, ge=60, le=85)
    sound: Optional[Literal["off", "white_noise", "nature"]] = None


class HousekeepingRequest(BaseModel):
    """Request for housekeeping services"""
    room: str
    request: Literal["towels", "turn_down", "clean", "amenities"]


class CheckoutRequest(BaseModel):
    """Express checkout request"""
    room: str
    email: str


class ThermostatRequest(BaseModel):
    """Thermostat control request"""
    room: str
    target_temp: int = Field(..., ge=60, le=85)


class SuccessResponse(BaseModel):
    """Generic success response"""
    success: bool
    message: str


@router.post("/environment", response_model=SuccessResponse)
async def control_room_environment(
    request: RoomEnvironmentRequest,
    token_payload: dict = Depends(jwt_verify)
):
    """
    Control room environment (lights, AC, sound)
    """
    
    # Check allowlist
    if not allowlist("room.environment"):
        raise HTTPException(status_code=403, detail="Action not permitted by allowlist")
    
    try:
        actions = []
        if request.lights:
            actions.append(f"lights set to {request.lights}")
        if request.ac_temp:
            actions.append(f"AC temperature set to {request.ac_temp}°F")
        if request.sound:
            actions.append(f"sound set to {request.sound}")
        
        message = f"Room {request.room}: {', '.join(actions)}"
        
        telemetry({
            "event_type": "room_environment",
            "user_id": token_payload.get("sub", "unknown"),
            "room": request.room,
            "actions": actions,
            "metadata": {"feature": "hotel_iot"}
        })
        
        return SuccessResponse(success=True, message=message)
        
    except Exception as e:
        telemetry({
            "event_type": "room_environment_error",
            "user_id": token_payload.get("sub", "unknown"),
            "error": str(e),
            "metadata": {"feature": "hotel_iot"}
        })
        raise HTTPException(status_code=500, detail=f"Environment control failed: {str(e)}")


@router.post("/housekeeping", response_model=SuccessResponse)
async def request_housekeeping(
    request: HousekeepingRequest,
    token_payload: dict = Depends(jwt_verify)
):
    """
    Request housekeeping services
    """
    
    try:
        service_names = {
            "towels": "fresh towels",
            "turn_down": "turndown service",
            "clean": "room cleaning",
            "amenities": "bathroom amenities"
        }
        
        service = service_names.get(request.request, request.request)
        message = f"Housekeeping request for {service} sent to room {request.room}"
        
        telemetry({
            "event_type": "housekeeping_request",
            "user_id": token_payload.get("sub", "unknown"),
            "room": request.room,
            "service": request.request,
            "metadata": {"feature": "hotel_iot"}
        })
        
        return SuccessResponse(success=True, message=message)
        
    except Exception as e:
        telemetry({
            "event_type": "housekeeping_error",
            "user_id": token_payload.get("sub", "unknown"),
            "error": str(e),
            "metadata": {"feature": "hotel_iot"}
        })
        raise HTTPException(status_code=500, detail=f"Housekeeping request failed: {str(e)}")


@router.post("/checkout", response_model=SuccessResponse)
async def express_checkout(
    request: CheckoutRequest,
    token_payload: dict = Depends(jwt_verify)
):
    """
    Express checkout (email receipt)
    """
    
    # Check allowlist
    if not allowlist("room.checkout"):
        raise HTTPException(status_code=403, detail="Action not permitted by allowlist")
    
    try:
        from shared.security import redact
        
        redacted_email = redact(request.email)
        message = f"Express checkout completed for room {request.room}. Receipt sent to {redacted_email}"
        
        telemetry({
            "event_type": "express_checkout",
            "user_id": token_payload.get("sub", "unknown"),
            "room": request.room,
            "metadata": {"feature": "hotel_iot"}
        })
        
        return SuccessResponse(success=True, message=message)
        
    except Exception as e:
        telemetry({
            "event_type": "checkout_error",
            "user_id": token_payload.get("sub", "unknown"),
            "error": str(e),
            "metadata": {"feature": "hotel_iot"}
        })
        raise HTTPException(status_code=500, detail=f"Checkout failed: {str(e)}")


@router.post("/thermostat", response_model=SuccessResponse)
async def control_thermostat(
    request: ThermostatRequest,
    token_payload: dict = Depends(jwt_verify)
):
    """
    Control room thermostat
    """
    
    try:
        message = f"Room {request.room} thermostat set to {request.target_temp}°F"
        
        telemetry({
            "event_type": "thermostat_control",
            "user_id": token_payload.get("sub", "unknown"),
            "room": request.room,
            "target_temp": request.target_temp,
            "metadata": {"feature": "hotel_iot"}
        })
        
        return SuccessResponse(success=True, message=message)
        
    except Exception as e:
        telemetry({
            "event_type": "thermostat_error",
            "user_id": token_payload.get("sub", "unknown"),
            "error": str(e),
            "metadata": {"feature": "hotel_iot"}
        })
        raise HTTPException(status_code=500, detail=f"Thermostat control failed: {str(e)}")


