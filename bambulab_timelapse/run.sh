#!/bin/bash
set -e

echo "[INFO] Démarrage Bambulab Timelapse Downloader..."

# Load configuration from /data/options.json
if [ -f /data/options.json ]; then
    export BAMBU_EMAIL=$(jq -r '.bambu_email // ""' /data/options.json)
    export BAMBU_PASSWORD=$(jq -r '.bambu_password // ""' /data/options.json)
    export BAMBU_REGION=$(jq -r '.bambu_region // "China"' /data/options.json)
    export PRINTER_SERIAL=$(jq -r '.printer_serial // ""' /data/options.json)
    export AUTO_DOWNLOAD=$(jq -r '.auto_download // true' /data/options.json)
    export CONVERT_TO_MP4=$(jq -r '.convert_to_mp4 // true' /data/options.json)
    export RESOLUTION=$(jq -r '.resolution // "original"' /data/options.json)
    
    if [ -z "$BAMBU_EMAIL" ] || [ -z "$BAMBU_PASSWORD" ] || [ -z "$PRINTER_SERIAL" ]; then
        echo "[ERROR] Configuration incomplète ! Veuillez configurer l'email Bambu, le mot de passe et le numéro de série."
        exit 1
    fi
    
    echo "[INFO] Bambu Cloud: $BAMBU_EMAIL (Région: $BAMBU_REGION)"
else
    echo "[WARN] Fichier /data/options.json non trouvé"
fi

# Start the application
exec python3 /app/server.py
