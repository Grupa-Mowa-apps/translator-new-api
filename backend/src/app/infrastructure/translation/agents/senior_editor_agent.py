from typing import Any
from app.infrastructure.translation.agents.base_agent import BaseLLMAgent


class SeniorEditorAgent(BaseLLMAgent):
    def build_messages(self, **kwargs) -> list[dict[str, Any]]:
        original_paragraphs: list[str] = kwargs["original_paragraphs"]
        draft_translations: list[str] = kwargs["draft_translations"]
        genre: str = kwargs["genre"]

        return [
            {
                "role": "developer",
                "content": (
                    "Jesteś starszym redaktorem tłumaczeń z polskiego na amerykański angielski.\n"
                    "Twoje zadanie: poprawiać błędy w tłumaczeniach młodszych tłumaczy bez zmiany sensu ani stylu.\n\n"
                    "Zasady:\n"
                    "- Nie parafrazuj ani nie zmieniaj struktury bez błędu.\n"
                    "- Nie upraszczaj ani nie dodawaj/nie usuwaj informacji.\n"
                    "- Zachowaj znaczenie 1:1.\n"
                    "- Unikaj synonimów – chyba że obecne słowo jest błędne lub nienaturalne.\n"
                    "- Cytaty w cudzysłowach (\"\", '', “”, „”, ‚’, ‘’, «», »«, ‹›) zostaw nietknięte. Nie zmieniaj też cudzysłowów.\n"
                    "- Przypisy w formacie [^numer] pozostaw bez zmian w treści i miejscu.\n"
                    "- Bardzo krótkie elementy (tytuły, nazwiska) – zostaw bez zmian lub przetłumacz dosłownie.\n"
                    "- Zajmujesz się poprawnością podkreślonych terminów (w znacznikach podkreślenia w html <u>). Są to terminy należące do zdefiniowanych dziedzin."
                    "- Sprawdzaj <u>-oznaczone terminy. Jeśli masz lepsze tłumaczenie, dodaj po ukośniku w środku <u> (np. <u>term/better</u>).\n"
                    "- Niektóre cytaty zostały zastąpione wyrażeniami \"QUOTEno\" - bezwzględnie nie zmieniaj ich oraz ich formatowania.\n"
                    "- NIE dodajesz żadnych nowych przypisów ani komentarzy.\n\n"
                    "- Odpowiedź = gotowe poprawione tłumaczenie. Bez wyjaśnień."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Popraw poniższe tłumaczenia zgodnie z powyższymi zasadami.\n"
                    "Nie zmieniaj struktury tekstu, formatowania przypisów ani nie dodawaj nowych treści."
                ),
            },
            {"role": "user", "content": f"Dziedziny: {genre}"},
            {"role": "user", "content": f"Oryginały (lista): {original_paragraphs}"},
            {"role": "user", "content": f"Tłumaczenia robocze (lista): {draft_translations}"},
        ]