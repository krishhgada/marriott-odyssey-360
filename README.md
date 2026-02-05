# Marriott's Odyssey 360 AI (M-Odyssey 360)

**The World's First Fully Intelligent Hospitality Operating System**

## 🌟 Vision

Build the first fully intelligent hospitality operating system, where AI and immersive guest technology converge to create a predictive, emotionally-aware, frictionless, and truly unforgettable experience—before, during, and after each stay.

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- Virtual environment (recommended)

### Installation

1. **Clone and Setup Backend**
```bash
cd marriott-odyssey-360
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Start Backend Server**
```bash
cd backend
python main.py
```
Backend runs on http://localhost:8000

3. **Setup Frontend**
```bash
cd frontend
npm install
npm start
```
Frontend runs on http://localhost:3000

4. **Access Demo**
- Open http://localhost:3000 in your browser
- Use demo mode for full experience without real hotel integration
- Toggle between demo and live mode in settings

## 🏗️ Project Structure

```
marriott-odyssey-360/
├── backend/                 # FastAPI backend services
│   ├── api/                # API endpoints
│   ├── core/               # Core AI and business logic
│   ├── models/             # Data models
│   ├── services/           # Business services
│   └── utils/              # Utilities
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # UI components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   └── utils/          # Frontend utilities
├── demo_data/              # Mock data and demos
├── docs/                   # Documentation
├── security/               # Security and privacy docs
└── tests/                  # Test suites
```

## 🎯 Core Features

### Original Features
- **Emotion AI Everywhere**: Real-time emotion detection and proactive adjustments
- **Immersive Local Discovery**: AR overlays and real-time guides  
- **Contactless Everything**: Biometric and blockchain-based access
- **AI Concierge for Life**: 24/7 multilingual companion with persistent memory
- **Wellness & Safety Priority**: IoT monitoring and personalized regimens

### 🆕 New AI-Powered Features

#### Predictive Privacy Controller
- Personalized privacy recommendations based on travel persona
- Dynamic privacy mode selection (Strict, Balanced, Perks)
- Risk tolerance-based configuration

#### Cultural Inclusion & Accessibility Adapter
- Multi-language support (11+ languages)
- Dietary restriction accommodations
- Comprehensive accessibility features
- Culturally appropriate content generation

#### TrustLens - Content Authenticity Checker
- Image authenticity verification
- Trust score calculation (0-100)
- Risk detection and remediation suggestions
- Metadata analysis

#### Intermodal Concierge (Door-to-Door)
- Multi-modal transportation planning
- Route optimization (Fast, Eco, Cheap)
- CO2 footprint tracking
- Real-time ETA calculations

#### AgentOps for Associates
- Policy RAG Q&A system
- Automated guest reply drafting
- Citation-backed responses
- Policy corpus search

#### Bio-Haptic Mood Insights
- Mood state classification
- Proactive wellness suggestions
- Context-aware recommendations
- Personalized action plans

#### Enhanced Hotel & IoT Control
- Extended room environment controls
- Housekeeping request management
- Express checkout functionality
- Advanced thermostat control

#### System Analytics & Metrics
- Real-time telemetry dashboard
- Request tracking and monitoring
- Performance metrics
- CSV export functionality

## 🚩 Feature Flags

All new features are controlled via feature flags (default: enabled in development):

```bash
# Backend (.env or environment variables)
FEATURE_PRIVACY=true
FEATURE_CULTURE=true  
FEATURE_TRUSTLENS=true
FEATURE_INTERMODAL=true
FEATURE_AGENTOPS=true
FEATURE_INSIGHTS=true
TELEMETRY_ENABLED=true

# Frontend (.env)
REACT_APP_FEATURE_PRIVACY=true
REACT_APP_FEATURE_CULTURE=true
REACT_APP_FEATURE_TRUSTLENS=true
REACT_APP_FEATURE_INTERMODAL=true
REACT_APP_FEATURE_AGENTOPS=true
REACT_APP_FEATURE_INSIGHTS=true
```

To disable a feature, set its flag to `false`. The feature will be hidden from navigation and API endpoints will return 501.

## 🔧 Demo Mode

The system includes a comprehensive demo mode with:
- **Demo Token**: Use `demo-token-odyssey360` for authentication
- Simulated guest interactions and mock hotel data
- Deterministic AI responses (no external API calls)
- Complete offline operation
- CSV telemetry logging in `./.telemetry/`

## 🔒 Security & Privacy

- Zero raw data retention policy
- Instant anonymization of bio and mood data
- Ethical-by-design AI operations
- Full guest control over data
- Transparent data usage policies

## 🧪 Testing

Run backend tests:
```bash
cd backend
pytest tests/test_new_features.py -v
```

All new endpoints include comprehensive test coverage:
- Privacy recommendation engine
- Culture adaptation
- TrustLens authenticity checking
- Intermodal routing
- AgentOps policy search
- Insights prediction
- Security utilities (redaction, allowlist)

## 📚 Documentation

- [API Documentation](http://localhost:8000/docs) (when backend is running)
- [Demo Script](DEMO_SCRIPT.md) - 8-minute guided walkthrough
- [Security & Privacy](security/SECURITY.md) - JWT, redaction, allowlist
- [Implementation Plan](PLAN.md) - Detailed architecture and rollback
- [Changelog](CHANGELOG.md) - Complete list of changes
- [Architecture Guide](docs/ARCHITECTURE.md)
- [Deployment Guide](docs/DEPLOYMENT.md)

## 📡 API Endpoints (New)

### Privacy
- `POST /api/privacy/recommend` - Get privacy recommendations

### Culture & Accessibility
- `POST /api/culture/adapt` - Get culturally adapted content

### TrustLens
- `POST /api/trust/check_image` - Verify image authenticity

### Intermodal
- `POST /api/intermodal/plan` - Plan door-to-door route

### AgentOps
- `POST /api/agentops/answer` - Ask policy question
- `POST /api/agentops/draft_reply` - Draft guest reply

### Insights
- `POST /api/insights/predict` - Get mood-based suggestions

### Hotel IoT
- `POST /api/room/environment` - Control room environment
- `POST /api/room/housekeeping` - Request housekeeping
- `POST /api/room/checkout` - Express checkout
- `POST /api/room/thermostat` - Control thermostat

### Offers
- `POST /api/offers/apply` - Apply personalized offer

### Analytics
- `GET /api/metrics` - Get system metrics

**Authentication**: All endpoints require `Authorization: Bearer <token>` header. Use `demo-token-odyssey360` for demo mode.

## 🤝 Contributing

This is a prototype for Marriott's next-generation hospitality platform. For internal development and testing only.

## 📄 License

Proprietary - Marriott International Inc.
