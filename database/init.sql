-- Initialize Crypto Analytics Database

-- Create extension for UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create extension for time-series optimization
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

-- Set timezone
SET timezone = 'UTC';

-- Create tables
\i schema.sql

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_crypto_prices_symbol_timestamp ON crypto_prices (symbol, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_sentiment_scores_symbol_timestamp ON sentiment_scores (symbol, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_aggregated_metrics_symbol_window ON aggregated_metrics (symbol, window_start DESC, window_end DESC);
CREATE INDEX IF NOT EXISTS idx_market_alerts_symbol_created ON market_alerts (symbol, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_market_alerts_active ON market_alerts (is_active) WHERE is_active = TRUE;

-- Convert to hypertables for time-series optimization (TimescaleDB)
-- Uncomment if using TimescaleDB
-- SELECT create_hypertable('crypto_prices', 'timestamp', if_not_exists => TRUE);
-- SELECT create_hypertable('sentiment_scores', 'timestamp', if_not_exists => TRUE);
-- SELECT create_hypertable('aggregated_metrics', 'timestamp', if_not_exists => TRUE);

-- Create views for common queries
CREATE OR REPLACE VIEW latest_prices AS
SELECT DISTINCT ON (symbol) 
    symbol,
    name,
    price,
    volume_24h,
    market_cap,
    price_change_24h,
    timestamp
FROM crypto_prices
ORDER BY symbol, timestamp DESC;

CREATE OR REPLACE VIEW hourly_aggregates AS
SELECT 
    symbol,
    date_trunc('hour', window_start) as hour,
    AVG(avg_price) as avg_price,
    MIN(min_price) as min_price,
    MAX(max_price) as max_price,
    SUM(total_volume) as total_volume,
    AVG(avg_sentiment) as avg_sentiment
FROM aggregated_metrics
GROUP BY symbol, date_trunc('hour', window_start)
ORDER BY symbol, hour DESC;

-- Insert sample data for testing
INSERT INTO crypto_prices (symbol, name, price, volume_24h, market_cap, price_change_24h, timestamp)
VALUES 
    ('BTCUSDT', 'Bitcoin', 45000.00, 28000000000, 880000000000, 2.5, NOW() - INTERVAL '1 hour'),
    ('ETHUSDT', 'Ethereum', 2500.00, 15000000000, 300000000000, 3.2, NOW() - INTERVAL '1 hour'),
    ('BNBUSDT', 'Binance Coin', 310.00, 1200000000, 47000000000, 1.8, NOW() - INTERVAL '1 hour');

-- Grant permissions (adjust user as needed)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO your_user;

ANALYZE crypto_prices;
ANALYZE sentiment_scores;
ANALYZE aggregated_metrics;
ANALYZE market_alerts;

-- Success message
SELECT 'Database initialization completed successfully!' AS status;
