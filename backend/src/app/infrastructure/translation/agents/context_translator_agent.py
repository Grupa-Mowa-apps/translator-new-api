from typing import Any
from app.infrastructure.translation.agents.base_agent import BaseLLMAgent


class ContextTranslatorAgent(BaseLLMAgent):
    def build_messages(self, **kwargs) -> list[dict[str, Any]]:
        paragraphs: list[str] = kwargs["paragraphs"]
        genre: str = kwargs["genre"]

        joined = "\n\n".join(paragraphs)

        return [
            {
                "role": "developer",
                "content": (
                    "Jesteś profesjonalnym tłumaczem z polskiego na amerykański angielski (US English). "
                    "Twoje zadanie: wykonywać wierne, literalne tłumaczenia 1:1.\n\n"
                    "Zasady:\n"
                    "- Nie parafrazuj, nie interpretuj, nie upraszczaj.\n"
                    "- Zachowaj dokładny sens, styl i ton oryginału.\n"
                    "- Nie dodawaj ani nie usuwaj żadnych informacji.\n"
                    "- Cytaty w cudzysłowach (\"\", '', “”, „”, ‚’, ‘’, «», »«, ‹›) zostaw nietknięte. "
                    "Nie zmieniaj też cudzysłowów.\n"
                    "- Przypisy w formacie [^numer] pozostaw bez zmian w treści i miejscu.\n"
                    "- Bardzo krótkie elementy (tytuły, nazwiska) – zostaw bez zmian lub przetłumacz dosłownie.\n"
                    "- Specjalistyczne terminy z podanych dziedzin oznacz <u> w HTML – niczego innego nie formatuj.\n"
                    "- Niektóre cytaty zostały zastąpione wyrażeniami \"QUOTEno\" - bezwzględnie nie zmieniaj ich oraz ich formatowania.\n\n"
                ),
            },
            {
                "role": "user",
                "content": (
                    "Przetłumacz poniższe akapity zgodnie z zasadami.\n"
                    "Nie zmieniaj żadnej innej struktury lub formatowania (w szczególności tytułów, przypisów (oznaczonych jako [^numer]), cytatów).\n\n"
                    f"Dziedziny: {genre}\n\n"
                    f"TEKST:\n{joined}"
                ),
            },
        ]