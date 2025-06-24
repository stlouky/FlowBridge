#!/bin/bash

# Získáme absolutní cestu k adresáři, kde se skript nachází
# To zajistí, že skript bude fungovat, ať ho spustíte odkudkoliv
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$SCRIPT_DIR"

echo "Spouštěcí skript FlowBridge..."

# 1. Aktivace virtuálního prostředí
echo "Aktivuji virtuální prostředí (myenv)..."
source myenv/bin/activate

# 2. Spuštění Flask serveru na pozadí
echo "Spouštím Flask server (python3 run.py)..."
# Použijeme 'nohup' aby server běžel i po zavření terminálu
# a výstup přesměrujeme do logu
nohup python3 run.py > flask_server.log 2>&1 &

# Uložíme si ID procesu (PID) serveru, abychom ho mohli později ukončit
SERVER_PID=$!
echo $SERVER_PID > server.pid
echo "Server spuštěn s PID: $SERVER_PID. Výstup se ukládá do flask_server.log"

# 3. Počkáme 2 sekundy, než se server plně nastartuje
echo "Čekám 2 sekundy, než se server plně spustí..."
sleep 2

# 4. Otevření aplikace ve výchozím webovém prohlížeči
echo "Otevírám aplikaci v prohlížeči..."
xdg-open http://127.0.0.1:5000/

echo "Hotovo! Aplikace by měla být otevřená. Server běží na pozadí."