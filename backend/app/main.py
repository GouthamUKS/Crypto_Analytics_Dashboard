from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional, TYPE_CHECKING
from datetime import datetime, timedelta
import asyncio

if TYPE_CHECKING:
    import uvicorn

from app.config import get_settings
from app.database import get_db, init_db
from app.models import CryptoPrice, SentimentScore, AggregatedMetrics, MarketAlert
from app.websocket import manager, BinanceStreamClient, CoinGeckoClient
from pydantic import BaseModel

settings = get_settings()

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Real-time Crypto Analytics Dashboard API"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Default tracked symbols
TRACKED_SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "SOLUSDT"]

# Global clients
binance_client = None
coingecko_client = None


# Pydantic models for API
class PriceResponse(BaseModel):
    symbol: str
    name: str
    price: float
    volume_24h: Optional[float]
    price_change_24h: Optional[float]
    timestamp: datetime
    
    class Config:
        from_attributes = True


class MetricsResponse(BaseModel):
    symbol: str
    window_start: datetime
    window_end: datetime
    avg_price: Optional[float]
    vwap: Optional[float]
    total_volume: Optional[float]
    price_volatility: Optional[float]
    avg_sentiment: Optional[float]
    
    class Config:
        from_attributes = True


@app.on_event("startup")
async def startup_event():
    """Initialize database and start background tasks"""
    global binance_client, coingecko_client
    
    # Initialize database
    init_db()
    print("Database initialized")
    
    # Initialize WebSocket clients
    binance_client = BinanceStreamClient(TRACKED_SYMBOLS)
    await binance_client.connect()
    
    coingecko_client = CoinGeckoClient()
    await coingecko_client.connect()
    
    # Start background task for Binance stream
    asyncio.create_task(binance_client.stream_prices())
    print("Binance WebSocket stream started")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    if binance_client:
        await binance_client.disconnect()
    if coingecko_client:
        await coingecko_client.disconnect()


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": settings.app_name,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/api/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": "connected",
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


@app.get("/api/prices/{symbol}", response_model=PriceResponse)
async def get_current_price(symbol: str, db: Session = Depends(get_db)):
    """Get current price for a specific cryptocurrency"""
    # Get latest price from database
    latest = db.query(CryptoPrice).filter(
        CryptoPrice.symbol == symbol.upper()
    ).order_by(CryptoPrice.timestamp.desc()).first()
    
    if not latest:
        raise HTTPException(status_code=404, detail="Symbol not found")
    
    return latest


@app.get("/api/historical/{symbol}")
async def get_historical_data(
    symbol: str,
    hours: int = 24,
    db: Session = Depends(get_db)
):
    """Get historical price data for a symbol"""
    time_threshold = datetime.utcnow() - timedelta(hours=hours)
    
    prices = db.query(CryptoPrice).filter(
        CryptoPrice.symbol == symbol.upper(),
        CryptoPrice.timestamp >= time_threshold
    ).order_by(CryptoPrice.timestamp.asc()).all()
    
    return {
        "symbol": symbol,
        "data": [
            {
                "price": p.price,
                "volume": p.volume_24h,
                "timestamp": p.timestamp.isoformat()
            }
            for p in prices
        ]
    }


@app.get("/api/metrics/{symbol}", response_model=List[MetricsResponse])
async def get_aggregated_metrics(
    symbol: str,
    hours: int = 24,
    db: Session = Depends(get_db)
):
    """Get aggregated metrics from Spark processing"""
    time_threshold = datetime.utcnow() - timedelta(hours=hours)
    
    metrics = db.query(AggregatedMetrics).filter(
        AggregatedMetrics.symbol == symbol.upper(),
        AggregatedMetrics.window_start >= time_threshold
    ).order_by(AggregatedMetrics.window_start.asc()).all()
    
    return metrics


@app.get("/api/sentiment/{symbol}")
async def get_sentiment(
    symbol: str,
    hours: int = 24,
    db: Session = Depends(get_db)
):
    """Get sentiment scores for a symbol"""
    time_threshold = datetime.utcnow() - timedelta(hours=hours)
    
    sentiments = db.query(SentimentScore).filter(
        SentimentScore.symbol == symbol.upper(),
        SentimentScore.timestamp >= time_threshold
    ).order_by(SentimentScore.timestamp.desc()).all()
    
    return {
        "symbol": symbol,
        "data": [
            {
                "score": s.sentiment_score,
                "source": s.source,
                "confidence": s.confidence,
                "timestamp": s.timestamp.isoformat()
            }
            for s in sentiments
        ]
    }


@app.get("/api/alerts")
async def get_active_alerts(db: Session = Depends(get_db)):
    """Get active market alerts"""
    alerts = db.query(MarketAlert).filter(
        MarketAlert.is_active == True
    ).order_by(MarketAlert.created_at.desc()).all()
    
    return {
        "alerts": [
            {
                "id": a.id,
                "symbol": a.symbol,
                "type": a.alert_type,
                "severity": a.severity,
                "message": a.message,
                "created_at": a.created_at.isoformat()
            }
            for a in alerts
        ]
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
    uvicorn.run(
        "app.main:app",
        host=settings.backend_host,
        port=settings.backend_port,
        reload=settings.debug
    )
