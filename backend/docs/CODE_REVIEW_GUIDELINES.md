# Wytyczne Code Review

## Spis treści
1. [Cel i zakres](#cel-i-zakres)
2. [Kiedy przeprowadzać code review](#kiedy-przeprowadzać-code-review)
3. [Checklist code review](#checklist-code-review)
4. [Jakość kodu](#jakość-kodu)
5. [Czytelność i styl](#czytelność-i-styl)
6. [Bezpieczeństwo](#bezpieczeństwo)
7. [Wydajność](#wydajność)
8. [Testy](#testy)
9. [Git i commity](#git-i-commity)
10. [Red Flags - sygnały ostrzegawcze](#red-flags---sygnały-ostrzegawcze)
11. [Kultura code review](#kultura-code-review)

---

## Cel i zakres

### Cel Code Review
- **Jakość**: Zapewnienie wysokiej jakości kodu
- **Błędy**: Wykrycie bugów przed produkcją
- **Wiedza**: Dzielenie się wiedzą w zespole
- **Spójność**: Utrzymanie jednolitego stylu
- **Nauka**: Rozwój umiejętności zespołu

### Różnica między Code Review a Architecture Review
| Aspekt | Code Review | Architecture Review |
|--------|-------------|---------------------|
| Fokus | Jakość kodu, styl, błędy | Struktura, zależności, wzorce |
| Poziom | Linie kodu, funkcje | Moduły, warstwy, komponenty |
| Pytanie | "Czy to działa poprawnie?" | "Czy to jest dobrze zaprojektowane?" |

---

## Kiedy przeprowadzać code review

### Obowiązkowe:
- [ ] Każdy Pull Request przed merge
- [ ] Zmiany w krytycznych modułach
- [ ] Nowy kod (nie refaktoring)

### Opcjonalne:
- [ ] Refaktoring (pair programming może wystarczyć)
- [ ] Dokumentacja

---

## Checklist code review

### Podstawowy checklist

#### 1. Funkcjonalność
- [ ] Czy kod robi to co powinien?
- [ ] Czy obsługuje edge cases?
- [ ] Czy obsługuje błędy poprawnie?

#### 2. Czytelność
- [ ] Czy kod jest zrozumiały?
- [ ] Czy nazwy są jasne i opisowe?
- [ ] Czy komentarze są potrzebne i aktualne?

#### 3. Testy
- [ ] Czy są testy dla nowego kodu?
- [ ] Czy testy przechodzą?

#### 4. Bezpieczeństwo
- [ ] Czy nie ma hardcodowanych secrets?
- [ ] Czy dane wejściowe są walidowane?

---

*Dokument wersja 1.0*
