# 🖨️ Queue d'impression 3D - Add-on Home Assistant

**Version 0.3.0**

Interface web familiale ultra-simple pour gérer les demandes d'impression 3D via MakerWorld.

## 🎯 Le problème résolu

Vos enfants/conjoint vous envoient des liens MakerWorld par message ? Cette solution centralise toutes les demandes dans Home Assistant avec une queue simple et claire.

## ✨ Fonctionnalités

- 📱 **Interface web minimaliste** - Parfait pour toute la famille
- 🔗 **Liens MakerWorld uniquement** - Simple et direct
- 🎨 **Choix de couleur** - 8 couleurs de filament
- ✅ **To-Do List intégrée** - Ajout automatique dans Home Assistant
- 🔔 **Notifications** - Alertes lors de nouvelles demandes
- 👤 **Détection automatique** - Récupère le nom d'utilisateur Home Assistant
- 📋 **Vue de la queue** - Suivez toutes les demandes en attente
- 🪶 **Ultra-léger** - Bottle framework (~90 MB image Alpine)

## 📦 Installation

### Méthode 1 : Via le store Home Assistant (Recommandé)

1. Ajoutez ce repository à vos add-on stores :
   - Supervisor → Add-on Store → ⋮ (menu) → Repositories
   - Ajoutez : `https://github.com/gubas/ha_3Dqueue`

2. Installez l'add-on "3D Print Queue"

3. Configurez l'add-on (voir section Configuration)

4. Démarrez l'add-on

### Méthode 2 : Installation manuelle

1. Copiez le dossier `ha_3Dqueue` dans `/addons/`
2. Rechargez Home Assistant
3. L'add-on apparaîtra dans le store

## ⚙️ Configuration

### Configuration minimale

```yaml
todo_list: todo.impressions_3d
```

C'est tout ! Plus besoin de configurer de capteurs ou de paramètres compliqués.

## 🚀 Utilisation

### 1. Accéder à l'interface

Ouvrez l'add-on via le bouton "OPEN WEB UI" ou accédez directement à :
```
http://homeassistant.local:5000
```

### 2. Soumettre une demande

1. **Nom du modèle** (optionnel) - Auto-détecté depuis l'URL si vide
2. **Votre nom** (optionnel) - Utilise votre compte Home Assistant si vide
3. **Lien MakerWorld** (requis) - Ex: `https://makerworld.com/en/models/123456`
4. **Couleur** - Choisissez parmi les 8 couleurs disponibles

Cliquez sur "Ajouter à la queue" et c'est fait !

### 3. Gérer la queue

Cliquez sur "Voir la queue" pour :
- Voir toutes les demandes en attente
- Consulter les détails (nom, couleur, demandeur, lien)
- Supprimer des éléments

## 🔧 Configuration Home Assistant

### Créer une To-Do List

Dans `configuration.yaml` :

```yaml
todo:
  - platform: local_todo
    name: Impressions 3D
```

Redémarrez Home Assistant, puis configurez l'add-on avec :
```yaml
todo_list: todo.impressions_3d
```

## 📱 Intégrations

### Notifications automatiques

L'add-on envoie automatiquement une notification via `notify.notify` à chaque nouvelle demande.

Pour personnaliser les notifications, créez une automation :

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

### Tableau de bord

Ajoutez une carte To-Do List dans votre dashboard :

```yaml
type: todo-list
entity: todo.impressions_3d
title: 🖨️ Queue d'impression 3D
```

## 🏗️ Architecture technique

- **Framework** : Bottle (micro-framework Python ultra-léger)
- **Base image** : Alpine Linux (~90 MB)
- **Dépendances** : bottle, requests
- **Stockage** : JSON local (`/data/queue.json`)
- **API** : Home Assistant Supervisor API
- **Auth** : Ingress avec détection automatique utilisateur

## 🔒 Sécurité

- Accès via Ingress Home Assistant (authentification intégrée)
- Validation stricte des URLs MakerWorld
- Aucun accès externe direct
- Stockage local sécurisé

## 🛠️ Développement

### Structure du projet

```
ha_3Dqueue/
├── app/
│   ├── app.py              # Application Bottle
│   └── templates/
│       ├── index.html      # Formulaire de soumission
│       └── queue.html      # Vue de la queue
├── config.yaml             # Configuration add-on
├── Dockerfile              # Image Alpine optimisée
├── build.yaml              # Multi-architecture
├── requirements.txt        # Dépendances Python
├── run.sh                  # Script de démarrage
└── README.md               # Cette doc
```

### Tester localement

```bash
# Installer les dépendances
pip install -r requirements.txt

# Variables d'environnement
export TODO_LIST="todo.impressions_3d"
export SUPERVISOR_TOKEN="votre_token"
export HA_URL="http://homeassistant.local:8123"

# Lancer l'app
python app/app.py
```

## 📝 Workflow typique

1. Un membre de la famille trouve un modèle sur MakerWorld
2. Il copie le lien
3. Il ouvre l'add-on et colle le lien
4. Il choisit la couleur souhaitée
5. Il soumet → automatiquement :
   - Ajouté à la queue locale
   - Ajouté à la To-Do List HA
   - Notification envoyée
6. Vous consultez la queue et imprimez !

## 🤝 Contribution

Les contributions sont bienvenues ! N'hésitez pas à :
- Ouvrir des issues pour les bugs
- Proposer des améliorations
- Soumettre des pull requests

## 📄 Licence

MIT License - Voir le fichier LICENSE

## 🙏 Remerciements

- Home Assistant pour l'écosystème add-on
- MakerWorld pour les modèles 3D
- Bottle pour le micro-framework léger

## 💡 FAQ

**Q: Pourquoi uniquement MakerWorld ?**  
A: Pour garder l'add-on simple et léger. MakerWorld est la plateforme principale pour Bambu Lab.

**Q: Puis-je uploader des fichiers STL ?**  
A: Non, volontairement retiré pour simplifier. Utilisez MakerWorld comme source unique.

**Q: Comment récupérer les fichiers depuis MakerWorld ?**  
A: Manuellement via le lien fourni dans la queue. Pas de téléchargement automatique.

**Q: L'add-on peut-il lancer l'impression automatiquement ?**  
A: Non, c'est une queue de demandes uniquement. L'impression reste manuelle.

**Q: Puis-je modifier les couleurs disponibles ?**  
A: Oui, éditez `FILAMENT_COLORS` dans `app/app.py`.

## 🐛 Support

- **Issues** : [GitHub Issues](https://github.com/gubas/ha_3Dqueue/issues)
- **Discussions** : [Community Forum](https://community.home-assistant.io/)

---

**Fait avec ❤️ pour la communauté Home Assistant**
