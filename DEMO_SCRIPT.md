# Marriott Odyssey 360 AI - Demo Script (8 Minutes)

## Pre-Demo Setup (Do before presenting)

1. **Start Backend**:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```
   Verify at http://localhost:8000/docs

2. **Start Frontend**:
   ```bash
   cd frontend
   npm start
   ```
   Opens at http://localhost:3000

3. **Login**: Use demo mode or enter any credentials

---

## Minute 0-1: Introduction & Dashboard

**Script**: "Welcome to Marriott Odyssey 360 AI - the world's first fully intelligent hospitality operating system. This system combines cutting-edge AI with practical hospitality needs. Let me show you our new AI-powered features."

**Actions**:
- Show clean dashboard with navigation sidebar
- Point out "New Features" section in sidebar
- Mention 7 new AI capabilities added

---

## Minute 1-2: Privacy Controller

**Navigate**: Sidebar → Privacy Controller

**Script**: "First, Predictive Privacy. Guests have different privacy needs based on their travel profile. Let me show you how the system adapts."

**Demo**:
1. Select "Business Traveler"
2. Trip type: "Work"  
3. Set risk tolerance slider to "2" (more private)
4. Click "Get Recommendations"
5. **Point out**: System recommends "Strict Mode" with specific toggles disabled

**Key Message**: "Notice it explains WHY—'Professional privacy' for business travelers. This builds trust through transparency."

---

## Minute 2-3: Culture & Accessibility

**Navigate**: Sidebar → Culture & Access

**Script**: "Cultural inclusion and accessibility aren't afterthoughts—they're built into the foundation."

**Demo**:
1. Select language: "Español"
2. Check dietary: "Halal" + "Gluten-Free"
3. Check accessibility: "Wheelchair Access"
4. Click "Get Personalized Content"
5. **Show**: Greeting in Spanish, curated menu, specific room notes
6. Click "Copy All" on any section

**Key Message**: "Every guest deserves content that respects their culture and accommodates their needs."

---

## Minute 3-4: TrustLens (Content Authenticity)

**Navigate**: Sidebar → TrustLens

**Script**: "In an era of deepfakes and misinformation, TrustLens verifies content authenticity."

**Demo**:
1. Tab to "Image URL"
2. Enter: `https://example.com/stock-photo-12345.jpg`
3. Click "Check Authenticity"
4. **Show**: Trust score (likely 60-75), detected risks
5. **Point out**: "Stock photo detected" + remediation suggestions

**Key Message**: "This helps staff and guests verify that promotional content is genuine, building trust."

---

## Minute 4-5: Intermodal Door-to-Door

**Navigate**: Sidebar → Door-to-Door

**Script**: "Guests don't just need a room—they need to GET to the hotel sustainably and efficiently."

**Demo**:
1. Enter origin: "San Francisco Airport"
2. Set arrival time: "18:00"
3. Priority: "Eco" (most eco-friendly)
4. Click "Plan Route"
5. **Show**: Multi-modal route (walk + subway + scooter)
6. **Highlight**: CO2 footprint, cost breakdown, recommended departure time

**Key Message**: "We're not just hospitality—we're full-journey partners. Notice the CO2 tracking—sustainability matters."

---

## Minute 5-6: AgentOps (Policy Assistant)

**Navigate**: Sidebar → AgentOps

**Script**: "Our associates are the heart of hospitality. AgentOps empowers them with instant policy knowledge."

**Demo Panel 1 - Q&A**:
1. Ask: "What is the cancellation policy?"
2. Click "Get Answer"
3. **Show**: Instant answer with policy citations [POL-BILLING]

**Demo Panel 2 - Draft Reply**:
1. Paste: "I need to cancel my reservation due to an emergency"
2. Click "Generate Reply"
3. **Show**: Professional, empathetic response with embedded citations

**Key Message**: "Associates can respond faster and more consistently, with policy-backed confidence."

---

## Minute 6-7: Mood & Wellness Insights

**Navigate**: Sidebar → Mood & Wellness

**Script**: "What if we could anticipate guest needs before they even ask?"

**Demo**:
1. Set stress level: **80%** (high)
2. Set energy level: **30%** (low)
3. Weather: "Rain"
4. Click "Get Personalized Suggestion"
5. **Show**: State = "STRESSED" or "FATIGUED"
6. **Show**: Suggestion (spa lounge or quiet space)
7. **Point out**: Evidence list explains the recommendation

**Key Message**: "Proactive care. We don't wait for complaints—we anticipate and delight."

---

## Minute 7-8: System Metrics & Wrap-Up

**Navigate**: Sidebar → Metrics

**Script**: "Behind every AI feature is transparency and observability."

**Show**:
- Real-time request counts
- Success rates (2xx responses)
- Recent API events with latency
- **Point out**: Telemetry CSV path

**Wrap-Up Script**:
"What you've seen is:
1. **Privacy by design** - not by compliance checkbox
2. **Cultural intelligence** - authentic inclusion
3. **Trust verification** - combating misinformation
4. **Sustainability** - CO2-conscious routing
5. **Staff empowerment** - AI that assists, not replaces
6. **Proactive care** - anticipatory hospitality
7. **Full transparency** - observable, explainable AI

This is Marriott Odyssey 360 AI—where technology serves humanity, one guest at a time."

---

## Optional: Quick Backend API Demo

If time permits, show FastAPI docs:

1. Navigate to http://localhost:8000/docs
2. Show auto-generated Swagger UI
3. Expand `/api/privacy/recommend`
4. Click "Try it out"
5. Use demo token: `demo-token-odyssey360`
6. Show live API response

---

## Troubleshooting

**Issue**: Page doesn't load  
**Fix**: Check browser console, verify both backend and frontend are running

**Issue**: Auth error  
**Fix**: Use token `demo-token-odyssey360` or login with demo credentials

**Issue**: Feature not visible  
**Fix**: Check feature flags in `backend/shared/config.py` and frontend `.env`

---

## Key Talking Points

- **Non-Breaking**: All existing functionality untouched
- **Offline Demo**: No external API calls, fully deterministic
- **Security**: JWT required, PII redaction, action allowlist
- **Rollback**: Feature flags allow instant disable
- **Testing**: Full pytest coverage for all endpoints
- **Documentation**: Comprehensive API docs + security guide

---

## Post-Demo Q&A Prep

**Q: Is this using real AI?**  
A: The architecture is production-ready. Current responses are deterministic for demo reliability, but designed to plug in real ML models.

**Q: How do you ensure privacy?**  
A: Three layers: JWT auth, PII redaction (emails/numbers), and action allowlist. Plus zero raw data retention policy.

**Q: Can we A/B test features?**  
A: Yes! Feature flags let you enable for specific cohorts. Telemetry tracks adoption.

**Q: What about GDPR/compliance?**  
A: Privacy Controller demonstrates transparency. All data handling is consent-based and logged.

**Q: Performance impact?**  
A: Telemetry shows sub-100ms latency. Async middleware prevents blocking.

---

**Total Time**: 8 minutes  
**Estimated Setup Time**: 3 minutes  
**Recommended Practice Runs**: 2-3 times

