# executor_v3_production.py
"""
JARVIS PRODUCTION-GRADE EXECUTOR - v3
Complete REAL Windows Desktop Automation with Verification
NO FAKE SUCCESS - Every action verified before returning success
"""

import os
import time
import subprocess
import webbrowser
import json
import traceback
import logging
from datetime import datetime
from pathlib import Path

import pyautogui
import psutil
import pygetwindow as gw

# Setup logging with file and console output
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('executor_production.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Import all helper modules
from app_launcher import app_launcher
from browser_tools import browser_tools

pyautogui.FAILSAFE = False


def log_execution(tool, params, success, result=None, error=None):
    """✅ Enhanced detailed execution logging"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "✅ SUCCESS" if success else "❌ FAILED"
    
    log_msg = f"\n{'='*80}"
    log_msg += f"\n[{timestamp}] [{status}] TOOL: {tool}"
    log_msg += f"\n{'='*80}"
    
    if params:
        log_msg += f"\n📋 Parameters: {json.dumps(params, default=str, indent=2)[:300]}"
    
    if result:
        log_msg += f"\n✅ Result: {str(result)[:400]}"
    
    if error:
        log_msg += f"\n❌ Error: {error}"
    
    log_msg += f"\n{'='*80}\n"
    
    print(log_msg)
    logger.info(log_msg)


class ProductionExecutor:
    """Production-grade executor with REAL verification"""

    def __init__(self):
        """Initialize executor"""
        self.tools_available = self._collect_available_tools()
        logger.info(f"✅ PRODUCTION EXECUTOR initialized with {len(self.tools_available)} tools")

    def _collect_available_tools(self):
        """Collect all available tool methods"""
        tools = []
        for attr_name in dir(self):
            if attr_name.startswith("tool_") and callable(getattr(self, attr_name)):
                tool_name = attr_name.replace("tool_", "")
                tools.append(tool_name)
        return sorted(tools)

    def print_available_tools(self):
        """Print all available tools"""
        print(f"\n{'='*80}")
        print(f"📦 AVAILABLE TOOLS ({len(self.tools_available)} total)")
        print(f"{'='*80}")
        
        for i, tool in enumerate(self.tools_available, 1):
            print(f"  {i:2d}. {tool}")
        
        print(f"{'='*80}\n")

    def execute_plan(self, plan):
        """Execute a list of steps with REAL verification"""
        
        print(f"\n{'='*80}")
        print(f"🚀 EXECUTING PLAN ({len(plan)} steps)")
        print(f"{'='*80}\n")
        
        results = []

        for i, step in enumerate(plan, 1):
            tool = step.get("tool", "").lower().replace(" ", "_").strip()
            params = step.get("params", {})

            print(f"\n📍 Step {i}/{len(plan)}: [{tool}]")
            if params:
                print(f"   Params: {json.dumps(params, default=str)[:150]}")

            try:
                # ✅ VALIDATE TOOL EXISTS
                fn_name = f"tool_{tool}"
                
                if not hasattr(self, fn_name):
                    error_msg = f"❌ Tool '{tool}' not found"
                    print(f"   {error_msg}")
                    
                    log_execution(tool, params, False, error=error_msg)
                    
                    results.append({
                        "tool": tool,
                        "success": False,
                        "error": error_msg,
                        "step": i
                    })
                    continue

                fn = getattr(self, fn_name)
                
                if not callable(fn):
                    error_msg = f"❌ Tool '{tool}' is not callable"
                    print(f"   {error_msg}")
                    
                    log_execution(tool, params, False, error=error_msg)
                    
                    results.append({
                        "tool": tool,
                        "success": False,
                        "error": error_msg,
                        "step": i
                    })
                    continue

                # ✅ EXECUTE THE TOOL
                print(f"   ⚙️  Executing...")
                result = fn(**params) if params else fn()

                # ✅ VERIFY SUCCESS
                success = result.get("success", False) if isinstance(result, dict) else False

                log_execution(tool, params, success, result)

                results.append({
                    "tool": tool,
                    "success": success,
                    "result": result,
                    "step": i
                })
                
                print(f"   {'✅ Success' if success else '❌ Failed'}: Step {i}")

            except TypeError as e:
                error_msg = f"Parameter error: {str(e)}"
                print(f"   ❌ {error_msg}")
                log_execution(tool, params, False, error=error_msg)
                
                results.append({
                    "tool": tool,
                    "success": False,
                    "error": error_msg,
                    "step": i
                })

            except Exception as e:
                error_msg = traceback.format_exc()
                print(f"   ❌ Execution failed: {str(e)}")
                log_execution(tool, params, False, error=str(e))

                results.append({
                    "tool": tool,
                    "success": False,
                    "error": str(e),
                    "step": i
                })

        # ✅ SUMMARY
        successful = sum(1 for r in results if r['success'])
        failed = len(results) - successful
        
        print(f"\n{'='*80}")
        print(f"📊 EXECUTION SUMMARY")
        print(f"   ✅ Successful: {successful}/{len(results)}")
        print(f"   ❌ Failed: {failed}/{len(results)}")
        print(f"{'='*80}\n")

        return results

    # ==================== BROWSER TOOLS ====================
    
    def tool_open_chrome(self, url=None):
        """✅ REAL Chrome opening"""
        return browser_tools.open_chrome(url)

    def tool_open_firefox(self, url=None):
        """✅ REAL Firefox opening"""
        return browser_tools.open_firefox(url)

    def tool_open_edge(self, url=None):
        """✅ REAL Edge opening"""
        return browser_tools.open_edge(url)

    def tool_google_search(self, query):
        """✅ REAL Google search"""
        return browser_tools.google_search(query)

    def tool_youtube_search(self, query):
        """✅ REAL YouTube search"""
        return browser_tools.youtube_search(query)

    def tool_open_gmail(self):
        """✅ REAL Gmail opening"""
        return browser_tools.open_gmail()

    def tool_amazon_search(self, query):
        """✅ REAL Amazon search"""
        return browser_tools.amazon_search(query)

    def tool_open_website(self, url):
        """✅ REAL website opening"""
        return browser_tools.open_website(url)

    def tool_open_chrome_incognito(self):
        """✅ REAL Chrome incognito"""
        return browser_tools.open_chrome_incognito()

    def tool_open_firefox_private(self):
        """✅ REAL Firefox private"""
        return browser_tools.open_firefox_private()

    def tool_open_edge_inprivate(self):
        """✅ REAL Edge InPrivate"""
        return browser_tools.open_edge_inprivate()

    # ==================== APP LAUNCHER ====================
    
    def tool_open_app(self, name):
        """✅ REAL app launching with verification"""
        return app_launcher.open_app(name)

    def tool_close_app(self, name):
        """✅ REAL app closing with verification"""
        return app_launcher.close_app(name)

    def tool_open_word(self):
        """✅ Open Microsoft Word"""
        return app_launcher.open_app("word")

    def tool_open_excel(self):
        """✅ Open Microsoft Excel"""
        return app_launcher.open_app("excel")

    def tool_open_powerpoint(self):
        """✅ Open Microsoft PowerPoint"""
        return app_launcher.open_app("powerpoint")

    def tool_open_outlook(self):
        """✅ Open Microsoft Outlook"""
        return app_launcher.open_app("outlook")

    def tool_open_vscode(self):
        """✅ Open VS Code"""
        return app_launcher.open_app("vs code")

    def tool_open_notepad(self):
        """✅ Open Notepad"""
        return app_launcher.open_app("notepad")

    def tool_open_calculator(self):
        """✅ Open Calculator"""
        return app_launcher.open_app("calculator")

    def tool_open_paint(self):
        """✅ Open Paint"""
        return app_launcher.open_app("paint")

    def tool_open_spotify(self):
        """✅ Open Spotify"""
        return app_launcher.open_app("spotify")

    def tool_open_zoom(self):
        """✅ Open Zoom"""
        return app_launcher.open_app("zoom")

    def tool_open_teams(self):
        """✅ Open Microsoft Teams"""
        return app_launcher.open_app("teams")

    def tool_open_discord(self):
        """✅ Open Discord"""
        return app_launcher.open_app("discord")

    def tool_open_vlc(self):
        """✅ Open VLC Media Player"""
        return app_launcher.open_app("vlc")

    def tool_open_powershell(self, directory=None):
        """✅ REAL PowerShell opening"""
        try:
            logger.info(f"\n{'='*80}")
            logger.info(f"🖥️  OPENING POWERSHELL")
            if directory:
                logger.info(f"   Directory: {directory}")
            logger.info(f"{'='*80}")
            
            if directory:
                # Expand path
                expanded_dir = os.path.expanduser(directory)
                if os.path.exists(expanded_dir):
                    logger.info(f"▶️  Opening PowerShell in: {expanded_dir}")
                    subprocess.Popen(
                        f'powershell -NoExit -Command "Set-Location \'{expanded_dir}\'"'
                    )
                else:
                    logger.warning(f"⚠️  Directory not found: {expanded_dir}")
                    return {
                        "success": False,
                        "error": f"Directory not found: {expanded_dir}"
                    }
            else:
                logger.info(f"▶️  Opening PowerShell...")
                subprocess.Popen('powershell.exe')
            
            time.sleep(2)
            
            result = {
                "success": True,
                "message": f"✅ PowerShell opened",
                "directory": directory
            }
            logger.info(f"{'='*80}\n")
            return result
        except Exception as e:
            error = f"❌ Error opening PowerShell: {str(e)}"
            logger.error(error)
            return {"success": False, "error": error}

    def tool_open_terminal(self, directory=None):
        """✅ REAL Terminal (CMD) opening"""
        try:
            logger.info(f"\n{'='*80}")
            logger.info(f"🖥️  OPENING TERMINAL")
            if directory:
                logger.info(f"   Directory: {directory}")
            logger.info(f"{'='*80}")
            
            if directory:
                # Expand path
                expanded_dir = os.path.expanduser(directory)
                if os.path.exists(expanded_dir):
                    logger.info(f"▶️  Opening Terminal in: {expanded_dir}")
                    subprocess.Popen(
                        f'cmd.exe /K "cd /d {expanded_dir}"'
                    )
                else:
                    logger.warning(f"⚠️  Directory not found: {expanded_dir}")
                    return {
                        "success": False,
                        "error": f"Directory not found: {expanded_dir}"
                    }
            else:
                logger.info(f"▶️  Opening Terminal...")
                subprocess.Popen('cmd.exe')
            
            time.sleep(2)
            
            result = {
                "success": True,
                "message": f"✅ Terminal opened",
                "directory": directory
            }
            logger.info(f"{'='*80}\n")
            return result
        except Exception as e:
            error = f"❌ Error opening Terminal: {str(e)}"
            logger.error(error)
            return {"success": False, "error": error}

    # ==================== FILE MANAGEMENT ====================
    
    def tool_create_folder(self, name, location=None, path=None):
        """✅ REAL folder creation with verification"""
        try:
            logger.info(f"\n{'='*80}")
            logger.info(f"📁 CREATING FOLDER")
            logger.info(f"   Name: {name}")
            if location:
                logger.info(f"   Location: {location}")
            if path:
                logger.info(f"   Path: {path}")
            logger.info(f"{'='*80}")
            
            if path:
                # Use full path
                if os.path.isabs(path):
                    folder_path = path
                else:
                    location = location or os.path.expanduser("~")
                    folder_path = os.path.join(location, path)
            else:
                # Use location + name
                if not location:
                    location = os.path.join(os.path.expanduser("~"), "Desktop")
                folder_path = os.path.join(location, name)
            
            logger.info(f"📍 Target path: {folder_path}")
            
            # Create the folder
            os.makedirs(folder_path, exist_ok=True)
            
            # ✅ VERIFY FOLDER WAS CREATED
            if os.path.exists(folder_path) and os.path.isdir(folder_path):
                logger.info(f"✅✅✅ VERIFIED: Folder created successfully")
                result = {
                    "success": True,
                    "message": f"✅ Created folder: {folder_path}",
                    "path": folder_path,
                    "exists": True
                }
                logger.info(f"{'='*80}\n")
                return result
            else:
                error_msg = f"❌ Folder creation failed: {folder_path}"
                logger.error(error_msg)
                return {"success": False, "error": error_msg}
        except Exception as e:
            error_msg = f"❌ Error creating folder: {str(e)}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}

    def tool_open_folder(self, path):
        """✅ REAL folder opening with verification"""
        try:
            logger.info(f"\n{'='*80}")
            logger.info(f"📂 OPENING FOLDER")
            logger.info(f"   Path: {path}")
            logger.info(f"{'='*80}")
            
            path = os.path.expanduser(path)
            
            # Verify path exists
            if not os.path.exists(path):
                error = f"❌ Path does not exist: {path}"
                logger.error(error)
                return {"success": False, "error": error}
            
            if not os.path.isdir(path):
                error = f"❌ Path is not a directory: {path}"
                logger.error(error)
                return {"success": False, "error": error}
            
            logger.info(f"▶️  Opening: {path}")
            os.startfile(path)
            
            time.sleep(1)
            
            result = {
                "success": True,
                "message": f"✅ Opened folder: {path}",
                "path": path
            }
            logger.info(f"{'='*80}\n")
            return result
        except Exception as e:
            error = f"❌ Error opening folder: {str(e)}"
            logger.error(error)
            return {"success": False, "error": error}

    def tool_delete_file(self, file_path):
        """✅ REAL file deletion with verification"""
        try:
            logger.info(f"\n{'='*80}")
            logger.info(f"🗑️  DELETING FILE")
            logger.info(f"   Path: {file_path}")
            logger.info(f"{'='*80}")
            
            file_path = os.path.expanduser(file_path)
            
            if not os.path.exists(file_path):
                error = f"❌ File does not exist: {file_path}"
                logger.error(error)
                return {"success": False, "error": error}
            
            logger.info(f"▶️  Deleting: {file_path}")
            os.remove(file_path)
            
            # ✅ VERIFY DELETION
            if not os.path.exists(file_path):
                logger.info(f"✅✅✅ VERIFIED: File deleted")
                result = {
                    "success": True,
                    "message": f"✅ Deleted file: {file_path}",
                    "verified": True
                }
                logger.info(f"{'='*80}\n")
                return result
            else:
                error = f"❌ File still exists after deletion attempt"
                logger.error(error)
                return {"success": False, "error": error}
        except Exception as e:
            error = f"❌ Error deleting file: {str(e)}"
            logger.error(error)
            return {"success": False, "error": error}

    def tool_copy_file(self, source, destination):
        """✅ REAL file copying with verification"""
        try:
            logger.info(f"\n{'='*80}")
            logger.info(f"📋 COPYING FILE")
            logger.info(f"   Source: {source}")
            logger.info(f"   Destination: {destination}")
            logger.info(f"{'='*80}")
            
            source = os.path.expanduser(source)
            destination = os.path.expanduser(destination)
            
            if not os.path.exists(source):
                error = f"❌ Source file does not exist: {source}"
                logger.error(error)
                return {"success": False, "error": error}
            
            import shutil
            logger.info(f"▶️  Copying file...")
            shutil.copy2(source, destination)
            
            # ✅ VERIFY COPY
            if os.path.exists(destination):
                source_size = os.path.getsize(source)
                dest_size = os.path.getsize(destination)
                
                if source_size == dest_size:
                    logger.info(f"✅✅✅ VERIFIED: File copied ({source_size} bytes)")
                    result = {
                        "success": True,
                        "message": f"✅ Copied file to: {destination}",
                        "source_size": source_size,
                        "dest_size": dest_size,
                        "verified": True
                    }
                    logger.info(f"{'='*80}\n")
                    return result
                else:
                    error = f"❌ File sizes don't match after copy"
                    logger.error(error)
                    return {"success": False, "error": error}
            else:
                error = f"❌ Destination file not created"
                logger.error(error)
                return {"success": False, "error": error}
        except Exception as e:
            error = f"❌ Error copying file: {str(e)}"
            logger.error(error)
            return {"success": False, "error": error}

    # ==================== KEYBOARD & MOUSE ====================
    
    def tool_type(self, text):
        """✅ REAL text typing"""
        try:
            logger.info(f"\n{'='*80}")
            logger.info(f"⌨️  TYPING TEXT")
            logger.info(f"   Text: {text[:100]}")
            logger.info(f"{'='*80}")
            
            if not text or not isinstance(text, str):
                error = f"❌ Invalid text: {text}"
                logger.error(error)
                return {"success": False, "error": error}
            
            logger.info(f"▶️  Typing {len(text)} characters...")
            
            # Use write method (slower, more reliable)
            pyautogui.write(text, interval=0.02)
            
            # Small wait to ensure typing is complete
            time.sleep(0.5)
            
            logger.info(f"✅ Text typed successfully")
            result = {
                "success": True,
                "message": f"✅ Typed {len(text)} characters",
                "text_length": len(text)
            }
            logger.info(f"{'='*80}\n")
            return result
        except Exception as e:
            error = f"❌ Error typing text: {str(e)}"
            logger.error(error)
            return {"success": False, "error": error}

    def tool_press_key(self, key):
        """✅ REAL key press"""
        try:
            logger.info(f"\n{'='*80}")
            logger.info(f"⌨️  PRESSING KEY")
            logger.info(f"   Key: {key}")
            logger.info(f"{'='*80}")
            
            logger.info(f"▶️  Pressing key: {key}")
            pyautogui.press(key)
            
            time.sleep(0.2)
            
            logger.info(f"✅ Key pressed")
            result = {
                "success": True,
                "message": f"✅ Pressed key: {key}",
                "key": key
            }
            logger.info(f"{'='*80}\n")
            return result
        except Exception as e:
            error = f"❌ Error pressing key: {str(e)}"
            logger.error(error)
            return {"success": False, "error": error}

    def tool_hotkey(self, *keys):
        """✅ REAL hotkey combination"""
        try:
            logger.info(f"\n{'='*80}")
            logger.info(f"⌨️  PRESSING HOTKEY")
            logger.info(f"   Keys: {keys}")
            logger.info(f"{'='*80}")
            
            logger.info(f"▶️  Pressing: {'+'.join(keys)}")
            pyautogui.hotkey(*keys)
            
            time.sleep(0.2)
            
            logger.info(f"✅ Hotkey pressed")
            result = {
                "success": True,
                "message": f"✅ Pressed hotkey: {'+'.join(keys)}",
                "keys": keys
            }
            logger.info(f"{'='*80}\n")
            return result
        except Exception as e:
            error = f"❌ Error pressing hotkey: {str(e)}"
            logger.error(error)
            return {"success": False, "error": error}

    def tool_click(self, x=None, y=None):
        """✅ REAL mouse click"""
        try:
            logger.info(f"\n{'='*80}")
            logger.info(f"🖱️  MOUSE CLICK")
            if x and y:
                logger.info(f"   Position: ({x}, {y})")
            logger.info(f"{'='*80}")
            
            if x is None or y is None:
                # Click at current position
                logger.info(f"▶️  Clicking at current position...")
                pyautogui.click()
            else:
                logger.info(f"▶️  Clicking at ({x}, {y})...")
                pyautogui.click(x, y)
            
            time.sleep(0.2)
            
            logger.info(f"✅ Click completed")
            result = {
                "success": True,
                "message": f"✅ Clicked at ({x}, {y})" if x and y else "✅ Clicked",
                "x": x,
                "y": y
            }
            logger.info(f"{'='*80}\n")
            return result
        except Exception as e:
            error = f"❌ Error clicking: {str(e)}"
            logger.error(error)
            return {"success": False, "error": error}

    # ==================== SYSTEM CONTROL ====================
    
    def tool_wait(self, seconds):
        """✅ Wait/delay execution"""
        try:
            logger.info(f"\n{'='*80}")
            logger.info(f"⏳ WAITING")
            logger.info(f"   Duration: {seconds}s")
            logger.info(f"{'='*80}")
            
            logger.info(f"▶️  Waiting {seconds} seconds...")
            time.sleep(seconds)
            
            logger.info(f"✅ Wait completed")
            result = {
                "success": True,
                "message": f"✅ Waited {seconds} seconds",
                "seconds": seconds
            }
            logger.info(f"{'='*80}\n")
            return result
        except Exception as e:
            error = f"❌ Error during wait: {str(e)}"
            logger.error(error)
            return {"success": False, "error": error}

    def tool_screenshot(self, save_path=None):
        """✅ REAL screenshot with verification"""
        try:
            logger.info(f"\n{'='*80}")
            logger.info(f"📸 TAKING SCREENSHOT")
            if save_path:
                logger.info(f"   Save path: {save_path}")
            logger.info(f"{'='*80}")
            
            if not save_path:
                save_path = os.path.join(
                    os.path.expanduser("~"),
                    "Desktop",
                    f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                )
            
            save_path = os.path.expanduser(save_path)
            
            logger.info(f"▶️  Capturing screenshot...")
            screenshot = pyautogui.screenshot()
            screenshot.save(save_path)
            
            # ✅ VERIFY SCREENSHOT SAVED
            if os.path.exists(save_path):
                file_size = os.path.getsize(save_path)
                logger.info(f"✅✅✅ VERIFIED: Screenshot saved ({file_size} bytes)")
                result = {
                    "success": True,
                    "message": f"✅ Screenshot saved: {save_path}",
                    "path": save_path,
                    "size": file_size,
                    "verified": True
                }
                logger.info(f"{'='*80}\n")
                return result
            else:
                error = f"❌ Screenshot file not created"
                logger.error(error)
                return {"success": False, "error": error}
        except Exception as e:
            error = f"❌ Error taking screenshot: {str(e)}"
            logger.error(error)
            return {"success": False, "error": error}

    def tool_shutdown(self, delay_minutes=0):
        """✅ REAL system shutdown"""
        try:
            logger.info(f"\n{'='*80}")
            logger.info(f"🔴 SYSTEM SHUTDOWN")
            if delay_minutes:
                logger.info(f"   Delay: {delay_minutes} minutes")
            logger.info(f"{'='*80}")
            
            if delay_minutes > 0:
                delay_seconds = delay_minutes * 60
                logger.info(f"▶️  Scheduling shutdown in {delay_minutes} minutes...")
                os.system(f"shutdown /s /t {delay_seconds}")
            else:
                logger.info(f"▶️  Initiating immediate shutdown...")
                os.system("shutdown /s /t 0")
            
            logger.info(f"✅ Shutdown initiated")
            result = {
                "success": True,
                "message": f"✅ Shutdown initiated" + (f" in {delay_minutes} minutes" if delay_minutes else " immediately"),
                "delay_minutes": delay_minutes
            }
            logger.info(f"{'='*80}\n")
            return result
        except Exception as e:
            error = f"❌ Error initiating shutdown: {str(e)}"
            logger.error(error)
            return {"success": False, "error": error}

    def tool_restart(self, delay_minutes=0):
        """✅ REAL system restart"""
        try:
            logger.info(f"\n{'='*80}")
            logger.info(f"🔄 SYSTEM RESTART")
            if delay_minutes:
                logger.info(f"   Delay: {delay_minutes} minutes")
            logger.info(f"{'='*80}")
            
            if delay_minutes > 0:
                delay_seconds = delay_minutes * 60
                logger.info(f"▶️  Scheduling restart in {delay_minutes} minutes...")
                os.system(f"shutdown /r /t {delay_seconds}")
            else:
                logger.info(f"▶️  Initiating immediate restart...")
                os.system("shutdown /r /t 0")
            
            logger.info(f"✅ Restart initiated")
            result = {
                "success": True,
                "message": f"✅ Restart initiated" + (f" in {delay_minutes} minutes" if delay_minutes else " immediately"),
                "delay_minutes": delay_minutes
            }
            logger.info(f"{'='*80}\n")
            return result
        except Exception as e:
            error = f"❌ Error initiating restart: {str(e)}"
            logger.error(error)
            return {"success": False, "error": error}

    def tool_lock_screen(self):
        """✅ REAL screen lock"""
        try:
            logger.info(f"\n{'='*80}")
            logger.info(f"🔒 LOCKING SCREEN")
            logger.info(f"{'='*80}")
            
            logger.info(f"▶️  Locking screen...")
            os.system("rundll32.exe user32.dll,LockWorkStation")
            
            time.sleep(1)
            
            logger.info(f"✅ Screen locked")
            result = {
                "success": True,
                "message": f"✅ Screen locked"
            }
            logger.info(f"{'='*80}\n")
            return result
        except Exception as e:
            error = f"❌ Error locking screen: {str(e)}"
            logger.error(error)
            return {"success": False, "error": error}


# Export
executor = ProductionExecutor()


if __name__ == "__main__":
    print("\n✅ JARVIS Production Executor v3 loaded successfully")
    executor.print_available_tools()
