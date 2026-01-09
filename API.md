# API Documentation

## Base URL

```
http://localhost:8000/api
```

## Authentication

Currently, the API does not require authentication. For production use, implement JWT or API key authentication.

## Endpoints

### Health Check

Check if the API is running.

**GET** `/health`

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "websocket": "active",
  "timestamp": "2026-01-09T12:00:00.000Z"
}
```

---

### Get Tracked Cryptocurrencies

Get the list of cryptocurrencies being tracked.

**GET** `/cryptos`

**Response:**
```json
{
  "symbols": ["BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "SOLUSDT"],
  "count": 5
}
```

---

### Get Current Price

Get the current price for a specific cryptocurrency.

**GET** `/prices/{symbol}`

**Parameters:**
- `symbol` (path): Cryptocurrency symbol (e.g., BTCUSDT)

**Response:**
```json
{
  "symbol": "BTCUSDT",
  "name": "Bitcoin",
  "price": 45000.50,
  "volume_24h": 28000000000,
  "price_change_24h": 2.5,
  "timestamp": "2026-01-09T12:00:00.000Z"
}
```

---

### Get Historical Data

Get historical price data for a cryptocurrency.

**GET** `/historical/{symbol}`

**Parameters:**
- `symbol` (path): Cryptocurrency symbol
- `hours` (query, optional): Number of hours of history (default: 24)

**Response:**
```json
{
  "symbol": "BTCUSDT",
  "data": [
    {
      "price": 44500.00,
      "volume": 27500000000,
      "timestamp": "2026-01-08T12:00:00.000Z"
    },
    {
      "price": 45000.50,
      "volume": 28000000000,
      "timestamp": "2026-01-09T12:00:00.000Z"
    }
  ]
}
```

---

### Get Aggregated Metrics

Get windowed aggregations from Spark processing.

**GET** `/metrics/{symbol}`

**Parameters:**
- `symbol` (path): Cryptocurrency symbol
- `hours` (query, optional): Number of hours of metrics (default: 24)

**Response:**
```json
[
  {
    "symbol": "BTCUSDT",
    "window_start": "2026-01-09T11:00:00.000Z",
    "window_end": "2026-01-09T11:05:00.000Z",
    "avg_price": 44800.25,
    "vwap": 44795.50,
    "total_volume": 125000000,
    "price_volatility": 25.5,
    "avg_sentiment": 0.65
  }
]
```

**Metric Definitions:**
- `avg_price`: Average price during the window
- `vwap`: Volume Weighted Average Price
- `total_volume`: Total trading volume
- `price_volatility`: Standard deviation of price
- `avg_sentiment`: Average sentiment score (-1 to 1)

---

### Get Sentiment Scores

Get sentiment analysis scores for a cryptocurrency.

**GET** `/sentiment/{symbol}`

**Parameters:**
- `symbol` (path): Cryptocurrency symbol
- `hours` (query, optional): Number of hours of sentiment data (default: 24)

**Response:**
```json
{
  "symbol": "BTCUSDT",
  "data": [
    {
      "score": 0.75,
      "source": "twitter",
      "confidence": 0.85,
      "timestamp": "2026-01-09T12:00:00.000Z"
    }
  ]
}
```

**Sentiment Score:**
- `-1.0 to -0.7`: Very Bearish
- `-0.7 to -0.3`: Bearish
- `-0.3 to 0.3`: Neutral
- `0.3 to 0.7`: Bullish
- `0.7 to 1.0`: Very Bullish

---

### Get Market Alerts

Get active market alerts and anomalies.

**GET** `/alerts`

**Response:**
```json
{
  "alerts": [
    {
      "id": 1,
      "symbol": "BTCUSDT",
      "type": "price_spike",
      "severity": "high",
      "message": "Price increased by 12% in 5 minutes",
      "created_at": "2026-01-09T12:00:00.000Z"
    }
  ]
}
```

**Alert Types:**
- `price_spike`: Significant price increase
- `price_drop`: Significant price decrease
- `volume_surge`: Unusual volume increase
- `sentiment_shift`: Rapid sentiment change

**Severity Levels:**
- `low`: Minor event
- `medium`: Notable event
- `high`: Significant event
- `critical`: Major event requiring attention

---

## WebSocket API

### Connection

Connect to the WebSocket endpoint:

```
ws://localhost:8000/ws
```

### Messages

#### Connection Confirmation

After connecting, you'll receive:

```json
{
  "type": "connection",
  "status": "connected",
  "timestamp": "2026-01-09T12:00:00.000Z"
}
```

#### Subscribe to Symbol

**Send:**
```json
{
  "action": "subscribe",
  "symbol": "BTCUSDT"
}
```

**Receive:**
```json
{
  "type": "subscription",
  "status": "subscribed",
  "symbol": "BTCUSDT"
}
```

#### Unsubscribe from Symbol

**Send:**
```json
{
  "action": "unsubscribe",
  "symbol": "BTCUSDT"
}
```

#### Price Updates

Real-time price updates:

```json
{
  "type": "price_update",
  "symbol": "BTCUSDT",
  "price": 45000.50,
  "price_change_24h": 2.5,
  "volume_24h": 28000000000,
  "high_24h": 45500.00,
  "low_24h": 43800.00,
  "timestamp": "2026-01-09T12:00:00.000Z"
}
```

#### Trade Updates

Individual trade events:

```json
{
  "type": "trade",
  "symbol": "BTCUSDT",
  "price": 45001.00,
  "quantity": 0.5,
  "is_buyer_maker": true,
  "timestamp": "2026-01-09T12:00:00.000Z"
}
```

---

## Rate Limits

Current implementation has no rate limits. For production, implement:

- 100 requests per minute per IP
- 1000 requests per hour per IP
- WebSocket: Max 50 concurrent connections per IP

---

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message here"
}
```

**HTTP Status Codes:**
- `200`: Success
- `400`: Bad Request
- `404`: Not Found
- `500`: Internal Server Error

---

## Examples

### Python

```python
import requests
import websocket
import json

# REST API
response = requests.get('http://localhost:8000/api/prices/BTCUSDT')
data = response.json()
print(f"BTC Price: ${data['price']}")

# WebSocket
def on_message(ws, message):
    data = json.loads(message)
    if data['type'] == 'price_update':
        print(f"{data['symbol']}: ${data['price']}")

ws = websocket.WebSocketApp(
    'ws://localhost:8000/ws',
    on_message=on_message
)
ws.run_forever()
```

### JavaScript

```javascript
// REST API
fetch('http://localhost:8000/api/prices/BTCUSDT')
  .then(res => res.json())
  .then(data => console.log(`BTC Price: $${data.price}`));

// WebSocket
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.type === 'price_update') {
    console.log(`${data.symbol}: $${data.price}`);
  }
};

ws.onopen = () => {
  ws.send(JSON.stringify({
    action: 'subscribe',
    symbol: 'BTCUSDT'
  }));
};
```

### cURL

```bash
# Get current price
curl http://localhost:8000/api/prices/BTCUSDT

# Get historical data
curl "http://localhost:8000/api/historical/BTCUSDT?hours=24"

# Health check
curl http://localhost:8000/api/health
```

---

## Interactive Documentation

Visit http://localhost:8000/docs for interactive Swagger UI documentation where you can test all endpoints directly in your browser.
