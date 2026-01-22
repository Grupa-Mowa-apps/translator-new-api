from abc import ABC, abstractmethod
import json
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
        return self._extract_translation_json(data=data)
    
    def _extract_translation_list(self, data: dict[str, Any]) -> list[str]:
        """Converts raw content to a list of strings"""
        content = self._extract_content(data=data)

        try:
            translations = json.loads(content)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"{LLMErrors.NO_JSON_OUTPT}: {content[:300]}") from e
        
        if not isinstance(translations, list) or not all(isinstance(x, str) for x in translations):
            raise RuntimeError(f"{LLMErrors.INVALID_JSON_STRUCTURE}")
        
        return translations

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