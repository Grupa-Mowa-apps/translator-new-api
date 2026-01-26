from abc import ABC, abstractmethod
import json
import re
from typing import Any

from app.domain.errors import LLMErrors
from app.domain.ports.llm_completion import LLMCompletionPort
from app.setup.config.settings import LLM_MODEL

class BaseLLMAgent(ABC):
    def __init__(self, llm: LLMCompletionPort, model: str = LLM_MODEL):
        self.llm = llm
        self.model = model

    @abstractmethod
    def build_messages(self, **kwargs: Any) -> list[dict[str, Any]]:
        """Return OpenAI chat messages"""
        raise NotImplementedError
    
    def run(self, **kwargs: Any) -> list[str]:
        """Main method to run an agent"""
        messages = self.build_messages(**kwargs)
        data = self.llm.create_completion(messages=messages, model=self.model)
        content = self._extract_content(data=data)

        parts = [p.strip() for p in re.split(r"\n\s*\n", content.strip())]
        return parts

    def _extract_content(self, data: dict[str, Any]) -> str:
        """Extracts raw strings from JSON from OpenAI response"""

        choices = data.get("choices")
        if not choices:
            raise RuntimeError(f"{LLMErrors.NO_CHOICES_IN_LLM_RESPONSE}: {data}")
        
        message = choices[0].get("message")
        if not message:
            raise RuntimeError(f"{LLMErrors.NO_MESSAGE_IN_FIRST_CHOICE}: {choices[0]}")
        
        content = message.get("content")
        if content is None:
            raise RuntimeError(f"{LLMErrors.NO_CONTENT_IN_MESSAGE}: {message}")
        
        return content