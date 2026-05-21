# app_launcher.py
"""
FULL DYNAMIC APP LAUNCHER
NO HARDCODED COMMANDS
REAL WINDOWS AUTOMATION
"""

import os
import time
import shutil
import logging
import subprocess
import psutil
import pyautogui

try:
    import pygetwindow as gw
except:
    gw = None

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)


class AppLauncher:

    def __init__(self):

        logger.info("🚀 Initializing Dynamic App Launcher")

        self.registry = self.build_dynamic_registry()

    # =====================================================
    # BUILD REGISTRY DYNAMICALLY
    # =====================================================

    def build_dynamic_registry(self):

        registry = {}

        logger.info("🔍 Building dynamic executable registry...")

        # PATH executables
        common_commands = [

            "chrome",
            "msedge",
            "firefox",
            "code",
            "python",
            "node",
            "git",
            "cmd",
            "powershell",
            "notepad",
            "spotify"
        ]

        for cmd in common_commands:

            exe = shutil.which(cmd)

            if exe:

                name = (
                    os.path.basename(exe)
                    .replace(".exe", "")
                    .lower()
                )

                registry[name] = exe

        # SEARCH WINDOWS PROGRAM FILES
        search_roots = [

            os.environ.get("ProgramFiles"),

            os.environ.get("ProgramFiles(x86)"),

            os.environ.get("LOCALAPPDATA")
        ]

        for root in search_roots:

            if not root:
                continue

            if not os.path.exists(root):
                continue

            logger.info(f"📂 Scanning: {root}")

            try:

                for current_root, dirs, files in os.walk(root):

                    for file in files:

                        if file.lower().endswith(".exe"):

                            exe_name = (
                                file
                                .replace(".exe", "")
                                .lower()
                            )

                            full_path = os.path.join(
                                current_root,
                                file
                            )

                            if exe_name not in registry:

                                registry[exe_name] = full_path

            except Exception as e:

                logger.warning(str(e))

        logger.info(
            f"✅ Registry loaded with {len(registry)} executables"
        )

        return registry

    # =====================================================
    # FIND APP
    # =====================================================

    def find_app(self, app_name):

        app_name = (
            app_name
            .lower()
            .strip()
        )

        # EXACT MATCH
        if app_name in self.registry:

            return self.registry[app_name]

        # PARTIAL MATCH
        for key, value in self.registry.items():

            if app_name in key:

                return value

        # FUZZY WORD MATCH
        words = app_name.split()

        for key, value in self.registry.items():

            score = 0

            for word in words:

                if word in key:

                    score += 1

            if score > 0:

                return value

        return None

    # =====================================================
    # VERIFY PROCESS
    # =====================================================

    def verify_process(self, exe_path):

        try:

            exe_name = os.path.basename(
                exe_path
            ).lower()

            for proc in psutil.process_iter(

                ['name']

            ):

                try:

                    if proc.info['name']:

                        if proc.info['name'].lower() == exe_name:

                            logger.info(
                                f"✅ Verified process: {exe_name}"
                            )

                            return True

                except:
                    pass

        except Exception as e:

            logger.error(str(e))

        return False

    # =====================================================
    # OPEN APPLICATION
    # =====================================================

    def open_app(
        self,
        app_name,
        wait_time=3
    ):

        try:

            logger.info(
                f"🚀 Opening app: {app_name}"
            )

            app_path = self.find_app(app_name)

            if not app_path:

                return {

                    "success": False,

                    "error": f"Application not found: {app_name}"
                }

            logger.info(
                f"📍 Resolved path: {app_path}"
            )

            proc = subprocess.Popen(

                app_path,

                shell=False
            )

            logger.info(
                f"🆔 PID: {proc.pid}"
            )

            time.sleep(wait_time)

            verified = self.verify_process(
                app_path
            )

            if not verified:

                return {

                    "success": False,

                    "error": f"Failed to verify launch: {app_name}",

                    "path": app_path
                }

            return {

                "success": True,

                "message": f"Opened {app_name}",

                "path": app_path,

                "pid": proc.pid,

                "verified": True
            }

        except Exception as e:

            logger.error(str(e))

            return {

                "success": False,

                "error": str(e),

                "app": app_name
            }

    # =====================================================
    # CLOSE APPLICATION
    # =====================================================

    def close_app(self, app_name):

        try:

            app_path = self.find_app(app_name)

            if not app_path:

                return {

                    "success": False,

                    "error": "Application not found"
                }

            exe_name = os.path.basename(
                app_path
            )

            subprocess.run(

                f'taskkill /f /im "{exe_name}"',

                shell=True,

                capture_output=True
            )

            time.sleep(1)

            if self.verify_process(app_path):

                return {

                    "success": False,

                    "error": f"Failed to close {app_name}"
                }

            return {

                "success": True,

                "message": f"Closed {app_name}"
            }

        except Exception as e:

            return {

                "success": False,

                "error": str(e)
            }

    # =====================================================
    # FOCUS WINDOW
    # =====================================================

    def focus_window(self, title):

        try:

            if gw is None:

                return {

                    "success": False,

                    "error": "pygetwindow not installed"
                }

            windows = gw.getWindowsWithTitle(title)

            if not windows:

                return {

                    "success": False,

                    "error": f"No window found: {title}"
                }

            win = windows[0]

            win.activate()

            time.sleep(1)

            return {

                "success": True,

                "message": f"Focused window: {title}"
            }

        except Exception as e:

            return {

                "success": False,

                "error": str(e)
            }

    # =====================================================
    # TYPE TEXT
    # =====================================================

    def type_text(
        self,
        text,
        interval=0.03
    ):

        try:

            pyautogui.write(

                text,

                interval=interval
            )

            return {

                "success": True,

                "typed": text
            }

        except Exception as e:

            return {

                "success": False,

                "error": str(e)
            }

    # =====================================================
    # PRESS KEY
    # =====================================================

    def press_key(self, key):

        try:

            pyautogui.press(key)

            return {

                "success": True,

                "key": key
            }

        except Exception as e:

            return {

                "success": False,

                "error": str(e)
            }

    # =====================================================
    # HOTKEY
    # =====================================================

    def hotkey(self, *keys):

        try:

            pyautogui.hotkey(*keys)

            return {

                "success": True,

                "keys": keys
            }

        except Exception as e:

            return {

                "success": False,

                "error": str(e)
            }

    # =====================================================
    # SCREENSHOT
    # =====================================================

    def take_screenshot(self):

        try:

            desktop = os.path.join(

                os.path.expanduser("~"),

                "Desktop"
            )

            filename = os.path.join(

                desktop,

                f"screenshot_{int(time.time())}.png"
            )

            image = pyautogui.screenshot()

            image.save(filename)

            return {

                "success": True,

                "file": filename
            }

        except Exception as e:

            return {

                "success": False,

                "error": str(e)
            }

    # =====================================================
    # LIST APPS
    # =====================================================

    def list_apps(self):

        return {

            "success": True,

            "count": len(self.registry),

            "apps": sorted(
                list(
                    self.registry.keys()
                )
            )
        }


# =====================================================
# GLOBAL INSTANCE
# =====================================================

app_launcher = AppLauncher()