from typing import Any
from app.infrastructure.translation.agents.base_agent import BaseLLMAgent


class ActiveVoiceAgent(BaseLLMAgent):
    def build_messages(self, **kwargs) -> list[dict[str, Any]]:
        paragraphs: list[str] = kwargs["paragraphs"]

        return [
            {
                "role": "system",
                "content": (
                    "You are an American editor specializing in converting passive voice to active voice while ensuring *absolute fidelity* to the original text.\n\n"
                    "Rules:\n"
                    "- Convert only passive constructions to active voice if this can be done naturally without changing meaning.\n"
                    "- If the paragraph is already in active voice, leave it unchanged.\n"
                    "- Never place a pronoun at the end of a sentence.\n"
                    "- NEVER add, remove, summarize, interpret, or rephrase content beyond the passive/active change.\n"
                    "- Do not replace words with synonyms unless absolutely unavoidable for grammar.\n"
                    "- Quotes in quotation marks (\"\", '', “”, „”, ‚’, ‘’, «», »«, ‹›) must remain untouched and unedited (both quotes and quotatiom marks)..\n"
                    "- Footnotes in [^number] format must remain exactly in place and unaltered.\n"
                    "- Very short elements (headings, titles, names) must remain untouched.\n"
                    "- Do not change the logical flow, length, or structure except strictly for passive-to-active conversion."
                    "- Some quotes are replaced with \"QUOTEno\" expressions - absolutely do not change them and their formatting.\n\n"
                    "- Do not add any comments or notes. Return only the final edited paragraph."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Rewrite the following paragraphs by converting passive voice into active voice if applicable, according to the above rules."
                ),
            },
            {"role": "user", "content": f"Paragraphs (list): {paragraphs}"},
        ]
