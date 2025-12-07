import os
import json
import shutil
import requests
import sys

# Paths
SOURCE_PATH = "/app/integration"
TARGET_PATH = "/config/custom_components/wled_icons"
SUPERVISOR_TOKEN = os.environ.get("SUPERVISOR_TOKEN")
SUPERVISOR_URL = "http://supervisor/core/api"

def get_manifest_version(path):
    manifest_path = os.path.join(path, "manifest.json")
    if not os.path.exists(manifest_path):
        return None
    try:
        with open(manifest_path, "r") as f:
            data = json.load(f)
            return data.get("version")
    except Exception as e:
        print(f"[UPDATE] Error reading manifest at {path}: {e}")
        return None

def notify_hass(title, message):
    if not SUPERVISOR_TOKEN:
        print("[UPDATE] No supervisor token found, cannot notify.")
        return

    url = f"{SUPERVISOR_URL}/services/persistent_notification/create"
    headers = {
        "Authorization": f"Bearer {SUPERVISOR_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {
        "title": title,
        "message": message,
        "notification_id": "wled_icons_update"
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            print("[UPDATE] Notification sent to Home Assistant.")
        else:
            print(f"[UPDATE] Failed to send notification: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[UPDATE] Error sending notification: {e}")

def main():
    print(f"[UPDATE] Starting integration check...")
    print(f"[UPDATE] Source: {SOURCE_PATH}")
    print(f"[UPDATE] Target: {TARGET_PATH}")
    
    if os.environ.get("SUPERVISOR_TOKEN"):
        print("[UPDATE] SUPERVISOR_TOKEN is present.")
    else:
        print("[UPDATE] WARNING: SUPERVISOR_TOKEN is missing!")

    if not os.path.exists(SOURCE_PATH):
        print(f"[UPDATE] FATAL: Source path {SOURCE_PATH} does not exist!")
        return

    source_version = get_manifest_version(SOURCE_PATH)
    target_version = get_manifest_version(TARGET_PATH)

    print(f"[UPDATE] Source version: {source_version}")
    print(f"[UPDATE] Installed version: {target_version}")

    should_install = False
    is_update = False

    if not target_version:
        print("[UPDATE] Integration not installed. Installing...")
        should_install = True
    elif source_version != target_version:
        print(f"[UPDATE] Version mismatch ({target_version} -> {source_version}). Updating...")
        should_install = True
        is_update = True
    else:
        # FORCE UPDATE for 1.0.2 to ensure selectors are applied
        print("[UPDATE] Versions match, but forcing update to ensure file integrity (fix selectors).")
        should_install = True
        is_update = False # Don't notify if versions match, just fix files silently

    if should_install:
        try:
            # Create parent directory if it doesn't exist
            os.makedirs(os.path.dirname(TARGET_PATH), exist_ok=True)

            # Remove existing target if it exists
            if os.path.exists(TARGET_PATH):
                print(f"[UPDATE] Removing existing directory: {TARGET_PATH}")
                shutil.rmtree(TARGET_PATH)
            
            # Copy new files
            print(f"[UPDATE] Copying from {SOURCE_PATH} to {TARGET_PATH}")
            shutil.copytree(SOURCE_PATH, TARGET_PATH)
            print(f"[UPDATE] Successfully installed/updated integration.")

            if is_update:
                print("[UPDATE] Sending notification to HA...")
                notify_hass(
                    title="WLED Icons Updated",
                    message=f"L'intégration WLED Icons a été mise à jour vers la version **{source_version}**.\n\n"
                            "Veuillez **redémarrer Home Assistant** pour appliquer les changements."
                )
        except Exception as e:
            print(f"[UPDATE] ERROR during install: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()
