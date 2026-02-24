# 🚀 Od Developmentu do Produkcji

Krótki przewodnik jak działa deployment w tym projekcie.

## 1. Lokalny Development

Pracujesz na swoim komputerze:

```bash
docker-compose up
```

To uruchamia:
- **PostgreSQL** (baza danych) - port 5432
- **Backend** (API) - port 8000
- **PgAdmin** (zarządzanie bazą) - port 5050

Wszystko jest w kontenerach, ale masz dostęp do kodu na dysku (hot reload).

## 2. Push do GitHub

Kiedy pushasz kod na branch (nie `main`):

```bash
git push origin feature/moja-funkcja
```

**GitHub Actions automatycznie:**
1. Buduje Docker image backendu i nginx'a
2. Pushuje je do GitHub Container Registry (GHCR)
3. Taguje je nazwą brancha (np. `feature-moja-funkcja-latest`)

Możesz zobaczyć status w zakładce "Actions" na GitHubie.

## 3. Deploy na TEST

Kiedy chcesz przetestować na serwerze testowym:

1. Idź do GitHub → Actions → "🚀 Deploy to TEST"
2. Kliknij "Run workflow"
3. Wybierz środowisko: `test_env_01` lub `test_env_02`
4. Czekaj ~2 minuty

**Co się dzieje:**
- Pobiera najnowszy image z Twojego brancha
- Uruchamia go na VPS-ie na porcie 3001 lub 3002
- Baza danych jest osobna dla każdego środowiska

**Dostęp:**
- Frontend: `http://vps-ip:3001` (lub 3002)
- API: `http://vps-ip:3001/api`

## 4. Release do PRODUKCJI

Kiedy kod jest gotowy do produkcji:

### Krok 1: Merge do `main`

```bash
git checkout main
git pull
git merge feature/moja-funkcja
git push origin main
```

### Krok 2: Utwórz release commit

```bash
git commit --allow-empty -m "release/1.2.3"
git push origin main
```

**GitHub Actions automatycznie:**
1. Buduje image z tagu wersji (np. `1.2.3-prod`)
2. Tworzy GitHub Release
3. Czeka na Twój sygnał do deploymentu

### Krok 3: Deploy na PROD

1. Idź do GitHub → Actions → "🧱 Deploy Production Container"
2. Kliknij "Run workflow"
3. Czekaj ~2 minuty

**Co się dzieje:**
- Pobiera najnowszy release image
- Uruchamia go na VPS-ie na porcie 3000
- Baza danych jest osobna dla produkcji

**Dostęp:**
- Frontend: `http://vps-ip:3000`
- API: `http://vps-ip:3000/api`

## 5. Struktura Dockerów

### `Dockerfile.backend` (dev)
- Python 3.11
- Instaluje zależności
- Uruchamia migracje bazy
- Startuje API

### `Dockerfile.backend.prod` (prod)
- Identyczny jak dev (optymalizacja może być później)

### `Dockerfile.nginx`
- Buduje frontend (React)
- Serwuje statyczne pliki
- Proxy do backendu na `/api`

### `docker-entrypoint.sh`
- Czeka aż baza będzie gotowa
- Uruchamia migracje Alembic
- Startuje uvicorn

## 6. Zmienne środowiskowe

### Dev (docker-compose.yml)
```
POSTGRES_HOST=postgres
POSTGRES_USER=admin
POSTGRES_PASSWORD=root
```

### Prod (docker-compose.prod.yml)
- Takie same, ale na VPS-ie
- Przechowywane w GitHub Secrets

## 7. Troubleshooting

**Port zajęty?**
```bash
lsof -i :8000
kill -9 <PID>
```

**Baza nie startuje?**
```bash
docker-compose down -v  # usuwa volume z danymi
docker-compose up
```

**Migracje nie działają?**
```bash
docker-compose exec backend alembic upgrade head
```

**Chcesz zobaczyć logi?**
```bash
docker-compose logs -f backend
docker-compose logs -f postgres
```

## 8. Workflow w skrócie

```
Feature branch → Push → Auto build → Deploy TEST → Merge main → Release commit → Auto build → Deploy PROD
```

Tyle! 🎉
