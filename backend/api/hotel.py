"""
Hotel Services API endpoints for Marriott's Odyssey 360 AI
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional, Dict, Any, List
from datetime import datetime
from models.user import User
from core.security import get_current_user

router = APIRouter()

@router.get("/room/status")
async def get_room_status(current_user: User = Depends(get_current_user)):
    """Get current room status and controls"""
    return {
        "success": True,
        "room_status": {
            "room_number": "1205",
            "floor": 12,
            "temperature": 72,
            "lighting": "dim",
            "curtains": "closed",
            "tv_status": "off",
            "music_playing": False,
            "do_not_disturb": False,
            "housekeeping_status": "clean",
            "amenities": [
                "minibar", "coffee_maker", "safe", "iron", "hairdryer"
            ]
        }
    }

@router.post("/room/control")
async def control_room(
    control_type: str,
    value: Any,
    current_user: User = Depends(get_current_user)
):
    """Control room settings"""
    return {
        "success": True,
        "message": f"Room {control_type} set to {value}",
        "updated_at": datetime.now().isoformat()
    }

@router.get("/services/room-service")
async def get_room_service_menu(current_user: User = Depends(get_current_user)):
    """Get room service menu"""
    return {
        "success": True,
        "menu": {
            "breakfast": [
                {"id": 1, "name": "Continental Breakfast", "price": 18.99, "description": "Fresh pastries, fruits, and coffee"},
                {"id": 2, "name": "American Breakfast", "price": 24.99, "description": "Eggs, bacon, toast, and coffee"},
                {"id": 3, "name": "Healthy Start", "price": 16.99, "description": "Greek yogurt, granola, and fresh berries"}
            ],
            "lunch": [
                {"id": 4, "name": "Caesar Salad", "price": 14.99, "description": "Fresh romaine, parmesan, croutons"},
                {"id": 5, "name": "Club Sandwich", "price": 16.99, "description": "Turkey, bacon, lettuce, tomato"},
                {"id": 6, "name": "Quinoa Bowl", "price": 18.99, "description": "Quinoa, vegetables, tahini dressing"}
            ],
            "dinner": [
                {"id": 7, "name": "Grilled Salmon", "price": 28.99, "description": "Atlantic salmon with seasonal vegetables"},
                {"id": 8, "name": "Ribeye Steak", "price": 34.99, "description": "12oz ribeye with mashed potatoes"},
                {"id": 9, "name": "Vegetarian Pasta", "price": 22.99, "description": "Penne with seasonal vegetables and marinara"}
            ],
            "beverages": [
                {"id": 10, "name": "Coffee", "price": 3.99, "description": "Freshly brewed coffee"},
                {"id": 11, "name": "Fresh Juice", "price": 4.99, "description": "Orange, apple, or cranberry"},
                {"id": 12, "name": "Wine Selection", "price": 12.99, "description": "Red or white wine by the glass"}
            ]
        }
    }

@router.post("/services/room-service/order")
async def place_room_service_order(
    order_items: List[Dict[str, Any]],
    current_user: User = Depends(get_current_user)
):
    """Place room service order"""
    return {
        "success": True,
        "order_id": "RS-2024-001",
        "estimated_delivery": "30 minutes",
        "total_amount": 45.97,
        "order_items": order_items,
        "status": "confirmed"
    }

@router.get("/services/housekeeping")
async def get_housekeeping_services(current_user: User = Depends(get_current_user)):
    """Get available housekeeping services"""
    return {
        "success": True,
        "services": [
            {
                "id": "hk-1",
                "name": "Daily Housekeeping",
                "description": "Full room cleaning and tidying",
                "duration": "30 minutes",
                "available_times": ["9:00 AM", "2:00 PM", "5:00 PM"]
            },
            {
                "id": "hk-2",
                "name": "Turndown Service",
                "description": "Evening turndown with chocolates",
                "duration": "15 minutes",
                "available_times": ["6:00 PM", "7:00 PM", "8:00 PM"]
            },
            {
                "id": "hk-3",
                "name": "Express Service",
                "description": "Quick refresh and amenity restock",
                "duration": "15 minutes",
                "available_times": ["Anytime"]
            }
        ]
    }

@router.post("/services/housekeeping/schedule")
async def schedule_housekeeping(
    service_id: str,
    preferred_time: str,
    special_requests: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """Schedule housekeeping service"""
    return {
        "success": True,
        "service_id": service_id,
        "scheduled_time": preferred_time,
        "special_requests": special_requests,
        "confirmation": "Service scheduled successfully"
    }

@router.get("/amenities")
async def get_available_amenities(current_user: User = Depends(get_current_user)):
    """Get available room amenities"""
    return {
        "success": True,
        "amenities": [
            {"id": "am-1", "name": "Extra Towels", "available": True},
            {"id": "am-2", "name": "Pillow Selection", "available": True},
            {"id": "am-3", "name": "Coffee Pods", "available": True},
            {"id": "am-4", "name": "Bathrobes", "available": True},
            {"id": "am-5", "name": "Slippers", "available": True},
            {"id": "am-6", "name": "Toiletries", "available": True}
        ]
    }

@router.post("/amenities/request")
async def request_amenities(
    amenity_ids: List[str],
    current_user: User = Depends(get_current_user)
):
    """Request room amenities"""
    return {
        "success": True,
        "requested_amenities": amenity_ids,
        "estimated_delivery": "15 minutes",
        "status": "processing"
    }
