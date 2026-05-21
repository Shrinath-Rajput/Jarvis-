# browser_tools.py
"""
Browser automation and control tools for JARVIS
FINAL WORKING VERSION
"""

import webbrowser
import subprocess
import time
import os
import logging
import psutil

# ============================================
# LOGGING
# ============================================

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

logger = logging.getLogger(__name__)

# ============================================
# CLASS
# ============================================

class BrowserTools:

    # ============================================
    # GET BROWSER PATH
    # ============================================

    @staticmethod
    def _get_browser_executable(browser_name):

        browser_paths = {

            "chrome": [

                r"C:\Program Files\Google\Chrome\Application\chrome.exe",

                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",

                "chrome.exe"
            ],

            "firefox": [

                r"C:\Program Files\Mozilla Firefox\firefox.exe",

                r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe",

                "firefox.exe"
            ],

            "edge": [

                r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",

                r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",

                "msedge.exe"
            ]
        }

        paths = browser_paths.get(
            browser_name.lower(),
            []
        )

        for path in paths:

            if os.path.exists(path):

                return path

            try:

                result = subprocess.run(

                    f"where {path}",

                    shell=True,

                    capture_output=True,

                    text=True,

                    timeout=2
                )

                if result.returncode == 0:

                    return result.stdout.strip().split('\n')[0]

            except:
                pass

        return None

    # ============================================
    # VERIFY BROWSER
    # ============================================

    @staticmethod
    def _is_browser_running(browser_name):

        processes = {

            "chrome": "chrome.exe",

            "firefox": "firefox.exe",

            "edge": "msedge.exe"
        }

        target = processes.get(
            browser_name.lower()
        )

        if not target:
            return False

        try:

            for proc in psutil.process_iter(['name']):

                name = proc.info['name']

                if name and name.lower() == target.lower():

                    return True

        except:
            pass

        return False

    # ============================================
    # OPEN CHROME
    # ============================================

    @staticmethod
    def open_chrome(url=None):

        try:

            logger.info("OPENING CHROME")

            chrome = BrowserTools._get_browser_executable(
                "chrome"
            )

            if not chrome:

                return {

                    "success": False,

                    "error": "Chrome not found"
                }

            if url:

                if not url.startswith("http"):

                    url = "https://" + url

                subprocess.Popen(
                    f'"{chrome}" "{url}"'
                )

            else:

                subprocess.Popen(chrome)

            time.sleep(3)

            verified = BrowserTools._is_browser_running(
                "chrome"
            )

            return {

                "success": verified,

                "message": "Chrome opened",

                "verified": verified
            }

        except Exception as e:

            return {

                "success": False,

                "error": str(e)
            }

    # ============================================
    # GOOGLE SEARCH
    # ============================================

    @staticmethod
    def google_search(query):

        try:

            url = (
                "https://www.google.com/search?q="
                + query.replace(" ", "+")
            )

            return BrowserTools.open_chrome(url)

        except Exception as e:

            return {

                "success": False,

                "error": str(e)
            }

    # ============================================
    # YOUTUBE SEARCH
    # ============================================

    @staticmethod
    def youtube_search(query):

        try:

            url = (
                "https://www.youtube.com/results?search_query="
                + query.replace(" ", "+")
            )

            return BrowserTools.open_chrome(url)

        except Exception as e:

            return {

                "success": False,

                "error": str(e)
            }

    # ============================================
    # OPEN WEBSITE
    # ============================================

    @staticmethod
    def open_website(url):

        try:

            return BrowserTools.open_chrome(url)

        except Exception as e:

            return {

                "success": False,

                "error": str(e)
            }

    # ============================================
    # OPEN GMAIL
    # ============================================

    @staticmethod
    def open_gmail():

        return BrowserTools.open_chrome(
            "https://mail.google.com"
        )

    # ============================================
    # AMAZON SEARCH
    # ============================================

    @staticmethod
    def amazon_search(query):

        try:

            url = (
                "https://www.amazon.in/s?k="
                + query.replace(" ", "+")
            )

            return BrowserTools.open_chrome(url)

        except Exception as e:

            return {

                "success": False,

                "error": str(e)
            }

    # ============================================
    # OPEN YOUTUBE
    # ============================================

    @staticmethod
    def open_youtube():

        return BrowserTools.open_chrome(
            "https://www.youtube.com"
        )

    # ============================================
    # OPEN GEMINI
    # ============================================

    @staticmethod
    def open_gemini():

        return BrowserTools.open_chrome(
            "https://gemini.google.com"
        )

    # ============================================
    # OPEN CHATGPT
    # ============================================

    @staticmethod
    def open_chatgpt():

        return BrowserTools.open_chrome(
            "https://chatgpt.com"
        )

    # ============================================
    # INCOGNITO
    # ============================================

    @staticmethod
    def open_incognito():

        try:

            chrome = BrowserTools._get_browser_executable(
                "chrome"
            )

            if not chrome:

                return {

                    "success": False,

                    "error": "Chrome not found"
                }

            subprocess.Popen(
                f'"{chrome}" --incognito'
            )

            time.sleep(2)

            return {

                "success": True,

                "message": "Incognito opened"
            }

        except Exception as e:

            return {

                "success": False,

                "error": str(e)
            }

    # ============================================
    # NEW TAB
    # ============================================

    @staticmethod
    def new_tab():

        try:

            import pyautogui

            pyautogui.hotkey(
                "ctrl",
                "t"
            )

            return {

                "success": True,

                "message": "New tab opened"
            }

        except Exception as e:

            return {

                "success": False,

                "error": str(e)
            }

    # ============================================
    # CLOSE TABS
    # ============================================

    @staticmethod
    def close_tabs():

        try:

            import pyautogui

            pyautogui.hotkey(
                "ctrl",
                "shift",
                "w"
            )

            return {

                "success": True,

                "message": "Tabs closed"
            }

        except Exception as e:

            return {

                "success": False,

                "error": str(e)
            }

# ============================================
# EXPORT
# ============================================

browser_tools = BrowserTools()