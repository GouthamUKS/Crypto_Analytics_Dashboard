import API_CONFIG from '../config';

const WS_URL = API_CONFIG.wsURL + '/ws';

class WebSocketService {
  constructor() {
    this.ws = null;
    this.reconnectInterval = 3000;
    this.listeners = new Map();
    this.isConnected = false;
  }

  connect(onConnectionChange) {
    try {
      this.ws = new WebSocket(WS_URL);

      this.ws.onopen = () => {
        console.log('WebSocket connected');
        this.isConnected = true;
        if (onConnectionChange) onConnectionChange(true);
      };

      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          this.notifyListeners(data);
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error);
      };

      this.ws.onclose = () => {
        console.log('WebSocket disconnected');
        this.isConnected = false;
        if (onConnectionChange) onConnectionChange(false);
        
        // Attempt to reconnect
        setTimeout(() => {
          console.log('Attempting to reconnect...');
          this.connect(onConnectionChange);
        }, this.reconnectInterval);
      };
    } catch (error) {
      console.error('Error creating WebSocket:', error);
    }
  }

  subscribe(symbol) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({
        action: 'subscribe',
        symbol: symbol
      }));
    }
  }

  unsubscribe(symbol) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({
        action: 'unsubscribe',
        symbol: symbol
      }));
    }
  }

  addListener(id, callback) {
    this.listeners.set(id, callback);
  }

  removeListener(id) {
    this.listeners.delete(id);
  }

  notifyListeners(data) {
    this.listeners.forEach(callback => {
      try {
        callback(data);
      } catch (error) {
        console.error('Error in listener callback:', error);
      }
    });
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    this.listeners.clear();
  }
}

export const wsService = new WebSocketService();
