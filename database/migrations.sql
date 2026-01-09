-- Database Migration Scripts

-- Migration: Add indexes for performance
-- Version: 1.0.0
-- Date: 2026-01-09

BEGIN;

-- Composite indexes for common queries
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_prices_symbol_timestamp 
    ON crypto_prices (symbol, timestamp DESC);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_metrics_symbol_window 
    ON aggregated_metrics (symbol, window_start DESC);

-- Partial indexes for active alerts
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_active_alerts 
    ON market_alerts (symbol, created_at DESC) 
    WHERE is_active = TRUE;

-- Index for sentiment analysis
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_sentiment_symbol_timestamp 
    ON sentiment_scores (symbol, timestamp DESC);

COMMIT;

-- Migration: Add materialized views for dashboard
BEGIN;

-- Materialized view for latest prices
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_latest_prices AS
SELECT DISTINCT ON (symbol)
    symbol,
    name,
    price,
    volume_24h,
    price_change_24h,
    timestamp
FROM crypto_prices
ORDER BY symbol, timestamp DESC;

-- Index on materialized view
CREATE UNIQUE INDEX IF NOT EXISTS idx_mv_latest_prices_symbol 
    ON mv_latest_prices (symbol);

-- Materialized view for 24h statistics
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_24h_stats AS
SELECT 
    symbol,
    COUNT(*) as data_points,
    AVG(price) as avg_price_24h,
    MIN(price) as min_price_24h,
    MAX(price) as max_price_24h,
    STDDEV(price) as price_volatility_24h,
    SUM(volume_24h) as total_volume_24h
FROM crypto_prices
WHERE timestamp >= NOW() - INTERVAL '24 hours'
GROUP BY symbol;

CREATE UNIQUE INDEX IF NOT EXISTS idx_mv_24h_stats_symbol 
    ON mv_24h_stats (symbol);

COMMIT;

-- Function to refresh materialized views
CREATE OR REPLACE FUNCTION refresh_dashboard_views()
RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY mv_latest_prices;
    REFRESH MATERIALIZED VIEW CONCURRENTLY mv_24h_stats;
END;
$$ LANGUAGE plpgsql;

-- Create a function to clean old data (retention policy)
CREATE OR REPLACE FUNCTION cleanup_old_data()
RETURNS void AS $$
BEGIN
    -- Keep only 30 days of raw price data
    DELETE FROM crypto_prices 
    WHERE timestamp < NOW() - INTERVAL '30 days';
    
    -- Keep only 90 days of aggregated metrics
    DELETE FROM aggregated_metrics 
    WHERE timestamp < NOW() - INTERVAL '90 days';
    
    -- Keep only 7 days of sentiment scores
    DELETE FROM sentiment_scores 
    WHERE timestamp < NOW() - INTERVAL '7 days';
    
    -- Archive resolved alerts older than 30 days
    DELETE FROM market_alerts 
    WHERE is_active = FALSE 
    AND resolved_at < NOW() - INTERVAL '30 days';
END;
$$ LANGUAGE plpgsql;

-- Success message
SELECT 'Migration completed successfully!' AS status;
