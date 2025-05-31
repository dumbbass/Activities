from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import status
import time
from functools import wraps

def rate_limit(limit=60, period=60):
    """
    Rate limiting decorator that limits the number of requests per IP address
    within a specified time period.
    
    Args:
        limit (int): Maximum number of requests allowed within the period
        period (int): Time period in seconds
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(self, request, *args, **kwargs):
            # Get client IP address
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')

            # Create a unique key for this IP and endpoint
            cache_key = f'rate_limit_{ip}_{request.path}'
            
            # Get current request count and timestamp
            current = cache.get(cache_key)
            
            if current is None:
                # First request from this IP
                cache.set(cache_key, {
                    'count': 1,
                    'timestamp': time.time()
                }, period)
            else:
                # Check if we're still within the time period
                if time.time() - current['timestamp'] > period:
                    # Reset if period has passed
                    cache.set(cache_key, {
                        'count': 1,
                        'timestamp': time.time()
                    }, period)
                else:
                    # Increment count if within period
                    current['count'] += 1
                    cache.set(cache_key, current, period)
                    
                    # Check if limit exceeded
                    if current['count'] > limit:
                        return Response({
                            'error': 'Rate limit exceeded',
                            'detail': f'Too many requests. Maximum {limit} requests per {period} seconds.'
                        }, status=status.HTTP_429_TOO_MANY_REQUESTS)

            # Process the request if rate limit not exceeded
            return view_func(self, request, *args, **kwargs)
        return wrapped_view
    return decorator 