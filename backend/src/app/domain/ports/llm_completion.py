from typing import Any, Dict, List, Optional, Protocol
from app.setup.config.settings import LLM_MODEL

class LLMCompletionPort(Protocol):
    def create_completion(
        self, 
        messages: List[Dict[str, Any]], 
        model=LLM_MODEL,
    ) -> Dict[str, Any]: 
        ...