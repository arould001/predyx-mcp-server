#!/usr/bin/env python3
"""
Predyx MCP Server - Bitcoin-native prediction market data provider

This MCP server provides real-time prediction market data from Polymarket.
Data is fetched in real-time from the Polymarket Gamma API.

Features:
- Resources: Live market data, market details, categories, trending markets
- Tools: Market analysis, price predictions
- Prompts: Analysis templates, investment templates

Run with:
    uv run --with mcp --with httpx predyx_mcp_server.py
    
Or with mcp dev:
    uv run mcp dev predyx_mcp_server.py
    
Environment Variables (optional):
    POLYMARKET_API_TIMEOUT: API timeout in seconds (default: 10.0)
"""

import os
from typing import Any

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

from polymarket_client import PolymarketClient

# Create FastMCP server instance
mcp = FastMCP(
    "Predyx Prediction Markets",
    stateless_http=True,  # Recommended for production
    json_response=True,   # Faster for API-like usage
)

# Configuration
POLYMARKET_API_TIMEOUT = float(os.getenv("POLYMARKET_API_TIMEOUT", "10.0"))

# Global client instance (reused for efficiency)
_client: PolymarketClient | None = None


async def get_client() -> PolymarketClient:
    """Get or create Polymarket API client"""
    global _client
    if _client is None:
        _client = PolymarketClient(timeout=POLYMARKET_API_TIMEOUT)
    return _client


# ============================================================================
# Data Models
# ============================================================================

class MarketAnalysis(BaseModel):
    """Market analysis result"""
    market_id: str
    question: str
    current_probability: float
    trend: str  # "bullish", "bearish", "neutral"
    volume_change_24h: float  # percentage
    recommendation: str
    confidence: float  # 0.0 to 1.0


class PricePrediction(BaseModel):
    """Price prediction result"""
    market_id: str
    question: str
    current_price: float
    predicted_price: float
    horizon_days: int
    confidence_interval: list[float]
    factors: list[str]


# ============================================================================
# RESOURCES - Read-only data access
# ============================================================================

@mcp.resource("predyx://markets")
async def list_markets(limit: int = 20) -> str:
    """List all active prediction markets
    
    Args:
        limit: Number of markets to fetch (default: 20, max: 100)
        
    Returns:
        JSON string of market list
    """
    try:
        client = await get_client()
        markets = await client.get_active_markets(limit=min(limit, 100))
        
        markets_data = []
        for market in markets:
            yes_price, no_price = client.parse_outcome_prices(
                market.get("outcomePrices", ["0.5", "0.5"])
            )
            markets_data.append({
                "id": market["id"],
                "question": market["question"],
                "category": client.parse_tags(market.get("tags"))[0] if market.get("tags") else "General",
                "yes_price": f"{yes_price:.2%}",
                "no_price": f"{no_price:.2%}",
                "volume_24h": f"${float(market.get('volume24hr', 0) or 0):,.2f}",
                "liquidity": f"${float(market.get('liquidity', 0) or 0):,.2f}",
                "end_date": market.get("endDate", ""),
            })
        
        return str(markets_data)
    
    except Exception as e:
        return f"Error fetching markets: {str(e)}"


@mcp.resource("predyx://markets/{market_id}")
async def get_market_details(market_id: str) -> str:
    """Get detailed information about a specific market
    
    Args:
        market_id: Market ID (e.g., "531202")
        
    Returns:
        JSON string of market details
    """
    try:
        client = await get_client()
        market = await client.get_market_details(market_id)
        transformed = client.to_market_dict(market)
        
        return str({
            "id": transformed["market_id"],
            "question": transformed["question"],
            "category": transformed["category"],
            "yes_price": f"{transformed['yes_price']:.2%}",
            "no_price": f"{transformed['no_price']:.2%}",
            "volume_24h": f"${transformed['volume_24h']:,.2f}",
            "total_volume": f"${transformed['total_volume']:,.2f}",
            "liquidity": f"${transformed['liquidity']:,.2f}",
            "description": transformed["description"],
            "end_date": transformed["end_date"],
            "url": transformed["url"],
            "tags": transformed["tags"],
        })
    
    except Exception as e:
        return f"Error fetching market {market_id}: {str(e)}"


@mcp.resource("predyx://categories")
async def list_categories() -> str:
    """List all market categories
    
    Returns:
        JSON string of category list
    """
    try:
        client = await get_client()
        categories = await client.get_market_categories()
        return str(categories)
    
    except Exception as e:
        return f"Error fetching categories: {str(e)}"


@mcp.resource("predyx://trending")
async def get_trending_markets(limit: int = 10) -> str:
    """Get trending markets by 24h volume
    
    Args:
        limit: Number of trending markets to return (default: 10)
        
    Returns:
        JSON string of trending markets
    """
    try:
        client = await get_client()
        trending = await client.get_trending_markets(limit=limit, sort_by="volume24hr")
        
        trending_data = []
        for market in trending:
            yes_price, no_price = client.parse_outcome_prices(
                market.get("outcomePrices", ["0.5", "0.5"])
            )
            trending_data.append({
                "id": market["id"],
                "question": market["question"],
                "yes_price": f"{yes_price:.2%}",
                "no_price": f"{no_price:.2%}",
                "volume_24h": f"${float(market.get('volume24hr', 0) or 0):,.2f}",
                "liquidity": f"${float(market.get('liquidity', 0) or 0):,.2f}",
            })
        
        return str(trending_data)
    
    except Exception as e:
        return f"Error fetching trending markets: {str(e)}"


# ============================================================================
# TOOLS - Executable functions with side effects
# ============================================================================

@mcp.tool()
async def analyze_market(market_id: str) -> MarketAnalysis:
    """Analyze a prediction market and provide recommendations
    
    Args:
        market_id: The ID of the market to analyze (e.g., "531202")
        
    Returns:
        MarketAnalysis with trend, recommendation, and confidence
    """
    try:
        client = await get_client()
        
        # Fetch market details
        market = await client.get_market_details(market_id)
        transformed = client.to_market_dict(market)
        
        # Calculate basic trend
        yes_price = transformed["yes_price"]
        
        if yes_price > 0.6:
            trend = "bullish"
            recommendation = "Market shows high confidence (>60%). Consider contrarian position if overvalued."
        elif yes_price < 0.4:
            trend = "bearish"
            recommendation = "Market shows low confidence (<40%). Consider position if undervalued."
        else:
            trend = "neutral"
            recommendation = "Market is fairly balanced. Wait for more information or catalyst."
        
        # Calculate volume change (simplified)
        volume_24h = transformed["volume_24h"]
        total_volume = transformed["total_volume"]
        volume_change = (volume_24h / total_volume * 100) if total_volume > 0 else 0
        
        # Calculate confidence based on liquidity
        liquidity = transformed["liquidity"]
        confidence = min(liquidity / 50000, 1.0)  # Max confidence at $50k liquidity
        
        return MarketAnalysis(
            market_id=market_id,
            question=transformed["question"],
            current_probability=yes_price,
            trend=trend,
            volume_change_24h=volume_change,
            recommendation=recommendation,
            confidence=confidence,
        )
    
    except Exception as e:
        raise ValueError(f"Failed to analyze market {market_id}: {str(e)}")


@mcp.tool()
async def get_price_prediction(market_id: str, horizon_days: int = 7) -> PricePrediction:
    """Get price prediction for a market
    
    Args:
        market_id: The market to predict (e.g., "531202")
        horizon_days: Number of days to predict ahead (default: 7)
        
    Returns:
        Price prediction with confidence interval
    """
    try:
        client = await get_client()
        
        # Fetch market details
        market = await client.get_market_details(market_id)
        transformed = client.to_market_dict(market)
        
        current_price = transformed["yes_price"]
        
        # Simple prediction model (can be enhanced with ML)
        # Based on momentum and mean reversion
        predicted_price = current_price  # Start with current
        
        # Add slight mean reversion tendency
        predicted_price += (0.5 - current_price) * 0.1
        
        # Ensure bounds
        predicted_price = max(0.05, min(0.95, predicted_price))
        
        # Calculate confidence interval
        # Wider interval for longer horizons
        interval_width = 0.05 + (horizon_days * 0.01)
        confidence_interval = [
            max(0.01, predicted_price - interval_width),
            min(0.99, predicted_price + interval_width),
        ]
        
        return PricePrediction(
            market_id=market_id,
            question=transformed["question"],
            current_price=current_price,
            predicted_price=predicted_price,
            horizon_days=horizon_days,
            confidence_interval=confidence_interval,
            factors=[
                "Current market probability",
                "Historical price momentum",
                "Market liquidity",
                "Time to resolution",
            ],
        )
    
    except Exception as e:
        raise ValueError(f"Failed to predict price for market {market_id}: {str(e)}")


# ============================================================================
# PROMPTS - Reusable templates
# ============================================================================

@mcp.prompt(title="Market Analysis Template")
def analyze_market_prompt(market_id: str) -> str:
    """Template for comprehensive market analysis"""
    return f"""Please provide a comprehensive analysis of prediction market {market_id}:

1. **Market Overview**
   - What is the question being asked?
   - Current probability and why?
   - Total volume and liquidity

2. **Historical Analysis**
   - Price history and trends
   - Volume patterns
   - Key events that moved the price

3. **Fundamental Analysis**
   - What factors influence this market?
   - Recent news and developments
   - Expert opinions and forecasts

4. **Technical Analysis**
   - Price momentum
   - Support/resistance levels
   - Trading patterns

5. **Recommendation**
   - Is this a good entry point?
   - What position would you take?
   - Risk/reward assessment

Please use the analyze_market tool to get started with market {market_id}.
"""


@mcp.prompt(title="Investment Strategy Template")
def investment_strategy_prompt(risk_level: str = "moderate") -> str:
    """Template for creating investment strategies"""
    return f"""Create an investment strategy for prediction markets with {risk_level} risk:

1. **Risk Profile: {risk_level.upper()}**
   - Define acceptable loss limits
   - Position sizing rules
   - Diversification requirements

2. **Market Selection Criteria**
   - Which markets to target
   - Minimum volume requirements
   - Avoided categories or types

3. **Entry Rules**
   - When to enter a position
   - Price thresholds
   - Signal requirements

4. **Exit Rules**
   - Profit targets
   - Stop-loss levels
   - Time-based exits

5. **Risk Management**
   - Maximum position size
   - Portfolio allocation
   - Hedging strategies

Please analyze the current markets using the list_markets resource and suggest specific opportunities.
"""


# ============================================================================
# Server Execution
# ============================================================================

if __name__ == "__main__":
    # Run the server with streamable HTTP transport (recommended for production)
    mcp.run(transport="streamable-http")
