# Security & Privacy Documentation

## Overview

Marriott Odyssey 360 AI implements security-by-default principles with multiple layers of protection for guest data and system operations.

---

## Authentication & Authorization

### JWT (JSON Web Tokens)

All new API endpoints require JWT authentication:

```python
from shared.security import jwt_verify

@router.post("/endpoint")
async def protected_endpoint(token_payload: dict = Depends(jwt_verify)):
    # Endpoint logic here
    pass
```

**Token Structure**:
- Algorithm: HS256
- Expiration: 30 minutes (configurable)
- Payload: `{"sub": "user_id", "email": "user@example.com"}`

### Demo Token

For local development and testing:

```
Token: demo-token-odyssey360
```

Set in `backend/shared/config.py`:
```python
DEMO_TOKEN = os.getenv("DEMO_TOKEN", "demo-token-odyssey360")
```

Usage in API calls:
```bash
curl -H "Authorization: Bearer demo-token-odyssey360" \
  http://localhost:8000/api/privacy/recommend
```

---

## PII Redaction

### Automatic Redaction

The `redact()` function automatically masks personally identifiable information:

```python
from shared.security import redact

# Email redaction
text = "Contact user@example.com"
redacted = redact(text)  # "Contact us**@ex*****.com"

# Numeric sequence redaction (12-16 digits)
text = "Card: 1234567890123456"
redacted = redact(text)  # "Card: 1234********3456"
```

**Applied To**:
- All telemetry logs
- API responses containing user input
- Email addresses in checkout confirmations

**Pattern Matching**:
- Emails: Shows first 2 chars of username and first 2 of domain
- Card numbers: Shows first 4 and last 4 digits
- Other 12-16 digit sequences: Masked

---

## Action Allowlist

### Purpose

Prevents unauthorized or dangerous actions from being executed, even with valid authentication.

### Implementation

```python
from shared.security import allowlist

@router.post("/sensitive-action")
async def sensitive_action(token: dict = Depends(jwt_verify)):
    if not allowlist("action.name"):
        raise HTTPException(403, "Action not permitted")
    # Proceed with action
```

### Allowed Actions

Only these actions are permitted:

```python
ALLOWED_ACTIONS = {
    "room.checkout",       # Express checkout
    "room.environment",    # Control lights/AC/sound
    "offers.apply",        # Apply promotional offers
}
```

**To add an action**:
1. Add to `ALLOWED_ACTIONS` in `backend/shared/security.py`
2. Document rationale in commit message
3. Require security review

---

## Telemetry & Logging

### Telemetry System

All API requests are logged to:
- **In-memory**: Last 1000 events
- **CSV File**: `./.telemetry/telemetry.csv`

**Logged Data**:
```csv
timestamp,event_type,path,method,status,latency_ms,user_id,metadata
2024-01-01T12:00:00Z,api_request,/api/privacy/recommend,POST,200,45.2,demo-user,{}
```

**Privacy Controls**:
- No request bodies logged
- User IDs are opaque (not emails)
- PII automatically redacted
- CSV files excluded from version control (`.gitignore`)

### Access Telemetry

```python
from shared.telemetry import get_metrics

metrics = get_metrics()
# Returns: {"counters": {...}, "recent_events": [...], "total_events": 1234}
```

Frontend endpoint: `GET /api/metrics`

---

## Privacy-by-Design Principles

### 1. Data Minimization

- Only collect data necessary for functionality
- No background data collection
- Explicit consent for each data type

### 2. Zero Raw Data Retention

- Bio/mood data: Anonymized immediately
- Policy: `raw_data_retention_seconds: 0`
- Only aggregated statistics stored

### 3. Guest Control

- Privacy Controller gives users full transparency
- Toggle-based consent for each feature:
  - Location sharing
  - Voice history
  - Personalization level

### 4. Transparency

- All AI decisions include explanations
- Citations for policy-based answers
- Trust scores show reasoning

### 5. Ethical AI Operations

- No discriminatory data usage
- Fairness audits for recommendations
- Human-in-the-loop for critical decisions

---

## Feature Flags for Security

### Disable Features Instantly

```bash
# Backend
export FEATURE_PRIVACY=false
export FEATURE_TRUSTLENS=false

# Frontend
REACT_APP_FEATURE_PRIVACY=false
```

Features become:
- Invisible in UI navigation
- API returns 501 Not Implemented
- No data collection

### Rollback Strategy

1. **Immediate**: Set feature flag to `false`
2. **Fast**: Comment out router in `main.py`
3. **Complete**: Delete new files (tracked in CHANGELOG.md)

---

## Security Headers

### CORS Configuration

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Strict allowlist
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Production**: Replace with actual domain whitelist

### Trusted Hosts

```python
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "*.marriott.com"]
)
```

---

## Threat Model

### Protected Against

✅ **Unauthorized Access**: JWT required for all endpoints  
✅ **PII Leakage**: Automatic redaction  
✅ **Action Abuse**: Allowlist prevents dangerous operations  
✅ **CSRF**: Token-based auth (not cookies)  
✅ **Injection**: Pydantic validation on all inputs  
✅ **Timing Attacks**: Constant-time comparisons for tokens  

### Not Yet Protected (Production TODO)

⚠️ **Rate Limiting**: Add per-user/IP rate limits  
⚠️ **Audit Logging**: Separate security audit log  
⚠️ **Encryption at Rest**: Database encryption  
⚠️ **Secret Management**: Use HashiCorp Vault or AWS Secrets Manager  
⚠️ **DDoS Protection**: Cloudflare or AWS Shield  

---

## Vulnerability Reporting

**Internal Use Only**: Contact security team for issues

For production:
- Email: security@marriott.com
- PGP Key: [To be added]
- Response SLA: 24 hours for critical, 7 days for moderate

---

## Compliance

### GDPR Considerations

- **Right to Access**: Export user data via `/api/user/export`
- **Right to Erasure**: Delete via `/api/user/delete`
- **Data Portability**: JSON export format
- **Consent Management**: Per-feature toggles

### CCPA Considerations

- **Do Not Sell**: No data selling; privacy mode enforces
- **Opt-Out**: One-click disable in Privacy Controller
- **Disclosure**: Privacy Policy available at `/privacy-policy`

### HIPAA (Future)

If handling health data:
- Encrypt all health metrics
- Separate database for PHI
- Business Associate Agreement required

---

## Security Checklist (Production)

- [ ] Replace `your-secret-key-change-in-production` with real secret
- [ ] Set `DEMO_MODE=false` in production
- [ ] Enable rate limiting middleware
- [ ] Add WAF (Web Application Firewall)
- [ ] Implement secret rotation
- [ ] Set up security monitoring/alerting
- [ ] Conduct penetration testing
- [ ] Enable database encryption at rest
- [ ] Configure backup encryption
- [ ] Document incident response procedures
- [ ] Train staff on security protocols
- [ ] Set up SIEM integration

---

## Testing Security

Run security tests:

```bash
cd backend
pytest tests/test_new_features.py::TestSecurity -v
```

Tests include:
- Redaction function correctness
- Allowlist enforcement
- JWT verification failure paths
- Unauthorized access attempts

---

## Audit Trail

All security-relevant changes are logged in:
- Git commit history
- CHANGELOG.md
- Telemetry CSV (for runtime events)

**Example Audit Query**:
```bash
grep "unauthorized" .telemetry/telemetry.csv
grep "403" .telemetry/telemetry.csv
```

---

## Contact

**Security Team**: [To be added in production]  
**Project Lead**: [To be added]  
**Architecture Review**: See PLAN.md

---

**Last Updated**: 2024-10-11  
**Version**: 1.0.0  
**Classification**: Internal Use Only
