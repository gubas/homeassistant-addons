# 💡 WLED Icons ![Version](https://img.shields.io/badge/version-v1.0.15-blue)

Générateur d'icônes personnalisées pour WLED.

Transformez vos textes et icônes en presets WLED pour matrices 8x8.

## ✨ Fonctionnalités

- 🔤 **Conversion de texte** - Créez des bannières défilantes à partir de texte
- 🖼️ **Support d'icônes** - Intégration des icônes LaMetric (cloud bit-p)
- 💡 **Matrices 8x8** - Optimisé pour les matrices LED standard WLED
- 🔌 **Intégration Native HA** - Fonctionne directement depuis Home Assistant
- 🖥️ **Interface simple** - Création de presets en un clic
- 🔄 **Snapshot & Restore** - Restauration automatique de l'état précédent de WLED (on/off, preset, playlist) après une notification

## 🚀 Installation

1. Ajoutez ce dépôt à Home Assistant : `https://github.com/gubas/homeassistant-addons`
2. Installez l'add-on "WLED Icons"
3. Démarrez l'add-on
4. Ouvrez l'interface web via le bouton "OPEN WEB UI" pour vérifier que tout fonctionne.

**Note :** L'intégration native "WLED Icons" (nécessaire pour les automations) est installée **automatiquement** au premier démarrage de l'add-on.

### Finalisation de l'installation de l'intégration :
1. Redémarrez Home Assistant.
2. Allez dans **Paramètres → Appareils et services**.
3. L'intégration devrait être découverte automatiquement. Si ce n'est pas le cas, cliquez sur **Ajouter une intégration** et cherchez **WLED Icons**.
4. Validez la configuration (les champs sont optionnels pour la plupart des usages).

## ⚙️ Configuration Add-on

L'add-on fonctionne généralement sans configuration.
Cependant, vous pouvez ajuster les options suivantes dans l'onglet "Configuration" de l'add-on :

- `log_level`: Niveau de détails des logs (INFO par défaut).

## 🔌 Utilisation dans une automation

Utilisez les services fournis par l'intégration pour contrôler votre matrice WLED.

### Service: `wled_icons.display`
Affiche une icône, un texte ou une animation.

| Paramètre | Description | Exemple |
| :--- | :--- | :--- |
| `icon_id` | **(Requis)** ID de l'icône LaMetric | `2480` (cloche), `638` (pluie) |
| `host` | IP de votre WLED (si non configuré globalement) | `192.168.1.50` |
| `color` | Recolorier l'icône (Hex) | `#FF0000` |
| `brightness` | Luminosité (0-255) | `200` |
| `animate` | Activer l'animation (pour les GIFs) | `true` |
| `duration` | Durée max en secondes avant arrêt auto | `10` |
| `loop` | Nombre de boucles (-1 = infini) | `3` |
| `fps` | Forcer la vitesse d'animation (Frames/sec) | `15` |
| `flip_h` | Miroir Horizontal | `true` |
| `flip_v` | Miroir Vertical | `false` |
| `rotate` | Rotation (0, 90, 180, 270) | `90` |

**Exemple d'automation (Sonnette) :**
```yaml
automation:
  - alias: "Sonnette Porte"
    trigger:
      - platform: state
        entity_id: binary_sensor.doorbell
        to: "on"
    action:
      - service: wled_icons.display
        data:
          icon_id: "2480"       # Cloche
          host: "192.168.1.50"
          animate: true
          brightness: 255
          duration: 10          # S'arrête tout seul après 10s et restaure WLED
          color: "#FF0000"      # En rouge
```

### Service: `wled_icons.stop`
Arrête l'animation en cours immédiatement et restaure l'état précédent de WLED.

| Paramètre | Description |
| :--- | :--- |
| `host` | IP de votre WLED (si nécessaire) |

```yaml
action:
  - service: wled_icons.stop
    data:
      host: "192.168.1.50"
```

## 📖 Utilisation Interface Web

1. Accédez à l'interface via le bouton "OPEN WEB UI".
2. **Rechercher** : Tapez un mot clé pour trouver des icônes (ex: "Mario", "Weather").
3. **Configurer** : Réglez la luminosité, la rotation, etc.
4. **Envoyer** : Cliquez sur le bouton d'envoi pour afficher sur votre WLED.

## 🛠️ Support

- **Issues** : [GitHub Issues](https://github.com/gubas/homeassistant-addons/issues)
- **Discussions** : [Community Forum](https://community.home-assistant.io/)

Pour plus de détails sur les mises à jour, consultez le [CHANGELOG](CHANGELOG.md).
