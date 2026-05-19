# ============================================
# FINAL FULL WORKING executor.py
# ============================================

import logging
import traceback
import pyautogui
import webbrowser
import time

from datetime import datetime
from typing import List, Dict

from browser_control import get_browser
from computer_control import ComputerControl
from config import DEBUG

from screen_ai import click_text

logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO
)

logger = logging.getLogger(__name__)

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 1.5


# ============================================
# RESULT
# ============================================

class ExecutionResult:

    def __init__(

        self,

        action,

        success,

        output=None,

        error=None
    ):

        self.action = action

        self.success = success

        self.output = output

        self.error = error

        self.timestamp = datetime.now()

    def to_dict(self):

        return {

            "action":
                self.action,

            "success":
                self.success,

            "output":
                self.output,

            "error":
                self.error,

            "timestamp":
                self.timestamp.isoformat()
        }


# ============================================
# EXECUTION ENGINE
# ============================================

class ExecutionEngine:

    def __init__(self):

        self.browser = get_browser()

        self.computer = ComputerControl()

        self.results = []

        logger.info(
            "🔥 FINAL EXECUTION ENGINE READY"
        )

    # ========================================
    # EXECUTE PLAN
    # ========================================

    def execute_plan(

        self,

        plan: List[Dict]
    ):

        self.results = []

        for action in plan:

            result = self.execute_action(
                action
            )

            self.results.append(result)

        return self.results

    # ========================================
    # EXECUTE SINGLE ACTION
    # ========================================

    def execute_action(

        self,

        action: Dict
    ):

        try:

            tool = action.get(
                "tool",
                ""
            ).lower()

            params = action.get(
                "params",
                {}
            )

            logger.info(
                f"RUNNING TOOL: {tool}"
            )

            # ====================================
            # OPEN WEBSITE
            # ====================================

            if tool in [

                "open_website",

                "navigate",

                "open_url"
            ]:

                url = params.get(
                    "url",
                    "https://google.com"
                )

                webbrowser.open(url)

                time.sleep(6)

                return ExecutionResult(

                    action,

                    True,

                    f"Opened {url}"
                )

            # ====================================
            # SEARCH GOOGLE
            # ====================================

            elif tool in [

                "search_google",

                "google_search"
            ]:

                query = params.get(
                    "query",
                    ""
                )

                url = (

                    "https://www.google.com/search?q="
                    + query
                )

                webbrowser.open(url)

                time.sleep(6)

                pyautogui.press("tab")

                time.sleep(1)

                pyautogui.press("enter")

                return ExecutionResult(

                    action,

                    True,

                    f"Searched Google: {query}"
                )

            # ====================================
            # YOUTUBE SEARCH
            # ====================================

            elif tool in [

                "search_youtube",

                "youtube_search"
            ]:

                query = params.get(
                    "query",
                    ""
                )

                url = (

                    "https://www.youtube.com/results?search_query="
                    + query
                )

                webbrowser.open(url)

                time.sleep(7)

                pyautogui.press("tab")

                time.sleep(1)

                pyautogui.press("enter")

                return ExecutionResult(

                    action,

                    True,

                    f"YouTube search: {query}"
                )

            # ====================================
            # CLICK
            # ====================================

            elif tool == "click":

                text = params.get(
                    "text",
                    ""
                )

                x = params.get("x")

                y = params.get("y")

                success = False

                # OCR CLICK
                if text:

                    success = click_text(text)

                # COORDINATE CLICK
                elif x is not None and y is not None:

                    pyautogui.click(x, y)

                    success = True

                return ExecutionResult(

                    action,

                    success,

                    f"Clicked {text or (x,y)}",

                    None if success else "Click failed"
                )

            # ====================================
            # TYPE
            # ====================================

            elif tool in [

                "type",

                "type_text"
            ]:

                text = params.get(
                    "text",
                    ""
                )

                pyautogui.write(

                    text,

                    interval=0.03
                )

                return ExecutionResult(

                    action,

                    True,

                    f"Typed: {text}"
                )

            # ====================================
            # PRESS KEY
            # ====================================

            elif tool == "press_key":

                key = params.get(
                    "key",
                    "enter"
                )

                pyautogui.press(key)

                return ExecutionResult(

                    action,

                    True,

                    f"Pressed {key}"
                )

            # ====================================
            # HOTKEY
            # ====================================

            elif tool == "hotkey":

                keys = params.get(
                    "keys",
                    []
                )

                pyautogui.hotkey(*keys)

                return ExecutionResult(

                    action,

                    True,

                    f"Hotkey: {keys}"
                )

            # ====================================
            # OPEN VS CODE
            # ====================================

            elif tool == "open_vscode":

                import subprocess

                subprocess.Popen("code")

                time.sleep(8)

                return ExecutionResult(

                    action,

                    True,

                    "VS Code opened"
                )

            # ====================================
            # CREATE FOLDER
            # ====================================

            elif tool == "create_folder":

                import os

                folder = params.get(
                    "name",
                    "NewFolder"
                )

                desktop = os.path.join(

                    os.path.expanduser("~"),

                    "Desktop"
                )

                path = os.path.join(
                    desktop,
                    folder
                )

                os.makedirs(

                    path,

                    exist_ok=True
                )

                return ExecutionResult(

                    action,

                    True,

                    f"Folder created: {folder}"
                )

            # ====================================
            # WAIT
            # ====================================

            elif tool == "wait":

                seconds = int(

                    params.get(
                        "seconds",
                        2
                    )
                )

                time.sleep(seconds)

                return ExecutionResult(

                    action,

                    True,

                    f"Waited {seconds}s"
                )

            # ====================================
            # DEFAULT
            # ====================================

            else:

                return ExecutionResult(

                    action,

                    False,

                    None,

                    f"Unknown tool: {tool}"
                )

        except Exception as e:

            logger.error(str(e))

            traceback.print_exc()

            return ExecutionResult(

                action,

                False,

                None,

                str(e)
            )

    # ========================================
    # GET RESULTS
    # ========================================

    def get_results(self):

        return [

            r.to_dict()

            for r in self.results
        ]


# ============================================
# GLOBAL ENGINE
# ============================================

engine = ExecutionEngine()


# ============================================
# HELPER
# ============================================

def execute_plan(plan):

    return engine.execute_plan(plan)