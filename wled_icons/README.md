# 💡 WLED Icons

Générateur d'icônes personnalisées pour WLED.

Transformez vos textes et icônes en presets WLED pour matrices 8x8.

## ✨ Fonctionnalités

- 🔤 **Conversion de texte** - Créez des bannières défilantes à partir de texte
- 🖼️ **Support d'icônes** - Intégration des icônes LaMetric (cloud bit-p)
- 💡 **Matrices 8x8** - Optimisé pour les matrices LED standard WLED
- 🔌 **Intégration HA** - Fonctionne directement depuis Home Assistant
- 🖥️ **Interface simple** - Création de presets en un clic

## 🚀 Installation

1. Ajoutez ce dépôt à Home Assistant : `https://github.com/gubas/homeassistant-addons`
2. Installez l'add-on "WLED Icons"
3. Démarrez l'add-on
4. Ouvrez l'interface web via le bouton "OPEN WEB UI"

## ⚙️ Configuration

Aucune configuration n'est requise pour cet add-on. Il fonctionne dès l'installation.

## 🔌 Intégration Home Assistant

Vous pouvez automatiser l'affichage d'icônes depuis vos scripts et automations Home Assistant en utilisant des `rest_command`.

### 1. Configuration `configuration.yaml`

Ajoutez ces lignes à votre fichier `configuration.yaml` (redémarrage requis) :

```yaml
rest_command:
  wled_show_icon:
    url: "http://localhost:8234/show/icon"
    method: POST
    payload: >
      {
        "host": "{{ host }}",
        "icon_id": "{{ icon }}",
        "animate": true,
        "brightness": 128
      }
    content_type:  'application/json'

  wled_stop_animation:
    url: "http://localhost:8234/stop"
    method: POST
    content_type:  'application/json'
```

### 2. Utilisation dans une automation

Exemple d'automation qui affiche une icône quand on sonne à la porte :

```yaml
automation:
  - alias: "Sonnette Porte"
    trigger:
      - platform: state
        entity_id: binary_sensor.doorbell
        to: "on"
    action:
      - service: rest_command.wled_show_icon
        data:
          host: "192.168.1.50"  # IP de votre WLED
          icon: "2480"          # ID icône LaMetric (cloche)
      - delay: "00:00:10"
      - service: rest_command.wled_stop_animation
```

## 📖 Utilisation

1. Accédez à l'interface via le panel Home Assistant ou le bouton "OPEN WEB UI"
2. Entrez votre texte ou sélectionnez une icône
3. Le preset est automatiquement créé sur votre appareil WLED connecté

## 🛠️ Support

- **Issues** : [GitHub Issues](https://github.com/gubas/homeassistant-addons/issues)
- **Discussions** : [Community Forum](https://community.home-assistant.io/)

Pour plus de détails sur les mises à jour, consultez le [CHANGELOG](CHANGELOG.md).
