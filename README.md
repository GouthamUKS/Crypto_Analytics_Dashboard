# Real-Time Crypto Analytics Dashboard 📊

A modern, real-time cryptocurrency analytics dashboard with live price updates, interactive charts, and a sleek glassmorphism UI design. Built with FastAPI and React.

## ✨ Features

- **Real-time Price Updates**: WebSocket-based live cryptocurrency price streaming
- **Interactive Charts**: Beautiful Chart.js visualizations with historical data
- **Modern UI Design**: Dark theme with glassmorphism effects and smooth animations
- **5 Major Cryptocurrencies**: BTC, ETH, BNB, SOL, ADA tracking
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Zero Database Required**: Simplified architecture for easy deployment
- **Free Deployment**: Deploy on Render.com + Vercel at $0/month

## 🏗️ Architecture (Simplified)

```
┌─────────────────┐     WebSocket      ┌──────────────────┐
│  Price Engine   │ ───────────────▶  │   FastAPI        │
│  (Simulated)    │                    │   Backend        │
└─────────────────┘                    └────────┬─────────┘
                                                │
                                                │ WebSocket
                                                │
                                        ┌───────▼─────────┐
                                        │  React Frontend │
                                        │  (Chart.js)     │
                                        └─────────────────┘
```

## 🎨 UI Features

- **Dark Theme**: Modern #0a0e27 background with purple gradients
- **Glassmorphism**: Frosted glass effects with backdrop blur
- **Gradient Text**: Eye-catching blue-to-purple-to-pink gradients
- **Live Animations**: Ping effects on real-time updates
- **Responsive Cards**: Adaptive layout for all screen sizes

## 📁 Project Structure

```
realtime_analytics_dashboard/
├── backend/                 # Python FastAPI backend
│   ├── app/
│   │   ├── main_simple.py  # Production entry point
│   │   ├── websocket.py    # WebSocket connection manager
│   │   └── __init__.py
│   ├── requirements-simple.txt
│   ├── render.yaml         # Render.com config
│   └── Dockerfile
├── frontend/               # React frontend
│   ├── src/
│   │   ├── App.jsx        # Main application
│   │   ├── index.css      # Modern styling
│   │   └── components/
│   │       ├── CryptoCard.jsx
│   │       └── PriceChart.jsx
│   ├── package.json
│   ├── vercel.json        # Vercel config
│   └── public/
├── DEPLOYMENT_GUIDE.md    # Complete deployment instructions
├── DEPLOYMENT_HISTORY.md  # Deployment tracking
└── README.md             # This file
```


## 🛠️ Tech Stack

### Backend
- **FastAPI 0.109.0**: High-performance Python web framework
- **Uvicorn**: ASGI server for production
- **WebSockets**: Real-time bidirectional communication
- **Pydantic**: Data validation and settings management

### Frontend
- **React 18.2**: Modern UI framework
- **Chart.js 4.4**: Interactive price charts
- **Axios**: HTTP client for API calls
- **CSS Variables**: Dynamic theming system

### Deployment
- **Render.com**: Backend hosting (free tier)
- **Vercel**: Frontend hosting (free tier)
- **GitHub**: Version control and CI/CD

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Git

### Local Development

#### 1. Clone Repository
```bash
git clone https://github.com/GouthamUKS/Crypto_Analytics_Dashboard.git
cd realtime_analytics_dashboard
```

#### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements-simple.txt

# Start backend server
python app/main_simple.py
# Backend runs at http://localhost:8000
```

#### 3. Frontend Setup
```bash
cd frontend
npm install

# Start development server
npm start
# Frontend runs at http://localhost:3000
```

#### 4. Open Browser
Visit http://localhost:3000 to see your dashboard!

## 🌐 Production Deployment

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for complete step-by-step instructions.

### Quick Deploy Summary:
1. **Backend**: Deploy to Render.com (3 minutes)
2. **Frontend**: Deploy to Vercel (2 minutes)
3. **Cost**: $0/month (both free tiers)

### Deployment Resources:
- 📖 [Complete Deployment Guide](DEPLOYMENT_GUIDE.md)
- 📊 [Deployment History](DEPLOYMENT_HISTORY.md)
- 🔧 [Architecture Docs](ARCHITECTURE.md)

# Submit Spark job
spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 \
  streaming_processor.py
```

#### 4. Frontend Setup
```bash
cd frontend
npm install


## 🔧 Configuration

### Environment Variables

#### Backend (Optional)
```env
# Production
ENVIRONMENT=production
ALLOWED_ORIGINS=https://your-app.vercel.app

# Local Development (defaults)
ENVIRONMENT=development
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

#### Frontend (For Production)
```env
# Vercel Environment Variables
REACT_APP_API_URL=https://your-backend.onrender.com
REACT_APP_WS_URL=wss://your-backend.onrender.com
```

## 📊 Features in Detail

### 1. Real-Time Price Tracking
- ✅ Live price updates every 2-3 seconds
- ✅ 5 major cryptocurrencies (BTC, ETH, BNB, SOL, ADA)
- ✅ Percentage change indicators
- ✅ Smooth animations on updates

### 2. Interactive Charts
- ✅ Historical price visualization
- ✅ 20-point rolling data window
- ✅ Gradient fill effects
- ✅ Responsive canvas rendering

### 3. Modern UI/UX
- ✅ Dark theme optimized for extended viewing
- ✅ Glassmorphism cards with backdrop blur
- ✅ Gradient text effects
- ✅ Mobile-responsive design
- ✅ Smooth fade-in animations

## 🎯 API Endpoints

### Health Check
```bash
GET http://localhost:8000/health
Response: {"status": "healthy"}
```

### WebSocket Connection
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/BTCUSDT');
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(data); // { symbol, price, change24h, timestamp }
};
```

### Supported Symbols
- `BTCUSDT` - Bitcoin
- `ETHUSDT` - Ethereum
- `BNBUSDT` - BNB
- `SOLUSDT` - Solana
- `ADAUSDT` - Cardano

```


## 🧪 Testing

### Local Testing
```bash
# Test backend
cd backend
source venv/bin/activate
python app/main_simple.py
# Visit http://localhost:8000/health

# Test frontend
cd frontend
npm start
# Visit http://localhost:3000
```

### WebSocket Testing
```bash
# Using wscat (install: npm install -g wscat)
wscat -c ws://localhost:8000/ws/BTCUSDT
# You should see real-time price updates
```

## 📂 Project Files

### Key Files
- [`backend/app/main_simple.py`](backend/app/main_simple.py) - Production backend
- [`backend/app/websocket.py`](backend/app/websocket.py) - WebSocket manager
- [`frontend/src/App.jsx`](frontend/src/App.jsx) - Main React app
- [`frontend/src/index.css`](frontend/src/index.css) - Modern styling
- [`backend/render.yaml`](backend/render.yaml) - Render config
- [`frontend/vercel.json`](frontend/vercel.json) - Vercel config

### Documentation
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Step-by-step deployment
- [DEPLOYMENT_HISTORY.md](DEPLOYMENT_HISTORY.md) - Deployment tracking
- [API.md](API.md) - API documentation
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture

## 🎨 Customization

### Adding New Cryptocurrencies
Edit [`backend/app/main_simple.py`](backend/app/main_simple.py):
```python
symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "ADAUSDT", "DOGEUSDT"]  # Add more
```

### Changing Update Frequency
```python
await asyncio.sleep(3)  # Change from 3 to desired seconds
```

### Customizing UI Colors
Edit [`frontend/src/index.css`](frontend/src/index.css):
```css
--bg-primary: #0a0e27;     /* Main background */
--accent-blue: #667eea;    /* Blue accent */
--accent-purple: #764ba2;  /* Purple accent */
```

## 📊 Live Demo

- **GitHub Repository**: https://github.com/GouthamUKS/Crypto_Analytics_Dashboard
- **Backend**: Deploy on Render.com (see deployment guide)
- **Frontend**: Deploy on Vercel (see deployment guide)

## 🤝 Contributing

Contributions are welcome! 

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

MIT License - feel free to use this project for learning or commercial purposes.

## 🙏 Acknowledgments

- FastAPI team for the amazing framework
- React and Chart.js communities
- Render.com and Vercel for free hosting

## 📞 Support

- 📧 Open an issue on GitHub
- 📖 Check [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for deployment help
- 💡 Review [DEPLOYMENT_HISTORY.md](DEPLOYMENT_HISTORY.md) for configuration details

---

**Built with ❤️ using FastAPI + React | Deployed on Render + Vercel**
