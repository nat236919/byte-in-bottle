import os

import ollama

from api.models.chats.ask_model import AskMode

# System prompts for different response modes
MODE_PROMPTS: dict[AskMode, str] = {
    AskMode.CONCISE: "Be brief and direct. No extra context or follow-ups.",
    AskMode.PROFESSIONAL: (
        "Use formal language and proper terminology. "
        "Be thorough yet precise. No follow-ups."
    ),
    AskMode.SARCASTIC: ("Be witty and sarcastic while staying helpful. No follow-ups."),
    AskMode.CREATIVE: (
        "Use metaphors and analogies. "
        "Think creatively while staying accurate. No follow-ups."
    ),
    AskMode.FRIENDLY: (
        "Be warm and conversational, like talking to a friend. No follow-ups."
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
        ollama_host = os.getenv("OLLAMA_HOST")
        if ollama_host:
            return ollama.Client(host=ollama_host)
        return ollama.Client()

    def _get_async_ollama_client(self) -> ollama.AsyncClient:
        """Get async Ollama client instance.

        Returns:
            ollama.AsyncClient: The async Ollama client.
        """
        ollama_host = os.getenv("OLLAMA_HOST")
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

    def get_system_prompt(self, mode: str = AskMode.CONCISE) -> str:
        """Get the system prompt for a given mode.

        Args:
            mode (str): The response mode (concise, professional, etc.).
                Defaults to AskMode.CONCISE.

        Returns:
            str: The system prompt for the specified mode.
        """
        return MODE_PROMPTS.get(mode, MODE_PROMPTS[AskMode.CONCISE])

    async def generate_text(
        self, model: str, prompt: str, system_prompt: str = ""
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
        return await self.async_ollama_client.generate(model=model, prompt=prompt)


# Singleton instance
core_service = CoreService()
