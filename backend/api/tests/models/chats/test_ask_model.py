import pytest
from pydantic import ValidationError

from api.models.chats.ask_model import AskMode, AskRequest, AskResponse


class TestAskMode:
    """Test suite for AskMode enum."""

    def test_enum_values_and_membership(self):
        """Test AskMode enum values and membership."""
        expected_modes = {
            AskMode.CONCISE: 'concise',
            AskMode.PROFESSIONAL: 'professional',
            AskMode.SARCASTIC: 'sarcastic',
            AskMode.CREATIVE: 'creative',
            AskMode.FRIENDLY: 'friendly',
        }
        for mode, value in expected_modes.items():
            assert mode == value
            assert mode in AskMode
        assert len(list(AskMode)) == 5


class TestAskRequest:
    """Test suite for AskRequest model."""

    def test_defaults(self):
        """Test default values."""
        request = AskRequest()
        assert request.model == 'llama3.2'
        assert request.prompt == 'hello world'
        assert request.mode == AskMode.CONCISE

    def test_custom_values_and_all_modes(self):
        """Test custom values and all mode variations."""
        for mode in AskMode:
            request = AskRequest(
                model='mistral', prompt='Test prompt', mode=mode
            )
            assert request.model == 'mistral'
            assert request.mode == mode

    def test_serialization(self):
        """Test serialization and deserialization."""
        data = {'model': 'llama3.2', 'prompt': 'Test', 'mode': 'professional'}
        request = AskRequest(**data)
        assert request.mode == AskMode.PROFESSIONAL

        serialized = request.model_dump()
        assert serialized['mode'] == 'professional'
        assert '"mode":"professional"' in request.model_dump_json()

    def test_validation(self):
        """Test validation errors."""
        with pytest.raises(ValidationError, match='mode'):
            AskRequest(mode='invalid_mode')

    def test_edge_cases(self):
        """Test edge cases."""
        assert AskRequest(prompt='').prompt == ''
        assert len(AskRequest(prompt='A' * 10000).prompt) == 10000
        special = 'Hello! @#$%^&*() 你好 🚀'
        assert AskRequest(prompt=special).prompt == special


class TestAskResponse:
    """Test suite for AskResponse model."""

    def test_full_response(self):
        """Test complete response with all fields."""
        response = AskResponse(
            model='llama3.2',
            response='Test response',
            created_at='2025-11-01T12:00:00Z',
            done=True,
            mode='concise'
        )
        assert response.model == 'llama3.2'
        assert response.response == 'Test response'
        assert response.created_at == '2025-11-01T12:00:00Z'
        assert response.done is True
        assert response.mode == 'concise'

    def test_all_modes(self):
        """Test all mode variations."""
        for mode in ['concise', 'professional', 'sarcastic',
                     'creative', 'friendly']:
            response = AskResponse(
                model='llama3.2', response='Test',
                created_at='2025-11-01T12:00:00Z',
                done=True, mode=mode
            )
            assert response.mode == mode

    def test_streaming_state(self):
        """Test streaming response with done=False."""
        response = AskResponse(
            model='llama3.2', response='Partial',
            created_at='2025-11-01T12:00:00Z',
            done=False, mode='concise'
        )
        assert response.done is False

    def test_serialization(self):
        """Test serialization and deserialization."""
        data = {
            'model': 'llama3.2', 'response': 'Hello',
            'created_at': '2025-11-01T12:00:00Z',
            'done': True, 'mode': 'friendly'
        }
        response = AskResponse(**data)
        serialized = response.model_dump()
        assert serialized['mode'] == 'friendly'
        assert '"done":true' in response.model_dump_json()

    def test_validation(self):
        """Test validation of required fields."""
        with pytest.raises(ValidationError):
            AskResponse()

    def test_edge_cases(self):
        """Test edge cases."""
        base_args = {
            'model': 'llama3.2',
            'created_at': '2025-11-01T12:00:00Z',
            'done': True,
            'mode': 'concise'
        }
        # Empty response
        assert AskResponse(**base_args, response='').response == ''
        # Long response
        long_text = 'A' * 100000
        assert len(AskResponse(**base_args, response=long_text).response) \
            == 100000
        # Special characters
        special = 'émojis 🎉 中文'
        assert AskResponse(**base_args, response=special).response == special
        # Multiline
        multiline = "Line 1\nLine 2"
        assert '\n' in AskResponse(**base_args, response=multiline).response
