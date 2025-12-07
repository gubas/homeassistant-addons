# 🖨️ Queue d'impression 3D

**Version 0.3.0**

Interface web familiale ultra-simple pour gérer les demandes d'impression 3D via MakerWorld.

> 🎯 **Le problème résolu** : Vos enfants/conjoint vous envoient des liens MakerWorld par message ? Cette solution centralise toutes les demandes dans Home Assistant avec une queue simple et claire.

## ✨ Fonctionnalités

- 📱 **Interface web minimaliste** - Parfait pour toute la famille
- 🔗 **Liens MakerWorld uniquement** - Simple et direct
- 🎨 **Choix de couleur** - 8 couleurs de filament
- ✅ **To-Do List intégrée** - Ajout automatique dans Home Assistant
- 🔔 **Notifications** - Alertes lors de nouvelles demandes
- 👤 **Détection automatique** - Récupère le nom d'utilisateur Home Assistant
- 📋 **Vue de la queue** - Suivez toutes les demandes en attente

## 🚀 Installation

1. Ajoutez ce dépôt à Home Assistant : `https://github.com/gubas/homeassistant-addons`
2. Installez l'add-on "3D Print Queue"
3. Configurez l'add-on (voir section Configuration)
4. Démarrez l'add-on
5. Accédez à l'interface via le bouton "OPEN WEB UI"

## ⚙️ Configuration

### Option obligatoire

| Option | Description | Exemple |
|--------|-------------|---------|
| `todo_list` | Entity ID de la To-Do List HA | `todo.impressions_3d` |

### Exemple de configuration

```yaml
todo_list: todo.impressions_3d
```

> **Note** : Vous devez créer une To-Do List "Local" dans Home Assistant avant de démarrer l'add-on.

## 📖 Utilisation

### Soumettre une demande

1. **Ouvrez l'interface** web
2. **Collez le lien** MakerWorld (ex: `https://makerworld.com/en/models/123456`)
3. **Choisissez une couleur**
4. **Validez** : La demande est ajoutée à la queue et une notification est envoyée

### Gérer la queue

- Consultez la liste des demandes en attente
- Imprimez les modèles demandés
- Supprimez les demandes terminées

## 🔧 Configuration Avancée (Home Assistant)

### Notifications

Pour recevoir des notifications, créez une automation :

```yaml
automation:
  - alias: "Nouvelle impression 3D"
    trigger:
      platform: state
      entity_id: todo.impressions_3d
    action:
      - service: notify.mobile_app_votre_telephone
        data:
          title: "🖨️ Nouvelle demande d'impression"
          message: "Consulte la queue d'impression"
```

## 🛠️ Support

- **Issues** : [GitHub Issues](https://github.com/gubas/homeassistant-addons/issues)
- **Discussions** : [Community Forum](https://community.home-assistant.io/)

## 📄 Licence

MIT License - Voir le dépôt principal pour les détails.

---

Développé avec ❤️ pour la communauté Home Assistant
