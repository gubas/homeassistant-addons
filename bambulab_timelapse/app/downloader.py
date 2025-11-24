"""
Bambulab Timelapse Downloader
Downloads timelapse videos from Bambu Lab P1S printer via FTPS
"""
import ftplib
import os
import subprocess
import json
from pathlib import Path
from datetime import datetime

class BambuTimelapseDownloader:
    """Downloads and converts timelapses from Bambu Lab printer"""
    
    def __init__(self, printer_ip, access_code, serial, output_dir="/share/bambulab_timelapses"):
        self.printer_ip = printer_ip
        self.access_code = access_code
        self.serial = serial
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # FTP paths on printer
        self.ftp_base_path = "/timelapse"
        
    def connect_ftp(self):
        """Connect to printer via FTPS"""
        try:
            print(f"[FTP] Connexion FTPS à {self.printer_ip}:990...", flush=True)
            ftp = ftplib.FTP_TLS()
            ftp.set_debuglevel(2)  # Enable verbose FTP logging
            ftp.connect(self.printer_ip, 990, timeout=10)
            print(f"[FTP] Connexion établie, login avec bblp...", flush=True)
            ftp.login("bblp", self.access_code)
            print(f"[FTP] Login réussi, activation mode sécurisé...", flush=True)
            ftp.prot_p()  # Enable secure data connection
            print(f"[FTP] Connecté à {self.printer_ip}", flush=True)
            return ftp
        except Exception as e:
            print(f"[FTP] Erreur de connexion: {e}", flush=True)
            import traceback
            traceback.print_exc()
            return None
    
    def list_timelapses(self):
        """List all available timelapses on printer"""
        print(f"[FTP] Tentative de connexion à {self.printer_ip}:990...", flush=True)
        ftp = self.connect_ftp()
        if not ftp:
            print("[FTP] Échec de connexion", flush=True)
            return []
        
        try:
            print(f"[FTP] Connexion réussie, accès au dossier {self.ftp_base_path}", flush=True)
            ftp.cwd(self.ftp_base_path)
            print("[FTP] Lecture de la liste des fichiers...", flush=True)
            
            files = []
            ftp.retrlines('LIST', files.append)
            
            print(f"[FTP] {len(files)} fichiers trouvés", flush=True)
            for line in files[:5]:  # Show first 5 for debug
                print(f"[FTP DEBUG] {line}", flush=True)
            
            # Parse file list
            timelapse_files = []
            for line in files:
                parts = line.split()
                if len(parts) >= 9:
                    filename = parts[-1]
                    if filename.endswith(('.avi', '.mp4')):
                        timelapse_files.append(filename)
                        print(f"[FTP] Timelapse trouvé: {filename}", flush=True)
            
            print(f"[FTP] {len(timelapse_files)} timelapses au total", flush=True)
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
            ftp.cwd(self.ftp_base_path)
            
            # Create dated subdirectory
            today = datetime.now().strftime("%Y-%m-%d")
            output_subdir = self.output_dir / today
            output_subdir.mkdir(parents=True, exist_ok=True)
            
            local_path = output_subdir / filename
            
            # Download file
            print(f"[DOWNLOAD] Téléchargement: {filename}...")
            with open(local_path, 'wb') as f:
                ftp.retrbinary(f'RETR {filename}', f.write)
            
            ftp.quit()
            print(f"[DOWNLOAD] Terminé: {local_path}")
            return local_path
            
        except Exception as e:
            print(f"[DOWNLOAD] Erreur: {e}")
            try:
                ftp.quit()
            except:
                pass
            return None
    
    def convert_to_mp4(self, input_path, resolution="1080p"):
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
            print(f"[CONVERT] Conversion en {resolution}...")
            subprocess.run(cmd, check=True, capture_output=True)
            
            # Replace original
            os.remove(input_path)
            output_path.rename(input_path.with_suffix('.mp4'))
            
            print(f"[CONVERT] Terminé: {input_path.with_suffix('.mp4')}")
            return input_path.with_suffix('.mp4')
        except subprocess.CalledProcessError as e:
            print(f"[CONVERT] Erreur: {e}")
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
                print(f"[DELETE] Supprimé: {file_path}")
                return True
            except Exception as e:
                print(f"[DELETE] Erreur: {e}")
                return False
        return False
