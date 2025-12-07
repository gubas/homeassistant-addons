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
    print("[UPDATE] Checking for integration updates...")
    
    if not os.path.exists(SOURCE_PATH):
        print(f"[UPDATE] Source path {SOURCE_PATH} does not exist. Skipping.")
        return

    source_version = get_manifest_version(SOURCE_PATH)
    target_version = get_manifest_version(TARGET_PATH)

    if not source_version:
        print("[UPDATE] Could not determine source version. Skipping.")
        return

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
        print("[UPDATE] Integration is up to date.")

    if should_install:
        # Create parent directory if it doesn't exist
        os.makedirs(os.path.dirname(TARGET_PATH), exist_ok=True)

        # Remove existing target if it exists
        if os.path.exists(TARGET_PATH):
            shutil.rmtree(TARGET_PATH)
        
        # Copy new files
        shutil.copytree(SOURCE_PATH, TARGET_PATH)
        print(f"[UPDATE] Successfully installed version {source_version}.")

        if is_update:
            notify_hass(
                title="WLED Icons Updated",
                message=f"L'intégration WLED Icons a été mise à jour vers la version **{source_version}**.\n\n"
                        "Veuillez **redémarrer Home Assistant** pour appliquer les changements."
            )

if __name__ == "__main__":
    main()
