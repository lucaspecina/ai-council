import asyncio
from openai import AsyncAzureOpenAI
from council.config import Settings


class LLMClient:
    """Unified async LLM client for Azure AI Foundry with retry + rate limiting."""

    def __init__(self, settings: Settings):
        self.client = AsyncAzureOpenAI(
            azure_endpoint=settings.azure_endpoint.rstrip("/"),
            api_key=settings.azure_api_key,
            api_version=settings.azure_api_version,
        )
        self.semaphore = asyncio.Semaphore(settings.max_concurrent)

    async def chat(
        self,
        model: str,
        messages: list[dict],
        max_tokens: int = 4000,
        max_retries: int = 3,
        timeout: float = 120.0,
    ) -> str:
        last_error = None

        for attempt in range(max_retries):
            try:
                async with self.semaphore:
                    response = await asyncio.wait_for(
                        self.client.chat.completions.create(
                            model=model,
                            messages=messages,
                            max_completion_tokens=max_tokens,
                        ),
                        timeout=timeout,
                    )
                return response.choices[0].message.content
            except Exception as e:
                last_error = e
                if attempt < max_retries - 1:
                    await asyncio.sleep(2**attempt)

        raise RuntimeError(f"LLM call failed after {max_retries} retries: {last_error}")

    async def close(self):
        await self.client.close()
