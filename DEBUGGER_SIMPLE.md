# Debugowanie w PyCharm - Proste rozwiązanie

## Metoda 1: Debugowanie lokalne (ZALECANE)

Zamiast debugować w Dockerze, uruchom aplikację lokalnie:

### 1. Zatrzymaj kontener backend
```bash
docker-compose stop backend
```

### 2. Uruchom tylko bazę danych
```bash
docker-compose up -d postgres
```

### 3. Zaktualizuj `.env` dla lokalnego uruchomienia
```bash
cd backend
# Zmień w .env:
# DATABASE_URL=postgresql://admin:root@localhost:5432/translator_db
```

### 4. W PyCharm:
1. Otwórz `backend/src/app/run.py`
2. Kliknij prawym na plik → **Debug 'run'**
3. Ustaw breakpoint w `users_controller.py`
4. Wykonaj: `curl http://localhost:8000/users`

**Gotowe!** Debugger działa natywnie bez żadnej dodatkowej konfiguracji.

---

## Metoda 2: Debugowanie w Dockerze (zaawansowane)

Jeśli koniecznie chcesz debugować w Dockerze, potrzebujesz PyCharm Professional z obsługą Docker.

### W PyCharm Professional:

1. **Run → Edit Configurations...**
2. **+ → Python**
3. Ustaw:
   - **Script path:** `/app/backend/src/app/run.py`
   - **Python interpreter:** Wybierz Docker Compose (backend service)
   - **Environment variables:** Skopiuj z docker-compose.yml

---

## Zalecenie

**Użyj Metody 1** - jest prostsza i działa identycznie. Docker używaj tylko do bazy danych.
