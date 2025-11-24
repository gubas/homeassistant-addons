# Changelog

All notable changes to this project will be documented in this file.

## 0.2.0 - Migration vers Cloud API

- **BREAKING**: Changement de méthode d'authentification - utilise maintenant Bambu Cloud (email/password) au lieu de FTPS direct
- **Feature**: Intégration de la bibliothèque `pybambu` pour une auth cloud fiable
- **Feature**: Détection automatique de l'IP et du code d'accès via le cloud
- **Fix**: Résout le problème de timeout FTPS qui nécessitait le mode "LAN Only"
- **Config**: Nouvelles options : `bambu_email`, `bambu_password`, `bambu_region` (remplacent `printer_ip` et `printer_access_code`)

> [!IMPORTANT]
> **Migration** : Vous devez reconfigurer l'add-on avec vos identifiants Bambu Cloud au lieu de l'IP/code d'accès.

## 0.1.4

- **Fix:** Ajout de `host_network: true` pour permettre l'accès direct au réseau local et résoudre le timeout FTPS.

## 0.1.3

- **Debug:** Ajout de logs détaillés pour diagnostiquer les problèmes de connexion FTPS et de lecture des timelapses.

## 0.1.2

- **Fix:** Correction du script `run.sh` pour utiliser bash standard au lieu de bashio.
- **Fix:** Ajout de `jq` au Dockerfile pour parser la configuration JSON.

## 0.1.1

- **Fix:** Résolution par défaut changée en "original" (la P1S filme en 720p natif, pas besoin d'upscale).

## 0.1.0

- **Initial release**: Bambulab Timelapse Downloader
- **Feature**: FTPS download from Bambu Lab P1S printer
- **Feature**: MP4 conversion with configurable resolution
- **Feature**: Web gallery interface
- **Feature**: Integration with Home Assistant media source
