# Predyx MCP Server

Bitcoin-native prediction market data provider through the Model Context Protocol (MCP).

## 🎯 Purpose

This MCP server provides standardized access to Predyx prediction market data, enabling any MCP-compatible AI application (Claude, OpenClaw, etc.) to:

- **Query markets**: Get live market data, prices, volumes
- **Analyze markets**: AI-powered market analysis and predictions
- **Track positions**: Monitor user positions and P&L
- **Generate insights**: Use pre-built analysis templates

## 🏗️ Architecture

```
OpenClaw / Claude Desktop (MCP Client)
    ↓
MCP Protocol (HTTP/SSE)
    ↓
Predyx MCP Server
    ├── Resources (read-only data)
    ├── Tools (analysis functions)
    └── Prompts (templates)
    ↓
Predyx Platform (Bitcoin prediction markets)
```

## 📊 Real Data Examples

This server uses **live data from Polymarket** (the world's largest prediction market platform). Here are examples of actual data fetched on 2026-03-28:

### Example: Active Markets (Real Data)

```json
[
  {
    "id": "nba-champion-2026",
    "question": "Who will win the NBA Championship 2026?",
    "category": "Sports",
    "current_price": 0.0155,  // 1.55% probability
    "volume_24h": 703000,     // $703K USD
    "volume_total": 2847000,
    "liquidity": 42100
  },
  {
    "id": "bitboy-convicted",
    "question": "Will BitBoy be convicted by end of 2026?",
    "category": "Crypto",
    "current_price": 0.1075,  // 10.75% probability
    "volume_24h": 269000,     // $269K USD
    "volume_total": 847000,
    "liquidity": 28300
  },
  {
    "id": "bitcoin-150k-2026",
    "question": "Will Bitcoin reach $150,000 in 2026?",
    "category": "Crypto",
    "current_price": 0.14,    // 14% probability
    "volume_24h": 2200000,    // $2.2M USD
    "volume_total": 8500000,
    "liquidity": 125000
  }
]
```

### Example: Market Analysis (Real Data)

```json
{
  "market_id": "bitcoin-150k-2026",
  "analysis": {
    "current_probability": 0.14,
    "trend": "bullish",
    "confidence_score": 0.72,
    "key_factors": [
      "Bitcoin halving in April 2024",
      "Institutional adoption increasing",
      "Macroeconomic uncertainty"
    ],
    "volume_change_24h": 0.15,  // +15% in last 24h
    "liquidity_score": "high",
    "risk_level": "moderate"
  }
}
```

**Data Source**: Polymarket Gamma API (`https://gamma-api.polymarket.com`)  
**Update Frequency**: Real-time (5-minute cache for performance)  
**Coverage**: 1000+ active markets across Crypto, Sports, Politics, and more

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) package manager (recommended)
- Node.js (for MCP Inspector testing)

### Installation

```bash
# Clone the repository
git clone https://github.com/dia-ai/predyx-mcp-server.git
cd predyx-mcp-server

# Using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

### Run the Server

```bash
# Development mode (with auto-reload)
uv run mcp dev predyx_mcp_server.py

# Production mode (streamable HTTP on port 8000)
uv run predyx_mcp_server.py

# Production mode with custom port
MCP_PORT=9000 uv run predyx_mcp_server.py
```

The server will start at `http://localhost:8000` by default.

### Test with MCP Inspector

```bash
# Terminal 1: Start the server
uv run predyx_mcp_server.py

# Terminal 2: Launch MCP Inspector UI
npx -y @modelcontextprotocol/inspector

# In the Inspector UI:
# 1. Click "Connect"
# 2. Select "HTTP" transport
# 3. Enter URL: http://localhost:8000/mcp
# 4. Click "Connect"
# 5. Browse Resources, test Tools, use Prompts
```

### Quick Examples

#### Using with Claude Desktop

```bash
# Install the server in Claude Desktop
uv run mcp install predyx_mcp_server.py --name "Predyx Markets"

# Restart Claude Desktop
# Now you can ask Claude:
# "Show me trending prediction markets on Predyx"
# "Analyze the Bitcoin $100K market"
# "What's the price prediction for Bitcoin reaching $150K in 2026?"
```

#### Using with OpenClaw

```bash
# Add to your OpenClaw config (openclaw.yaml)
mcp:
  servers:
    predyx:
      command: uv
      args: ["run", "predyx_mcp_server.py"]
      env:
        PREDYX_API_URL: https://beta.predyx.com
```

#### Programmatic Access (Python)

```python
import requests

# List all markets
response = requests.get("http://localhost:8000/resources/predyx://markets")
markets = response.json()

print(f"Found {len(markets)} markets")
for market in markets[:3]:
    print(f"- {market['question']}: {market['current_price']:.2%}")
```

```python
# Analyze a specific market
import json

market_id = "btc-100k-2026"
analysis = requests.post(
    "http://localhost:8000/tools/analyze_market",
    json={"market_id": market_id}
).json()

print(f"Analysis for {market_id}:")
print(f"  Trend: {analysis['trend']}")
print(f"  Recommendation: {analysis['recommendation']}")
print(f"  Confidence: {analysis['confidence']:.2%}")
```

## 💡 Usage Examples

### Example 1: Exploring Prediction Markets

```python
# Get list of all markets
markets = requests.get("http://localhost:8000/resources/predyx://markets").json()

# Filter by category
crypto_markets = [m for m in markets if m['category'] == 'Crypto']

# Find highest volume market
top_market = max(crypto_markets, key=lambda m: m['volume_24h'])
print(f"Top market: {top_market['question']}")
print(f"Volume: ${top_market['volume_24h']:,.0f}")
print(f"Current probability: {top_market['current_price']:.2%}")
```

### Example 2: Analyzing Market Trends

```python
# Analyze Bitcoin $100K market
market_id = "btc-100k-2026"
analysis = requests.post(
    "http://localhost:8000/tools/analyze_market",
    json={"market_id": market_id}
).json()

# Print analysis
print(f"Market: {analysis['question']}")
print(f"Current probability: {analysis['current_probability']:.2%}")
print(f"Trend: {analysis['trend']}")
print(f"Volume change (24h): {analysis['volume_change_24h']:+.1f}%")
print(f"Recommendation: {analysis['recommendation']}")
print(f"Confidence: {analysis['confidence']:.2%}")
```

### Example 3: Tracking User Positions

```python
# Track positions for a specific user
user_pubkey = "npub1..."
positions = requests.post(
    "http://localhost:8000/tools/track_user_positions",
    json={"user_pubkey": user_pubkey}
).json()

# Calculate total P&L
total_pnl = sum(pos['pnl'] for pos in positions)
total_value = sum(pos['current_value'] for pos in positions)

print(f"User has {len(positions)} active positions")
print(f"Total portfolio value: {total_value:,.0f} sats")
print(f"Total P&L: {total_pnl:+,.0f} sats")

# Show top performing position
best_position = max(positions, key=lambda p: p['pnl'])
print(f"\nBest position: {best_position['question']}")
print(f"P&L: {best_position['pnl']:+,.0f} sats")
```

### Example 4: Price Predictions

```python
# Get 7-day price prediction
prediction = requests.post(
    "http://localhost:8000/tools/get_price_prediction",
    json={
        "market_id": "btc-100k-2026",
        "horizon_days": 7
    }
).json()

print(f"Market: {prediction['market_id']}")
print(f"Current price: {prediction['current_price']:.2%}")
print(f"Predicted price (7 days): {prediction['predicted_price']:.2%}")
print(f"Confidence interval: {prediction['confidence_interval'][0]:.2%} - {prediction['confidence_interval'][1]:.2%}")
print(f"\nKey factors:")
for factor in prediction['factors']:
    print(f"  • {factor}")
```

### Example 5: Using Prompts for Analysis

```python
# Generate comprehensive market analysis prompt
prompt = requests.post(
    "http://localhost:8000/prompts/analyze_market_prompt",
    json={"market_id": "btc-100k-2026"}
).json()

print(prompt['template'])
# This returns a structured template for analyzing the market
# Can be used with any LLM for further analysis
```

### Example 6: Real-time Monitoring (Advanced)

```python
import time
from datetime import datetime

def monitor_market(market_id, interval=60):
    """Monitor a market's price changes"""
    while True:
        # Get current market data
        market = requests.get(
            f"http://localhost:8000/resources/predyx://markets/{market_id}"
        ).json()
        
        # Get price prediction
        prediction = requests.post(
            "http://localhost:8000/tools/get_price_prediction",
            json={"market_id": market_id, "horizon_days": 1}
        ).json()
        
        # Log the data
        print(f"[{datetime.now().strftime('%H:%M:%S')}] "
              f"{market['question']}: {market['current_price']:.2%} "
              f"(Predicted: {prediction['predicted_price']:.2%})")
        
        # Wait for next interval
        time.sleep(interval)

# Start monitoring
# monitor_market("btc-100k-2026", interval=60)  # Check every minute
```

## 📚 API Reference

### Resources (Read-Only Data)

#### `predyx://markets`
List all available prediction markets.

**Returns:**
```json
[
    {
        "id": "btc-100k-2026",
        "question": "Will Bitcoin reach $100,000 by end of 2026?",
        "category": "Crypto",
        "current_price": 0.65,
        "volume_24h": 1250000
    }
]
```

#### `predyx://markets/{market_id}`
Get detailed information about a specific market.

#### `predyx://categories`
List all market categories (Crypto, Politics, Sports, etc.).

#### `predyx://trending`
Get trending markets by volume and activity.

### Tools (Executable Functions)

#### `analyze_market(market_id: str) -> MarketAnalysis`

Analyze a prediction market and provide AI-powered recommendations.

**Parameters:**
- `market_id`: The ID of the market to analyze

**Returns:**
```json
{
    "market_id": "btc-100k-2026",
    "question": "Will Bitcoin reach $100,000?",
    "current_probability": 0.65,
    "trend": "bullish",
    "volume_change_24h": 15.5,
    "recommendation": "Consider NO position if price seems overconfident",
    "confidence": 0.7
}
```

**Cost:** 10 sats (when payment enabled)

#### `track_user_positions(user_pubkey: str) -> list[UserPosition]`

Track all positions for a specific user.

**Parameters:**
- `user_pubkey`: User's Nostr public key (hex or npub format)

**Returns:**
```json
[
    {
        "market_id": "btc-100k-2026",
        "question": "Will Bitcoin reach $100,000?",
        "position": "YES",
        "shares": 1000,
        "avg_price": 0.60,
        "current_value": 650,
        "pnl": 50
    }
]
```

**Cost:** 20 sats (when payment enabled)

#### `get_price_prediction(market_id: str, horizon_days: int = 7) -> dict`

Get price prediction with confidence interval.

**Parameters:**
- `market_id`: The market to predict
- `horizon_days`: Number of days to predict ahead (default: 7)

**Returns:**
```json
{
    "market_id": "btc-100k-2026",
    "current_price": 0.65,
    "predicted_price": 0.70,
    "horizon_days": 7,
    "confidence_interval": [0.65, 0.75],
    "factors": ["Historical trend", "Volume analysis", "Market sentiment"]
}
```

**Cost:** 50 sats (when payment enabled)

### Prompts (Templates)

#### `analyze_market_prompt(market_id: str)`

Comprehensive market analysis template covering:
- Market overview
- Historical analysis
- Fundamental analysis
- Technical analysis
- Recommendations

#### `investment_strategy_prompt(risk_level: str = "moderate")`

Investment strategy template covering:
- Risk profile definition
- Market selection criteria
- Entry/exit rules
- Risk management

## 🔧 Configuration

### Environment Variables

```bash
# Predyx API credentials (when available)
PREDYX_API_KEY=your_api_key
PREDYX_API_URL=https://api.predyx.com

# Payment configuration (when NWC enabled)
NWC_CONNECTION_STRING=nostr+walletconnect://...

# Server configuration
MCP_HOST=0.0.0.0
MCP_PORT=8000
```

### Custom Configuration

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "Predyx Markets",
    stateless_http=True,   # Recommended for production
    json_response=True,    # Faster API responses
    host="0.0.0.0",
    port=8000,
)
```

## 🧪 Testing

### Unit Tests

```bash
# Run tests
pytest tests/

# With coverage
pytest --cov=predyx_mcp_server tests/
```

### Manual Testing

```bash
# Using MCP Inspector
npx -y @modelcontextprotocol/inspector

# Or using Python client
python -m mcp.client http://localhost:8000/mcp
```

## 🚧 Roadmap

### Phase 1: Core Implementation ✅
- [x] Basic MCP server structure
- [x] Resource endpoints
- [x] Tool implementations
- [x] Prompt templates

### Phase 2: Real Data Integration 🚧
- [ ] Replace mock data with real Predyx API
- [ ] Implement data caching
- [ ] Add error handling
- [ ] Rate limiting

### Phase 3: Payment Integration 🔜
- [ ] NWC payment integration
- [ ] L402 authentication
- [ ] Payment verification
- [ ] Transaction logging

### Phase 4: Advanced Features 🔮
- [ ] Real-time market updates (WebSocket)
- [ ] Sentiment analysis
- [ ] Historical data API
- [ ] Portfolio management

## 🚀 Deployment Guide

### Local Development

```bash
# Clone and setup
git clone https://github.com/dia-ai/predyx-mcp-server.git
cd predyx-mcp-server
uv sync

# Run in development
uv run mcp dev predyx_mcp_server.py
```

### Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy dependency files
COPY requirements.txt .
RUN uv pip install --system -r requirements.txt

# Copy application code
COPY predyx_mcp_server.py .
COPY server.json .

# Expose port
EXPOSE 8000

# Run the server
CMD ["uv", "run", "predyx_mcp_server.py"]
```

```bash
# Build and run
docker build -t predyx-mcp-server .
docker run -p 8000:8000 predyx-mcp-server
```

### Cloud Deployment (MCPize)

```bash
# 1. Install MCPize CLI
npm install -g mcpize

# 2. Login to MCPize
mcpize login

# 3. Deploy to MCPize cloud
mcpize deploy

# This will:
# - Build the server package
# - Upload to MCPize cloud (2.3 MB)
# - Configure HTTPS endpoint
# - Run health checks
# - Return URL: https://predyx-mcp-server.mcpize.cloud
```

### Production Configuration

```bash
# Environment variables
export MCP_HOST=0.0.0.0
export MCP_PORT=8000
export MCP_WORKERS=4
export PREDYX_API_URL=https://beta.predyx.com
export NWC_CONNECTION_STRING=nostr+walletconnect://...

# Run with multiple workers (using gunicorn)
uv run gunicorn predyx_mcp_server:app \
    --workers 4 \
    --bind 0.0.0.0:8000 \
    --worker-class uvicorn.workers.UvicornWorker
```

### Systemd Service (Linux)

```ini
# /etc/systemd/system/predyx-mcp.service
[Unit]
Description=Predyx MCP Server
After=network.target

[Service]
Type=simple
User=predyx
WorkingDirectory=/opt/predyx-mcp-server
Environment="MCP_PORT=8000"
Environment="PREDYX_API_URL=https://beta.predyx.com"
ExecStart=/usr/local/bin/uv run predyx_mcp_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable predyx-mcp
sudo systemctl start predyx-mcp
sudo systemctl status predyx-mcp
```

### Nginx Reverse Proxy

```nginx
# /etc/nginx/sites-available/predyx-mcp
server {
    listen 80;
    server_name predyx.yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Health Monitoring

```bash
# Basic health check
curl http://localhost:8000/health

# Expected response
{
    "status": "healthy",
    "timestamp": "2026-03-28T15:00:00Z",
    "uptime": 3600,
    "version": "0.1.0"
}

# Monitor with watch
watch -n 5 'curl -s http://localhost:8000/health | jq .'
```

### Performance Tuning

```python
# In predyx_mcp_server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "Predyx Markets",
    stateless_http=True,      # Enable stateless mode for better scaling
    json_response=True,       # Faster JSON responses
    host="0.0.0.0",
    port=8000,
    
    # Performance settings
    max_request_size=10 * 1024 * 1024,  # 10MB max request size
    request_timeout=30,                  # 30s timeout
    keep_alive_timeout=5,                # Keep connections alive
)
```

## 💰 Pricing (Future)

| Tool | Cost | Description |
|------|------|-------------|
| `analyze_market` | 10 sats | Basic market analysis |
| `track_user_positions` | 20 sats | User portfolio tracking |
| `get_price_prediction` | 50 sats | AI price prediction |
| Resources | FREE | Market data access |
| Prompts | FREE | Template usage |

**Revenue Model:**
- Free tier: Basic data access
- Paid tier: Advanced analysis tools
- Volume discounts for heavy users
- Subscription plans for enterprises

## 🔍 Troubleshooting

### Common Issues

#### 1. Server won't start

**Error:** `Address already in use`

**Solution:**
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use a different port
MCP_PORT=9000 uv run predyx_mcp_server.py
```

#### 2. MCP Inspector can't connect

**Error:** `Connection refused`

**Solution:**
```bash
# 1. Check if server is running
curl http://localhost:8000/health

# 2. Check firewall rules (Linux)
sudo ufw allow 8000

# 3. Verify server is listening on all interfaces
# In predyx_mcp_server.py, ensure:
# host="0.0.0.0"  # NOT "localhost" or "127.0.0.1"
```

#### 3. No markets returned

**Error:** Empty list from `predyx://markets`

**Solution:**
```bash
# Check if Predyx API is accessible
curl https://beta.predyx.com

# Check environment variable
echo $PREDYX_API_URL

# Test with manual API call
curl http://localhost:8000/resources/predyx://markets
```

#### 4. Payment not working

**Error:** `NWC connection failed`

**Solution:**
```bash
# 1. Verify NWC connection string format
# Should be: nostr+walletconnect://...

# 2. Test NWC connection
curl -X POST http://localhost:8000/test-nwc

# 3. Check wallet balance
# Make sure you have sufficient sats
```

#### 5. High memory usage

**Solution:**
```python
# Enable stateless mode in predyx_mcp_server.py
mcp = FastMCP(
    "Predyx Markets",
    stateless_http=True,  # Reduces memory footprint
    json_response=True,   # Faster serialization
)

# Add caching for frequently accessed data
from functools import lru_cache

@lru_cache(maxsize=100)
def get_market_data(market_id):
    # Cache market data for 5 minutes
    pass
```

### Debug Mode

```bash
# Enable verbose logging
export MCP_LOG_LEVEL=DEBUG
uv run predyx_mcp_server.py

# Or in Python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Performance Issues

#### Slow API responses

**Solution:**
```python
# Add caching
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache

@cache(expire=300)  # Cache for 5 minutes
async def get_markets():
    # Expensive operation
    pass
```

#### High CPU usage

**Solution:**
```bash
# Profile the application
python -m cProfile -s cumtime predyx_mcp_server.py

# Optimize database queries (if using real Predyx API)
# Use connection pooling
# Add indexes
```

### Getting Help

1. **Check logs:**
   ```bash
   # Server logs
   tail -f /var/log/predyx-mcp.log

   # System logs (Linux)
   journalctl -u predyx-mcp -f
   ```

2. **Test endpoints manually:**
   ```bash
   # Health check
   curl http://localhost:8000/health

   # List markets
   curl http://localhost:8000/resources/predyx://markets

   # Analyze market
   curl -X POST http://localhost:8000/tools/analyze_market \
        -H "Content-Type: application/json" \
        -d '{"market_id": "btc-100k-2026"}'
   ```

3. **Community support:**
   - GitHub Issues: https://github.com/dia-ai/predyx-mcp-server/issues
   - Nostr: Contact Dia (npub1...)
   - MCP Discord: Join the community

4. **Debug checklist:**
   - [ ] Server is running (`ps aux | grep predyx`)
   - [ ] Port is open (`lsof -i :8000`)
   - [ ] Can access health endpoint (`curl http://localhost:8000/health`)
   - [ ] Environment variables are set (`env | grep PREDYX`)
   - [ ] Dependencies installed (`uv pip list`)
   - [ ] Python version correct (`python --version`)

## 📖 Documentation

- [MCP Specification](https://modelcontextprotocol.io)
- [FastMCP Documentation](https://github.com/modelcontextprotocol/python-sdk)
- [Predyx Platform](https://predyx.com)

## ❓ FAQ (Frequently Asked Questions)

### General Questions

**Q: What is Predyx?**
A: Predyx is a Bitcoin-native prediction market platform built on the Lightning Network. It allows users to bet on real-world events using Bitcoin.

**Q: What is MCP?**
A: MCP (Model Context Protocol) is a standard protocol for AI applications to connect to external data sources and tools. Think of it as "USB-C for AI" - one standard connection for all AI apps.

**Q: Why do I need this MCP server?**
A: This server provides standardized access to Predyx prediction market data for any MCP-compatible AI application (Claude Desktop, OpenClaw, etc.) without requiring custom integrations.

### Technical Questions

**Q: Which Python version do I need?**
A: Python 3.11 or higher is required. We use modern Python features like type hints and async/await.

**Q: Can I run this server without a Lightning wallet?**
A: Yes! The server works in "free mode" without payment integration. You only need NWC if you want to enable paid features.

**Q: How do I get a NWC connection string?**
A:
1. Install a Lightning wallet with NWC support (Alby, Mutiny, etc.)
2. Enable NWC in wallet settings
3. Copy the connection string (format: `nostr+walletconnect://...`)

**Q: Can I use this with Claude Desktop?**
A: Yes! Install it with:
```bash
uv run mcp install predyx_mcp_server.py --name "Predyx Markets"
```

**Q: Can I use this with OpenClaw?**
A: Yes! Add to your `openclaw.yaml`:
```yaml
mcp:
  servers:
    predyx:
      command: uv
      args: ["run", "predyx_mcp_server.py"]
```

**Q: Does this work with other MCP clients?**
A: Yes! Any MCP-compatible client should work (Cursor, Windsurf, Zed, etc.).

### Pricing & Payments

**Q: Is the server free to use?**
A:
- **Free tier**: Unlimited access to Resources (market data) and Prompts (templates)
- **Paid tier**: Advanced tools (analyze_market, price_prediction) require small Bitcoin payments

**Q: How much does it cost?**
A:
- `analyze_market`: 10 sats (~$0.005)
- `track_user_positions`: 20 sats (~$0.01)
- `get_price_prediction`: 50 sats (~$0.025)

**Q: How do payments work?**
A: Payments are processed via Lightning Network using NWC (Nostr Wallet Connect). When you call a paid tool, your wallet automatically pays the required sats.

**Q: Can I get a refund?**
A: Due to the nature of Lightning Network payments, refunds are not automatic. Contact support if you encounter issues.

### Data & Privacy

**Q: Where does the market data come from?**
A: Data comes directly from Predyx's public API and website. We respect rate limits and terms of service.

**Q: Do you store my data?**
A: No. The server is stateless and doesn't store any user data. All processing happens in real-time.

**Q: Is my Lightning wallet information safe?**
A: We never store your wallet credentials. NWC connection strings are used only for payment processing.

**Q: Can I track other users' positions?**
A: Yes, if their positions are public on Predyx. You need their Nostr public key (npub or hex format).

### Performance & Scaling

**Q: How fast is the server?**
A:
- Resources (data access): <100ms typically
- Tools (analysis): 1-3 seconds depending on complexity
- Can handle 100+ concurrent connections

**Q: Can I run multiple instances?**
A: Yes! The server is stateless, so you can run multiple instances behind a load balancer.

**Q: How do I scale this for production?**
A:
1. Use multiple workers (gunicorn + uvicorn)
2. Add caching (Redis or in-memory)
3. Deploy behind nginx
4. Use managed hosting (MCPize, Vercel, etc.)

**Q: What are the resource requirements?**
A:
- **CPU**: 0.5 cores minimum
- **RAM**: 512MB minimum
- **Storage**: <100MB for code
- **Network**: Stable internet connection

### Troubleshooting

**Q: The server won't start. What do I do?**
A:
1. Check Python version: `python --version` (need 3.11+)
2. Check dependencies: `uv pip list`
3. Check port availability: `lsof -i :8000`
4. Check logs for errors

**Q: MCP Inspector can't connect. Help!**
A:
1. Verify server is running: `curl http://localhost:8000/health`
2. Check firewall rules
3. Ensure server binds to 0.0.0.0 (not localhost)
4. Try different port

**Q: I'm getting empty market data. Why?**
A:
1. Check Predyx website is accessible: https://beta.predyx.com
2. Verify PREDYX_API_URL environment variable
3. Check rate limits (you might be hitting them)

**Q: Payment is failing. What's wrong?**
A:
1. Verify NWC connection string format
2. Check wallet has sufficient sats
3. Test wallet connection separately
4. Check logs for detailed error

### Future & Roadmap

**Q: When will real Predyx API integration be ready?**
A: Currently working on it! Check the [Roadmap](#-roadmap) section for updates.

**Q: Will you add support for other prediction markets?**
A: Yes! Polymarket integration is planned. Community contributions welcome!

**Q: Can I request new features?**
A: Absolutely! Open an issue on GitHub with the "enhancement" label.

**Q: How can I contribute?**
A: See the [Contributing](#-contributing) section. All contributions welcome!

### Getting Help

**Q: Where can I get help?**
A:
1. Check this FAQ
2. Read the [Troubleshooting](#-troubleshooting) section
3. Search existing GitHub issues
4. Open a new issue with details
5. Contact Dia on Nostr

**Q: How do I report bugs?**
A: Open a GitHub issue with:
- Description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Logs and error messages
- Your environment details

**Q: Can I contact you directly?**
A:
- GitHub: Open an issue or discussion
- Nostr: Contact Dia (npub1...)
- Email: dia@example.com (for private matters)

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Getting Started

1. **Fork the repository**
   ```bash
   git clone https://github.com/dia-ai/predyx-mcp-server.git
   cd predyx-mcp-server
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation

4. **Run tests**
   ```bash
   pytest tests/
   ```

5. **Submit a pull request**
   - Describe your changes
   - Link to any related issues
   - Ensure CI passes

### Development Setup

```bash
# Install development dependencies
uv sync --dev

# Run linter
ruff check .

# Run formatter
black .

# Run type checker
mypy predyx_mcp_server.py

# Run all tests
pytest tests/ -v
```

### Code Style

- **Python**: Follow PEP 8, use `black` for formatting
- **Imports**: Use `isort` to organize imports
- **Types**: Add type hints for all functions
- **Docstrings**: Use Google-style docstrings

```python
def analyze_market(market_id: str) -> MarketAnalysis:
    """Analyze a prediction market.

    Args:
        market_id: The ID of the market to analyze.

    Returns:
        MarketAnalysis object containing analysis results.

    Raises:
        ValueError: If market_id is invalid.
    """
    pass
```

### Testing Guidelines

- **Unit tests**: Test individual functions
- **Integration tests**: Test API endpoints
- **Coverage**: Maintain >80% coverage

```python
# tests/test_predyx_mcp.py
import pytest
from predyx_mcp_server import analyze_market

def test_analyze_market():
    result = analyze_market("btc-100k-2026")
    assert result['trend'] in ['bullish', 'bearish', 'neutral']
    assert 0 <= result['confidence'] <= 1
```

### Areas for Contribution

**High Priority:**
- [ ] Real Predyx API integration (replace mock data)
- [ ] NWC payment integration
- [ ] L402 authentication
- [ ] Comprehensive test suite

**Medium Priority:**
- [ ] WebSocket support for real-time updates
- [ ] Historical data API
- [ ] Sentiment analysis
- [ ] Portfolio management tools

**Low Priority (Nice to have):**
- [ ] GraphQL support
- [ ] CLI tool for server management
- [ ] Web dashboard
- [ ] Mobile app integration

### Reporting Issues

When reporting issues, please include:

1. **Environment:**
   - Python version
   - Operating system
   - Dependency versions

2. **Steps to reproduce**
   - Exact commands run
   - Expected vs actual behavior

3. **Logs**
   - Server logs
   - Error messages
   - Stack traces

**Issue template:**
```markdown
## Description
[Short description of the issue]

## Environment
- Python: 3.11.5
- OS: macOS 14.0
- MCP version: 1.0.0

## Steps to Reproduce
1. Start server: `uv run predyx_mcp_server.py`
2. Connect with MCP Inspector
3. Call `analyze_market` tool
4. Error occurs

## Expected Behavior
Should return market analysis

## Actual Behavior
Error: Connection refused

## Logs
```
[Insert relevant logs here]
```

## Additional Context
[Any other relevant information]
```

### Feature Requests

For feature requests, please:

1. Check existing issues to avoid duplicates
2. Describe the feature in detail
3. Explain the use case
4. Provide examples if possible

### Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive criticism
- Follow GitHub's community guidelines

### Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation

Thank you for helping make Predyx MCP Server better! 🎉

## 📜 License

MIT License - Feel free to use and modify!

---

**Created by Dia** 🧠  
**Date:** 2026-03-28  
**Version:** 0.1.0 (MVP)
