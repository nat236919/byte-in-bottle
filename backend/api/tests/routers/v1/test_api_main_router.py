import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from api.main import app


class TestMainRouter:
    """Test suite for main v1 router endpoints."""

    @pytest.fixture
    def client(self):
        """Create a test client."""
        return TestClient(app)

    def test_root_endpoint(self, client):
        """Test the root endpoint returns welcome message."""
        response = client.get('/v1/')
        assert response.status_code == 200
        data = response.json()
        assert data['message'] == 'Welcome to Byte in Bottle API v1'

    @pytest.mark.asyncio
    async def test_health_check_all_healthy(self, client):
        """Test health check when all services are healthy."""
        # Return list of model names instead of Mock objects
        mock_models = ['llama3.2', 'mistral']

        with patch(
            'api.routers.v1.api_main_router.core_service.get_ollama_models',
            new_callable=AsyncMock,
            return_value=mock_models
        ), patch(
            'api.routers.v1.api_main_router.cache_service.health_check',
            new_callable=AsyncMock,
            return_value=True
        ):
            response = client.get('/v1/health')
            assert response.status_code == 200
            data = response.json()
            assert data['status'] == 'healthy'
            assert data['ollama'] == 'connected'
            assert data['redis'] == 'connected'
            assert len(data['available_models']) == 2

    @pytest.mark.asyncio
    async def test_health_check_ollama_down(self, client):
        """Test health check when Ollama is disconnected."""
        with patch(
            'api.routers.v1.api_main_router.core_service.get_ollama_models',
            new_callable=AsyncMock,
            side_effect=Exception('Ollama error')
        ), patch(
            'api.routers.v1.api_main_router.cache_service.health_check',
            new_callable=AsyncMock,
            return_value=True
        ):
            response = client.get('/v1/health')
            assert response.status_code == 200
            data = response.json()
            assert data['status'] == 'degraded'
            assert data['ollama'] == 'disconnected'
            assert data['redis'] == 'connected'
            assert data['available_models'] == []

    @pytest.mark.asyncio
    async def test_health_check_redis_down(self, client):
        """Test health check when Redis is disconnected."""
        mock_models = ['llama3.2']

        with patch(
            'api.routers.v1.api_main_router.core_service.get_ollama_models',
            new_callable=AsyncMock,
            return_value=mock_models
        ), patch(
            'api.routers.v1.api_main_router.cache_service.health_check',
            new_callable=AsyncMock,
            return_value=False
        ):
            response = client.get('/v1/health')
            assert response.status_code == 200
            data = response.json()
            assert data['status'] == 'degraded'
            assert data['ollama'] == 'connected'
            assert data['redis'] == 'disconnected'

    @pytest.mark.asyncio
    async def test_health_check_all_down(self, client):
        """Test health check when all services are down."""
        with patch(
            'api.routers.v1.api_main_router.core_service.get_ollama_models',
            new_callable=AsyncMock,
            side_effect=Exception('Error')
        ), patch(
            'api.routers.v1.api_main_router.cache_service.health_check',
            new_callable=AsyncMock,
            return_value=False
        ):
            response = client.get('/v1/health')
            assert response.status_code == 200
            data = response.json()
            assert data['status'] == 'unhealthy'
            assert data['ollama'] == 'disconnected'
            assert data['redis'] == 'disconnected'
