# 🚀 Deployment Guide - Anime Picker System

Complete guide for deploying the Anime Picker System to production.

---

## 📋 Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Deployment Options](#deployment-options)
3. [Option 1: Deploy to Heroku](#option-1-deploy-to-heroku)
4. [Option 2: Deploy to Railway](#option-2-deploy-to-railway)
5. [Option 3: Deploy to AWS EC2](#option-3-deploy-to-aws-ec2)
6. [Option 4: Deploy to DigitalOcean](#option-4-deploy-to-digitalocean)
7. [Frontend Deployment](#frontend-deployment)
8. [Post-Deployment](#post-deployment)
9. [Monitoring & Maintenance](#monitoring--maintenance)

---

## Pre-Deployment Checklist

### ✅ Code Preparation

- [ ] All code tested locally
- [ ] Environment variables configured
- [ ] Dependencies listed in `requirements.txt`
- [ ] `.gitignore` configured properly
- [ ] Debug mode disabled (`DEBUG=False`)
- [ ] CORS configured for production domain
- [ ] Logs configured appropriately

### ✅ Files to Include

```
Backend/
├── app.py
├── config.py
├── preprocess.py
├── requirements.txt
├── .env.example
├── .gitignore
├── anime_clean.csv
├── anime_embeddings.pkl
├── Procfile (for Heroku)
└── runtime.txt (optional)
```

### ✅ Files to Exclude (.gitignore)

```
__pycache__/
*.pyc
*.log
.env
venv/
anime_picker.log
```

### ✅ Configuration Changes

**config.py** - Update for production:

```python
import os

class Config:
    # Model Settings
    MODEL_NAME = 'all-mpnet-base-v2'
    EMBEDDINGS_FILE = 'anime_embeddings.pkl'

    # Search Settings
    MAX_RESULTS = 5
    CANDIDATE_POOL_SIZE = 50
    MAX_QUERY_LENGTH = 500

    # Server Settings
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'False') == 'True'  # False in production
    HOST = os.getenv('HOST', '0.0.0.0')  # 0.0.0.0 for production

    # Cache Settings
    ENABLE_QUERY_CACHE = True
    MAX_CACHE_SIZE = 100

    # Logging Settings
    LOG_FILE = 'anime_picker.log'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')  # INFO in production
```

**app.py** - Update CORS:

```python
from flask_cors import CORS

# Development
# CORS(app)

# Production - restrict to your frontend domain
CORS(app, origins=[
    "https://your-frontend-domain.com",
    "https://www.your-frontend-domain.com"
])
```

---

## Deployment Options

### Comparison Table

| Platform         | Difficulty | Cost                | Best For                    |
| ---------------- | ---------- | ------------------- | --------------------------- |
| **Heroku**       | Easy       | Free tier available | Quick deployment, beginners |
| **Railway**      | Easy       | Free tier available | Modern, simple deployment   |
| **AWS EC2**      | Medium     | Pay as you go       | Full control, scalability   |
| **DigitalOcean** | Medium     | $5/month            | Balance of control and ease |
| **Render**       | Easy       | Free tier available | Alternative to Heroku       |

---

## Option 1: Deploy to Heroku

### Step 1: Prepare Files

Create `Procfile` in Backend directory:

```
web: gunicorn app:app
```

Create `runtime.txt` (optional):

```
python-3.11.0
```

Update `requirements.txt` - add gunicorn:

```txt
# Add this line
gunicorn==21.2.0

# Keep all existing requirements
Flask==3.1.2
flask-cors==6.0.1
...
```

### Step 2: Install Heroku CLI

```bash
# Windows
winget install Heroku.HerokuCLI

# Mac
brew tap heroku/brew && brew install heroku

# Or download from: https://devcenter.heroku.com/articles/heroku-cli
```

### Step 3: Deploy

```bash
# Login to Heroku
heroku login

# Create new app
cd "d:/Anime Picker system/Backend"
heroku create anime-picker-api

# Set environment variables
heroku config:set DEBUG=False
heroku config:set HOST=0.0.0.0
heroku config:set LOG_LEVEL=INFO

# Initialize git (if not already)
git init
git add .
git commit -m "Initial deployment"

# Deploy
git push heroku main

# Open app
heroku open
```

### Step 4: Verify Deployment

```bash
# Check logs
heroku logs --tail

# Test health endpoint
curl https://anime-picker-api.herokuapp.com/health

# Test search
curl "https://anime-picker-api.herokuapp.com/search?q=action"
```

### Heroku Notes

- **Free tier**: Limited to 550-1000 dyno hours/month
- **Memory**: 512 MB RAM (may need to upgrade for AI model)
- **Sleep**: Free dynos sleep after 30 min of inactivity
- **Upgrade**: Consider Hobby dyno ($7/month) for always-on

---

## Option 2: Deploy to Railway

### Step 1: Prepare Files

Create `railway.json` (optional):

```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn app:app",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Step 2: Deploy via Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
cd "d:/Anime Picker system/Backend"
railway init

# Deploy
railway up

# Set environment variables
railway variables set DEBUG=False
railway variables set HOST=0.0.0.0

# Get URL
railway domain
```

### Step 3: Deploy via GitHub (Recommended)

1. Push code to GitHub
2. Go to [railway.app](https://railway.app)
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your repository
6. Railway auto-detects Python and deploys
7. Add environment variables in Railway dashboard
8. Generate domain

### Railway Notes

- **Free tier**: $5 credit/month
- **Memory**: More generous than Heroku
- **Auto-deploy**: Automatic deployments from GitHub
- **Custom domains**: Easy to configure

---

## Option 3: Deploy to AWS EC2

### Step 1: Launch EC2 Instance

1. Go to AWS Console → EC2
2. Click "Launch Instance"
3. Choose **Ubuntu Server 22.04 LTS**
4. Instance type: **t2.medium** (2 GB RAM minimum for AI model)
5. Configure security group:
   - SSH (22) - Your IP
   - HTTP (80) - Anywhere
   - HTTPS (443) - Anywhere
   - Custom TCP (5000) - Anywhere (temporary)
6. Launch and download key pair

### Step 2: Connect to Instance

```bash
# Windows (PowerShell)
ssh -i "your-key.pem" ubuntu@your-ec2-public-ip

# Set key permissions first (if needed)
icacls "your-key.pem" /inheritance:r /grant:r "%username%:R"
```

### Step 3: Setup Server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3-pip python3-venv nginx -y

# Create app directory
mkdir ~/anime-picker
cd ~/anime-picker

# Upload files (from local machine)
# Use SCP or SFTP
scp -i "your-key.pem" -r "d:/Anime Picker system/Backend/*" ubuntu@your-ec2-ip:~/anime-picker/
```

### Step 4: Setup Application

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Test application
python app.py
# Press Ctrl+C after verifying it works
```

### Step 5: Setup Gunicorn Service

Create `/etc/systemd/system/anime-picker.service`:

```ini
[Unit]
Description=Anime Picker API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/anime-picker
Environment="PATH=/home/ubuntu/anime-picker/venv/bin"
ExecStart=/home/ubuntu/anime-picker/venv/bin/gunicorn --workers 2 --bind 0.0.0.0:5000 app:app

[Install]
WantedBy=multi-user.target
```

Start service:

```bash
sudo systemctl start anime-picker
sudo systemctl enable anime-picker
sudo systemctl status anime-picker
```

### Step 6: Setup Nginx Reverse Proxy

Create `/etc/nginx/sites-available/anime-picker`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/anime-picker /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 7: Setup SSL (HTTPS)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal is configured automatically
```

### AWS EC2 Notes

- **Cost**: ~$15-30/month for t2.medium
- **Full control**: Complete server access
- **Scalability**: Easy to upgrade instance type
- **Maintenance**: You manage updates and security

---

## Option 4: Deploy to DigitalOcean

### Step 1: Create Droplet

1. Go to DigitalOcean → Create → Droplets
2. Choose **Ubuntu 22.04**
3. Plan: **Basic $6/month** (1 GB RAM) or **$12/month** (2 GB RAM recommended)
4. Add SSH key
5. Create Droplet

### Step 2: Setup (Same as AWS EC2)

Follow AWS EC2 steps 2-7, replacing `ubuntu@your-ec2-ip` with `root@your-droplet-ip`

### DigitalOcean Notes

- **Cost**: $6-12/month
- **Simple**: Easier than AWS
- **App Platform**: Alternative 1-click deployment option
- **Backups**: Easy automated backups

---

## Frontend Deployment

### Option 1: Vercel (Recommended for React/Next.js)

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd your-frontend-directory
vercel

# Set environment variable
vercel env add REACT_APP_API_URL
# Enter: https://your-backend-domain.com
```

### Option 2: Netlify (Recommended for Static Sites)

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Build frontend
npm run build

# Deploy
netlify deploy --prod

# Set environment variable in Netlify dashboard
# REACT_APP_API_URL=https://your-backend-domain.com
```

### Option 3: GitHub Pages (Static Only)

```bash
# Add to package.json
"homepage": "https://yourusername.github.io/anime-picker",

# Install gh-pages
npm install --save-dev gh-pages

# Add deploy scripts
"scripts": {
  "predeploy": "npm run build",
  "deploy": "gh-pages -d build"
}

# Deploy
npm run deploy
```

### Frontend Environment Variables

Create `.env.production`:

```bash
REACT_APP_API_URL=https://your-backend-domain.com
REACT_APP_API_TIMEOUT=10000
```

Update API calls:

```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:5000";

fetch(`${API_BASE_URL}/search?q=${query}`);
```

---

## Post-Deployment

### 1. Update CORS

In `app.py`, update allowed origins:

```python
CORS(app, origins=[
    "https://your-frontend-domain.com",
    "https://www.your-frontend-domain.com"
])
```

### 2. Test All Endpoints

```bash
# Health check
curl https://your-api-domain.com/health

# Search
curl "https://your-api-domain.com/search?q=action&limit=5"

# Pagination
curl "https://your-api-domain.com/search?q=fantasy&limit=10&offset=5"
```

### 3. Monitor Logs

```bash
# Heroku
heroku logs --tail

# Railway
railway logs

# AWS/DigitalOcean
sudo journalctl -u anime-picker -f
```

### 4. Setup Custom Domain

**Backend:**

- Add A record pointing to server IP
- Update SSL certificate
- Update CORS settings

**Frontend:**

- Configure in Vercel/Netlify dashboard
- Add CNAME record

---

## Monitoring & Maintenance

### Health Monitoring

Setup monitoring service (e.g., UptimeRobot):

- Monitor: `https://your-api-domain.com/health`
- Interval: Every 5 minutes
- Alert: Email/SMS on downtime

### Log Rotation

On AWS/DigitalOcean, setup log rotation:

```bash
sudo nano /etc/logrotate.d/anime-picker
```

```
/home/ubuntu/anime-picker/anime_picker.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
}
```

### Backup Strategy

1. **Database**: Backup `anime_clean.csv` and `anime_embeddings.pkl`
2. **Code**: Keep in Git repository
3. **Logs**: Archive important logs
4. **Frequency**: Weekly backups recommended

### Performance Monitoring

Consider adding:

- **Sentry**: Error tracking
- **New Relic**: Performance monitoring
- **DataDog**: Infrastructure monitoring

---

## Troubleshooting

### Common Issues

**1. Out of Memory**

```bash
# Solution: Upgrade instance or add swap
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

**2. Slow Model Loading**

```bash
# Solution: Keep server warm or use larger instance
# Add health check pings every 5 minutes
```

**3. CORS Errors**

```python
# Solution: Check CORS configuration
CORS(app, origins=["https://your-frontend.com"])
```

**4. 502 Bad Gateway**

```bash
# Solution: Check if gunicorn is running
sudo systemctl status anime-picker
sudo systemctl restart anime-picker
```

---

## Security Checklist

- [ ] HTTPS enabled (SSL certificate)
- [ ] CORS restricted to frontend domain
- [ ] Debug mode disabled
- [ ] Firewall configured
- [ ] SSH key authentication only
- [ ] Regular security updates
- [ ] Environment variables secured
- [ ] API rate limiting (future)
- [ ] Input validation enabled

---

## Cost Estimation

### Monthly Costs

| Platform     | Tier      | Cost | Notes                 |
| ------------ | --------- | ---- | --------------------- |
| Heroku       | Free      | $0   | Limited hours, sleeps |
| Heroku       | Hobby     | $7   | Always on             |
| Railway      | Free      | $0   | $5 credit/month       |
| AWS EC2      | t2.medium | $30  | Full control          |
| DigitalOcean | Basic     | $12  | 2 GB RAM              |
| Vercel       | Free      | $0   | Frontend only         |
| Netlify      | Free      | $0   | Frontend only         |

**Recommended Setup:**

- Backend: Railway ($0-5/month) or DigitalOcean ($12/month)
- Frontend: Vercel (Free)
- **Total**: $0-12/month

---

## Quick Deploy Commands

### Heroku

```bash
heroku create anime-picker-api
git push heroku main
heroku open
```

### Railway

```bash
railway init
railway up
railway domain
```

### AWS EC2

```bash
ssh -i key.pem ubuntu@ip
git clone your-repo
cd Backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
gunicorn app:app
```

---

## Support & Resources

- **Heroku Docs**: https://devcenter.heroku.com/
- **Railway Docs**: https://docs.railway.app/
- **AWS Docs**: https://docs.aws.amazon.com/
- **DigitalOcean Docs**: https://docs.digitalocean.com/
- **Nginx Docs**: https://nginx.org/en/docs/

---

**Deployment Guide Version:** 1.0  
**Last Updated:** 2025-11-20  
**Status:** Ready for Production 🚀
