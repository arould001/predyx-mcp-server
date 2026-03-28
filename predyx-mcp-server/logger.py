"""
Structured logging system for Predyx MCP Server.

Provides JSON-formatted logs for better parsing and analysis.
Tracks API calls, tool executions, and resource access.
"""

import json
import logging
import time
from datetime import datetime
from typing import Any, Dict, Optional
from functools import wraps


class StructuredLogger:
    """Structured logger with JSON output."""
    
    def __init__(self, name: str = "predyx"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Configure handler if not already configured
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter('%(message)s'))
            self.logger.addHandler(handler)
    
    def _log(self, level: str, event: str, data: Dict[str, Any]) -> None:
        """Log a structured event."""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": level,
            "event": event,
            "data": data
        }
        
        if level == "DEBUG":
            self.logger.debug(json.dumps(log_entry))
        elif level == "INFO":
            self.logger.info(json.dumps(log_entry))
        elif level == "WARNING":
            self.logger.warning(json.dumps(log_entry))
        elif level == "ERROR":
            self.logger.error(json.dumps(log_entry))
        elif level == "CRITICAL":
            self.logger.critical(json.dumps(log_entry))
    
    def log_api_call(
        self,
        endpoint: str,
        duration_ms: float,
        success: bool,
        error: Optional[str] = None
    ) -> None:
        """Log an API call with performance data."""
        data = {
            "endpoint": endpoint,
            "duration_ms": round(duration_ms, 2),
            "success": success
        }
        
        if error:
            data["error"] = error
        
        level = "ERROR" if not success else "INFO"
        self._log(level, "api_call", data)
    
    def log_tool_execution(
        self,
        tool_name: str,
        duration_ms: float,
        success: bool,
        error: Optional[str] = None,
        **kwargs
    ) -> None:
        """Log a tool execution with performance data."""
        data = {
            "tool_name": tool_name,
            "duration_ms": round(duration_ms, 2),
            "success": success,
            **kwargs
        }
        
        if error:
            data["error"] = error
        
        level = "ERROR" if not success else "INFO"
        self._log(level, "tool_execution", data)
    
    def log_resource_access(
        self,
        resource_uri: str,
        duration_ms: float,
        success: bool,
        cache_hit: Optional[bool] = None,
        error: Optional[str] = None
    ) -> None:
        """Log a resource access with performance data."""
        data = {
            "resource_uri": resource_uri,
            "duration_ms": round(duration_ms, 2),
            "success": success
        }
        
        if cache_hit is not None:
            data["cache_hit"] = cache_hit
        
        if error:
            data["error"] = error
        
        level = "ERROR" if not success else "INFO"
        self._log(level, "resource_access", data)
    
    def log_error(self, event: str, data: Dict[str, Any]) -> None:
        """Log an error event."""
        self._log("ERROR", event, data)
    
    def log_warning(self, event: str, data: Dict[str, Any]) -> None:
        """Log a warning event."""
        self._log("WARNING", event, data)
    
    def log_info(self, event: str, data: Dict[str, Any]) -> None:
        """Log an info event."""
        self._log("INFO", event, data)
    
    def log_debug(self, event: str, data: Dict[str, Any]) -> None:
        """Log a debug event."""
        self._log("DEBUG", event, data)


# Global logger instance
logger = StructuredLogger("predyx")


def track_performance(event_type: str = "function"):
    """
    Decorator to track function execution performance.
    
    Usage:
        @track_performance("tool_execution")
        async def my_tool():
            ...
    """
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                duration_ms = (time.time() - start_time) * 1000
                
                logger._log("INFO", f"{event_type}_success", {
                    "function": func.__name__,
                    "duration_ms": round(duration_ms, 2)
                })
                
                return result
            except Exception as e:
                duration_ms = (time.time() - start_time) * 1000
                
                logger._log("ERROR", f"{event_type}_error", {
                    "function": func.__name__,
                    "duration_ms": round(duration_ms, 2),
                    "error": str(e)
                })
                
                raise
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration_ms = (time.time() - start_time) * 1000
                
                logger._log("INFO", f"{event_type}_success", {
                    "function": func.__name__,
                    "duration_ms": round(duration_ms, 2)
                })
                
                return result
            except Exception as e:
                duration_ms = (time.time() - start_time) * 1000
                
                logger._log("ERROR", f"{event_type}_error", {
                    "function": func.__name__,
                    "duration_ms": round(duration_ms, 2),
                    "error": str(e)
                })
                
                raise
        
        # Return appropriate wrapper based on function type
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


# Example usage
if __name__ == "__main__":
    # Test the logger
    logger.log_api_call("get_markets", 123.45, True)
    logger.log_tool_execution("analyze_market", 234.56, True, market_id="bitcoin-100k")
    logger.log_resource_access("predyx://markets", 100.00, True, cache_hit=True)
    logger.log_error("connection_failed", {"endpoint": "api.polymarket.com"})
