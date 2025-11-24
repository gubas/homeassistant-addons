#!/usr/bin/with-contenv bashio

echo "[INFO] Démarrage Bambulab Timelapse Downloader..."

# Get configuration
PRINTER_IP=$(bashio::config 'printer_ip')
PRINTER_CODE=$(bashio::config 'printer_access_code')
PRINTER_SERIAL=$(bashio::config 'printer_serial')

if [ -z "$PRINTER_IP" ] || [ -z "$PRINTER_CODE" ] || [ -z "$PRINTER_SERIAL" ]; then
    echo "[ERROR] Configuration incomplète ! Veuillez configurer l'IP, le code d'accès et le numéro de série."
    exit 1
fi

echo "[INFO] Imprimante configurée: $PRINTER_IP"

# Start the application
python3 /app/server.py
