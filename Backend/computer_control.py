"""
Computer Control System
Handles keyboard, mouse, applications, and file system operations
"""
import os
import subprocess
import logging
import pyautogui
from pathlib import Path
from config import DEBUG

logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO)
logger = logging.getLogger(__name__)

# Disable pyautogui fail-safe
pyautogui.FAILSAFE = False

class ComputerControl:
    """
    Control computer operations: keyboard, mouse, apps, files
    """
    
    def __init__(self):
        self.last_mouse_position = pyautogui.position()
        logger.info("ComputerControl initialized")
    
    # ========================
    # MOUSE OPERATIONS
    # ========================
    
    def mouse_move(self, x, y, duration=0.5):
        """Move mouse to position"""
        try:
            pyautogui.moveTo(x, y, duration=duration)
            self.last_mouse_position = (x, y)
            logger.info(f"Mouse moved to ({x}, {y})")
            return True
        except Exception as e:
            logger.error(f"Mouse move error: {str(e)}")
            return False
    
    def mouse_click(self, x=None, y=None, button='left', clicks=1, interval=0.1):
        """Click mouse"""
        try:
            if x and y:
                pyautogui.moveTo(x, y, duration=0.3)
            
            pyautogui.click(button=button, clicks=clicks, interval=interval)
            logger.info(f"Mouse clicked ({button})")
            return True
        except Exception as e:
            logger.error(f"Mouse click error: {str(e)}")
            return False
    
    def mouse_scroll(self, x, y, direction='up', amount=3):
        """Scroll mouse"""
        try:
            pyautogui.moveTo(x, y)
            scroll_value = amount if direction.lower() == 'down' else -amount
            pyautogui.scroll(scroll_value)
            logger.info(f"Scrolled {direction}")
            return True
        except Exception as e:
            logger.error(f"Mouse scroll error: {str(e)}")
            return False
    
    def get_mouse_position(self):
        """Get current mouse position"""
        return pyautogui.position()
    
    # ========================
    # KEYBOARD OPERATIONS
    # ========================
    
    def press_key(self, key):
        """Press a single key"""
        try:
            pyautogui.press(key)
            logger.info(f"Key pressed: {key}")
            return True
        except Exception as e:
            logger.error(f"Press key error: {str(e)}")
            return False
    
    def type_text(self, text, interval=0.05):
        """Type text"""
        try:
            pyautogui.typewrite(text, interval=interval)
            logger.info(f"Typed: {text[:50]}...")
            return True
        except Exception as e:
            logger.error(f"Type text error: {str(e)}")
            return False
    
    def hotkey(self, *keys):
        """Press key combination"""
        try:
            pyautogui.hotkey(*keys)
            logger.info(f"Hotkey pressed: {'+'.join(keys)}")
            return True
        except Exception as e:
            logger.error(f"Hotkey error: {str(e)}")
            return False
    
    def copy(self):
        """Copy to clipboard"""
        return self.hotkey('ctrl', 'c')
    
    def paste(self):
        """Paste from clipboard"""
        return self.hotkey('ctrl', 'v')
    
    def select_all(self):
        """Select all (Ctrl+A)"""
        return self.hotkey('ctrl', 'a')
    
    # ========================
    # APPLICATION OPERATIONS
    # ========================
    
    def open_application(self, app_name):
        """Open an application"""
        try:
            app_name = app_name.lower()
            
            # Common applications
            apps = {
                'chrome': 'chrome',
                'firefox': 'firefox',
                'edge': 'msedge',
                'vscode': 'code',
                'notepad': 'notepad',
                'calculator': 'calc',
                'excel': 'excel',
                'word': 'winword',
                'powerpoint': 'powerpnt',
                'photoshop': 'photoshop',
            }
            
            if app_name in apps:
                command = apps[app_name]
            else:
                command = app_name
            
            if os.name == 'nt':  # Windows
                os.startfile(command)
            else:  # Unix-like
                subprocess.Popen([command])
            
            logger.info(f"Opened application: {app_name}")
            return True
            
        except Exception as e:
            logger.error(f"Open application error: {str(e)}")
            return False
    
    def close_application(self, app_name=None):
        """Close an application"""
        try:
            if os.name == 'nt':  # Windows
                if app_name:
                    os.system(f'taskkill /IM {app_name}.exe /F')
                else:
                    self.hotkey('alt', 'F4')
            else:
                self.hotkey('cmd', 'Q')
            
            logger.info(f"Closed application: {app_name or 'active'}")
            return True
            
        except Exception as e:
            logger.error(f"Close application error: {str(e)}")
            return False
    
    # ========================
    # FILE OPERATIONS
    # ========================
    
    def create_folder(self, path):
        """Create a folder"""
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            logger.info(f"Folder created: {path}")
            return True
        except Exception as e:
            logger.error(f"Create folder error: {str(e)}")
            return False
    
    def create_file(self, path, content=""):
        """Create a file"""
        try:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            Path(path).write_text(content)
            logger.info(f"File created: {path}")
            return True
        except Exception as e:
            logger.error(f"Create file error: {str(e)}")
            return False
    
    def read_file(self, path):
        """Read a file"""
        try:
            content = Path(path).read_text()
            logger.info(f"File read: {path}")
            return content
        except Exception as e:
            logger.error(f"Read file error: {str(e)}")
            return None
    
    def delete_file(self, path):
        """Delete a file"""
        try:
            Path(path).unlink()
            logger.info(f"File deleted: {path}")
            return True
        except Exception as e:
            logger.error(f"Delete file error: {str(e)}")
            return False
    
    def delete_folder(self, path):
        """Delete a folder"""
        try:
            import shutil
            shutil.rmtree(path)
            logger.info(f"Folder deleted: {path}")
            return True
        except Exception as e:
            logger.error(f"Delete folder error: {str(e)}")
            return False
    
    # ========================
    # SCREENSHOT & OCR
    # ========================
    
    def take_screenshot(self, output_path=None):
        """Take a screenshot"""
        try:
            if output_path:
                screenshot = pyautogui.screenshot()
                screenshot.save(output_path)
                logger.info(f"Screenshot saved: {output_path}")
                return output_path
            else:
                return pyautogui.screenshot()
        except Exception as e:
            logger.error(f"Screenshot error: {str(e)}")
            return None
    
    # ========================
    # SYSTEM COMMANDS
    # ========================
    
    def run_command(self, command):
        """Execute a system command"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True
            )
            
            output = result.stdout if result.returncode == 0 else result.stderr
            logger.info(f"Command executed: {command}")
            return output
            
        except Exception as e:
            logger.error(f"Command execution error: {str(e)}")
            return f"Error: {str(e)}"
    
    def open_url(self, url):
        """Open URL in default browser"""
        try:
            if os.name == 'nt':
                os.startfile(url)
            else:
                subprocess.Popen(['open', url])
            
            logger.info(f"Opened URL: {url}")
            return True
        except Exception as e:
            logger.error(f"Open URL error: {str(e)}")
            return False
    
    # ========================
    # CLEANUP
    # ========================
    
    def cleanup(self):
        """Clean up resources"""
        logger.info("ComputerControl cleanup")
        return True


if __name__ == "__main__":
    print("Testing ComputerControl...")
    
    control = ComputerControl()
    
    # Test mouse position
    pos = control.get_mouse_position()
    print(f"✅ Mouse position: {pos}")
    
    # Test file operations
    control.create_folder("test_folder")
    print("✅ Folder created")
    
    control.create_file("test_folder/test.txt", "Hello World")
    print("✅ File created")
    
    content = control.read_file("test_folder/test.txt")
    print(f"✅ File content: {content}")
    
    # Cleanup
    control.delete_folder("test_folder")
    print("✅ Folder deleted")
    
    print("\n✅ ComputerControl tests complete")
