"""
FINAL STABLE TOOL IMPLEMENTATIONS
100% WORKING VERSION
YOUTUBE SEARCH + CLICK + TYPE
VS CODE
FOLDER CREATE
CHATGPT
GEMINI
GOOGLE
"""

import os
import logging
import webbrowser
import pyautogui
import asyncio
import subprocess
from pathlib import Path
from typing import Dict, Any

from tool_registry import (
    Tool,
    ToolRegistry,
    ToolCategory,
    get_tool_registry
)

# =========================================================
# CONFIG
# =========================================================

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 1

# =========================================================
# APPLICATION TOOLS
# =========================================================

async def launch_application(
    app_name: str,
    arguments: str = ""
) -> Dict[str, Any]:

    try:

        app_name = app_name.lower()

        if app_name in ["chrome", "browser"]:

            subprocess.Popen(
                r'C:\Program Files\Google\Chrome\Application\chrome.exe'
            )

        elif app_name in ["vscode", "vs code", "code"]:

            subprocess.Popen("code")

        elif app_name == "notepad":

            subprocess.Popen("notepad")

        elif app_name == "calculator":

            subprocess.Popen("calc")

        else:

            os.system(f"start {app_name}")

        await asyncio.sleep(3)

        pyautogui.hotkey("win", "up")

        return {

            "success": True,

            "message": f"{app_name} launched"
        }

    except Exception as e:

        return {

            "success": False,

            "error": str(e)
        }

# =========================================================
# WEBSITE
# =========================================================

async def open_website(
    site_name: str = "",
    url: str = ""
) -> Dict[str, Any]:

    websites = {

        "youtube":
            "https://www.youtube.com",

        "google":
            "https://www.google.com",

        "chatgpt":
            "https://chat.openai.com",

        "gemini":
            "https://gemini.google.com",
    }

    try:

        target_url = url

        if not target_url:

            target_url = websites.get(
                site_name.lower(),
                f"https://{site_name}.com"
            )

        logger.info(
            f"🌐 Opening {target_url}"
        )

        webbrowser.open(target_url)

        await asyncio.sleep(5)

        pyautogui.hotkey("win", "up")

        await asyncio.sleep(1)

        return {

            "success": True,

            "message": f"Opened {target_url}"
        }

    except Exception as e:

        return {

            "success": False,

            "error": str(e)
        }

# =========================================================
# SEARCH GOOGLE
# =========================================================

async def search_google(
    query: str
) -> Dict[str, Any]:

    try:

        search_url = (
            "https://www.google.com/search?q="
            + query.replace(" ", "+")
        )

        webbrowser.open(search_url)

        await asyncio.sleep(5)

        return {

            "success": True,

            "message": f"Searched Google: {query}"
        }

    except Exception as e:

        return {

            "success": False,

            "error": str(e)
        }

# =========================================================
# SEARCH YOUTUBE
# =========================================================

async def search_youtube(
    query: str
) -> Dict[str, Any]:

    try:

        search_url = (
            "https://www.youtube.com/results?search_query="
            + query.replace(" ", "+")
        )

        webbrowser.open(search_url)

        await asyncio.sleep(5)

        return {

            "success": True,

            "message": f"Searched YouTube: {query}"
        }

    except Exception as e:

        return {

            "success": False,

            "error": str(e)
        }

# =========================================================
# CREATE FOLDER
# =========================================================

async def create_folder(
    folder_path: str
) -> Dict[str, Any]:

    try:

        Path(folder_path).mkdir(

            parents=True,

            exist_ok=True
        )

        return {

            "success": True,

            "message":
                f"Folder created: {folder_path}"
        }

    except Exception as e:

        return {

            "success": False,

            "error": str(e)
        }

# =========================================================
# CREATE FILE
# =========================================================

async def create_file(
    file_path: str,
    content: str = ""
) -> Dict[str, Any]:

    try:

        Path(file_path).parent.mkdir(

            parents=True,

            exist_ok=True
        )

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(content)

        return {

            "success": True,

            "message":
                f"Created file: {file_path}"
        }

    except Exception as e:

        return {

            "success": False,

            "error": str(e)
        }

# =========================================================
# WRITE FILE
# =========================================================

async def write_to_file(
    file_path: str,
    content: str,
    append: bool = False
) -> Dict[str, Any]:

    try:

        mode = "a" if append else "w"

        with open(
            file_path,
            mode,
            encoding="utf-8"
        ) as f:

            f.write(content)

        return {

            "success": True,

            "message":
                f"Written file: {file_path}"
        }

    except Exception as e:

        return {

            "success": False,

            "error": str(e)
        }

# =========================================================
# TYPE TEXT
# =========================================================

async def type_text(
    text: str,
    delay: float = 0.05
) -> Dict[str, Any]:

    try:

        await asyncio.sleep(1)

        pyautogui.click()

        await asyncio.sleep(0.5)

        pyautogui.write(

            text,

            interval=delay
        )

        return {

            "success": True,

            "message": f"Typed: {text}"
        }

    except Exception as e:

        return {

            "success": False,

            "error": str(e)
        }

# =========================================================
# PRESS KEY
# =========================================================

async def press_key(
    key_name: str,
    times: int = 1
) -> Dict[str, Any]:

    try:

        await asyncio.sleep(0.5)

        for _ in range(times):

            pyautogui.press(key_name)

            await asyncio.sleep(0.3)

        return {

            "success": True,

            "message": f"Pressed {key_name}"
        }

    except Exception as e:

        return {

            "success": False,

            "error": str(e)
        }

# =========================================================
# HOTKEY
# =========================================================

async def press_hotkey(
    *keys
) -> Dict[str, Any]:

    try:

        pyautogui.hotkey(*keys)

        return {

            "success": True,

            "message":
                f"Pressed {' + '.join(keys)}"
        }

    except Exception as e:

        return {

            "success": False,

            "error": str(e)
        }

# =========================================================
# MOVE MOUSE
# =========================================================

async def move_mouse(
    x: int,
    y: int,
    duration: float = 1
) -> Dict[str, Any]:

    try:

        pyautogui.moveTo(

            x,
            y,
            duration=duration
        )

        return {

            "success": True,

            "message":
                f"Moved to {x},{y}"
        }

    except Exception as e:

        return {

            "success": False,

            "error": str(e)
        }

# =========================================================
# CLICK
# =========================================================

async def click_mouse(
    x: int,
    y: int,
    button: str = "left",
    clicks: int = 1
) -> Dict[str, Any]:

    try:

        pyautogui.moveTo(

            x,
            y,
            duration=1
        )

        await asyncio.sleep(0.5)

        pyautogui.click(

            x=x,
            y=y,
            button=button,
            clicks=clicks
        )

        return {

            "success": True,

            "message":
                f"Clicked at {x},{y}"
        }

    except Exception as e:

        return {

            "success": False,

            "error": str(e)
        }

# =========================================================
# SCROLL
# =========================================================

async def scroll(
    direction: str = "down",
    amount: int = 500
) -> Dict[str, Any]:

    try:

        if direction == "down":

            pyautogui.scroll(-amount)

        else:

            pyautogui.scroll(amount)

        return {

            "success": True,

            "message":
                f"Scrolled {direction}"
        }

    except Exception as e:

        return {

            "success": False,

            "error": str(e)
        }

# =========================================================
# SCREENSHOT
# =========================================================

async def take_screenshot():

    try:

        screenshot = pyautogui.screenshot()

        path = "jarvis_screenshot.png"

        screenshot.save(path)

        return {

            "success": True,

            "path": path
        }

    except Exception as e:

        return {

            "success": False,

            "error": str(e)
        }

# =========================================================
# WAIT
# =========================================================

async def wait(
    seconds: float
):

    await asyncio.sleep(seconds)

    return {

        "success": True,

        "message": f"Waited {seconds}"
    }

# =========================================================
# REGISTER TOOLS
# =========================================================

def register_all_tools():

    registry = get_tool_registry()

    registry.register(Tool(
        name="launch_app",
        category=ToolCategory.APPLICATION,
        function=launch_application,
        description="Launch application",
        parameters=[]
    ))

    registry.register(Tool(
        name="open_website",
        category=ToolCategory.BROWSER,
        function=open_website,
        description="Open website",
        parameters=[]
    ))

    registry.register(Tool(
        name="search_google",
        category=ToolCategory.BROWSER,
        function=search_google,
        description="Search Google",
        parameters=[]
    ))

    registry.register(Tool(
        name="search_youtube",
        category=ToolCategory.BROWSER,
        function=search_youtube,
        description="Search YouTube",
        parameters=[]
    ))

    registry.register(Tool(
        name="create_folder",
        category=ToolCategory.FILE_SYSTEM,
        function=create_folder,
        description="Create folder",
        parameters=[]
    ))

    registry.register(Tool(
        name="create_file",
        category=ToolCategory.FILE_SYSTEM,
        function=create_file,
        description="Create file",
        parameters=[]
    ))

    registry.register(Tool(
        name="write_file",
        category=ToolCategory.FILE_SYSTEM,
        function=write_to_file,
        description="Write file",
        parameters=[]
    ))

    registry.register(Tool(
        name="type_text",
        category=ToolCategory.KEYBOARD,
        function=type_text,
        description="Type text",
        parameters=[]
    ))

    registry.register(Tool(
        name="press_key",
        category=ToolCategory.KEYBOARD,
        function=press_key,
        description="Press key",
        parameters=[]
    ))

    registry.register(Tool(
        name="press_hotkey",
        category=ToolCategory.KEYBOARD,
        function=press_hotkey,
        description="Hotkey",
        parameters=[]
    ))

    registry.register(Tool(
        name="move_mouse",
        category=ToolCategory.MOUSE,
        function=move_mouse,
        description="Move mouse",
        parameters=[]
    ))

    registry.register(Tool(
        name="click",
        category=ToolCategory.MOUSE,
        function=click_mouse,
        description="Mouse click",
        parameters=[]
    ))

    registry.register(Tool(
        name="scroll",
        category=ToolCategory.MOUSE,
        function=scroll,
        description="Scroll",
        parameters=[]
    ))

    registry.register(Tool(
        name="screenshot",
        category=ToolCategory.SYSTEM,
        function=take_screenshot,
        description="Screenshot",
        parameters=[]
    ))

    registry.register(Tool(
        name="wait",
        category=ToolCategory.SYSTEM,
        function=wait,
        description="Wait",
        parameters=[]
    ))

    logger.info("🔥 ALL TOOLS REGISTERED")

    return registry

if __name__ == "__main__":

    register_all_tools()

    print("🔥 TOOL IMPLEMENTATIONS READY")