from app.domain.errors import TranslationTaskErrors
from app.domain.ports.llm_completion import LLMCompletionPort
from app.domain.ports.translation_port import TranslationPort
from app.infrastructure.translation.agents.active_voice_agent import ActiveVoiceAgent
from app.infrastructure.translation.agents.context_translator_agent import ContextTranslatorAgent
from app.infrastructure.translation.agents.senior_editor_agent import SeniorEditorAgent


class TranslationAdapter(TranslationPort):
    def __init__(self, llm: LLMCompletionPort):
        self._context_translator = ContextTranslatorAgent(llm=llm)
        self._senior_editor = SeniorEditorAgent(llm=llm)
        self._active_voice = ActiveVoiceAgent(llm=llm)

    def translate_batch(self, paragraphs: list[str], genre: str) -> list[str]:
        if not paragraphs:
            return []
        return self._context_translator.run(paragraphs=paragraphs, genre=genre)
    
    def improve_batch(self, original_paragraphs: list[str], draft_translations: list[str], genre: str) -> list[str]:
        if not original_paragraphs:
            return []
        if len(original_paragraphs) != len(draft_translations):
            raise ValueError(TranslationTaskErrors.INVALID_LENGTH_OF_ORIGINAL_AND_DRAFT_TRANSLATIONS_PARAGRAPHS)
        
        return self._senior_editor.run(
            original_paragraphs=original_paragraphs,
            draft_translations=draft_translations,
            genre=genre,
        )
    
    def apply_active_voice_batch(self, paragraphs: list[str]) -> list[str]:
        if not paragraphs:
            return []
        
        return self._active_voice.run(paragraphs=paragraphs)