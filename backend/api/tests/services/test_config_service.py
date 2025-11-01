import pytest
from pathlib import Path
from unittest.mock import mock_open, patch

from api.services.config_service import ConfigService


class TestConfigService:
    """Test suite for ConfigService."""

    @pytest.fixture
    def mock_pyproject_data(self):
        """Mock pyproject.toml data."""
        return {
            'project': {
                'name': 'backend',
                'version': '0.1.0',
                'description': 'Byte in Bottle FastAPI Backend Service.',
            }
        }

    @pytest.fixture
    def service(self):
        """Create a fresh ConfigService instance."""
        return ConfigService()

    def test_initialization(self, service):
        """Test service initialization."""
        assert service._pyproject_data is None
        assert isinstance(service._pyproject_path, Path)
        assert service._pyproject_path.name == 'pyproject.toml'

    def test_pyproject_path(self, service):
        """Test pyproject path resolution."""
        path = service._get_pyproject_path()
        assert path.name == 'pyproject.toml'
        assert path.is_absolute()

    def test_lazy_loading(self, service, mock_pyproject_data):
        """Test that pyproject is loaded lazily and cached."""
        with patch('builtins.open', mock_open()):
            with patch('tomllib.load', return_value=mock_pyproject_data):
                # First call should load
                assert service._pyproject_data is None
                result1 = service._load_pyproject()
                assert service._pyproject_data is not None

                # Second call should use cache
                result2 = service._load_pyproject()
                assert result1 is result2

    def test_get_project_info(self, service, mock_pyproject_data):
        """Test retrieving project info."""
        with patch.object(
            service, '_load_pyproject', return_value=mock_pyproject_data
        ):
            info = service.get_project_info()
            assert info == mock_pyproject_data['project']

    def test_get_project_name(self, service, mock_pyproject_data):
        """Test getting project name."""
        with patch.object(
            service, '_load_pyproject', return_value=mock_pyproject_data
        ):
            assert service.get_project_name() == 'backend'

    def test_get_project_version(self, service, mock_pyproject_data):
        """Test getting project version."""
        with patch.object(
            service, '_load_pyproject', return_value=mock_pyproject_data
        ):
            assert service.get_project_version() == '0.1.0'

    def test_get_project_description(self, service, mock_pyproject_data):
        """Test getting project description."""
        with patch.object(
            service, '_load_pyproject', return_value=mock_pyproject_data
        ):
            desc = service.get_project_description()
            assert desc == 'Byte in Bottle FastAPI Backend Service.'

    def test_get_api_title_default(self, service, mock_pyproject_data):
        """Test getting API title with default name."""
        with patch.object(
            service, '_load_pyproject', return_value=mock_pyproject_data
        ):
            assert service.get_api_title() == 'Byte in Bottle API'

    def test_get_api_title_custom(self, service):
        """Test getting API title with custom name."""
        custom_data = {'project': {'name': 'custom-backend'}}
        with patch.object(
            service, '_load_pyproject', return_value=custom_data
        ):
            title = service.get_api_title()
            assert 'Byte in Bottle API' in title

    def test_defaults_on_missing_data(self, service):
        """Test default values when project data is missing."""
        empty_data = {'project': {}}
        with patch.object(
            service, '_load_pyproject', return_value=empty_data
        ):
            assert service.get_project_name() == 'backend'
            assert service.get_project_version() == '0.1.0'
            assert 'Powered by bytes' in service.get_project_description()
