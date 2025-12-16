# Wytyczne Review Architektonicznego

## Spis treści
1. [Cel i zakres](#cel-i-zakres)
2. [Kiedy przeprowadzać review architektoniczne](#kiedy-przeprowadzać-review-architektoniczne)
3. [Checklist warstw aplikacji](#checklist-warstw-aplikacji)
4. [Zasady SOLID](#zasady-solid)
5. [Wzorce projektowe](#wzorce-projektowe)
6. [Coupling i Cohesion](#coupling-i-cohesion)
7. [Skalowalność i wydajność](#skalowalność-i-wydajność)
8. [Testowalność](#testowalność)
9. [Bezpieczeństwo architektoniczne](#bezpieczeństwo-architektoniczne)
10. [Red Flags - sygnały ostrzegawcze](#red-flags---sygnały-ostrzegawcze)
11. [Dokumentacja decyzji architektonicznych](#dokumentacja-decyzji-architektonicznych)

---

## Cel i zakres

### Cel Review Architektonicznego
- **Spójność**: Zapewnienie zgodności z przyjętą architekturą projektu
- **Skalowalność**: Ocena czy rozwiązanie będzie skalowalne w przyszłości
- **Utrzymywalność**: Weryfikacja łatwości wprowadzania zmian i rozszerzeń
- **Separacja odpowiedzialności**: Sprawdzenie czy komponenty mają jasno zdefiniowane role

### Różnica między Code Review a Architecture Review
| Aspekt | Code Review | Architecture Review |
|--------|-------------|---------------------|
| Fokus | Jakość kodu, styl, błędy | Struktura, zależności, wzorce |
| Poziom | Linie kodu, funkcje | Moduły, warstwy, komponenty |
| Pytanie | "Czy to działa poprawnie?" | "Czy to jest dobrze zaprojektowane?" |

---

## Kiedy przeprowadzać review architektoniczne

### Obowiązkowe review architektoniczne:
- [ ] Dodanie nowego modułu/pakietu
- [ ] Wprowadzenie nowej zależności zewnętrznej
- [ ] Zmiana w warstwie domain (encje, porty)
- [ ] Nowy adapter infrastrukturalny
- [ ] Zmiana przepływu danych między warstwami
- [ ] Refaktoryzacja struktury projektu

### Opcjonalne (ale zalecane):
- [ ] Duże PR (>500 linii)
- [ ] Zmiany w więcej niż 3 modułach jednocześnie
- [ ] Nowa integracja z zewnętrznym systemem

---

## Checklist warstw aplikacji

### Warstwa Domain (`domain/`)

#### Encje (`domain/entities/`)
- [ ] Czy encja reprezentuje koncept biznesowy?
- [ ] Czy encja jest niezależna od infrastruktury (brak ORM, HTTP)?
- [ ] Czy zawiera logikę biznesową, nie tylko dane?
- [ ] Czy walidacja jest w encji, nie w kontrolerze?
- [ ] Czy encja jest immutable gdzie to możliwe?

#### Porty (`domain/ports/`)
- [ ] Czy port definiuje interfejs (Protocol/ABC)?
- [ ] Czy port jest niezależny od konkretnej implementacji?
- [ ] Czy nazwy metod są domenowe (nie techniczne)?
- [ ] Czy port nie zawiera szczegółów implementacyjnych?

```python
# ❌ Źle - szczegóły techniczne w porcie
class UserRepository(Protocol):
    def execute_sql(self, query: str) -> List[dict]: ...

# ✅ Dobrze - język domenowy
class UserRepository(Protocol):
    def find_by_id(self, user_id: UserId) -> Optional[User]: ...
    def save(self, user: User) -> None: ...
```

#### Value Objects (`domain/value_objects/`)
- [ ] Czy obiekt jest immutable?
- [ ] Czy zawiera walidację w konstruktorze?
- [ ] Czy porównanie jest przez wartość, nie referencję?
- [ ] Czy nie ma setterów?

#### Serwisy domenowe (`domain/services/`)
- [ ] Czy serwis zawiera logikę, która nie pasuje do żadnej encji?
- [ ] Czy serwis jest bezstanowy?
- [ ] Czy nie duplikuje logiki z encji?

### Warstwa Application (`application/`)

#### Commands (`application/commands/`)
- [ ] Czy command reprezentuje jedną operację biznesową?
- [ ] Czy command modyfikuje stan (write operation)?
- [ ] Czy handler ma jedną odpowiedzialność?
- [ ] Czy zależności są wstrzykiwane przez konstruktor?

#### Queries (`application/queries/`)
- [ ] Czy query tylko odczytuje dane (read operation)?
- [ ] Czy nie modyfikuje stanu?
- [ ] Czy zwraca DTO, nie encję domenową?

#### DTOs (`application/dto/`)
- [ ] Czy DTO jest prostą strukturą danych?
- [ ] Czy nie zawiera logiki biznesowej?
- [ ] Czy jest używane do transferu między warstwami?

### Warstwa Infrastructure (`infrastructure/`)

#### Repozytoria (`infrastructure/db/repositories/`)
- [ ] Czy implementuje port z domain?
- [ ] Czy mapuje między encją domenową a modelem ORM?
- [ ] Czy nie wycieka ORM do warstwy application?
- [ ] Czy obsługuje transakcje poprawnie?

#### Adaptery
- [ ] Czy adapter implementuje port z domain?
- [ ] Czy szczegóły techniczne są ukryte za interfejsem?
- [ ] Czy jest łatwy do zastąpienia inną implementacją?

```python
# ❌ Źle - szczegóły LLM w warstwie application
class TranslateCommand:
    def execute(self):
        response = openai.ChatCompletion.create(...)  # Bezpośrednie użycie OpenAI

# ✅ Dobrze - użycie portu
class TranslateCommand:
    def __init__(self, llm_port: LLMCompletionPort):
        self.llm = llm_port
    
    def execute(self):
        response = self.llm.complete(prompt)  # Abstrakcja
```

### Warstwa API (`api/`)

#### Kontrolery (`api/http/controllers/`)
- [ ] Czy kontroler jest "cienki" (thin controller)?
- [ ] Czy deleguje logikę do warstwy application?
- [ ] Czy zajmuje się tylko HTTP (request/response)?
- [ ] Czy nie zawiera logiki biznesowej?

#### Schematy (`api/http/schemas/`)
- [ ] Czy schematy są używane do walidacji wejścia?
- [ ] Czy są oddzielne dla request i response?
- [ ] Czy mapują na/z DTO?

---

## Zasady SOLID

### Single Responsibility Principle (SRP)
- [ ] Czy klasa/moduł ma jeden powód do zmiany?
- [ ] Czy nazwa jasno opisuje odpowiedzialność?
- [ ] Czy klasa nie jest "god class" (>300 linii)?

### Open/Closed Principle (OCP)
- [ ] Czy można rozszerzyć funkcjonalność bez modyfikacji istniejącego kodu?
- [ ] Czy używane są abstrakcje (Protocol, ABC)?

### Liskov Substitution Principle (LSP)
- [ ] Czy podklasy mogą zastąpić klasy bazowe bez zmiany zachowania?
- [ ] Czy nie ma "refused bequest" (puste implementacje)?

### Interface Segregation Principle (ISP)
- [ ] Czy interfejsy są małe i fokusowane?
- [ ] Czy klient nie musi implementować metod, których nie używa?

### Dependency Inversion Principle (DIP)
- [ ] Czy moduły wysokopoziomowe nie zależą od niskopoziomowych?
- [ ] Czy zależności są wstrzykiwane, nie tworzone wewnątrz?
- [ ] Czy używane są abstrakcje (porty), nie implementacje?

---

## Wzorce projektowe

### Wzorce używane w projekcie

#### Repository Pattern
- [ ] Czy repozytoria ukrywają mechanizm persystencji?
- [ ] Czy interfejs jest domenowy?
- [ ] Czy nie ma "leaky abstraction"?

#### Command/Query Separation (CQS)
- [ ] Czy commands tylko modyfikują stan?
- [ ] Czy queries tylko odczytują dane?
- [ ] Czy nie ma mieszania operacji?

#### Dependency Injection
- [ ] Czy zależności są wstrzykiwane przez konstruktor?
- [ ] Czy jest możliwość łatwej podmiany implementacji?
- [ ] Czy nie ma `new` wewnątrz klas biznesowych?

#### Factory Pattern (gdy potrzebny)
- [ ] Czy tworzenie złożonych obiektów jest wydzielone?
- [ ] Czy factory ukrywa szczegóły konstrukcji?

### Anti-patterns do wykrycia
- [ ] **Service Locator** - ukryte zależności
- [ ] **God Class** - klasa wie/robi za dużo
- [ ] **Anemic Domain Model** - encje bez logiki
- [ ] **Feature Envy** - metoda używa więcej danych innej klasy
- [ ] **Shotgun Surgery** - zmiana wymaga edycji wielu plików

---

## Coupling i Cohesion

### Low Coupling (niskie sprzężenie)
- [ ] Czy moduły są niezależne od siebie?
- [ ] Czy zmiana w jednym module nie wymaga zmian w innych?
- [ ] Czy zależności są przez abstrakcje (interfejsy)?

### High Cohesion (wysoka spójność)
- [ ] Czy elementy modułu są powiązane funkcjonalnie?
- [ ] Czy moduł realizuje jeden spójny cel?
- [ ] Czy nie ma "utility" klas z niepowiązanymi metodami?

### Metryki do sprawdzenia
```
Afferent Coupling (Ca) - ile modułów zależy od tego modułu
Efferent Coupling (Ce) - od ilu modułów ten moduł zależy
Instability = Ce / (Ca + Ce) - 0 = stabilny, 1 = niestabilny
```

### Zasada kierunku zależności
```
API → Application → Domain ← Infrastructure
          ↓              ↑
    zależy od      implementuje
```

---

## Skalowalność i wydajność

### Pytania architektoniczne
- [ ] Czy rozwiązanie będzie działać przy 10x większym ruchu?
- [ ] Czy można łatwo dodać caching?
- [ ] Czy są wąskie gardła (single point of failure)?
- [ ] Czy operacje I/O są asynchroniczne gdzie potrzeba?

### Baza danych
- [ ] Czy nie ma N+1 queries?
- [ ] Czy indeksy są odpowiednie?
- [ ] Czy transakcje są krótkie?
- [ ] Czy jest strategia na dużą ilość danych?

### Zewnętrzne zależności
- [ ] Czy jest obsługa timeout?
- [ ] Czy jest retry logic?
- [ ] Czy jest circuit breaker (dla krytycznych integracji)?
- [ ] Czy awaria zależności nie powala całej aplikacji?

---

## Testowalność

### Checklist testowalności
- [ ] Czy komponenty można testować w izolacji?
- [ ] Czy zależności można łatwo mockować?
- [ ] Czy nie ma ukrytych zależności (globals, singletons)?
- [ ] Czy logika biznesowa jest oddzielona od I/O?

### Piramida testów
```
        /\
       /  \   E2E (mało)
      /----\
     /      \  Integration (średnio)
    /--------\
   /          \ Unit (dużo)
  /------------\
```

- [ ] Czy proporcje testów są odpowiednie?
- [ ] Czy domain jest dobrze pokryte unit testami?
- [ ] Czy są testy integracyjne dla repozytoriów?

---

## Bezpieczeństwo architektoniczne

### Granice zaufania
- [ ] Czy dane z zewnątrz są walidowane na granicy (API)?
- [ ] Czy nie ma SQL injection, XSS, etc.?
- [ ] Czy secrets nie są w kodzie?

### Autoryzacja
- [ ] Czy jest sprawdzane kto może wykonać operację?
- [ ] Czy autoryzacja jest w warstwie application (nie API)?
- [ ] Czy nie ma "insecure direct object reference"?

### Audit
- [ ] Czy krytyczne operacje są logowane?
- [ ] Czy logi nie zawierają wrażliwych danych?

---

## Red Flags - sygnały ostrzegawcze

### 🚩 Natychmiastowa interwencja
- Import z `infrastructure` w `domain`
- Logika biznesowa w kontrolerze
- Bezpośrednie użycie ORM w warstwie application
- Hardcodowane URL-e, klucze API
- Cykliczne zależności między modułami

### ⚠️ Do dyskusji
- Klasa >300 linii
- Metoda >50 linii
- Więcej niż 5 parametrów w funkcji
- Głębokie zagnieżdżenie (>3 poziomy)
- Komentarze tłumaczące "co" zamiast "dlaczego"

### 💡 Sugestie
- Brak docstringów w publicznym API
- Nieużywane importy/zmienne
- Magic numbers bez stałych
- Duplikacja kodu między modułami

---

## Dokumentacja decyzji architektonicznych

### Architecture Decision Records (ADR)
Dla ważnych decyzji architektonicznych twórz ADR:

```markdown
# ADR-001: Użycie hexagonal architecture

## Status
Accepted

## Context
Potrzebujemy architektury, która pozwoli na łatwą wymianę infrastruktury...

## Decision
Stosujemy hexagonal architecture z podziałem na domain, application, infrastructure, api.

## Consequences
+ Łatwa testowalność
+ Niezależność od frameworka
- Więcej boilerplate'u
- Krzywa uczenia się dla nowych developerów
```

### Gdzie dokumentować
- `/docs/adr/` - Architecture Decision Records
- `/docs/diagrams/` - Diagramy architektury
- `README.md` - Przegląd wysokopoziomowy

---

## Podsumowanie - Quick Reference

### Przed zatwierdzeniem PR sprawdź:

```
✅ Domain nie importuje z infrastructure
✅ Application używa portów, nie implementacji
✅ Kontrolery są "cienkie"
✅ Encje zawierają logikę biznesową
✅ Zależności są wstrzykiwane
✅ Nowe moduły są w odpowiednim miejscu
✅ Wzorce projektu są respektowane
✅ Brak red flags
```

---

*Dokument wersja 1.0 | Data: 2025-12-10*

