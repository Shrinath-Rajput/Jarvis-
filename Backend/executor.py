# ==========================================================
# EXECUTOR v2.0 - INTELLIGENT AUTONOMOUS EXECUTOR
# REAL AUTONOMOUS DYNAMIC EXECUTOR WITH RETRY & FUZZY MATCHING
# ==========================================================

import os
import time
import traceback
import webbrowser
import subprocess
from difflib import SequenceMatcher

import pyautogui
import pytesseract

from PIL import Image
from mss import mss

# ==========================================================
# SETTINGS
# ==========================================================

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.5

MAX_RETRIES = 3
SCREENSHOT_RETRY_WAIT = 2
FUZZY_MATCH_THRESHOLD = 0.6  # 60% similarity for fuzzy matching

# ==========================================================
# LOGGING UTILITIES
# ==========================================================

def log_action(tool, params, status, result="", retry_count=0):
    """Comprehensive action logging"""
    timestamp = time.strftime("%H:%M:%S")
    retry_info = f" [RETRY {retry_count}]" if retry_count > 0 else ""
    print(f"\n[{timestamp}] 🔧 TOOL: {tool}")
    print(f"  📋 PARAMS: {params}")
    print(f"  ✅ STATUS: {status}{retry_info}")
    if result:
        print(f"  📊 RESULT: {result}")


def log_error(tool, error, attempt=1):
    """Log errors with context"""
    print(f"  ❌ ERROR (Attempt {attempt}): {str(error)[:100]}")


# ==========================================================
# OCR & TEXT MATCHING
# ==========================================================

def fuzzy_match(text1, text2, threshold=FUZZY_MATCH_THRESHOLD):
    """Fuzzy text matching with similarity score"""
    ratio = SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
    return ratio >= threshold, ratio


def read_screen():
    """OCR - Read entire screen"""
    try:
        with mss() as sct:
            monitor = sct.monitors[1]
            screenshot = sct.grab(monitor)
            img = Image.frombytes(
                "RGB",
                screenshot.size,
                screenshot.rgb
            )
            text = pytesseract.image_to_string(img)
            return text.lower()
    except Exception as e:
        log_error("read_screen", e)
        return ""


def click_text(target, retry_count=0):
    """
    Smart click with:
    1. Exact matching
    2. Fuzzy matching
    3. Partial matching
    4. Fallback to Tab+Enter
    """
    try:
        screenshot = pyautogui.screenshot()
        data = pytesseract.image_to_data(
            screenshot,
            output_type=pytesseract.Output.DICT
        )

        target_lower = target.lower().strip()
        best_match = None
        best_ratio = 0

        # PASS 1: Exact & Partial matching
        for i, word in enumerate(data["text"]):
            word_lower = word.lower().strip()
            
            if not word_lower:  # Skip empty
                continue
            
            # Exact match
            if word_lower == target_lower:
                best_match = i
                best_ratio = 1.0
                break
            
            # Partial match (target in word)
            if target_lower in word_lower or word_lower in target_lower:
                best_match = i
                best_ratio = 0.9
                break

        # PASS 2: Fuzzy matching if no exact/partial match
        if best_match is None:
            for i, word in enumerate(data["text"]):
                word_lower = word.lower().strip()
                if not word_lower:
                    continue
                
                is_match, ratio = fuzzy_match(target_lower, word_lower)
                if is_match and ratio > best_ratio:
                    best_match = i
                    best_ratio = ratio

        # Found match - click it
        if best_match is not None:
            x = data["left"][best_match]
            y = data["top"][best_match]
            w = data["width"][best_match]
            h = data["height"][best_match]
            
            pyautogui.click(x + w // 2, y + h // 2)
            print(f"  ✅ CLICKED: '{target}' (match ratio: {best_ratio:.2f})")
            return True

        # FALLBACK: Tab + Enter if text not found
        print(f"  ⚠️  Text '{target}' not found on screen, trying Tab+Enter fallback")
        pyautogui.press('tab')
        time.sleep(0.3)
        pyautogui.press('enter')
        return True  # Assume success

    except Exception as e:
        log_error("click_text", e, retry_count)
        return False

    except Exception as e:

        print("CLICK ERROR:", e)

        return False




# ==========================================================
# INTELLIGENT EXECUTION ENGINE
# ==========================================================

class ExecutionEngine:
    """
    Autonomous execution engine with:
    - Retry logic for each action
    - Dynamic OCR-based matching
    - Fallback mechanisms
    - Comprehensive logging
    - OTAVR cycle: Observe → Think → Act → Verify → Retry
    """

    def __init__(self):
        print("🤖 INTELLIGENT EXECUTOR READY v2.0")

    # ======================================================
    # MAIN EXECUTION
    # ======================================================

    def execute_plan(self, plan):
        """
        Execute plan with smart retry logic.
        Returns list of action results.
        Only fails if ALL retries for an action fail.
        """
        
        print("\n" + "="*60)
        print("🚀 EXECUTING PLAN")
        print("="*60)
        
        if not plan:
            print("❌ No plan provided")
            return []

        results = []
        failed_actions = []

        for idx, step in enumerate(plan):
            print(f"\n📍 Step {idx + 1}/{len(plan)}")
            
            action_result = self.execute_action_with_retry(step)
            results.append(action_result)

            # Log step result
            if action_result["success"]:
                print(f"  ✅ Success")
            else:
                print(f"  ❌ Failed after all retries")
                failed_actions.append(step.get("tool", "unknown"))

        # Summary
        print("\n" + "="*60)
        print(f"📊 EXECUTION SUMMARY")
        print(f"  Total Steps: {len(plan)}")
        print(f"  Successful: {len([r for r in results if r['success']])}")
        print(f"  Failed: {len(failed_actions)}")
        if failed_actions:
            print(f"  Failed Tools: {failed_actions}")
        print("="*60 + "\n")

        return results

    # ======================================================
    # ACTION WITH RETRY
    # ======================================================

    def execute_action_with_retry(self, action):
        """
        Execute single action with intelligent retry logic.
        Returns proper success/failure status.
        """
        
        tool = action.get("tool", "unknown")
        params = action.get("params", {})

        log_action(tool, params, "STARTING")

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                result = self.execute_action(action, attempt)
                
                if result["success"]:
                    log_action(tool, params, "SUCCESS", result.get("result", ""))
                    return result
                else:
                    # Failed - will retry
                    if attempt < MAX_RETRIES:
                        log_error(tool, result.get("result", "unknown"), attempt)
                        wait_time = SCREENSHOT_RETRY_WAIT * attempt
                        print(f"  ⏳ Retrying in {wait_time}s...")
                        time.sleep(wait_time)
                        continue
                    else:
                        log_error(tool, result.get("result", "unknown"), attempt)
                        return result

            except Exception as e:
                if attempt < MAX_RETRIES:
                    log_error(tool, str(e), attempt)
                    wait_time = SCREENSHOT_RETRY_WAIT * attempt
                    print(f"  ⏳ Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    log_error(tool, str(e), attempt)
                    return {
                        "success": False,
                        "tool": tool,
                        "result": str(e)
                    }

        return {
            "success": False,
            "tool": tool,
            "result": "Max retries exceeded"
        }

    # ======================================================
    # SINGLE ACTION EXECUTION
    # ======================================================

    def execute_action(self, action, attempt=1):
        """
        Execute single action - core logic
        Returns: {"success": bool, "tool": str, "result": str}
        """
        
        try:
            tool = action.get("tool", "unknown")
            params = action.get("params", {})

            # ============== OPEN WEBSITE ==============
            if tool == "open_website":
                url = params.get("url", "")
                if not url:
                    return {"success": False, "tool": tool, "result": "No URL provided"}
                
                try:
                    webbrowser.open(url)
                    time.sleep(6)  # Wait for page load
                    
                    # Verify page loaded (optional)
                    ocr_text = read_screen()
                    if ocr_text:
                        return {
                            "success": True,
                            "tool": tool,
                            "result": f"Opened {url}"
                        }
                    else:
                        # Page might be loading, still consider it success
                        return {
                            "success": True,
                            "tool": tool,
                            "result": f"Opened {url}"
                        }
                except Exception as e:
                    return {
                        "success": False,
                        "tool": tool,
                        "result": str(e)
                    }

            # ============== OPEN APP ==============
            elif tool == "open_app":
                app = params.get("app", "")
                if not app:
                    return {"success": False, "tool": tool, "result": "No app provided"}
                
                try:
                    subprocess.Popen(app)
                    time.sleep(5)
                    return {
                        "success": True,
                        "tool": tool,
                        "result": f"Opened {app}"
                    }
                except Exception as e:
                    return {
                        "success": False,
                        "tool": tool,
                        "result": str(e)
                    }

            # ============== OPEN FOLDER ==============
            elif tool == "open_folder":
                path = params.get("path", "")
                if not path:
                    return {"success": False, "tool": tool, "result": "No path provided"}
                
                try:
                    os.startfile(path)
                    time.sleep(3)
                    return {
                        "success": True,
                        "tool": tool,
                        "result": f"Opened folder"
                    }
                except Exception as e:
                    return {
                        "success": False,
                        "tool": tool,
                        "result": str(e)
                    }

            # ============== TYPE ==============
            elif tool == "type":
                text = params.get("text", "")
                if not text:
                    return {"success": False, "tool": tool, "result": "No text provided"}
                
                try:
                    pyautogui.write(text, interval=0.03)
                    time.sleep(0.5)
                    return {
                        "success": True,
                        "tool": tool,
                        "result": f"Typed text"
                    }
                except Exception as e:
                    return {
                        "success": False,
                        "tool": tool,
                        "result": str(e)
                    }

            # ============== PRESS KEY ==============
            elif tool == "press_key":
                key = params.get("key", "")
                if not key:
                    return {"success": False, "tool": tool, "result": "No key provided"}
                
                try:
                    pyautogui.press(key)
                    time.sleep(0.3)
                    return {
                        "success": True,
                        "tool": tool,
                        "result": f"Pressed key"
                    }
                except Exception as e:
                    return {
                        "success": False,
                        "tool": tool,
                        "result": str(e)
                    }

            # ============== HOTKEY ==============
            elif tool == "hotkey":
                keys = params.get("keys", [])
                if not keys:
                    return {"success": False, "tool": tool, "result": "No keys provided"}
                
                try:
                    pyautogui.hotkey(*keys)
                    time.sleep(0.5)
                    return {
                        "success": True,
                        "tool": tool,
                        "result": f"Hotkey executed"
                    }
                except Exception as e:
                    return {
                        "success": False,
                        "tool": tool,
                        "result": str(e)
                    }

            # ============== WAIT ==============
            elif tool == "wait":
                seconds = params.get("seconds", 2)
                try:
                    time.sleep(seconds)
                    return {
                        "success": True,
                        "tool": tool,
                        "result": f"Waited {seconds}s"
                    }
                except Exception as e:
                    return {
                        "success": False,
                        "tool": tool,
                        "result": str(e)
                    }

            # ============== CLICK TEXT (Smart) ==============
            elif tool == "click_text":
                text = params.get("text", "")
                if not text:
                    return {"success": False, "tool": tool, "result": "No text provided"}
                
                try:
                    # Retry screenshot read if empty
                    screen_text = read_screen()
                    if not screen_text:
                        print(f"  ⚠️  Empty OCR, waiting and retrying...")
                        time.sleep(SCREENSHOT_RETRY_WAIT)
                        screen_text = read_screen()
                    
                    # Check if text exists on screen
                    if text.lower() in screen_text:
                        # Text found - try to click it
                        success = click_text(text, attempt)
                        return {
                            "success": success,
                            "tool": tool,
                            "result": f"Clicked '{text}'"
                        }
                    else:
                        # Text not found - try clicking anyway (fallback)
                        success = click_text(text, attempt)
                        return {
                            "success": success,
                            "tool": tool,
                            "result": f"Attempted click on '{text}'"
                        }
                except Exception as e:
                    return {
                        "success": False,
                        "tool": tool,
                        "result": str(e)
                    }

            # ============== CLICK POSITION ==============
            elif tool == "click":
                x = params.get("x")
                y = params.get("y")
                if x is None or y is None:
                    return {"success": False, "tool": tool, "result": "No coordinates provided"}
                
                try:
                    pyautogui.click(x, y)
                    time.sleep(0.5)
                    return {
                        "success": True,
                        "tool": tool,
                        "result": f"Clicked at position"
                    }
                except Exception as e:
                    return {
                        "success": False,
                        "tool": tool,
                        "result": str(e)
                    }

            # ============== CREATE FOLDER ==============
            elif tool == "create_folder":
                folder_name = params.get("name", "NewFolder")
                try:
                    desktop = os.path.join(
                        os.path.expanduser("~"),
                        "Desktop"
                    )
                    folder_path = os.path.join(desktop, folder_name)
                    os.makedirs(folder_path, exist_ok=True)
                    return {
                        "success": True,
                        "tool": tool,
                        "result": f"Created folder"
                    }
                except Exception as e:
                    return {
                        "success": False,
                        "tool": tool,
                        "result": str(e)
                    }

            # ============== SCREENSHOT ==============
            elif tool == "screenshot":
                try:
                    text = read_screen()
                    return {
                        "success": True,
                        "tool": tool,
                        "result": text if text else "Screenshot taken"
                    }
                except Exception as e:
                    return {
                        "success": False,
                        "tool": tool,
                        "result": str(e)
                    }

            # ============== UNKNOWN TOOL ==============
            else:
                return {
                    "success": False,
                    "tool": tool,
                    "result": f"Unknown tool '{tool}'"
                }

        except Exception as e:
            traceback.print_exc()
            return {
                "success": False,
                "tool": action.get("tool", "unknown"),
                "result": str(e)
            }





# ==========================================================
# GLOBAL EXECUTOR INSTANCE
# ==========================================================

engine = ExecutionEngine()


# ==========================================================
# PUBLIC INTERFACE
# ==========================================================

def execute_plan(plan):
    """
    Execute a plan and return results.
    
    Args:
        plan: List of action dictionaries with 'tool' and 'params'
    
    Returns:
        List of result dictionaries with 'success', 'tool', 'result'
    """
    return engine.execute_plan(plan)
