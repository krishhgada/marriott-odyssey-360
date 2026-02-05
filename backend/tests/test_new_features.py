"""
Tests for new features
Run with: pytest backend/tests/test_new_features.py -v
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Demo token for testing
DEMO_TOKEN = "demo-token-odyssey360"
AUTH_HEADER = {"Authorization": f"Bearer {DEMO_TOKEN}"}


class TestPrivacy:
    """Test Privacy Controller endpoints"""
    
    def test_privacy_recommend_success(self):
        response = client.post(
            "/api/privacy/recommend",
            json={
                "persona": "business",
                "trip_type": "work",
                "risk_tolerance": 3
            },
            headers=AUTH_HEADER
        )
        assert response.status_code == 200
        data = response.json()
        assert "mode" in data
        assert "toggles" in data
        assert "explanation" in data
        assert data["mode"] in ["strict", "balanced", "perks"]
    
    def test_privacy_recommend_unauthorized(self):
        response = client.post(
            "/api/privacy/recommend",
            json={"persona": "business", "trip_type": "work", "risk_tolerance": 3}
        )
        assert response.status_code == 403  # Missing auth header


class TestCulture:
    """Test Culture & Accessibility endpoints"""
    
    def test_culture_adapt_success(self):
        response = client.post(
            "/api/culture/adapt",
            json={
                "language_pref": "es",
                "dietary": ["veg", "halal"],
                "accessibility": ["wheelchair"]
            },
            headers=AUTH_HEADER
        )
        assert response.status_code == 200
        data = response.json()
        assert "greetings_text" in data
        assert "menu_highlights" in data
        assert "room_notes" in data
        assert "accessibility_hints" in data
        assert len(data["menu_highlights"]) > 0


class TestTrustLens:
    """Test TrustLens endpoints"""
    
    def test_trustlens_check_url(self):
        response = client.post(
            "/api/trust/check_image",
            json={
                "image_url": "https://example.com/image.jpg",
                "filename": "image.jpg",
                "metadata": {"camera": "iPhone 12"}
            },
            headers=AUTH_HEADER
        )
        assert response.status_code == 200
        data = response.json()
        assert "trust_score" in data
        assert "risks" in data
        assert "remediation" in data
        assert 0 <= data["trust_score"] <= 100


class TestIntermodal:
    """Test Intermodal routing endpoints"""
    
    def test_intermodal_plan_fast(self):
        response = client.post(
            "/api/intermodal/plan",
            json={
                "origin": "Airport",
                "arrival_time": "18:00",
                "priority": "fast"
            },
            headers=AUTH_HEADER
        )
        assert response.status_code == 200
        data = response.json()
        assert "routes" in data
        assert "total_duration_min" in data
        assert "total_co2_kg" in data
        assert "total_cost" in data
        assert len(data["routes"]) > 0


class TestAgentOps:
    """Test AgentOps endpoints"""
    
    def test_agentops_answer(self):
        response = client.post(
            "/api/agentops/answer",
            json={"question": "What is the cancellation policy?"},
            headers=AUTH_HEADER
        )
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert "citations" in data
        assert len(data["answer"]) > 0
    
    def test_agentops_draft_reply(self):
        response = client.post(
            "/api/agentops/draft_reply",
            json={"ticket_text": "I need to cancel my reservation"},
            headers=AUTH_HEADER
        )
        assert response.status_code == 200
        data = response.json()
        assert "draft" in data
        assert "citations" in data
        assert len(data["draft"]) > 0


class TestInsights:
    """Test Insights endpoints"""
    
    def test_insights_predict(self):
        response = client.post(
            "/api/insights/predict",
            json={
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
                    "likes_quiet": True,
                    "preferred_cuisine": "Italian"
                }
            },
            headers=AUTH_HEADER
        )
        assert response.status_code == 200
        data = response.json()
        assert "state" in data
        assert "suggestion" in data
        assert data["state"] in ["STRESSED", "FATIGUED", "CURIOUS", "CELEBRATORY", "NEUTRAL"]
        assert "text" in data["suggestion"]
        assert "action_id" in data["suggestion"]


class TestHotelIoT:
    """Test Hotel IoT endpoints"""
    
    def test_room_environment(self):
        response = client.post(
            "/api/room/environment",
            json={
                "room": "402",
                "lights": "dim",
                "ac_temp": 72,
                "sound": "white_noise"
            },
            headers=AUTH_HEADER
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "message" in data
    
    def test_housekeeping(self):
        response = client.post(
            "/api/room/housekeeping",
            json={
                "room": "402",
                "request": "towels"
            },
            headers=AUTH_HEADER
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_express_checkout(self):
        response = client.post(
            "/api/room/checkout",
            json={
                "room": "402",
                "email": "guest@example.com"
            },
            headers=AUTH_HEADER
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True


class TestOffers:
    """Test Offers endpoints"""
    
    def test_offer_apply(self):
        response = client.post(
            "/api/offers/apply",
            json={
                "guest_id": "G123",
                "offer_id": "SUITE_UPGRADE_WINE"
            },
            headers=AUTH_HEADER
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "applied_offer" in data


class TestAnalytics:
    """Test Analytics endpoints"""
    
    def test_get_metrics(self):
        response = client.get("/api/metrics", headers=AUTH_HEADER)
        assert response.status_code == 200
        data = response.json()
        assert "counters" in data
        assert "recent_events" in data
        assert "total_events" in data
        assert "csv_path" in data


class TestSecurity:
    """Test security features"""
    
    def test_redaction(self):
        from shared.security import redact
        
        # Test email redaction
        text_with_email = "Contact user@example.com for help"
        redacted = redact(text_with_email)
        assert "us**@ex*****.com" in redacted
        
        # Test digit redaction
        text_with_digits = "Card: 1234567890123456"
        redacted = redact(text_with_digits)
        assert "1234********3456" in redacted
    
    def test_allowlist(self):
        from shared.security import allowlist
        
        assert allowlist("room.checkout") is True
        assert allowlist("room.environment") is True
        assert allowlist("offers.apply") is True
        assert allowlist("invalid.action") is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


