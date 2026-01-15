# Debugowanie aplikacji w Docker

## Konfiguracja

Aplikacja jest skonfigurowana do debugowania zdalnego przez debugpy na porcie 5678.

## Jak używać debugera w PyCharm

### 1. Uruchom kontenery Docker
```bash
docker-compose up -d
```

### 2. Sprawdź czy kontenery działają
```bash
docker-compose ps
```

### 3. Uruchom migracje (jeśli potrzeba)
```bash
docker-compose exec backend alembic upgrade head
```

### 4. Podłącz debugger w PyCharm

1. Otwórz PyCharm
2. Wybierz konfigurację **"Docker Remote Debug"** z listy konfiguracji (prawy górny róg)
3. Kliknij ikonę debugowania (zielony robak) lub naciśnij Shift+F9
4. Debugger powinien się podłączyć do kontenera

### 5. Ustaw breakpointy

Ustaw breakpoint w dowolnym miejscu kodu, np.:
- `backend/src/app/api/http/controllers/users_controller.py` - linia 45 (funkcja list_users)
- `backend/src/app/application/queries/list_users.py` - w metodzie run()

### 6. Wykonaj request

```bash
curl http://localhost:8000/users
```

lub użyj skryptu testowego:
```bash
./test_debugger.sh
```

### 7. Debuguj!

Gdy request trafi do kodu z breakpointem, debugger zatrzyma wykonanie i będziesz mógł:
- Sprawdzać wartości zmiennych
- Wykonywać kod krok po kroku (F8 - Step Over, F7 - Step Into)
- Oceniać wyrażenia w konsoli debugera
- Modyfikować wartości zmiennych

## Porty

- **8000** - FastAPI (HTTP)
- **5678** - debugpy (Remote Debug)
- **5432** - PostgreSQL
- **5050** - pgAdmin

## Mapowanie ścieżek

- Local: `$PROJECT_DIR$/backend`
- Remote: `/app/backend`

## Troubleshooting

### Debugger się nie podłącza
1. Sprawdź czy kontener działa: `docker-compose ps`
2. Sprawdź logi: `docker-compose logs backend`
3. Sprawdź czy port 5678 jest otwarty: `docker-compose port backend 5678`

### Breakpointy nie działają
1. Upewnij się, że mapowanie ścieżek jest poprawne
2. Sprawdź czy plik jest w wolumenie (backend/)
3. Zrestartuj kontenery: `docker-compose restart backend`

### Aplikacja nie odpowiada
1. Sprawdź logi: `docker-compose logs backend --tail=50`
2. Sprawdź czy baza danych działa: `docker-compose logs postgres`
3. Uruchom migracje: `docker-compose exec backend alembic upgrade head`

## Zatrzymanie kontenerów

```bash
docker-compose down
```

## Restart kontenerów

```bash
docker-compose restart backend
```

## Przebudowanie obrazów

```bash
docker-compose up -d --build
```
