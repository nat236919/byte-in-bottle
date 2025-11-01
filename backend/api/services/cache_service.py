"""Cache service for Redis operations."""
import hashlib
import json
import os
from typing import Optional

import redis.asyncio as redis

from api.models.chats.ask_model import AskMode


class CacheService:
    """Service for caching and rate limiting using Redis.

    This service provides async Redis operations for:
    - Caching LLM responses to reduce redundant API calls
    - Rate limiting to prevent abuse
    - Session management for conversation history

    Attributes:
        redis_client: Async Redis client instance
        cache_ttl: Time-to-live for cached responses in seconds
        rate_limit_window: Time window for rate limiting in seconds
        rate_limit_max: Maximum requests allowed per window
    """

    def __init__(self):
        """Initialize the cache service.

        Connects to Redis using REDIS_URL from environment.
        Falls back to localhost if not specified.
        """
        redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
        self.redis_client = redis.from_url(
            redis_url,
            encoding='utf-8',
            decode_responses=True,
        )
        self.cache_ttl = int(os.getenv('CACHE_TTL', '3600'))  # 1 hour
        self.rate_limit_window = int(
            os.getenv('RATE_LIMIT_WINDOW', '60')
        )  # 60 seconds
        self.rate_limit_max = int(
            os.getenv('RATE_LIMIT_MAX', '10')
        )  # 10 requests

    def _generate_cache_key(
        self, model: str, prompt: str, mode: str = AskMode.CONCISE
    ) -> str:
        """Generate a cache key for LLM responses.

        Args:
            model (str): The model name
            prompt (str): The prompt text
            mode (str): The response mode (concise, professional, etc.)

        Returns:
            str: Cache key in format 'llm:{model}:{mode}:{hash}'
        """
        # Use SHA256 hash of prompt for consistent key generation
        prompt_hash = hashlib.sha256(prompt.encode()).hexdigest()[:16]
        return f'llm:{model}:{mode}:{prompt_hash}'

    async def get_cached_response(
        self, model: str, prompt: str, mode: str = AskMode.CONCISE
    ) -> Optional[dict]:
        """Get cached LLM response if available.

        Args:
            model (str): The model name
            prompt (str): The prompt text
            mode (str): The response mode (concise, professional, etc.)

        Returns:
            Optional[dict]: Cached response dict or None if not found
        """
        try:
            cache_key = self._generate_cache_key(model, prompt, mode)
            cached_data = await self.redis_client.get(cache_key)
            if cached_data:
                return json.loads(cached_data)
            return None
        except Exception:
            # If Redis fails, don't break the app - just skip cache
            return None

    async def cache_response(
        self,
        model: str,
        prompt: str,
        response: dict,
        mode: str = AskMode.CONCISE,
        ttl: Optional[int] = None,
    ) -> bool:
        """Cache an LLM response.

        Args:
            model (str): The model name
            prompt (str): The prompt text
            response (dict): The response data to cache
            mode (str): The response mode (concise, professional, etc.)
            ttl (Optional[int]): Time-to-live in seconds, uses default if None

        Returns:
            bool: True if cached successfully, False otherwise
        """
        try:
            cache_key = self._generate_cache_key(model, prompt, mode)
            ttl = ttl or self.cache_ttl
            await self.redis_client.setex(
                cache_key, ttl, json.dumps(response)
            )
            return True
        except Exception:
            # If Redis fails, don't break the app - just skip cache
            return False

    async def check_rate_limit(self, identifier: str) -> tuple[bool, int]:
        """Check if request is within rate limit.

        Args:
            identifier (str): Unique identifier (user ID, IP address, etc.)

        Returns:
            tuple[bool, int]: (is_allowed, current_count)
                is_allowed: True if request is allowed
                current_count: Current number of requests in window
        """
        try:
            key = f'rate_limit:{identifier}'
            current_count = await self.redis_client.get(key)

            if current_count is None:
                current_count = 0
            else:
                current_count = int(current_count)

            is_allowed = current_count < self.rate_limit_max
            return is_allowed, current_count

        except Exception:
            # If Redis fails, allow the request (fail open)
            return True, 0

    async def increment_rate_limit(self, identifier: str) -> int:
        """Increment rate limit counter.

        Args:
            identifier (str): Unique identifier (user ID, IP address, etc.)

        Returns:
            int: New count after increment
        """
        try:
            key = f'rate_limit:{identifier}'
            count = await self.redis_client.incr(key)

            # Set expiry on first request
            if count == 1:
                await self.redis_client.expire(key, self.rate_limit_window)

            return count
        except Exception:
            # If Redis fails, return 0
            return 0

    async def clear_cache(self, pattern: str = 'llm:*') -> int:
        """Clear cached entries matching pattern.

        Args:
            pattern (str): Redis key pattern to match

        Returns:
            int: Number of keys deleted
        """
        try:
            cursor = 0
            deleted = 0
            while True:
                cursor, keys = await self.redis_client.scan(
                    cursor, match=pattern, count=100
                )
                if keys:
                    deleted += await self.redis_client.delete(*keys)
                if cursor == 0:
                    break
            return deleted
        except Exception:
            return 0

    async def health_check(self) -> bool:
        """Check if Redis connection is healthy.

        Returns:
            bool: True if Redis is accessible, False otherwise
        """
        try:
            await self.redis_client.ping()
            return True
        except Exception:
            return False

    async def close(self):
        """Close Redis connection."""
        try:
            await self.redis_client.close()
        except Exception:
            pass


# Singleton instance
cache_service = CacheService()
