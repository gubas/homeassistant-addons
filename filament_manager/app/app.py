print("[DEBUG] Démarrage app.py (version 0.1.0)", flush=True)
"""
Filament Manager - Application Bottle
Gestionnaire de filaments 3D avec suivi de consommation
"""

import os
import json
import requests
from bottle import Bottle, request, response, template, static_file, redirect
from datetime import datetime

# Import des modules locaux
import database as db
import calculations as calc

app = Bottle()

# Configuration depuis les variables d'environnement
SUPERVISOR_TOKEN = os.getenv('SUPERVISOR_TOKEN', '')
HA_URL = os.getenv('HA_URL', 'http://supervisor/core')
INGRESS_PATH = os.getenv('INGRESS_PATH', '')
PRINTER_ENTITY = os.getenv('PRINTER_ENTITY', 'sensor.p1s_print_progress')
CURRENCY = os.getenv('CURRENCY', 'EUR')
WEIGHT_UNIT = os.getenv('WEIGHT_UNIT', 'g')
LOW_STOCK_THRESHOLD = float(os.getenv('LOW_STOCK_THRESHOLD', '200'))

# Initialiser la base de données
db.init_db()

# Types et couleurs disponibles
FILAMENT_TYPES = ['PLA', 'PETG', 'ABS', 'TPU', 'ASA', 'Nylon', 'HIPS', 'PC']
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


# ============ Routes Web ============

@app.route('/')
@app.route('/index')
def index():
    """Page principale - redirige vers l'inventaire"""
    return redirect('/inventory')


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
                   weight_unit=WEIGHT_UNIT)


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


# ============ Static Files ============

@app.route('/static/<filepath:path>')
def serve_static(filepath):
    """Sert les fichiers statiques"""
    return static_file(filepath, root='/app/static')


# Ingress est géré automatiquement par Home Assistant
run_app = app


if __name__ == '__main__':
    print(f"[INFO] Démarrage Filament Manager v0.1.0", flush=True)
    print(f"[INFO] Imprimante configurée: {PRINTER_ENTITY}", flush=True)
    print(f"[INFO] Devise: {CURRENCY}, Unité: {WEIGHT_UNIT}", flush=True)
    print(f"[INFO] Seuil stock faible: {LOW_STOCK_THRESHOLD}g", flush=True)
    run_app.run(host='0.0.0.0', port=5001, debug=False, server='wsgiref')
