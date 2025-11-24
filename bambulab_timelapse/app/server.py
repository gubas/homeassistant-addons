"""
Web server for Bambulab Timelapse add-on
Provides UI for viewing and managing timelapses
"""
print("[INFO] Démarrage server.py (version 0.1.4)", flush=True)

from bottle import Bottle, request, response, static_file, template, run
import os
import json
from pathlib import Path
from downloader import BambuTimelapseDownloader

app = Bottle()

# Configuration from Home Assistant
PRINTER_IP = os.environ.get('PRINTER_IP', '')
PRINTER_CODE = os.environ.get('PRINTER_ACCESS_CODE', '')
PRINTER_SERIAL = os.environ.get('PRINTER_SERIAL', '')
AUTO_DOWNLOAD = os.environ.get('AUTO_DOWNLOAD', 'true').lower() == 'true'
CONVERT_MP4 = os.environ.get('CONVERT_TO_MP4', 'true').lower() == 'true'
RESOLUTION = os.environ.get('RESOLUTION', 'original')
OUTPUT_DIR = "/share/bambulab_timelapses"

# Load config from /data/options.json
OPTIONS_FILE = Path('/data/options.json')
if OPTIONS_FILE.exists():
    try:
        with open(OPTIONS_FILE, 'r') as f:
            options = json.load(f)
            PRINTER_IP = options.get('printer_ip', PRINTER_IP)
            PRINTER_CODE = options.get('printer_access_code', PRINTER_CODE)
            PRINTER_SERIAL = options.get('printer_serial', PRINTER_SERIAL)
            AUTO_DOWNLOAD = options.get('auto_download', AUTO_DOWNLOAD)
            CONVERT_MP4 = options.get('convert_to_mp4', CONVERT_MP4)
            RESOLUTION = options.get('resolution', RESOLUTION)
            print(f"[CONFIG] Imprimante: {PRINTER_IP}", flush=True)
    except Exception as e:
        print(f"[CONFIG] Erreur lecture options.json: {e}", flush=True)

# Initialize downloader
downloader = BambuTimelapseDownloader(PRINTER_IP, PRINTER_CODE, PRINTER_SERIAL, OUTPUT_DIR)


@app.route('/')
def index():
    """Page principale - galerie de timelapses"""
    html_file = Path(__file__).parent / 'templates' / 'index.html'
    return html_file.read_text()


@app.route('/api/timelapses')
def get_timelapses():
    """API: Liste des timelapses téléchargés"""
    response.content_type = 'application/json'
    files = downloader.get_downloaded_files()
    return json.dumps(files)


@app.route('/api/available')
def get_available_timelapses():
    """API: Liste des timelapses disponibles sur l'imprimante"""
    response.content_type = 'application/json'
    files = downloader.list_timelapses()
    return json.dumps(files)


@app.route('/api/download', method=['POST'])
def download_timelapse():
    """API: Télécharge un timelapse depuis l'imprimante"""
    response.content_type = 'application/json'
    try:
        filename = request.forms.get('filename', '').strip()
        if not filename:
            response.status = 400
            return json.dumps({'error': 'Filename requis'})
        
        print(f"[API] Téléchargement demandé: {filename}", flush=True)
        local_path = downloader.download_timelapse(filename)
        
        if not local_path:
            response.status = 500
            return json.dumps({'error': 'Échec du téléchargement'})
        
        # Convert if enabled
        if CONVERT_MP4:
            converted_path = downloader.convert_to_mp4(local_path, RESOLUTION)
            if not converted_path:
                return json.dumps({'message': 'Téléchargé mais conversion échouée', 'path': str(local_path)})
            local_path = converted_path
        
        return json.dumps({'message': 'Téléchargement réussi', 'path': str(local_path)})
        
    except Exception as e:
        print(f"[API] Erreur: {e}", flush=True)
        response.status = 500
        return json.dumps({'error': str(e)})


@app.route('/api/delete/<filename>', method=['DELETE'])
def delete_timelapse(filename):
    """API: Supprime un timelapse"""
    response.content_type = 'application/json'
    success = downloader.delete_timelapse(filename)
    if success:
        return json.dumps({'success': True})
    else:
        response.status = 404
        return json.dumps({'error': 'Fichier non trouvé'})


@app.route('/video/<date>/<filename>')
def serve_video(date, filename):
    """Sert les fichiers vidéo"""
    video_dir = Path(OUTPUT_DIR) / date
    return static_file(filename, root=str(video_dir))


@app.route('/static/<filename>')
def serve_static(filename):
    """Sert les fichiers statiques"""
    static_dir = Path(__file__).parent / 'static'
    return static_file(filename, root=str(static_dir))


if __name__ == '__main__':
    print(f"[SERVER] Démarrage sur le port 8099", flush=True)
    run(app, host='0.0.0.0', port=8099, server='wsgiref')
