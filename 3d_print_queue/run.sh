#!/usr/bin/with-contenv bashio

# Get configuration
export TODO_LIST=$(bashio::config 'todo_list')
export SUPERVISOR_TOKEN="${SUPERVISOR_TOKEN}"
export HA_URL="http://supervisor/core"

bashio::log.info "Démarrage de la Queue d'impression 3D..."
bashio::log.info "Liste de tâches: ${TODO_LIST}"

# Start Flask application
cd /app
python3 app.py
