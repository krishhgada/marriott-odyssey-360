"""
Cultural Inclusion & Accessibility Adapter
Provides culturally appropriate and accessible content recommendations
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from shared.security import jwt_verify
from shared.telemetry import telemetry
from shared.config import flags

router = APIRouter()


class CultureAdaptRequest(BaseModel):
    """Request model for cultural adaptation"""
    language_pref: str = Field(..., description="Preferred language (e.g., 'en', 'es', 'fr')")
    dietary: List[str] = Field(default=[], description="Dietary restrictions (e.g., ['veg', 'halal'])")
    accessibility: List[str] = Field(default=[], description="Accessibility needs (e.g., ['wheelchair', 'low_vision'])")


class CultureAdaptResponse(BaseModel):
    """Response model for cultural adaptation"""
    greetings_text: str
    menu_highlights: List[str]
    room_notes: List[str]
    accessibility_hints: List[str]
    alt_text_samples: List[str]


# Curated content database
GREETINGS = {
    "en": "Welcome! We're delighted to have you with us.",
    "es": "¡Bienvenido! Estamos encantados de tenerlo con nosotros.",
    "fr": "Bienvenue! Nous sommes ravis de vous accueillir.",
    "de": "Willkommen! Wir freuen uns, Sie bei uns zu haben.",
    "it": "Benvenuto! Siamo lieti di averla con noi.",
    "pt": "Bem-vindo! Estamos felizes em tê-lo conosco.",
    "zh": "欢迎! 我们很高兴您能与我们在一起。",
    "ja": "ようこそ！お越しいただき誠にありがとうございます。",
    "ko": "환영합니다! 함께 해주셔서 기쁩니다.",
    "ar": "مرحبا! يسعدنا أن نكون معكم.",
    "hi": "स्वागत है! हमें आपके साथ पाकर खुशी हो रही है।",
}

DIETARY_MENUS = {
    "veg": [
        "Grilled Vegetable Platter with Quinoa",
        "Mediterranean Chickpea Salad",
        "Mushroom Risotto with Truffle Oil",
        "Roasted Butternut Squash Soup"
    ],
    "vegetarian": [
        "Grilled Vegetable Platter with Quinoa",
        "Mediterranean Chickpea Salad",
        "Mushroom Risotto with Truffle Oil",
        "Roasted Butternut Squash Soup"
    ],
    "vegan": [
        "Plant-Based Buddha Bowl",
        "Vegan Thai Green Curry",
        "Quinoa-Stuffed Bell Peppers",
        "Raw Zucchini Noodles with Cashew Cream"
    ],
    "halal": [
        "Halal-Certified Lamb Tagine",
        "Grilled Halal Chicken Kebab",
        "Moroccan Couscous with Vegetables",
        "Beef Shawarma Platter (Halal)"
    ],
    "kosher": [
        "Kosher Herb-Crusted Salmon",
        "Matzo Ball Soup",
        "Kosher Beef Brisket",
        "Israeli Salad with Tahini"
    ],
    "allergen_nuts": [
        "Nut-Free Grilled Chicken Breast",
        "Nut-Free Pasta Primavera",
        "Nut-Free Chocolate Cake",
        "Plain Rice and Steamed Vegetables"
    ],
    "allergen_gluten": [
        "Gluten-Free Pizza with Fresh Vegetables",
        "Grilled Fish with Rice and Asparagus",
        "Gluten-Free Pasta with Marinara",
        "Rice Noodle Stir-Fry"
    ],
    "allergen_dairy": [
        "Dairy-Free Coconut Curry",
        "Grilled Steak with Herb Potatoes",
        "Dairy-Free Sorbet Selection",
        "Rice Pilaf with Vegetables"
    ]
}

ROOM_NOTES = {
    "default": [
        "Climate control via tablet on nightstand",
        "Smart lighting with voice commands",
        "Mini-bar restocked daily"
    ],
    "wheelchair": [
        "Lowered light switches and thermostat (36 inches from floor)",
        "Roll-in shower with grab bars and shower seat",
        "Accessible desk height and furniture placement",
        "Emergency pull cord in bathroom"
    ],
    "low_vision": [
        "High-contrast room signage and labels",
        "Tactile room number on door",
        "Voice-activated room controls available",
        "Braille labels on key surfaces"
    ],
    "hearing": [
        "Visual fire alarm and doorbell indicators",
        "Closed-captioning on TV",
        "Text-based room service ordering",
        "Vibrating alarm clock available"
    ]
}

ACCESSIBILITY_HINTS = {
    "wheelchair": [
        "All public areas are wheelchair accessible",
        "Accessible van service available at valet",
        "Pool lift available (notify staff 1 hour in advance)",
        "Accessible paths marked with blue wayfinding"
    ],
    "low_vision": [
        "High-contrast wayfinding throughout property",
        "Audio elevator announcements",
        "Tactile maps at main entrances",
        "Staff trained in sighted guide technique"
    ],
    "hearing": [
        "Visual paging system in public areas",
        "ASL interpreters available (48 hours notice)",
        "All announcements displayed on lobby screens",
        "Hearing loop installed in conference rooms"
    ],
    "mobility": [
        "Accessible parking in covered garage (spots 1-8)",
        "Ramps with handrails at all entrances",
        "Accessible seating in restaurant (request via app)",
        "Elevators have audio and visual floor indicators"
    ]
}

ALT_TEXT_SAMPLES = [
    "Hotel exterior: Modern 20-story glass building with palm trees lining the entrance",
    "Lobby: Spacious open area with marble floors, contemporary art, and floor-to-ceiling windows",
    "Guest room: King bed with white linens, wooden desk, and city view through large window",
    "Pool area: Infinity pool on rooftop with lounge chairs and downtown skyline view",
    "Restaurant: Elegant dining room with warm lighting, white tablecloths, and open kitchen",
]


def generate_cultural_content(
    language_pref: str,
    dietary: List[str],
    accessibility: List[str]
) -> CultureAdaptResponse:
    """
    Generate culturally appropriate and accessible content
    """
    
    # Greeting in preferred language
    greetings_text = GREETINGS.get(language_pref, GREETINGS["en"])
    
    # Menu highlights based on dietary restrictions
    menu_highlights = []
    for diet in dietary:
        if diet.lower() in DIETARY_MENUS:
            menu_highlights.extend(DIETARY_MENUS[diet.lower()][:2])  # 2 items per restriction
    
    # If no dietary restrictions, show popular items
    if not menu_highlights:
        menu_highlights = [
            "Chef's Signature Ribeye Steak",
            "Pan-Seared Atlantic Salmon",
            "House-Made Pasta with Seasonal Vegetables",
            "Farm-to-Table Mixed Green Salad"
        ]
    
    # Remove duplicates
    menu_highlights = list(dict.fromkeys(menu_highlights))[:6]
    
    # Room notes based on accessibility needs
    room_notes = list(ROOM_NOTES.get("default", []))
    for need in accessibility:
        if need.lower() in ROOM_NOTES:
            room_notes.extend(ROOM_NOTES[need.lower()])
    
    # Remove duplicates
    room_notes = list(dict.fromkeys(room_notes))
    
    # Accessibility hints
    accessibility_hints = []
    for need in accessibility:
        if need.lower() in ACCESSIBILITY_HINTS:
            accessibility_hints.extend(ACCESSIBILITY_HINTS[need.lower()])
    
    # If no specific needs, show general accessibility info
    if not accessibility_hints:
        accessibility_hints = [
            "ADA-compliant facilities throughout property",
            "Service animals welcome",
            "Accessible transportation available",
            "Staff trained in accessibility assistance"
        ]
    
    # Remove duplicates
    accessibility_hints = list(dict.fromkeys(accessibility_hints))
    
    return CultureAdaptResponse(
        greetings_text=greetings_text,
        menu_highlights=menu_highlights,
        room_notes=room_notes,
        accessibility_hints=accessibility_hints,
        alt_text_samples=ALT_TEXT_SAMPLES
    )


@router.post("/adapt", response_model=CultureAdaptResponse)
async def adapt_cultural_content(
    request: CultureAdaptRequest,
    token_payload: dict = Depends(jwt_verify)
):
    """
    Get culturally appropriate and accessible content
    
    Based on language preference, dietary restrictions, and accessibility needs,
    provides tailored greetings, menu recommendations, room notes, and accessibility information.
    """
    
    # Check feature flag
    if not flags.FEATURE_CULTURE:
        raise HTTPException(status_code=501, detail="Culture feature is not enabled")
    
    try:
        # Generate content
        content = generate_cultural_content(
            language_pref=request.language_pref,
            dietary=request.dietary,
            accessibility=request.accessibility
        )
        
        # Log telemetry
        telemetry({
            "event_type": "culture_adapt",
            "user_id": token_payload.get("sub", "unknown"),
            "language": request.language_pref,
            "dietary_count": len(request.dietary),
            "accessibility_count": len(request.accessibility),
            "metadata": {"feature": "culture"}
        })
        
        return content
        
    except Exception as e:
        # Log error
        telemetry({
            "event_type": "culture_error",
            "user_id": token_payload.get("sub", "unknown"),
            "error": str(e),
            "metadata": {"feature": "culture"}
        })
        raise HTTPException(status_code=500, detail=f"Cultural adaptation failed: {str(e)}")


