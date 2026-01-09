import re
from typing import Dict, Any
from pyspark.sql import DataFrame
from pyspark.sql.functions import udf, col
from pyspark.sql.types import DoubleType


class SentimentAnalyzer:
    """Simple sentiment analysis for crypto market data"""
    
    def __init__(self):
        # Simple sentiment keywords
        self.positive_keywords = {
            'bullish', 'moon', 'pump', 'rally', 'surge', 'profit', 
            'gain', 'buy', 'long', 'hodl', 'breakout', 'support'
        }
        
        self.negative_keywords = {
            'bearish', 'dump', 'crash', 'sell', 'short', 'loss',
            'drop', 'fall', 'resistance', 'fear', 'panic'
        }
        
    def analyze_text(self, text: str) -> float:
        """
        Analyze sentiment of text
        Returns: sentiment score between -1 (very negative) and 1 (very positive)
        """
        if not text:
            return 0.0
            
        text = text.lower()
        words = re.findall(r'\w+', text)
        
        positive_count = sum(1 for word in words if word in self.positive_keywords)
        negative_count = sum(1 for word in words if word in self.negative_keywords)
        
        total_sentiment_words = positive_count + negative_count
        
        if total_sentiment_words == 0:
            return 0.0
            
        # Calculate sentiment score
        sentiment = (positive_count - negative_count) / total_sentiment_words
        
        return sentiment
        
    def analyze_price_action(self, price_change: float) -> Dict[str, Any]:
        """
        Analyze sentiment based on price action
        
        Args:
            price_change: Percentage price change
            
        Returns:
            Dict with sentiment score and confidence
        """
        # Convert price change to sentiment
        # Large positive change = positive sentiment
        # Large negative change = negative sentiment
        
        if price_change > 10:
            return {'sentiment': 1.0, 'confidence': 0.9, 'label': 'very_bullish'}
        elif price_change > 5:
            return {'sentiment': 0.7, 'confidence': 0.8, 'label': 'bullish'}
        elif price_change > 2:
            return {'sentiment': 0.4, 'confidence': 0.6, 'label': 'slightly_bullish'}
        elif price_change > -2:
            return {'sentiment': 0.0, 'confidence': 0.5, 'label': 'neutral'}
        elif price_change > -5:
            return {'sentiment': -0.4, 'confidence': 0.6, 'label': 'slightly_bearish'}
        elif price_change > -10:
            return {'sentiment': -0.7, 'confidence': 0.8, 'label': 'bearish'}
        else:
            return {'sentiment': -1.0, 'confidence': 0.9, 'label': 'very_bearish'}
            
    def analyze_volume(self, volume: float, avg_volume: float) -> float:
        """
        Analyze sentiment based on volume
        High volume with price increase = very bullish
        High volume with price decrease = very bearish
        """
        if avg_volume == 0:
            return 0.0
            
        volume_ratio = volume / avg_volume
        
        if volume_ratio > 2:
            return 0.8  # High conviction
        elif volume_ratio > 1.5:
            return 0.6  # Medium conviction
        else:
            return 0.3  # Low conviction
            
    def create_sentiment_udf(self):
        """Create UDF for sentiment analysis"""
        return udf(self.analyze_price_action, DoubleType())
        
    def add_sentiment_features(self, df: DataFrame) -> DataFrame:
        """
        Add sentiment analysis features to DataFrame
        
        Args:
            df: Spark DataFrame with price data
            
        Returns:
            DataFrame with additional sentiment columns
        """
        
        # Create UDF for price-based sentiment
        @udf(returnType=DoubleType())
        def price_sentiment(price_change):
            if price_change is None:
                return 0.0
            return self.analyze_price_action(price_change)['sentiment']
            
        # Add sentiment score based on price change
        df = df.withColumn("price_sentiment", price_sentiment(col("price_change_24h")))
        
        return df
        
    def aggregate_sentiment(self, df: DataFrame, window_col: str = "window") -> DataFrame:
        """
        Aggregate sentiment scores over time windows
        
        Args:
            df: DataFrame with sentiment scores
            window_col: Name of the window column
            
        Returns:
            DataFrame with aggregated sentiment metrics
        """
        from pyspark.sql.functions import avg, count, stddev
        
        sentiment_agg = df.groupBy("symbol", window_col).agg(
            avg("price_sentiment").alias("avg_sentiment"),
            count("*").alias("sentiment_count"),
            stddev("price_sentiment").alias("sentiment_volatility")
        )
        
        return sentiment_agg


def calculate_fear_greed_index(
    price_change: float,
    volume_ratio: float,
    volatility: float
) -> int:
    """
    Calculate Fear & Greed Index (0-100)
    
    Args:
        price_change: 24h price change percentage
        volume_ratio: Current volume / average volume
        volatility: Price volatility measure
        
    Returns:
        Fear & Greed Index (0 = Extreme Fear, 100 = Extreme Greed)
    """
    # Weight different factors
    price_score = min(100, max(0, 50 + price_change * 2))
    volume_score = min(100, volume_ratio * 30)
    volatility_score = min(100, max(0, 100 - volatility * 10))
    
    # Weighted average
    index = (price_score * 0.5 + volume_score * 0.3 + volatility_score * 0.2)
    
    return int(index)


def get_sentiment_label(sentiment_score: float) -> str:
    """
    Convert sentiment score to label
    
    Args:
        sentiment_score: Score between -1 and 1
        
    Returns:
        Sentiment label
    """
    if sentiment_score >= 0.7:
        return "Very Bullish"
    elif sentiment_score >= 0.3:
        return "Bullish"
    elif sentiment_score >= -0.3:
        return "Neutral"
    elif sentiment_score >= -0.7:
        return "Bearish"
    else:
        return "Very Bearish"
