import React from 'react';

const CryptoCard = ({ symbol, data, priceChange }) => {
  const getPriceChangeClass = (change) => {
    if (!change) return 'neutral';
    return change > 0 ? 'positive' : change < 0 ? 'negative' : 'neutral';
  };

  const formatPrice = (price) => {
    return price ? `$${price.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}` : 'Loading...';
  };

  const formatVolume = (volume) => {
    if (!volume) return 'N/A';
    if (volume >= 1e9) return `$${(volume / 1e9).toFixed(2)}B`;
    if (volume >= 1e6) return `$${(volume / 1e6).toFixed(2)}M`;
    return `$${volume.toLocaleString()}`;
  };

  const formatChange = (change) => {
    if (!change) return '0.00%';
    const prefix = change > 0 ? '+' : '';
    return `${prefix}${change.toFixed(2)}%`;
  };

  return (
    <div className="card crypto-card">
      <div className="card-header">
        <div>
          <div className="crypto-symbol">{symbol}</div>
          <div className="crypto-name">{data?.name || 'Cryptocurrency'}</div>
        </div>
        <span className={`price-change ${getPriceChangeClass(priceChange)}`}>
          {formatChange(priceChange)}
        </span>
      </div>

      <div className="price-display">
        {formatPrice(data?.price)}
      </div>

      <div className="metrics-grid">
        <div className="metric">
          <div className="metric-label">24h Volume</div>
          <div className="metric-value">{formatVolume(data?.volume_24h)}</div>
        </div>
        <div className="metric">
          <div className="metric-label">24h High</div>
          <div className="metric-value">{data?.high_24h ? formatPrice(data.high_24h) : 'N/A'}</div>
        </div>
        <div className="metric">
          <div className="metric-label">24h Low</div>
          <div className="metric-value">{data?.low_24h ? formatPrice(data.low_24h) : 'N/A'}</div>
        </div>
        <div className="metric">
          <div className="metric-label">Last Update</div>
          <div className="metric-value" style={{ fontSize: '0.85rem' }}>
            {data?.timestamp ? new Date(data.timestamp).toLocaleTimeString() : 'N/A'}
          </div>
        </div>
      </div>
    </div>
  );
};

export default CryptoCard;
