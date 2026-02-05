"""
Targeted Offer Generation
Cross-feature personalized offers
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from shared.security import jwt_verify, allowlist
from shared.telemetry import telemetry
from shared.config import flags

router = APIRouter()


class OfferApplyRequest(BaseModel):
    """Request to apply an offer"""
    guest_id: str
    offer_id: str


class OfferApplyResponse(BaseModel):
    """Response after applying offer"""
    success: bool
    message: str
    applied_offer: str


@router.post("/apply", response_model=OfferApplyResponse)
async def apply_offer(
    request: OfferApplyRequest,
    token_payload: dict = Depends(jwt_verify)
):
    """
    Apply a personalized offer
    """
    
    # Check allowlist
    if not allowlist("offers.apply"):
        raise HTTPException(status_code=403, detail="Action not permitted by allowlist")
    
    try:
        # Map offer IDs to descriptions
        offers = {
            "SUITE_UPGRADE_WINE": "Suite upgrade with complimentary wine",
            "SPA_DISCOUNT_50": "50% off spa services",
            "LATE_CHECKOUT_FREE": "Complimentary late checkout",
            "DINING_CREDIT_100": "$100 dining credit",
            "WELCOME_AMENITY": "Premium welcome amenity"
        }
        
        offer_desc = offers.get(request.offer_id, "Special offer")
        message = f"Offer '{offer_desc}' successfully applied for guest {request.guest_id}"
        
        telemetry({
            "event_type": "offer_applied",
            "user_id": token_payload.get("sub", "unknown"),
            "guest_id": request.guest_id,
            "offer_id": request.offer_id,
            "metadata": {"feature": "offers"}
        })
        
        return OfferApplyResponse(
            success=True,
            message=message,
            applied_offer=offer_desc
        )
        
    except Exception as e:
        telemetry({
            "event_type": "offer_error",
            "user_id": token_payload.get("sub", "unknown"),
            "error": str(e),
            "metadata": {"feature": "offers"}
        })
        raise HTTPException(status_code=500, detail=f"Offer application failed: {str(e)}")


