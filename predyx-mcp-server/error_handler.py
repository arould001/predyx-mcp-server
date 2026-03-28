"""
Intelligent error handling with automatic retry and user-friendly messages.

Provides:
- Automatic retry with exponential backoff
- Jitter to prevent thundering herd
- User-friendly error messages
- Retry tracking and logging
"""

import asyncio
import random
import time
from functools import wraps
from typing import Any, Callable, Optional, Type, Tuple
from logger import logger


class RetryExhaustedError(Exception):
    """Raised when all retry attempts are exhausted."""
    pass


class UserFriendlyError(Exception):
    """User-friendly error with actionable message."""
    
    def __init__(self, message: str, original_error: Optional[Exception] = None):
        self.message = message
        self.original_error = original_error
        super().__init__(self.message)


def get_user_friendly_message(operation: str, error: Exception) -> str:
    """
    Convert technical errors into user-friendly messages.
    
    Args:
        operation: What operation was being performed (e.g., "fetch market details")
        error: The original exception
    
    Returns:
        User-friendly error message
    """
    error_str = str(error).lower()
    
    # Timeout errors
    if "timeout" in error_str or "timed out" in error_str:
        return f"Request timed out while trying to {operation}. Please try again."
    
    # Connection errors
    if "connection" in error_str or "network" in error_str or "unreachable" in error_str:
        return f"Connection failed while trying to {operation}. Please check your network."
    
    # Not found errors
    if "not found" in error_str or "404" in error_str:
        return f"Resource not found while trying to {operation}. Please verify the ID."
    
    # Rate limit errors
    if "rate limit" in error_str or "429" in error_str or "too many requests" in error_str:
        return f"Rate limit exceeded while trying to {operation}. Please wait a moment and try again."
    
    # Authentication errors
    if "unauthorized" in error_str or "401" in error_str or "forbidden" in error_str or "403" in error_str:
        return f"Authentication failed while trying to {operation}. Please check your credentials."
    
    # Validation errors
    if "validation" in error_str or "invalid" in error_str:
        return f"Invalid input while trying to {operation}. Please check your parameters."
    
    # Default generic message
    return f"An error occurred while trying to {operation}. Please try again later."


def retry_on_failure(
    max_retries: int = 3,
    delay: float = 1.0,
    backoff_factor: float = 2.0,
    max_delay: float = 30.0,
    jitter: bool = True,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
):
    """
    Decorator for automatic retry with exponential backoff.
    
    Args:
        max_retries: Maximum number of retry attempts
        delay: Initial delay in seconds
        backoff_factor: Multiplier for delay after each retry
        max_delay: Maximum delay between retries
        jitter: Add random jitter to prevent thundering herd
        exceptions: Tuple of exception types to catch
    
    Usage:
        @retry_on_failure(max_retries=3, delay=1.0)
        async def fetch_data():
            # API call that might fail
            pass
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            last_exception = None
            current_delay = delay
            
            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    
                    # Log the error
                    logger.log_warning("retry_attempt", {
                        "function": func.__name__,
                        "attempt": attempt + 1,
                        "max_retries": max_retries,
                        "error": str(e),
                        "next_delay": current_delay if attempt < max_retries else None
                    })
                    
                    # If this was the last attempt, raise
                    if attempt == max_retries:
                        logger.log_error("retry_exhausted", {
                            "function": func.__name__,
                            "attempts": max_retries + 1,
                            "final_error": str(e)
                        })
                        raise RetryExhaustedError(
                            f"All {max_retries + 1} attempts failed for {func.__name__}"
                        ) from e
                    
                    # Calculate delay with optional jitter
                    actual_delay = current_delay
                    if jitter:
                        actual_delay += random.uniform(0, 0.5)
                    
                    # Wait before retrying
                    await asyncio.sleep(actual_delay)
                    
                    # Increase delay for next attempt
                    current_delay = min(current_delay * backoff_factor, max_delay)
            
            # Should never reach here, but just in case
            raise last_exception
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs) -> Any:
            last_exception = None
            current_delay = delay
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    
                    # Log the error
                    logger.log_warning("retry_attempt", {
                        "function": func.__name__,
                        "attempt": attempt + 1,
                        "max_retries": max_retries,
                        "error": str(e),
                        "next_delay": current_delay if attempt < max_retries else None
                    })
                    
                    # If this was the last attempt, raise
                    if attempt == max_retries:
                        logger.log_error("retry_exhausted", {
                            "function": func.__name__,
                            "attempts": max_retries + 1,
                            "final_error": str(e)
                        })
                        raise RetryExhaustedError(
                            f"All {max_retries + 1} attempts failed for {func.__name__}"
                        ) from e
                    
                    # Calculate delay with optional jitter
                    actual_delay = current_delay
                    if jitter:
                        actual_delay += random.uniform(0, 0.5)
                    
                    # Wait before retrying
                    time.sleep(actual_delay)
                    
                    # Increase delay for next attempt
                    current_delay = min(current_delay * backoff_factor, max_delay)
            
            # Should never reach here, but just in case
            raise last_exception
        
        # Return appropriate wrapper based on function type
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


def handle_api_error(operation: str, error: Exception, context: Optional[dict] = None) -> UserFriendlyError:
    """
    Convert API errors into user-friendly errors with context.
    
    Args:
        operation: What operation was being performed
        error: The original exception
        context: Additional context for logging
    
    Returns:
        UserFriendlyError with actionable message
    """
    user_message = get_user_friendly_message(operation, error)
    
    # Log the error with context
    log_data = {
        "operation": operation,
        "error_type": type(error).__name__,
        "error_message": str(error),
        "user_message": user_message
    }
    
    if context:
        log_data.update(context)
    
    logger.log_error("api_error", log_data)
    
    return UserFriendlyError(user_message, error)


# Example usage
if __name__ == "__main__":
    import aiohttp
    
    @retry_on_failure(max_retries=3, delay=1.0)
    async def fetch_example():
        """Example function that might fail."""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://httpbin.org/status/500") as response:
                if response.status != 200:
                    raise Exception(f"HTTP {response.status}")
                return await response.json()
    
    async def test():
        try:
            await fetch_example()
        except RetryExhaustedError as e:
            print(f"Failed after all retries: {e}")
        except UserFriendlyError as e:
            print(f"User-friendly error: {e.message}")
    
    # Run test
    asyncio.run(test())
