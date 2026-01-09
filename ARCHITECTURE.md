# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     External Data Sources                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Binance    │  │  CoinGecko   │  │   Twitter    │          │
│  │  WebSocket   │  │     API      │  │     API      │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
└─────────┼──────────────────┼──────────────────┼──────────────────┘
          │                  │                  │
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                         Backend Layer                            │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              FastAPI Backend (Python)                      │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │ │
│  │  │  WebSocket   │  │  REST API    │  │  Data        │    │ │
│  │  │  Manager     │  │  Endpoints   │  │  Validator   │    │ │
│  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘    │ │
│  └─────────┼──────────────────┼──────────────────┼────────────┘ │
└────────────┼──────────────────┼──────────────────┼──────────────┘
             │                  │                  │
             ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Message/Cache Layer                         │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    Redis Cache                             │ │
│  │  • Real-time price caching                                 │ │
│  │  • Pub/Sub messaging                                       │ │
│  │  • Session management                                      │ │
│  └────────────────────────────────────────────────────────────┘ │
└──────────────────────────────┬───────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Processing Layer (Apache Spark)               │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                  Spark Streaming Jobs                      │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │ │
│  │  │  Windowed    │  │  Sentiment   │  │  Anomaly     │    │ │
│  │  │  Aggregations│  │  Analysis    │  │  Detection   │    │ │
│  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘    │ │
│  └─────────┼──────────────────┼──────────────────┼────────────┘ │
└────────────┼──────────────────┼──────────────────┼──────────────┘
             │                  │                  │
             ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Storage Layer                               │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    PostgreSQL Database                     │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │ │
│  │  │ crypto_prices│  │ sentiment_   │  │ aggregated_  │    │ │
│  │  │              │  │ scores       │  │ metrics      │    │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘    │ │
│  └────────────────────────────────────────────────────────────┘ │
└──────────────────────────────┬───────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Frontend Layer                              │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                   React Dashboard                          │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │ │
│  │  │  Price Cards │  │  Charts      │  │  WebSocket   │    │ │
│  │  │              │  │  (Chart.js)  │  │  Client      │    │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘    │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Data Ingestion Flow

```
External APIs → Backend WebSocket Handler → Redis Cache → Client WebSocket
                                          ↓
                                    Spark Consumer
```

1. **External APIs**: Binance WebSocket streams real-time trade/ticker data
2. **Backend**: FastAPI receives, validates, and caches data in Redis
3. **Broadcasting**: Data is broadcast to connected WebSocket clients
4. **Spark Processing**: Spark reads from Redis for stream processing

### 2. Stream Processing Flow

```
Redis Stream → Spark Streaming → Windowed Aggregations → PostgreSQL
                               → Sentiment Analysis     → PostgreSQL
                               → Anomaly Detection      → PostgreSQL
```

1. **Spark reads** from Redis (or Kafka in production)
2. **Processes** data in 5-minute, 15-minute, and 1-hour windows
3. **Calculates** metrics: VWAP, volatility, volume aggregates
4. **Writes** results to PostgreSQL for historical analysis

### 3. Query Flow

```
Frontend → REST API → PostgreSQL → Response → Frontend
        ↓
    WebSocket → Real-time Updates
```

1. **Initial Load**: Frontend fetches historical data via REST API
2. **Real-time**: WebSocket connection for live price updates
3. **Queries**: Historical analysis queries PostgreSQL directly

## Component Details

### Backend (FastAPI)

**Responsibilities:**
- WebSocket connection management
- External API integration (Binance, CoinGecko)
- Data validation and normalization
- REST API endpoints
- Redis caching

**Key Files:**
- `app/main.py`: FastAPI application and routes
- `app/websocket.py`: WebSocket handlers and clients
- `app/models.py`: SQLAlchemy database models
- `app/database.py`: Database connection management

### Spark Streaming

**Responsibilities:**
- Real-time stream processing
- Windowed aggregations (5min, 15min, 1h)
- VWAP calculation
- Sentiment analysis
- Anomaly detection
- Write to PostgreSQL

**Key Files:**
- `spark/streaming_processor.py`: Main Spark job
- `spark/sentiment_analyzer.py`: Sentiment analysis logic

**Processing Windows:**
- **5-minute**: Short-term price movements
- **15-minute**: Medium-term trends
- **1-hour**: Long-term analysis

### Database (PostgreSQL)

**Tables:**
- `crypto_prices`: Raw price data
- `sentiment_scores`: Sentiment analysis results
- `aggregated_metrics`: Spark-computed metrics
- `market_alerts`: Anomaly detection alerts

**Indexes:**
- Composite indexes on (symbol, timestamp)
- Partial indexes for active alerts
- Time-series optimizations

### Frontend (React)

**Responsibilities:**
- Real-time data visualization
- WebSocket connection handling
- Interactive charts
- Responsive UI

**Key Components:**
- `App.jsx`: Main application component
- `CryptoCard.jsx`: Individual crypto display
- `PriceChart.jsx`: Chart.js integration
- `services/websocket.js`: WebSocket service
- `services/api.js`: REST API client

## Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **WebSockets**: Real-time bidirectional communication
- **SQLAlchemy**: ORM for database operations
- **Pydantic**: Data validation

### Processing
- **Apache Spark 3.5**: Distributed stream processing
- **PySpark**: Python API for Spark

### Storage
- **PostgreSQL 15**: Relational database
- **Redis**: In-memory cache and message broker

### Frontend
- **React 18**: UI framework
- **Chart.js**: Data visualization
- **Axios**: HTTP client

### DevOps
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration

## Scalability Considerations

### Horizontal Scaling

1. **Backend**: Add more FastAPI instances behind load balancer
2. **Spark**: Add more worker nodes for parallel processing
3. **Database**: Use read replicas for query scaling
4. **Redis**: Use Redis Cluster for distributed caching

### Vertical Scaling

1. **Spark**: Increase executor memory and cores
2. **PostgreSQL**: Increase connection pool size
3. **Redis**: Increase memory allocation

### Performance Optimizations

1. **Caching**: Redis for frequently accessed data
2. **Database**: Proper indexing, materialized views
3. **WebSocket**: Connection pooling, message batching
4. **Spark**: Partition tuning, checkpoint optimization

## Monitoring & Observability

### Metrics to Track

1. **Latency**: End-to-end data processing time
2. **Throughput**: Messages processed per second
3. **Error Rate**: Failed processing attempts
4. **Connection Count**: Active WebSocket connections

### Logging

- **Structured Logging**: JSON format
- **Log Levels**: DEBUG, INFO, WARN, ERROR
- **Centralized**: All logs aggregated

### Monitoring Stack (Future)

- **Prometheus**: Metrics collection
- **Grafana**: Visualization
- **Spark UI**: Job monitoring
- **PgAdmin**: Database management

## Security Considerations

1. **API Authentication**: JWT tokens (to be implemented)
2. **Rate Limiting**: Prevent abuse
3. **Input Validation**: Pydantic models
4. **SQL Injection**: SQLAlchemy ORM
5. **CORS**: Configured for specific origins
6. **Environment Variables**: Sensitive data in .env

## Future Enhancements

1. **Kafka Integration**: Replace Redis with Kafka for production
2. **Machine Learning**: Price prediction models
3. **Alert System**: Email/SMS notifications
4. **User Accounts**: Personalized watchlists
5. **Mobile App**: React Native application
6. **Advanced Analytics**: More sophisticated indicators
