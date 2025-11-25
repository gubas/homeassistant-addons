# Filament Manager 🎨

Gestionnaire de filaments 3D pour Home Assistant avec suivi automatique de consommation et statistiques avancées.

## ✨ Fonctionnalités

- 📦 **Inventaire complet** - Gérez vos bobines de filament avec nom, type, couleur, poids et coût
- 📊 **Statistiques détaillées** - Visualisez votre consommation par type, coûts totaux, et historique
- 🔔 **Alertes de stock faible** - Notifications automatiques quand une bobine approche de la fin
- 💰 **Calcul des coûts** - Suivi précis du coût par impression
- 🎯 **Interface moderne** - Design responsive et intuitif
- 🔌 **Intégration HA** - Compatible avec l'intégration HA-Bambulab

## 📸 Aperçu

L'interface permet de :
- Voir tous vos filaments avec barres de progression visuelles
- Ajouter/Éditer/Supprimer des filaments facilement
- Enregistrer des consommations manuellement
- Consulter des statistiques en temps réel
- Recevoir des alertes de stock faible

## 🚀 Installation

1. Ajoutez ce dépôt à Home Assistant : `https://github.com/gubas/homeassistant-addons`
2. Installez l'add-on "Filament Manager"
3. Configurez les options (voir ci-dessous)
4. Démarrez l'add-on
5. Accédez à l'interface via le panel latéral

## ⚙️ Configuration

### Options disponibles

| Option | Description | Défaut |
|--------|-------------|--------|
| `printer_entity` | Entity ID de votre imprimante Bambulab | `sensor.p1s_print_progress` |
| `currency` | Devise pour les coûts (EUR, USD, GBP) | `EUR` |
| `weight_unit` | Unité de poids (g, kg) | `g` |
| `low_stock_threshold` | Seuil d'alerte stock faible (en grammes) | `200` |

### Exemple de configuration

```yaml
printer_entity: "sensor.p1s_print_progress"
currency: "EUR"
weight_unit: "g"
low_stock_threshold: 200
```

## 🔌 Intégration avec HA-Bambulab

Pour profiter du suivi automatique de consommation :

1. Installez l'intégration [HA-Bambulab](https://github.com/greghesp/ha-bambulab)
2. Configurez votre imprimante dans Home Assistant
3. Notez l'entity ID principal (ex: `sensor.p1s_print_progress`)
4. Configurez cet entity ID dans les options de Filament Manager

> **Note** : Le suivi automatique dépend des sensors exposés par l'intégration HA-Bambulab. Pour l'instant, les consommations peuvent être enregistrées manuellement.

## 📖 Utilisation

### Ajouter un filament

1. Cliquez sur "➕ Ajouter" dans la navigation
2. Remplissez les informations :
   - Nom (ex: "PLA Blanc Esun")
   - Type (PLA, PETG, ABS, TPU, etc.)
   - Couleur
   - Poids initial (généralement 1000g)
   - Coût (en devise configurée)
   - Notes (optionnel)
3. Cliquez sur "Ajouter"

### Enregistrer une consommation

1. Dans l'inventaire, cliquez sur "📉 Consommer" sur une bobine
2. Entrez le poids utilisé (en grammes)
3. Entrez le nom de l'impression (optionnel)
4. Validez

Le système calcule automatiquement le coût de l'impression et met à jour le stock restant.

### Consulter les statistiques

La page "📊 Statistiques" affiche :
- Investissement total en filaments
- Coût total des impressions
- Stock total restant
- Nombre de bobines en stock faible
- Consommation par type de filament (graphique)
- Liste des filaments en stock faible
- Historique des dernières consommations

## 🔔 Notifications

L'add-on envoie des notifications Home Assistant :
- ✅ Quand un nouveau filament est ajouté
- ⚠️ Quand un filament passe en stock faible (sous le seuil configuré)

## 🛠️ Support

- **Issues** : [GitHub Issues](https://github.com/gubas/homeassistant-addons/issues)
- **Discussions** : [GitHub Discussions](https://github.com/gubas/homeassistant-addons/discussions)

## 📝 Changelog

Voir [CHANGELOG.md](CHANGELOG.md) pour l'historique des versions.

## 📄 Licence

MIT License - Voir le dépôt principal pour les détails.

---

Développé avec ❤️ pour la communauté Home Assistant
