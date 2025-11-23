#!/usr/bin/with-contenv bashio

# Get configuration
export TODO_LIST=$(bashio::config 'todo_list')
export SUPERVISOR_TOKEN="${SUPERVISOR_TOKEN}"
export HA_URL="http://supervisor/core"

bashio::log.info "Démarrage de la Queue d'impression 3D..."
bashio::log.info "Liste de tâches: ${TODO_LIST}"

# Debug: afficher les premières lignes du fichier exécuté pour vérifier le code dans l'image
bashio::log.info "Affichage des 1ères lignes de /app/app.py pour debug (contenu copié dans l'image)"
if [ -f /app/app.py ]; then
	sed -n '1,80p' /app/app.py | sed 's/^/[APP_FILE] /'
else
	bashio::log.warning "/app/app.py introuvable"
fi

# Start Flask application (unbuffered stdout for immediate logs)
cd /app
python3 -u app.py
