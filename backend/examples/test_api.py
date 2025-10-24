"""
Example usage script for the Byte in Bottle API.
"""

import httpx
import asyncio


async def test_api():
    """Test the Byte in Bottle API endpoints."""
    base_url = "http://localhost:8000"

    async with httpx.AsyncClient() as client:
        # Test health endpoint
        print("🔍 Testing health endpoint...")
        response = await client.get(f"{base_url}/health")
        print(f"Health: {response.json()}\n")

        # Test root endpoint
        print("🔍 Testing root endpoint...")
        response = await client.get(f"{base_url}/")
        print(f"Root: {response.json()}\n")

        # Test list models
        print("🔍 Listing available models...")
        try:
            response = await client.get(f"{base_url}/models")
            models = response.json()
            print(f"Available models: {len(models)}")
            for model in models:
                print(f"  - {model['name']}")
            print()
        except Exception as e:
            print(f"Error listing models: {e}\n")

        # Test chat endpoint
        print("🔍 Testing chat endpoint...")
        try:
            chat_request = {
                "model": "llama3.2",
                "messages": [{"role": "user", "content": "Say hello in one sentence!"}],
            }
            response = await client.post(f"{base_url}/chat", json=chat_request)
            result = response.json()
            print(f"Chat response: {result['message']['content']}\n")
        except Exception as e:
            print(f"Error in chat: {e}\n")

        # Test generate endpoint
        print("🔍 Testing generate endpoint...")
        try:
            response = await client.post(
                f"{base_url}/generate", params={"model": "llama3.2", "prompt": "Hi!"}
            )
            result = response.json()
            print(f"Generate response: {result['response']}\n")
        except Exception as e:
            print(f"Error in generate: {e}\n")


if __name__ == "__main__":
    print("🍾 Byte in Bottle API Test")
    print("Powered by bytes. Driven by attitude.\n")
    asyncio.run(test_api())
