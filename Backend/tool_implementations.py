"""
Dynamic Tool Implementations
Replaces hardcoded tool logic with flexible, discoverable implementations
Organized by category and designed for LLM-driven selection
"""
import os
import logging
import webbrowser
import pyautogui
import time
import json
from pathlib import Path
from typing import Dict, List, Any
import subprocess

from tool_registry import (
    Tool, ToolRegistry, ToolCategory, ToolParameter, get_tool_registry
)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# =========================
# APPLICATION TOOLS
# =========================

async def launch_application(app_name: str, arguments: str = "") -> Dict[str, Any]:
    """
    Launch an application
    
    Args:
        app_name: Name of application (chrome, vscode, notepad, etc.)
        arguments: Optional command line arguments
    
    Returns:
        Result dict with success status
    """
    app_commands = {
        "chrome": "start chrome {args}",
        "edge": "start msedge {args}",
        "firefox": "start firefox {args}",
        "vscode": "code {args}",
        "notepad": "notepad {args}",
        "calculator": "calc {args}",
        "explorer": "explorer {args}",
        "powershell": "powershell {args}",
        "cmd": "cmd {args}",
        "word": "start winword {args}",
        "excel": "start excel {args}",
        "powerpoint": "start powerpnt {args}",
    }
    
    app_lower = app_name.lower()
    
    if app_lower not in app_commands:
        return {
            "success": False,
            "error": f"Unknown application: {app_name}. Available: {', '.join(app_commands.keys())}"
        }
    
    try:
        command = app_commands[app_lower].format(args=arguments)
        os.system(command)
        logger.info(f"✅ Launched {app_name}")
        time.sleep(1)  # Give app time to start
        
        return {
            "success": True,
            "message": f"Launched {app_name}",
            "app": app_name
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to launch {app_name}: {str(e)}"
        }


async def close_application(app_name: str) -> Dict[str, Any]:
    """Close an application"""
    try:
        os.system(f"taskkill /IM {app_name}.exe /F")
        logger.info(f"✅ Closed {app_name}")
        return {
            "success": True,
            "message": f"Closed {app_name}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# =========================
# BROWSER TOOLS
# =========================

async def open_website(site_name: str, url: str = "") -> Dict[str, Any]:
    """
    Open a website
    
    Args:
        site_name: Common name (google, youtube, etc.) or custom
        url: Optional full URL
    
    Returns:
        Result dict with success status
    """
    website_map = {
        "google": "https://google.com",
        "youtube": "https://youtube.com",
        "chatgpt": "https://chat.openai.com",
        "claude": "https://claude.ai",
        "gemini": "https://gemini.google.com",
        "github": "https://github.com",
        "stackoverflow": "https://stackoverflow.com",
        "linkedin": "https://linkedin.com",
        "twitter": "https://twitter.com",
        "reddit": "https://reddit.com",
        "facebook": "https://facebook.com",
        "instagram": "https://instagram.com",
        "gmail": "https://mail.google.com",
        "outlook": "https://outlook.com",
        "notion": "https://notion.so",
        "figma": "https://figma.com",
    }
    
    # Use provided URL or lookup in map
    target_url = url if url else website_map.get(site_name.lower())
    
    if not target_url:
        return {
            "success": False,
            "error": f"Unknown website: {site_name}"
        }
    
    try:
        webbrowser.open(target_url)
        logger.info(f"✅ Opened {target_url}")
        time.sleep(1)
        
        return {
            "success": True,
            "message": f"Opened {target_url}",
            "url": target_url
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


async def navigate_to_url(url: str) -> Dict[str, Any]:
    """
    Navigate to a specific URL
    
    Args:
        url: Full URL to navigate to
    
    Returns:
        Result dict
    """
    if not url.startswith("http"):
        url = f"https://{url}"
    
    try:
        webbrowser.open(url)
        logger.info(f"✅ Navigated to {url}")
        time.sleep(1)
        
        return {
            "success": True,
            "message": f"Navigated to {url}",
            "url": url
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


async def search_google(query: str) -> Dict[str, Any]:
    """
    Perform a Google search
    
    Args:
        query: Search query
    
    Returns:
        Result dict with search URL
    """
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    
    try:
        webbrowser.open(search_url)
        logger.info(f"✅ Searched Google for '{query}'")
        time.sleep(1)
        
        return {
            "success": True,
            "message": f"Searched for '{query}'",
            "query": query,
            "url": search_url
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


async def search_youtube(query: str) -> Dict[str, Any]:
    """
    Search YouTube
    
    Args:
        query: Search query
    
    Returns:
        Result dict
    """
    search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    
    try:
        webbrowser.open(search_url)
        logger.info(f"✅ Searched YouTube for '{query}'")
        time.sleep(1)
        
        return {
            "success": True,
            "message": f"Searched YouTube for '{query}'",
            "query": query,
            "url": search_url
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# =========================
# FILE SYSTEM TOOLS
# =========================

async def create_folder(folder_path: str) -> Dict[str, Any]:
    """
    Create a folder
    
    Args:
        folder_path: Path to create
    
    Returns:
        Result dict
    """
    try:
        Path(folder_path).mkdir(parents=True, exist_ok=True)
        logger.info(f"✅ Created folder: {folder_path}")
        
        return {
            "success": True,
            "message": f"Created folder: {folder_path}",
            "path": folder_path
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


async def create_file(file_path: str, content: str = "") -> Dict[str, Any]:
    """
    Create a file with optional content
    
    Args:
        file_path: Path to file
        content: Optional file content
    
    Returns:
        Result dict
    """
    try:
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w') as f:
            f.write(content)
        
        logger.info(f"✅ Created file: {file_path}")
        
        return {
            "success": True,
            "message": f"Created file: {file_path}",
            "path": file_path,
            "size": len(content)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


async def delete_file(file_path: str) -> Dict[str, Any]:
    """Delete a file"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"✅ Deleted file: {file_path}")
            return {
                "success": True,
                "message": f"Deleted file: {file_path}"
            }
        else:
            return {
                "success": False,
                "error": f"File not found: {file_path}"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


async def write_to_file(file_path: str, content: str, append: bool = False) -> Dict[str, Any]:
    """
    Write content to a file
    
    Args:
        file_path: Path to file
        content: Content to write
        append: Whether to append (True) or overwrite (False)
    
    Returns:
        Result dict
    """
    try:
        mode = 'a' if append else 'w'
        
        with open(file_path, mode) as f:
            f.write(content)
        
        action = "appended to" if append else "wrote to"
        logger.info(f"✅ {action} file: {file_path}")
        
        return {
            "success": True,
            "message": f"Successfully {action} {file_path}",
            "path": file_path,
            "content_length": len(content)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# =========================
# KEYBOARD TOOLS
# =========================

async def type_text(text: str, delay: float = 0.05) -> Dict[str, Any]:
    """
    Type text character by character
    
    Args:
        text: Text to type
        delay: Delay between characters in seconds
    
    Returns:
        Result dict
    """
    try:
        pyautogui.write(text, interval=delay)
        logger.info(f"✅ Typed: {text[:50]}...")
        
        return {
            "success": True,
            "message": f"Typed {len(text)} characters",
            "text_length": len(text)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


async def press_key(key_name: str, times: int = 1) -> Dict[str, Any]:
    """
    Press a keyboard key
    
    Args:
        key_name: Key name (enter, esc, tab, etc.)
        times: Number of times to press
    
    Returns:
        Result dict
    """
    try:
        for _ in range(times):
            pyautogui.press(key_name)
        
        logger.info(f"✅ Pressed {key_name} {times} time(s)")
        
        return {
            "success": True,
            "message": f"Pressed {key_name} {times} time(s)"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


async def press_hotkey(*keys) -> Dict[str, Any]:
    """
    Press a hotkey combination
    
    Args:
        *keys: Keys to press together (e.g., 'ctrl', 'c')
    
    Returns:
        Result dict
    """
    try:
        pyautogui.hotkey(*keys)
        logger.info(f"✅ Pressed hotkey: {' + '.join(keys)}")
        
        return {
            "success": True,
            "message": f"Pressed {' + '.join(keys)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# =========================
# MOUSE TOOLS
# =========================

async def move_mouse(x: int, y: int, duration: float = 0.5) -> Dict[str, Any]:
    """
    Move mouse to coordinates
    
    Args:
        x: X coordinate
        y: Y coordinate
        duration: Duration of movement in seconds
    
    Returns:
        Result dict
    """
    try:
        pyautogui.moveTo(x, y, duration=duration)
        logger.info(f"✅ Moved mouse to ({x}, {y})")
        
        return {
            "success": True,
            "message": f"Moved mouse to ({x}, {y})",
            "x": x,
            "y": y
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


async def click_mouse(x: int, y: int, button: str = "left", clicks: int = 1) -> Dict[str, Any]:
    """
    Click at coordinates
    
    Args:
        x: X coordinate
        y: Y coordinate
        button: Mouse button (left, right, middle)
        clicks: Number of clicks
    
    Returns:
        Result dict
    """
    try:
        pyautogui.click(x, y, clicks=clicks, button=button)
        logger.info(f"✅ Clicked at ({x}, {y}) with {button} button {clicks} times")
        
        return {
            "success": True,
            "message": f"Clicked at ({x}, {y})",
            "x": x,
            "y": y,
            "button": button,
            "clicks": clicks
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


async def scroll(direction: str = "down", amount: int = 3) -> Dict[str, Any]:
    """
    Scroll in a direction
    
    Args:
        direction: Direction to scroll (up, down)
        amount: Number of scroll increments
    
    Returns:
        Result dict
    """
    try:
        scroll_amount = amount if direction.lower() == "down" else -amount
        pyautogui.scroll(scroll_amount)
        logger.info(f"✅ Scrolled {direction} by {amount} increments")
        
        return {
            "success": True,
            "message": f"Scrolled {direction}",
            "direction": direction,
            "amount": amount
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


async def drag_mouse(x1: int, y1: int, x2: int, y2: int, duration: float = 0.5) -> Dict[str, Any]:
    """
    Drag mouse from one point to another
    
    Args:
        x1, y1: Starting coordinates
        x2, y2: Ending coordinates
        duration: Duration of drag in seconds
    
    Returns:
        Result dict
    """
    try:
        pyautogui.drag(x2 - x1, y2 - y1, duration=duration)
        logger.info(f"✅ Dragged from ({x1}, {y1}) to ({x2}, {y2})")
        
        return {
            "success": True,
            "message": f"Dragged to ({x2}, {y2})",
            "from": (x1, y1),
            "to": (x2, y2)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# =========================
# SYSTEM TOOLS
# =========================

async def take_screenshot() -> Dict[str, Any]:
    """
    Take a screenshot
    
    Returns:
        Result dict with screenshot path
    """
    try:
        from screen_understanding import ScreenCapture
        cap = ScreenCapture()
        path = cap.save_screenshot()
        
        return {
            "success": True,
            "message": "Screenshot taken",
            "path": path
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


async def wait(seconds: float) -> Dict[str, Any]:
    """
    Wait for a specified duration
    
    Args:
        seconds: Seconds to wait
    
    Returns:
        Result dict
    """
    try:
        time.sleep(seconds)
        logger.info(f"✅ Waited {seconds} seconds")
        
        return {
            "success": True,
            "message": f"Waited {seconds} seconds"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# =========================
# REGISTRY INITIALIZATION
# =========================

def register_all_tools() -> ToolRegistry:
    """
    Register all available tools with the registry
    Called at application startup
    """
    registry = get_tool_registry()
    
    # APPLICATION TOOLS
    registry.register(Tool(
        name="launch_app",
        category=ToolCategory.APPLICATION,
        function=launch_application,
        description="Launch an application (Chrome, VS Code, Notepad, etc.)",
        parameters=[
            ToolParameter("app_name", "string", required=True, description="Application name"),
            ToolParameter("arguments", "string", required=False, description="Optional arguments")
        ]
    ))
    
    registry.register(Tool(
        name="close_app",
        category=ToolCategory.APPLICATION,
        function=close_application,
        description="Close a running application",
        parameters=[ToolParameter("app_name", "string", required=True, description="Application name")]
    ))
    
    # BROWSER TOOLS
    registry.register(Tool(
        name="open_website",
        category=ToolCategory.BROWSER,
        function=open_website,
        description="Open a website by name or URL",
        parameters=[
            ToolParameter("site_name", "string", required=True, description="Site name or identifier"),
            ToolParameter("url", "string", required=False, description="Full URL (optional)")
        ]
    ))
    
    registry.register(Tool(
        name="navigate_url",
        category=ToolCategory.BROWSER,
        function=navigate_to_url,
        description="Navigate to a specific URL",
        parameters=[ToolParameter("url", "string", required=True, description="URL to navigate to")]
    ))
    
    registry.register(Tool(
        name="search_google",
        category=ToolCategory.BROWSER,
        function=search_google,
        description="Search Google for a query",
        parameters=[ToolParameter("query", "string", required=True, description="Search query")]
    ))
    
    registry.register(Tool(
        name="search_youtube",
        category=ToolCategory.BROWSER,
        function=search_youtube,
        description="Search YouTube for videos",
        parameters=[ToolParameter("query", "string", required=True, description="Search query")]
    ))
    
    # FILE SYSTEM TOOLS
    registry.register(Tool(
        name="create_folder",
        category=ToolCategory.FILE_SYSTEM,
        function=create_folder,
        description="Create a folder",
        parameters=[ToolParameter("folder_path", "string", required=True, description="Path to create")]
    ))
    
    registry.register(Tool(
        name="create_file",
        category=ToolCategory.FILE_SYSTEM,
        function=create_file,
        description="Create a file with optional content",
        parameters=[
            ToolParameter("file_path", "string", required=True, description="Path to create"),
            ToolParameter("content", "string", required=False, description="File content")
        ]
    ))
    
    registry.register(Tool(
        name="delete_file",
        category=ToolCategory.FILE_SYSTEM,
        function=delete_file,
        description="Delete a file",
        parameters=[ToolParameter("file_path", "string", required=True, description="Path to delete")]
    ))
    
    registry.register(Tool(
        name="write_file",
        category=ToolCategory.FILE_SYSTEM,
        function=write_to_file,
        description="Write content to a file",
        parameters=[
            ToolParameter("file_path", "string", required=True, description="Path to write to"),
            ToolParameter("content", "string", required=True, description="Content to write"),
            ToolParameter("append", "boolean", required=False, description="Append mode")
        ]
    ))
    
    # KEYBOARD TOOLS
    registry.register(Tool(
        name="type_text",
        category=ToolCategory.KEYBOARD,
        function=type_text,
        description="Type text into focused input",
        parameters=[
            ToolParameter("text", "string", required=True, description="Text to type"),
            ToolParameter("delay", "float", required=False, description="Delay between chars")
        ]
    ))
    
    registry.register(Tool(
        name="press_key",
        category=ToolCategory.KEYBOARD,
        function=press_key,
        description="Press a keyboard key",
        parameters=[
            ToolParameter("key_name", "string", required=True, description="Key name"),
            ToolParameter("times", "int", required=False, description="Number of times")
        ]
    ))
    
    registry.register(Tool(
        name="press_hotkey",
        category=ToolCategory.KEYBOARD,
        function=press_hotkey,
        description="Press keyboard hotkey combination",
        parameters=[ToolParameter("keys", "string[]", required=True, description="Keys to combine")]
    ))
    
    # MOUSE TOOLS
    registry.register(Tool(
        name="move_mouse",
        category=ToolCategory.MOUSE,
        function=move_mouse,
        description="Move mouse to coordinates",
        parameters=[
            ToolParameter("x", "int", required=True, description="X coordinate"),
            ToolParameter("y", "int", required=True, description="Y coordinate"),
            ToolParameter("duration", "float", required=False, description="Duration in seconds")
        ]
    ))
    
    registry.register(Tool(
        name="click",
        category=ToolCategory.MOUSE,
        function=click_mouse,
        description="Click at coordinates",
        parameters=[
            ToolParameter("x", "int", required=True, description="X coordinate"),
            ToolParameter("y", "int", required=True, description="Y coordinate"),
            ToolParameter("button", "string", required=False, description="Mouse button"),
            ToolParameter("clicks", "int", required=False, description="Number of clicks")
        ]
    ))
    
    registry.register(Tool(
        name="scroll",
        category=ToolCategory.MOUSE,
        function=scroll,
        description="Scroll the screen",
        parameters=[
            ToolParameter("direction", "string", required=False, description="Direction (up/down)"),
            ToolParameter("amount", "int", required=False, description="Scroll amount")
        ]
    ))
    
    registry.register(Tool(
        name="drag",
        category=ToolCategory.MOUSE,
        function=drag_mouse,
        description="Drag mouse from one point to another",
        parameters=[
            ToolParameter("x1", "int", required=True, description="Start X"),
            ToolParameter("y1", "int", required=True, description="Start Y"),
            ToolParameter("x2", "int", required=True, description="End X"),
            ToolParameter("y2", "int", required=True, description="End Y"),
            ToolParameter("duration", "float", required=False, description="Duration")
        ]
    ))
    
    # SYSTEM TOOLS
    registry.register(Tool(
        name="screenshot",
        category=ToolCategory.SYSTEM,
        function=take_screenshot,
        description="Take a screenshot",
        parameters=[]
    ))
    
    registry.register(Tool(
        name="wait",
        category=ToolCategory.SYSTEM,
        function=wait,
        description="Wait for a duration",
        parameters=[ToolParameter("seconds", "float", required=True, description="Seconds to wait")]
    ))
    
    logger.info(f"✅ Registered {len(registry.get_all_tools())} tools")
    return registry


if __name__ == "__main__":
    # Initialize and display available tools
    registry = register_all_tools()
    print("\n" + "="*60)
    print("AVAILABLE TOOLS")
    print("="*60)
    print(registry.get_tools_for_llm())
