from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()


class CryptoPrice(Base):
    """Model for storing cryptocurrency price data"""
    __tablename__ = "crypto_prices"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    volume_24h = Column(Float)
    market_cap = Column(Float)
    price_change_1h = Column(Float)
    price_change_24h = Column(Float)
    price_change_7d = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    __table_args__ = (
        Index('idx_symbol_timestamp', 'symbol', 'timestamp'),
    )


class SentimentScore(Base):
    """Model for storing sentiment analysis scores"""
    __tablename__ = "sentiment_scores"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), nullable=False, index=True)
    sentiment_score = Column(Float, nullable=False)  # -1 to 1
    source = Column(String(50))  # twitter, reddit, news, etc.
    confidence = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    __table_args__ = (
        Index('idx_sentiment_symbol_timestamp', 'symbol', 'timestamp'),
    )


class AggregatedMetrics(Base):
    """Model for storing windowed aggregations from Spark"""
    __tablename__ = "aggregated_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), nullable=False, index=True)
    window_start = Column(DateTime(timezone=True), nullable=False)
    window_end = Column(DateTime(timezone=True), nullable=False)
    
    # Price metrics
    avg_price = Column(Float)
    min_price = Column(Float)
    max_price = Column(Float)
    vwap = Column(Float)  # Volume Weighted Average Price
    
    # Volume metrics
    total_volume = Column(Float)
    trade_count = Column(Integer)
    
    # Volatility metrics
    price_volatility = Column(Float)
    price_range = Column(Float)
    
    # Sentiment metrics
    avg_sentiment = Column(Float)
    sentiment_count = Column(Integer)
    
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    __table_args__ = (
        Index('idx_metrics_symbol_window', 'symbol', 'window_start', 'window_end'),
    )


class MarketAlert(Base):
    """Model for storing market alerts and anomalies"""
    __tablename__ = "market_alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), nullable=False, index=True)
    alert_type = Column(String(50), nullable=False)  # price_spike, volume_surge, sentiment_shift
    severity = Column(String(20))  # low, medium, high, critical
    message = Column(String(500))
    trigger_value = Column(Float)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    resolved_at = Column(DateTime(timezone=True), nullable=True)
