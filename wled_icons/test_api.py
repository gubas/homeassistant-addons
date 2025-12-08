
import os
import requests
import json

SUPERVISOR_TOKEN = os.environ.get("SUPERVISOR_TOKEN")
SUPERVISOR_URL = "http://supervisor/core/api"

headers = {
    "Authorization": f"Bearer {SUPERVISOR_TOKEN}",
    "Content-Type": "application/json",
}

def check_services():
    url = f"{SUPERVISOR_URL}/services"
    try:
        r = requests.get(url, headers=headers)
        if r.ok:
            services = r.json()
            # print(json.dumps(services, indent=2))
            for domain in services:
                if domain['domain'] == 'repairs':
                    print("Found repairs domain services:", domain['services'])
    except Exception as e:
        print(f"Error checking services: {e}")

def create_update_entity():
    url = f"{SUPERVISOR_URL}/states/update.wled_icons_restart_request"
    data = {
        "state": "on",
        "attributes": {
            "friendly_name": "Redémarrage WLED Icons requis",
            "installed_version": "1.0.12",
            "latest_version": "1.0.13",
            "title": "Redémarrage Nécessaire",
            "release_summary": "L'intégration a été mise à jour. Veuillez redémarrer Home Assistant.",
            "entity_picture": "https://brands.home-assistant.io/_/wled/icon.png", # Fake icon
            "supported_features": 0 # No install support
        }
    }
    try:
        r = requests.post(url, headers=headers, json=data)
        print(f"Created update entity: {r.status_code} {r.text}")
    except Exception as e:
        print(f"Error creating entity: {e}")

if __name__ == "__main__":
    if not SUPERVISOR_TOKEN:
        print("No token")
    else:
        check_services()
        create_update_entity()
