import asyncio
import json
import websockets
from typing import Set, Dict, Any
from datetime import datetime
from fastapi import WebSocket, WebSocketDisconnect
import aiohttp
from app.config import get_settings
try:
    import redis.asyncio as redis
except ImportError:
    import redis

settings = get_settings()


class ConnectionManager:
    """Manages WebSocket connections to clients"""
    
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        self.subscriptions: Dict[str, Set[WebSocket]] = {}
        
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
        
    def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)
        # Remove from all subscriptions
        for symbol_set in self.subscriptions.values():
            symbol_set.discard(websocket)
            
    async def subscribe(self, websocket: WebSocket, symbol: str):
        """Subscribe a client to a specific symbol"""
        if symbol not in self.subscriptions:
            self.subscriptions[symbol] = set()
        self.subscriptions[symbol].add(websocket)
        
    async def unsubscribe(self, websocket: WebSocket, symbol: str):
        """Unsubscribe a client from a symbol"""
        if symbol in self.subscriptions:
            self.subscriptions[symbol].discard(websocket)
            
    async def broadcast(self, message: Dict[str, Any]):
        """Broadcast message to all connected clients"""
        disconnected = set()
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except WebSocketDisconnect:
                disconnected.add(connection)
            except Exception:
                disconnected.add(connection)
                
        # Clean up disconnected clients
        for conn in disconnected:
            self.disconnect(conn)
            
    async def send_to_symbol_subscribers(self, symbol: str, message: Dict[str, Any]):
        """Send message to all subscribers of a specific symbol"""
        if symbol not in self.subscriptions:
            return
            
        disconnected = set()
        for connection in self.subscriptions[symbol]:
            try:
                await connection.send_json(message)
            except WebSocketDisconnect:
                disconnected.add(connection)
            except Exception:
                disconnected.add(connection)
                
        # Clean up disconnected clients
        for conn in disconnected:
            self.disconnect(conn)


manager = ConnectionManager()


class BinanceStreamClient:
    """Client for connecting to Binance WebSocket streams"""
    
    def __init__(self, symbols: list[str]):
        self.symbols = [s.lower() for s in symbols]
        self.ws_url = self._build_ws_url()
        self.redis_client = None
        
    def _build_ws_url(self) -> str:
        """Build Binance WebSocket URL for multiple symbols"""
        streams = [f"{symbol}@trade" for symbol in self.symbols]
        streams.extend([f"{symbol}@ticker" for symbol in self.symbols])
        return f"{settings.binance_ws_url}/stream?streams={'/'.join(streams)}"
        
    async def connect(self):
        """Connect to Redis for caching"""
        self.redis_client = await redis.from_url(settings.redis_url)
        
    async def disconnect(self):
        """Disconnect from Redis"""
        if self.redis_client:
            await self.redis_client.close()
            
    async def stream_prices(self):
        """Stream real-time prices from Binance"""
        while True:
            try:
                async with websockets.connect(self.ws_url) as websocket:
                    print(f"Connected to Binance WebSocket: {self.ws_url}")
                    
                    async for message in websocket:
                        data = json.loads(message)
                        await self._process_message(data)
                        
            except websockets.exceptions.WebSocketException as e:
                print(f"WebSocket error: {e}")
                await asyncio.sleep(5)  # Wait before reconnecting
            except Exception as e:
                print(f"Unexpected error: {e}")
                await asyncio.sleep(5)
                
    async def _process_message(self, data: Dict[str, Any]):
        """Process incoming WebSocket message"""
        if 'stream' not in data:
            return
            
        stream = data['stream']
        stream_data = data['data']
        
        if '@ticker' in stream:
            # Process ticker data
            processed = {
                'type': 'price_update',
                'symbol': stream_data['s'],
                'price': float(stream_data['c']),
                'price_change_24h': float(stream_data['P']),
                'volume_24h': float(stream_data['v']),
                'high_24h': float(stream_data['h']),
                'low_24h': float(stream_data['l']),
                'timestamp': datetime.fromtimestamp(stream_data['E'] / 1000).isoformat()
            }
            
            # Cache in Redis
            if self.redis_client:
                await self.redis_client.setex(
                    f"price:{processed['symbol']}",
                    60,  # Cache for 60 seconds
                    json.dumps(processed)
                )
            
            # Broadcast to WebSocket clients
            await manager.send_to_symbol_subscribers(
                processed['symbol'],
                processed
            )
            
        elif '@trade' in stream:
            # Process trade data
            processed = {
                'type': 'trade',
                'symbol': stream_data['s'],
                'price': float(stream_data['p']),
                'quantity': float(stream_data['q']),
                'is_buyer_maker': stream_data['m'],
                'timestamp': datetime.fromtimestamp(stream_data['T'] / 1000).isoformat()
            }
            
            # Broadcast to WebSocket clients
            await manager.send_to_symbol_subscribers(
                processed['symbol'],
                processed
            )


class CoinGeckoClient:
    """Client for fetching additional market data from CoinGecko"""
    
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.redis_client = None
        
    async def connect(self):
        """Connect to Redis for caching"""
        self.redis_client = await redis.from_url(settings.redis_url)
        
    async def disconnect(self):
        """Disconnect from Redis"""
        if self.redis_client:
            await self.redis_client.close()
            
    async def fetch_market_data(self, symbols: list[str]):
        """Fetch market data for multiple cryptocurrencies"""
        # Convert symbols to CoinGecko IDs (this is simplified)
        coin_ids = [s.replace('USDT', '').lower() for s in symbols]
        
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/coins/markets"
            params = {
                'vs_currency': 'usd',
                'ids': ','.join(coin_ids),
                'order': 'market_cap_desc',
                'sparkline': False
            }
            
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._process_market_data(data)
                    
        return []
        
    def _process_market_data(self, data: list) -> list:
        """Process CoinGecko market data"""
        processed = []
        for coin in data:
            processed.append({
                'symbol': coin['symbol'].upper() + 'USDT',
                'name': coin['name'],
                'market_cap': coin.get('market_cap'),
                'market_cap_rank': coin.get('market_cap_rank'),
                'total_volume': coin.get('total_volume'),
                'price_change_1h': coin.get('price_change_percentage_1h_in_currency'),
                'price_change_24h': coin.get('price_change_percentage_24h'),
                'price_change_7d': coin.get('price_change_percentage_7d'),
                'circulating_supply': coin.get('circulating_supply'),
                'total_supply': coin.get('total_supply'),
                'ath': coin.get('ath'),
                'atl': coin.get('atl'),
            })
        return processed
