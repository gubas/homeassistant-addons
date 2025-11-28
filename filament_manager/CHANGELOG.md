# Changelog - Filament Manager

Toutes les modifications notables de ce projet seront documentées dans ce fichier.



## 0.4.7

- ✨ Amélioration : Affichage de tous les slots AMS même vides (pour bobines non-Bambulab)

## 0.4.6

- 🔍 Debug : Ajout de logs au niveau de la route API

## 0.4.5

- 🔍 Debug : Ajout de logs détaillés pour le scan AMS

## 0.4.4

- ✨ Amélioration : Support automatique des formats de noms AMS (ex: `ams_1_emplacement_1`)

## 0.4.3

- 🐛 Fix : Correction du crash au démarrage (variable PORT manquante)

## 0.4.2

- ✨ Ajout du support AMS : Visualisation des slots et activation rapide
- 🐛 Fix : Suppression et activation impossibles si le nom contient des guillemets
- 🔧 Config : Ajout de l'option `ams_tray_prefix`

## [0.4.1] - 2025-11-26

### Changé
- 🔧 Configuration complète des entités d'imprimante (`printer_status_entity`, `printer_weight_entity`)
- 🔧 Port configurable via les options de l'add-on
- 📝 Suppression de l'ancienne variable `printer_entity` obsolète

## [0.4.0] - 2025-11-26

### Ajouté
- ⭐ **Automatisation de la consommation** : Décompte automatique du stock quand une impression se termine
- 🤖 Monitoring en arrière-plan de l'imprimante via l'intégration Bambulab
- 🎯 Sélection du filament actif avec badge visuel animé
- 🔔 Notifications automatiques après déduction du stock
- 📡 API endpoint pour définir le filament actif

### Changé
- 💾 Ajout de la colonne `is_active` à la base de données (migration automatique)
- 🎨 Interface améliorée avec indicateur du filament actif

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
