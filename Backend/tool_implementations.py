# -*- coding: utf-8 -*-
"""
GENERIC TOOL IMPLEMENTATIONS
=============================

NO hardcoding. Pure dynamic delegation to universal executor.

This module provides backwards-compatibility with existing code
while delegating all operations to the UniversalExecutor.
"""

import logging
from typing import Dict, Any, Optional, List
from executor_universal import get_executor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ToolImplementations:
    """
    Generic tool implementations.
    All operations delegated to UniversalExecutor (zero hardcoding).
    """
    
    def __init__(self):
        self.executor = get_executor()
        logger.info("✅ ToolImplementations initialized (generic)")
    
    async def execute_generic_task(self, task_description: str, plan: List[Dict]) -> Dict:
        """
        Execute any task dynamically
        
        Args:
            task_description: What the user wants
            plan: Action plan from planner
        
        Returns:
            Execution result
        """
        try:
            logger.info(f"Executing: {task_description}")
            
            results = self.executor.execute_plan(plan)
            
            success = all(r.get("success", False) for r in results)
            
            return {
                "success": success,
                "result": f"Task '{task_description}' completed",
                "details": results
            }
        
        except Exception as e:
            logger.error(f"Task execution failed: {e}")
            return {
                "success": False,
                "result": f"Task failed: {e}",
                "details": []
            }
    
    async def open_website(self, url: str) -> Dict:
        """Open any website dynamically"""
        try:
            result = self.executor.execute_action({
                "tool": "open_website",
                "params": {"url": url},
                "critical": True
            })
            
            return {
                "success": result.success,
                "result": result.output or "Website opened"
            }
        except Exception as e:
            return {"success": False, "result": str(e)}
    
    async def open_app(self, app_name: str) -> Dict:
        """Open any application dynamically"""
        try:
            result = self.executor.execute_action({
                "tool": "open_app",
                "params": {"name": app_name},
                "critical": True
            })
            
            return {
                "success": result.success,
                "result": result.output or f"App {app_name} opened"
            }
        except Exception as e:
            return {"success": False, "result": str(e)}
    
    async def create_folder(self, path: str, name: str = None) -> Dict:
        """Create folder with dynamic path handling"""
        try:
            if name:
                import os
                full_path = os.path.join(path, name)
            else:
                full_path = path
            
            result = self.executor.execute_action({
                "tool": "create_folder",
                "params": {"path": full_path},
                "critical": True
            })
            
            return {
                "success": result.success,
                "result": result.output or f"Folder created: {full_path}"
            }
        except Exception as e:
            return {"success": False, "result": str(e)}
    
    async def search_web(self, query: str, engine: str = "google") -> Dict:
        """Search on any website dynamically"""
        try:
            # Determine URL
            engines = {
                "google": "https://www.google.com/search?q=",
                "bing": "https://www.bing.com/search?q=",
                "duckduckgo": "https://duckduckgo.com/?q=",
                "youtube": "https://www.youtube.com/results?search_query="
            }
            
            base_url = engines.get(engine.lower(), engines["google"])
            search_url = base_url + query
            
            plan = [
                {"tool": "open_website", "params": {"url": search_url}, "critical": True},
                {"tool": "wait", "params": {"seconds": 3}, "critical": False},
                {"tool": "screenshot", "params": {}, "critical": False}
            ]
            
            results = self.executor.execute_plan(plan)
            
            return {
                "success": all(r.get("success") for r in results),
                "result": f"Searched '{query}' on {engine}",
                "details": results
            }
        except Exception as e:
            return {"success": False, "result": str(e)}
    
    async def type_text(self, text: str) -> Dict:
        """Type text dynamically"""
        try:
            result = self.executor.execute_action({
                "tool": "type",
                "params": {"text": text},
                "critical": True
            })
            
            return {
                "success": result.success,
                "result": result.output or f"Typed: {text}"
            }
        except Exception as e:
            return {"success": False, "result": str(e)}
    
    async def click_text_element(self, text: str) -> Dict:
        """Click element by text (OCR-based)"""
        try:
            # First take screenshot
            self.executor.execute_action({
                "tool": "screenshot",
                "params": {},
                "critical": False
            })
            
            result = self.executor.execute_action({
                "tool": "click_text",
                "params": {"text": text},
                "critical": True
            })
            
            return {
                "success": result.success,
                "result": result.output or f"Clicked: {text}"
            }
        except Exception as e:
            return {"success": False, "result": str(e)}
    
    async def press_key(self, key: str) -> Dict:
        """Press any key dynamically"""
        try:
            result = self.executor.execute_action({
                "tool": "press_key",
                "params": {"key": key},
                "critical": True
            })
            
            return {
                "success": result.success,
                "result": result.output or f"Pressed: {key}"
            }
        except Exception as e:
            return {"success": False, "result": str(e)}
    
    async def keyboard_hotkey(self, *keys) -> Dict:
        """Press keyboard combination"""
        try:
            result = self.executor.execute_action({
                "tool": "hotkey",
                "params": {"keys": list(keys)},
                "critical": True
            })
            
            return {
                "success": result.success,
                "result": result.output or f"Hotkey: {'+'.join(keys)}"
            }
        except Exception as e:
            return {"success": False, "result": str(e)}
    
    async def verify_task_success(self, expected_text: str, timeout: int = 5) -> Dict:
        """Verify task succeeded"""
        try:
            result = self.executor.execute_action({
                "tool": "verify_text",
                "params": {"text": expected_text, "timeout": timeout},
                "critical": False
            })
            
            return {
                "success": result.success,
                "result": result.output or f"Verification result: {result.success}"
            }
        except Exception as e:
            return {"success": False, "result": str(e)}
    
    async def take_screenshot(self) -> Dict:
        """Take screenshot for analysis"""
        try:
            result = self.executor.execute_action({
                "tool": "screenshot",
                "params": {},
                "critical": True
            })
            
            return {
                "success": result.success,
                "result": result.output or "Screenshot taken",
                "path": self.executor.last_screenshot
            }
        except Exception as e:
            return {"success": False, "result": str(e)}
    
    async def open_browser(self) -> Dict:
        """Open browser (dynamic)"""
        try:
            result = self.executor.execute_action({
                "tool": "open_website",
                "params": {"url": "https://www.google.com"},
                "critical": True
            })
            
            return {
                "success": result.success,
                "result": result.output or "Browser opened"
            }
        except Exception as e:
            return {"success": False, "result": str(e)}
    
    # Backwards compatibility - these now delegate dynamically
    async def open_google_search(self, query: str = "") -> Dict:
        """Backwards compat: search Google"""
        return await self.search_web(query, "google")
    
    async def open_youtube_search(self, query: str = "") -> Dict:
        """Backwards compat: search YouTube"""
        return await self.search_web(query, "youtube")
    
    async def open_gemini_search(self, query: str = "") -> Dict:
        """Backwards compat: search Gemini"""
        try:
            result = self.executor.execute_action({
                "tool": "open_website",
                "params": {"url": "https://gemini.google.com"},
                "critical": True
            })
            
            return {
                "success": result.success,
                "result": result.output or "Gemini opened"
            }
        except Exception as e:
            return {"success": False, "result": str(e)}
    
    async def open_vscode_create_folder(self, folder_name: str = "portfolio") -> Dict:
        """Backwards compat: create folder and open in VS Code"""
        try:
            import os
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            
            plan = [
                {"tool": "create_folder", "params": {"path": os.path.join(desktop, folder_name)}, "critical": True},
                {"tool": "wait", "params": {"seconds": 1}, "critical": False},
                {"tool": "open_app", "params": {"name": "code"}, "critical": True},
                {"tool": "wait", "params": {"seconds": 3}, "critical": False},
            ]
            
            results = self.executor.execute_plan(plan)
            
            return {
                "success": all(r.get("success") for r in results),
                "result": f"Folder {folder_name} created and VS Code opened",
                "details": results
            }
        except Exception as e:
            return {"success": False, "result": str(e)}


# Export
__all__ = ["ToolImplementations"]
