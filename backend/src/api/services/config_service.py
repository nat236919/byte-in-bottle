"""Configuration service for loading project metadata."""
import tomllib
from pathlib import Path
from typing import Any


class ConfigService:
    """Service for loading and managing project configuration.

    This service provides a centralized way to access project metadata
    from pyproject.toml file. It implements lazy loading and caching
    to improve performance.

    Attributes:
        _pyproject_data: Cached pyproject.toml data as a dictionary.
        _pyproject_path: Path to the pyproject.toml file.
    """

    def __init__(self):
        """Initialize the configuration service.

        Sets up the pyproject path and prepares the cache for lazy loading.
        """
        self._pyproject_data: dict[str, Any] | None = None
        self._pyproject_path = self._get_pyproject_path()

    @staticmethod
    def _get_pyproject_path() -> Path:
        """Get the path to pyproject.toml file.

        Returns:
            Path: Absolute path to the pyproject.toml file.
        """
        # Navigate from api/services to backend root
        return Path(__file__).parent.parent.parent.parent / 'pyproject.toml'

    def _load_pyproject(self) -> dict[str, Any]:
        """Load pyproject.toml file.

        Loads and caches the pyproject.toml file content. Subsequent calls
        will return the cached data without re-reading the file.

        Returns:
            dict[str, Any]: Parsed pyproject.toml data as a dictionary.
        """
        if self._pyproject_data is None:
            with open(self._pyproject_path, 'rb') as f:
                self._pyproject_data = tomllib.load(f)
        return self._pyproject_data

    def get_project_info(self) -> dict[str, Any]:
        """Get project information from pyproject.toml.

        Returns:
            dict[str, Any]: Project section from pyproject.toml containing
                metadata like name, version, description, etc.
        """
        pyproject = self._load_pyproject()
        return pyproject.get('project', {})

    def get_project_name(self) -> str:
        """Get project name.

        Returns:
            str: Project name from pyproject.toml, defaults to 'backend'
                if not found.
        """
        project_info = self.get_project_info()
        return project_info.get('name', 'backend')

    def get_project_version(self) -> str:
        """Get project version.

        Returns:
            str: Project version from pyproject.toml, defaults to '0.1.0'
                if not found.
        """
        project_info = self.get_project_info()
        return project_info.get('version', '0.1.0')

    def get_project_description(self) -> str:
        """Get project description.

        Returns:
            str: Project description from pyproject.toml, defaults to
                'Powered by bytes. Driven by attitude.' if not found.
        """
        project_info = self.get_project_info()
        return project_info.get(
            'description',
            'Powered by bytes. Driven by attitude.'
        )

    def get_api_title(self) -> str:
        """Get API title formatted for FastAPI.

        Transforms the project name into a user-friendly API title.
        If the project name is 'backend', it returns 'Byte in Bottle API'.

        Returns:
            str: Formatted API title suitable for FastAPI application.
        """
        name = self.get_project_name()
        if name == 'backend':
            return 'Byte in Bottle API'
        return name.replace('backend', 'Byte in Bottle API')


# Singleton instance
config_service = ConfigService()
