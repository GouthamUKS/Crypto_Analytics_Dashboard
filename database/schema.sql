-- Crypto Analytics Database Schema

-- Table: crypto_prices
-- Stores real-time and historical cryptocurrency price data
CREATE TABLE IF NOT EXISTS crypto_prices (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    name VARCHAR(100) NOT NULL,
    price DOUBLE PRECISION NOT NULL,
    volume_24h DOUBLE PRECISION,
    market_cap DOUBLE PRECISION,
    price_change_1h DOUBLE PRECISION,
    price_change_24h DOUBLE PRECISION,
    price_change_7d DOUBLE PRECISION,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Table: sentiment_scores
-- Stores sentiment analysis scores from various sources
CREATE TABLE IF NOT EXISTS sentiment_scores (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    sentiment_score DOUBLE PRECISION NOT NULL CHECK (sentiment_score >= -1 AND sentiment_score <= 1),
    source VARCHAR(50),
    confidence DOUBLE PRECISION CHECK (confidence >= 0 AND confidence <= 1),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Table: aggregated_metrics
-- Stores windowed aggregations computed by Spark
CREATE TABLE IF NOT EXISTS aggregated_metrics (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    window_start TIMESTAMP WITH TIME ZONE NOT NULL,
    window_end TIMESTAMP WITH TIME ZONE NOT NULL,
    
    -- Price metrics
    avg_price DOUBLE PRECISION,
    min_price DOUBLE PRECISION,
    max_price DOUBLE PRECISION,
    vwap DOUBLE PRECISION,
    
    -- Volume metrics
    total_volume DOUBLE PRECISION,
    trade_count INTEGER,
    
    -- Volatility metrics
    price_volatility DOUBLE PRECISION,
    price_range DOUBLE PRECISION,
    
    -- Sentiment metrics
    avg_sentiment DOUBLE PRECISION,
    sentiment_count INTEGER,
    
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    
    CONSTRAINT unique_symbol_window UNIQUE (symbol, window_start, window_end)
);

-- Table: market_alerts
-- Stores market alerts and anomaly detection results
CREATE TABLE IF NOT EXISTS market_alerts (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    alert_type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    message VARCHAR(500),
    trigger_value DOUBLE PRECISION,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    resolved_at TIMESTAMP WITH TIME ZONE
);

-- Table: user_watchlist (optional - for user preferences)
CREATE TABLE IF NOT EXISTS user_watchlist (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(100),
    symbol VARCHAR(20) NOT NULL,
    added_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Table: price_predictions (optional - for ML model predictions)
CREATE TABLE IF NOT EXISTS price_predictions (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    predicted_price DOUBLE PRECISION NOT NULL,
    prediction_timeframe VARCHAR(20),
    confidence DOUBLE PRECISION,
    model_version VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Comments for documentation
COMMENT ON TABLE crypto_prices IS 'Real-time and historical cryptocurrency price data';
COMMENT ON TABLE sentiment_scores IS 'Sentiment analysis scores from various sources (social media, news, etc.)';
COMMENT ON TABLE aggregated_metrics IS 'Windowed aggregations computed by Apache Spark (5min, 15min, 1h windows)';
COMMENT ON TABLE market_alerts IS 'Market alerts and anomaly detection results';

COMMENT ON COLUMN crypto_prices.price IS 'Current price in USD';
COMMENT ON COLUMN crypto_prices.volume_24h IS '24-hour trading volume in USD';
COMMENT ON COLUMN crypto_prices.market_cap IS 'Total market capitalization in USD';
COMMENT ON COLUMN sentiment_scores.sentiment_score IS 'Sentiment score ranging from -1 (very negative) to 1 (very positive)';
COMMENT ON COLUMN aggregated_metrics.vwap IS 'Volume Weighted Average Price for the window';
COMMENT ON COLUMN aggregated_metrics.price_volatility IS 'Standard deviation of price within the window';
