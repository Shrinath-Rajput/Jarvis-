# -*- coding: utf-8 -*-
"""
UNIVERSAL EXECUTOR - TRULY AUTONOMOUS
Generic actions only. NO hardcoding.

Implements: OBSERVE → THINK → ACT → VERIFY

Actions:
- open_website: Open any URL
- open_app: Open any application
- open_folder: Open any folder
- screenshot: Capture screen
- click_text: Click visible text (OCR)
- click: Click coordinates
- type: Type text
- press_key: Press single key
- hotkey: Key combinations
- scroll: Scroll screen
- wait: Wait time
- create_folder: Create folder
- verify_text: Verify text appeared
- search: Search on current site
"""

import logging
import pyautogui
import webbrowser
import subprocess
import os
import time
import json
import shutil
import platform
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from pathlib import Path

try:
    from screen_understanding import ScreenUnderstanding
    SCREEN_UNDERSTANDING_AVAILABLE = True
except:
    SCREEN_UNDERSTANDING_AVAILABLE = False

try:
    from PIL import Image
    import pytesseract
    PIL_AVAILABLE = True
except:
    PIL_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.3


# ======================================
# EXECUTION RESULT
# ======================================

class ExecutionResult:
    """Result of a single action execution"""
    
    def __init__(self, tool: str, params: Dict, success: bool, 
                 output: Optional[str] = None, error: Optional[str] = None,
                 retry_count: int = 0):
        self.tool = tool
        self.params = params
        self.success = success
        self.output = output
        self.error = error
        self.retry_count = retry_count
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        return {
            "tool": self.tool,
            "params": self.params,
            "success": self.success,
            "output": self.output,
            "error": self.error,
            "retry_count": self.retry_count,
            "timestamp": self.timestamp
        }


# ======================================
# UNIVERSAL EXECUTOR
# ======================================

class UniversalExecutor:
    """
    Generic executor with NO hardcoding.
    Only universal actions.
    Automatic retry with verification.
    """
    
    def __init__(self):
        self.results = []
        self.screen_reader = None
        self.max_retries = 3
        self.last_screenshot = None
        
        # Initialize screen reader if available
        if SCREEN_UNDERSTANDING_AVAILABLE:
            try:
                self.screen_reader = ScreenUnderstanding()
                logger.info("✅ Screen reader initialized")
            except Exception as e:
                logger.warning(f"⚠️ Screen reader unavailable: {e}")
        
        logger.info("✅ UniversalExecutor initialized")
    
    def execute_plan(self, plan: List[Dict], max_retries: int = 3) -> Dict:
        """Execute complete action plan with retry logic"""
        
        self.results = []
        self.max_retries = max_retries
        total_actions = len(plan)
        successful_count = 0
        failed_count = 0
        
        logger.info(f"🚀 Executing plan: {total_actions} actions")
        
        for i, action in enumerate(plan, 1):
            logger.info(f"📍 Action {i}/{total_actions}")
            
            result = self._execute_with_retry(action)
            self.results.append(result.to_dict())
            
            if result.success:
                successful_count += 1
            else:
                failed_count += 1
                if action.get("critical", True):
                    logger.error(f"❌ Critical action failed: {action.get('tool')}")
                    # Don't break - continue to gather all results
        
        logger.info(f"✅ Plan completed: {successful_count}/{total_actions} actions succeeded")
        
        return {
            "status": "completed",
            "total_actions": total_actions,
            "successful": successful_count,
            "failed": failed_count,
            "results": self.results
        }
    
    def _execute_with_retry(self, action: Dict, retry: int = 0) -> ExecutionResult:
        """Execute single action with automatic retry"""
        
        try:
            result = self.execute_action(action)
            
            # Retry if failed and not at max retries
            if not result.success and retry < self.max_retries:
                tool = action.get("tool", "unknown")
                logger.warning(f"⚠️ Retry {retry+1}/{self.max_retries}: {tool}")
                
                time.sleep(1)  # Wait before retry
                result = self._execute_with_retry(action, retry + 1)
                result.retry_count = retry + 1
            
            return result
        
        except Exception as e:
            logger.error(f"Execution error: {e}")
            return ExecutionResult(
                action.get("tool", "unknown"),
                action.get("params", {}),
                False,
                error=str(e)
            )
    
    def execute_action(self, action: Dict) -> ExecutionResult:
        """Execute single generic action"""
        
        tool = action.get("tool", "").lower().strip()
        params = action.get("params", {})
        
        logger.info(f"🔧 Tool: {tool}")
        
        try:
            # Route to appropriate handler
            if tool == "open_website":
                return self._open_website(params)
            elif tool == "open_app":
                return self._open_app(params)
            elif tool == "open_folder":
                return self._open_folder(params)
            elif tool == "screenshot":
                return self._screenshot(params)
            elif tool == "click_text":
                return self._click_text(params)
            elif tool == "click":
                return self._click(params)
            elif tool == "type":
                return self._type(params)
            elif tool == "press_key":
                return self._press_key(params)
            elif tool == "hotkey":
                return self._hotkey(params)
            elif tool == "scroll":
                return self._scroll(params)
            elif tool == "wait":
                return self._wait(params)
            elif tool == "create_folder":
                return self._create_folder(params)
            elif tool == "verify_text":
                return self._verify_text(params)
            elif tool == "search":
                return self._search(params)
            elif tool == "select_all":
                return self._select_all(params)
            elif tool == "copy":
                return self._copy(params)
            elif tool == "paste":
                return self._paste(params)
            elif tool == "clear_field":
                return self._clear_field(params)
            else:
                return ExecutionResult(tool, params, False, error=f"Unknown tool: {tool}")
        
        except Exception as e:
            logger.error(f"Execution exception: {e}")
            return ExecutionResult(tool, params, False, error=str(e))
    
    # ======================================
    # GENERIC ACTIONS (NO HARDCODING)
    # ======================================
    
    def _open_website(self, params: Dict) -> ExecutionResult:
        """Open any website - NO hardcoded mappings"""
        
        try:
            url = params.get("url", "").strip()
            
            if not url:
                return ExecutionResult("open_website", params, False, 
                                      error="No URL provided")
            
            # Add protocol if missing
            if not url.startswith(("http://", "https://", "ftp://")):
                # Smart protocol detection
                if "." not in url or url.count(".") == 0:
                    url = f"https://www.{url}.com"
                elif not "." in url.split("/")[0]:  # No dot in domain
                    url = f"https://{url}"
                else:
                    url = f"https://{url}" if not url.startswith("www.") else f"https://{url}"
            
            logger.info(f"🌐 Opening: {url}")
            webbrowser.open(url)
            time.sleep(3)
            
            return ExecutionResult("open_website", params, True, 
                                  output=f"Opened: {url}")
        
        except Exception as e:
            logger.error(f"Open website error: {e}")
            return ExecutionResult("open_website", params, False, error=str(e))
    
    def _open_app(self, params: Dict) -> ExecutionResult:
        """Open any application - NO hardcoded app mappings"""
        
        try:
            app_name = params.get("name", "").strip()
            
            if not app_name:
                return ExecutionResult("open_app", params, False, 
                                      error="No app name provided")
            
            logger.info(f"🚀 Opening app: {app_name}")
            
            # Try multiple methods to find and open app
            # 1. Try direct execution
            try:
                subprocess.Popen(app_name)
                time.sleep(2)
                return ExecutionResult("open_app", params, True, 
                                      output=f"Opened: {app_name}")
            except:
                pass
            
            # 2. Try with .exe extension on Windows
            if platform.system() == "Windows":
                try:
                    subprocess.Popen(f"{app_name}.exe")
                    time.sleep(2)
                    return ExecutionResult("open_app", params, True, 
                                          output=f"Opened: {app_name}")
                except:
                    pass
            
            # 3. Try in PATH using shutil
            exe_path = shutil.which(app_name)
            if exe_path:
                subprocess.Popen(exe_path)
                time.sleep(2)
                return ExecutionResult("open_app", params, True, 
                                      output=f"Opened: {app_name}")
            
            # 4. Try with .exe if not found
            exe_path = shutil.which(f"{app_name}.exe")
            if exe_path:
                subprocess.Popen(exe_path)
                time.sleep(2)
                return ExecutionResult("open_app", params, True, 
                                      output=f"Opened: {app_name}")
            
            return ExecutionResult("open_app", params, False, 
                                  error=f"App not found: {app_name}")
        
        except Exception as e:
            logger.error(f"Open app error: {e}")
            return ExecutionResult("open_app", params, False, error=str(e))
    
    def _open_folder(self, params: Dict) -> ExecutionResult:
        """Open any folder - dynamic path handling"""
        
        try:
            path = params.get("path", "").strip()
            
            if not path:
                path = os.path.expanduser("~")
            
            # Expand home directory
            if path.startswith("~"):
                path = os.path.expanduser(path)
            
            # Convert relative to absolute
            if not os.path.isabs(path):
                path = os.path.abspath(path)
            
            logger.info(f"📁 Opening folder: {path}")
            
            # Create folder if it doesn't exist
            if not os.path.exists(path):
                logger.info(f"📝 Creating folder: {path}")
                os.makedirs(path, exist_ok=True)
            
            # Open folder
            if platform.system() == "Windows":
                subprocess.Popen(f'explorer "{path}"')
            elif platform.system() == "Darwin":  # macOS
                subprocess.Popen(["open", path])
            else:  # Linux
                subprocess.Popen(["xdg-open", path])
            
            time.sleep(1)
            
            return ExecutionResult("open_folder", params, True, 
                                  output=f"Opened: {path}")
        
        except Exception as e:
            logger.error(f"Open folder error: {e}")
            return ExecutionResult("open_folder", params, False, error=str(e))
    
    def _screenshot(self, params: Dict) -> ExecutionResult:
        """Take screenshot"""
        
        try:
            logger.info("📸 Taking screenshot")
            
            if self.screen_reader:
                screenshot_path = self.screen_reader.take_screenshot()
                self.last_screenshot = screenshot_path
                
                return ExecutionResult("screenshot", params, True, 
                                      output=f"Screenshot saved: {screenshot_path}")
            else:
                # Fallback: use pyautogui
                import mss
                monitor = mss.mss().monitors[1]
                screenshot = pyautogui.screenshot()
                screenshot_path = f"screenshots/screenshot_{int(time.time())}.png"
                screenshot.save(screenshot_path)
                self.last_screenshot = screenshot_path
                
                return ExecutionResult("screenshot", params, True, 
                                      output=f"Screenshot: {screenshot_path}")
        
        except Exception as e:
            logger.error(f"Screenshot error: {e}")
            return ExecutionResult("screenshot", params, False, error=str(e))
    
    def _click_text(self, params: Dict) -> ExecutionResult:
        """Click visible text using OCR - NO hardcoding"""
        
        try:
            text = params.get("text", "").strip()
            
            if not text:
                return ExecutionResult("click_text", params, False, 
                                      error="No text specified")
            
            logger.info(f"🔍 Finding text: '{text}'")
            
            if not self.screen_reader:
                return ExecutionResult("click_text", params, False, 
                                      error="Screen reader not available")
            
            # Take screenshot and analyze
            elements = self.screen_reader.find_text_on_screen(text)
            
            if not elements:
                logger.warning(f"⚠️ Text not found: '{text}'")
                return ExecutionResult("click_text", params, False, 
                                      error=f"Text not found: '{text}'")
            
            # Click center of first element
            element = elements[0] if isinstance(elements, list) else elements
            x, y = element.center()
            
            logger.info(f"✅ Clicking at ({x}, {y})")
            pyautogui.click(x, y)
            time.sleep(0.5)
            
            return ExecutionResult("click_text", params, True, 
                                  output=f"Clicked: '{text}' at ({x}, {y})")
        
        except Exception as e:
            logger.error(f"Click text error: {e}")
            return ExecutionResult("click_text", params, False, error=str(e))
    
    def _click(self, params: Dict) -> ExecutionResult:
        """Click at coordinates"""
        
        try:
            x = params.get("x")
            y = params.get("y")
            button = params.get("button", "left")
            
            if x is None or y is None:
                return ExecutionResult("click", params, False, 
                                      error="No coordinates provided")
            
            x = int(x)
            y = int(y)
            
            logger.info(f"🖱️ Clicking at ({x}, {y}) - {button}")
            pyautogui.click(x, y, button=button)
            time.sleep(0.5)
            
            return ExecutionResult("click", params, True, 
                                  output=f"Clicked at ({x}, {y})")
        
        except Exception as e:
            logger.error(f"Click error: {e}")
            return ExecutionResult("click", params, False, error=str(e))
    
    def _type(self, params: Dict) -> ExecutionResult:
        """Type text - handles special characters"""
        
        try:
            text = params.get("text", "")
            interval = params.get("interval", 0.05)
            
            if not text:
                return ExecutionResult("type", params, False, 
                                      error="No text to type")
            
            logger.info(f"⌨️ Typing: {text[:50]}...")
            
            # Use pyautogui's typewrite with support for special chars
            for char in text:
                if char == ' ':
                    pyautogui.press('space')
                elif char == '\n':
                    pyautogui.press('enter')
                elif char == '\t':
                    pyautogui.press('tab')
                elif char in '!@#$%^&*()_+-=[]{}|;:"\',.<>?/':
                    # Special characters - use write instead
                    pyautogui.write(char, interval=interval)
                else:
                    pyautogui.write(char, interval=interval)
                time.sleep(interval)
            
            time.sleep(0.3)
            
            return ExecutionResult("type", params, True, 
                                  output=f"Typed: {text}")
        
        except Exception as e:
            logger.error(f"Type error: {e}")
            return ExecutionResult("type", params, False, error=str(e))
    
    def _press_key(self, params: Dict) -> ExecutionResult:
        """Press single key"""
        
        try:
            key = params.get("key", "").lower().strip()
            
            if not key:
                return ExecutionResult("press_key", params, False, 
                                      error="No key specified")
            
            logger.info(f"🔑 Pressing: {key}")
            
            # Map common key names
            key_map = {
                "enter": "return",
                "return": "return",
                "tab": "tab",
                "space": "space",
                "backspace": "backspace",
                "delete": "delete",
                "escape": "escape",
                "esc": "escape",
                "up": "up",
                "down": "down",
                "left": "left",
                "right": "right",
                "home": "home",
                "end": "end",
                "pageup": "pageup",
                "pagedown": "pagedown",
                "f1": "f1", "f2": "f2", "f3": "f3", "f4": "f4",
                "f5": "f5", "f6": "f6", "f7": "f7", "f8": "f8",
                "f9": "f9", "f10": "f10", "f11": "f11", "f12": "f12",
            }
            
            key_to_press = key_map.get(key, key)
            pyautogui.press(key_to_press)
            time.sleep(0.3)
            
            return ExecutionResult("press_key", params, True, 
                                  output=f"Pressed: {key}")
        
        except Exception as e:
            logger.error(f"Press key error: {e}")
            return ExecutionResult("press_key", params, False, error=str(e))
    
    def _hotkey(self, params: Dict) -> ExecutionResult:
        """Press key combination (Ctrl+C, Alt+Tab, etc)"""
        
        try:
            keys = params.get("keys", [])
            
            if not keys:
                # Try single key param for backward compatibility
                key = params.get("key", "")
                if not key:
                    return ExecutionResult("hotkey", params, False, 
                                          error="No keys specified")
                keys = [key]
            
            logger.info(f"⌨️ Hotkey: {'+'.join(keys)}")
            
            # Convert to pyautogui compatible format
            converted_keys = []
            for key in keys:
                key_lower = key.lower().strip()
                if key_lower in ["ctrl", "control"]:
                    converted_keys.append("ctrl")
                elif key_lower in ["shift"]:
                    converted_keys.append("shift")
                elif key_lower in ["alt"]:
                    converted_keys.append("alt")
                elif key_lower in ["cmd", "command"]:
                    converted_keys.append("cmd")
                else:
                    converted_keys.append(key_lower)
            
            pyautogui.hotkey(*converted_keys)
            time.sleep(0.3)
            
            return ExecutionResult("hotkey", params, True, 
                                  output=f"Hotkey: {'+'.join(keys)}")
        
        except Exception as e:
            logger.error(f"Hotkey error: {e}")
            return ExecutionResult("hotkey", params, False, error=str(e))
    
    def _scroll(self, params: Dict) -> ExecutionResult:
        """Scroll mouse wheel"""
        
        try:
            pixels = params.get("pixels", 5)
            x = params.get("x")
            y = params.get("y")
            
            # Default to center if not specified
            if x is None or y is None:
                x, y = pyautogui.position()
            
            logger.info(f"📜 Scrolling: {pixels} pixels at ({x}, {y})")
            
            pyautogui.moveTo(x, y)
            pyautogui.scroll(pixels)
            time.sleep(0.5)
            
            return ExecutionResult("scroll", params, True, 
                                  output=f"Scrolled: {pixels} pixels")
        
        except Exception as e:
            logger.error(f"Scroll error: {e}")
            return ExecutionResult("scroll", params, False, error=str(e))
    
    def _wait(self, params: Dict) -> ExecutionResult:
        """Wait for specified seconds"""
        
        try:
            seconds = params.get("seconds", 1)
            seconds = float(seconds)
            
            logger.info(f"⏳ Waiting: {seconds} seconds")
            time.sleep(seconds)
            
            return ExecutionResult("wait", params, True, 
                                  output=f"Waited: {seconds} seconds")
        
        except Exception as e:
            logger.error(f"Wait error: {e}")
            return ExecutionResult("wait", params, False, error=str(e))
    
    def _create_folder(self, params: Dict) -> ExecutionResult:
        """Create folder with exact name - NO hardcoding"""
        
        try:
            path = params.get("path", "").strip()
            
            if not path:
                return ExecutionResult("create_folder", params, False, 
                                      error="No path specified")
            
            # Expand home
            if path.startswith("~"):
                path = os.path.expanduser(path)
            
            # Convert to absolute
            if not os.path.isabs(path):
                path = os.path.abspath(path)
            
            logger.info(f"📁 Creating folder: {path}")
            
            os.makedirs(path, exist_ok=True)
            
            if os.path.exists(path):
                return ExecutionResult("create_folder", params, True, 
                                      output=f"Created: {path}")
            else:
                return ExecutionResult("create_folder", params, False, 
                                      error=f"Failed to create: {path}")
        
        except Exception as e:
            logger.error(f"Create folder error: {e}")
            return ExecutionResult("create_folder", params, False, error=str(e))
    
    def _verify_text(self, params: Dict) -> ExecutionResult:
        """Verify text appeared on screen"""
        
        try:
            text = params.get("text", "").strip()
            timeout = params.get("timeout", 5)
            
            if not text:
                return ExecutionResult("verify_text", params, False, 
                                      error="No text to verify")
            
            logger.info(f"✔️ Verifying text: '{text}'")
            
            if not self.screen_reader:
                return ExecutionResult("verify_text", params, False, 
                                      error="Screen reader not available")
            
            # Take screenshot and check
            elements = self.screen_reader.find_text_on_screen(text)
            
            if elements:
                return ExecutionResult("verify_text", params, True, 
                                      output=f"Text found: '{text}'")
            else:
                return ExecutionResult("verify_text", params, False, 
                                      error=f"Text not found: '{text}'")
        
        except Exception as e:
            logger.error(f"Verify text error: {e}")
            return ExecutionResult("verify_text", params, False, error=str(e))
    
    def _search(self, params: Dict) -> ExecutionResult:
        """Search on current website"""
        
        try:
            query = params.get("query", "").strip()
            
            if not query:
                return ExecutionResult("search", params, False, 
                                      error="No query specified")
            
            logger.info(f"🔍 Searching: {query}")
            
            # Common search patterns
            pyautogui.hotkey("ctrl", "f")  # Open find
            time.sleep(0.5)
            pyautogui.typewrite(query, interval=0.05)
            pyautogui.press("enter")
            time.sleep(1)
            
            return ExecutionResult("search", params, True, 
                                  output=f"Searched: {query}")
        
        except Exception as e:
            logger.error(f"Search error: {e}")
            return ExecutionResult("search", params, False, error=str(e))
    
    def _select_all(self, params: Dict) -> ExecutionResult:
        """Select all (Ctrl+A)"""
        
        try:
            logger.info("📋 Select all")
            pyautogui.hotkey("ctrl", "a")
            time.sleep(0.3)
            
            return ExecutionResult("select_all", params, True, 
                                  output="Selected all")
        
        except Exception as e:
            logger.error(f"Select all error: {e}")
            return ExecutionResult("select_all", params, False, error=str(e))
    
    def _copy(self, params: Dict) -> ExecutionResult:
        """Copy (Ctrl+C)"""
        
        try:
            logger.info("📋 Copy")
            pyautogui.hotkey("ctrl", "c")
            time.sleep(0.3)
            
            return ExecutionResult("copy", params, True, 
                                  output="Copied")
        
        except Exception as e:
            logger.error(f"Copy error: {e}")
            return ExecutionResult("copy", params, False, error=str(e))
    
    def _paste(self, params: Dict) -> ExecutionResult:
        """Paste (Ctrl+V)"""
        
        try:
            logger.info("📋 Paste")
            pyautogui.hotkey("ctrl", "v")
            time.sleep(0.3)
            
            return ExecutionResult("paste", params, True, 
                                  output="Pasted")
        
        except Exception as e:
            logger.error(f"Paste error: {e}")
            return ExecutionResult("paste", params, False, error=str(e))
    
    def _clear_field(self, params: Dict) -> ExecutionResult:
        """Clear field (Select all + Delete)"""
        
        try:
            logger.info("🗑️ Clearing field")
            pyautogui.hotkey("ctrl", "a")
            time.sleep(0.1)
            pyautogui.press("delete")
            time.sleep(0.3)
            
            return ExecutionResult("clear_field", params, True, 
                                  output="Field cleared")
        
        except Exception as e:
            logger.error(f"Clear field error: {e}")
            return ExecutionResult("clear_field", params, False, error=str(e))


# ======================================
# EXPORT FUNCTIONS
# ======================================

_executor_instance = None

def get_executor() -> UniversalExecutor:
    """Get executor singleton"""
    global _executor_instance
    if _executor_instance is None:
        _executor_instance = UniversalExecutor()
    return _executor_instance

def execute_plan(plan: List[Dict]) -> Dict:
    """Execute action plan"""
    return get_executor().execute_plan(plan)

def execute_action(action: Dict) -> Dict:
    """Execute single action"""
    result = get_executor().execute_action(action)
    return result.to_dict()
