# ✅ Aplikacja uruchomiona w Docker z debuggerem

## Status
- ✅ Kontenery uruchomione
- ✅ PostgreSQL działa (port 5432)
- ✅ Backend działa (port 8000)
- ✅ Debugpy działa (port 5678)
- ✅ pgAdmin działa (port 5050)

## Szybki start

### 1. Uruchom aplikację
```bash
docker-compose up -d
```

### 2. Uruchom migracje (pierwsza instalacja)
```bash
docker-compose exec backend alembic upgrade head
```

### 3. Testuj API
```bash
curl http://localhost:8000/users
```

### 4. Debuguj w PyCharm

**Krok po kroku:**

1. W PyCharm wybierz konfigurację **"Docker Remote Debug"** (prawy górny róg)
2. Ustaw breakpoint w pliku `backend/src/app/api/http/controllers/users_controller.py` (np. linia 45)
3. Kliknij ikonę debugowania (zielony robak) lub naciśnij **Shift+F9**
4. Wykonaj request: `curl http://localhost:8000/users`
5. Debugger zatrzyma się na breakpoincie! 🎉

## Przydatne komendy

```bash
# Status kontenerów
docker-compose ps

# Logi backendu
docker-compose logs backend --tail=50

# Restart backendu
docker-compose restart backend

# Zatrzymanie wszystkich kontenerów
docker-compose down

# Przebudowanie i uruchomienie
docker-compose up -d --build
```

## Porty

| Serwis | Port | URL |
|--------|------|-----|
| Backend API | 8000 | http://localhost:8000 |
| Debugpy | 5678 | localhost:5678 |
| PostgreSQL | 5432 | localhost:5432 |
| pgAdmin | 5050 | http://localhost:5050 |

## Więcej informacji

Zobacz [DEBUG_DOCKER.md](DEBUG_DOCKER.md) dla szczegółowej dokumentacji debugowania.

## Test debugera

Użyj skryptu testowego:
```bash
./test_debugger.sh
```
