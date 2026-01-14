# 🐳 Docker Quick Start Guide

## Fastest Way to Run the App

### 1️⃣ Prerequisites
```bash
# Check if Docker is installed
docker --version
docker-compose --version
```

If not installed:
- **macOS**: Download Docker Desktop from https://www.docker.com/products/docker-desktop
- **Windows**: Download Docker Desktop from https://www.docker.com/products/docker-desktop
- **Linux**: `curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh`

### 2️⃣ One Command to Run Everything
```bash
cd realtime_analytics_dashboard
docker-compose up
```

**That's it!** ✨

### 3️⃣ Open in Browser
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Health Check**: http://localhost:8000/health

### 4️⃣ Stop Services
```bash
docker-compose down
```

---

## Common Commands

### View Logs
```bash
# Backend logs
docker-compose logs backend

# Frontend logs
docker-compose logs frontend

# Follow logs (live)
docker-compose logs -f backend
```

### Check Status
```bash
# See all services
docker-compose ps

# Check specific container
docker ps | grep crypto
```

### Rebuild Images
```bash
# Rebuild if code changed
docker-compose up --build

# Rebuild without cache
docker-compose up --build --no-cache
```

### Access Container Shell
```bash
# Backend shell
docker exec -it crypto_dashboard_backend bash

# Frontend shell
docker exec -it crypto_dashboard_frontend sh
```

### Clean Up Everything
```bash
# Stop and remove containers
docker-compose down

# Also remove volumes
docker-compose down -v

# Remove unused images and networks
docker system prune -a
```

---

## 🔧 Troubleshooting

### Port Already in Use
```bash
# If port 3000 or 8000 is already in use:
# Option 1: Stop other services using those ports
# Option 2: Change ports in docker-compose.yml
#   - "3001:3000"  (change first number)
#   - "8001:8000"  (change first number)
```

### Container Fails to Start
```bash
# Check logs for errors
docker-compose logs backend

# Common fixes:
# 1. Ensure requirements-simple.txt exists in backend/
# 2. Ensure package.json exists in frontend/
# 3. Check Docker disk space: docker system df
```

### WebSocket Connection Issues
```bash
# Check if backend is healthy
docker-compose exec backend curl http://localhost:8000/health

# Verify environment variables
docker-compose exec frontend env | grep REACT_APP
```

### Slow Performance
```bash
# Docker needs more resources:
# On Docker Desktop:
# 1. Click Docker icon in menu bar
# 2. Select "Preferences" → "Resources"
# 3. Increase CPU and Memory
```

---

## 📊 What's Running?

```
🚀 Backend (FastAPI)
   ├── Port: 8000
   ├── Container: crypto_dashboard_backend
   └── URL: http://localhost:8000

🎨 Frontend (React)
   ├── Port: 3000
   ├── Container: crypto_dashboard_frontend
   └── URL: http://localhost:3000

🌐 Network: crypto_network
   └── Allows containers to communicate
```

---

## 🎯 Next Steps

### Local Development
- Docker Compose is perfect for local development
- Changes to code are reflected (with rebuild)

### Deploy to Production
- See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for:
  - Cloud deployment (Render + Vercel)
  - Self-hosted deployment
  - Custom domain setup

### Customize Ports
Edit `docker-compose.yml`:
```yaml
ports:
  - "3001:3000"    # Use 3001 instead of 3000
  - "8001:8000"    # Use 8001 instead of 8000
```

---

## 📚 Learn More

- [Complete Deployment Guide](DEPLOYMENT_GUIDE.md)
- [Deployment History](DEPLOYMENT_HISTORY.md)
- [API Documentation](API.md)
- [Architecture Overview](ARCHITECTURE.md)

---

**That's it! Happy coding! 🚀**
