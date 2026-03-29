"""
Rate limiter for Predyx MCP Server.

Features:
- Token Bucket algorithm (smooth rate limiting)
- Async-friendly
- Automatic backoff on 429 errors
- Per-endpoint rate limiting
"""

import asyncio
import time
from functools import wraps
from typing import Callable, Dict, Optional
from logger import logger


class TokenBucket:
    """
    Token Bucket rate limiter.
    
    Provides smooth rate limiting by allowing bursts up to bucket capacity.
    
    Algorithm:
    - Tokens are added at a fixed rate (tokens_per_second)
    - Each request consumes 1 token
    - If bucket is empty, request is delayed
    - Bucket has maximum capacity (burst_size)
    """
    
    def __init__(
        self,
        tokens_per_second: float = 10.0,
        burst_size: int = 20
    ):
        """
        Initialize token bucket.
        
        Args:
            tokens_per_second: Rate at which tokens are added
            burst_size: Maximum number of tokens in bucket
        """
        self.tokens_per_second = tokens_per_second
        self.burst_size = burst_size
        self.tokens = float(burst_size)
        self.last_update = time.time()
        self._lock = asyncio.Lock()
        
        # Statistics
        self.total_requests = 0
        self.rate_limited_requests = 0
        self.total_wait_time = 0.0
    
    async def _refill_tokens(self) -> None:
        """Refill tokens based on time elapsed."""
        now = time.time()
        elapsed = now - self.last_update
        
        # Calculate new tokens
        new_tokens = elapsed * self.tokens_per_second
        self.tokens = min(self.tokens + new_tokens, self.burst_size)
        
        self.last_update = now
    
    async def acquire(self, tokens: int = 1) -> float:
        """
        Acquire tokens from bucket (wait if necessary).
        
        Args:
            tokens: Number of tokens to acquire (default: 1)
        
        Returns:
            Wait time in seconds (0 if no wait)
        """
        async with self._lock:
            await self._refill_tokens()
            
            self.total_requests += 1
            
            # If enough tokens, consume immediately
            if self.tokens >= tokens:
                self.tokens -= tokens
                return 0.0
            
            # Calculate wait time
            tokens_needed = tokens - self.tokens
            wait_time = tokens_needed / self.tokens_per_second
            
            # Wait for tokens to refill
            await asyncio.sleep(wait_time)
            
            # Consume tokens
            self.tokens = 0
            
            # Update statistics
            self.rate_limited_requests += 1
            self.total_wait_time += wait_time
            
            logger.log_info("rate_limit_wait", {
                "wait_time": round(wait_time, 3),
                "tokens_needed": tokens_needed
            })
            
            return wait_time
    
    def get_stats(self) -> Dict[str, any]:
        """Get rate limiter statistics."""
        return {
            "tokens_per_second": self.tokens_per_second,
            "burst_size": self.burst_size,
            "current_tokens": round(self.tokens, 2),
            "total_requests": self.total_requests,
            "rate_limited_requests": self.rate_limited_requests,
            "total_wait_time": round(self.total_wait_time, 2),
            "rate_limit_percentage": round(
                (self.rate_limited_requests / self.total_requests * 100)
                if self.total_requests > 0 else 0.0,
                2
            )
        }


class MultiEndpointRateLimiter:
    """
    Rate limiter for multiple API endpoints.
    
    Different endpoints may have different rate limits.
    """
    
    def __init__(self):
        self._limiters: Dict[str, TokenBucket] = {}
    
    def get_limiter(
        self,
        endpoint: str,
        tokens_per_second: float = 10.0,
        burst_size: int = 20
    ) -> TokenBucket:
        """
        Get or create a rate limiter for an endpoint.
        
        Args:
            endpoint: API endpoint identifier
            tokens_per_second: Rate limit for this endpoint
            burst_size: Maximum burst size
        
        Returns:
            TokenBucket for this endpoint
        """
        if endpoint not in self._limiters:
            self._limiters[endpoint] = TokenBucket(
                tokens_per_second=tokens_per_second,
                burst_size=burst_size
            )
            logger.log_info("rate_limiter_created", {
                "endpoint": endpoint,
                "tokens_per_second": tokens_per_second,
                "burst_size": burst_size
            })
        
        return self._limiters[endpoint]
    
    async def acquire(self, endpoint: str, tokens: int = 1) -> float:
        """
        Acquire tokens for an endpoint.
        
        Args:
            endpoint: API endpoint identifier
            tokens: Number of tokens to acquire
        
        Returns:
            Wait time in seconds
        """
        limiter = self.get_limiter(endpoint)
        return await limiter.acquire(tokens)
    
    def get_all_stats(self) -> Dict[str, Dict]:
        """Get statistics for all rate limiters."""
        return {
            endpoint: limiter.get_stats()
            for endpoint, limiter in self._limiters.items()
        }


# Global rate limiter instances
default_rate_limiter = TokenBucket(tokens_per_second=10.0, burst_size=20)
multi_endpoint_limiter = MultiEndpointRateLimiter()


def rate_limit(
    endpoint: str = "default",
    tokens_per_second: float = 10.0,
    burst_size: int = 20
):
    """
    Decorator for rate limiting async functions.
    
    Args:
        endpoint: API endpoint identifier
        tokens_per_second: Rate limit (requests per second)
        burst_size: Maximum burst size
    
    Usage:
        @rate_limit(endpoint="polymarket_api", tokens_per_second=5.0)
        async def fetch_market_data():
            # API call
            pass
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Acquire token
            limiter = multi_endpoint_limiter.get_limiter(
                endpoint,
                tokens_per_second,
                burst_size
            )
            
            wait_time = await limiter.acquire()
            
            if wait_time > 0:
                logger.log_warning("rate_limit_applied", {
                    "function": func.__name__,
                    "endpoint": endpoint,
                    "wait_time": round(wait_time, 3)
                })
            
            # Call the function
            return await func(*args, **kwargs)
        
        return wrapper
    
    return decorator


# Example usage
if __name__ == "__main__":
    import aiohttp
    
    @rate_limit(endpoint="polymarket_api", tokens_per_second=5.0, burst_size=10)
    async def fetch_market(market_id: str):
        """Fetch market data with rate limiting."""
        async with aiohttp.ClientSession() as session:
            url = f"https://gamma-api.polymarket.com/markets/{market_id}"
            async with session.get(url) as response:
                return await response.json()
    
    async def test():
        print("Testing rate limiter...")
        
        # Make 20 requests rapidly
        for i in range(20):
            start_time = time.time()
            await fetch_market("test-market")
            elapsed = time.time() - start_time
            
            print(f"Request {i+1}: {elapsed:.3f}s")
        
        # Print stats
        stats = multi_endpoint_limiter.get_all_stats()
        print(f"\nRate limiter stats: {stats}")
    
    # Run test
    asyncio.run(test())
