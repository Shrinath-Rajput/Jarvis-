# ============================================
# FINAL FULL WORKING planner_ai.py
# ============================================

# -*- coding: utf-8 -*-

import json
import logging
import os

from typing import Dict, List, Optional

import google.generativeai as genai

# ============================================
# LOGGING
# ============================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# ============================================
# GEMINI CONFIG
# ============================================

API_KEY = os.getenv(
    "GEMINI_API_KEY",
    "YOUR_GEMINI_API_KEY"
)

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel(
    "gemini-1.5-pro"
)

# ============================================
# SYSTEM PROMPT
# ============================================

SYSTEM_PROMPT = """
You are a REAL autonomous computer AI agent.

Convert ANY user request into executable JSON actions.

AVAILABLE TOOLS:

1. open_website
2. open_app
3. open_folder
4. click_text
5. click
6. type
7. press_key
8. hotkey
9. scroll
10. wait
11. create_folder
12. screenshot

IMPORTANT:

- NO HARDCODED COMMANDS
- Understand ANY user request dynamically
- Auto-correct typos
- Multi-step planning supported
- RETURN ONLY JSON ARRAY
- NEVER markdown
- NEVER explanation

EXAMPLE:

[
  {
    "tool":"open_website",
    "params":{
      "url":"https://youtube.com"
    }
  },
  {
    "tool":"wait",
    "params":{
      "seconds":2
    }
  },
  {
    "tool":"type",
    "params":{
      "text":"Virat Kohli"
    }
  },
  {
    "tool":"press_key",
    "params":{
      "key":"Return"
    }
  }
]
"""

# ============================================
# DYNAMIC PLANNER
# ============================================

class DynamicPlanner:

    def __init__(self):

        self.model = model

        logger.info(
            "DynamicPlanner initialized"
        )

    # ========================================
    # SMART FALLBACK PLAN
    # ========================================

    def _fallback_plan(self, task: str):

        logger.warning(
            "Using smart fallback plan"
        )

        task_lower = task.lower()

        # ====================================
        # WEBSITE DETECTION
        # ====================================

        websites = {

            "youtube":
                "https://www.youtube.com",

            "google":
                "https://www.google.com",

            "chatgpt":
                "https://chat.openai.com",

            "gpt":
                "https://chat.openai.com",

            "gemini":
                "https://gemini.google.com",

            "netflix":
                "https://www.netflix.com",

            "instagram":
                "https://www.instagram.com",

            "facebook":
                "https://www.facebook.com",

            "linkedin":
                "https://www.linkedin.com",

            "github":
                "https://github.com",

            "railway":
                "https://railway.app",

            "render":
                "https://render.com",

            "gmail":
                "https://mail.google.com"
        }

        # ====================================
        # APP DETECTION
        # ====================================

        apps = [

            "vscode",
            "vs code",
            "notepad",
            "paint",
            "calculator",
            "cmd",
            "chrome",
            "explorer"
        ]

        # ====================================
        # OPEN APP
        # ====================================

        for app in apps:

            if app in task_lower:

                return [

                    {
                        "tool": "open_app",

                        "params": {

                            "name": app
                        },

                        "critical": True
                    }
                ]

        # ====================================
        # OPEN DRIVE
        # ====================================

        if "open d" in task_lower:

            return [

                {
                    "tool": "open_folder",

                    "params": {

                        "path": "D:\\"
                    },

                    "critical": True
                }
            ]

        if "open c" in task_lower:

            return [

                {
                    "tool": "open_folder",

                    "params": {

                        "path": "C:\\"
                    },

                    "critical": True
                }
            ]

        # ====================================
        # WEBSITE SELECT
        # ====================================

        selected_url = "https://www.google.com"

        for key, url in websites.items():

            if key in task_lower:

                selected_url = url

                break

        # ====================================
        # SEARCH CLEAN
        # ====================================

        search_query = task

        remove_words = [

            "open",
            "search",
            "youtube",
            "google",
            "gemini",
            "chatgpt",
            "gpt",
            "and",
            "click",
            "first",
            "video",
            "play",
            "this"
        ]

        for word in remove_words:

            search_query = search_query.replace(
                word,
                ""
            )

        search_query = search_query.strip()

        # ====================================
        # FINAL PLAN
        # ====================================

        plan = [

            {
                "tool": "open_website",

                "params": {

                    "url": selected_url
                },

                "critical": True
            },

            {
                "tool": "wait",

                "params": {

                    "seconds": 3
                },

                "critical": False
            }
        ]

        # ====================================
        # SEARCH
        # ====================================

        if len(search_query) > 1:

            plan.extend([

                {
                    "tool": "type",

                    "params": {

                        "text": search_query
                    },

                    "critical": True
                },

                {
                    "tool": "press_key",

                    "params": {

                        "key": "Return"
                    },

                    "critical": True
                }
            ])

        return plan

    # ========================================
    # PLAN TASK
    # ========================================

    def plan_task(

        self,

        user_input: str,

        context: Optional[List[str]] = None

    ) -> List[Dict]:

        try:

            logger.info(
                f"Planning task: {user_input}"
            )

            # ====================================
            # NO MODEL
            # ====================================

            if not self.model:

                logger.error(
                    "No Gemini model"
                )

                return self._fallback_plan(
                    user_input
                )

            # ====================================
            # PROMPT
            # ====================================

            prompt = f"""
{SYSTEM_PROMPT}

USER TASK:
{user_input}

RETURN ONLY JSON ARRAY:
"""

            # ====================================
            # GEMINI REQUEST
            # ====================================

            response = self.model.generate_content(

                prompt,

                generation_config={

                    "temperature": 0.3,

                    "max_output_tokens": 2000,

                    "top_p": 0.95,

                    "top_k": 40
                }
            )

            # ====================================
            # RESPONSE
            # ====================================

            try:

                response_text = response.text.strip()

            except Exception:

                logger.error(
                    "Empty Gemini response"
                )

                return self._fallback_plan(
                    user_input
                )

            print("\n🔥 RAW RESPONSE:\n")
            print(response_text)

            # ====================================
            # EXTRACT PLAN
            # ====================================

            plan = self._extract_json_plan(

                response_text,

                user_input
            )

            # ====================================
            # VALIDATE
            # ====================================

            if not isinstance(plan, list):

                return self._fallback_plan(
                    user_input
                )

            if len(plan) == 0:

                return self._fallback_plan(
                    user_input
                )

            print("\n✅ FINAL PLAN:\n")
            print(json.dumps(plan, indent=2))

            return plan

        except Exception as e:

            logger.error(
                f"Planner error: {e}"
            )

            return self._fallback_plan(
                user_input
            )

    # ========================================
    # EXTRACT JSON
    # ========================================

    def _extract_json_plan(

        self,

        response_text: str,

        user_input: str

    ) -> List[Dict]:

        try:

            cleaned = response_text.strip()

            # ====================================
            # REMOVE MARKDOWN
            # ====================================

            cleaned = cleaned.replace(
                "```json",
                ""
            )

            cleaned = cleaned.replace(
                "```",
                ""
            )

            cleaned = cleaned.strip()

            # ====================================
            # FIND JSON
            # ====================================

            start = cleaned.find("[")

            end = cleaned.rfind("]")

            if start == -1 or end == -1:

                logger.error(
                    "No JSON array found"
                )

                return self._fallback_plan(
                    user_input
                )

            json_text = cleaned[
                start:end + 1
            ]

            print("\n🔥 EXTRACTED JSON:\n")
            print(json_text)

            # ====================================
            # PARSE
            # ====================================

            plan = json.loads(json_text)

            if not isinstance(plan, list):

                return self._fallback_plan(
                    user_input
                )

            if len(plan) == 0:

                return self._fallback_plan(
                    user_input
                )

            return plan

        except Exception as e:

            logger.error(
                f"JSON parse failed: {e}"
            )

            return self._fallback_plan(
                user_input
            )

# ============================================
# EXPORT
# ============================================

__all__ = [
    "DynamicPlanner"
]