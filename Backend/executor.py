# executor.py
# FINAL FULL WORKING EXECUTOR

import os
import time
import subprocess
import pyautogui

from app_launcher import app_launcher
from browser_tools import browser_tools

pyautogui.FAILSAFE = False


class DynamicExecutor:

    # =====================================================
    # MAIN EXECUTOR
    # =====================================================

    def execute_plan(self, plan):

        results = []

        overall_success = False

        for step in plan:

            tool = step.get("tool")

            params = step.get(
                "params",
                {}
            )

            print(f"\n[EXECUTOR] TOOL: {tool}")

            print(f"[EXECUTOR] PARAMS: {params}")

            try:

                fn = getattr(

                    self,

                    f"tool_{tool}",

                    None
                )

                if fn is None:

                    raise Exception(
                        f"Tool not found: {tool}"
                    )

                result = fn(**params)

                success = False

                if isinstance(result, dict):

                    success = result.get(
                        "success",
                        False
                    )

                else:

                    success = bool(result)

                if success:

                    overall_success = True

                    print(
                        f"[EXECUTOR] SUCCESS: {tool}"
                    )

                else:

                    print(
                        f"[EXECUTOR] FAILED: {tool}"
                    )

                results.append({

                    "tool": tool,

                    "success": success,

                    "result": result
                })

            except Exception as e:

                print(
                    f"[EXECUTOR ERROR] {e}"
                )

                results.append({

                    "tool": tool,

                    "success": False,

                    "error": str(e)
                })

        return {

            "success": overall_success,

            "results": results
        }

    # =====================================================
    # OPEN VS CODE
    # =====================================================

    def tool_open_vscode(self):

        return app_launcher.open_app(
            "code"
        )

    # =====================================================
    # OPEN WORD
    # =====================================================

    def tool_open_word(self):

        return app_launcher.open_app(
            "word"
        )

    # =====================================================
    # OPEN EXCEL
    # =====================================================

    def tool_open_excel(self):

        return app_launcher.open_app(
            "excel"
        )

    # =====================================================
    # OPEN TERMINAL
    # =====================================================

    def tool_open_terminal(self):

        return app_launcher.open_app(
            "cmd"
        )

    # =====================================================
    # OPEN CHROME
    # =====================================================

    def tool_open_chrome(self):

        return app_launcher.open_app(
            "chrome"
        )

    # =====================================================
    # OPEN GEMINI
    # =====================================================

    def tool_open_gemini(self):

        return browser_tools.open_gemini()

    # =====================================================
    # OPEN CHATGPT
    # =====================================================

    def tool_open_chatgpt(self):

        return browser_tools.open_chatgpt()

    # =====================================================
    # GOOGLE SEARCH
    # =====================================================

    def tool_google_search(
        self,
        query
    ):

        return browser_tools.google_search(
            query
        )

    # =====================================================
    # YOUTUBE SEARCH
    # =====================================================

    def tool_youtube_search(
        self,
        query
    ):

        return browser_tools.youtube_search(
            query
        )

    # =====================================================
    # OPEN YOUTUBE
    # =====================================================

    def tool_open_youtube(self):

        return browser_tools.open_youtube()

    # =====================================================
    # CREATE FOLDER
    # =====================================================

    def tool_create_folder(

        self,

        name="NewFolder"
    ):

        desktop = os.path.join(

            os.path.expanduser("~"),

            "Desktop"
        )

        folder = os.path.join(
            desktop,
            name
        )

        os.makedirs(
            folder,
            exist_ok=True
        )

        exists = os.path.exists(folder)

        return {

            "success": exists,

            "folder": folder
        }

    # =====================================================
    # TYPE TEXT
    # =====================================================

    def tool_type_text(

        self,

        text
    ):

        pyautogui.write(

            text,

            interval=0.03
        )

        return {

            "success": True,

            "typed": text
        }

    # =====================================================
    # PRESS KEY
    # =====================================================

    def tool_press_key(

        self,

        key
    ):

        pyautogui.press(key)

        return {

            "success": True,

            "key": key
        }

    # =====================================================
    # HOTKEY
    # =====================================================

    def tool_hotkey(

        self,

        keys
    ):

        pyautogui.hotkey(*keys)

        return {

            "success": True,

            "keys": keys
        }

    # =====================================================
    # TAKE SCREENSHOT
    # =====================================================

    def tool_take_screenshot(self):

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

    # =====================================================
    # PLAY SPOTIFY
    # =====================================================

    def tool_play_spotify(

        self,

        search_query=""
    ):

        result = app_launcher.open_app(
            "spotify"
        )

        time.sleep(5)

        if search_query:

            pyautogui.hotkey(
                "ctrl",
                "l"
            )

            time.sleep(1)

            pyautogui.write(
                search_query,
                interval=0.03
            )

            pyautogui.press("enter")

        return result

    # =====================================================
    # UNKNOWN TASK
    # =====================================================

    def tool_unknown_task(

        self,

        original_task=None,

        error=None
    ):

        return {

            "success": False,

            "message": "Could not understand task",

            "task": original_task,

            "error": error
        }


# =====================================================
# GLOBAL EXECUTOR
# =====================================================

executor = DynamicExecutor()


# =====================================================
# EXPORT FUNCTION
# =====================================================

def execute_plan(plan):

    return executor.execute_plan(plan)