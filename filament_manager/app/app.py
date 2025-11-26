print("[DEBUG] Démarrage app.py (version 0.4.1)", flush=True)
"""
Filament Manager - Application Bottle
Gestionnaire de filaments 3D avec suivi de consommation
"""

import os
import json
import requests
from bottle import Bottle, request, response, jinja2_template as template, static_file, redirect, TEMPLATE_PATH
from datetime import datetime
import threading
import time

# Import des modules locaux
import database as db
import calculations as calc

# Configuration du chemin des templates
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH.insert(0, '/app/templates')
TEMPLATE_PATH.insert(0, os.path.join(BASE_DIR, 'templates'))

app = Bottle()

# Configuration depuis les variables d'environnement
SUPERVISOR_TOKEN = os.getenv('SUPERVISOR_TOKEN', '')
HA_URL = os.getenv('HA_URL', 'http://supervisor/core')
INGRESS_PATH = os.getenv('INGRESS_PATH', '')
PRINTER_STATUS_ENTITY = os.getenv('PRINTER_STATUS_ENTITY', 'sensor.p1s_stage')
PRINTER_WEIGHT_ENTITY = os.getenv('PRINTER_WEIGHT_ENTITY', 'sensor.p1s_print_weight')
CURRENCY = os.getenv('CURRENCY', 'EUR')
WEIGHT_UNIT = os.getenv('WEIGHT_UNIT', 'g')
LOW_STOCK_THRESHOLD = float(os.getenv('LOW_STOCK_THRESHOLD', '200'))
PORT = int(os.getenv('PORT', '5001'))

# Initialiser la base de données
db.init_db()

# Types et couleurs disponibles
FILAMENT_TYPES = ['PLA', 'PETG', 'ABS', 'TPU', 'ASA', 'Nylon', 'HIPS', 'PC']
FILAMENT_COLORS = [
    'Blanc', 'Noir', 'Gris', 'Rouge', 'Bleu', 'Vert', 
    'Jaune', 'Orange', 'Violet', 'Rose', 'Marron', 'Transparent'
]


def get_color_code(color):
    """Retourne un code couleur CSS basé sur le nom"""
    colors = {
        'Blanc': '#ffffff',
        'Noir': '#000000',
        'Gris': '#808080',
        'Rouge': '#e74c3c',
        'Bleu': '#3498db',
        'Vert': '#2ecc71',
        'Jaune': '#f1c40f',
        'Orange': '#e67e22',
        'Violet': '#9b59b6',
        'Rose': '#ff69b4',
        'Marron': '#8b4513',
        'Transparent': 'linear-gradient(45deg, #ccc 25%, transparent 25%, transparent 75%, #ccc 75%, #ccc), linear-gradient(45deg, #ccc 25%, white 25%, white 75%, #ccc 75%, #ccc)'
    }
    return colors.get(color, '#cccccc')


class HomeAssistantAPI:
    """Interface avec Home Assistant"""
    
    def __init__(self):
        self.headers = {
            'Authorization': f'Bearer {SUPERVISOR_TOKEN}',
            'Content-Type': 'application/json'
        }
    
    def get_state(self, entity_id: str):
        """Récupère l'état d'une entité"""
        try:
            url = f"{HA_URL}/api/states/{entity_id}"
            resp = requests.get(url, headers=self.headers, timeout=5)
            if resp.status_code == 200:
                return resp.json()
            else:
                print(f"[HA API] Erreur get_state: {resp.status_code}", flush=True)
                return None
        except Exception as e:
            print(f"[HA API] Exception get_state: {e}", flush=True)
            return None
    
    def send_notification(self, title: str, message: str):
        """Envoie une notification via HA"""
        try:
            url = f"{HA_URL}/api/services/persistent_notification/create"
            data = {
                "title": title,
                "message": message
            }
            resp = requests.post(url, headers=self.headers, json=data, timeout=5)
            return resp.status_code == 200
        except Exception as e:
            print(f"[HA API] Exception notification: {e}", flush=True)
            return False


ha_api = HomeAssistantAPI()


class PrinterMonitor(threading.Thread):
    """Thread de surveillance de l'imprimante"""
    
    def __init__(self):
        super().__init__()
        self.daemon = True
        self.running = True
        self.last_status = None
        
    def run(self):
        print("[MONITOR] Démarrage du monitoring imprimante...", flush=True)
        while self.running:
            try:
                self.check_printer()
            except Exception as e:
                print(f"[MONITOR] Erreur: {e}", flush=True)
            time.sleep(30)  # Vérifier toutes les 30 secondes
            
    def check_printer(self):
        # 1. Récupérer l'état
        state_data = ha_api.get_state(PRINTER_STATUS_ENTITY)
        if not state_data:
            return
            
        current_status = state_data.get('state')
        
        # Détection de la fin d'impression (transition vers 'finish' ou 'success')
        # Note: Adapter selon les états réels de l'intégration Bambulab
        if current_status in ['finish', 'success'] and self.last_status not in ['finish', 'success', None]:
            print(f"[MONITOR] Fin d'impression détectée (Status: {current_status})", flush=True)
            self.handle_print_finished()
            
        self.last_status = current_status
        
    def handle_print_finished(self):
        # 1. Récupérer le filament actif
        active_filament = db.get_active_filament()
        if not active_filament:
            print("[MONITOR] Pas de filament actif sélectionné !", flush=True)
            ha_api.send_notification(
                "⚠️ Filament Manager",
                "Impression terminée mais aucun filament n'est sélectionné comme actif. Impossible de décompter le stock."
            )
            return

        # 2. Récupérer le poids consommé
        weight_data = ha_api.get_state(PRINTER_WEIGHT_ENTITY)
        if not weight_data:
            print("[MONITOR] Impossible de lire le poids consommé", flush=True)
            return
            
        try:
            weight_used = float(weight_data.get('state', 0))
        except ValueError:
            print(f"[MONITOR] Valeur de poids invalide: {weight_data.get('state')}", flush=True)
            return
            
        if weight_used <= 0:
            print("[MONITOR] Poids consommé nul ou négatif, ignoré", flush=True)
            return
            
        # 3. Décompter le stock
        print(f"[MONITOR] Décompte de {weight_used}g sur le filament {active_filament['name']}", flush=True)
        db.update_filament_weight(
            filament_id=active_filament['id'],
            weight_used=weight_used,
            print_name="Impression automatique"
        )
        
        # 4. Notification
        ha_api.send_notification(
            "Filament Manager",
            f"Impression terminée. {weight_used}g déduits du stock de {active_filament['name']}."
        )


# Démarrer le monitoring
monitor = PrinterMonitor()
monitor.start()


# ============ Routes Web ============

@app.route('/')
@app.route('/index')
@app.route('/inventory')
def inventory():
    """Page d'inventaire des filaments"""
    filaments = db.get_all_filaments()
    
    # Enrichir avec les pourcentages et alertes
    for fil in filaments:
        fil['percentage'] = calc.get_remaining_percentage(
            fil['current_weight'], fil['initial_weight']
        )
        fil['is_low_stock'] = calc.is_low_stock(
            fil['current_weight'], LOW_STOCK_THRESHOLD
        )
        fil['formatted_cost'] = calc.format_currency(fil['cost'], CURRENCY)
        fil['formatted_current'] = calc.format_weight(fil['current_weight'], WEIGHT_UNIT)
        fil['formatted_initial'] = calc.format_weight(fil['initial_weight'], WEIGHT_UNIT)
    
    return template('inventory', 
                   filaments=filaments,
                   ingress_path='',
                   currency=CURRENCY,
                   weight_unit=WEIGHT_UNIT,
                   get_color_code=get_color_code)


@app.route('/add')
def add_filament_page():
    """Page d'ajout de filament"""
    return template('add_filament',
                   filament=None,
                   types=FILAMENT_TYPES,
                   colors=FILAMENT_COLORS,
                   ingress_path='',
                   edit_mode=False)


@app.route('/edit/<filament_id:int>')
def edit_filament_page(filament_id):
    """Page d'édition de filament"""
    filament = db.get_filament(filament_id)
    if not filament:
        return "Filament non trouvé", 404
    
    return template('add_filament',
                   filament=filament,
                   types=FILAMENT_TYPES,
                   colors=FILAMENT_COLORS,
                   ingress_path='',
                   edit_mode=True)


@app.route('/statistics')
def statistics():
    """Page des statistiques"""
    # Récupérer les données pour les stats
    all_filaments = db.get_all_filaments()
    all_consumptions = db.get_all_consumptions()
    total_spent = db.get_total_spent()
    total_consumption_cost = db.get_total_consumption_cost()
    consumption_by_type = db.get_consumption_by_type()
    low_stock = db.get_low_stock_filaments(LOW_STOCK_THRESHOLD)
    
    # Calculer le total de poids restant
    total_remaining = sum(f['current_weight'] for f in all_filaments)
    
    return template('statistics',
                   filaments=all_filaments,
                   consumptions=all_consumptions,
                   total_spent=total_spent,
                   total_consumption_cost=total_consumption_cost,
                   consumption_by_type=consumption_by_type,
                   low_stock=low_stock,
                   total_remaining=total_remaining,
                   ingress_path='',
                   currency=CURRENCY,
                   weight_unit=WEIGHT_UNIT)


# ============ API Routes ============

@app.route('/api/filaments', method='GET')
def api_get_filaments():
    """API: Liste tous les filaments"""
    response.content_type = 'application/json'
    filaments = db.get_all_filaments()
    return json.dumps(filaments)


@app.route('/api/filaments', method='POST')
def api_add_filament():
    """API: Ajoute un nouveau filament"""
    response.content_type = 'application/json'
    
    try:
        data = request.json
        filament_id = db.add_filament(
            name=data['name'],
            filament_type=data['type'],
            color=data['color'],
            weight=float(data['weight']),
            cost=float(data['cost']),
            notes=data.get('notes', '')
        )
        
        # Notification
        ha_api.send_notification(
            "Filament Manager",
            f"Nouveau filament ajouté: {data['name']}"
        )
        
        return json.dumps({'success': True, 'id': filament_id})
    except Exception as e:
        response.status = 400
        return json.dumps({'success': False, 'error': str(e)})


@app.route('/api/filaments/<filament_id:int>', method='PUT')
def api_update_filament(filament_id):
    """API: Met à jour un filament"""
    response.content_type = 'application/json'
    
    try:
        data = request.json
        success = db.update_filament(
            filament_id=filament_id,
            name=data['name'],
            filament_type=data['type'],
            color=data['color'],
            initial_weight=float(data['initial_weight']),
            current_weight=float(data['current_weight']),
            cost=float(data['cost']),
            notes=data.get('notes', '')
        )
        
        return json.dumps({'success': success})
    except Exception as e:
        response.status = 400
        return json.dumps({'success': False, 'error': str(e)})


@app.route('/api/filaments/<filament_id:int>', method='DELETE')
def api_delete_filament(filament_id):
    """API: Supprime un filament"""
    response.content_type = 'application/json'
    
    success = db.delete_filament(filament_id)
    return json.dumps({'success': success})


@app.route('/api/filaments/<filament_id:int>/consume', method='POST')
def api_consume_filament(filament_id):
    """API: Enregistre une consommation de filament"""
    response.content_type = 'application/json'
    
    try:
        data = request.json
        success = db.update_filament_weight(
            filament_id=filament_id,
            weight_used=float(data['weight_used']),
            print_name=data.get('print_name', '')
        )
        
        # Vérifier si stock faible après consommation
        filament = db.get_filament(filament_id)
        if filament and calc.is_low_stock(filament['current_weight'], LOW_STOCK_THRESHOLD):
            ha_api.send_notification(
                "⚠️ Filament Manager - Stock Faible",
                f"Le filament '{filament['name']}' est en stock faible ({filament['current_weight']:.0f}g restants)"
            )
        
        return json.dumps({'success': success})
    except Exception as e:
        response.status = 400
        return json.dumps({'success': False, 'error': str(e)})


@app.route('/api/filaments/<filament_id:int>/set_active', method='POST')
def api_set_active_filament(filament_id):
    """API: Définit le filament actif"""
    response.content_type = 'application/json'
    
    success = db.set_active_filament(filament_id)
    return json.dumps({'success': success})


# ============ Static Files ============

@app.route('/static/<filepath:path>')
def serve_static(filepath):
    """Sert les fichiers statiques"""
    return static_file(filepath, root='/app/static')


# Ingress est géré automatiquement par Home Assistant
run_app = app


if __name__ == '__main__':
    print(f"[INFO] Démarrage Filament Manager v0.4.1", flush=True)
    print(f"[INFO] Statut imprimante: {PRINTER_STATUS_ENTITY}", flush=True)
    print(f"[INFO] Poids imprimante: {PRINTER_WEIGHT_ENTITY}", flush=True)
    print(f"[INFO] Devise: {CURRENCY}, Unité: {WEIGHT_UNIT}", flush=True)
    print(f"[INFO] Seuil stock faible: {LOW_STOCK_THRESHOLD}g", flush=True)
    print(f"[INFO] Port: {PORT}", flush=True)
    run_app.run(host='0.0.0.0', port=PORT, debug=False, server='wsgiref')
