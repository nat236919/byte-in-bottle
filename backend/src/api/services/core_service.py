import os

import ollama


class CoreService:

    def __init__(self):
        self.ollama_client = self._get_ollama_client()

    def _get_ollama_client(self) -> ollama.Client:
        """Get Ollama client instance.

        Returns:
            ollama.Client: The Ollama client.
        """
        ollama_host = os.getenv('OLLAMA_HOST')
        if ollama_host:
            return ollama.Client(host=ollama_host)
        return ollama.Client()

    def get_ollama_models(self) -> list:
        """Retrieve the list of available Ollama models.

        Returns:
            list: A list of available Ollama model objects.
        """
        res = self.ollama_client.list()
        return res.models

    def generate_text(self, model: str, prompt: str) -> dict:
        """Generate text using a specified Ollama model.

        Args:
            model (str): The Ollama model to use.
            prompt (str): The prompt text.

        Returns:
            dict: The generated text response.

        Raises:
            ValueError: If the specified model is not available.
        """
        return self.ollama_client.generate(model=model, prompt=prompt)
