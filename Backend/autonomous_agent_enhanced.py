import asyncio
from tool_implementations import ToolImplementations


class EnhancedAutonomousAgent:

    def __init__(self, *args, **kwargs):

        self.tools = ToolImplementations()

        print("🤖 Enhanced Autonomous Agent Ready")

    # ======================================================
    # MAIN EXECUTION
    # ======================================================

    async def execute_task(self, task):

        text = task.lower()

        print(f"🔥 TASK RECEIVED: {text}")

        try:

            # ==================================================
            # YOUTUBE
            # ==================================================

            if "youtube" in text:

                query = ""

                if "search" in text:

                    query = text.split("search")[-1]

                    query = (
                        query
                        .replace("play", "")
                        .replace("first video", "")
                        .replace("video", "")
                        .replace("this", "")
                        .strip()
                    )

                result = await self.tools.open_youtube_search(
                    query
                )

                return {

                    "success": True,

                    "response":
                        result.get(
                            "result",
                            "YouTube completed"
                        )
                }

            # ==================================================
            # GOOGLE / BROWSER
            # ==================================================

            elif (
                "google" in text
                or "browser" in text
                or "chrome" in text
            ):

                query = ""

                if "search" in text:

                    query = text.split("search")[-1]

                    query = (
                        query
                        .replace("click the first link", "")
                        .strip()
                    )

                result = await self.tools.open_google_search(
                    query
                )

                # CLICK FIRST LINK
                if "first link" in text:

                    import pyautogui
                    import time

                    time.sleep(5)

                    pyautogui.click(
                        x=500,
                        y=320
                    )

                return {

                    "success": True,

                    "response":
                        result.get(
                            "result",
                            "Google completed"
                        )
                }

            # ==================================================
            # GEMINI
            # ==================================================

            elif "gemini" in text:

                query = ""

                if "search" in text:

                    query = text.split("search")[-1].strip()

                result = await self.tools.open_gemini_search(
                    query
                )

                return {

                    "success": True,

                    "response":
                        result.get(
                            "result",
                            "Gemini completed"
                        )
                }

            # ==================================================
            # VS CODE
            # ==================================================

            elif (
                "vs code" in text
                or "vscode" in text
                or "code" in text
            ):

                folder_name = "portfolio"

                if "dashboard" in text:
                    folder_name = "dashboard"

                elif "jarvis" in text:
                    folder_name = "jarvis"

                elif "project" in text:
                    folder_name = "project"

                result = await self.tools.open_vscode_create_folder(
                    folder_name
                )

                return {

                    "success": True,

                    "response":
                        result.get(
                            "result",
                            "VS Code completed"
                        )
                }

            # ==================================================
            # OPEN BROWSER
            # ==================================================

            elif "open browser" in text:

                result = await self.tools.open_browser()

                return {

                    "success": True,

                    "response":
                        result.get(
                            "result",
                            "Browser opened"
                        )
                }

            # ==================================================
            # DEFAULT
            # ==================================================

            else:

                return {

                    "success": False,

                    "response":
                        "Command not understood"
                }

        except Exception as e:

            print(f"❌ ERROR: {e}")

            return {

                "success": False,

                "response": str(e)
            }


# ==========================================================
# GLOBAL INSTANCE
# ==========================================================

agent = EnhancedAutonomousAgent()


# ==========================================================
# MAIN FUNCTION
# ==========================================================

async def execute_autonomous_task(task):

    return await agent.execute_task(task)