# ============================================
# FINAL DYNAMIC executor.py
# NO HARDCODED COMMANDS
# ============================================

import logging
import traceback
import pyautogui
import webbrowser
import subprocess
import os
import time

from datetime import datetime
from typing import List, Dict

from screen_ai import click_text

logging.basicConfig(
    level=logging.INFO
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

        self.results = []

        logger.info(
            "🤖 DYNAMIC EXECUTOR READY"
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
            )

            params = action.get(
                "params",
                {}
            )

            print(
                f"🔥 TOOL: {tool}"
            )

            # ====================================
            # OPEN WEBSITE
            # ====================================

            if tool == "open_website":

                url = params.get(
                    "url",
                    ""
                )

                webbrowser.open(url)

                time.sleep(6)

                return ExecutionResult(

                    action,

                    True,

                    f"Opened {url}"
                )

            # ====================================
            # OPEN APP
            # ====================================

            elif tool == "open_app":

                app = params.get(
                    "app",
                    ""
                )

                subprocess.Popen(app)

                time.sleep(5)

                return ExecutionResult(

                    action,

                    True,

                    f"Opened app: {app}"
                )

            # ====================================
            # OPEN FOLDER
            # ====================================

            elif tool == "open_folder":

                path = params.get(
                    "path",
                    ""
                )

                os.startfile(path)

                time.sleep(3)

                return ExecutionResult(

                    action,

                    True,

                    f"Opened folder: {path}"
                )

            # ====================================
            # CLICK TEXT
            # ====================================

            elif tool == "click_text":

                text = params.get(
                    "text",
                    ""
                )

                success = click_text(text)

                return ExecutionResult(

                    action,

                    success,

                    f"Clicked text: {text}"
                )

            # ====================================
            # CLICK POSITION
            # ====================================

            elif tool == "click":

                x = params.get("x")

                y = params.get("y")

                pyautogui.click(x, y)

                return ExecutionResult(

                    action,

                    True,

                    f"Clicked {x},{y}"
                )

            # ====================================
            # TYPE
            # ====================================

            elif tool == "type":

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

                    f"Pressed: {key}"
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
            # CREATE FOLDER
            # ====================================

            elif tool == "create_folder":

                path = params.get(
                    "path",
                    ""
                )

                os.makedirs(

                    path,

                    exist_ok=True
                )

                return ExecutionResult(

                    action,

                    True,

                    f"Folder created: {path}"
                )

            # ====================================
            # UNKNOWN TOOL
            # ====================================

            else:

                return ExecutionResult(

                    action,

                    False,

                    None,

                    f"Unknown tool: {tool}"
                )

        except Exception as e:

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