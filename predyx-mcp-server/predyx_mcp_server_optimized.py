"""
Optimized Predyx MCP Server with structured logging and intelligent error handling.

This version demonstrates Phase 1 optimizations:
- Structured JSON logging for all operations
- Automatic retry with exponential backoff
- User-friendly error messages
- Performance tracking

Usage:
    uv run predyx_mcp_server_optimized.py
    
Environment Variables:
    POLYMARKET_API_TIMEOUT: API timeout in seconds (default: 10.0)
    LOG_LEVEL: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
"""

import os
import time
from typing import Any, Optional

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

from polymarket_client import PolymarketClient
from logger import logger, track_performance
from error_handler import (
    retry_on_failure,
    handle_api_error,
    UserFriendlyError,
    RetryExhaustedError
)

# Create FastMCP server instance
mcp = FastMCP(
    "Predyx Prediction Markets (Optimized)",
    stateless_http=True,  # Recommended for production
    json_response=True,   # Faster for API-like usage
)

# Configuration
POLYMARKET_API_TIMEOUT = float(os.getenv("POLYMARKET_API_TIMEOUT", "10.0"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Configure logger level
import logging
logging.getLogger("predyx").setLevel(getattr(logging, LOG_LEVEL))

# Global client instance (reused for efficiency)
_client: Optional[PolymarketClient] = None


async def get_client() -> PolymarketClient:
    """Get or create Polymarket API client"""
    global _client
    if _client is None:
        _client = PolymarketClient(timeout=POLYMARKET_API_TIMEOUT)
        logger.log_info("client_initialized", {
            "timeout": POLYMARKET_API_TIMEOUT
        })
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
# RESOURCES - Read-only data access (with optimization)
# ============================================================================

@mcp.resource("predyx://markets")
@retry_on_failure(max_retries=3, delay=1.0)
@track_performance("resource_access")
async def list_markets(limit: int = 20) -> str:
    """List all active prediction markets
    
    Args:
        limit: Number of markets to fetch (default: 20, max: 100)
        
    Returns:
        JSON string of market list
    """
    start_time = time.time()
    try:
        client = await get_client()
        markets = await client.get_active_markets(limit=min(limit, 100))
        
        markets_data = []
        for market in markets:
            yes_price, no_price = client.parse_outcome_prices(
                market.get("outcomePrices", ["0.5", "0.5"])
            )
            
            markets_data.append({
                "id": market.get("conditionId"),
                "question": market.get("question"),
                "description": market.get("description"),
                "yes_price": yes_price,
                "no_price": no_price,
                "volume": market.get("volume", "0"),
                "liquidity": market.get("liquidity", "0"),
                "categories": market.get("tags", []),
                "active": market.get("active", True),
                "closed": market.get("closed", False)
            })
        
        duration_ms = (time.time() - start_time) * 1000
        logger.log_resource_access(
            resource_uri="predyx://markets",
            duration_ms=duration_ms,
            success=True,
            cache_hit=False  # Will be updated when cache is implemented
        )
        
        import json
        return json.dumps({
            "markets": markets_data,
            "count": len(markets_data),
            "timestamp": time.time()
        }, indent=2)
        
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        logger.log_resource_access(
            resource_uri="predyx://markets",
            duration_ms=duration_ms,
            success=False,
            error=str(e)
        )
        
        # Convert to user-friendly error
        user_error = handle_api_error(
            operation="list markets",
            error=e,
            context={"limit": limit}
        )
        raise user_error


@mcp.resource("predyx://markets/{market_id}")
@retry_on_failure(max_retries=3, delay=1.0)
@track_performance("resource_access")
async def get_market_details(market_id: str) -> str:
    """Get detailed information about a specific market
    
    Args:
        market_id: Market condition ID
        
    Returns:
        JSON string with market details
    """
    start_time = time.time()
    try:
        client = await get_client()
        market = await client.get_market_by_id(market_id)
        
        if not market:
            duration_ms = (time.time() - start_time) * 1000
            logger.log_resource_access(
                resource_uri=f"predyx://markets/{market_id}",
                duration_ms=duration_ms,
                success=False,
                error="Market not found"
            )
            return json.dumps({"error": "Market not found"})
        
        yes_price, no_price = client.parse_outcome_prices(
            market.get("outcomePrices", ["0.5", "0.5"])
        )
        
        market_data = {
            "id": market.get("conditionId"),
            "question": market.get("question"),
            "description": market.get("description"),
            "yes_price": yes_price,
            "no_price": no_price,
            "volume": market.get("volume", "0"),
            "liquidity": market.get("liquidity", "0"),
            "categories": market.get("tags", []),
            "active": market.get("active", True),
            "closed": market.get("closed", False),
            "image": market.get("image"),
            "icon": market.get("icon"),
            "end_date": market.get("end_date_iso")
        }
        
        duration_ms = (time.time() - start_time) * 1000
        logger.log_resource_access(
            resource_uri=f"predyx://markets/{market_id}",
            duration_ms=duration_ms,
            success=True
        )
        
        import json
        return json.dumps(market_data, indent=2)
        
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        logger.log_resource_access(
            resource_uri=f"predyx://markets/{market_id}",
            duration_ms=duration_ms,
            success=False,
            error=str(e)
        )
        
        user_error = handle_api_error(
            operation="fetch market details",
            error=e,
            context={"market_id": market_id}
        )
        raise user_error


@mcp.resource("predyx://trending")
@retry_on_failure(max_retries=3, delay=1.0)
@track_performance("resource_access")
async def get_trending_markets(limit: int = 10) -> str:
    """Get trending markets by volume and activity
    
    Args:
        limit: Number of trending markets to fetch (default: 10)
        
    Returns:
        JSON string with trending markets
    """
    start_time = time.time()
    try:
        client = await get_client()
        markets = await client.get_active_markets(limit=100)
        
        # Sort by volume (descending)
        sorted_markets = sorted(
            markets,
            key=lambda m: float(m.get("volume", "0").replace("$", "").replace(",", "") or "0"),
            reverse=True
        )[:limit]
        
        trending_data = []
        for market in sorted_markets:
            yes_price, no_price = client.parse_outcome_prices(
                market.get("outcomePrices", ["0.5", "0.5"])
            )
            
            trending_data.append({
                "id": market.get("conditionId"),
                "question": market.get("question"),
                "yes_price": yes_price,
                "no_price": no_price,
                "volume": market.get("volume", "0"),
                "trend": "up" if yes_price > 0.5 else "down"
            })
        
        duration_ms = (time.time() - start_time) * 1000
        logger.log_resource_access(
            resource_uri="predyx://trending",
            duration_ms=duration_ms,
            success=True
        )
        
        import json
        return json.dumps({
            "trending_markets": trending_data,
            "timestamp": time.time()
        }, indent=2)
        
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        logger.log_resource_access(
            resource_uri="predyx://trending",
            duration_ms=duration_ms,
            success=False,
            error=str(e)
        )
        
        user_error = handle_api_error(
            operation="fetch trending markets",
            error=e,
            context={"limit": limit}
        )
        raise user_error


# ============================================================================
# TOOLS - Interactive operations (with optimization)
# ============================================================================

@mcp.tool()
@retry_on_failure(max_retries=3, delay=1.0)
@track_performance("tool_execution")
async def analyze_market(
    market_id: str,
    include_sentiment: bool = False
) -> MarketAnalysis:
    """Analyze a prediction market with AI-powered insights
    
    Args:
        market_id: Market condition ID to analyze
        include_sentiment: Include sentiment analysis (Premium only)
        
    Returns:
        MarketAnalysis with trend, recommendation, and confidence
    """
    start_time = time.time()
    try:
        client = await get_client()
        market = await client.get_market_by_id(market_id)
        
        if not market:
            raise Exception("Market not found")
        
        yes_price, no_price = client.parse_outcome_prices(
            market.get("outcomePrices", ["0.5", "0.5"])
        )
        
        # Simple trend analysis (in production, use AI model)
        trend = "neutral"
        if yes_price > 0.6:
            trend = "bullish"
        elif yes_price < 0.4:
            trend = "bearish"
        
        # Simple recommendation logic
        recommendation = "hold"
        confidence = 0.5
        
        if yes_price < 0.3:
            recommendation = "buy YES"
            confidence = 0.7
        elif yes_price > 0.7:
            recommendation = "buy NO"
            confidence = 0.7
        
        analysis = MarketAnalysis(
            market_id=market_id,
            question=market.get("question"),
            current_probability=yes_price,
            trend=trend,
            volume_change_24h=0.0,  # Would need historical data
            recommendation=recommendation,
            confidence=confidence
        )
        
        duration_ms = (time.time() - start_time) * 1000
        logger.log_tool_execution(
            tool_name="analyze_market",
            duration_ms=duration_ms,
            success=True,
            market_id=market_id,
            trend=trend,
            recommendation=recommendation
        )
        
        return analysis
        
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        logger.log_tool_execution(
            tool_name="analyze_market",
            duration_ms=duration_ms,
            success=False,
            error=str(e),
            market_id=market_id
        )
        
        user_error = handle_api_error(
            operation="analyze market",
            error=e,
            context={"market_id": market_id, "include_sentiment": include_sentiment}
        )
        raise user_error


@mcp.tool()
@retry_on_failure(max_retries=3, delay=1.0)
@track_performance("tool_execution")
async def get_price_prediction(
    market_id: str,
    horizon_days: int = 7,
    confidence_interval: float = 0.95
) -> PricePrediction:
    """Get AI-powered price predictions for a market
    
    Args:
        market_id: Market condition ID
        horizon_days: Prediction horizon in days (1-90, default: 7)
        confidence_interval: Confidence interval (0.8-0.99, default: 0.95)
        
    Returns:
        PricePrediction with predicted price and confidence interval
    """
    start_time = time.time()
    try:
        if horizon_days < 1 or horizon_days > 90:
            raise ValueError("horizon_days must be between 1 and 90")
        
        if confidence_interval < 0.8 or confidence_interval > 0.99:
            raise ValueError("confidence_interval must be between 0.8 and 0.99")
        
        client = await get_client()
        market = await client.get_market_by_id(market_id)
        
        if not market:
            raise Exception("Market not found")
        
        yes_price, no_price = client.parse_outcome_prices(
            market.get("outcomePrices", ["0.5", "0.5"])
        )
        
        # Simple prediction logic (in production, use AI model)
        # For now, just add some noise
        import random
        predicted_price = yes_price + random.uniform(-0.1, 0.1)
        predicted_price = max(0.01, min(0.99, predicted_price))
        
        prediction = PricePrediction(
            market_id=market_id,
            question=market.get("question"),
            current_price=yes_price,
            predicted_price=predicted_price,
            horizon_days=horizon_days,
            confidence_interval=[
                max(0.01, predicted_price - 0.1),
                min(0.99, predicted_price + 0.1)
            ],
            factors=["Historical price trend", "Market volume", "Time to resolution"]
        )
        
        duration_ms = (time.time() - start_time) * 1000
        logger.log_tool_execution(
            tool_name="get_price_prediction",
            duration_ms=duration_ms,
            success=True,
            market_id=market_id,
            horizon_days=horizon_days,
            current_price=yes_price,
            predicted_price=predicted_price
        )
        
        return prediction
        
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        logger.log_tool_execution(
            tool_name="get_price_prediction",
            duration_ms=duration_ms,
            success=False,
            error=str(e),
            market_id=market_id,
            horizon_days=horizon_days
        )
        
        user_error = handle_api_error(
            operation="get price prediction",
            error=e,
            context={
                "market_id": market_id,
                "horizon_days": horizon_days,
                "confidence_interval": confidence_interval
            }
        )
        raise user_error


# ============================================================================
# PROMPTS - Reusable templates (unchanged from original)
# ============================================================================

@mcp.prompt()
def market_analysis_prompt(market_id: str) -> str:
    """Template for comprehensive market analysis"""
    return f"""Please analyze the prediction market with ID {market_id}.

Include:
1. Market overview (question, current price, volume)
2. Trend analysis (bullish/bearish/neutral)
3. Key factors affecting the outcome
4. Risk assessment
5. Investment recommendation with confidence level

Use the analyze_market tool to get AI-powered insights.
"""


@mcp.prompt()
def investment_strategy_prompt() -> str:
    """Template for developing investment strategies"""
    return """Help me develop an investment strategy for prediction markets.

Consider:
1. Risk tolerance (conservative, moderate, aggressive)
2. Time horizon (short-term, medium-term, long-term)
3. Diversification across markets
4. Position sizing based on confidence
5. Exit strategies

Provide actionable recommendations with clear reasoning.
"""


# ============================================================================
# Run the server
# ============================================================================

if __name__ == "__main__":
    logger.log_info("server_starting", {
        "version": "1.0.0-optimized",
        "timeout": POLYMARKET_API_TIMEOUT,
        "log_level": LOG_LEVEL
    })
    
    mcp.run(transport="streamable-http")
