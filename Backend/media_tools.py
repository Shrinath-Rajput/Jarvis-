# media_tools.py
"""
Media operations for JARVIS
"""

import subprocess
import os
from datetime import datetime


class MediaTools:
    """Handle media operations"""
    
    @staticmethod
    def play_music(file_path):
        """Play music file"""
        try:
            file_path = os.path.expanduser(file_path)
            
            if not os.path.exists(file_path):
                return {"success": False, "error": f"File not found: {file_path}"}
            
            subprocess.Popen(['powershell', '-Command', f'& {{(New-Object Media.SoundPlayer "{file_path}").PlaySync()}}']).wait()
            
            return {"success": True, "message": f"Playing {file_path}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def pause_playback():
        """Pause music playback (using media keys)"""
        try:
            import pyautogui
            pyautogui.press('mediaplaypause')
            
            return {"success": True, "message": "Playback paused"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def next_song():
        """Play next song"""
        try:
            import pyautogui
            pyautogui.press('medianexttrack')
            
            return {"success": True, "message": "Playing next song"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def previous_song():
        """Play previous song"""
        try:
            import pyautogui
            pyautogui.press('mediaprevioustrack')
            
            return {"success": True, "message": "Playing previous song"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def convert_video(input_path, output_path, format_type="mp4"):
        """Convert video file"""
        try:
            input_path = os.path.expanduser(input_path)
            output_path = os.path.expanduser(output_path)
            
            if not os.path.exists(input_path):
                return {"success": False, "error": f"File not found: {input_path}"}
            
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Using ffmpeg if available
            cmd = f'ffmpeg -i "{input_path}" "{output_path}"'
            subprocess.run(cmd, shell=True, capture_output=True)
            
            if os.path.exists(output_path):
                return {"success": True, "message": f"Video converted to {output_path}"}
            else:
                return {"success": False, "error": "Conversion failed"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def edit_image(image_path, operation="resize", params=None):
        """Edit image file"""
        try:
            from PIL import Image, ImageFilter, ImageOps
            
            image_path = os.path.expanduser(image_path)
            
            if not os.path.exists(image_path):
                return {"success": False, "error": f"Image not found: {image_path}"}
            
            img = Image.open(image_path)
            
            if operation == "resize" and params:
                width, height = params.get("width", 800), params.get("height", 600)
                img = img.resize((width, height))
            elif operation == "rotate" and params:
                angle = params.get("angle", 90)
                img = img.rotate(angle)
            elif operation == "crop" and params:
                box = (params.get("left", 0), params.get("top", 0), 
                       params.get("right", 100), params.get("bottom", 100))
                img = img.crop(box)
            elif operation == "blur":
                img = img.filter(ImageFilter.BLUR)
            elif operation == "grayscale":
                img = ImageOps.grayscale(img)
            
            output_path = image_path.replace('.', f'_edited.')
            img.save(output_path)
            
            return {"success": True, "message": f"Image edited: {output_path}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def create_slideshow(image_folder, output_path, duration_per_image=3):
        """Create slideshow from images"""
        try:
            image_folder = os.path.expanduser(image_folder)
            output_path = os.path.expanduser(output_path)
            
            if not os.path.exists(image_folder):
                return {"success": False, "error": f"Folder not found: {image_folder}"}
            
            import cv2
            import glob
            
            images = sorted(glob.glob(os.path.join(image_folder, '*.jpg')) +
                          glob.glob(os.path.join(image_folder, '*.png')))
            
            if not images:
                return {"success": False, "error": "No images found in folder"}
            
            first_image = cv2.imread(images[0])
            height, width, layers = first_image.shape
            
            video = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), 
                                   1/duration_per_image, (width, height))
            
            for image_path in images:
                video.write(cv2.imread(image_path))
            
            video.release()
            
            return {"success": True, "message": f"Slideshow created: {output_path}"}
        except Exception as e:
            return {"success": False, "error": str(e)}


# Export
media_tools = MediaTools()
