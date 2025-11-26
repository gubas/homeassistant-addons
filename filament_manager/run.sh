#!/usr/bin/with-contenv bashio

# Get configuration
export PRINTER_STATUS_ENTITY=$(bashio::config 'printer_status_entity')
export PRINTER_WEIGHT_ENTITY=$(bashio::config 'printer_weight_entity')
export CURRENCY=$(bashio::config 'currency')
export WEIGHT_UNIT=$(bashio::config 'weight_unit')
export LOW_STOCK_THRESHOLD=$(bashio::config 'low_stock_threshold')
export PORT=$(bashio::config 'port')
export SUPERVISOR_TOKEN="${SUPERVISOR_TOKEN}"
export HA_URL="http://supervisor/core"

bashio::log.info "Démarrage du Filament Manager..."
bashio::log.info "Statut imprimante: ${PRINTER_STATUS_ENTITY}"
bashio::log.info "Poids imprimante: ${PRINTER_WEIGHT_ENTITY}"
bashio::log.info "Devise: ${CURRENCY}"
bashio::log.info "Port: ${PORT}"

# Start application (unbuffered stdout for immediate logs)
cd /app
python3 -u app.py
