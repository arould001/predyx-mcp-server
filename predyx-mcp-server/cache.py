"""
Smart caching layer for Predyx MCP Server.

Features:
- In-memory LRU cache with TTL (Time To Live)
- Automatic cache invalidation
- Cache hit/miss tracking
- Async-friendly
"""

import asyncio
import time
from functools import wraps
from typing import Any, Callable, Optional, Dict, Tuple
from collections import OrderedDict
import threading
from logger import logger


class CacheEntry:
    """A single cache entry with TTL."""
    
    def __init__(self, value: Any, ttl_seconds: float):
        self.value = value
        self.expires_at = time.time() + ttl_seconds
    
    def is_expired(self) -> bool:
        """Check if this entry has expired."""
        return time.time() > self.expires_at


class SmartCache:
    """
    Thread-safe LRU cache with TTL support.
    
    Features:
    - LRU eviction when cache is full
    - TTL-based expiration
    - Cache statistics tracking
    - Async-friendly
    """
    
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self._cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self._lock = threading.Lock()
        
        # Statistics
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        self.expirations = 0
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from the cache.
        
        Args:
            key: Cache key
        
        Returns:
            Cached value or None if not found/expired
        """
        with self._lock:
            if key not in self._cache:
                self.misses += 1
                logger.log_debug("cache_miss", {"key": key})
                return None
            
            entry = self._cache[key]
            
            # Check if expired
            if entry.is_expired():
                del self._cache[key]
                self.expirations += 1
                self.misses += 1
                logger.log_debug("cache_expired", {"key": key})
                return None
            
            # Move to end (most recently used)
            self._cache.move_to_end(key)
            self.hits += 1
            
            logger.log_debug("cache_hit", {"key": key})
            return entry.value
    
    def set(self, key: str, value: Any, ttl_seconds: float = 300.0) -> None:
        """
        Set a value in the cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl_seconds: Time to live in seconds (default: 5 minutes)
        """
        with self._lock:
            # If key exists, remove it first (to update position)
            if key in self._cache:
                del self._cache[key]
            
            # Evict oldest entries if cache is full
            while len(self._cache) >= self.max_size:
                oldest_key = next(iter(self._cache))
                del self._cache[oldest_key]
                self.evictions += 1
                logger.log_debug("cache_eviction", {"key": oldest_key})
            
            # Add new entry
            self._cache[key] = CacheEntry(value, ttl_seconds)
            
            logger.log_debug("cache_set", {"key": key, "ttl": ttl_seconds})
    
    def delete(self, key: str) -> bool:
        """
        Delete a value from the cache.
        
        Args:
            key: Cache key
        
        Returns:
            True if deleted, False if not found
        """
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                logger.log_debug("cache_delete", {"key": key})
                return True
            return False
    
    def clear(self) -> None:
        """Clear all cache entries."""
        with self._lock:
            self._cache.clear()
            logger.log_info("cache_clear", {"entries_cleared": len(self._cache)})
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache stats
        """
        with self._lock:
            total_requests = self.hits + self.misses
            hit_rate = (self.hits / total_requests * 100) if total_requests > 0 else 0.0
            
            return {
                "size": len(self._cache),
                "max_size": self.max_size,
                "hits": self.hits,
                "misses": self.misses,
                "evictions": self.evictions,
                "expirations": self.expirations,
                "hit_rate": round(hit_rate, 2)
            }
    
    def cleanup_expired(self) -> int:
        """
        Remove all expired entries.
        
        Returns:
            Number of entries removed
        """
        with self._lock:
            expired_keys = [
                key for key, entry in self._cache.items()
                if entry.is_expired()
            ]
            
            for key in expired_keys:
                del self._cache[key]
                self.expirations += 1
            
            if expired_keys:
                logger.log_info("cache_cleanup", {"expired_count": len(expired_keys)})
            
            return len(expired_keys)


# Global cache instance
cache = SmartCache(max_size=1000)


def cached(
    ttl_seconds: float = 300.0,
    key_prefix: str = ""
):
    """
    Decorator for caching function results.
    
    Args:
        ttl_seconds: Time to live in seconds (default: 5 minutes)
        key_prefix: Optional prefix for cache keys
    
    Usage:
        @cached(ttl_seconds=60.0, key_prefix="market")
        async def get_market_data(market_id: str):
            # Expensive API call
            pass
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            # Generate cache key
            cache_key = f"{key_prefix}:{func.__name__}:{args}:{kwargs}"
            
            # Try to get from cache
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                logger.log_info("cache_hit_decorator", {
                    "function": func.__name__,
                    "key": cache_key
                })
                return cached_value
            
            # Call the function
            result = await func(*args, **kwargs)
            
            # Cache the result
            cache.set(cache_key, result, ttl_seconds)
            
            logger.log_info("cache_set_decorator", {
                "function": func.__name__,
                "key": cache_key,
                "ttl": ttl_seconds
            })
            
            return result
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs) -> Any:
            # Generate cache key
            cache_key = f"{key_prefix}:{func.__name__}:{args}:{kwargs}"
            
            # Try to get from cache
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                logger.log_info("cache_hit_decorator", {
                    "function": func.__name__,
                    "key": cache_key
                })
                return cached_value
            
            # Call the function
            result = func(*args, **kwargs)
            
            # Cache the result
            cache.set(cache_key, result, ttl_seconds)
            
            logger.log_info("cache_set_decorator", {
                "function": func.__name__,
                "key": cache_key,
                "ttl": ttl_seconds
            })
            
            return result
        
        # Return appropriate wrapper based on function type
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


# Example usage
if __name__ == "__main__":
    import aiohttp
    
    @cached(ttl_seconds=60.0, key_prefix="polymarket")
    async def fetch_markets() -> list:
        """Fetch markets from Polymarket API (cached for 60 seconds)."""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://gamma-api.polymarket.com/markets") as response:
                return await response.json()
    
    async def test():
        # First call (cache miss)
        print("First call...")
        markets1 = await fetch_markets()
        print(f"Fetched {len(markets1)} markets")
        
        # Second call (cache hit)
        print("\nSecond call (should be instant)...")
        markets2 = await fetch_markets()
        print(f"Fetched {len(markets2)} markets")
        
        # Check cache stats
        stats = cache.get_stats()
        print(f"\nCache stats: {stats}")
    
    # Run test
    asyncio.run(test())
