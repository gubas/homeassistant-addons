# Bambulab Timelapse Downloader

Télécharge et convertit automatiquement les timelapses de votre imprimante Bambu Lab P1S.

## Fonctionnalités

- 📥 Téléchargement automatique des timelapses via FTPS
- 🎬 Conversion en MP4 optimisé (1080p, 720p, 480p)
- 🖼️ Galerie web pour visionner vos timelapses
- 🗑️ Gestion des vidéos (lecture, téléchargement, suppression)
- 🔔 Intégration avec Home Assistant (notifications, media source)

## Installation

1. Ajoutez ce repository à vos add-ons Home Assistant
2. Installez l'add-on "Bambulab Timelapse"
3. Configurez les paramètres depuis l'interface

## Configuration

### Paramètres requis

| Paramètre | Description |
|-----------|-------------|
| `bambu_email` | Email de votre compte Bambu Lab |
| `bambu_password` | Mot de passe Bambu Lab |
| `bambu_region` | Région (China, Europe, USA) |
| `printer_serial` | Numéro de série de l'imprimante |

### Paramètres optionnels

| Paramètre | Description | Défaut |
|-----------|-------------|---------|
| `auto_download` | Téléchargement automatique | `true` |
| `convert_to_mp4` | Conversion en MP4 | `true` |
| `resolution` | Résolution (original, 1080p, 720p, 480p) | `1080p` |
| `notify_on_complete` | Notifications | `true` |

## Utilisation

### Via l'interface web

1. Accédez à l'add-on via le panneau Home Assistant
2. Cliquez sur "Télécharger depuis l'imprimante"
3. Sélectionnez le timelapse à télécharger
4. La vidéo sera convertie et ajoutée à la galerie

### Via Home Assistant

Les timelapses sont automatiquement disponibles dans :
- **Media Browser** → `bambulab_timelapses`
- **Dossier partagé** : `/share/bambulab_timelapses/`

### Organisation des fichiers

```
/share/bambulab_timelapses/
├── 2025-01-15/
│   ├── print_001.mp4
│   └── print_002.mp4
├── 2025-01-16/
│   └── print_003.mp4
```

## Troubleshooting

### Impossible de se connecter

- Vérifiez que vos **identifiants Bambu Cloud** sont corrects
- Vérifiez la **région** (China pour les comptes `.cn`, Europe/USA pour les autres)
- Assurez-vous que votre imprimante est connectée au cloud

### Timelapses non trouvés

- Vérifiez que l'imprimante est allumée et connectée au réseau
- Assurez-vous que des timelapses ont été créés (fonction activée sur l'imprimante)

### Conversion échoue

- Vérifiez que `ffmpeg` est bien installé dans le conteneur
- Essayez avec `resolution: "original"` pour désactiver le scaling

### Espace disque

Les timelapses peuvent être volumineux. Surveillez l'espace disponible dans `/share`.

## Support

Pour signaler un bug ou demander une fonctionnalité, ouvrez une issue sur GitHub.

## Licence

MIT
