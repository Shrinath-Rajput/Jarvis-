"""
FINAL WORKING autonomous_agent_enhanced.py
FULL STABLE VERSION
YOUTUBE + GOOGLE + GEMINI + CHATGPT + VS CODE
SEARCH + CLICK + TYPE + PLAY VIDEO
"""

import asyncio
import logging
import uuid
from datetime import datetime

from tool_implementations import register_all_tools

# =========================================================
# LOGGING
# =========================================================

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

# =========================================================
# AGENT
# =========================================================

class EnhancedAutonomousAgent:

    def __init__(self):

        logger.info(
            "🤖 Initializing Enhanced Agent..."
        )

        self.tool_registry = register_all_tools()

        logger.info(
            "✅ Enhanced Agent Ready"
        )

    # =====================================================
    # MAIN EXECUTION
    # =====================================================

    async def execute_autonomous_task(

        self,
        user_intent: str,
        max_steps: int = 10

    ):

        task_id = (
            f"task_{uuid.uuid4().hex[:8]}"
        )

        start_time = datetime.now()

        try:

            result = await self._execute(
                user_intent.lower()
            )

            end_time = datetime.now()

            duration = (
                end_time - start_time
            ).total_seconds()

            return {

                "success": True,

                "status": "completed",

                "task_id": task_id,

                "user_intent": user_intent,

                "duration_seconds": duration,

                "result": result,

                "created_at":
                    start_time.isoformat(),

                "completed_at":
                    end_time.isoformat()
            }

        except Exception as e:

            logger.error(str(e))

            return {

                "success": False,

                "status": "failed",

                "task_id": task_id,

                "error": str(e)
            }

    # =====================================================
    # EXECUTION ENGINE
    # =====================================================

    async def _execute(
        self,
        text: str
    ):

        logger.info(
            f"🔥 EXECUTING: {text}"
        )

        # =================================================
        # YOUTUBE
        # =================================================

        if "youtube" in text:

            await self.tool_registry.execute_tool(
                "open_website",
                site_name="youtube"
            )

            await asyncio.sleep(5)

            # CLICK SEARCH BAR
            await self.tool_registry.execute_tool(
                "click",
                x=650,
                y=115
            )

            await asyncio.sleep(1)

            # SEARCH
            if "search" in text:

                query = text.split("search")[-1]

                query = (
                    query
                    .replace("play", "")
                    .replace("first video", "")
                    .replace("video", "")
                    .strip()
                )

                await self.tool_registry.execute_tool(
                    "type_text",
                    text=query
                )

                await asyncio.sleep(1)

                await self.tool_registry.execute_tool(
                    "press_key",
                    key_name="enter"
                )

                await asyncio.sleep(5)

            # PLAY VIDEO
            if (
                "play" in text
                or "first video" in text
            ):

                await self.tool_registry.execute_tool(
                    "click",
                    x=500,
                    y=350
                )

            return "YouTube automation completed"

        # =================================================
        # GOOGLE
        # =================================================

        if (
            "google" in text
            or "browser" in text
            or "chrome" in text
        ):

            await self.tool_registry.execute_tool(
                "open_website",
                site_name="google"
            )

            await asyncio.sleep(5)

            if "search" in text:

                query = text.split("search")[-1].strip()

                await self.tool_registry.execute_tool(
                    "click",
                    x=700,
                    y=350
                )

                await asyncio.sleep(1)

                await self.tool_registry.execute_tool(
                    "type_text",
                    text=query
                )

                await asyncio.sleep(1)

                await self.tool_registry.execute_tool(
                    "press_key",
                    key_name="enter"
                )

            return "Google automation completed"

        # =================================================
        # GEMINI
        # =================================================

        if "gemini" in text:

            await self.tool_registry.execute_tool(
                "open_website",
                site_name="gemini"
            )

            await asyncio.sleep(5)

            if "search" in text:

                query = text.split("search")[-1].strip()

                await self.tool_registry.execute_tool(
                    "type_text",
                    text=query
                )

                await asyncio.sleep(1)

                await self.tool_registry.execute_tool(
                    "press_key",
                    key_name="enter"
                )

            return "Gemini opened"

        # =================================================
        # CHATGPT
        # =================================================

        if (
            "chatgpt" in text
            or "chat gpt" in text
        ):

            await self.tool_registry.execute_tool(
                "open_website",
                site_name="chatgpt"
            )

            return "ChatGPT opened"

        # =================================================
        # VS CODE
        # =================================================

        if (
            "vs code" in text
            or "vscode" in text
            or "code" in text
        ):

            await self.tool_registry.execute_tool(
                "launch_app",
                app_name="code"
            )

            await asyncio.sleep(5)

            # CREATE FOLDER
            if "folder" in text:

                folder_name = "NewFolder"

                if "portfolio" in text:
                    folder_name = "portfolio"

                elif "dashboard" in text:
                    folder_name = "dashboard"

                elif "jarvis" in text:
                    folder_name = "jarvis"

                # CTRL SHIFT P
                await self.tool_registry.execute_tool(
                    "press_hotkey",
                    "ctrl",
                    "shift",
                    "p"
                )

                await asyncio.sleep(2)

                # OPEN FOLDER
                await self.tool_registry.execute_tool(
                    "type_text",
                    text="File: Open Folder"
                )

                await asyncio.sleep(1)

                await self.tool_registry.execute_tool(
                    "press_key",
                    key_name="enter"
                )

                await asyncio.sleep(3)

                # PATH
                await self.tool_registry.execute_tool(
                    "type_text",
                    text=f"D:\\{folder_name}"
                )

                await asyncio.sleep(1)

                await self.tool_registry.execute_tool(
                    "press_key",
                    key_name="enter"
                )

                await asyncio.sleep(3)

                # EXPLORER
                await self.tool_registry.execute_tool(
                    "press_hotkey",
                    "ctrl",
                    "shift",
                    "e"
                )

                await asyncio.sleep(2)

                # NEW FOLDER
                await self.tool_registry.execute_tool(
                    "press_hotkey",
                    "ctrl",
                    "shift",
                    "n"
                )

                await asyncio.sleep(1)

                await self.tool_registry.execute_tool(
                    "type_text",
                    text=folder_name
                )

                await asyncio.sleep(1)

                await self.tool_registry.execute_tool(
                    "press_key",
                    key_name="enter"
                )

                return f"{folder_name} folder created"

            return "VS Code opened"

        # =================================================
        # CREATE FOLDER
        # =================================================

        if "create folder" in text:

            folder_name = "NewFolder"

            if "portfolio" in text:
                folder_name = "portfolio"

            await self.tool_registry.execute_tool(
                "create_folder",
                folder_path=folder_name
            )

            return f"Folder created: {folder_name}"

        # =================================================
        # DEFAULT
        # =================================================

        return "No matching automation found"


# =========================================================
# GLOBAL AGENT
# =========================================================

_agent = None

def get_autonomous_agent():

    global _agent

    if _agent is None:

        _agent = EnhancedAutonomousAgent()

    return _agent