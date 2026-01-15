# 🎯 Debugowanie lokalne w PyCharm - GOTOWE!

## ✅ Konfiguracja zakończona

### Co zostało zrobione:
1. ✅ Backend zatrzymany w Dockerze
2. ✅ PostgreSQL działa w Dockerze (port 5432)
3. ✅ `.env` zaktualizowany na `localhost`

---

## 🚀 Jak debugować w PyCharm

### Krok 1: Otwórz plik do uruchomienia
W PyCharm otwórz: `backend/src/app/run.py`

### Krok 2: Uruchom w trybie debug
**Opcja A - Szybka:**
- Kliknij prawym przyciskiem na `run.py`
- Wybierz **"Debug 'run'"**

**Opcja B - Przez konfigurację:**
1. **Run → Edit Configurations...**
2. **+ → Python**
3. Ustaw:
   - **Name:** `Backend Local`
   - **Script path:** `backend/src/app/run.py`
   - **Working directory:** `backend/src`
   - **Environment variables:** `PYTHONPATH=backend/src`
4. Kliknij **OK** i uruchom debug (Shift+F9)

### Krok 3: Ustaw breakpoint
- Otwórz `backend/src/app/api/http/controllers/users_controller.py`
- Kliknij na marginesie przy linii 45 (funkcja `list_users`)

### Krok 4: Testuj!
```bash
curl http://localhost:8000/users
```

**Debugger zatrzyma się na breakpoincie!** 🎉

---

## 📋 Przydatne komendy

### Sprawdź status bazy danych
```bash
docker-compose ps
```

### Uruchom migracje
```bash
cd backend
alembic upgrade head
```

### Zatrzymaj wszystko
```bash
docker-compose down
```

### Uruchom ponownie tylko bazę
```bash
docker-compose up -d postgres
```

---

## 🔧 Troubleshooting

### "Connection refused" do bazy
```bash
# Sprawdź czy PostgreSQL działa
docker-compose ps

# Uruchom bazę
docker-compose up -d postgres
```

### Brak modułów Python
```bash
# Zainstaluj zależności
pip install -r requirements.txt
```

### Port 8000 zajęty
```bash
# Zatrzymaj backend w Dockerze
docker-compose stop backend
```

---

## 🎯 Gotowe!

Teraz możesz debugować aplikację lokalnie w PyCharm bez żadnych dodatkowych konfiguracji Docker!
