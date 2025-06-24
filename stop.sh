#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$SCRIPT_DIR"

echo "Vypínám server FlowBridge..."

if [ -f "server.pid" ]; then
    PID=$(cat server.pid)
    echo "Nalezen proces s PID: $PID. Ukončuji..."
    kill $PID
    rm server.pid
    echo "Server úspěšně zastaven."
else
    echo "Soubor server.pid nenalezen. Není co zastavit, nebo byl server ukončen jinak."
fi