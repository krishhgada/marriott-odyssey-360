"""
TrustLens - Content Authenticity Checker
Mock implementation for verifying image authenticity using deterministic heuristics
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
import re
import hashlib
from shared.security import jwt_verify
from shared.telemetry import telemetry
from shared.config import flags

router = APIRouter()


class TrustCheckRequest(BaseModel):
    """Request model for trust/authenticity check"""
    image_url: Optional[str] = Field(None, description="URL of image to check")
    base64: Optional[str] = Field(None, description="Base64-encoded image data")
    metadata: Dict = Field(default={}, description="Image metadata (EXIF, etc.)")
    filename: Optional[str] = Field(None, description="Original filename")


class TrustCheckResponse(BaseModel):
    """Response model for trust check"""
    trust_score: int = Field(..., ge=0, le=100, description="Trust score (0-100)")
    risks: List[str]
    remediation: List[str]
    details: Dict


def calculate_trust_score(
    image_url: Optional[str],
    base64_data: Optional[str],
    metadata: Dict,
    filename: Optional[str]
) -> TrustCheckResponse:
    """
    Calculate trust score based on various heuristics
    This is a deterministic mock implementation
    """
    
    score = 100  # Start with perfect score
    risks = []
    remediation = []
    details = {}
    
    # Check 1: EXIF metadata presence
    if not metadata or len(metadata) == 0:
        score -= 20
        risks.append("Missing EXIF metadata - cannot verify source")
        remediation.append("Request original image with metadata intact")
        details["exif_present"] = False
    else:
        details["exif_present"] = True
        
        # Check for camera info
        if "camera" in metadata or "device" in metadata:
            details["camera_info"] = True
        else:
            score -= 10
            risks.append("No camera/device information in metadata")
            remediation.append("Verify image source device")
    
    # Check 2: Filename analysis
    if filename:
        # Check for stock photo patterns
        stock_patterns = [
            r'shutterstock',
            r'getty',
            r'istockphoto',
            r'stock-photo',
            r'unsplash',
            r'pexels'
        ]
        
        for pattern in stock_patterns:
            if re.search(pattern, filename.lower()):
                score -= 15
                risks.append(f"Filename suggests stock/downloaded image: {pattern}")
                remediation.append("Verify if stock image is appropriate for use case")
                details["stock_image_detected"] = True
                break
        
        # Check for generic names
        if re.match(r'^(image|img|photo|picture)\d*\.(jpg|png)$', filename.lower()):
            score -= 5
            risks.append("Generic filename - may indicate processing or editing")
            details["generic_filename"] = True
    
    # Check 3: URL analysis (if provided)
    if image_url:
        # Check for suspicious domains
        suspicious_domains = ['imgur', 'tinypic', 'postimg', 'imgbb']
        if any(domain in image_url.lower() for domain in suspicious_domains):
            score -= 10
            risks.append("Image hosted on third-party service - origin unclear")
            remediation.append("Request original source or direct upload")
            details["third_party_host"] = True
        
        # Check for HTTPS
        if not image_url.startswith('https://'):
            score -= 5
            risks.append("Non-HTTPS URL - connection not secure")
            remediation.append("Use secure HTTPS connection")
            details["secure_connection"] = False
        else:
            details["secure_connection"] = True
    
    # Check 4: Simulate Laplacian variance (blur detection)
    # In reality, this would analyze actual image data
    # For demo, we'll use a deterministic value based on input hash
    if base64_data:
        data_hash = hashlib.md5(base64_data[:100].encode()).hexdigest()
        variance = int(data_hash[:4], 16) % 200  # 0-199
        
        if variance < 50:
            score -= 15
            risks.append("Image appears blurry or low quality")
            remediation.append("Request higher resolution image")
            details["blur_detected"] = True
        else:
            details["image_sharpness"] = "acceptable"
    
    # Check 5: Metadata consistency
    if metadata:
        # Check for creation vs modification date
        if "created" in metadata and "modified" in metadata:
            # In real implementation, would compare actual dates
            # For demo, just check if both exist
            details["date_consistency"] = True
        else:
            score -= 5
            risks.append("Incomplete date information in metadata")
    
    # Check 6: Watermark detection (simple filename check)
    if filename and ('watermark' in filename.lower() or 'wm' in filename.lower()):
        score += 10  # Watermark is actually good for authenticity
        details["watermark_present"] = True
    
    # Ensure score stays in valid range
    score = max(0, min(100, score))
    
    # Add general recommendations based on score
    if score >= 80:
        remediation.insert(0, "✅ Image appears trustworthy")
    elif score >= 60:
        remediation.insert(0, "⚠️ Use caution - verify source before using")
    else:
        remediation.insert(0, "❌ High risk - additional verification strongly recommended")
    
    # Add risk-free message if no risks
    if not risks:
        risks.append("No significant authenticity concerns detected")
    
    return TrustCheckResponse(
        trust_score=score,
        risks=risks,
        remediation=remediation,
        details=details
    )


@router.post("/check_image", response_model=TrustCheckResponse)
async def check_image_authenticity(
    request: TrustCheckRequest,
    token_payload: dict = Depends(jwt_verify)
):
    """
    Check image authenticity and provide trust score
    
    Analyzes image metadata, filename, URL, and simulated image properties
    to provide a trust score and recommendations.
    """
    
    # Check feature flag
    if not flags.FEATURE_TRUSTLENS:
        raise HTTPException(status_code=501, detail="TrustLens feature is not enabled")
    
    # Validate input
    if not request.image_url and not request.base64:
        raise HTTPException(
            status_code=400,
            detail="Either image_url or base64 data must be provided"
        )
    
    try:
        # Calculate trust score
        result = calculate_trust_score(
            image_url=request.image_url,
            base64_data=request.base64,
            metadata=request.metadata,
            filename=request.filename
        )
        
        # Log telemetry
        telemetry({
            "event_type": "trustlens_check",
            "user_id": token_payload.get("sub", "unknown"),
            "trust_score": result.trust_score,
            "risk_count": len(result.risks),
            "has_url": request.image_url is not None,
            "has_metadata": len(request.metadata) > 0,
            "metadata": {"feature": "trustlens"}
        })
        
        return result
        
    except Exception as e:
        # Log error
        telemetry({
            "event_type": "trustlens_error",
            "user_id": token_payload.get("sub", "unknown"),
            "error": str(e),
            "metadata": {"feature": "trustlens"}
        })
        raise HTTPException(status_code=500, detail=f"Trust check failed: {str(e)}")


