# Crypto Analytics Dashboard

A stunning real-time cryptocurrency analytics dashboard with live price updates, interactive charts, and modern glassmorphism UI.

![Dashboard Preview](https://img.shields.io/badge/Status-Live-success)
![License](https://img.shields.io/badge/License-MIT-blue)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![React](https://img.shields.io/badge/React-18.2-blue)

## ✨ Features

- 🔴 **Real-time Price Updates** - Live cryptocurrency prices updating every 2 seconds via WebSocket
- 📊 **Interactive Charts** - Beautiful Chart.js visualizations showing 24h price history
- 🎨 **Modern UI** - Sleek dark theme with glassmorphism effects and smooth animations
- ⚡ **Fast & Responsive** - Optimized performance with real-time data streaming
- 📱 **Mobile Friendly** - Fully responsive design works on all devices

## 🚀 Live Demo

- **Frontend**: [Your Vercel URL]
- **Backend API**: [Your Render URL]

## 🛠️ Tech Stack

### Frontend
- React 18.2
- Chart.js for visualizations
- WebSocket for real-time updates
- Modern CSS with glassmorphism

### Backend
- FastAPI (Python)
- WebSocket support
- Simulated real-time crypto data
- CORS-enabled REST API

## 📦 Installation & Running Locally

### Prerequisites
- Python 3.9+
- Node.js 16+
- npm or yarn

### Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements-simple.txt
python app/main_simple.py
```

Backend will run on `http://localhost:8000`

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

Frontend will run on `http://localhost:3000`

## 🌐 Deployment

Deploy this app **100% FREE** using Render.com (backend) and Vercel (frontend).

**📖 See detailed instructions in [DEPLOYMENT.md](DEPLOYMENT.md)**

Quick steps:
1. Push code to GitHub
2. Deploy backend to Render.com (free tier)
3. Deploy frontend to Vercel (free tier)
4. Update environment variables
5. Done! 🎉

## 🎯 API Endpoints

### REST API
- `GET /` - Health check
- `GET /api/health` - Detailed health status
- `GET /api/cryptos` - List of tracked cryptocurrencies
- `GET /api/prices/{symbol}` - Current price for a symbol
- `GET /api/historical/{symbol}` - Historical price data

### WebSocket
- `WS /ws` - Real-time price updates
  - Subscribe: `{"action": "subscribe", "symbol": "BTCUSDT"}`
  - Unsubscribe: `{"action": "unsubscribe", "symbol": "BTCUSDT"}`

## 📊 Tracked Cryptocurrencies

- Bitcoin (BTC)
- Ethereum (ETH)
- Binance Coin (BNB)
- Cardano (ADA)
- Solana (SOL)

## 🎨 UI Features

- **Dark Theme** - Easy on the eyes with a modern dark color scheme
- **Glassmorphism** - Frosted glass effect cards with backdrop blur
- **Gradient Accents** - Beautiful blue-purple-pink gradients
- **Smooth Animations** - Fade-in effects and hover transitions
- **Live Indicators** - Pulsing connection status indicator
- **Price Badges** - Color-coded positive/negative price changes

## 📝 License

MIT License - feel free to use this project for learning or your portfolio!

## 🙏 Acknowledgments

- Price data simulation based on real crypto market behavior
- UI inspired by modern design trends
- Built for students learning full-stack development

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 📧 Contact

Questions? Open an issue or reach out!

---

**Made with ❤️ for the crypto community**

⭐ Star this repo if you found it helpful!
