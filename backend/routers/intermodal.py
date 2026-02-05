"""
Intermodal Concierge - Door-to-Door Routing
Provides multi-modal transportation recommendations
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List, Literal
from shared.security import jwt_verify
from shared.telemetry import telemetry
from shared.config import flags
from datetime import datetime, timedelta

router = APIRouter()


class IntermodalPlanRequest(BaseModel):
    """Request model for intermodal routing"""
    origin: str = Field(..., description="Starting location")
    arrival_time: str = Field(..., description="Desired arrival time (HH:MM)")
    priority: Literal["fast", "eco", "cheap"] = Field(..., description="Routing priority")


class RouteSegment(BaseModel):
    """Single segment of route"""
    mode: str
    eta: str
    duration_min: int
    co2_kg: float
    cost_estimate: float
    instructions: str


class IntermodalPlanResponse(BaseModel):
    """Response model for intermodal plan"""
    routes: List[RouteSegment]
    total_duration_min: int
    total_co2_kg: float
    total_cost: float
    recommended_departure: str


# Hard-coded transportation graph (deterministic)
TRANSPORT_OPTIONS = {
    "rideshare": {
        "speed_kmh": 40,
        "co2_per_km": 0.15,
        "cost_per_km": 2.5,
        "base_wait_min": 5
    },
    "taxi": {
        "speed_kmh": 40,
        "co2_per_km": 0.18,
        "cost_per_km": 3.0,
        "base_wait_min": 3
    },
    "scooter": {
        "speed_kmh": 25,
        "co2_per_km": 0.02,
        "cost_per_km": 0.5,
        "base_wait_min": 2
    },
    "bike": {
        "speed_kmh": 20,
        "co2_per_km": 0.0,
        "cost_per_km": 0.0,
        "base_wait_min": 1
    },
    "walk": {
        "speed_kmh": 5,
        "co2_per_km": 0.0,
        "cost_per_km": 0.0,
        "base_wait_min": 0
    },
    "subway": {
        "speed_kmh": 35,
        "co2_per_km": 0.05,
        "cost_per_km": 0.3,
        "base_wait_min": 5
    },
    "bus": {
        "speed_kmh": 25,
        "co2_per_km": 0.08,
        "cost_per_km": 0.2,
        "base_wait_min": 7
    }
}


def parse_time(time_str: str) -> datetime:
    """Parse HH:MM time string to today's datetime"""
    hour, minute = map(int, time_str.split(':'))
    now = datetime.now()
    return datetime(now.year, now.month, now.day, hour, minute)


def generate_route_options(
    origin: str,
    arrival_time: str,
    priority: str
) -> List[RouteSegment]:
    """
    Generate route options based on priority
    Deterministic routing over simplified graph
    """
    
    # Assume 8km distance for demo
    distance_km = 8.0
    
    routes = []
    
    if priority == "fast":
        # Fast: Rideshare direct
        mode = "rideshare"
        opt = TRANSPORT_OPTIONS[mode]
        duration = int((distance_km / opt["speed_kmh"]) * 60 + opt["base_wait_min"])
        co2 = distance_km * opt["co2_per_km"]
        cost = distance_km * opt["cost_per_km"]
        
        routes.append(RouteSegment(
            mode=mode,
            eta=arrival_time,
            duration_min=duration,
            co2_kg=round(co2, 2),
            cost_estimate=round(cost, 2),
            instructions=f"Request rideshare pickup at {origin}. Direct route to hotel."
        ))
        
    elif priority == "eco":
        # Eco: Combination of public transit + bike
        # Segment 1: Walk to subway (1km, 12min)
        walk_opt = TRANSPORT_OPTIONS["walk"]
        walk_duration = int((1.0 / walk_opt["speed_kmh"]) * 60)
        
        # Segment 2: Subway (6km, 15min including wait)
        subway_opt = TRANSPORT_OPTIONS["subway"]
        subway_duration = int((6.0 / subway_opt["speed_kmh"]) * 60 + subway_opt["base_wait_min"])
        subway_co2 = 6.0 * subway_opt["co2_per_km"]
        subway_cost = 6.0 * subway_opt["cost_per_km"]
        
        # Segment 3: Scooter last mile (1km, 4min)
        scooter_opt = TRANSPORT_OPTIONS["scooter"]
        scooter_duration = int((1.0 / scooter_opt["speed_kmh"]) * 60 + scooter_opt["base_wait_min"])
        scooter_co2 = 1.0 * scooter_opt["co2_per_km"]
        scooter_cost = 1.0 * scooter_opt["cost_per_km"]
        
        routes.extend([
            RouteSegment(
                mode="walk",
                eta="",
                duration_min=walk_duration,
                co2_kg=0.0,
                cost_estimate=0.0,
                instructions="Walk to nearest subway station (1km)"
            ),
            RouteSegment(
                mode="subway",
                eta="",
                duration_min=subway_duration,
                co2_kg=round(subway_co2, 2),
                cost_estimate=round(subway_cost, 2),
                instructions="Take Green Line subway to Downtown Station"
            ),
            RouteSegment(
                mode="scooter",
                eta=arrival_time,
                duration_min=scooter_duration,
                co2_kg=round(scooter_co2, 2),
                cost_estimate=round(scooter_cost, 2),
                instructions="Rent e-scooter for last mile to hotel"
            )
        ])
        
    elif priority == "cheap":
        # Cheap: Bus + walk
        # Segment 1: Walk to bus stop (0.5km, 6min)
        walk1_duration = int((0.5 / TRANSPORT_OPTIONS["walk"]["speed_kmh"]) * 60)
        
        # Segment 2: Bus (7km, 25min including wait)
        bus_opt = TRANSPORT_OPTIONS["bus"]
        bus_duration = int((7.0 / bus_opt["speed_kmh"]) * 60 + bus_opt["base_wait_min"])
        bus_co2 = 7.0 * bus_opt["co2_per_km"]
        bus_cost = 7.0 * bus_opt["cost_per_km"]
        
        # Segment 3: Walk to hotel (0.5km, 6min)
        walk2_duration = int((0.5 / TRANSPORT_OPTIONS["walk"]["speed_kmh"]) * 60)
        
        routes.extend([
            RouteSegment(
                mode="walk",
                eta="",
                duration_min=walk1_duration,
                co2_kg=0.0,
                cost_estimate=0.0,
                instructions="Walk to bus stop on Main Street"
            ),
            RouteSegment(
                mode="bus",
                eta="",
                duration_min=bus_duration,
                co2_kg=round(bus_co2, 2),
                cost_estimate=round(bus_cost, 2),
                instructions="Take Bus #42 toward Downtown (8 stops)"
            ),
            RouteSegment(
                mode="walk",
                eta=arrival_time,
                duration_min=walk2_duration,
                co2_kg=0.0,
                cost_estimate=0.0,
                instructions="Walk from bus stop to hotel entrance"
            )
        ])
    
    return routes


@router.post("/plan", response_model=IntermodalPlanResponse)
async def plan_intermodal_route(
    request: IntermodalPlanRequest,
    token_payload: dict = Depends(jwt_verify)
):
    """
    Plan door-to-door intermodal route
    
    Provides multi-modal transportation recommendations based on priority
    (fastest, most eco-friendly, or cheapest).
    """
    
    # Check feature flag
    if not flags.FEATURE_INTERMODAL:
        raise HTTPException(status_code=501, detail="Intermodal feature is not enabled")
    
    try:
        # Generate route segments
        routes = generate_route_options(
            origin=request.origin,
            arrival_time=request.arrival_time,
            priority=request.priority
        )
        
        # Calculate totals
        total_duration = sum(r.duration_min for r in routes)
        total_co2 = sum(r.co2_kg for r in routes)
        total_cost = sum(r.cost_estimate for r in routes)
        
        # Calculate recommended departure time
        arrival_dt = parse_time(request.arrival_time)
        departure_dt = arrival_dt - timedelta(minutes=total_duration)
        recommended_departure = departure_dt.strftime("%H:%M")
        
        response = IntermodalPlanResponse(
            routes=routes,
            total_duration_min=total_duration,
            total_co2_kg=round(total_co2, 2),
            total_cost=round(total_cost, 2),
            recommended_departure=recommended_departure
        )
        
        # Log telemetry
        telemetry({
            "event_type": "intermodal_plan",
            "user_id": token_payload.get("sub", "unknown"),
            "priority": request.priority,
            "segments": len(routes),
            "total_duration_min": total_duration,
            "total_co2_kg": total_co2,
            "metadata": {"feature": "intermodal"}
        })
        
        return response
        
    except Exception as e:
        # Log error
        telemetry({
            "event_type": "intermodal_error",
            "user_id": token_payload.get("sub", "unknown"),
            "error": str(e),
            "metadata": {"feature": "intermodal"}
        })
        raise HTTPException(status_code=500, detail=f"Route planning failed: {str(e)}")


