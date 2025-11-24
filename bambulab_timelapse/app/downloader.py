"""
Bambulab Timelapse Downloader - Cloud API Version
Downloads timelapse videos from Bambu Lab P1S printer via Cloud API + FTP
"""
import os
import subprocess
from pathlib import Path
from datetime import datetime
from pybambu import BambuClient
import ftplib

class BambuTimelapseDownloader:
    """Downloads and converts timelapses from Bambu Lab printer via Cloud API"""
    
    def __init__(self, email, password, region, serial, output_dir="/share/bambulab_timelapses"):
        self.email = email
        self.password = password
        self.region = region
        self.serial = serial
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.client = None
        self.printer_ip = None
        self.access_code = None
        
    def authenticate(self):
        """Authenticate with Bambu Cloud and get printer info"""
        try:
            print(f"[CLOUD] Authentification Bambu Cloud ({self.region})...", flush=True)
            self.client = BambuClient(
                email=self.email,
                password=self.password,
                region=self.region
            )
            
            # Get printer details
            printers = self.client.get_device_list()
            printer = next((p for p in printers if p['dev_id'] == self.serial), None)
            
            if not printer:
                print(f"[CLOUD] Imprimante {self.serial} non trouvée", flush=True)
                return False
            
            self.printer_ip = printer.get('dev_ip')
            self.access_code = printer.get('access_code')
            
            print(f"[CLOUD] Authentifié - IP: {self.printer_ip}", flush=True)
            return True
            
        except Exception as e:
            print(f"[CLOUD] Erreur auth: {e}", flush=True)
            import traceback
            traceback.print_exc()
            return False
    
    def connect_ftp(self):
        """Connect to printer via FTPS using cloud-provided credentials"""
        if not self.printer_ip or not self.access_code:
            print("[FTP] Authentification cloud requise d'abord", flush=True)
            if not self.authenticate():
                return None
        
        try:
            print(f"[FTP] Connexion FTPS à {self.printer_ip}:990...", flush=True)
            ftp = ftplib.FTP_TLS()
            ftp.set_debuglevel(0)  # Disable verbose logging
            ftp.connect(self.printer_ip, 990, timeout=10)
            print(f"[FTP] Login avec bblp...", flush=True)
            ftp.login("bblp", self.access_code)
            ftp.prot_p()  # Enable secure data connection
            print(f"[FTP] Connecté", flush=True)
            return ftp
        except Exception as e:
            print(f"[FTP] Erreur connexion: {e}", flush=True)
            import traceback
            traceback.print_exc()
            return None
    
    def list_timelapses(self):
        """List all available timelapses on printer SD card"""
        print(f"[FTP] Liste des timelapses...", flush=True)
        ftp = self.connect_ftp()
        if not ftp:
            print("[FTP] Échec connexion", flush=True)
            return []
        
        try:
            # Try different possible paths
            paths_to_try = ["/timelapse", "/sdcard/timelapse", "/"]
            timelapse_files = []
            
            for path in paths_to_try:
                try:
                    print(f"[FTP] Essai du chemin: {path}", flush=True)
                    ftp.cwd(path)
                    files = []
                    ftp.retrlines('LIST', files.append)
                    
                    print(f"[FTP] {len(files)} fichiers trouvés dans {path}", flush=True)
                    
                    for line in files:
                        parts = line.split()
                        if len(parts) >= 9:
                            filename = parts[-1]
                            if filename.endswith(('.avi', '.mp4')):
                                timelapse_files.append(filename)
                                print(f"[FTP] Timelapse: {filename}", flush=True)
                    
                    if timelapse_files:
                        break  # Found timelapses, stop searching
                        
                except Exception as e:
                    print(f"[FTP] Pas de timelapses dans {path}: {e}", flush=True)
                    continue
            
            print(f"[FTP] {len(timelapse_files)} timelapses total", flush=True)
            ftp.quit()
            return timelapse_files
            
        except Exception as e:
            print(f"[FTP] Erreur lecture: {e}", flush=True)
            import traceback
            traceback.print_exc()
            try:
                ftp.quit()
            except:
                pass
            return []
    
    def download_timelapse(self, filename):
        """Download a specific timelapse file"""
        ftp = self.connect_ftp()
        if not ftp:
            return None
        
        try:
            # Navigate to timelapse directory
            paths_to_try = ["/timelapse", "/sdcard/timelapse", "/"]
            file_found = False
            
            for path in paths_to_try:
                try:
                    ftp.cwd(path)
                    # Check if file exists
                    files = []
                    ftp.retrlines('LIST', files.append)
                    if any(filename in line for line in files):
                        file_found = True
                        break
                except:
                    continue
            
            if not file_found:
                print(f"[DOWNLOAD] Fichier {filename} introuvable", flush=True)
                ftp.quit()
                return None
            
            # Create dated subdirectory
            today = datetime.now().strftime("%Y-%m-%d")
            output_subdir = self.output_dir / today
            output_subdir.mkdir(parents=True, exist_ok=True)
            
            local_path = output_subdir / filename
            
            # Download file
            print(f"[DOWNLOAD] Téléchargement: {filename}...", flush=True)
            with open(local_path, 'wb') as f:
                ftp.retrbinary(f'RETR {filename}', f.write)
            
            ftp.quit()
            print(f"[DOWNLOAD] Terminé: {local_path}", flush=True)
            return local_path
            
        except Exception as e:
            print(f"[DOWNLOAD] Erreur: {e}", flush=True)
            import traceback
            traceback.print_exc()
            try:
                ftp.quit()
            except:
                pass
            return None
    
    def convert_to_mp4(self, input_path, resolution="original"):
        """Convert timelapse to optimized MP4"""
        output_path = input_path.with_suffix('.converted.mp4')
        
        # Resolution mapping
        res_map = {
            "1080p": "1920:1080",
            "720p": "1280:720",
            "480p": "854:480",
            "original": None
        }
        
        scale_filter = res_map.get(resolution)
        
        # Build ffmpeg command
        cmd = [
            "ffmpeg", "-i", str(input_path),
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "23",
            "-c:a", "aac",
            "-b:a", "128k",
            "-movflags", "+faststart"
        ]
        
        if scale_filter:
            cmd.extend(["-vf", f"scale={scale_filter}"])
        
        cmd.append(str(output_path))
        
        try:
            print(f"[CONVERT] Conversion en {resolution}...", flush=True)
            subprocess.run(cmd, check=True, capture_output=True)
            
            # Replace original
            os.remove(input_path)
            output_path.rename(input_path.with_suffix('.mp4'))
            
            print(f"[CONVERT] Terminé: {input_path.with_suffix('.mp4')}", flush=True)
            return input_path.with_suffix('.mp4')
        except subprocess.CalledProcessError as e:
            print(f"[CONVERT] Erreur: {e}", flush=True)
            return None
    
    def get_downloaded_files(self):
        """Get list of all downloaded timelapses"""
        files = []
        for file_path in self.output_dir.rglob("*.mp4"):
            files.append({
                "name": file_path.name,
                "path": str(file_path),
                "date": file_path.parent.name,
                "size": file_path.stat().st_size,
                "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
            })
        return sorted(files, key=lambda x: x['modified'], reverse=True)
    
    def delete_timelapse(self, filename):
        """Delete a downloaded timelapse"""
        for file_path in self.output_dir.rglob(filename):
            try:
                os.remove(file_path)
                print(f"[DELETE] Supprimé: {file_path}", flush=True)
                return True
            except Exception as e:
                print(f"[DELETE] Erreur: {e}", flush=True)
                return False
        return False
