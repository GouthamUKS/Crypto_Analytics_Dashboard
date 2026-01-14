import asyncio
import json
from typing import Set, Dict, Any
from datetime import datetime
from fastapi import WebSocket, WebSocketDisconnect


class ConnectionManager:
    """Manages WebSocket connections to clients - simplified version"""
    
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
