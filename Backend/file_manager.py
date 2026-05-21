# file_manager.py
"""
Comprehensive file management operations for JARVIS
"""

import os
import shutil
import zipfile
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
import psutil


class FileManager:
    """Handle all file operations"""
    
    @staticmethod
    def copy_file(source, destination):
        """Copy a file"""
        try:
            source = os.path.expanduser(source)
            destination = os.path.expanduser(destination)
            
            if not os.path.exists(source):
                return {"success": False, "error": f"Source file not found: {source}"}
            
            shutil.copy2(source, destination)
            return {"success": True, "message": f"File copied to {destination}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def move_file(source, destination):
        """Move a file"""
        try:
            source = os.path.expanduser(source)
            destination = os.path.expanduser(destination)
            
            if not os.path.exists(source):
                return {"success": False, "error": f"Source file not found: {source}"}
            
            shutil.move(source, destination)
            return {"success": True, "message": f"File moved to {destination}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def rename_file(file_path, new_name):
        """Rename a file"""
        try:
            file_path = os.path.expanduser(file_path)
            
            if not os.path.exists(file_path):
                return {"success": False, "error": f"File not found: {file_path}"}
            
            directory = os.path.dirname(file_path)
            new_path = os.path.join(directory, new_name)
            
            os.rename(file_path, new_path)
            return {"success": True, "message": f"File renamed to {new_name}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def delete_file(file_path):
        """Delete a file"""
        try:
            file_path = os.path.expanduser(file_path)
            
            if not os.path.exists(file_path):
                return {"success": False, "error": f"File not found: {file_path}"}
            
            os.remove(file_path)
            return {"success": True, "message": f"File deleted: {file_path}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def delete_old_files(folder_path, days=30):
        """Delete files older than specified days"""
        try:
            folder_path = os.path.expanduser(folder_path)
            
            if not os.path.exists(folder_path):
                return {"success": False, "error": f"Folder not found: {folder_path}"}
            
            cutoff_time = datetime.now() - timedelta(days=days)
            deleted_count = 0
            
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                
                if os.path.isfile(file_path):
                    file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    
                    if file_time < cutoff_time:
                        os.remove(file_path)
                        deleted_count += 1
            
            return {"success": True, "message": f"Deleted {deleted_count} old files"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def search_files(folder_path, pattern="*"):
        """Search files matching a pattern"""
        try:
            folder_path = os.path.expanduser(folder_path)
            
            if not os.path.exists(folder_path):
                return {"success": False, "error": f"Folder not found: {folder_path}"}
            
            from pathlib import Path
            results = list(Path(folder_path).rglob(pattern))
            
            return {"success": True, "files": [str(f) for f in results]}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def zip_files(source_folder, zip_path):
        """Create a zip file from a folder"""
        try:
            source_folder = os.path.expanduser(source_folder)
            zip_path = os.path.expanduser(zip_path)
            
            if not os.path.exists(source_folder):
                return {"success": False, "error": f"Folder not found: {source_folder}"}
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(source_folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, source_folder)
                        zipf.write(file_path, arcname)
            
            return {"success": True, "message": f"Files zipped to {zip_path}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def unzip_files(zip_path, extract_path):
        """Extract a zip file"""
        try:
            zip_path = os.path.expanduser(zip_path)
            extract_path = os.path.expanduser(extract_path)
            
            if not os.path.exists(zip_path):
                return {"success": False, "error": f"Zip file not found: {zip_path}"}
            
            os.makedirs(extract_path, exist_ok=True)
            
            with zipfile.ZipFile(zip_path, 'r') as zipf:
                zipf.extractall(extract_path)
            
            return {"success": True, "message": f"Files extracted to {extract_path}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def organize_desktop():
        """Organize desktop files into folders by type"""
        try:
            desktop = os.path.expanduser("~/Desktop")
            
            if not os.path.exists(desktop):
                return {"success": False, "error": "Desktop not found"}
            
            categories = {
                "Documents": [".doc", ".docx", ".pdf", ".txt", ".xls", ".xlsx"],
                "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
                "Videos": [".mp4", ".avi", ".mkv", ".mov"],
                "Audio": [".mp3", ".wav", ".flac", ".aac"],
                "Archives": [".zip", ".rar", ".7z"],
                "Code": [".py", ".js", ".html", ".css", ".java"]
            }
            
            for filename in os.listdir(desktop):
                file_path = os.path.join(desktop, filename)
                
                if os.path.isfile(file_path):
                    ext = os.path.splitext(filename)[1].lower()
                    
                    for category, extensions in categories.items():
                        if ext in extensions:
                            category_path = os.path.join(desktop, category)
                            os.makedirs(category_path, exist_ok=True)
                            shutil.move(file_path, os.path.join(category_path, filename))
                            break
            
            return {"success": True, "message": "Desktop organized"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def get_disk_space():
        """Get disk space information"""
        try:
            partitions = psutil.disk_partitions()
            disk_info = []
            
            for partition in partitions:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_info.append({
                    "drive": partition.device,
                    "mountpoint": partition.mountpoint,
                    "total_gb": round(usage.total / (1024**3), 2),
                    "used_gb": round(usage.used / (1024**3), 2),
                    "free_gb": round(usage.free / (1024**3), 2),
                    "percent": usage.percent
                })
            
            return {"success": True, "disks": disk_info}
        except Exception as e:
            return {"success": False, "error": str(e)}


# Export functions for direct use
file_manager = FileManager()
