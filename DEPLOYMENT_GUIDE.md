# 🚀 Complete Deployment Guide

## Quick Overview
- **Option 1**: Deploy on Render.com + Vercel (Free tier - recommended)
- **Option 2**: Deploy locally with Docker (recommended for development)
- **Option 3**: Self-hosted with Docker on your own server
- **Total Cost**: $0/month for all options

---

## 📋 Prerequisites
1. GitHub account (you already have the repo)
2. For Cloud Deployment:
   - Vercel account (free - sign up at vercel.com)
   - Render account (free - sign up at render.com)
3. For Docker Deployment:
   - Docker installed (`docker --version`)
   - Docker Compose installed (`docker-compose --version`)

---

## 🐳 Option 1: Deploy Locally with Docker (Quickest!)

### Prerequisites
```bash
# Check Docker installation
docker --version
docker-compose --version
```

### Step 1: Start All Services with One Command
```bash
cd /path/to/realtime_analytics_dashboard
docker-compose up
```

**That's it!** Your app is now running:
- 🌐 Frontend: http://localhost:3000
- 🔌 Backend API: http://localhost:8000
- 📊 API Health: http://localhost:8000/health

### Step 2: Verify Services Are Running
```bash
# In another terminal
docker-compose ps
# You should see both backend and frontend services running
```

### Step 3: Stop Services
```bash
docker-compose down
# Use -v flag to also remove volumes: docker-compose down -v
```

### Docker Useful Commands
```bash
# View logs
docker-compose logs backend      # Backend logs
docker-compose logs frontend     # Frontend logs
docker-compose logs -f backend   # Follow backend logs

# Rebuild images
docker-compose up --build

# Remove all containers and images
docker-compose down -v

# Access container shell
docker exec -it crypto_dashboard_backend bash
docker exec -it crypto_dashboard_frontend sh
```

### Environment in Docker
Docker Compose automatically sets:
- Backend URL: `http://backend:8000` (internal)
- WebSocket URL: `ws://backend:8000` (internal)
- Frontend accesses backend via service name `backend`

---

## Part 1: Deploy Backend on Render.com (Cloud)

### Step 1: Create Render Account
1. Go to https://render.com
2. Click "Get Started for Free"
3. Sign up with GitHub (recommended)

### Step 2: Create New Web Service
1. Click "New +" button (top right)
2. Select "Web Service"
3. Connect your GitHub repository: `GouthamUKS/Crypto_Analytics_Dashboard`
4. Click "Connect"

### Step 3: Configure Web Service
Fill in these settings:

- **Name**: `crypto-dashboard-backend` (or any name you prefer)
- **Region**: Choose closest to you (e.g., Oregon USA)
- **Branch**: `main`
- **Root Directory**: `backend`
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements-simple.txt`
- **Start Command**: `uvicorn app.main_simple:app --host 0.0.0.0 --port $PORT`
- **Instance Type**: `Free`

### Step 4: Add Environment Variables
Click "Advanced" → "Add Environment Variable"

Add these:
- **Key**: `ENVIRONMENT`  
  **Value**: `production`

- **Key**: `CORS_ORIGINS`  
  **Value**: `https://YOUR-VERCEL-APP.vercel.app`
  (We'll update this after deploying frontend)

### Step 5: Deploy
1. Click "Create Web Service"
2. Wait 3-5 minutes for deployment
3. Copy the URL (e.g., `https://crypto-dashboard-backend.onrender.com`)
4. **SAVE THIS URL** - you'll need it for frontend!

---

## Part 2: Deploy Frontend on Vercel

### Step 1: Create Vercel Account
1. Go to https://vercel.com
2. Click "Sign Up"
3. Choose "Continue with GitHub"
4. Authorize Vercel

### Step 2: Import Repository
1. Click "Add New..." → "Project"
2. Find `GouthamUKS/Crypto_Analytics_Dashboard`
3. Click "Import"

### Step 3: Configure Project Settings
**IMPORTANT**: Configure these settings:

- **Framework Preset**: `Create React App`
- **Root Directory**: `frontend` (click Edit → select `frontend`)
- **Build Command**: `npm run build`
- **Output Directory**: `build`
- **Install Command**: `npm install`

### Step 4: Add Environment Variables
Click "Environment Variables" section

Add these:
- **Key**: `REACT_APP_API_URL`  
  **Value**: `https://crypto-dashboard-backend.onrender.com` (YOUR Render URL from Part 1)

- **Key**: `REACT_APP_WS_URL`  
  **Value**: `wss://crypto-dashboard-backend.onrender.com` (YOUR Render URL with wss://)

### Step 5: Deploy
1. Click "Deploy"
2. Wait 2-3 minutes
3. Your app will be live at `https://YOUR-APP.vercel.app`

---

## Part 3: Final Configuration

### Update Backend CORS
1. Go back to Render.com
2. Open your backend service
3. Go to "Environment" tab
4. Update `CORS_ORIGINS` to your Vercel URL:
   ```
   https://YOUR-APP.vercel.app
   ```
5. Click "Save Changes"
6. Service will redeploy automatically

---

## 🎉 Testing Your Deployment

1. Visit your Vercel URL: `https://YOUR-APP.vercel.app`
2. You should see the crypto dashboard
3. Prices should update in real-time
4. If you see errors, check browser console (F12)

---

## 🐛 Troubleshooting

### Frontend shows "Cannot connect to server"
- Check if backend is running on Render
- Verify `REACT_APP_API_URL` matches your Render URL
- Check browser console for CORS errors

### Backend deployment fails
- Check Render logs for errors
- Verify `requirements-simple.txt` exists in `backend/` folder
- Make sure `app/main_simple.py` exists

### Vercel shows 404
1. Go to Vercel project settings
2. Click "General"
3. Verify "Root Directory" is set to `frontend`
4. Click "Redeploy" from Deployments tab

### CORS Errors
1. Go to Render backend settings
2. Check `CORS_ORIGINS` environment variable
3. Make sure it matches your Vercel URL exactly (with https://)
4. No trailing slash!

---

## 📊 Free Tier Limits

### Render.com Free Tier
- 750 hours/month (always on for one service)
- Auto-sleeps after 15 min of inactivity
- Takes ~30 seconds to wake up on first request
- 512 MB RAM
- **Perfect for this project!**

### Vercel Free Tier
- 100 GB bandwidth/month
- Unlimited deployments
- Automatic HTTPS
- Global CDN
- **More than enough!**

---

## 🔄 Updating Your App

### Update Code
1. Make changes locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update features"
   git push origin main
   ```
3. Vercel redeploys automatically
4. Render redeploys automatically

That's it! Both services auto-deploy on git push.

---

## 🐳 Option 2: Self-Hosted Docker Deployment

### On Your Own Server (AWS EC2, DigitalOcean, Linode, etc.)

#### Step 1: Server Setup
```bash
# SSH into your server
ssh ubuntu@your-server-ip

# Install Docker and Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group (avoid using sudo)
sudo usermod -aG docker $USER
```

#### Step 2: Clone Repository
```bash
git clone https://github.com/GouthamUKS/Crypto_Analytics_Dashboard.git
cd realtime_analytics_dashboard
```

#### Step 3: Update Environment Variables
```bash
# Edit docker-compose.yml for production
nano docker-compose.yml

# Update ALLOWED_ORIGINS to your domain:
# ALLOWED_ORIGINS: http://localhost:3000,http://your-domain.com,https://your-domain.com
```

#### Step 4: Start Services with Nginx Reverse Proxy
```bash
# Create nginx config
sudo nano /etc/nginx/sites-available/crypto-dashboard

# Add this configuration:
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /ws {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_set_header Host $host;
    }
}

# Enable the site
sudo ln -s /etc/nginx/sites-available/crypto-dashboard /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

#### Step 5: Run Docker Compose
```bash
# Run in background with detach
docker-compose up -d

# Verify services
docker-compose ps

# View logs
docker-compose logs -f
```

#### Step 6: Optional - Add SSL with Let's Encrypt
```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renew certs
sudo systemctl enable certbot.timer
```

#### Management Commands
```bash
# Restart services
docker-compose restart

# Update app (pull latest code)
git pull
docker-compose up -d --build

# View service status
docker-compose ps

# Check logs
docker-compose logs backend
docker-compose logs frontend

# Stop all services
docker-compose stop

# Remove everything (careful!)
docker-compose down -v
```

### Cost Estimates (Self-Hosted)
- **DigitalOcean Droplet** (Basic): $5-6/month
- **AWS EC2 Free Tier**: $0 (first year)
- **Linode**: $5/month (basic)
- **Vultr**: $2.50-6/month

---

## 🎨 Custom Domain (Optional)

### On Vercel
1. Go to Project Settings → Domains
2. Add your custom domain
3. Follow DNS configuration steps

### On Render
1. Go to Service Settings → Custom Domain
2. Add your domain
3. Update DNS records

### On Self-Hosted
1. Update DNS records to point to server IP
2. Configure Nginx as shown above
3. Get SSL certificate with Let's Encrypt

---

## 📊 Deployment Comparison

| Feature | Docker Local | Render/Vercel | Self-Hosted Docker |
|---------|--------------|---------------|-------------------|
| Cost | $0 | $0 (free tiers) | $5-50/month |
| Setup Time | 2 minutes | 10 minutes | 15-30 minutes |
| Best For | Development | Production (easy) | Full Control |
| Scaling | Manual | Auto | Manual |
| SSL | Not needed | Automatic | Let's Encrypt |
| Maintenance | Minimal | Minimal | More involved |
| Performance | Local | Good (CDN) | Depends on server |

---

## 📞 Need Help?

Common issues:
1. **Backend sleeping**: First request takes 30s (Render free tier)
2. **CORS errors**: Double-check environment variables
3. **Build errors**: Check deployment logs in Render/Vercel dashboard

---

## ✅ Final Checklist

- [ ] Backend deployed on Render
- [ ] Frontend deployed on Vercel
- [ ] Environment variables set correctly
- [ ] CORS configured with Vercel URL
- [ ] App loads and shows data
- [ ] Real-time updates working
- [ ] No console errors

---

## 🎯 Your Live URLs

Backend: `https://crypto-dashboard-backend.onrender.com`  
Frontend: `https://YOUR-APP.vercel.app`

**Share your frontend URL - that's your live app!** 🚀
