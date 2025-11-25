# 🐳 Docker Setup Guide - Anime Picker

Run the entire Anime Picker application with a single command using Docker Compose!

---

## 📋 Prerequisites

### Required Software

- **Docker Desktop** (includes Docker Compose)
  - [Download for Windows](https://docs.docker.com/desktop/install/windows-install/)
  - [Download for Mac](https://docs.docker.com/desktop/install/mac-install/)
  - [Download for Linux](https://docs.docker.com/desktop/install/linux-install/)

### System Requirements

- **RAM:** 4 GB minimum (8 GB recommended)
- **Disk Space:** ~2 GB for Docker images
- **CPU:** Any modern processor (no GPU required)

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/anime-picker.git
cd anime-picker
```

### 2. Start the Application

```bash
docker-compose up
```

**That's it!** 🎉

The application will:

1. Build the backend Docker image (~1-2 minutes)
2. Build the frontend Docker image (~2-3 minutes)
3. Start both services
4. Wait for backend to be healthy
5. Start frontend

### 3. Access the Application

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:5000
- **Health Check:** http://localhost:5000/health

---

## 📦 What Gets Built

### Backend Container

- **Base Image:** Python 3.13 slim
- **Size:** ~800 MB
- **Includes:**
  - Flask web server
  - Sentence Transformers AI model
  - scikit-learn for similarity search
  - All Python dependencies
  - Anime dataset and embeddings

### Frontend Container

- **Base Image:** Node 20 Alpine
- **Size:** ~150 MB (optimized multi-stage build)
- **Includes:**
  - Next.js production build
  - Optimized static assets
  - Standalone server

---

## 🛠️ Docker Commands

### Start Services

```bash
# Start in foreground (see logs)
docker-compose up

# Start in background (detached mode)
docker-compose up -d

# Start and rebuild images
docker-compose up --build

# Start specific service
docker-compose up backend
```

### Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Stop specific service
docker-compose stop backend
```

### View Logs

```bash
# View all logs
docker-compose logs

# Follow logs in real-time
docker-compose logs -f

# View specific service logs
docker-compose logs backend
docker-compose logs frontend

# Last 100 lines
docker-compose logs --tail=100
```

### Rebuild Images

```bash
# Rebuild all images
docker-compose build

# Rebuild without cache
docker-compose build --no-cache

# Rebuild specific service
docker-compose build backend
```

### Check Status

```bash
# List running containers
docker-compose ps

# View resource usage
docker stats

# Check backend health
curl http://localhost:5000/health
```

---

## 🔧 Configuration

### Environment Variables

You can customize the application by creating a `.env` file in the project root:

```bash
# Backend Configuration
BACKEND_PORT=5000
BACKEND_DEBUG=False

# Frontend Configuration
FRONTEND_PORT=3000
NEXT_PUBLIC_API_URL=http://localhost:5000
```

### Port Mapping

To change ports, edit `docker-compose.yml`:

```yaml
services:
  backend:
    ports:
      - "8080:5000" # Change 8080 to your desired port

  frontend:
    ports:
      - "8000:3000" # Change 8000 to your desired port
```

---

## 📊 Service Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Docker Network                       │
│                 (anime-picker-network)                  │
│                                                         │
│  ┌──────────────────┐         ┌──────────────────┐    │
│  │    Frontend      │         │     Backend      │    │
│  │   (Next.js)      │────────▶│     (Flask)      │    │
│  │   Port: 3000     │         │   Port: 5000     │    │
│  └──────────────────┘         └──────────────────┘    │
│         │                              │               │
└─────────┼──────────────────────────────┼───────────────┘
          │                              │
          ▼                              ▼
    localhost:3000              localhost:5000
```

---

## 🐛 Troubleshooting

### Issue: "Port already in use"

**Solution:**

```bash
# Find process using port 5000
netstat -ano | findstr :5000  # Windows
lsof -i :5000                 # Mac/Linux

# Stop the process or change port in docker-compose.yml
```

### Issue: "Cannot connect to Docker daemon"

**Solution:**

1. Make sure Docker Desktop is running
2. Restart Docker Desktop
3. Check Docker status: `docker info`

### Issue: Backend health check failing

**Solution:**

```bash
# Check backend logs
docker-compose logs backend

# Verify embeddings file exists
ls -lh Backend/anime_embeddings.pkl

# If missing, generate embeddings:
cd Backend
python preprocess.py
```

### Issue: Frontend shows "Could not connect to server"

**Solution:**

```bash
# Check if backend is running
docker-compose ps

# Verify backend health
curl http://localhost:5000/health

# Check frontend environment
docker-compose exec frontend env | grep API_URL
```

### Issue: Images not loading

**Solution:**

The Next.js config already includes MyAnimeList CDN. If issues persist:

```bash
# Rebuild frontend
docker-compose build --no-cache frontend
docker-compose up frontend
```

### Issue: Out of disk space

**Solution:**

```bash
# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune

# Remove everything (careful!)
docker system prune -a --volumes
```

---

## 🔄 Development Workflow

### Making Changes

#### Backend Changes:

```bash
# 1. Edit Python files in Backend/
# 2. Rebuild and restart
docker-compose build backend
docker-compose up backend
```

#### Frontend Changes:

```bash
# 1. Edit files in frontend/src/
# 2. Rebuild and restart
docker-compose build frontend
docker-compose up frontend
```

### Live Development (Alternative)

For faster development, run services locally instead:

```bash
# Terminal 1 - Backend
cd Backend
python app.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

---

## 📈 Performance

### First Run

- **Build Time:** 3-5 minutes (downloads dependencies)
- **Startup Time:** 30-40 seconds (model loading)

### Subsequent Runs

- **Startup Time:** 10-15 seconds (cached images)

### Resource Usage

- **Backend:** ~500 MB RAM
- **Frontend:** ~100 MB RAM
- **Total:** ~600 MB RAM

---

## 🔐 Security Notes

### Production Deployment

If deploying to production, update:

1. **Remove debug mode:**

   ```yaml
   environment:
     - DEBUG=False
   ```

2. **Use secrets for sensitive data:**

   ```yaml
   secrets:
     - db_password
   ```

3. **Enable HTTPS** (use reverse proxy like Nginx)

4. **Restrict CORS** in backend:
   ```python
   CORS(app, origins=['https://your-domain.com'])
   ```

---

## 📚 Additional Resources

### Docker Commands Reference

| Command                               | Description              |
| ------------------------------------- | ------------------------ |
| `docker-compose up`                   | Start services           |
| `docker-compose down`                 | Stop services            |
| `docker-compose ps`                   | List services            |
| `docker-compose logs`                 | View logs                |
| `docker-compose build`                | Build images             |
| `docker-compose exec <service> <cmd>` | Run command in container |
| `docker-compose restart`              | Restart services         |

### Useful Docker Exec Commands

```bash
# Access backend shell
docker-compose exec backend bash

# Access frontend shell
docker-compose exec frontend sh

# Check Python version in backend
docker-compose exec backend python --version

# Check Node version in frontend
docker-compose exec frontend node --version
```

---

## 🎯 Common Use Cases

### 1. Fresh Start

```bash
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

### 2. Update Dependencies

```bash
# Backend
cd Backend
# Update requirements.txt
docker-compose build --no-cache backend

# Frontend
cd frontend
# Update package.json
docker-compose build --no-cache frontend
```

### 3. View Real-time Logs

```bash
docker-compose logs -f --tail=50
```

### 4. Restart Single Service

```bash
docker-compose restart backend
```

---

## ✅ Verification Checklist

After running `docker-compose up`, verify:

- [ ] Backend container is running: `docker-compose ps`
- [ ] Frontend container is running: `docker-compose ps`
- [ ] Backend health check passes: `curl http://localhost:5000/health`
- [ ] Frontend loads: Open http://localhost:3000
- [ ] Search works: Try searching for "action anime"
- [ ] Images load correctly
- [ ] No errors in logs: `docker-compose logs`

---

## 🆘 Getting Help

### Check Logs First

```bash
docker-compose logs -f
```

### Common Log Locations

- Backend logs: `docker-compose logs backend`
- Frontend logs: `docker-compose logs frontend`
- Build logs: `docker-compose build --progress=plain`

### Debug Mode

Enable verbose logging:

```yaml
# In docker-compose.yml
environment:
  - DEBUG=True
  - LOG_LEVEL=DEBUG
```

---

## 📝 Notes

### Data Persistence

- Anime dataset and embeddings are mounted as volumes
- Changes to these files are reflected immediately
- No need to rebuild containers for data updates

### Network Communication

- Services communicate via Docker network
- Frontend uses `http://localhost:5000` (from host machine)
- Containers can use service names: `http://backend:5000`

### Image Sizes

- Backend: ~800 MB (includes AI model)
- Frontend: ~150 MB (optimized build)
- Total: ~950 MB

---

## 🎊 Success!

If you see this, you're all set:

```
✅ Backend running on http://localhost:5000
✅ Frontend running on http://localhost:3000
✅ Health check passing
✅ Search functionality working
```

**Enjoy your Anime Picker! 🎭**

---

**Docker Setup Version:** 1.0  
**Last Updated:** 2025-11-25  
**Status:** ✅ Production Ready
