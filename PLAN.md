# Marriott Odyssey 360 AI - Feature Extension Plan

## Current Architecture Summary

### Backend (FastAPI)
**Entrypoint:** `backend/main.py` (runs on http://localhost:8000)

**Technology Stack:**
- FastAPI 0.104.1 with Uvicorn
- Pydantic v2 for data validation
- SQLAlchemy 2.0.23 + SQLite (odyssey360.db)
- JWT Authentication (python-jose + passlib)
- CORS middleware for frontend communication

**Existing Structure:**
```
backend/
├── main.py                    # FastAPI app with existing routers
├── api/                       # API endpoints (routers)
│   ├── auth_simple.py         # Authentication (login/register/logout)
│   ├── concierge.py           # AI Concierge
│   ├── emotion.py             # Emotion AI
│   ├── hotel.py               # Hotel services
│   ├── wellness.py            # Wellness & Safety
│   └── local_discovery.py     # Local Discovery
├── core/                      # Core business logic
│   ├── config.py              # Settings (existing)
│   ├── database.py            # Database initialization
│   ├── security.py            # JWT utilities (existing)
│   ├── concierge_ai.py        # AI logic
│   └── emotion_ai.py          # Emotion detection
└── models/
    └── user.py                # User model
```

**Existing API Routes (prefixed with /api/v1):**
- `/auth/*` - Authentication endpoints
- `/concierge/*` - AI Concierge services
- `/emotion/*` - Emotion AI services
- `/hotel/*` - Hotel/room services
- `/wellness/*` - Wellness monitoring
- `/local/*` - Local discovery

### Frontend (React)
**Entrypoint:** `frontend/src/index.js` (runs on http://localhost:3000)

**Technology Stack:**
- React 18.2.0 (Create React App)
- React Router v6
- styled-components 5.3.6
- React Query 3.39.3 (data fetching)
- Framer Motion 10.0.1 (animations)
- Lucide React 0.263.1 (icons)
- react-hot-toast 2.4.0 (notifications)
- Context API for auth & theme

**Existing Structure:**
```
frontend/src/
├── App.js                     # Main app with routing
├── index.js                   # React entrypoint
├── components/
│   ├── Header.js              # Top navigation bar
│   ├── Sidebar.js             # Left navigation sidebar
│   ├── LoginModal.js          # Login/register modal
│   └── LoadingScreen.js       # Initial loading screen
├── pages/                     # Route components
│   ├── Dashboard.js           # Home dashboard
│   ├── Concierge.js           # AI Concierge interface
│   ├── RoomControl.js         # Room/IoT controls
│   ├── Wellness.js            # Wellness monitoring
│   ├── LocalDiscovery.js      # Local attractions/events
│   └── Settings.js            # User settings
├── hooks/
│   ├── useAuth.js             # Authentication logic + axios setup
│   └── useTheme.js            # Theme management
├── services/                  # API client layer (empty, to be populated)
└── utils/                     # Utilities (empty)
```

**Existing Routes:**
- `/` - Dashboard
- `/concierge` - AI Concierge
- `/room` - Room Control
- `/wellness` - Wellness & Safety
- `/discovery` - Local Discovery
- `/settings` - Settings

---

## New Features to Add

### Phase 1: Core Enablers (Shared Infrastructure)

#### Backend Shared Modules
1. **`backend/shared/security.py`**
   - `redact(text: str) -> str` - PII redaction (emails, 12-16 digit sequences)
   - `jwt_verify` - FastAPI dependency for JWT validation (uses existing security.py)
   - `allowlist(action: str) -> bool` - Permit-list for side-effecting actions
   - DEMO_TOKEN support for local testing

2. **`backend/shared/telemetry.py`**
   - `telemetry(event: dict)` - Append to in-memory list + CSV file
   - In-memory counters dict
   - `get_metrics()` - Return metrics summary
   - Auto-create `./.telemetry/` directory

3. **`backend/shared/config.py`**
   - Feature flags: PRIVACY, CULTURE, TRUSTLENS, INTERMODAL, AGENTOPS, INSIGHTS (all default True)
   - Service base URLs
   - DEMO_TOKEN configuration

4. **Middleware in `main.py`**
   - Add telemetry middleware (log path, method, status, latency per request)
   - Non-breaking: wrap existing app

#### Frontend Shared Modules
1. **`frontend/src/context/FeatureFlagsContext.jsx`**
   - Context provider for feature flags
   - Read from environment or defaults (all True)
   - Export `useFeatureFlags()` hook

2. **`frontend/src/hooks/useApiClient.js`**
   - Axios instance with base URL
   - Auto-inject Authorization header from useAuth
   - Centralized error handling

3. **Update `frontend/src/components/Sidebar.js`**
   - Add new navigation items (conditionally rendered by feature flags)
   - New icons from Lucide: Shield, Globe, CheckCircle, Route, Users, Activity, TrendingUp

---

### Phase 2: New Features (Backend Routers + Frontend Pages)

#### A. Predictive Privacy Controller
**Backend:**
- **Router:** `backend/routers/privacy.py`
- **Endpoint:** `POST /api/privacy/recommend`
- **Request:** `{ persona, trip_type, risk_tolerance }`
- **Response:** `{ mode, toggles, explanation }`
- **Logic:** Deterministic rules based on inputs

**Frontend:**
- **Page:** `frontend/src/pages/Privacy.js`
- **Service:** `frontend/src/services/privacy.js`
- Form with selects/slider → result card with "Apply" button

#### B. Cultural Inclusion & Accessibility Adapter
**Backend:**
- **Router:** `backend/routers/culture.py`
- **Endpoint:** `POST /api/culture/adapt`
- **Request:** `{ language_pref, dietary, accessibility }`
- **Response:** `{ greetings_text, menu_highlights, room_notes, accessibility_hints, alt_text_samples }`

**Frontend:**
- **Page:** `frontend/src/pages/CultureAccessibility.js`
- **Service:** `frontend/src/services/culture.js`
- Multi-select form → cards with "Copy" buttons

#### C. TrustLens (Content Authenticity Checker)
**Backend:**
- **Router:** `backend/routers/trustlens.py`
- **Endpoint:** `POST /api/trust/check_image`
- **Request:** `{ image_url?, base64?, metadata }`
- **Response:** `{ trust_score, risks, remediation }`
- **Logic:** Mock EXIF check, Laplacian variance simulation, filename heuristics

**Frontend:**
- **Page:** `frontend/src/pages/TrustLens.js`
- **Service:** `frontend/src/services/trustlens.js`
- File picker or URL input → score badge + risk list

#### D. Intermodal Concierge (Door-to-Door)
**Backend:**
- **Router:** `backend/routers/intermodal.py`
- **Endpoint:** `POST /api/intermodal/plan`
- **Request:** `{ origin, arrival_time, priority }`
- **Response:** `[ { mode, eta, co2_kg, cost_estimate } ]`
- **Logic:** Hard-coded graph with 3-5 nodes, deterministic routing

**Frontend:**
- **Page:** `frontend/src/pages/Intermodal.js`
- **Service:** `frontend/src/services/intermodal.js`
- Form → result table with priority highlighting

#### E. AgentOps for Associates (Policy RAG stub)
**Backend:**
- **Router:** `backend/routers/agentops.py`
- **Endpoints:** 
  - `POST /api/agentops/answer` - Q&A with citations
  - `POST /api/agentops/draft_reply` - Draft response with inline citations
- **Data:** `backend/data/policies/*.md` (synthetic policy corpus)
- **Logic:** Simple keyword matching + citation extraction

**Frontend:**
- **Page:** `frontend/src/pages/AgentOps.js`
- **Service:** `frontend/src/services/agentops.js`
- Two panels: Q&A and Draft Reply → render with citation chips

#### F. Insights: Bio-Haptic Mood → Proactive Suggestions
**Backend:**
- **Router:** `backend/routers/insights.py`
- **Endpoint:** `POST /api/insights/predict`
- **Request:** `{ guest_id, mood, context, preferences }`
- **Response:** `{ state, suggestion: { text, action_id, evidence } }`
- **Logic:** Deterministic classifier (STRESSED, FATIGUED, CURIOUS, CELEBRATORY, NEUTRAL)

**Frontend:**
- **Page:** `frontend/src/pages/MoodWellness.js`
- **Service:** `frontend/src/services/insights.js`
- Sliders/selects → suggestion card with "Apply" action

#### G. Hotel & IoT Enhancements
**Backend:**
- **Router:** `backend/routers/hotel_iot.py`
- **Endpoints:**
  - `POST /api/room/environment` - Control lights, AC, sound
  - `POST /api/room/housekeeping` - Request services
  - `POST /api/room/checkout` - Express checkout
  - `POST /api/device/thermostat` - Temperature control
- All use allowlist and telemetry

**Frontend:**
- **Update:** `pages/RoomControl.js` (NON-BREAKING)
- Add new control tiles (dim lights, white noise, housekeeping, checkout)
- Keep existing functionality intact

#### H. Local Guide Mini-Widget + LocalDiscovery Integration
**Backend:**
- **Data:** `backend/data/local_guide/{pois.json, restaurants.json, events.json}`
- **Endpoint:** `POST /api/local_guide/book` (mock booking)
- Serve static fixtures

**Frontend:**
- **Update:** `pages/LocalDiscovery.js` (NON-BREAKING)
- Add filters (rating, cuisine, noise_level, walking_distance_m)
- "Book Table (mock)" button

#### I. Live Events Gap-Fill
**Backend:**
- **Router:** `backend/routers/events.py`
- **Endpoint:** `GET /api/events/gap_suggest?city=&start=&end=`
- Return 1-2 short activities

**Frontend:**
- **Update:** `pages/LocalDiscovery.js` (NON-BREAKING)
- "Fill my gap" mini-form in Events section

#### J. Targeted Offer Generation
**Backend:**
- **Router:** `backend/routers/offers.py`
- **Endpoint:** `POST /api/offers/apply`
- **Request:** `{ guest_id, offer_id }`
- Business rule: if insights state = CELEBRATORY or birthday nearby, suggest upgrade

**Frontend:**
- **Update:** `pages/Dashboard.js` or `pages/Concierge.js` (NON-BREAKING)
- Show conditional "Suite upgrade + wine" card
- "Apply Offer" button

#### K. Analytics & Metrics
**Backend:**
- **Router:** `backend/routers/analytics.py`
- **Endpoint:** `GET /api/metrics`
- Return: counts per route, last 10 events, error tally

**Frontend:**
- **Page:** `frontend/src/pages/Metrics.js`
- **Service:** `frontend/src/services/analytics.js`
- Poll with React Query → render counters + event list

---

## File-by-File Change Plan

### Backend - New Files

| File Path | Purpose | Dependencies |
|-----------|---------|--------------|
| `backend/shared/security.py` | PII redaction, JWT verify, allowlist | `core/security.py`, `core/config.py` |
| `backend/shared/telemetry.py` | Event tracking, metrics, CSV logging | built-in modules |
| `backend/shared/config.py` | Feature flags, DEMO_TOKEN | `pydantic_settings` |
| `backend/routers/privacy.py` | Privacy recommendation endpoint | `shared/security`, `shared/telemetry` |
| `backend/routers/culture.py` | Cultural adaptation endpoint | `shared/security`, `shared/telemetry` |
| `backend/routers/trustlens.py` | Content authenticity checker | `shared/security`, `shared/telemetry` |
| `backend/routers/intermodal.py` | Door-to-door routing | `shared/security`, `shared/telemetry` |
| `backend/routers/agentops.py` | Policy RAG Q&A | `shared/security`, `shared/telemetry` |
| `backend/routers/insights.py` | Mood-based suggestions | `shared/security`, `shared/telemetry` |
| `backend/routers/hotel_iot.py` | Extended room/IoT controls | `shared/security`, `shared/telemetry` |
| `backend/routers/offers.py` | Targeted offers | `shared/security`, `shared/telemetry` |
| `backend/routers/analytics.py` | Metrics dashboard | `shared/telemetry` |
| `backend/data/policies/*.md` | Synthetic policy corpus (3-5 files) | - |
| `backend/data/local_guide/*.json` | Local guide fixtures | - |

### Backend - Modified Files

| File Path | Modification | Rationale |
|-----------|--------------|-----------|
| `backend/main.py` | Add telemetry middleware, mount new routers | Non-breaking: new middleware runs after existing, new routers under `/api/*` |

### Frontend - New Files

| File Path | Purpose | Dependencies |
|-----------|---------|--------------|
| `frontend/src/context/FeatureFlagsContext.jsx` | Feature flags provider | React Context |
| `frontend/src/hooks/useApiClient.js` | Centralized API client | `axios`, `useAuth` |
| `frontend/src/services/privacy.js` | Privacy API client | `useApiClient` |
| `frontend/src/services/culture.js` | Culture API client | `useApiClient` |
| `frontend/src/services/trustlens.js` | TrustLens API client | `useApiClient` |
| `frontend/src/services/intermodal.js` | Intermodal API client | `useApiClient` |
| `frontend/src/services/agentops.js` | AgentOps API client | `useApiClient` |
| `frontend/src/services/insights.js` | Insights API client | `useApiClient` |
| `frontend/src/services/analytics.js` | Analytics API client | `useApiClient` |
| `frontend/src/pages/Privacy.js` | Privacy settings page | `services/privacy`, `useFeatureFlags` |
| `frontend/src/pages/CultureAccessibility.js` | Culture/accessibility page | `services/culture`, `useFeatureFlags` |
| `frontend/src/pages/TrustLens.js` | Content authenticity page | `services/trustlens`, `useFeatureFlags` |
| `frontend/src/pages/Intermodal.js` | Door-to-door routing page | `services/intermodal`, `useFeatureFlags` |
| `frontend/src/pages/AgentOps.js` | Policy assistant page | `services/agentops`, `useFeatureFlags` |
| `frontend/src/pages/MoodWellness.js` | Mood-based wellness page | `services/insights`, `useFeatureFlags` |
| `frontend/src/pages/Metrics.js` | Analytics dashboard | `services/analytics`, `useFeatureFlags` |

### Frontend - Modified Files

| File Path | Modification | Rationale |
|-----------|--------------|-----------|
| `frontend/src/App.js` | Add new routes for 7 pages | Non-breaking: append to existing `<Routes>` |
| `frontend/src/components/Sidebar.js` | Add new nav items with feature flags | Non-breaking: append to existing nav sections |
| `frontend/src/pages/RoomControl.js` | Add dim/white-noise controls, housekeeping, checkout | Non-breaking: add new tiles to existing layout |
| `frontend/src/pages/LocalDiscovery.js` | Add filters, booking, gap-fill | Non-breaking: enhance existing page with new sections |
| `frontend/src/pages/Dashboard.js` | Add offer callout card (conditional) | Non-breaking: inject card when conditions met |

### Documentation - New/Modified Files

| File Path | Modification | Rationale |
|-----------|--------------|-----------|
| `PLAN.md` | This file | Project planning |
| `README.md` | Update with new features, feature flags, run commands | Central documentation |
| `DEMO_SCRIPT.md` | 8-minute walkthrough | Demo guide |
| `security/SECURITY.md` | Update with JWT mock, redaction, allowlist, telemetry | Security documentation |
| `CHANGELOG.md` | List of all changes | Change tracking |

### Test Files

| File Path | Purpose |
|-----------|---------|
| `backend/tests/test_privacy.py` | Test privacy endpoint |
| `backend/tests/test_culture.py` | Test culture endpoint |
| `backend/tests/test_trustlens.py` | Test trustlens endpoint |
| `backend/tests/test_intermodal.py` | Test intermodal endpoint |
| `backend/tests/test_agentops.py` | Test agentops endpoints |
| `backend/tests/test_insights.py` | Test insights endpoint |
| `backend/tests/test_security_shared.py` | Test redaction, allowlist, jwt_verify |

---

## Rollback Strategy

### Feature Flag Rollback
All new features are gated behind feature flags in `backend/shared/config.py`:

```python
FEATURE_PRIVACY = True
FEATURE_CULTURE = True
FEATURE_TRUSTLENS = True
FEATURE_INTERMODAL = True
FEATURE_AGENTOPS = True
FEATURE_INSIGHTS = True
```

To disable a feature:
1. Set flag to `False` in `backend/shared/config.py`
2. The router will return 404 or 501 (Not Implemented)
3. Frontend nav items won't render (feature flags check in Sidebar.js)

### Router-Level Rollback
Each new router can be commented out in `backend/main.py`:
```python
# app.include_router(privacy.router, prefix="/api/privacy", tags=["Privacy"])
```

### Page-Level Rollback
Each new page route can be commented out in `frontend/src/App.js`:
```jsx
{/* <Route path="/privacy" element={<Privacy />} /> */}
```

### Full Rollback
To completely revert:
1. Delete all new files (see "New Files" lists above)
2. Revert modified files to original (git checkout)
3. Remove telemetry middleware from `main.py`
4. System returns to original state

---

## Implementation Order

### Phase 1: Foundation (30 mins)
1. ✅ Create PLAN.md
2. Backend shared modules: `security.py`, `telemetry.py`, `config.py`
3. Add telemetry middleware to `main.py`
4. Frontend shared: `FeatureFlagsContext.jsx`, `useApiClient.js`
5. Create data fixtures directories + sample files

### Phase 2A: Quick Wins (45 mins)
6. Privacy Controller (backend + frontend)
7. Culture Adapter (backend + frontend)
8. TrustLens (backend + frontend)

### Phase 2B: Complex Features (60 mins)
9. Intermodal Concierge (backend + frontend)
10. AgentOps (backend + frontend + policy fixtures)
11. Insights (backend + frontend)

### Phase 2C: Enhancements (30 mins)
12. Hotel IoT extensions (backend + update RoomControl.js)
13. Local Discovery enhancements (backend + update LocalDiscovery.js)
14. Targeted Offers (backend + update Dashboard.js)

### Phase 2D: Observability (15 mins)
15. Analytics & Metrics (backend + frontend)

### Phase 3: Quality & Documentation (45 mins)
16. Add tests for all new endpoints
17. Update Sidebar.js with new nav items
18. Update App.js with new routes
19. Update README.md
20. Create DEMO_SCRIPT.md
21. Update SECURITY.md
22. Create CHANGELOG.md

---

## Security Considerations

### JWT Authentication
- All new endpoints require `Depends(jwt_verify)`
- DEMO_TOKEN = `"demo-token-odyssey360"` for local testing
- Existing JWT flow from `core/security.py` remains unchanged

### PII Redaction
- `redact()` function masks emails and numeric sequences (12-16 digits)
- Applied to all telemetry logs and user-facing outputs
- Pattern: `user@example.com` → `us**@ex*****.com`
- Pattern: `1234567890123456` → `1234********3456`

### Allowlist
Permit only these actions:
- `room.checkout`
- `room.environment`
- `offers.apply`

All other side-effecting actions are blocked by default.

### Telemetry Privacy
- No PII in telemetry logs
- CSV files in `./.telemetry/` (gitignored)
- Telemetry contains: timestamp, path, method, status, latency (no user data)

### Zero External Network Calls
- All new features use deterministic logic or static fixtures
- No calls to external APIs (OpenAI, Google, etc.)
- Fully offline capable

---

## Testing Strategy

### Backend Unit Tests
- Test all new endpoints for 200 OK status
- Test JWT requirement (401 when missing token)
- Test allowlist enforcement
- Test redaction function with sample PII
- Test telemetry increments
- Coverage target: 80%+

### Frontend Integration Tests
- Verify all new pages render
- Verify feature flag hiding/showing
- Verify API client includes auth header
- Manual testing of user flows

### End-to-End Demo Flow
1. Login with demo credentials
2. Visit Privacy → submit form → see recommendation
3. Visit MoodWellness → adjust sliders → get suggestion
4. Visit Intermodal → plan route → see options
5. Visit TrustLens → upload mock image → see score
6. Visit AgentOps → ask policy question → see answer with citations
7. Visit Metrics → see telemetry counters

---

## Success Criteria

✅ All existing pages work unchanged  
✅ All new pages accessible behind feature flags  
✅ All new endpoints require JWT  
✅ Telemetry CSV contains at least 10 logged events  
✅ Redaction function correctly masks test PII  
✅ Allowlist blocks unauthorized actions  
✅ Zero external network calls during demo  
✅ All pytest tests pass  
✅ README.md updated with clear instructions  
✅ DEMO_SCRIPT.md provides 8-minute walkthrough  
✅ SECURITY.md documents new security measures  

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Breaking existing auth | Use existing `core/security.py`, only extend with `jwt_verify` wrapper |
| Breaking existing pages | Zero changes to existing page files (except RoomControl, LocalDiscovery, Dashboard - additive only) |
| Feature conflicts | All new routes under unique paths (`/api/privacy`, `/privacy`, etc.) |
| Performance impact | Telemetry middleware runs async, minimal overhead |
| Testing blockers | Use pytest fixtures with mock JWT tokens |
| Incomplete rollback | Feature flags at multiple levels (router + frontend nav) |

---

## Post-Implementation Checklist

- [ ] Run backend: `cd backend && uvicorn main:app --reload`
- [ ] Run frontend: `cd frontend && npm start`
- [ ] Visit http://localhost:3000, login with demo credentials
- [ ] Navigate to all 13 pages (6 existing + 7 new)
- [ ] Verify telemetry CSV created in `./.telemetry/`
- [ ] Run `pytest -q` in backend, confirm all tests pass
- [ ] Review CHANGELOG.md for completeness
- [ ] Generate cURL examples for all new endpoints
- [ ] Create sample screenshots for DEMO_SCRIPT.md

---

## Estimated Timeline

- **Phase 0 (Planning):** 30 minutes ✅
- **Phase 1 (Foundation):** 30 minutes
- **Phase 2 (Features):** 135 minutes
- **Phase 3 (Quality):** 45 minutes
- **Total:** ~4 hours for full implementation

---

*This plan ensures backward compatibility, security by default, and a smooth path to production.*


