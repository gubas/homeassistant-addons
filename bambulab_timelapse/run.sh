#!/bin/bash
set -e

echo "[INFO] Démarrage Bambulab Timelapse Downloader..."

# Load configuration from /data/options.json
if [ -f /data/options.json ]; then
    export PRINTER_IP=$(jq -r '.printer_ip // ""' /data/options.json)
    export PRINTER_ACCESS_CODE=$(jq -r '.printer_access_code // ""' /data/options.json)
    export PRINTER_SERIAL=$(jq -r '.printer_serial // ""' /data/options.json)
    export AUTO_DOWNLOAD=$(jq -r '.auto_download // true' /data/options.json)
    export CONVERT_TO_MP4=$(jq -r '.convert_to_mp4 // true' /data/options.json)
    export RESOLUTION=$(jq -r '.resolution // "original"' /data/options.json)
    
    if [ -z "$PRINTER_IP" ] || [ -z "$PRINTER_ACCESS_CODE" ] || [ -z "$PRINTER_SERIAL" ]; then
        echo "[ERROR] Configuration incomplète ! Veuillez configurer l'IP, le code d'accès et le numéro de série."
        exit 1
    fi
    
    echo "[INFO] Imprimante configurée: $PRINTER_IP"
else
    echo "[WARN] Fichier /data/options.json non trouvé"
fi

# Start the application
exec python3 /app/server.py
