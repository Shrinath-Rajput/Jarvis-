import os
import time
import webbrowser
import subprocess
import pyautogui
import keyboard

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 1.8


class ToolImplementations:

    def __init__(self):

        print("✅ TOOL IMPLEMENTATIONS READY")

    # =====================================================
    # OPEN GOOGLE + SEARCH + CLICK FIRST LINK
    # =====================================================

    async def open_google_search(self, query=""):

        webbrowser.open(
            "https://www.google.com"
        )

        time.sleep(6)

        # SEARCH BOX
        pyautogui.hotkey("ctrl", "l")

        time.sleep(1)

        pyautogui.write(
            f"google.com/search?q={query}",
            interval=0.03
        )

        pyautogui.press("enter")

        time.sleep(5)

        # FIRST LINK
        pyautogui.press("tab")
        time.sleep(1)

        pyautogui.press("enter")

        return {

            "success": True,

            "result":
                "Google search completed"
        }

    # =====================================================
    # YOUTUBE SEARCH + PLAY FIRST VIDEO
    # =====================================================

    async def open_youtube_search(self, query=""):

        webbrowser.open(
            "https://www.youtube.com"
        )

        time.sleep(7)

        # SEARCH BAR
        pyautogui.hotkey("ctrl", "l")

        time.sleep(1)

        pyautogui.write(

            f"https://www.youtube.com/results?search_query={query}",

            interval=0.03
        )

        pyautogui.press("enter")

        time.sleep(6)

        # FIRST VIDEO
        pyautogui.press("tab")

        time.sleep(1)

        pyautogui.press("enter")

        return {

            "success": True,

            "result":
                "YouTube video played"
        }

    # =====================================================
    # GEMINI SEARCH
    # =====================================================

    async def open_gemini_search(self, query=""):

        webbrowser.open(
            "https://gemini.google.com/app"
        )

        time.sleep(10)

        # TRY TAB NAVIGATION
        for i in range(8):

            pyautogui.press("tab")

            time.sleep(0.4)

        pyautogui.press("enter")

        time.sleep(2)

        pyautogui.write(
            query,
            interval=0.04
        )

        time.sleep(1)

        pyautogui.press("enter")

        return {

            "success": True,

            "result":
                "Gemini search completed"
        }

    # =====================================================
    # OPEN VS CODE + CREATE FOLDER
    # =====================================================

    async def open_vscode_create_folder(

        self,

        folder_name="portfolio"
    ):

        # CREATE FOLDER

        desktop = os.path.join(

            os.path.expanduser("~"),

            "Desktop"
        )

        folder_path = os.path.join(

            desktop,

            folder_name
        )

        os.makedirs(

            folder_path,

            exist_ok=True
        )

        # OPEN VS CODE

        subprocess.Popen("code")

        time.sleep(8)

        # OPEN FOLDER

        pyautogui.hotkey(
            "ctrl",
            "k"
        )

        time.sleep(1)

        pyautogui.hotkey(
            "ctrl",
            "o"
        )

        time.sleep(4)

        pyautogui.write(
            folder_path,
            interval=0.03
        )

        time.sleep(1)

        pyautogui.press("enter")

        return {

            "success": True,

            "result":
                f"{folder_name} folder created"
        }

    # =====================================================
    # OPEN CHROME
    # =====================================================

    async def open_browser(self):

        webbrowser.open(
            "https://www.google.com"
        )

        return {

            "success": True,

            "result":
                "Browser opened"
        }