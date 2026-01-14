# 🚀 Complete Deployment Guide

## Quick Overview
- **Backend**: Deploy on Render.com (Free tier)
- **Frontend**: Deploy on Vercel (Free tier)
- **Total Cost**: $0/month

---

## 📋 Prerequisites
1. GitHub account (you already have the repo)
2. Vercel account (free - sign up at vercel.com)
3. Render account (free - sign up at render.com)

---

## Part 1: Deploy Backend on Render.com

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

## 🎨 Custom Domain (Optional)

### On Vercel
1. Go to Project Settings → Domains
2. Add your custom domain
3. Follow DNS configuration steps

### On Render
1. Go to Service Settings → Custom Domain
2. Add your domain
3. Update DNS records

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
