# 💡 WLED Icons ![Version](https://img.shields.io/badge/version-v1.0.14-blue)

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

## 🔌 Intégration Native Home Assistant
 
 Une intégration native est incluse avec cet add-on pour faciliter son utilisation dans Home Assistant.
 
 ### 1. Installation de l'intégration
 
 **Automatique (Recommandé) :**
 L'intégration est installée automatiquement au démarrage de l'add-on. Redémarrez simplement Home Assistant après le premier démarrage de l'add-on, puis ajoutez l'intégration "WLED Icons".
 
 **Manuelle (Si l'automatique échoue) :**
 1. Copiez le dossier `wled_icons/integration` de ce dépôt vers `/config/custom_components/wled_icons`.
 2. Redémarrez Home Assistant.
 3. Allez dans **Paramètres → Appareils et services**.
 4. Cliquez sur **Ajouter une intégration** et cherchez **WLED Icons**.
 
 ### 2. Utilisation dans une automation
 
 Utilisez le service `wled_icons.display` (anciennement `show_lametric`).
 
 Exemple d'automation (Sonnette) :
 
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
           icon_id: "2480"       # ID icône LaMetric (cloche)
           host: "192.168.1.50"  # IP de votre WLED
           animate: true
           brightness: 200
       - delay: "00:00:10"
       - service: wled_icons.stop
         data:
             host: "192.168.1.50"
 ```
 
 ### Services disponibles
 
 - **wled_icons.display** : Affiche une icône ou une animation.
   - `icon_id` (Requis) : ID de l'icône (ex: `1486`).
   - `host` : IP du WLED.
   - `color` : Couleur hexadécimale pour recolorier l'icône (ex: `#FF0000`).
   - `animate` : `true` pour animer les GIFs.
   - `rotate` : Rotation (0, 90, 180, 270).

- **wled_icons.stop** : Arrête l'animation en cours.

## 📖 Utilisation

1. Accédez à l'interface via le panel Home Assistant ou le bouton "OPEN WEB UI"
2. Entrez votre texte ou sélectionnez une icône
3. Le preset est automatiquement créé sur votre appareil WLED connecté

## 🛠️ Support

- **Issues** : [GitHub Issues](https://github.com/gubas/homeassistant-addons/issues)
- **Discussions** : [Community Forum](https://community.home-assistant.io/)

Pour plus de détails sur les mises à jour, consultez le [CHANGELOG](CHANGELOG.md).
