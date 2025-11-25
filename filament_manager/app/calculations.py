"""
Filament Manager - Calculations Module
Fonctions de calculs pour les coûts et statistiques
"""

from typing import Dict


def calculate_print_cost(initial_weight: float, total_cost: float, 
                        weight_used: float) -> float:
    """
    Calcule le coût d'une impression basé sur la consommation
    
    Args:
        initial_weight: Poids initial de la bobine (g)
        total_cost: Coût total de la bobine (€)
        weight_used: Poids utilisé pour l'impression (g)
    
    Returns:
        Coût de l'impression (€)
    """
    if initial_weight <= 0:
        return 0.0
    
    cost_per_gram = total_cost / initial_weight
    return round(weight_used * cost_per_gram, 2)


def get_remaining_percentage(current_weight: float, initial_weight: float) -> int:
    """
    Calcule le pourcentage restant de filament
    
    Args:
        current_weight: Poids actuel (g)
        initial_weight: Poids initial (g)
    
    Returns:
        Pourcentage restant (0-100)
    """
    if initial_weight <= 0:
        return 0
    
    percentage = (current_weight / initial_weight) * 100
    return max(0, min(100, int(percentage)))


def is_low_stock(current_weight: float, threshold: float) -> bool:
    """
    Détermine si le stock est faible
    
    Args:
        current_weight: Poids actuel (g)
        threshold: Seuil d'alerte (g)
    
    Returns:
        True si stock faible
    """
    return current_weight <= threshold


def format_currency(amount: float, currency: str = "EUR") -> str:
    """
    Formate un montant avec la devise
    
    Args:
        amount: Montant
        currency: Code devise (EUR, USD, etc.)
    
    Returns:
        Montant formaté
    """
    symbols = {
        "EUR": "€",
        "USD": "$",
        "GBP": "£"
    }
    
    symbol = symbols.get(currency, currency)
    
    if currency in ["EUR", "GBP"]:
        return f"{amount:.2f} {symbol}"
    else:
        return f"{symbol} {amount:.2f}"


def format_weight(weight: float, unit: str = "g") -> str:
    """
    Formate un poids avec l'unité
    
    Args:
        weight: Poids
        unit: Unité (g, kg)
    
    Returns:
        Poids formaté
    """
    if unit == "kg":
        return f"{weight / 1000:.2f} kg"
    else:
        return f"{int(weight)} g"
