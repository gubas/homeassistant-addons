#!/bin/sh
set -e

# Auto-install integration into Home Assistant
INTEGRATION_SOURCE="/app/integration"
INTEGRATION_TARGET="/config/custom_components/wled_icons"

# Run the update script
python3 /app/app/update_integration.py

echo "[STARTUP] Starting WLED Icons service..."
export PYTHONPATH=/app
exec uvicorn app.main:app --host 0.0.0.0 --port 8234
