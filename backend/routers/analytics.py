"""
Analytics & Metrics Dashboard
Provides system telemetry and usage statistics
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Dict, List, Any
from shared.security import jwt_verify
from shared.telemetry import get_metrics

router = APIRouter()


class MetricsResponse(BaseModel):
    """Response model for metrics"""
    counters: Dict[str, int]
    recent_events: List[Dict[str, Any]]
    total_events: int
    csv_path: str


@router.get("/metrics", response_model=MetricsResponse)
async def get_system_metrics(token_payload: dict = Depends(jwt_verify)):
    """
    Get system metrics and telemetry data
    
    Returns event counts, recent events, and telemetry file path.
    """
    
    metrics = get_metrics()
    
    return MetricsResponse(
        counters=metrics["counters"],
        recent_events=metrics["recent_events"],
        total_events=metrics["total_events"],
        csv_path=metrics["csv_path"]
    )


