# Installation Guide

This guide will walk you through setting up the Crypto Analytics Dashboard.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Docker & Docker Compose** (recommended for easy setup)
  - [Install Docker](https://docs.docker.com/get-docker/)
  - [Install Docker Compose](https://docs.docker.com/compose/install/)

OR for manual installation:

- **Python 3.11+**
- **Node.js 18+**
- **PostgreSQL 15+**
- **Redis**
- **Java 11+** (for Spark)
- **Apache Spark 3.5+**

## Quick Start with Docker (Recommended)

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd realtime_analytics_dashboard
```

### 2. Configure Environment Variables

```bash
cp .env.example .env
# Edit .env with your settings (optional for local development)
```

### 3. Run the Setup Script

```bash
chmod +x start.sh
./start.sh
```

This will:
- Build all Docker images
- Start all services (PostgreSQL, Redis, Backend, Spark, Frontend)
- Initialize the database
- Display service URLs

### 4. Access the Application

- **Frontend Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Spark UI**: http://localhost:8080

## Manual Installation

### 1. Database Setup

```bash
# Create database
createdb crypto_analytics

# Run initialization script
psql -d crypto_analytics -f database/init.sql
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/crypto_analytics"
export REDIS_URL="redis://localhost:6379"

# Start the server
uvicorn app.main:app --reload --port 8000
```

### 3. Spark Streaming Setup

```bash
cd spark

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/crypto_analytics"
export REDIS_URL="redis://localhost:6379"

# Submit Spark job
spark-submit \
  --packages org.postgresql:postgresql:42.6.0 \
  streaming_processor.py
```

### 4. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

## Databricks Setup (Optional)

To run this on Databricks Community Edition:

### 1. Upload Spark Scripts

1. Log in to [Databricks Community Edition](https://community.cloud.databricks.com/)
2. Create a new notebook
3. Upload `spark/streaming_processor.py`
4. Upload `spark/sentiment_analyzer.py`

### 2. Configure Cluster

Create a cluster with:
- Runtime: 13.3 LTS or later
- Python: 3.10+
- Install libraries:
  - psycopg2-binary
  - redis

### 3. Set Environment Variables

In your Databricks notebook:

```python
import os
os.environ['DATABASE_URL'] = 'your_database_url'
os.environ['REDIS_URL'] = 'your_redis_url'
```

### 4. Run the Notebook

Execute the cells to start stream processing.

## Verification

### Check Services are Running

```bash
# With Docker
docker-compose ps

# Expected output: All services should be "Up"
```

### Test Backend API

```bash
curl http://localhost:8000/api/health
# Expected: {"status": "healthy", ...}
```

### Test WebSocket Connection

Open browser console at http://localhost:3000 and check for WebSocket connection messages.

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f spark-streaming
```

## Troubleshooting

### Port Already in Use

If you get port conflict errors:

```bash
# Check what's using the port
lsof -i :8000  # or :3000, :5432, etc.

# Kill the process or change port in docker-compose.yml
```

### Database Connection Error

```bash
# Check PostgreSQL is running
docker-compose ps postgres

# View PostgreSQL logs
docker-compose logs postgres

# Reset database
docker-compose down -v
docker-compose up -d postgres
```

### Spark Job Not Running

```bash
# Check Spark logs
docker-compose logs spark-streaming

# Restart Spark
docker-compose restart spark-streaming
```

### Frontend Not Loading

```bash
# Check frontend logs
docker-compose logs frontend

# Rebuild frontend
docker-compose build frontend
docker-compose up -d frontend
```

### WebSocket Not Connecting

1. Check backend is running: http://localhost:8000
2. Check browser console for errors
3. Verify CORS settings in `.env`
4. Check firewall settings

## Development Tips

### Hot Reload

All services support hot reload:
- **Backend**: FastAPI auto-reloads on file changes
- **Frontend**: React development server auto-reloads
- **Spark**: Restart job manually after changes

### Database Access

```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U postgres -d crypto_analytics

# Run SQL queries
SELECT * FROM crypto_prices ORDER BY timestamp DESC LIMIT 10;
```

### Redis Access

```bash
# Connect to Redis
docker-compose exec redis redis-cli

# Check cached data
KEYS *
GET price:BTCUSDT
```

## Production Deployment

For production deployment:

1. Use environment-specific `.env` files
2. Set up proper secrets management
3. Configure HTTPS/SSL
4. Set up monitoring (Prometheus, Grafana)
5. Configure backup strategy for PostgreSQL
6. Use production-grade Redis cluster
7. Scale Spark workers as needed

## Next Steps

- [API Documentation](http://localhost:8000/docs)
- [Architecture Overview](../README.md#architecture)
- [Contributing Guidelines](CONTRIBUTING.md)

## Getting Help

- Check logs: `docker-compose logs -f`
- Open an issue on GitHub
- Review [FAQ](FAQ.md)
