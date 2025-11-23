



# Changelog

## 0.4.2

- **Chore:** Ajout de logs de débogage pour analyser les problèmes de détection d'utilisateur.

## 0.4.1

- **Fix:** Ajout de la dépendance manquante `beautifulsoup4`.

## 0.4.0

- **Feature:** Extraction automatique des métadonnées MakerWorld (Poids, AMS, Couleurs).
- **Feature:** Affichage des badges de filaments et AMS dans la queue.
- **Fix:** Nettoyage du code et suppression de configurations redondantes.

## [0.3.9] - 2025-11-23

### Added
- Affichage du nom de l'utilisateur courant sur la page d'accueil
- Pré-remplissage du champ "Votre nom" avec l'utilisateur Home Assistant

### Fixed
- Correction affichage queue vide (problème path Ingress)
- Amélioration robustesse navigation (chemins relatifs)
- Nettoyage code rendu serveur inutile

## [0.3.7] - 2025-11-23

### Debug
- Ajout print [DEBUG] Démarrage app.py (version 0.3.6) pour vérifier le code exécuté
 
## [0.3.8] - 2025-11-23

### Debug
- Affichage des premières lignes de `/app/app.py` au démarrage (via `run.sh`) pour vérifier le code réellement copié dans l'image Docker

### Debug
- Ajout de logs détaillés pour chaque étape du POST /submit (données reçues, sauvegarde queue, appel to-do, exceptions)

### Fixed
- Bouton "Voir la queue" compatible ingress (chemin dynamique)
- Log d'erreur explicite si ajout à la to-do échoue
- Route POST /submit et /submit/ bien exposées et versionnées sur GitHub

### Fixed
- Bouton "Voir la queue" compatible ingress (chemin dynamique)
- Log d'erreur explicite si ajout à la to-do échoue
- Route POST /submit et /submit/ bien exposées et versionnées sur GitHub

## [0.3.3] - 2025-11-22

### Fixed
- Support complet Ingress : accepte aussi POST sur /submit/ (slash final)

## [0.3.2] - 2025-11-22

### Fixed
- Compatibilité Ingress : correction du chemin dynamique pour /submit dans le JS (window.location.pathname)

## [0.3.1] - 2025-11-22

### Fixed
- Correction bug champ nom optionnel

## [0.3.0] - 2025-11-22

### Added
- Support Ingress Home Assistant pour accès sécurisé
- Icône dans la sidebar (panel_icon: mdi:printer-3d)
- Panel accessible depuis la sidebar Home Assistant
- Variable d'environnement INGRESS_PATH pour routing

### Fixed
- Interface web maintenant accessible via Ingress
- Détection automatique du username via header X-Ingress-User fonctionnelle
- Suppression du champ image obsolète dans config.yaml

## [0.2.0] - 2025-11-22

### Changed
- Migration de Flask vers Bottle (framework ultra-léger)
- Simplification drastique : uniquement liens MakerWorld
- Optimisation Dockerfile (Alpine Linux optimisé)
- Réduction des dépendances (2 au lieu de 3)

### Added
- Détection automatique du nom d'utilisateur Home Assistant via header X-Ingress-User
- Champs optionnels : nom du modèle et requester auto-détectés
- Documentation complète mise à jour

### Removed
- Support Thingiverse
- Upload de fichiers STL
- Estimation de poids via PrusaSlicer
- Vérification de stock de filament
- PrusaSlicer CLI du conteneur Docker
- BeautifulSoup, numpy-stl, Werkzeug

### Fixed
- Image Docker plus légère (~90 MB vs ~300 MB)
- Démarrage plus rapide
- Interface simplifiée et plus claire
