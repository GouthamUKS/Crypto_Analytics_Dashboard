import axios from 'axios';
import API_CONFIG from '../config';

const api = axios.create({
  baseURL: API_CONFIG.baseURL + '/api',
  timeout: 10000,
});

export const cryptoAPI = {
  // Get list of tracked cryptocurrencies
  getTrackedCryptos: async () => {
    const response = await api.get('/cryptos');
    return response.data;
  },

  // Get current price for a symbol
  getCurrentPrice: async (symbol) => {
    const response = await api.get(`/prices/${symbol}`);
    return response.data;
  },

  // Get historical data
  getHistoricalData: async (symbol, hours = 24) => {
    const response = await api.get(`/historical/${symbol}`, {
      params: { hours }
    });
    return response.data;
  },

  // Get aggregated metrics
  getMetrics: async (symbol, hours = 24) => {
    const response = await api.get(`/metrics/${symbol}`, {
      params: { hours }
    });
    return response.data;
  },

  // Get sentiment scores
  getSentiment: async (symbol, hours = 24) => {
    const response = await api.get(`/sentiment/${symbol}`, {
      params: { hours }
    });
    return response.data;
  },

  // Get active alerts
  getAlerts: async () => {
    const response = await api.get('/alerts');
    return response.data;
  },

  // Health check
  healthCheck: async () => {
    const response = await api.get('/health');
    return response.data;
  },
};

export default api;
