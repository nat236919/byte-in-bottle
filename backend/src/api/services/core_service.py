import os

import ollama


# System prompts for different response modes
MODE_PROMPTS = {
    'concise': (
        'Please provide a concise answer to the following question '
        'without any additional explanations or context. Be brief and '
        'to the point.'
        'Do not ask back questions.'
    ),
    'professional': (
        'Please provide a professional, well-structured answer to the '
        'following question. Use formal language, proper terminology, '
        'and maintain a business-appropriate tone.'
        'Do not ask back questions.'
    ),
    'sarcastic': (
        'Please answer the following question with a sarcastic and witty '
        'tone. Be clever, use humor, and don\'t take things too seriously, '
        'but still provide a helpful answer.'
        'Do not ask back questions.'
    ),
    'creative': (
        'Please provide a creative and imaginative answer to the following '
        'question. Feel free to use metaphors, analogies, and think outside '
        'the box while still being informative.'
        'Do not ask back questions.'
    ),
    'friendly': (
        'Please provide a friendly, casual answer to the following question. '
        'Use a warm, conversational tone as if talking to a friend. '
        'Be approachable and personable.'
        'Do not ask back questions.'
    ),
}


class CoreService:

    def __init__(self):
        self.ollama_client = self._get_ollama_client()
        self.async_ollama_client = self._get_async_ollama_client()

    def _get_ollama_client(self) -> ollama.Client:
        """Get Ollama client instance.

        Returns:
            ollama.Client: The Ollama client.
        """
        ollama_host = os.getenv('OLLAMA_HOST')
        if ollama_host:
            return ollama.Client(host=ollama_host)
        return ollama.Client()

    def _get_async_ollama_client(self) -> ollama.AsyncClient:
        """Get async Ollama client instance.

        Returns:
            ollama.AsyncClient: The async Ollama client.
        """
        ollama_host = os.getenv('OLLAMA_HOST')
        if ollama_host:
            return ollama.AsyncClient(host=ollama_host)
        return ollama.AsyncClient()

    async def get_ollama_models(self) -> list:
        """Retrieve the list of available Ollama models.

        Returns:
            list: A list of available Ollama model objects.
        """
        res = await self.async_ollama_client.list()
        return res.models

    def get_system_prompt(self, mode: str = 'concise') -> str:
        """Get the system prompt for a given mode.

        Args:
            mode (str): The response mode (concise, professional, etc.).
                Defaults to 'concise'.

        Returns:
            str: The system prompt for the specified mode.
        """
        return MODE_PROMPTS.get(mode, MODE_PROMPTS['concise'])

    async def generate_text(
        self, model: str,
        prompt: str,
        system_prompt: str = ''
    ) -> dict:
        """Generate text using a specified Ollama model.

        Args:
            model (str): The Ollama model to use.
            prompt (str): The prompt text.
            system_prompt (str): The system prompt to guide the model.
                Defaults to ''.

        Returns:
            dict: The generated text response.

        Raises:
            ValueError: If the specified model is not available.
        """
        if system_prompt:
            prompt = f"{system_prompt}:\n\n{prompt}"
        return await self.async_ollama_client.generate(
            model=model, prompt=prompt
        )


# Singleton instance
core_service = CoreService()
