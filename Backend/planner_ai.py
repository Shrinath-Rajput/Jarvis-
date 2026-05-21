# planner_ai.py
# FINAL DYNAMIC VERSION
# NO HARDCODED COMMANDS

import json
import ollama
import logging

from config import (
    OLLAMA_MODEL,
    OLLAMA_BASE_URL
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)

# =========================================================
# TOOL REGISTRY
# =========================================================

TOOLS = [

    {
        "name": "open_chrome",
        "description": "Open Chrome browser",
        "params": []
    },

    {
        "name": "google_search",
        "description": "Search on Google",
        "params": ["query"]
    },

    {
        "name": "youtube_search",
        "description": "Search videos on YouTube",
        "params": ["query"]
    },

    {
        "name": "open_vscode",
        "description": "Open Visual Studio Code",
        "params": []
    },

    {
        "name": "open_word",
        "description": "Open Microsoft Word",
        "params": []
    },

    {
        "name": "open_excel",
        "description": "Open Microsoft Excel",
        "params": []
    },

    {
        "name": "open_terminal",
        "description": "Open CMD or PowerShell",
        "params": []
    },

    {
        "name": "create_folder",
        "description": "Create folder",
        "params": ["name"]
    },

    {
        "name": "play_spotify",
        "description": "Play Spotify song",
        "params": ["search_query"]
    },

    {
        "name": "take_screenshot",
        "description": "Take screenshot",
        "params": []
    },

    {
        "name": "open_gemini",
        "description": "Open Gemini AI",
        "params": []
    },

    {
        "name": "open_chatgpt",
        "description": "Open ChatGPT",
        "params": []
    },

    {
        "name": "type_text",
        "description": "Type text using keyboard",
        "params": ["text"]
    },

    {
        "name": "unknown_task",
        "description": "Unknown task fallback",
        "params": [
            "original_task",
            "error"
        ]
    }
]

# =========================================================
# SYSTEM PROMPT
# =========================================================

SYSTEM_PROMPT = f"""
You are JARVIS autonomous desktop AI.

Convert natural language into JSON plans.

AVAILABLE TOOLS:
{json.dumps(TOOLS, indent=2)}

RULES:
1. Return ONLY JSON array
2. NO markdown
3. NO explanation
4. NEVER invent tools
5. Use ONLY tool names from registry
6. Extract parameters dynamically
7. Multi-step tasks allowed
8. NEVER change user intent
9. NEVER hallucinate commands

FORMAT:

[
  {{
    "tool": "tool_name",
    "params": {{
      "key": "value"
    }}
  }}
]
"""

# =========================================================
# DYNAMIC PLANNER
# =========================================================

class DynamicPlanner:

    def __init__(self):

        logger.info(
            "Initializing Dynamic Planner"
        )

        self.client = ollama.Client(
            host=OLLAMA_BASE_URL
        )

    # =====================================================
    # VALIDATE PLAN
    # =====================================================

    def validate_plan(self, plan):

        valid_tools = {

            tool["name"]
            for tool in TOOLS
        }

        validated = []

        for step in plan:

            tool_name = (
                step.get("tool", "")
                .strip()
            )

            params = step.get(
                "params",
                {}
            )

            if tool_name not in valid_tools:

                logger.warning(
                    f"Invalid tool: {tool_name}"
                )

                continue

            validated.append({

                "tool": tool_name,

                "params": params
            })

        return validated

    # =====================================================
    # PLAN TASK
    # =====================================================

    def plan_task(self, task):

        try:

            logger.info(
                f"Planning task: {task}"
            )

            prompt = f"""
{SYSTEM_PROMPT}

USER REQUEST:
{task}
"""

            response = self.client.chat(

                model=OLLAMA_MODEL,

                messages=[

                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                stream=False
            )

            raw_text = (
                response.get("message", {})
                .get("content", "")
                .strip()
            )

            logger.info(
                f"RAW RESPONSE:\n{raw_text}"
            )

            # CLEAN RESPONSE
            cleaned = raw_text.replace(
                "```json",
                ""
            )

            cleaned = cleaned.replace(
                "```",
                ""
            )

            # EXTRACT JSON
            start = cleaned.find("[")

            end = cleaned.rfind("]")

            if start == -1 or end == -1:

                raise Exception(
                    "No JSON array found"
                )

            json_text = cleaned[start:end + 1]

            logger.info(
                f"JSON:\n{json_text}"
            )

            plan = json.loads(
                json_text
            )

            validated_plan = (
                self.validate_plan(plan)
            )

            if not validated_plan:

                raise Exception(
                    "No valid tools generated"
                )

            logger.info(
                f"VALID PLAN:\n{validated_plan}"
            )

            return validated_plan

        except Exception as e:

            logger.error(
                f"PLANNER ERROR: {e}"
            )

            return [

                {
                    "tool": "unknown_task",

                    "params": {

                        "original_task": task,

                        "error": str(e)
                    }
                }
            ]