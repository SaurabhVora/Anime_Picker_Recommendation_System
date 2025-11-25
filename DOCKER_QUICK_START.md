# 🚀 Quick Reference - Docker Commands

## Start Application

```bash
# Start (foreground - see logs)
docker-compose up

# Start (background)
docker-compose up -d

# Start with rebuild
docker-compose up --build
```

## Stop Application

```bash
# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## View Logs

```bash
# All logs (follow)
docker-compose logs -f

# Backend only
docker-compose logs -f backend

# Frontend only
docker-compose logs -f frontend

# Last 50 lines
docker-compose logs --tail=50
```

## Check Status

```bash
# List running containers
docker-compose ps

# Check backend health
curl http://localhost:5000/health

# View resource usage
docker stats
```

## Rebuild

```bash
# Rebuild all
docker-compose build

# Rebuild without cache
docker-compose build --no-cache

# Rebuild specific service
docker-compose build backend
```

## Access Points

- **Frontend:** http://localhost:3000
- **Backend:** http://localhost:5000
- **Health Check:** http://localhost:5000/health

## Troubleshooting

```bash
# View backend logs
docker-compose logs backend

# View frontend logs
docker-compose logs frontend

# Restart service
docker-compose restart backend

# Clean everything
docker system prune -a
```

## Helper Scripts

**Windows:**

```cmd
docker-start.bat
```

**PowerShell:**

```powershell
.\docker-start.ps1
```

---

**For detailed documentation, see [DOCKER_README.md](DOCKER_README.md)**
