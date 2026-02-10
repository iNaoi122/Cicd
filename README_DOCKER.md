# 🏇 RaceTracker - Docker Setup Complete

**Status**: ✅ **FULLY OPERATIONAL**

> This is the Docker deployment guide for the completed RaceTracker application.
> The application is **running now** and ready to use immediately.

## 🚀 Quick Start (30 seconds)

### Already Running?
The application is already running! Access it at:
- 🌐 **Frontend**: http://localhost
- 🔌 **API**: http://localhost:8000
- 📖 **Docs**: http://localhost:8000/docs

### Start Fresh
```bash
cd /home/sergey/University/cicd
./START.sh
```

Or manually:
```bash
docker-compose up -d
```

## 📍 Access Points

| Service | URL | Status |
|---------|-----|--------|
| **Frontend** | http://localhost | ✅ Running |
| **Backend API** | http://localhost:8000 | ✅ Running |
| **API Documentation** | http://localhost:8000/docs | ✅ Available |
| **Health Check** | http://localhost:8000/health | ✅ Healthy |

## 📦 What's Running

```
✅ racetracker-frontend (Nginx on port 80)
   └─ Vanilla JS SPA with FSD architecture
   
✅ racetracker-backend (FastAPI on port 8000)
   └─ Python 3.11 with SQLAlchemy ORM
```

## 🛑 Stop Application

```bash
docker-compose down
```

## 📊 View Logs

```bash
# All containers
docker-compose logs -f

# Specific service
docker logs -f racetracker-backend
docker logs -f racetracker-frontend
```

## 🔄 Restart Application

```bash
docker-compose restart
```

## 🔨 Rebuild Containers

```bash
docker-compose build --no-cache
docker-compose up -d
```

## 📚 Full Documentation

- **[GETTING_STARTED.md](./GETTING_STARTED.md)** - Complete user guide with API examples
- **[DOCKER_SETUP.md](./DOCKER_SETUP.md)** - Detailed Docker configuration
- **[PROJECT_STATUS.md](./PROJECT_STATUS.md)** - Project overview and status
- **[COMPLETION_REPORT.md](./COMPLETION_REPORT.md)** - Detailed completion report

## 🎯 Features

### Frontend
- ✅ 6 Pages (Races, Jockeys, Horses with details)
- ✅ 4 Forms (Create Race, Add Jockey, Add Horse, Add Result)
- ✅ Responsive design (mobile-friendly)
- ✅ Hash-based routing
- ✅ Real-time validation

### Backend
- ✅ 15 API endpoints
- ✅ Full CRUD operations
- ✅ Relationship queries (jockey races, horse races)
- ✅ Automatic database migrations
- ✅ Pydantic validation

## 🐛 Troubleshooting

### Port already in use
```bash
# Kill process on port 80 or 8000
sudo lsof -i :80
sudo lsof -i :8000

# Or stop containers and try again
docker-compose down
```

### Container won't start
```bash
# Check logs
docker logs racetracker-backend
docker logs racetracker-frontend

# Rebuild
docker-compose build --no-cache
docker-compose up -d
```

### API not responding
```bash
# Check health
curl http://localhost:8000/health

# Check logs
docker logs racetracker-backend
```

## 🔗 Quick Links

- **Frontend**: http://localhost
- **API Base**: http://localhost:8000/api/v1
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📊 API Example

```bash
# Get all races
curl http://localhost:8000/api/v1/races/

# Create a race
curl -X POST http://localhost:8000/api/v1/races/ \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2026-02-15",
    "time": "14:00:00",
    "hippodrome": "Hippodromo Central",
    "name": "Grand Prix 2026"
  }'
```

## ✨ Environment

The application uses:
- **Docker** for containerization
- **Docker Compose** for orchestration
- **Nginx** as reverse proxy
- **FastAPI** for backend
- **SQLAlchemy** for ORM
- **SQLite** for database (in-memory)

## 📝 Configuration Files

- `docker-compose.yml` - Service definitions
- `frontend/Dockerfile` - Frontend container image
- `backend/Dockerfile` - Backend container image
- `frontend/nginx.conf` - Nginx reverse proxy config
- `frontend/.env` - Frontend environment variables
- `backend/requirements.txt` - Python dependencies

## 🎓 Technology Stack

**Frontend**: Vanilla HTML/CSS/JavaScript (ES6+) with FSD architecture
**Backend**: Python 3.11 + FastAPI + SQLAlchemy 2.0
**DevOps**: Docker + Docker Compose + Nginx

## ✅ Status

| Component | Status |
|-----------|--------|
| Frontend | ✅ Running |
| Backend | ✅ Running |
| API | ✅ Operational |
| Database | ✅ Initialized |
| Network | ✅ Connected |

---

**Version**: 1.0.0  
**Status**: Production Ready  
**Last Updated**: 2026-02-09

For more information, see the full documentation files listed above.
