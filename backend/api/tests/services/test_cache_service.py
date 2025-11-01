import pytest
import json
from unittest.mock import AsyncMock, patch
import os

from api.services.cache_service import CacheService


class TestCacheService:
    """Test suite for CacheService."""

    @pytest.fixture
    def mock_redis(self):
        """Create a mock Redis client."""
        mock = AsyncMock()
        mock.get = AsyncMock(return_value=None)
        mock.setex = AsyncMock()
        mock.incr = AsyncMock(return_value=1)
        mock.expire = AsyncMock()
        mock.scan = AsyncMock(return_value=(0, []))
        mock.delete = AsyncMock(return_value=0)
        mock.ping = AsyncMock()
        mock.close = AsyncMock()
        return mock

    @pytest.fixture
    def service(self, mock_redis):
        """Create a CacheService with mocked Redis."""
        with patch('api.services.cache_service.redis.from_url',
                   return_value=mock_redis):
            return CacheService()

    def test_initialization(self, service):
        """Test service initialization."""
        assert service.redis_client is not None
        assert service.cache_ttl > 0
        assert service.rate_limit_window > 0
        assert service.rate_limit_max > 0

    def test_initialization_with_env_vars(self):
        """Test initialization with environment variables."""
        env_vars = {
            'REDIS_URL': 'redis://custom:6380/1',
            'CACHE_TTL': '7200',
            'RATE_LIMIT_WINDOW': '120',
            'RATE_LIMIT_MAX': '20'
        }
        with patch.dict(os.environ, env_vars):
            with patch('api.services.cache_service.redis.from_url') as mock:
                service = CacheService()
                mock.assert_called_once()
                assert service.cache_ttl == 7200
                assert service.rate_limit_window == 120
                assert service.rate_limit_max == 20

    def test_generate_cache_key(self, service):
        """Test cache key generation."""
        key1 = service._generate_cache_key('llama3.2', 'test', 'concise')
        key2 = service._generate_cache_key('llama3.2', 'test', 'concise')
        key3 = service._generate_cache_key('llama3.2', 'other', 'concise')

        assert key1 == key2  # Same input = same key
        assert key1 != key3  # Different prompt = different key
        assert key1.startswith('llm:llama3.2:concise:')
        assert len(key1.split(':')[-1]) == 16  # Hash length

    @pytest.mark.asyncio
    async def test_get_cached_response_hit(self, service, mock_redis):
        """Test getting cached response when cache exists."""
        cached_data = {'response': 'cached'}
        mock_redis.get.return_value = json.dumps(cached_data)

        result = await service.get_cached_response(
            'llama3.2', 'test', 'concise'
        )

        assert result == cached_data
        mock_redis.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_cached_response_miss(self, service, mock_redis):
        """Test getting cached response when cache doesn't exist."""
        mock_redis.get.return_value = None

        result = await service.get_cached_response(
            'llama3.2', 'test', 'concise'
        )

        assert result is None

    @pytest.mark.asyncio
    async def test_get_cached_response_error(self, service, mock_redis):
        """Test cache get handles errors gracefully."""
        mock_redis.get.side_effect = Exception('Redis error')

        result = await service.get_cached_response(
            'llama3.2', 'test', 'concise'
        )

        assert result is None  # Fails gracefully

    @pytest.mark.asyncio
    async def test_cache_response_success(self, service, mock_redis):
        """Test caching a response."""
        response_data = {'response': 'test'}

        result = await service.cache_response(
            'llama3.2', 'test', response_data, 'concise'
        )

        assert result is True
        mock_redis.setex.assert_called_once()
        call_args = mock_redis.setex.call_args[0]
        assert call_args[1] == service.cache_ttl  # Default TTL
        assert json.loads(call_args[2]) == response_data

    @pytest.mark.asyncio
    async def test_cache_response_custom_ttl(self, service, mock_redis):
        """Test caching with custom TTL."""
        await service.cache_response(
            'llama3.2', 'test', {}, 'concise', ttl=1800
        )

        call_args = mock_redis.setex.call_args[0]
        assert call_args[1] == 1800

    @pytest.mark.asyncio
    async def test_cache_response_error(self, service, mock_redis):
        """Test cache set handles errors gracefully."""
        mock_redis.setex.side_effect = Exception('Redis error')

        result = await service.cache_response(
            'llama3.2', 'test', {}, 'concise'
        )

        assert result is False  # Fails gracefully

    @pytest.mark.asyncio
    async def test_check_rate_limit_allowed(self, service, mock_redis):
        """Test rate limit check when allowed."""
        mock_redis.get.return_value = '5'
        service.rate_limit_max = 10

        is_allowed, count = await service.check_rate_limit('user123')

        assert is_allowed is True
        assert count == 5

    @pytest.mark.asyncio
    async def test_check_rate_limit_exceeded(self, service, mock_redis):
        """Test rate limit check when exceeded."""
        mock_redis.get.return_value = '10'
        service.rate_limit_max = 10

        is_allowed, count = await service.check_rate_limit('user123')

        assert is_allowed is False
        assert count == 10

    @pytest.mark.asyncio
    async def test_check_rate_limit_new_user(self, service, mock_redis):
        """Test rate limit check for new user."""
        mock_redis.get.return_value = None

        is_allowed, count = await service.check_rate_limit('user123')

        assert is_allowed is True
        assert count == 0

    @pytest.mark.asyncio
    async def test_increment_rate_limit(self, service, mock_redis):
        """Test incrementing rate limit counter."""
        mock_redis.incr.return_value = 1

        count = await service.increment_rate_limit('user123')

        assert count == 1
        mock_redis.incr.assert_called_once()
        mock_redis.expire.assert_called_once()

    @pytest.mark.asyncio
    async def test_increment_rate_limit_existing(self, service, mock_redis):
        """Test incrementing existing rate limit counter."""
        mock_redis.incr.return_value = 5

        count = await service.increment_rate_limit('user123')

        assert count == 5
        # Expire should not be called for existing counter
        mock_redis.expire.assert_not_called()

    @pytest.mark.asyncio
    async def test_clear_cache(self, service, mock_redis):
        """Test clearing cache entries."""
        mock_redis.scan.return_value = (0, ['key1', 'key2', 'key3'])
        mock_redis.delete.return_value = 3

        deleted = await service.clear_cache('llm:*')

        assert deleted == 3
        mock_redis.delete.assert_called_once_with('key1', 'key2', 'key3')

    @pytest.mark.asyncio
    async def test_clear_cache_pagination(self, service, mock_redis):
        """Test clearing cache with pagination."""
        # Simulate two pages of results
        mock_redis.scan.side_effect = [
            (1, ['key1', 'key2']),
            (0, ['key3'])
        ]
        mock_redis.delete.return_value = 1

        deleted = await service.clear_cache()

        assert deleted == 2
        assert mock_redis.scan.call_count == 2

    @pytest.mark.asyncio
    async def test_health_check_healthy(self, service, mock_redis):
        """Test health check when Redis is healthy."""
        result = await service.health_check()

        assert result is True
        mock_redis.ping.assert_called_once()

    @pytest.mark.asyncio
    async def test_health_check_unhealthy(self, service, mock_redis):
        """Test health check when Redis is unhealthy."""
        mock_redis.ping.side_effect = Exception('Connection error')

        result = await service.health_check()

        assert result is False

    @pytest.mark.asyncio
    async def test_close(self, service, mock_redis):
        """Test closing Redis connection."""
        await service.close()
        mock_redis.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_close_error_handling(self, service, mock_redis):
        """Test close handles errors gracefully."""
        mock_redis.close.side_effect = Exception('Close error')
        # Should not raise exception
        await service.close()
