# 🚀 Quick Deployment Guide

Your code is now on GitHub! Follow these steps to deploy:

## ✅ Step 1: Deploy Frontend to Vercel (3 minutes)

1. Go to https://vercel.com
2. Click **"Sign Up"** (use GitHub - it's free!)
3. Click **"Add New..."** → **"Project"**
4. Select **"Crypto_Analytics_Dashboard"** from your repos
5. Configure:
   - **Root Directory**: Click **"Edit"** → Enter: `frontend`
   - **Framework Preset**: Create React App (auto-detected)
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
   
6. Add **Environment Variables**:
   - Click **"Environment Variables"**
   - Add: `REACT_APP_API_URL` = `https://YOUR-BACKEND.onrender.com` (get this from Step 2)
   - Add: `REACT_APP_WS_URL` = `wss://YOUR-BACKEND.onrender.com` (get this from Step 2)
   
7. Click **"Deploy"**

⏳ Wait 2-3 minutes... Your frontend will be live at: `https://your-app.vercel.app`

---

## ✅ Step 2: Deploy Backend to Render (5 minutes)

1. Go to https://render.com
2. Click **"Get Started"** (use GitHub - FREE, no credit card!)
3. Click **"New +"** → **"Web Service"**
4. Connect your GitHub → Select **"Crypto_Analytics_Dashboard"**
5. Configure:
   - **Name**: `crypto-analytics-backend`
   - **Region**: Choose closest to you
   - **Root Directory**: `backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements-simple.txt`
   - **Start Command**: `python app/main_simple.py`
   - **Plan**: **FREE**
   
6. Add **Environment Variable**:
   - Click **"Advanced"** → **"Add Environment Variable"**
   - Key: `ALLOWED_ORIGINS`
   - Value: `https://your-app.vercel.app` (copy from Step 1)
   
7. Click **"Create Web Service"**

⏳ Wait 3-5 minutes... Your backend will be live!

**Copy your Render URL**: `https://crypto-analytics-backend-xxxx.onrender.com`

---

## ✅ Step 3: Connect Frontend to Backend

1. Go back to **Vercel** dashboard
2. Click your project → **"Settings"** → **"Environment Variables"**
3. Update the variables with your **Render URL** from Step 2:
   - `REACT_APP_API_URL` = `https://YOUR-RENDER-URL.onrender.com`
   - `REACT_APP_WS_URL` = `wss://YOUR-RENDER-URL.onrender.com`
4. Click **"Save"**
5. Go to **"Deployments"** → Click **"..."** → **"Redeploy"**

---

## 🎉 You're Live!

After ~2 minutes, visit your Vercel URL and enjoy your live dashboard!

### ⚠️ First Load Tip
Free Render services sleep after 15 min. First visit may take 30-50 seconds to wake up.

### 🔄 Future Updates
Just push to GitHub - both services auto-deploy!
```bash
git add .
git commit -m "Update feature"
git push
```

---

## 📊 Your Live URLs

- **Frontend (Vercel)**: https://your-app.vercel.app
- **Backend (Render)**: https://crypto-analytics-backend-xxxx.onrender.com
- **GitHub**: https://github.com/GouthamUKS/Crypto_Analytics_Dashboard

---

## 🎯 Quick Links

- [Vercel Dashboard](https://vercel.com/dashboard)
- [Render Dashboard](https://dashboard.render.com)
- [Full Deployment Guide](DEPLOYMENT.md)

**Total Time**: ~10 minutes  
**Total Cost**: $0 (100% FREE!)

Happy deploying! 🚀
