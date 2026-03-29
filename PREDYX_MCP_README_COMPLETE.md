# Predyx MCP Server

> 🚀 **Bitcoin-native prediction market data provider** - Real-time market data, AI-powered analysis, and price predictions via Model Context Protocol (MCP)

[![MCP Version](https://img.shields.io/badge/MCP-1.0-blue)](https://modelcontextprotocol.io)
[![Python](https://img.shields.io/badge/Python-3.11+-green)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## 📖 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
- [API Reference](#api-reference)
- [Pricing](#pricing)
- [Architecture](#architecture)
- [Development](#development)
- [Contributing](#contributing)
- [Support](#support)

---

## 🎯 Overview

**Predyx MCP Server** bridges prediction markets (Polymarket, Predyx) with AI agents through the **Model Context Protocol (MCP)** - the emerging standard for AI tool connectivity.

### Why Predyx MCP Server?

- ✅ **Bitcoin-Native**: Built for Lightning Network with sats-based pricing
- ✅ **Real-Time Data**: Live market data from Polymarket and Predyx
- ✅ **AI-Powered Analysis**: Advanced market analysis and price predictions
- ✅ **MCP Standard**: Works with Claude, Cursor, VS Code, and other MCP clients
- ✅ **Freemium Model**: Free tier for exploration, pay only for advanced features

### Use Cases

- **AI Trading Assistants**: Provide real-time market analysis to AI agents
- **Research Tools**: Aggregate prediction market data for research
- **Portfolio Tracking**: Monitor positions across multiple markets
- **Price Predictions**: AI-powered forecasting for market outcomes

---

## ✨ Features

### 📊 Resources (Read-Only Data)

| Resource | Description | Free |
|----------|-------------|------|
| `predyx://markets` | List all prediction markets | ✅ |
| `predyx://markets/{id}` | Market details & price history | ✅ |
| `predyx://categories` | Market categories (Crypto, Sports, Politics) | ✅ |
| `predyx://trending` | Most active markets in 24h | ✅ |

### 🔧 Tools (Paid Services)

| Tool | Description | Price |
|------|-------------|-------|
| `analyze_market` | AI-powered market analysis | 10 sats |
| `track_user_positions` | Track user's portfolio | 20 sats |
| `get_price_prediction` | Price prediction (1-30 days) | 50 sats |

### 📝 Prompts (Templates)

| Prompt | Description |
|--------|-------------|
| `analyze_market_prompt` | Comprehensive analysis with risk assessment |
| `investment_strategy_prompt` | Generate investment strategies |

---

## 🚀 Installation

### Prerequisites

- Python 3.11+
- `uv` package manager (recommended)
- Optional: NWC connection string for payment processing

### Install via MCP Client

**Claude Desktop**:
```json
{
  "mcpServers": {
    "predyx": {
      "command": "uv",
      "args": ["run", "--with", "mcp", "predyx_mcp_server.py"]
    }
  }
}
```

**Cursor / VS Code**:
```json
{
  "predyx": {
    "command": "uv",
    "args": ["run", "--with", "mcp", "predyx_mcp_server.py"],
    "env": {
      "NWC_CONN_STR": "your_nwc_string_here"
    }
  }
}
```

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/dia-ai/predyx-mcp-server.git
cd predyx-mcp-server

# Install dependencies
pip install mcp pydantic

# Run the server
python predyx_mcp_server.py
```

---

## 🏃 Quick Start

### Example 1: List Markets

```python
# Using MCP client
result = await client.read_resource("predyx://markets")

# Sample output
{
  "markets": [
    {
      "id": "btc-100k-2026",
      "question": "Will Bitcoin reach $100K in 2026?",
      "current_price": 0.69,
      "volume_24h": 44252,
      "category": "Crypto"
    }
  ]
}
```

### Example 2: Analyze Market

```python
# Call the analysis tool
analysis = await client.call_tool(
    "analyze_market",
    {"market_id": "btc-100k-2026"}
)

# Sample output
{
  "market_id": "btc-100k-2026",
  "sentiment": "bullish",
  "confidence": 0.72,
  "key_factors": [
    "Institutional adoption increasing",
    "Hash rate at all-time high",
    "Regulatory clarity improving"
  ],
  "risk_level": "moderate",
  "recommendation": "Consider long position with 2-5% portfolio allocation"
}
```

### Example 3: Price Prediction

```python
# Get 7-day price prediction
prediction = await client.call_tool(
    "get_price_prediction",
    {
        "market_id": "btc-100k-2026",
        "horizon_days": 7
    }
)

# Sample output
{
  "market_id": "btc-100k-2026",
  "current_price": 0.69,
  "predicted_price": 0.74,
  "confidence_interval": [0.68, 0.80],
  "model": "ensemble_lstm",
  "factors": ["Historical volatility", "Market sentiment", "Correlation with BTC/USD"]
}
```

---

## 📚 API Reference

### Resources

#### `predyx://markets`
List all available prediction markets.

**Returns**: JSON array of market objects

```json
{
  "id": "string",
  "question": "string",
  "current_price": "number (0-1)",
  "volume_24h": "number (sats)",
  "category": "string",
  "end_date": "ISO 8601 date"
}
```

#### `predyx://markets/{market_id}`
Get detailed information about a specific market.

**Returns**: Market object with price history and statistics

```json
{
  "id": "string",
  "question": "string",
  "description": "string",
  "current_price": "number",
  "price_history": [
    {"timestamp": "ISO 8601", "price": "number"}
  ],
  "volume_total": "number",
  "liquidity": "number",
  "creator": "string (npub)"
}
```

#### `predyx://categories`
List all market categories.

**Returns**: Array of category objects

```json
[
  {
    "name": "Crypto",
    "market_count": 42,
    "total_volume": "number (sats)"
  }
]
```

#### `predyx://trending`
Get trending markets in the last 24 hours.

**Returns**: Top 10 markets sorted by volume and activity

### Tools

#### `analyze_market`
Perform AI-powered analysis on a specific prediction market.

**Parameters**:
- `market_id` (string, required): Market identifier

**Returns**:
```json
{
  "market_id": "string",
  "sentiment": "bullish|bearish|neutral",
  "confidence": "number (0-1)",
  "key_factors": ["string"],
  "risk_level": "low|moderate|high",
  "recommendation": "string"
}
```

**Pricing**: 10 sats per call

#### `track_user_positions`
Track a user's positions and profit/loss across all markets.

**Parameters**:
- `pubkey` (string, required): User's Nostr public key (npub format)

**Returns**:
```json
{
  "pubkey": "string",
  "positions": [
    {
      "market_id": "string",
      "outcome": "yes|no",
      "shares": "number",
      "avg_price": "number",
      "current_price": "number",
      "pnl": "number (sats)",
      "pnl_percent": "number"
    }
  ],
  "total_pnl": "number (sats)"
}
```

**Pricing**: 20 sats per call

#### `get_price_prediction`
Get AI-powered price prediction for a market over a specified time horizon.

**Parameters**:
- `market_id` (string, required): Market identifier
- `horizon_days` (integer, optional): Prediction horizon (1-30 days, default: 7)

**Returns**:
```json
{
  "market_id": "string",
  "current_price": "number",
  "predicted_price": "number",
  "confidence_interval": ["number", "number"],
  "model": "string",
  "factors": ["string"]
}
```

**Pricing**: 50 sats per call

### Prompts

#### `analyze_market_prompt`
Generate comprehensive market analysis template.

**Arguments**:
- `market_id` (string, required): Market to analyze
- `risk_tolerance` (string, optional): User's risk tolerance (conservative/moderate/aggressive)

#### `investment_strategy_prompt`
Generate investment strategy based on market conditions.

**Arguments**:
- `market_category` (string, required): Category of markets to focus on
- `investment_amount` (number, optional): Amount to invest in sats

---

## 💰 Pricing

### Freemium Model

#### Free Tier
- ✅ **Unlimited** access to all Resources (market data, listings, trending)
- ✅ **5 free tool calls** per day
- ✅ All Prompts templates

#### Paid Tier
- **`analyze_market`**: 10 sats/call
- **`track_user_positions`**: 20 sats/call
- **`get_price_prediction`**: 50 sats/call

### Payment Methods

- **Lightning Network (NWC)**: Instant, low-fee micropayments
- **L402 (HTTP 402)**: Standardized API access protocol

### How to Upgrade

1. Set up a Lightning wallet with NWC support (Alby, LNbits, etc.)
2. Get your NWC connection string
3. Configure in your MCP client:
   ```json
   {
     "env": {
       "NWC_CONN_STR": "nostr+walletconnect://..."
     }
   }
   ```
4. Start making paid calls!

---

## 🏗️ Architecture

```
┌─────────────────┐
│  MCP Client     │ (Claude, Cursor, VS Code)
│  (Claude/etc)   │
└────────┬────────┘
         │ MCP Protocol
         ▼
┌─────────────────┐
│ Predyx MCP      │
│ Server          │
└──┬───────────┬──┘
   │           │
   ▼           ▼
┌─────┐   ┌──────┐
│Data │   │Payment│
│Layer│   │ Layer │
└─────┘   └──────┘
   │           │
   ▼           ▼
┌─────────┐ ┌────────┐
│Polymarket│ │Lightning│
│Predyx   │ │Network  │
└─────────┘ └────────┘
```

### Technology Stack

- **Language**: Python 3.11+
- **Framework**: FastMCP (official MCP Python SDK)
- **Data Validation**: Pydantic
- **Transport**: Streamable HTTP (production-ready)
- **Payment**: NWC (Nostr Wallet Connect) + L402

---

## 🛠️ Development

### Local Development

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run linter
ruff check .

# Format code
black .
```

### Testing with MCP Inspector

```bash
# Interactive UI testing
npx @modelcontextprotocol/inspector uv run --with mcp predyx_mcp_server.py

# CLI testing
npx @modelcontextprotocol/inspector --cli uv run --with mcp predyx_mcp_server.py
```

### Project Structure

```
predyx-mcp-server/
├── predyx_mcp_server.py    # Main server implementation
├── polymarket_client.py     # Polymarket API client
├── server.json             # MCP Registry configuration
├── mcpize.yaml             # MCPize deployment config
├── README.md               # This file
├── tests/                  # Test suite
│   └── test_predyx_mcp.py
└── examples/               # Usage examples
    ├── basic_usage.py
    └── advanced_analysis.py
```

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Roadmap

- [ ] Add more prediction market platforms (Metaculus, Manifold Markets)
- [ ] Implement WebSocket for real-time updates
- [ ] Add portfolio management tools
- [ ] Create web dashboard for analytics
- [ ] Multi-language SDK support

---

## 📞 Support

- **Documentation**: [GitHub Wiki](https://github.com/dia-ai/predyx-mcp-server/wiki)
- **Issues**: [GitHub Issues](https://github.com/dia-ai/predyx-mcp-server/issues)
- **Nostr**: `npub1...` (coming soon)
- **Email**: dia@example.com

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Anthropic** for the Model Context Protocol
- **Polymarket** for the public API
- **Predyx** for Bitcoin-native prediction markets
- **Lightning Network** for instant micropayments

---

**Built with ❤️ by Dia AI** | **Powered by MCP + Lightning Network**

---

## 📊 Stats

![GitHub stars](https://img.shields.io/github/stars/dia-ai/predyx-mcp-server?style=social)
![GitHub forks](https://img.shields.io/github/forks/dia-ai/predyx-mcp-server?style=social)
![MCP Downloads](https://img.shields.io/badge/Downloads-Coming_Soon-blue)

---

### 🔗 Quick Links

- [MCP Documentation](https://modelcontextprotocol.io)
- [Polymarket API Docs](https://docs.polymarket.com)
- [Predyx Platform](https://predyx.com)
- [Lightning Network](https://lightning.network)
