# Changelog - Filament Manager

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

## [0.3.0] - 2025-11-26

### Changé
- ♻️ Migration du moteur de template vers Jinja2 pour plus de stabilité
- 🔧 Correction des erreurs de syntaxe dans les templates HTML
- 🐛 Ajout de `legacy-cgi` pour compatibilité Python 3.13+

## [0.1.0] - 2025-11-25

### Ajouté
- ✨ Interface web moderne pour la gestion des filaments
- 📦 Système d'inventaire complet (CRUD)
- 💾 Base de données SQLite pour stockage persistant
- 📊 Dashboard de statistiques avec graphiques
- 💰 Calcul automatique des coûts par impression
- 🔔 Notifications Home Assistant (ajout, stock faible)
- ⚠️ Système d'alertes pour stock faible
- 🎨 Design moderne et responsive
- 🔌 Support de l'intégration Home Assistant API
- 📝 Enregistrement manuel des consommations
- 📈 Historique complet des consommations
- 🌍 Support multi-devises (EUR, USD, GBP)
- ⚖️ Support multi-unités de poids (g, kg)
- 🎯 Filtrage et recherche dans l'inventaire
- 📱 Interface responsive (mobile/tablette/desktop)

### Notes
- Version initiale
- Intégration HA-Bambulab préparée pour futur suivi automatique
- Pas de QR codes dans cette version (peut être ajouté ultérieurement)
