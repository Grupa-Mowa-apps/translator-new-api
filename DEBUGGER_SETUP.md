# Jak podłączyć debugger w PyCharm

## Problem
PyCharm próbował utworzyć nowy kontener Docker, ale port 5678 jest już zajęty przez istniejący kontener z docker-compose.

## Rozwiązanie
Podłączamy się do istniejącego kontenera używając **Python Remote Debug**.

## Kroki:

### 1. Upewnij się, że kontenery działają
```bash
docker-compose ps
```

### 2. W PyCharm:

1. **Run → Edit Configurations...**
2. Kliknij **+** (Add New Configuration)
3. Wybierz **Python Remote Debug** (nie Docker Image!)
4. Ustaw:
   - **Name:** `Attach to Docker`
   - **Port:** `5678`
   
5. W sekcji **Path mappings** kliknij folder i dodaj:
   - **Local path:** `/Users/gmtomasz/PycharmProjects/translator-new-api/backend/src`
   - **Remote path:** `/app/backend/src`

6. Kliknij **OK**

### 3. Ustaw breakpoint
- Otwórz `backend/src/app/api/http/controllers/users_controller.py`
- Kliknij na marginesie przy linii 45 (funkcja `list_users`)

### 4. Uruchom debugger
- Wybierz konfigurację **"Attach to Docker"**
- Kliknij ikonę debugowania (zielony robak) lub **Shift+F9**
- Powinieneś zobaczyć: "Connected to pydev debugger"

### 5. Wykonaj request
```bash
curl http://localhost:8000/users
```

### 6. Debugger zatrzyma się na breakpoincie! 🎉

## Troubleshooting

### "Connection refused"
```bash
# Sprawdź czy kontener działa
docker-compose ps

# Sprawdź logi
docker-compose logs backend --tail=20

# Restart kontenera
docker-compose restart backend
```

### "Breakpoint nie działa"
- Sprawdź mapowanie ścieżek (musi być `/backend/src` → `/app/backend/src`)
- Upewnij się, że plik jest w wolumenie Docker
- Zrestartuj debugger
