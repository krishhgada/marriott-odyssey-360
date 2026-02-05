"""
Wellness & Safety API endpoints for Marriott's Odyssey 360 AI
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional, Dict, Any, List
from datetime import datetime
from models.user import User
from core.security import get_current_user

router = APIRouter()

@router.get("/spa/services")
async def get_spa_services(current_user: User = Depends(get_current_user)):
    """Get available spa services"""
    return {
        "success": True,
        "spa_services": [
            {
                "id": "spa-1",
                "name": "Deep Tissue Massage",
                "description": "Therapeutic massage for muscle tension relief",
                "duration": "60 minutes",
                "price": 120.00,
                "available_times": ["10:00 AM", "2:00 PM", "4:00 PM"]
            },
            {
                "id": "spa-2",
                "name": "Facial Treatment",
                "description": "Rejuvenating facial with premium products",
                "duration": "75 minutes",
                "price": 95.00,
                "available_times": ["9:00 AM", "1:00 PM", "3:00 PM"]
            },
            {
                "id": "spa-3",
                "name": "Aromatherapy Session",
                "description": "Relaxing aromatherapy with essential oils",
                "duration": "45 minutes",
                "price": 80.00,
                "available_times": ["11:00 AM", "3:00 PM", "5:00 PM"]
            }
        ]
    }

@router.post("/spa/book")
async def book_spa_service(
    service_id: str,
    preferred_time: str,
    special_requests: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """Book spa service"""
    return {
        "success": True,
        "booking_id": "SPA-2024-001",
        "service_id": service_id,
        "scheduled_time": preferred_time,
        "special_requests": special_requests,
        "confirmation": "Spa service booked successfully"
    }

@router.get("/fitness/classes")
async def get_fitness_classes(current_user: User = Depends(get_current_user)):
    """Get available fitness classes"""
    return {
        "success": True,
        "fitness_classes": [
            {
                "id": "fit-1",
                "name": "Morning Yoga",
                "description": "Gentle yoga flow to start your day",
                "duration": "45 minutes",
                "time": "7:00 AM",
                "instructor": "Sarah Johnson",
                "difficulty": "Beginner"
            },
            {
                "id": "fit-2",
                "name": "HIIT Workout",
                "description": "High-intensity interval training",
                "duration": "30 minutes",
                "time": "6:00 PM",
                "instructor": "Mike Chen",
                "difficulty": "Advanced"
            },
            {
                "id": "fit-3",
                "name": "Meditation Session",
                "description": "Guided meditation for relaxation",
                "duration": "20 minutes",
                "time": "8:00 PM",
                "instructor": "Lisa Park",
                "difficulty": "All Levels"
            }
        ]
    }

@router.post("/fitness/register")
async def register_fitness_class(
    class_id: str,
    current_user: User = Depends(get_current_user)
):
    """Register for fitness class"""
    return {
        "success": True,
        "class_id": class_id,
        "registration_id": "FIT-2024-001",
        "confirmation": "Successfully registered for fitness class"
    }

@router.get("/wellness/monitoring")
async def get_wellness_monitoring(current_user: User = Depends(get_current_user)):
    """Get wellness monitoring data"""
    return {
        "success": True,
        "wellness_data": {
            "air_quality": {
                "pm2_5": 12,
                "pm10": 18,
                "co2": 420,
                "temperature": 72,
                "humidity": 45,
                "status": "excellent"
            },
            "sleep_quality": {
                "last_night_score": 8.5,
                "sleep_duration": "7h 32m",
                "deep_sleep": "2h 15m",
                "rem_sleep": "1h 45m",
                "recommendations": ["Maintain consistent sleep schedule", "Reduce screen time before bed"]
            },
            "stress_level": {
                "current_level": 3,
                "scale": "1-10",
                "trend": "decreasing",
                "recommendations": ["Try meditation", "Take a walk", "Schedule spa treatment"]
            }
        }
    }

@router.get("/safety/alerts")
async def get_safety_alerts(current_user: User = Depends(get_current_user)):
    """Get safety alerts and information"""
    return {
        "success": True,
        "safety_alerts": [
            {
                "id": "alert-1",
                "type": "weather",
                "severity": "moderate",
                "message": "Rain expected this afternoon. Umbrellas available at concierge.",
                "timestamp": "2024-01-01T10:00:00Z"
            },
            {
                "id": "alert-2",
                "type": "maintenance",
                "severity": "low",
                "message": "Elevator maintenance scheduled for tomorrow 2-4 PM.",
                "timestamp": "2024-01-01T09:30:00Z"
            }
        ]
    }

@router.post("/safety/emergency")
async def report_emergency(
    emergency_type: str,
    description: str,
    location: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """Report emergency situation"""
    return {
        "success": True,
        "emergency_id": "EMG-2024-001",
        "type": emergency_type,
        "description": description,
        "location": location or "Room 1205",
        "status": "reported",
        "response_time": "immediate",
        "message": "Emergency services have been notified"
    }

@router.get("/nutrition/menu")
async def get_nutrition_menu(current_user: User = Depends(get_current_user)):
    """Get nutrition-focused menu options"""
    return {
        "success": True,
        "nutrition_menu": {
            "healthy_breakfast": [
                {"name": "Acai Bowl", "calories": 320, "protein": 8, "fiber": 12},
                {"name": "Avocado Toast", "calories": 280, "protein": 12, "fiber": 8},
                {"name": "Greek Yogurt Parfait", "calories": 250, "protein": 15, "fiber": 6}
            ],
            "low_carb_lunch": [
                {"name": "Grilled Chicken Salad", "calories": 180, "protein": 25, "carbs": 8},
                {"name": "Cauliflower Rice Bowl", "calories": 220, "protein": 18, "carbs": 12},
                {"name": "Zucchini Noodles", "calories": 160, "protein": 12, "carbs": 6}
            ],
            "protein_dinner": [
                {"name": "Grilled Salmon", "calories": 350, "protein": 35, "fat": 18},
                {"name": "Lean Beef Steak", "calories": 280, "protein": 28, "fat": 12},
                {"name": "Tofu Stir Fry", "calories": 240, "protein": 20, "fat": 8}
            ]
        }
    }
