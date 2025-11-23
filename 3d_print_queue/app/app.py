print("[DEBUG] Démarrage app.py (version 0.4.1)", flush=True)
"""
3D Print Queue - Application Bottle ultra-légère
Gestion de queue d'impressions 3D depuis MakerWorld uniquement
"""
from bottle import Bottle, request, response, static_file, template, run
import os
import json
import requests
from datetime import datetime
from pathlib import Path
import re
import sys
from bs4 import BeautifulSoup

app = Bottle()

# Configuration
DATA_DIR = Path('/data')
if not DATA_DIR.exists():
    DATA_DIR = Path(__file__).parent / 'data'
    DATA_DIR.mkdir(exist_ok=True)

QUEUE_FILE = DATA_DIR / 'queue.json'
HA_TOKEN = os.environ.get('SUPERVISOR_TOKEN')
HA_URL = "http://supervisor/core"
TODO_LIST = "todo.file_d_attente_impression_3d"
SUPERVISOR_TOKEN = os.getenv('SUPERVISOR_TOKEN', '') # Keep existing SUPERVISOR_TOKEN for now, will be replaced by HA_TOKEN later
INGRESS_PATH = os.getenv('INGRESS_PATH', '')


def fetch_makerworld_metadata(url):
    """Récupère les métadonnées depuis MakerWorld"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code != 200:
            print(f"[METADATA] Erreur HTTP {resp.status_code}")
            return None

        soup = BeautifulSoup(resp.text, 'html.parser')
        next_data = soup.find('script', id='__NEXT_DATA__')
        
        if not next_data:
            print("[METADATA] Balise __NEXT_DATA__ introuvable")
            return None
            
        data = json.loads(next_data.string)
        design = data.get('props', {}).get('pageProps', {}).get('design', {})
        instances = design.get('instances', [])
        
        if not instances:
            print("[METADATA] Aucune instance trouvée")
            return None
            
        # Trouver l'instance par défaut ou prendre la première
        target_instance = instances[0]
        for inst in instances:
            if inst.get('isDefault'):
                target_instance = inst
                break
                
        metadata = {
            'weight': target_instance.get('weight', 0),
            'needs_ams': target_instance.get('needAms', False),
            'filaments': []
        }
        
        for fil in target_instance.get('instanceFilaments', []):
            metadata['filaments'].append({
                'color': fil.get('color'),
                'type': fil.get('type'),
                'used_g': fil.get('usedG')
            })
            
        print(f"[METADATA] Succès: {metadata}")
        return metadata
        
    except Exception as e:
        print(f"[METADATA] Exception: {e}")
        return None

# Dossier de données


FILAMENT_COLORS = [
    'Blanc', 'Noir', 'Gris', 'Rouge', 'Bleu', 'Vert', 
    'Jaune', 'Orange', 'Violet', 'Rose', 'Marron', 'Transparent'
]


class HomeAssistantAPI:
    """Interface avec Home Assistant"""
    
    def __init__(self):
        self.headers = {
            'Authorization': f'Bearer {SUPERVISOR_TOKEN}',
            'Content-Type': 'application/json'
        }
    
    def add_to_todo_list(self, item_data):
        """Ajoute un élément à la To-Do List HA"""
        try:
            summary = f"🖨️ {item_data['name']} - {item_data['color']}"
            description = f"Demandé par: {item_data['requester']}\nLien: {item_data['url']}"
            response = requests.post(
                f'{HA_URL}/api/services/todo/add_item',
                headers=self.headers,
                json={
                    'entity_id': TODO_LIST,
                    'item': summary,
                    'description': description
                },
                timeout=5
            )
            if response.status_code not in [200, 201]:
                print(f"[ERREUR TODO] Status: {response.status_code} | Body: {response.text}")
            return response.status_code in [200, 201]
        except Exception as e:
            print(f"[EXCEPTION TODO] Erreur ajout to-do: {e}")
            return False
    
    def send_notification(self, title, message):
        """Envoie une notification via HA"""
        try:
            requests.post(
                f'{HA_URL}/api/services/notify/notify',
                headers=self.headers,
                json={
                    'title': title,
                    'message': message
                },
                timeout=5
            )
        except Exception as e:
            print(f"Erreur notification: {e}")


def validate_makerworld_url(url):
    """Valide qu'une URL est bien un lien MakerWorld valide"""
    if not url:
        return False, "URL vide"
    
    if 'makerworld.com' not in url.lower():
        return False, "Seuls les liens MakerWorld sont acceptés"
    
    model_match = re.search(r'/models/(\d+)', url)
    if not model_match:
        return False, "Format de lien MakerWorld invalide"
    
    return True, model_match.group(1)


def extract_model_name_from_url(url):
    """Extrait le nom du modèle depuis l'URL MakerWorld"""
    try:
        parts = url.split('/')[-1]
        name_part = parts.split('-', 1)[-1] if '-' in parts else parts
        name = name_part.replace('-', ' ').title()
        return name
    except:
        return "Modèle MakerWorld"


def load_queue():
    """Charge la queue depuis le fichier JSON"""
    if QUEUE_FILE.exists():
        with open(QUEUE_FILE, 'r') as f:
            return json.load(f)
    return []


def save_queue(queue):
    """Sauvegarde la queue dans le fichier JSON"""
    with open(QUEUE_FILE, 'w') as f:
        json.dump(queue, f, indent=2)


@app.route('/')
def index():
    """Page principale"""
    user = request.headers.get('X-Ingress-User', '')
    print(f"[DEBUG] User detected: {user}", flush=True)
    html_file = Path(__file__).parent / 'templates' / 'index.html'
    html = html_file.read_text()
    return html.replace('{{USER}}', user)


@app.route('/queue')
def view_queue():
    """Affiche la queue"""
    html_file = Path(__file__).parent / 'templates' / 'queue.html'
    return html_file.read_text()



@app.route('/submit', method=['POST'])
def submit_print():
    """Soumet une nouvelle demande d'impression"""
    response.content_type = 'application/json'
    try:
        print("[DEBUG] POST /submit appelé", flush=True)
        url = request.forms.get('url', '').strip()
        name = request.forms.get('name', '').strip()
        color = request.forms.get('color', 'Blanc')
        requester = request.forms.get('requester', '').strip()
        print(f"[DEBUG] Données reçues: url={url}, name={name}, color={color}, requester={requester}", flush=True)
        if not requester:
            ingress_user = request.headers.get('X-Ingress-User')
            requester = ingress_user if ingress_user else 'Anonyme'
        is_valid, result = validate_makerworld_url(url)
        if not is_valid:
            print(f"[DEBUG] URL MakerWorld invalide: {result}", flush=True)
            response.status = 400
            return json.dumps({'error': result})
        model_id = result
        if not name:
            name = extract_model_name_from_url(url)
        
        # Récupération des métadonnées
        metadata = fetch_makerworld_metadata(url)
        
        ha_api = HomeAssistantAPI()
        queue_item = {
            'id': datetime.now().strftime('%Y%m%d%H%M%S'),
            'name': name,
            'requester': requester,
            'color': color,
            'url': url,
            'model_id': model_id,
            'timestamp': datetime.now().isoformat(),
            'status': 'pending'
        }
        
        if metadata:
            queue_item.update(metadata)
        print(f"[DEBUG] Ajout à la queue: {queue_item}", flush=True)
        queue = load_queue()
        queue.append(queue_item)
        save_queue(queue)
        print("[DEBUG] Queue sauvegardée dans /data/queue.json", flush=True)
        # Lire et afficher le contenu du fichier queue.json pour vérifier la persistance
        try:
            with open(QUEUE_FILE, 'r') as qf:
                content = qf.read()
            print(f"[QUEUE_FILE] {content}", flush=True)
        except Exception as e:
            print(f"[QUEUE_FILE] Impossible de lire {QUEUE_FILE}: {e}", flush=True)

        todo_ok = ha_api.add_to_todo_list(queue_item)
        print((f"[DEBUG] Ajout à la to-do: OK") if todo_ok else (f"[DEBUG] Ajout à la to-do: ECHEC"), flush=True)
        ha_api.send_notification(
            '🖨️ Nouvelle demande d\'impression',
            f"{requester} demande: {name} ({color})"
        )
        return json.dumps({'message': 'Demande ajoutée avec succès!', 'item': queue_item})
    except Exception as e:
        print(f"[EXCEPTION SUBMIT] {e}", flush=True)
        response.status = 500
        return json.dumps({'error': str(e)})

# Route alternative pour /submit/ (avec slash final)
@app.route('/submit/', method=['POST'])
def submit_print_slash():
    return submit_print()


@app.route('/api/queue')
def get_queue():
    """API: Récupère la queue"""
    response.content_type = 'application/json'
    return json.dumps(load_queue())


@app.route('/api/delete/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    """API: Supprime un élément"""
    response.content_type = 'application/json'
    queue = load_queue()
    queue = [item for item in queue if item['id'] != item_id]
    save_queue(queue)
    return json.dumps({'success': True})


# Support Ingress - mount app sous le path ingress si défini
if INGRESS_PATH:
    main_app = Bottle()
    main_app.mount(INGRESS_PATH, app)
    run_app = main_app
else:
    run_app = app


if __name__ == '__main__':
    run_app.run(host='0.0.0.0', port=5000, debug=False, server='wsgiref')
