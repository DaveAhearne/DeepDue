from typing import Callable, Awaitable, TypedDict
from litellm import acompletion
from deepdue.config import settings

LLMClient = Callable[[list[dict], float, dict], Awaitable[str]]

class LLMClients(TypedDict):
    extraction: LLMClient
    reasoning: LLMClient
    synthesis: LLMClient

def make_llm_client(model: str) -> LLMClient:
    async def complete(messages: list[dict], temperature: float = 0.0, meta: dict | None = None) -> str:
        response = await acompletion(
            model=f"{settings.llm_provider}/{model}",
            messages=messages,
            api_base=settings.llm_base_url,
            temperature=temperature,
            max_tokens=None,
            metadata = meta or {},
        )
        return response.choices[0].message.content

    return complete

def make_llm_clients() -> LLMClients:
    return {
        "extraction": make_llm_client(settings.llm_extraction_model),
        "reasoning": make_llm_client(settings.llm_reasoning_model),
        "synthesis": make_llm_client(settings.llm_synthesis_model),
    }