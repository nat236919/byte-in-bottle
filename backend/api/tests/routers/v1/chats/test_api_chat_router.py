import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from api.main import app


class TestChatRouter:
    """Test suite for chat router endpoints."""

    @pytest.fixture
    def client(self):
        """Create a test client."""
        return TestClient(app)

    @pytest.fixture
    def mock_services(self):
        """Mock all service dependencies."""
        with patch(
            'api.routers.v1.chats.api_chat_router.cache_service'
        ) as mock_cache, patch(
            'api.routers.v1.chats.api_chat_router.core_service'
        ) as mock_core:
            # Default mocks
            mock_cache.check_rate_limit = AsyncMock(return_value=(True, 0))
            mock_cache.increment_rate_limit = AsyncMock(return_value=1)
            mock_cache.get_cached_response = AsyncMock(return_value=None)
            mock_cache.cache_response = AsyncMock(return_value=True)
            mock_cache.rate_limit_max = 10
            mock_cache.rate_limit_window = 60

            mock_core.get_system_prompt = lambda mode: f"System: {mode}"
            mock_core.generate_text = AsyncMock(return_value={
                'response': 'Generated response',
                'created_at': '2025-11-01T12:00:00Z',
                'done': True
            })

            yield mock_cache, mock_core

    def test_ask_endpoint_success(self, client, mock_services):
        """Test successful ask request."""
        payload = {
            'model': 'llama3.2',
            'prompt': 'What is AI?',
            'mode': 'concise'
        }

        response = client.post('/v1/chats/ask', json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data['model'] == 'llama3.2'
        assert data['response'] == 'Generated response'
        assert data['mode'] == 'concise'
        assert data['done'] is True

    def test_ask_endpoint_with_cache_hit(self, client, mock_services):
        """Test ask request with cached response."""
        mock_cache, _ = mock_services
        mock_cache.get_cached_response = AsyncMock(return_value={
            'response': 'Cached response',
            'created_at': '2025-11-01T11:00:00Z',
            'done': True
        })

        payload = {
            'model': 'llama3.2',
            'prompt': 'What is AI?',
            'mode': 'concise'
        }

        response = client.post('/v1/chats/ask', json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data['response'] == 'Cached response'

    def test_ask_endpoint_rate_limit_exceeded(self, client, mock_services):
        """Test ask request when rate limit is exceeded."""
        mock_cache, _ = mock_services
        mock_cache.check_rate_limit = AsyncMock(return_value=(False, 10))

        payload = {
            'model': 'llama3.2',
            'prompt': 'What is AI?',
            'mode': 'concise'
        }

        response = client.post('/v1/chats/ask', json=payload)
        assert response.status_code == 429
        assert 'Rate limit exceeded' in response.json()['detail']

    def test_ask_endpoint_all_modes(self, client, mock_services):
        """Test ask request with all available modes."""
        modes = ['concise', 'professional', 'sarcastic',
                 'creative', 'friendly']

        for mode in modes:
            payload = {
                'model': 'llama3.2',
                'prompt': 'Test',
                'mode': mode
            }
            response = client.post('/v1/chats/ask', json=payload)
            assert response.status_code == 200
            assert response.json()['mode'] == mode

    def test_ask_endpoint_generation_error(self, client, mock_services):
        """Test ask request when generation fails."""
        _, mock_core = mock_services
        mock_core.generate_text = AsyncMock(
            side_effect=Exception('Generation failed')
        )

        payload = {
            'model': 'llama3.2',
            'prompt': 'What is AI?',
            'mode': 'concise'
        }

        response = client.post('/v1/chats/ask', json=payload)
        assert response.status_code == 500
        assert 'Generation failed' in response.json()['detail']

    def test_ask_endpoint_invalid_mode(self, client):
        """Test ask request with invalid mode."""
        payload = {
            'model': 'llama3.2',
            'prompt': 'What is AI?',
            'mode': 'invalid_mode'
        }

        response = client.post('/v1/chats/ask', json=payload)
        assert response.status_code == 422  # Validation error

    def test_ask_endpoint_missing_fields(self, client, mock_services):
        """Test ask request validation with Pydantic defaults."""
        # With default values, this should succeed not fail
        # The model has defaults for all fields
        response = client.post('/v1/chats/ask', json={
            'prompt': 'Test'
        })
        # Should succeed because defaults are provided
        assert response.status_code == 200

    def test_ask_endpoint_default_values(self, client, mock_services):
        """Test ask request uses default values."""
        # Don't specify model, prompt, or mode - should use defaults
        response = client.post('/v1/chats/ask', json={})
        assert response.status_code == 200
        data = response.json()
        assert data['model'] == 'llama3.2'
        assert data['mode'] == 'concise'

    def test_ask_endpoint_caches_response(self, client, mock_services):
        """Test that successful responses are cached."""
        mock_cache, _ = mock_services

        payload = {
            'model': 'llama3.2',
            'prompt': 'What is AI?',
            'mode': 'concise'
        }

        response = client.post('/v1/chats/ask', json=payload)
        assert response.status_code == 200

        # Verify cache_response was called
        mock_cache.cache_response.assert_called_once()
        call_args = mock_cache.cache_response.call_args
        assert call_args[0][0] == 'llama3.2'  # model
        assert call_args[0][1] == 'What is AI?'  # prompt
        assert call_args[0][3] == 'concise'  # mode

    def test_ask_endpoint_increments_rate_limit(self, client, mock_services):
        """Test that rate limit is incremented on new requests."""
        mock_cache, _ = mock_services

        payload = {
            'model': 'llama3.2',
            'prompt': 'What is AI?',
            'mode': 'concise'
        }

        response = client.post('/v1/chats/ask', json=payload)
        assert response.status_code == 200

        # Verify rate limit was incremented
        mock_cache.increment_rate_limit.assert_called_once()

    def test_ask_endpoint_skips_rate_increment_on_cache_hit(
        self, client, mock_services
    ):
        """Test that rate limit is not incremented on cache hit."""
        mock_cache, _ = mock_services
        mock_cache.get_cached_response = AsyncMock(return_value={
            'response': 'Cached',
            'created_at': '2025-11-01T11:00:00Z',
            'done': True
        })

        payload = {
            'model': 'llama3.2',
            'prompt': 'What is AI?',
            'mode': 'concise'
        }

        response = client.post('/v1/chats/ask', json=payload)
        assert response.status_code == 200

        # Rate limit should NOT be incremented on cache hit
        mock_cache.increment_rate_limit.assert_not_called()
