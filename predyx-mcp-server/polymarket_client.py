#!/usr/bin/env python3
"""
Polymarket API Client

Real-time data fetching from Polymarket API.
Documentation: https://docs.polymarket.com/llms.txt

Usage:
    from polymarket_client import PolymarketClient
    
    client = PolymarketClient()
    markets = await client.get_active_markets(limit=10)
    market = await client.get_market_details("531202")
"""

import json
from datetime import datetime
from typing import Any

import httpx


class PolymarketClient:
    """Client for fetching data from Polymarket API"""
    
    GAMMA_API = "https://gamma-api.polymarket.com"
    CLOB_API = "https://clob.polymarket.com"
    
    def __init__(self, timeout: float = 10.0):
        self.client = httpx.AsyncClient(timeout=timeout)
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
    
    # ========================================================================
    # MARKET DATA
    # ========================================================================
    
    async def get_active_markets(
        self,
        limit: int = 20,
        offset: int = 0,
        tag: str | None = None,
    ) -> list[dict[str, Any]]:
        """Get list of active markets
        
        Args:
            limit: Number of markets to fetch (max 100)
            offset: Pagination offset
            tag: Filter by tag (e.g., "Crypto", "Politics")
            
        Returns:
            List of market dictionaries
        """
        params = {
            "active": "true",
            "closed": "false",
            "limit": min(limit, 100),
            "offset": offset,
        }
        
        if tag:
            params["tag"] = tag
        
        response = await self.client.get(
            f"{self.GAMMA_API}/markets",
            params=params,
        )
        response.raise_for_status()
        
        return response.json()
    
    async def get_market_details(self, market_id: str) -> dict[str, Any]:
        """Get detailed information about a specific market
        
        Args:
            market_id: Market ID (e.g., "531202")
            
        Returns:
            Market dictionary with full details
        """
        response = await self.client.get(
            f"{self.GAMMA_API}/markets/{market_id}",
        )
        response.raise_for_status()
        
        return response.json()
    
    async def get_trending_markets(
        self,
        limit: int = 10,
        sort_by: str = "volume24hr",
    ) -> list[dict[str, Any]]:
        """Get trending markets sorted by volume or activity
        
        Args:
            limit: Number of markets to fetch
            sort_by: Sort field (volume24hr, volume1wk, liquidity)
            
        Returns:
            List of trending market dictionaries
        """
        markets = await self.get_active_markets(limit=100)
        
        # Sort by specified field (descending)
        sorted_markets = sorted(
            markets,
            key=lambda m: float(m.get(sort_by, 0) or 0),
            reverse=True,
        )
        
        return sorted_markets[:limit]
    
    async def get_market_categories(self) -> list[str]:
        """Get list of all market categories/tags
        
        Returns:
            List of category names
        """
        markets = await self.get_active_markets(limit=100)
        
        # Extract unique tags
        tags = set()
        for market in markets:
            if "tags" in market:
                # Tags might be a list or JSON string
                market_tags = market["tags"]
                if isinstance(market_tags, str):
                    try:
                        market_tags = json.loads(market_tags)
                    except json.JSONDecodeError:
                        continue
                
                if isinstance(market_tags, list):
                    tags.update(market_tags)
        
        return sorted(list(tags))
    
    async def get_market_price_history(
        self,
        market_id: str,
        interval: str = "1d",
        start_ts: int | None = None,
        end_ts: int | None = None,
    ) -> list[dict[str, Any]]:
        """Get historical price data for a market
        
        Args:
            market_id: Market ID
            interval: Time interval (1h, 1d, 1w)
            start_ts: Start timestamp (Unix)
            end_ts: End timestamp (Unix)
            
        Returns:
            List of price points
        """
        params = {"interval": interval}
        
        if start_ts:
            params["start_ts"] = start_ts
        if end_ts:
            params["end_ts"] = end_ts
        
        response = await self.client.get(
            f"{self.GAMMA_API}/markets/{market_id}/prices-history",
            params=params,
        )
        response.raise_for_status()
        
        return response.json()
    
    # ========================================================================
    # DATA TRANSFORMATION
    # ========================================================================
    
    @staticmethod
    def parse_outcome_prices(outcome_prices: str | list) -> tuple[float, float]:
        """Parse outcome prices from JSON string or list
        
        Args:
            outcome_prices: JSON string or list (e.g., '["0.65", "0.35"]')
            
        Returns:
            Tuple of (yes_price, no_price)
        """
        if isinstance(outcome_prices, str):
            try:
                prices = json.loads(outcome_prices)
            except json.JSONDecodeError:
                return 0.5, 0.5
        else:
            prices = outcome_prices
        
        if len(prices) >= 2:
            return float(prices[0]), float(prices[1])
        
        return 0.5, 0.5
    
    @staticmethod
    def parse_tags(tags: str | list | None) -> list[str]:
        """Parse tags from JSON string or list
        
        Args:
            tags: JSON string, list, or None
            
        Returns:
            List of tag strings
        """
        if not tags:
            return []
        
        if isinstance(tags, str):
            try:
                return json.loads(tags)
            except json.JSONDecodeError:
                return []
        
        return list(tags)
    
    @staticmethod
    def to_market_dict(market_data: dict[str, Any]) -> dict[str, Any]:
        """Transform Polymarket API response to our Market format
        
        Args:
            market_data: Raw market data from API
            
        Returns:
            Transformed market dictionary
        """
        yes_price, no_price = PolymarketClient.parse_outcome_prices(
            market_data.get("outcomePrices", ["0.5", "0.5"])
        )
        
        tags = PolymarketClient.parse_tags(market_data.get("tags"))
        category = tags[0] if tags else "General"
        
        return {
            "market_id": market_data["id"],
            "question": market_data["question"],
            "category": category,
            "current_price": yes_price,
            "yes_price": yes_price,
            "no_price": no_price,
            "volume_24h": float(market_data.get("volume24hr", 0) or 0),
            "total_volume": float(market_data.get("volume", 0) or 0),
            "liquidity": float(market_data.get("liquidity", 0) or 0),
            "created_at": market_data.get("createdAt", ""),
            "end_date": market_data.get("endDate", ""),
            "description": market_data.get("description", ""),
            "active": market_data.get("active", True),
            "closed": market_data.get("closed", False),
            "tags": tags,
            "url": f"https://polymarket.com/event/{market_data.get('slug', '')}",
        }
    
    # ========================================================================
    # ANALYSIS HELPERS
    # ========================================================================
    
    async def calculate_market_stats(self, market_id: str) -> dict[str, Any]:
        """Calculate market statistics
        
        Args:
            market_id: Market ID
            
        Returns:
            Statistics dictionary
        """
        market = await self.get_market_details(market_id)
        history = await self.get_market_price_history(market_id, interval="1d")
        
        yes_price, no_price = self.parse_outcome_prices(
            market.get("outcomePrices", ["0.5", "0.5"])
        )
        
        # Calculate price change
        price_change_24h = 0.0
        if history and len(history) > 1:
            old_price = float(history[0].get("price", yes_price))
            new_price = yes_price
            if old_price > 0:
                price_change_24h = ((new_price - old_price) / old_price) * 100
        
        return {
            "market_id": market_id,
            "current_price": yes_price,
            "price_change_24h": price_change_24h,
            "volume_24h": float(market.get("volume24hr", 0) or 0),
            "liquidity": float(market.get("liquidity", 0) or 0),
            "num_traders": len(market.get("events", [])),
        }


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

async def get_markets_for_mcp(limit: int = 20) -> list[dict[str, Any]]:
    """Fetch markets and transform for MCP Server
    
    This is a convenience function for direct use in predyx_mcp_server.py
    
    Args:
        limit: Number of markets to fetch
        
    Returns:
        List of transformed market dictionaries
    """
    async with PolymarketClient() as client:
        raw_markets = await client.get_active_markets(limit=limit)
        return [PolymarketClient.to_market_dict(m) for m in raw_markets]


async def get_market_details_for_mcp(market_id: str) -> dict[str, Any]:
    """Fetch market details and transform for MCP Server
    
    Args:
        market_id: Market ID
        
    Returns:
        Transformed market dictionary
    """
    async with PolymarketClient() as client:
        raw_market = await client.get_market_details(market_id)
        return PolymarketClient.to_market_dict(raw_market)


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    import asyncio
    
    async def test():
        print("🧪 Testing Polymarket API Client...")
        
        async with PolymarketClient() as client:
            # Test 1: Get active markets
            print("\n📊 Fetching active markets...")
            markets = await client.get_active_markets(limit=5)
            print(f"✅ Found {len(markets)} markets")
            
            for i, market in enumerate(markets[:3], 1):
                print(f"\n{i}. {market['question']}")
                print(f"   ID: {market['id']}")
                print(f"   Volume 24h: ${market.get('volume24hr', 0):,.2f}")
            
            # Test 2: Get trending markets
            print("\n🔥 Fetching trending markets...")
            trending = await client.get_trending_markets(limit=3)
            print(f"✅ Top 3 by 24h volume:")
            
            for i, market in enumerate(trending, 1):
                yes_price, no_price = client.parse_outcome_prices(
                    market.get("outcomePrices", ["0.5", "0.5"])
                )
                print(f"\n{i}. {market['question']}")
                print(f"   Yes: {yes_price:.2%} | No: {no_price:.2%}")
                print(f"   Volume: ${market.get('volume24hr', 0):,.2f}")
            
            # Test 3: Get market details
            if markets:
                market_id = markets[0]["id"]
                print(f"\n🔍 Fetching details for market {market_id}...")
                details = await client.get_market_details(market_id)
                transformed = client.to_market_dict(details)
                
                print(f"✅ Question: {transformed['question']}")
                print(f"   Category: {transformed['category']}")
                print(f"   Yes Price: {transformed['yes_price']:.2%}")
                print(f"   Total Volume: ${transformed['total_volume']:,.2f}")
            
            # Test 4: Get categories
            print("\n📁 Fetching categories...")
            categories = await client.get_market_categories()
            print(f"✅ Found {len(categories)} categories:")
            print(f"   {', '.join(categories[:10])}")
        
        print("\n✅ All tests passed!")
    
    asyncio.run(test())
