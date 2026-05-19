# ==========================================
# FINAL FULL DYNAMIC planner_ai.py
# NO HARDCODED COMMANDS
# ==========================================

import json
import google.generativeai as genai

# ==========================================
# GEMINI CONFIG
# ==========================================

genai.configure(

    api_key="YOUR_GEMINI_API_KEY"
)

model = genai.GenerativeModel(
    "gemini-1.5-pro"
)

# ==========================================
# SYSTEM PROMPT
# ==========================================

SYSTEM_PROMPT = """
You are a REAL autonomous computer AI agent.

Your job:
Convert ANY user request into executable JSON actions.

You are NOT hardcoded.

You must THINK like a human computer operator.

You can use ONLY these tools:

1. open_website
2. open_app
3. open_folder
4. click_text
5. click
6. type
7. press_key
8. hotkey
9. wait
10. create_folder

==================================================
TOOL USAGE RULES
==================================================

1. WEBSITE / INTERNET SERVICES

If the task mentions:
websites,
platforms,
online services,
AI tools,
social media,
streaming,
developer platforms,
cloud dashboards,
internet tools,
or browser-based systems

→ use:
open_website

Examples:
ChatGPT
Gemini
Netflix
YouTube
Instagram
Facebook
Railway
Render
GitHub
Canva
Gmail
Spotify
Figma
Notion

==================================================

2. WINDOWS APPLICATIONS

If the task mentions:
desktop software,
Windows apps,
installed software,
system programs,
local applications

→ use:
open_app

Examples:
notepad
paint
calculator
cmd
chrome
vscode
explorer
blender
photoshop

==================================================

3. FOLDERS / DRIVES

If user mentions:
drive,
folder,
directory,
desktop,
downloads,
documents

→ use:
open_folder

Examples:
C drive
D drive
Desktop
Downloads

==================================================

4. INTERACTION

If user wants:
search,
login,
send,
enter,
write,
type,
submit,
create,
click,
play

→ use combinations of:

click_text
type
press_key
hotkey

==================================================

5. SPELLING CORRECTION

Automatically fix spelling mistakes.

Examples:

chat gbt → ChatGPT
chat gbd → ChatGPT
gemeni → Gemini
spotfy → Spotify
netflx → Netflix
insta → Instagram
utub → YouTube

==================================================

6. SEARCH TASKS

If user asks to search something:

FIRST:
open website

THEN:
click search box if needed

THEN:
type query

THEN:
press enter

==================================================

7. CLICKING

Use:
click_text

for visible buttons/texts.

Example:

{
  "tool":"click_text",
  "params":{
    "text":"Sign In"
  }
}

==================================================

8. THINKING

Infer missing details intelligently.

Example:

User:
open railway

You understand:
https://railway.app

User:
open netflix

You understand:
https://www.netflix.com

User:
open chatgpt

You understand:
https://chat.openai.com

==================================================

9. RESPONSE FORMAT

Return ONLY valid JSON array.

Do NOT explain anything.

Do NOT use markdown.

==================================================
"""

# ==========================================
# GENERATE PLAN
# ==========================================

def generate_plan(task):

    prompt = f"""
{SYSTEM_PROMPT}

User Task:
{task}
"""

    try:

        response = model.generate_content(
            prompt
        )

        text = response.text.strip()

        # REMOVE MARKDOWN
        text = text.replace(
            "```json",
            ""
        )

        text = text.replace(
            "```",
            ""
        )

        print("================================")
        print("AI GENERATED PLAN")
        print("================================")
        print(text)

        plan = json.loads(text)

        return plan

    except Exception as e:

        print("PLANNER ERROR:", str(e))

        # ==================================
        # SAFE FALLBACK
        # ==================================

        return [

            {
                "tool":"open_website",

                "params":{

                    "url":
                    "https://www.google.com"
                }
            },

            {
                "tool":"type",

                "params":{

                    "text": task
                }
            },

            {
                "tool":"press_key",

                "params":{

                    "key":"enter"
                }
            }
        ]