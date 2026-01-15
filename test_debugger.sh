#!/bin/bash

echo "=== Test debugera Docker ==="
echo ""
echo "1. Uruchom konfigurację 'Docker Remote Debug' w PyCharm"
echo "2. Ustaw breakpoint w pliku users_controller.py (np. linia 45)"
echo "3. Wykonaj request:"
echo ""
echo "curl http://localhost:8000/users"
echo ""
echo "4. Debugger powinien zatrzymać się na breakpoincie"
echo ""
echo "Wykonuję request..."
curl -s http://localhost:8000/users | python3 -m json.tool
echo ""
echo "=== Test zakończony ==="
