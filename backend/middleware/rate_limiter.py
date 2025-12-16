import time
from typing import Dict
from fastapi import Request, HTTPException
from collections import defaultdict, deque


class RateLimiter:
    def __init__(self, max_requests: int = 100, window_seconds: int = 3600):  # 100 requests per hour
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, deque] = defaultdict(deque)
    
    def is_allowed(self, identifier: str) -> bool:
        """
        Check if a request from the given identifier is allowed.
        
        Args:
            identifier: A unique identifier for the requester (e.g., IP address)
            
        Returns:
            True if allowed, False otherwise
        """
        current_time = time.time() 
        # Remove requests that are outside the current window
        while (self.requests[identifier] and 
               current_time - self.requests[identifier][0] > self.window_seconds):
            self.requests[identifier].popleft()
        
        # Check if we're under the limit
        if len(self.requests[identifier]) < self.max_requests:
            self.requests[identifier].append(current_time)
            return True
        
        return False


# Create a global rate limiter instance (100 requests per hour per IP)
rate_limiter = RateLimiter(max_requests=100, window_seconds=3600)


def rate_limit_middleware(request: Request) -> None:
    """
    Rate limiting middleware function.
    
    Args:
        request: The incoming request object
        
    Raises:
        HTTPException: If the rate limit is exceeded
    """
    # Use the client's IP address as the identifier
    client_ip = request.client.host
    
    if not rate_limiter.is_allowed(client_ip):
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Please try again later."
        )