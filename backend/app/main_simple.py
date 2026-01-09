from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List
from datetime import datetime, timedelta
import asyncio
import json
import random
import os

# Initialize FastAPI app
app = FastAPI(
    title="Crypto Analytics Dashboard",
    version="1.0.0",
    description="Real-time Crypto Analytics Dashboard API"
)

# Get allowed origins from environment variable or use defaults
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

# In-memory storage
price_data: Dict[str, Dict] = {}
historical_data: Dict[str, List] = {symbol: [] for symbol in TRACKED_SYMBOLS}

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.subscriptions: Dict[WebSocket, set] = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.subscriptions[websocket] = set()

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        if websocket in self.subscriptions:
            del self.subscriptions[websocket]

    async def subscribe(self, websocket: WebSocket, symbol: str):
        if websocket in self.subscriptions:
            self.subscriptions[websocket].add(symbol)

    async def unsubscribe(self, websocket: WebSocket, symbol: str):
        if websocket in self.subscriptions:
            self.subscriptions[websocket].discard(symbol)

    async def broadcast(self, symbol: str, message: dict):
        disconnected = []
        for connection in self.active_connections:
            if symbol in self.subscriptions.get(connection, set()):
                try:
                    await connection.send_json(message)
                except:
                    disconnected.append(connection)
        
        for connection in disconnected:
            self.disconnect(connection)

manager = ConnectionManager()

# Initial prices (approximate current values)
INITIAL_PRICES = {
    "BTCUSDT": 45000.0,
    "ETHUSDT": 2500.0,
    "BNBUSDT": 350.0,
    "ADAUSDT": 0.55,
    "SOLUSDT": 110.0
}

# Symbol to name mapping
SYMBOL_NAMES = {
    "BTCUSDT": "Bitcoin",
    "ETHUSDT": "Ethereum",
    "BNBUSDT": "Binance Coin",
    "ADAUSDT": "Cardano",
    "SOLUSDT": "Solana"
}

# Initialize price data
for symbol in TRACKED_SYMBOLS:
    base_price = INITIAL_PRICES.get(symbol, 100.0)
    price_data[symbol] = {
        "symbol": symbol,
        "name": SYMBOL_NAMES.get(symbol, symbol),
        "price": base_price,
        "volume_24h": random.uniform(1e9, 10e9),
        "price_change_24h": random.uniform(-5, 5),
        "high_24h": base_price * 1.05,
        "low_24h": base_price * 0.95,
        "timestamp": datetime.utcnow().isoformat()
    }


async def simulate_price_updates():
    """Background task to simulate real-time price updates"""
    while True:
        for symbol in TRACKED_SYMBOLS:
            # Simulate price change
            current_price = price_data[symbol]["price"]
            change_percent = random.uniform(-0.5, 0.5) / 100
            new_price = current_price * (1 + change_percent)
            
            # Update price data
            price_data[symbol]["price"] = new_price
            price_data[symbol]["volume_24h"] = random.uniform(1e9, 10e9)
            price_data[symbol]["timestamp"] = datetime.utcnow().isoformat()
            
            # Add to historical data
            historical_entry = {
                "price": new_price,
                "volume": price_data[symbol]["volume_24h"],
                "timestamp": datetime.utcnow().isoformat()
            }
            historical_data[symbol].append(historical_entry)
            
            # Keep only last 100 entries
            if len(historical_data[symbol]) > 100:
                historical_data[symbol] = historical_data[symbol][-100:]
            
            # Broadcast update
            await manager.broadcast(symbol, {
                "type": "price_update",
                **price_data[symbol]
            })
        
        await asyncio.sleep(2)  # Update every 2 seconds


@app.on_event("startup")
async def startup_event():
    """Initialize background tasks"""
    asyncio.create_task(simulate_price_updates())
    print("✓ Backend server started")
    print("✓ Price simulation started")


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Crypto Analytics Dashboard",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/api/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "websocket": "active",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/api/cryptos")
async def get_tracked_cryptos():
    """Get list of tracked cryptocurrencies"""
    return {
        "symbols": TRACKED_SYMBOLS,
        "count": len(TRACKED_SYMBOLS)
    }


@app.get("/api/prices/{symbol}")
async def get_current_price(symbol: str):
    """Get current price for a specific cryptocurrency"""
    symbol = symbol.upper()
    if symbol not in price_data:
        return {"error": "Symbol not found"}, 404
    
    return price_data[symbol]


@app.get("/api/historical/{symbol}")
async def get_historical_data(symbol: str, hours: int = 24):
    """Get historical price data for a symbol"""
    symbol = symbol.upper()
    if symbol not in historical_data:
        return {"error": "Symbol not found"}, 404
    
    return {
        "symbol": symbol,
        "data": historical_data[symbol]
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time data streaming"""
    await manager.connect(websocket)
    
    try:
        # Send initial connection confirmation
        await websocket.send_json({
            "type": "connection",
            "status": "connected",
            "timestamp": datetime.utcnow().isoformat()
        })
        
        while True:
            # Receive messages from client
            data = await websocket.receive_json()
            
            if data.get("action") == "subscribe":
                symbol = data.get("symbol", "").upper()
                if symbol in TRACKED_SYMBOLS:
                    await manager.subscribe(websocket, symbol)
                    await websocket.send_json({
                        "type": "subscription",
                        "status": "subscribed",
                        "symbol": symbol
                    })
                    # Send current price immediately
                    if symbol in price_data:
                        await websocket.send_json({
                            "type": "price_update",
                            **price_data[symbol]
                        })
                    
            elif data.get("action") == "unsubscribe":
                symbol = data.get("symbol", "").upper()
                await manager.unsubscribe(websocket, symbol)
                await websocket.send_json({
                    "type": "subscription",
                    "status": "unsubscribed",
                    "symbol": symbol
                })
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main_simple:app",
        host="0.0.0.0",
        port=port,
        reload=False
    )
