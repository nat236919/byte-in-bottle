import pytest
from pydantic import ValidationError

from api.models.generic_model import RootResponse, HealthCheckResponse


class TestRootResponse:
    """Test suite for RootResponse model."""

    def test_valid_creation_and_serialization(self):
        """Test RootResponse creation and serialization."""
        response = RootResponse(message='Test message')
        assert response.message == 'Test message'
        assert response.model_dump() == {'message': 'Test message'}

    def test_edge_cases(self):
        """Test RootResponse edge cases."""
        assert RootResponse(message='').message == ''
        with pytest.raises(ValidationError, match='message'):
            RootResponse()


class TestHealthCheckResponse:
    """Test suite for HealthCheckResponse model."""

    def test_full_data_creation(self):
        """Test HealthCheckResponse with all fields."""
        response = HealthCheckResponse(
            status='healthy',
            ollama='connected',
            redis='connected',
            available_models=['llama3.2', 'mistral'],
            error=None
        )
        assert response.status == 'healthy'
        assert response.ollama == 'connected'
        assert response.redis == 'connected'
        assert response.available_models == ['llama3.2', 'mistral']
        assert response.error is None

    def test_minimal_data_with_defaults(self):
        """Test HealthCheckResponse with defaults."""
        response = HealthCheckResponse(
            status='healthy', ollama='connected', redis='connected'
        )
        assert response.available_models == []
        assert response.error is None

    def test_error_state(self):
        """Test HealthCheckResponse with error."""
        response = HealthCheckResponse(
            status='unhealthy',
            ollama='disconnected',
            redis='connected',
            error='Ollama service unavailable'
        )
        assert response.status == 'unhealthy'
        assert response.error == 'Ollama service unavailable'

    def test_serialization(self):
        """Test serialization and deserialization."""
        data = {
            'status': 'healthy',
            'ollama': 'connected',
            'redis': 'connected',
            'available_models': ['model1'],
        }
        response = HealthCheckResponse(**data)
        serialized = response.model_dump()
        assert serialized['status'] == 'healthy'
        assert serialized['available_models'] == ['model1']

    def test_validation(self):
        """Test validation of required fields."""
        with pytest.raises(ValidationError):
            HealthCheckResponse()
