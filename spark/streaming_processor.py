import os
import json
from datetime import datetime, timedelta
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    from_json, col, window, avg, min as spark_min, max as spark_max,
    sum as spark_sum, count, stddev, lit, current_timestamp,
    to_timestamp, expr, when
)
from pyspark.sql.types import (
    StructType, StructField, StringType, DoubleType, 
    TimestampType, LongType, BooleanType
)
import redis


class CryptoStreamProcessor:
    """Spark Streaming processor for crypto market data"""
    
    def __init__(self):
        self.spark = None
        self.redis_client = None
        self.db_url = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/crypto_analytics")
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        
        # Extract DB connection details
        self._parse_db_url()
        
    def _parse_db_url(self):
        """Parse database URL into components"""
        # postgresql://user:password@host:port/database
        url_parts = self.db_url.replace("postgresql://", "").split("@")
        user_pass = url_parts[0].split(":")
        host_db = url_parts[1].split("/")
        host_port = host_db[0].split(":")
        
        self.db_user = user_pass[0]
        self.db_password = user_pass[1]
        self.db_host = host_port[0]
        self.db_port = host_port[1] if len(host_port) > 1 else "5432"
        self.db_name = host_db[1]
        
    def initialize_spark(self):
        """Initialize Spark session"""
        self.spark = SparkSession.builder \
            .appName("CryptoAnalytics") \
            .config("spark.jars.packages", "org.postgresql:postgresql:42.6.0") \
            .config("spark.sql.streaming.checkpointLocation", "/tmp/spark-checkpoint") \
            .config("spark.sql.shuffle.partitions", "4") \
            .getOrCreate()
            
        self.spark.sparkContext.setLogLevel("WARN")
        print("Spark session initialized")
        
    def initialize_redis(self):
        """Initialize Redis connection"""
        redis_host = self.redis_url.replace("redis://", "").split(":")[0]
        redis_port = int(self.redis_url.split(":")[-1])
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
        print(f"Connected to Redis at {redis_host}:{redis_port}")
        
    def get_price_schema(self):
        """Define schema for price data"""
        return StructType([
            StructField("type", StringType(), True),
            StructField("symbol", StringType(), True),
            StructField("price", DoubleType(), True),
            StructField("price_change_24h", DoubleType(), True),
            StructField("volume_24h", DoubleType(), True),
            StructField("high_24h", DoubleType(), True),
            StructField("low_24h", DoubleType(), True),
            StructField("timestamp", StringType(), True)
        ])
        
    def get_trade_schema(self):
        """Define schema for trade data"""
        return StructType([
            StructField("type", StringType(), True),
            StructField("symbol", StringType(), True),
            StructField("price", DoubleType(), True),
            StructField("quantity", DoubleType(), True),
            StructField("is_buyer_maker", BooleanType(), True),
            StructField("timestamp", StringType(), True)
        ])
        
    def read_from_redis(self):
        """Read streaming data from Redis"""
        # In production, you'd use Kafka or another message queue
        # For this demo, we'll simulate by reading from Redis Pub/Sub
        
        # This is a simplified version - in production use Kafka
        print("Starting Redis stream consumer...")
        
        # Get tracked symbols
        symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "SOLUSDT"]
        
        # Create streaming DataFrame (simulated)
        # In production, replace with:
        # df = spark.readStream.format("kafka") ...
        
        return None  # Placeholder
        
    def process_windowed_aggregations(self, df):
        """Process windowed aggregations on streaming data"""
        
        # 5-minute window aggregations
        windowed_5min = df \
            .withColumn("timestamp", to_timestamp(col("timestamp"))) \
            .withWatermark("timestamp", "10 minutes") \
            .groupBy(
                col("symbol"),
                window(col("timestamp"), "5 minutes")
            ) \
            .agg(
                avg("price").alias("avg_price"),
                spark_min("price").alias("min_price"),
                spark_max("price").alias("max_price"),
                spark_sum(col("price") * col("volume_24h")).alias("price_volume"),
                spark_sum("volume_24h").alias("total_volume"),
                count("*").alias("trade_count"),
                stddev("price").alias("price_volatility")
            ) \
            .withColumn("vwap", col("price_volume") / col("total_volume")) \
            .withColumn("price_range", col("max_price") - col("min_price")) \
            .select(
                col("symbol"),
                col("window.start").alias("window_start"),
                col("window.end").alias("window_end"),
                col("avg_price"),
                col("min_price"),
                col("max_price"),
                col("vwap"),
                col("total_volume"),
                col("trade_count").cast("int"),
                col("price_volatility"),
                col("price_range"),
                current_timestamp().alias("timestamp")
            )
            
        return windowed_5min
        
    def detect_anomalies(self, df):
        """Detect price anomalies and generate alerts"""
        
        # Calculate z-score for price changes
        anomalies = df \
            .withColumn("price_spike", 
                when(col("price_change_24h") > 10, "high")
                .when(col("price_change_24h") > 5, "medium")
                .when(col("price_change_24h") < -10, "high")
                .when(col("price_change_24h") < -5, "medium")
                .otherwise("low")
            ) \
            .withColumn("volume_surge",
                when(col("volume_24h") > 1000000000, "high")
                .when(col("volume_24h") > 500000000, "medium")
                .otherwise("low")
            ) \
            .filter((col("price_spike") != "low") | (col("volume_surge") != "low"))
            
        return anomalies
        
    def write_to_postgres(self, df, table_name, mode="append"):
        """Write DataFrame to PostgreSQL"""
        
        jdbc_url = f"jdbc:postgresql://{self.db_host}:{self.db_port}/{self.db_name}"
        
        properties = {
            "user": self.db_user,
            "password": self.db_password,
            "driver": "org.postgresql.Driver"
        }
        
        query = df.writeStream \
            .foreachBatch(lambda batch_df, batch_id: 
                batch_df.write.jdbc(
                    url=jdbc_url,
                    table=table_name,
                    mode=mode,
                    properties=properties
                )
            ) \
            .outputMode("append") \
            .option("checkpointLocation", f"/tmp/checkpoint/{table_name}") \
            .start()
            
        return query
        
    def process_batch_data(self):
        """Process batch data from Redis (simulated streaming)"""
        print("Processing batch data from Redis...")
        
        # Get all price data from Redis
        keys = self.redis_client.keys("price:*")
        
        if not keys:
            print("No data in Redis yet")
            return
            
        data = []
        for key in keys:
            value = self.redis_client.get(key)
            if value:
                data.append(json.loads(value))
                
        if not data:
            print("No valid data found")
            return
            
        # Create DataFrame
        df = self.spark.createDataFrame(data)
        
        print(f"Processing {len(data)} records")
        
        # Show sample
        df.show(5, truncate=False)
        
        # Write to PostgreSQL
        jdbc_url = f"jdbc:postgresql://{self.db_host}:{self.db_port}/{self.db_name}"
        
        properties = {
            "user": self.db_user,
            "password": self.db_password,
            "driver": "org.postgresql.Driver"
        }
        
        # Transform for crypto_prices table
        prices_df = df.select(
            col("symbol"),
            lit("Cryptocurrency").alias("name"),
            col("price"),
            col("volume_24h"),
            lit(None).cast(DoubleType()).alias("market_cap"),
            lit(None).cast(DoubleType()).alias("price_change_1h"),
            col("price_change_24h"),
            lit(None).cast(DoubleType()).alias("price_change_7d"),
            to_timestamp(col("timestamp")).alias("timestamp")
        )
        
        try:
            prices_df.write.jdbc(
                url=jdbc_url,
                table="crypto_prices",
                mode="append",
                properties=properties
            )
            print(f"Wrote {prices_df.count()} records to crypto_prices table")
        except Exception as e:
            print(f"Error writing to database: {e}")
            
        # Calculate and write aggregations
        self._calculate_aggregations(df, jdbc_url, properties)
        
    def _calculate_aggregations(self, df, jdbc_url, properties):
        """Calculate aggregations for the batch"""
        
        # Convert timestamp
        df = df.withColumn("timestamp", to_timestamp(col("timestamp")))
        
        # Calculate 5-minute aggregations
        window_df = df.groupBy(
            col("symbol"),
            window(col("timestamp"), "5 minutes")
        ).agg(
            avg("price").alias("avg_price"),
            spark_min("price").alias("min_price"),
            spark_max("price").alias("max_price"),
            avg("volume_24h").alias("total_volume"),
            count("*").alias("trade_count"),
            stddev("price").alias("price_volatility")
        ).select(
            col("symbol"),
            col("window.start").alias("window_start"),
            col("window.end").alias("window_end"),
            col("avg_price"),
            col("min_price"),
            col("max_price"),
            col("avg_price").alias("vwap"),  # Simplified VWAP
            col("total_volume"),
            col("trade_count").cast("int"),
            col("price_volatility"),
            (col("max_price") - col("min_price")).alias("price_range"),
            lit(None).cast(DoubleType()).alias("avg_sentiment"),
            lit(None).cast("int").alias("sentiment_count"),
            current_timestamp().alias("timestamp")
        )
        
        try:
            window_df.write.jdbc(
                url=jdbc_url,
                table="aggregated_metrics",
                mode="append",
                properties=properties
            )
            print(f"Wrote {window_df.count()} aggregated metrics")
        except Exception as e:
            print(f"Error writing aggregations: {e}")
            
    def run(self):
        """Main processing loop"""
        self.initialize_spark()
        self.initialize_redis()
        
        print("Crypto Stream Processor started")
        print(f"Database: {self.db_host}:{self.db_port}/{self.db_name}")
        
        try:
            # Run batch processing every 30 seconds
            import time
            while True:
                self.process_batch_data()
                print("Waiting 30 seconds before next batch...")
                time.sleep(30)
                
        except KeyboardInterrupt:
            print("\nShutting down...")
        finally:
            if self.spark:
                self.spark.stop()
                

if __name__ == "__main__":
    processor = CryptoStreamProcessor()
    processor.run()
