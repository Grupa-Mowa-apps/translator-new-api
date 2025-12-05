from typing import Optional

import openai
from openai import APIError, APITimeoutError, RateLimitError, APIConnectionError

from app.domain.ports.llm_completion import LLMCompletionPort
from app.setup.config.settings import OPENAI_API_KEY, LLM_MODEL
from app.domain.errors import LLMErrors

class LLMCompletionAdapter(LLMCompletionPort):
    def __init__(self, api_key: str = OPENAI_API_KEY, default_model: str = LLM_MODEL):
        self.client = openai.Client(api_key=api_key)
        self.default_model = default_model

    def create_completion(self, messages: list[dict[str, any]], model: Optional[str] = None) -> dict[str, any]:
        used_model = model or self.default_model

        try:
            response = self.client.chat.completions.create(model=used_model, messages=messages)

            return response.model_dump()
        
        except (RateLimitError, APITimeoutError, APIConnectionError, APIError) as e:
            raise RuntimeError(f"{LLMErrors.LLM_REQUEST_FAILED}: {e}") from e