# API Examples - cURL Commands

Quick reference for testing all new endpoints with cURL.

## Authentication

All requests require the demo token:
```bash
TOKEN="demo-token-odyssey360"
```

---

## 1. Privacy Controller

**Get Privacy Recommendations**:
```bash
curl -X POST http://localhost:8000/api/privacy/recommend \
  -H "Authorization: Bearer demo-token-odyssey360" \
  -H "Content-Type: application/json" \
  -d '{
    "persona": "business",
    "trip_type": "work",
    "risk_tolerance": 3
  }'
```

**Expected Response**:
```json
{
  "mode": "balanced",
  "toggles": {
    "location_sharing": true,
    "voice_history": false,
    "personalization": true
  },
  "explanation": [
    "Business traveler: location sharing for meetings",
    "Voice history disabled for professional privacy",
    "⚖️ Balanced privacy and personalization"
  ]
}
```

---

## 2. Culture & Accessibility

**Get Culturally Adapted Content**:
```bash
curl -X POST http://localhost:8000/api/culture/adapt \
  -H "Authorization: Bearer demo-token-odyssey360" \
  -H "Content-Type: application/json" \
  -d '{
    "language_pref": "es",
    "dietary": ["veg", "halal"],
    "accessibility": ["wheelchair"]
  }'
```

**Expected Response**:
```json
{
  "greetings_text": "¡Bienvenido! Estamos encantados de tenerlo con nosotros.",
  "menu_highlights": [
    "Grilled Vegetable Platter with Quinoa",
    "Mediterranean Chickpea Salad",
    "Halal-Certified Lamb Tagine",
    "Grilled Halal Chicken Kebab"
  ],
  "room_notes": [
    "Climate control via tablet on nightstand",
    "Lowered light switches and thermostat (36 inches from floor)",
    "Roll-in shower with grab bars and shower seat"
  ],
  "accessibility_hints": [
    "All public areas are wheelchair accessible",
    "Accessible van service available at valet"
  ],
  "alt_text_samples": [...]
}
```

---

## 3. TrustLens (Content Authenticity)

**Check Image Authenticity**:
```bash
curl -X POST http://localhost:8000/api/trust/check_image \
  -H "Authorization: Bearer demo-token-odyssey360" \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "https://example.com/hotel-photo.jpg",
    "filename": "hotel-photo.jpg",
    "metadata": {
      "camera": "iPhone 12",
      "created": "2024-01-01"
    }
  }'
```

**Expected Response**:
```json
{
  "trust_score": 85,
  "risks": [
    "No significant authenticity concerns detected"
  ],
  "remediation": [
    "✅ Image appears trustworthy"
  ],
  "details": {
    "exif_present": true,
    "camera_info": true,
    "secure_connection": true
  }
}
```

---

## 4. Intermodal Routing

**Plan Door-to-Door Route**:
```bash
curl -X POST http://localhost:8000/api/intermodal/plan \
  -H "Authorization: Bearer demo-token-odyssey360" \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "San Francisco Airport",
    "arrival_time": "18:00",
    "priority": "eco"
  }'
```

**Expected Response**:
```json
{
  "routes": [
    {
      "mode": "walk",
      "eta": "",
      "duration_min": 12,
      "co2_kg": 0.0,
      "cost_estimate": 0.0,
      "instructions": "Walk to nearest subway station (1km)"
    },
    {
      "mode": "subway",
      "eta": "",
      "duration_min": 15,
      "co2_kg": 0.3,
      "cost_estimate": 1.8,
      "instructions": "Take Green Line subway to Downtown Station"
    },
    {
      "mode": "scooter",
      "eta": "18:00",
      "duration_min": 6,
      "co2_kg": 0.02,
      "cost_estimate": 0.5,
      "instructions": "Rent e-scooter for last mile to hotel"
    }
  ],
  "total_duration_min": 33,
  "total_co2_kg": 0.32,
  "total_cost": 2.3,
  "recommended_departure": "17:27"
}
```

---

## 5. AgentOps - Policy Q&A

**Ask Policy Question**:
```bash
curl -X POST http://localhost:8000/api/agentops/answer \
  -H "Authorization: Bearer demo-token-odyssey360" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the cancellation policy?"
  }'
```

**Expected Response**:
```json
{
  "answer": "Standard check-in time is 3:00 PM, and check-out time is 12:00 PM noon. Guests may request a room change within the first 24 hours of stay at no charge if they are dissatisfied with their accommodated room.",
  "citations": ["POL-GUEST-SERVICES", "POL-BILLING"]
}
```

**Draft Guest Reply**:
```bash
curl -X POST http://localhost:8000/api/agentops/draft_reply \
  -H "Authorization: Bearer demo-token-odyssey360" \
  -H "Content-Type: application/json" \
  -d '{
    "ticket_text": "I need to cancel my reservation due to an emergency"
  }'
```

**Expected Response**:
```json
{
  "draft": "Thank you for contacting us. According to our cancellation policy [POL-BILLING], cancellations made before 6:00 PM on the day of arrival receive a full refund. I'd be happy to process this for you. May I have your confirmation number?",
  "citations": ["POL-BILLING"]
}
```

---

## 6. Mood & Wellness Insights

**Get Mood-Based Suggestions**:
```bash
curl -X POST http://localhost:8000/api/insights/predict \
  -H "Authorization: Bearer demo-token-odyssey360" \
  -H "Content-Type: application/json" \
  -d '{
    "guest_id": "G123",
    "mood": {
      "stress_level": 0.8,
      "energy_level": 0.3,
      "local_weather": "Rain"
    },
    "context": {
      "time_of_day": "14:30",
      "occupancy_pct": 75.0
    },
    "preferences": {
      "likes_quiet": true,
      "preferred_cuisine": "Italian"
    }
  }'
```

**Expected Response**:
```json
{
  "state": "STRESSED",
  "suggestion": {
    "text": "We recommend our quiet spa lounge with complimentary aromatherapy",
    "action_id": "SPA_QUIET_LOUNGE",
    "evidence": [
      "Elevated stress level detected (0.8)",
      "Guest preference: quiet environments",
      "Spa lounge currently at 30% capacity"
    ]
  }
}
```

---

## 7. Hotel IoT Control

**Control Room Environment**:
```bash
curl -X POST http://localhost:8000/api/room/environment \
  -H "Authorization: Bearer demo-token-odyssey360" \
  -H "Content-Type: application/json" \
  -d '{
    "room": "402",
    "lights": "dim",
    "ac_temp": 72,
    "sound": "white_noise"
  }'
```

**Request Housekeeping**:
```bash
curl -X POST http://localhost:8000/api/room/housekeeping \
  -H "Authorization: Bearer demo-token-odyssey360" \
  -H "Content-Type: application/json" \
  -d '{
    "room": "402",
    "request": "towels"
  }'
```

**Express Checkout**:
```bash
curl -X POST http://localhost:8000/api/room/checkout \
  -H "Authorization: Bearer demo-token-odyssey360" \
  -H "Content-Type: application/json" \
  -d '{
    "room": "402",
    "email": "guest@example.com"
  }'
```

**Expected Response** (all IoT endpoints):
```json
{
  "success": true,
  "message": "Room 402: lights set to dim, AC temperature set to 72°F, sound set to white_noise"
}
```

---

## 8. Offers

**Apply Personalized Offer**:
```bash
curl -X POST http://localhost:8000/api/offers/apply \
  -H "Authorization: Bearer demo-token-odyssey360" \
  -H "Content-Type: application/json" \
  -d '{
    "guest_id": "G123",
    "offer_id": "SUITE_UPGRADE_WINE"
  }'
```

**Expected Response**:
```json
{
  "success": true,
  "message": "Offer 'Suite upgrade with complimentary wine' successfully applied for guest G123",
  "applied_offer": "Suite upgrade with complimentary wine"
}
```

---

## 9. Analytics & Metrics

**Get System Metrics**:
```bash
curl -X GET http://localhost:8000/api/metrics \
  -H "Authorization: Bearer demo-token-odyssey360"
```

**Expected Response**:
```json
{
  "counters": {
    "total_events": 42,
    "event_api_request": 42,
    "status_2xx": 40,
    "status_4xx": 2
  },
  "recent_events": [
    {
      "timestamp": "2024-01-01T12:00:00Z",
      "event_type": "api_request",
      "path": "/api/privacy/recommend",
      "method": "POST",
      "status": 200,
      "latency_ms": 45.2,
      "user_agent": "curl/7.68.0"
    }
  ],
  "total_events": 42,
  "csv_path": "/path/to/.telemetry/telemetry.csv"
}
```

---

## Testing Without Authentication (Expected Failure)

```bash
curl -X POST http://localhost:8000/api/privacy/recommend \
  -H "Content-Type: application/json" \
  -d '{"persona": "business", "trip_type": "work", "risk_tolerance": 3}'
```

**Expected Response** (401 or 403):
```json
{
  "detail": "Not authenticated"
}
```

---

## Batch Testing Script

Save as `test_all_endpoints.sh`:

```bash
#!/bin/bash

TOKEN="demo-token-odyssey360"
BASE_URL="http://localhost:8000"

echo "Testing Privacy..."
curl -X POST $BASE_URL/api/privacy/recommend \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"persona":"business","trip_type":"work","risk_tolerance":3}'

echo -e "\n\nTesting Culture..."
curl -X POST $BASE_URL/api/culture/adapt \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"language_pref":"es","dietary":["veg"],"accessibility":["wheelchair"]}'

echo -e "\n\nTesting TrustLens..."
curl -X POST $BASE_URL/api/trust/check_image \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"image_url":"https://example.com/img.jpg","filename":"img.jpg","metadata":{}}'

echo -e "\n\nTesting Intermodal..."
curl -X POST $BASE_URL/api/intermodal/plan \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"origin":"Airport","arrival_time":"18:00","priority":"fast"}'

echo -e "\n\nTesting AgentOps..."
curl -X POST $BASE_URL/api/agentops/answer \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"question":"What is the cancellation policy?"}'

echo -e "\n\nTesting Insights..."
curl -X POST $BASE_URL/api/insights/predict \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"guest_id":"G123","mood":{"stress_level":0.5,"energy_level":0.5,"local_weather":"Clear"},"context":{"time_of_day":"14:00","occupancy_pct":70},"preferences":{"likes_quiet":true,"preferred_cuisine":"Italian"}}'

echo -e "\n\nTesting Room Control..."
curl -X POST $BASE_URL/api/room/environment \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"room":"402","lights":"dim","ac_temp":72,"sound":"off"}'

echo -e "\n\nTesting Offers..."
curl -X POST $BASE_URL/api/offers/apply \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"guest_id":"G123","offer_id":"SUITE_UPGRADE_WINE"}'

echo -e "\n\nTesting Metrics..."
curl -X GET $BASE_URL/api/metrics \
  -H "Authorization: Bearer $TOKEN"

echo -e "\n\nAll tests complete!"
```

Make executable and run:
```bash
chmod +x test_all_endpoints.sh
./test_all_endpoints.sh
```

---

## Swagger UI (Interactive Testing)

Open in browser: http://localhost:8000/docs

1. Click "Authorize" button at top
2. Enter: `demo-token-odyssey360`
3. Click any endpoint to expand
4. Click "Try it out"
5. Fill in example data
6. Click "Execute"

---

## Notes

- All endpoints return JSON
- All require `Authorization: Bearer demo-token-odyssey360` header
- Responses are deterministic (same input = same output)
- No external API calls
- Telemetry logged to `./.telemetry/telemetry.csv`


