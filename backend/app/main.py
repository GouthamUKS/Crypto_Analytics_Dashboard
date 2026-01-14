from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import datetime, timedelta
import asyncio
import os

# For deployment without database - use main_simple.py instead
# This file requires PostgreSQL, Redis, and other dependencies

# Initialize FastAPI app
app = FastAPI(
    title="Crypto Analytics Dashboard",
    version="1.0.0",
    description="Real-time Crypto Analytics Dashboard API"
)

# Get allowed origins from environment
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000"
).split(",")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Default tracked symbols
TRACKED_SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "SOLUSDT"]


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Crypto Analytics Dashboard",
        "message": "Use main_simple.py for deployment without database",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/api/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "note": "This is the database version - use main_simple.py for simple deployment",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/api/cryptos")
async def get_tracked_cryptos():
    """Get list of tracked cryptocurrencies"""
    return {
        "symbols": TRACKED_SYMBOLS,
        "count": len(TRACKED_SYMBOLS),
        "note": "Database features disabled - use main_simple.py"
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print("⚠️  Note: This version requires database setup")
    print("💡 For simple deployment, use: python app/main_simple.py")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=False
    )