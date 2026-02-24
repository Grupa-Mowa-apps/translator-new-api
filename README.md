# translator-new-api

Aplikacja do tłumaczenia dokumentów z backendem Python/FastAPI i frontendem React/TypeScript.

## Struktura projektu

- **backend/** - API (FastAPI, SQLAlchemy, Alembic)
- **frontend/** - UI (React, TypeScript, Vite)
- **tests/** - Testy jednostkowe i integracyjne
- **docker-compose.yml** - Konfiguracja dla lokalnego developmentu

## Setup

```bash
# Backend
cd backend
pip install -r ../requirements.txt
python -m uvicorn src.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## Docker

```bash
docker-compose up
```

## Testy

```bash
pytest tests/
```

## Architektura

Backend wykorzystuje architekturę heksagonalną:
- **domain/** - Logika biznesowa, encje, serwisy
- **application/** - Komendy, zapytania, DTO
- **infrastructure/** - Implementacje portów (baza danych, LLM, pliki)
- **api/http/** - Endpointy REST

Frontend:
- **src/components/** - Komponenty React
- **src/pages/** - Strony aplikacji
- **src/services/** - Komunikacja z API

## Zmienne środowiskowe

Backend (`.env`):
```
DATABASE_URL=postgresql://...
LLM_API_KEY=...
```

Frontend (`.env`):
```
VITE_API_URL=http://localhost:8000
```

## Workflow developmentu

1. Utwórz branch: `git checkout -b feature/nazwa`
2. Implementuj zmiany
3. Uruchom testy: `pytest tests/`
4. Commituj: `git commit -m "feat: opis"`
5. Push i utwórz PR

## Troubleshooting

- **Port 8000 zajęty**: `lsof -i :8000` i zabij proces
- **Migracje bazy**: `alembic upgrade head`
- **Czyszczenie cache**: `rm -rf node_modules && npm install`
