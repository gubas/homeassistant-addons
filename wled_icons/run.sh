#!/bin/sh
set -e

# Auto-install integration into Home Assistant
INTEGRATION_SOURCE="/app/integration"
INTEGRATION_TARGET="/config/custom_components/wled_icons"

# Run the update script
echo "[SETUP] Launching update script..."
ls -la /app/app/update_integration.py || echo "[SETUP] Script not found at /app/app/update_integration.py"

python3 /app/app/update_integration.py
echo "[SETUP] Update script finished."

echo "[STARTUP] Starting WLED Icons service..."
export PYTHONPATH=/app
exec uvicorn app.main:app --host 0.0.0.0 --port 8234
