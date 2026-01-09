// API Configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const WS_BASE_URL = process.env.REACT_APP_WS_URL || 'ws://localhost:8000';

export const API_CONFIG = {
  baseURL: API_BASE_URL,
  wsURL: WS_BASE_URL,
  endpoints: {
    health: '/api/health',
    cryptos: '/api/cryptos',
    prices: '/api/prices',
    historical: '/api/historical',
    websocket: '/ws'
  }
};

export default API_CONFIG;
