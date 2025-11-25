#!/usr/bin/with-contenv bashio

# Get configuration
export PRINTER_ENTITY=$(bashio::config 'printer_entity')
export CURRENCY=$(bashio::config 'currency')
export WEIGHT_UNIT=$(bashio::config 'weight_unit')
export LOW_STOCK_THRESHOLD=$(bashio::config 'low_stock_threshold')
export SUPERVISOR_TOKEN="${SUPERVISOR_TOKEN}"
export HA_URL="http://supervisor/core"

bashio::log.info "Démarrage du Filament Manager..."
bashio::log.info "Imprimante: ${PRINTER_ENTITY}"
bashio::log.info "Devise: ${CURRENCY}"

# Start application (unbuffered stdout for immediate logs)
cd /app
python3 -u app.py
