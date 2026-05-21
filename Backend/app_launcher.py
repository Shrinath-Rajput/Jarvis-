# app_launcher.py
"""
Application launcher and manager for JARVIS
PRODUCTION-GRADE with real verification and error handling
"""

import subprocess
import os
import time
import psutil
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)


class AppLauncher:
    """Handle application launching with REAL verification"""
    
    # Application paths mapping with actual Windows executables
    APP_PATHS = {
        # Microsoft Office
        "word": [
            "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
            "C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
            "C:\\Program Files\\Microsoft Office\\Office16\\WINWORD.EXE",
            "winword.exe"
        ],
        "excel": [
            "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE",
            "C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\EXCEL.EXE",
            "C:\\Program Files\\Microsoft Office\\Office16\\EXCEL.EXE",
            "excel.exe"
        ],
        "powerpoint": [
            "C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE",
            "C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\POWERPNT.EXE",
            "C:\\Program Files\\Microsoft Office\\Office16\\POWERPNT.EXE",
            "powerpnt.exe"
        ],
        "outlook": [
            "C:\\Program Files\\Microsoft Office\\root\\Office16\\OUTLOOK.EXE",
            "C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\OUTLOOK.EXE",
            "outlook.exe"
        ],
        
        # Development
        "vs code": ["code", "C:\\Program Files\\Microsoft VS Code\\Code.exe"],
        "vscode": ["code", "C:\\Program Files\\Microsoft VS Code\\Code.exe"],
        "notepad": ["notepad.exe"],
        "notepad++": ["C:\\Program Files\\Notepad++\\notepad++.exe", "C:\\Program Files (x86)\\Notepad++\\notepad++.exe", "notepad++.exe"],
        
        # Browsers
        "chrome": [
            "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
            "chrome.exe"
        ],
        "firefox": [
            "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
            "C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe",
            "firefox.exe"
        ],
        "edge": [
            "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
            "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
            "msedge.exe"
        ],
        
        # Productivity
        "calculator": ["calc.exe"],
        "calculator app": ["calc.exe"],
        "paint": ["mspaint.exe"],
        "task manager": ["taskmgr.exe"],
        
        # Media
        "spotify": [
            "C:\\Users\\%USERNAME%\\AppData\\Roaming\\Spotify\\Spotify.exe",
            "spotify.exe"
        ],
        "vlc": [
            "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe",
            "C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe",
            "vlc.exe"
        ],
        
        # Communication
        "zoom": ["zoom.exe", "C:\\Program Files\\Zoom\\Zoom.exe"],
        "teams": ["C:\\Program Files\\Microsoft\\Teams\\Teams.exe", "teams.exe"],
        "discord": ["discord.exe"],
        
        # Settings
        "settings": ["ms-settings:"],
        "control panel": ["control.exe"],
        
        # Other
        "file explorer": ["explorer.exe"],
        "terminal": ["cmd.exe"],
        "powershell": ["powershell.exe"],
    }
    
    # Process names for verification
    PROCESS_NAMES = {
        "chrome": "chrome.exe",
        "firefox": "firefox.exe",
        "edge": "msedge.exe",
        "word": "WINWORD.EXE",
        "excel": "EXCEL.EXE",
        "powerpoint": "POWERPNT.EXE",
        "outlook": "OUTLOOK.EXE",
        "vs code": "Code.exe",
        "vscode": "Code.exe",
        "spotify": "Spotify.exe",
        "notepad": "notepad.exe",
        "notepad++": "notepad++.exe",
        "calculator": "Calculator.exe",
        "paint": "mspaint.exe",
        "teams": "Teams.exe",
        "discord": "Discord.exe",
        "zoom": "Zoom.exe",
        "vlc": "vlc.exe",
        "terminal": "cmd.exe",
        "powershell": "powershell.exe",
    }
    
    @staticmethod
    def _is_process_running(process_name):
        """✅ Verify if a process is running"""
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'].lower() == process_name.lower():
                    return True
            return False
        except Exception as e:
            logger.error(f"Error checking process: {e}")
            return False
    
    @staticmethod
    def _find_executable(app_name):
        """🔍 Find actual executable path"""
        app_name_lower = app_name.lower().strip()
        
        # Get possible paths
        paths = AppLauncher.APP_PATHS.get(app_name_lower, [app_name_lower])
        
        if isinstance(paths, str):
            paths = [paths]
        
        # Try each path
        for path in paths:
            expanded_path = os.path.expandvars(path)
            
            # Check if it's a Windows settings URI
            if expanded_path.startswith("ms-"):
                return expanded_path, "uri"
            
            # Check if file exists
            if os.path.exists(expanded_path) and os.path.isfile(expanded_path):
                return expanded_path, "file"
            
            # For shell commands without extension
            if not expanded_path.endswith(".exe") and not expanded_path.endswith(".EXE"):
                # Try to find it in PATH
                try:
                    result = subprocess.run(
                        f"where {expanded_path}",
                        shell=True,
                        capture_output=True,
                        text=True,
                        timeout=2
                    )
                    if result.returncode == 0:
                        found_path = result.stdout.strip().split('\n')[0]
                        if found_path and os.path.exists(found_path):
                            return found_path, "file"
                except:
                    pass
        
        return None, None
    
    @staticmethod
    def open_app(app_name, wait_time=3):
        """✅ Open application with REAL verification"""
        try:
            logger.info(f"🚀 Attempting to open: {app_name}")
            app_name_lower = app_name.lower().strip()
            
            # Find the executable
            executable, exec_type = AppLauncher._find_executable(app_name)
            
            if not executable:
                error_msg = f"❌ Could not find executable for app: {app_name}"
                logger.error(error_msg)
                return {"success": False, "error": error_msg}
            
            logger.info(f"📍 Found executable: {executable}")
            
            # Get process name for verification
            process_name = AppLauncher.PROCESS_NAMES.get(app_name_lower)
            
            # Try to open the app
            try:
                if exec_type == "uri":
                    # Windows settings URI
                    logger.info(f"🔗 Opening URI: {executable}")
                    subprocess.Popen(f"start {executable}", shell=True)
                else:
                    # File executable
                    logger.info(f"▶️  Launching: {executable}")
                    proc = subprocess.Popen(executable, shell=False)
                    
                    # Verify process started with valid PID
                    if proc.pid is None:
                        error_msg = f"❌ Failed to get process ID for {app_name}"
                        logger.error(error_msg)
                        return {"success": False, "error": error_msg}
                    
                    logger.info(f"✅ Process started with PID: {proc.pid}")
                
                # Wait for app to start
                logger.info(f"⏳ Waiting {wait_time}s for {app_name} to load...")
                time.sleep(wait_time)
                
                # Verify process is running
                if process_name:
                    if AppLauncher._is_process_running(process_name):
                        logger.info(f"✅ Process verified: {process_name} is running")
                        return {
                            "success": True,
                            "message": f"✅ Successfully opened {app_name}",
                            "process": process_name,
                            "executable": executable
                        }
                    else:
                        # Give it more time
                        logger.warning(f"⚠️  Process not detected yet, waiting 2 more seconds...")
                        time.sleep(2)
                        
                        if AppLauncher._is_process_running(process_name):
                            logger.info(f"✅ Process verified: {process_name} is running")
                            return {
                                "success": True,
                                "message": f"✅ Successfully opened {app_name}",
                                "process": process_name,
                                "executable": executable
                            }
                        else:
                            error_msg = f"❌ Process {process_name} not found after {wait_time + 2}s"
                            logger.error(error_msg)
                            return {"success": False, "error": error_msg}
                
                # If no process name, assume success after wait
                logger.info(f"✅ App opened: {app_name}")
                return {
                    "success": True,
                    "message": f"✅ Successfully opened {app_name}",
                    "executable": executable
                }
                
            except Exception as e:
                error_msg = f"❌ Failed to execute {executable}: {str(e)}"
                logger.error(error_msg)
                return {"success": False, "error": error_msg}
        
        except Exception as e:
            error_msg = f"❌ Error opening app {app_name}: {str(e)}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    @staticmethod
    def close_app(app_name):
        """✅ Close an application with verification"""
        try:
            logger.info(f"🛑 Attempting to close: {app_name}")
            app_name_lower = app_name.lower().strip()
            
            # Get process name
            process_name = AppLauncher.PROCESS_NAMES.get(app_name_lower, f"{app_name}.exe")
            
            logger.info(f"🎯 Targeting process: {process_name}")
            
            # Try to terminate the process
            result = subprocess.run(
                f'taskkill /IM "{process_name}" /F',
                shell=True,
                capture_output=True,
                text=True
            )
            
            # Check if process was killed
            if result.returncode == 0:
                logger.info(f"✅ Successfully terminated: {process_name}")
                time.sleep(1)  # Wait for process to fully close
                
                # Verify process is closed
                if not AppLauncher._is_process_running(process_name):
                    logger.info(f"✅ Verified: {process_name} is closed")
                    return {"success": True, "message": f"✅ Closed {app_name}"}
                else:
                    logger.warning(f"⚠️  Process still running: {process_name}")
                    return {"success": False, "error": f"Process still running after termination"}
            else:
                error_msg = f"Process not found or already closed: {process_name}"
                logger.info(f"ℹ️  {error_msg}")
                return {"success": True, "message": error_msg}
        except Exception as e:
            error_msg = f"❌ Error closing {app_name}: {str(e)}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    @staticmethod
    def list_running_apps():
        """✅ List all running applications"""
        try:
            logger.info("📋 Listing running applications...")
            running_apps = []
            
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.info['name'].endswith('.exe'):
                        running_apps.append(proc.info['name'])
                except:
                    pass
            
            unique_apps = list(set(running_apps))
            logger.info(f"✅ Found {len(unique_apps)} running applications")
            
            return {"success": True, "apps": unique_apps, "count": len(unique_apps)}
        except Exception as e:
            error_msg = f"❌ Error listing apps: {str(e)}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    @staticmethod
    def focus_window(window_name):
        """✅ Focus a specific window"""
        try:
            import pygetwindow as gw
            
            logger.info(f"🎯 Focusing window: {window_name}")
            
            windows = gw.getWindowsWithTitle(window_name)
            
            if windows:
                windows[0].activate()
                time.sleep(0.5)
                logger.info(f"✅ Focused window: {window_name}")
                return {"success": True, "message": f"Focused window: {window_name}"}
            else:
                error_msg = f"❌ Window not found: {window_name}"
                logger.error(error_msg)
                return {"success": False, "error": error_msg}
        except ImportError:
            logger.warning("⚠️  pygetwindow not available, skipping window focus")
            return {"success": False, "error": "pygetwindow not installed"}
        except Exception as e:
            error_msg = f"❌ Error focusing window: {str(e)}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}


app_launcher = AppLauncher()


# Export
app_launcher = AppLauncher()
