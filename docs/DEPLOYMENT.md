# Deployment Guide
## Marriott's Odyssey 360 AI

This guide provides comprehensive instructions for deploying Marriott's Odyssey 360 AI in various environments.

## Prerequisites

### System Requirements
- **CPU**: 8+ cores (16+ recommended for production)
- **RAM**: 16GB+ (32GB+ recommended for production)
- **Storage**: 100GB+ SSD (500GB+ recommended for production)
- **Network**: 1Gbps+ bandwidth
- **OS**: Ubuntu 20.04+ / CentOS 8+ / macOS 12+

### Software Dependencies
- **Python**: 3.9+
- **Node.js**: 16+
- **Docker**: 20.10+
- **Docker Compose**: 2.0+
- **Kubernetes**: 1.21+ (for production)
- **PostgreSQL**: 13+
- **Redis**: 6.0+
- **MongoDB**: 5.0+

## Quick Start (Development)

### 1. Clone Repository
```bash
git clone https://github.com/marriott/odyssey-360-ai.git
cd odyssey-360-ai
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment Configuration
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 4. Database Setup
```bash
# Start PostgreSQL and Redis
docker-compose up -d postgres redis

# Run migrations
python -m alembic upgrade head
```

### 5. Start Backend
```bash
python main.py
```

### 6. Frontend Setup
```bash
cd frontend
npm install
npm start
```

### 7. Access Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Docker Deployment

### 1. Build Images
```bash
# Build all services
docker-compose build

# Or build specific service
docker-compose build backend
docker-compose build frontend
```

### 2. Start Services
```bash
# Start all services
docker-compose up -d

# Start specific services
docker-compose up -d backend frontend
```

### 3. View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
```

### 4. Stop Services
```bash
docker-compose down
```

## Kubernetes Deployment (Production)

### 1. Prerequisites
- Kubernetes cluster (1.21+)
- kubectl configured
- Helm 3.0+

### 2. Create Namespace
```bash
kubectl create namespace odyssey-360
```

### 3. Deploy with Helm
```bash
# Add Helm repository
helm repo add odyssey-360 https://charts.marriott.com/odyssey-360

# Install chart
helm install odyssey-360 odyssey-360/odyssey-360 \
  --namespace odyssey-360 \
  --set image.tag=latest \
  --set ingress.enabled=true \
  --set ingress.host=odyssey-360.marriott.com
```

### 4. Verify Deployment
```bash
# Check pods
kubectl get pods -n odyssey-360

# Check services
kubectl get services -n odyssey-360

# Check ingress
kubectl get ingress -n odyssey-360
```

## Environment-Specific Configurations

### Development Environment
```yaml
# docker-compose.dev.yml
version: '3.8'
services:
  backend:
    build: ./backend
    environment:
      - DEBUG=true
      - DEMO_MODE=true
      - LOG_LEVEL=debug
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
      - /app/venv
```

### Staging Environment
```yaml
# docker-compose.staging.yml
version: '3.8'
services:
  backend:
    image: odyssey-360/backend:staging
    environment:
      - DEBUG=false
      - DEMO_MODE=false
      - LOG_LEVEL=info
    ports:
      - "8000:8000"
    deploy:
      replicas: 2
      resources:
        limits:
          memory: 1G
          cpus: '0.5'
```

### Production Environment
```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  backend:
    image: odyssey-360/backend:latest
    environment:
      - DEBUG=false
      - DEMO_MODE=false
      - LOG_LEVEL=warning
    ports:
      - "8000:8000"
    deploy:
      replicas: 5
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
        reservations:
          memory: 1G
          cpus: '0.5'
    restart: unless-stopped
```

## Database Setup

### PostgreSQL Configuration
```sql
-- Create database
CREATE DATABASE odyssey_360;

-- Create user
CREATE USER odyssey_user WITH PASSWORD 'secure_password';

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE odyssey_360 TO odyssey_user;

-- Create extensions
\c odyssey_360;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
```

### Redis Configuration
```conf
# redis.conf
maxmemory 2gb
maxmemory-policy allkeys-lru
save 900 1
save 300 10
save 60 10000
```

### MongoDB Configuration
```javascript
// mongodb-init.js
use odyssey_360;
db.createUser({
  user: "odyssey_user",
  pwd: "secure_password",
  roles: [
    { role: "readWrite", db: "odyssey_360" }
  ]
});
```

## Security Configuration

### 1. SSL/TLS Setup
```bash
# Generate SSL certificates
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

# Configure nginx
server {
    listen 443 ssl;
    server_name odyssey-360.marriott.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 2. Environment Variables
```bash
# .env.production
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=postgresql://user:password@localhost:5432/odyssey_360
REDIS_URL=redis://localhost:6379
MONGODB_URL=mongodb://localhost:27017/odyssey_360
OPENAI_API_KEY=your-openai-api-key
JWT_SECRET=your-jwt-secret
ENCRYPTION_KEY=your-encryption-key
```

### 3. Firewall Configuration
```bash
# UFW (Ubuntu)
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# iptables
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT
```

## Monitoring Setup

### 1. Prometheus Configuration
```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'odyssey-360'
    static_configs:
      - targets: ['backend:8000', 'frontend:3000']
```

### 2. Grafana Dashboard
```json
{
  "dashboard": {
    "title": "Odyssey 360 AI Monitoring",
    "panels": [
      {
        "title": "API Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))"
          }
        ]
      }
    ]
  }
}
```

### 3. Log Aggregation
```yaml
# filebeat.yml
filebeat.inputs:
- type: log
  enabled: true
  paths:
    - /var/log/odyssey-360/*.log

output.elasticsearch:
  hosts: ["elasticsearch:9200"]
```

## Performance Optimization

### 1. Database Optimization
```sql
-- Create indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_messages_timestamp ON messages(timestamp);
CREATE INDEX idx_emotions_user_id ON emotions(user_id);

-- Analyze tables
ANALYZE users;
ANALYZE messages;
ANALYZE emotions;
```

### 2. Caching Strategy
```python
# Redis caching
import redis
from functools import wraps

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache_result(expiration=300):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
            result = func(*args, **kwargs)
            redis_client.setex(cache_key, expiration, json.dumps(result))
            return result
        return wrapper
    return decorator
```

### 3. Load Balancing
```nginx
# nginx.conf
upstream backend {
    server backend1:8000;
    server backend2:8000;
    server backend3:8000;
}

server {
    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Backup and Recovery

### 1. Database Backup
```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump odyssey_360 > backup_${DATE}.sql
aws s3 cp backup_${DATE}.sql s3://odyssey-360-backups/
```

### 2. Application Backup
```bash
#!/bin/bash
# app_backup.sh
tar -czf odyssey-360-${DATE}.tar.gz /opt/odyssey-360/
aws s3 cp odyssey-360-${DATE}.tar.gz s3://odyssey-360-backups/
```

### 3. Recovery Procedure
```bash
# Restore database
psql odyssey_360 < backup_20240101_120000.sql

# Restore application
tar -xzf odyssey-360-20240101_120000.tar.gz -C /opt/

# Restart services
docker-compose restart
```

## Troubleshooting

### Common Issues

#### 1. Database Connection Failed
```bash
# Check database status
docker-compose ps postgres

# Check logs
docker-compose logs postgres

# Test connection
psql -h localhost -U odyssey_user -d odyssey_360
```

#### 2. Frontend Build Failed
```bash
# Clear node modules
rm -rf node_modules package-lock.json

# Reinstall dependencies
npm install

# Check Node.js version
node --version
```

#### 3. API Not Responding
```bash
# Check backend logs
docker-compose logs backend

# Check port binding
netstat -tlnp | grep 8000

# Test API endpoint
curl http://localhost:8000/health
```

### Performance Issues

#### 1. High Memory Usage
```bash
# Check memory usage
docker stats

# Increase memory limits
docker-compose up -d --scale backend=3
```

#### 2. Slow Database Queries
```sql
-- Check slow queries
SELECT query, mean_time, calls 
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;
```

#### 3. API Timeout
```python
# Increase timeout in nginx
proxy_read_timeout 300s;
proxy_connect_timeout 300s;
proxy_send_timeout 300s;
```

## Maintenance

### 1. Regular Updates
```bash
# Update dependencies
pip install -r requirements.txt --upgrade
npm update

# Update Docker images
docker-compose pull
docker-compose up -d
```

### 2. Log Rotation
```bash
# Configure logrotate
cat > /etc/logrotate.d/odyssey-360 << EOF
/var/log/odyssey-360/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 odyssey odyssey
}
EOF
```

### 3. Health Checks
```bash
#!/bin/bash
# health_check.sh
curl -f http://localhost:8000/health || exit 1
curl -f http://localhost:3000 || exit 1
```

---

**Document Version**: 1.0  
**Last Updated**: January 2024  
**Next Review**: April 2024
