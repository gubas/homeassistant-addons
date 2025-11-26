"""
Filament Manager - Database Module
Gestion de la base de données SQLite pour l'inventaire de filaments
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple

DB_PATH = os.getenv('DB_PATH', '/data/filaments.db')


def get_db():
    """Crée une connexion à la base de données"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Pour accéder aux colonnes par nom
    return conn


def init_db():
    """Initialise la base de données avec les tables nécessaires"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Table des filaments
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS filaments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            color TEXT NOT NULL,
            initial_weight REAL NOT NULL,
            current_weight REAL NOT NULL,
            cost REAL NOT NULL,
            purchase_date TEXT NOT NULL,
            notes TEXT,
            created_at TEXT NOT NULL,
            is_active BOOLEAN DEFAULT 0
        )
    ''')
    
    # Migration: Ajouter la colonne is_active si elle n'existe pas (pour les bases existantes)
    try:
        cursor.execute('SELECT is_active FROM filaments LIMIT 1')
    except sqlite3.OperationalError:
        print("[DB] Migration: Ajout de la colonne is_active", flush=True)
        cursor.execute('ALTER TABLE filaments ADD COLUMN is_active BOOLEAN DEFAULT 0')
    
    # Table des consommations
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS consumptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filament_id INTEGER NOT NULL,
            print_name TEXT,
            weight_used REAL NOT NULL,
            cost REAL NOT NULL,
            consumption_date TEXT NOT NULL,
            FOREIGN KEY (filament_id) REFERENCES filaments (id) ON DELETE CASCADE
        )
    ''')
    
    # Table des paramètres
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
    print("[DB] Base de données initialisée", flush=True)


# ============ CRUD Filaments ============

def add_filament(name: str, filament_type: str, color: str, 
                 weight: float, cost: float, notes: str = "") -> int:
    """Ajoute un nouveau filament à l'inventaire"""
    conn = get_db()
    cursor = conn.cursor()
    
    now = datetime.now().isoformat()
    purchase_date = datetime.now().date().isoformat()
    
    cursor.execute('''
        INSERT INTO filaments 
        (name, type, color, initial_weight, current_weight, cost, purchase_date, notes, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, filament_type, color, weight, weight, cost, purchase_date, notes, now))
    
    filament_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    print(f"[DB] Filament ajouté: {name} (ID: {filament_id})", flush=True)
    print(f"[DB] Filament ajouté: {name} (ID: {filament_id})", flush=True)
    return filament_id


def set_active_filament(filament_id: int) -> bool:
    """Définit un filament comme étant celui actif (utilisé par l'imprimante)"""
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        # 1. Désactiver tous les filaments
        cursor.execute('UPDATE filaments SET is_active = 0')
        
        # 2. Activer le filament choisi
        cursor.execute('UPDATE filaments SET is_active = 1 WHERE id = ?', (filament_id,))
        
        success = cursor.rowcount > 0
        conn.commit()
        return success
    except Exception as e:
        print(f"[DB] Erreur set_active_filament: {e}", flush=True)
        return False
    finally:
        conn.close()


def get_all_filaments() -> List[Dict]:
    """Récupère tous les filaments"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM filaments ORDER BY created_at DESC')
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


def get_filament(filament_id: int) -> Optional[Dict]:
    """Récupère un filament par son ID"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM filaments WHERE id = ?', (filament_id,))
    row = cursor.fetchone()
    conn.close()
    
    return dict(row) if row else None


def get_active_filament() -> Optional[Dict]:
    """Récupère le filament actuellement actif"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM filaments WHERE is_active = 1 LIMIT 1')
    row = cursor.fetchone()
    conn.close()
    
    return dict(row) if row else None


def update_filament(filament_id: int, name: str, filament_type: str, 
                   color: str, initial_weight: float, current_weight: float,
                   cost: float, notes: str = "") -> bool:
    """Met à jour un filament existant"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE filaments 
        SET name = ?, type = ?, color = ?, initial_weight = ?, 
            current_weight = ?, cost = ?, notes = ?
        WHERE id = ?
    ''', (name, filament_type, color, initial_weight, current_weight, cost, notes, filament_id))
    
    success = cursor.rowcount > 0
    conn.commit()
    conn.close()
    
    return success


def delete_filament(filament_id: int) -> bool:
    """Supprime un filament"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM filaments WHERE id = ?', (filament_id,))
    success = cursor.rowcount > 0
    
    conn.commit()
    conn.close()
    
    return success


def update_filament_weight(filament_id: int, weight_used: float, 
                          print_name: str = "") -> bool:
    """
    Diminue le poids d'un filament et enregistre la consommation
    """
    filament = get_filament(filament_id)
    if not filament:
        return False
    
    new_weight = max(0, filament['current_weight'] - weight_used)
    
    # Calculer le coût de cette consommation
    cost_per_gram = filament['cost'] / filament['initial_weight']
    consumption_cost = weight_used * cost_per_gram
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Mettre à jour le poids
    cursor.execute(
        'UPDATE filaments SET current_weight = ? WHERE id = ?',
        (new_weight, filament_id)
    )
    
    # Enregistrer la consommation
    cursor.execute('''
        INSERT INTO consumptions (filament_id, print_name, weight_used, cost, consumption_date)
        VALUES (?, ?, ?, ?, ?)
    ''', (filament_id, print_name, weight_used, consumption_cost, datetime.now().isoformat()))
    
    conn.commit()
    conn.close()
    
    print(f"[DB] Consommation enregistrée: {weight_used}g pour {print_name}", flush=True)
    return True


# ============ Consumptions ============

def get_all_consumptions() -> List[Dict]:
    """Récupère toutes les consommations avec les infos du filament"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT c.*, f.name as filament_name, f.color, f.type
        FROM consumptions c
        JOIN filaments f ON c.filament_id = f.id
        ORDER BY c.consumption_date DESC
    ''')
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


def get_filament_consumptions(filament_id: int) -> List[Dict]:
    """Récupère toutes les consommations d'un filament spécifique"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM consumptions
        WHERE filament_id = ?
        ORDER BY consumption_date DESC
    ''', (filament_id,))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


# ============ Statistics ============

def get_total_spent() -> float:
    """Calcule le coût total dépensé en filaments"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT SUM(cost) as total FROM filaments')
    result = cursor.fetchone()
    conn.close()
    
    return result['total'] or 0.0


def get_total_consumption_cost() -> float:
    """Calcule le coût total des consommations"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT SUM(cost) as total FROM consumptions')
    result = cursor.fetchone()
    conn.close()
    
    return result['total'] or 0.0


def get_consumption_by_type() -> Dict[str, float]:
    """Récupère la consommation par type de filament"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT f.type, SUM(c.weight_used) as total_weight
        FROM consumptions c
        JOIN filaments f ON c.filament_id = f.id
        GROUP BY f.type
    ''')
    
    rows = cursor.fetchall()
    conn.close()
    
    return {row['type']: row['total_weight'] for row in rows}


def get_low_stock_filaments(threshold: float) -> List[Dict]:
    """Récupère les filaments avec un stock faible"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM filaments
        WHERE current_weight <= ?
        ORDER BY current_weight ASC
    ''', (threshold,))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]
