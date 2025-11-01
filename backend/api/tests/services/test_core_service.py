import pytest
from unittest.mock import AsyncMock, Mock, patch
import os

from api.services.core_service import CoreService, MODE_PROMPTS, AskMode


class TestCoreService:
    """Test suite for CoreService."""

    @pytest.fixture
    def service(self):
        """Create a CoreService instance with mocked clients."""
        with patch('api.services.core_service.ollama.Client'), \
                patch('api.services.core_service.ollama.AsyncClient'):
            return CoreService()

    def test_initialization(self, service):
        """Test service initialization."""
        assert service.ollama_client is not None
        assert service.async_ollama_client is not None

    def test_ollama_client_with_host(self):
        """Test Ollama client creation with custom host."""
        with patch.dict(os.environ, {'OLLAMA_HOST': 'http://custom:11434'}):
            with patch('api.services.core_service.ollama.Client') as mock:
                service = CoreService()
                service._get_ollama_client()
                mock.assert_called_with(host='http://custom:11434')

    def test_ollama_client_default(self):
        """Test Ollama client creation with default host."""
        with patch.dict(os.environ, {}, clear=True):
            with patch('api.services.core_service.ollama.Client') as mock:
                service = CoreService()
                service._get_ollama_client()
                mock.assert_called_with()

    def test_async_ollama_client_with_host(self):
        """Test async Ollama client creation with custom host."""
        with patch.dict(os.environ, {'OLLAMA_HOST': 'http://custom:11434'}):
            with patch(
                'api.services.core_service.ollama.AsyncClient'
            ) as mock:
                service = CoreService()
                service._get_async_ollama_client()
                mock.assert_called_with(host='http://custom:11434')

    @pytest.mark.asyncio
    async def test_get_ollama_models(self, service):
        """Test retrieving available models."""
        mock_models = [
            Mock(name='llama3.2'),
            Mock(name='mistral'),
        ]
        mock_response = Mock(models=mock_models)
        service.async_ollama_client.list = AsyncMock(
            return_value=mock_response
        )

        models = await service.get_ollama_models()
        assert models == mock_models
        service.async_ollama_client.list.assert_called_once()

    def test_get_system_prompt_all_modes(self, service):
        """Test system prompt for all modes."""
        for mode in AskMode:
            prompt = service.get_system_prompt(mode)
            assert isinstance(prompt, str)
            assert len(prompt) > 0
            assert prompt == MODE_PROMPTS[mode]

    def test_get_system_prompt_default(self, service):
        """Test default system prompt."""
        prompt = service.get_system_prompt()
        assert prompt == MODE_PROMPTS[AskMode.CONCISE]

    def test_get_system_prompt_invalid_mode(self, service):
        """Test system prompt with invalid mode defaults to concise."""
        prompt = service.get_system_prompt('invalid_mode')
        assert prompt == MODE_PROMPTS[AskMode.CONCISE]

    @pytest.mark.asyncio
    async def test_generate_text_basic(self, service):
        """Test text generation without system prompt."""
        mock_response = {'response': 'Generated text'}
        service.async_ollama_client.generate = AsyncMock(
            return_value=mock_response
        )

        result = await service.generate_text('llama3.2', 'Test prompt')

        assert result == mock_response
        service.async_ollama_client.generate.assert_called_once_with(
            model='llama3.2',
            prompt='Test prompt'
        )

    @pytest.mark.asyncio
    async def test_generate_text_with_system_prompt(self, service):
        """Test text generation with system prompt."""
        mock_response = {'response': 'Generated text'}
        service.async_ollama_client.generate = AsyncMock(
            return_value=mock_response
        )

        result = await service.generate_text(
            'llama3.2',
            'Test prompt',
            'System instruction'
        )

        assert result == mock_response
        call_args = service.async_ollama_client.generate.call_args
        assert call_args[1]['model'] == 'llama3.2'
        assert 'System instruction' in call_args[1]['prompt']
        assert 'Test prompt' in call_args[1]['prompt']

    def test_mode_prompts_exist(self):
        """Test that all mode prompts are defined."""
        for mode in AskMode:
            assert mode in MODE_PROMPTS
            assert isinstance(MODE_PROMPTS[mode], str)
            assert len(MODE_PROMPTS[mode]) > 0
