import React, { useState, useEffect } from 'react';
import { wsService } from './services/websocket';
import { cryptoAPI } from './services/api';
import CryptoCard from './components/CryptoCard';
import PriceChart from './components/PriceChart';
import './index.css';

function App() {
  const [isConnected, setIsConnected] = useState(false);
  const [cryptoData, setCryptoData] = useState({});
  const [historicalData, setHistoricalData] = useState({});
  const [trackedSymbols, setTrackedSymbols] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Initialize WebSocket connection and fetch initial data
  useEffect(() => {
    const initialize = async () => {
      try {
        // Fetch tracked cryptocurrencies
        const cryptos = await cryptoAPI.getTrackedCryptos();
        setTrackedSymbols(cryptos.symbols || []);

        // Fetch initial data for each symbol
        for (const symbol of cryptos.symbols || []) {
          try {
            const [priceData, historical] = await Promise.all([
              cryptoAPI.getCurrentPrice(symbol),
              cryptoAPI.getHistoricalData(symbol, 24)
            ]);

            setCryptoData(prev => ({
              ...prev,
              [symbol]: priceData
            }));

            setHistoricalData(prev => ({
              ...prev,
              [symbol]: historical.data || []
            }));
          } catch (err) {
            console.error(`Error fetching data for ${symbol}:`, err);
          }
        }

        setLoading(false);
      } catch (err) {
        console.error('Error initializing app:', err);
        setError('Failed to load cryptocurrency data. Please try again later.');
        setLoading(false);
      }
    };

    initialize();

    // Connect to WebSocket
    wsService.connect(setIsConnected);

    // Listen for WebSocket updates
    wsService.addListener('app', (data) => {
      if (data.type === 'price_update') {
        setCryptoData(prev => ({
          ...prev,
          [data.symbol]: {
            ...prev[data.symbol],
            ...data
          }
        }));

        // Update historical data
        setHistoricalData(prev => ({
          ...prev,
          [data.symbol]: [
            ...(prev[data.symbol] || []),
            {
              price: data.price,
              volume: data.volume_24h,
              timestamp: data.timestamp
            }
          ].slice(-100) // Keep last 100 data points
        }));
      }
    });

    // Subscribe to all tracked symbols
    const subscribeToSymbols = () => {
      if (wsService.isConnected) {
        trackedSymbols.forEach(symbol => {
          wsService.subscribe(symbol);
        });
      }
    };

    // Subscribe after connection
    const timer = setTimeout(subscribeToSymbols, 1000);

    // Cleanup
    return () => {
      clearTimeout(timer);
      wsService.removeListener('app');
      wsService.disconnect();
    };
  }, []);

  // Subscribe to symbols when they change
  useEffect(() => {
    if (isConnected && trackedSymbols.length > 0) {
      trackedSymbols.forEach(symbol => {
        wsService.subscribe(symbol);
      });
    }
  }, [isConnected, trackedSymbols]);

  if (loading) {
    return (
      <div className="App">
        <div className="loading">
          <h2>Loading Crypto Analytics Dashboard...</h2>
          <p>Connecting to data sources...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="App">
        <div className="error">
          <h3>Error</h3>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="App">
      {/* Connection Status */}
      <div className="connection-status">
        <span className={`status-indicator ${isConnected ? 'connected' : 'disconnected'}`}></span>
        {isConnected ? 'Connected' : 'Disconnected'}
      </div>

      {/* Header */}
      <div className="header">
        <h1>⚡ Crypto Analytics Dashboard</h1>
        <p>Real-time cryptocurrency market tracking powered by Apache Spark & WebSocket</p>
      </div>

      {/* Dashboard Grid */}
      <div className="dashboard-grid">
        {trackedSymbols.map(symbol => (
          <CryptoCard
            key={symbol}
            symbol={symbol}
            data={cryptoData[symbol]}
            priceChange={cryptoData[symbol]?.price_change_24h}
          />
        ))}

        {/* Price Charts */}
        {trackedSymbols.map(symbol => (
          historicalData[symbol] && historicalData[symbol].length > 0 && (
            <PriceChart
              key={`chart-${symbol}`}
              symbol={symbol}
              data={historicalData[symbol]}
            />
          )
        ))}
      </div>

      {/* Footer */}
      <div style={{ 
        textAlign: 'center', 
        color: 'var(--text-secondary)', 
        marginTop: '60px',
        marginBottom: '20px',
        fontSize: '0.9rem',
        opacity: 0.8
      }}>
        <p>Built with React • FastAPI • Apache Spark • PostgreSQL</p>
        <p style={{ marginTop: '8px', fontSize: '0.85rem' }}>Data updates in real-time via WebSocket</p>
      </div>
    </div>
  );
}

export default App;
