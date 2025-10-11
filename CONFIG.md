# Configuration Guide

This project separates **secrets** from **configuration** for better security.

## 🔐 Secrets (.env file)
**Location:** `/opt/portfolio/.env` on production server  
**Contains:** Sensitive data that should never be committed to git
- Passwords (database, services)
- API keys and tokens
- Secret keys for encryption/signing
- Private credentials

**Setup:**
```bash
# On production server
cp .env.example .env
nano .env  # Update with real secrets
chmod 600 .env  # Secure permissions
```

## ⚙️ Configuration (docker-compose.yml)
**Location:** Committed to git in `docker-compose.prod.yml`  
**Contains:** Non-sensitive settings that can be public
- Service hostnames and ports
- Feature flags and debug settings
- Public API endpoints
- Application modes (production/development)

## 🔄 How It Works

1. **Docker Compose loads .env first** (secrets)
2. **Then applies environment section** (config)  
3. **Environment section overrides .env** if same variable exists

## 📋 Variable Categories

### Secrets (in .env only):
- `FLASK_SECRET_KEY` - Flask session signing
- `PODOLOGY_SECRET_KEY` - Podology app secrets
- `ELASTIC_PASSWORD` - Elasticsearch auth
- `DATABASE_PASSWORD` - Database credentials
- `API_KEYS` - Third-party service keys

### Config (in docker-compose.yml only):
- `FLASK_ENV=production` - Application mode
- `PORT=5000` - Service port
- `ELASTICSEARCH_HOST=podology-elasticsearch` - Service discovery
- `DASH_URL_PREFIX=/pks/` - URL routing
- `DEBUG=0` - Debug flags

## 🚨 Security Rules

1. **Never commit .env files** - they're in .gitignore
2. **Only put secrets in .env** - everything else goes in docker-compose
3. **Use strong secrets** - generate with `openssl rand -base64 32`
4. **Rotate secrets regularly** - especially in production
5. **Restrict .env permissions** - `chmod 600 .env`

## 🛠️ Development vs Production

### Development:
- Use `.env.local` for local secrets
- Override with environment variables as needed
- Use `docker-compose.yml` (not .prod.yml)

### Production:  
- Use `.env` with real secrets
- Use `docker-compose.prod.yml` 
- Deploy script validates secrets are set
