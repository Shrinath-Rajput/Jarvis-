import ollama
import json


TOOLS = """
Available tools:

1. open_app(app_name)
2. search_google(query)
3. search_youtube(query)
4. create_folder(name)
5. write_text(text)
6. take_screenshot()

Return ONLY JSON list.

Example:

[
  {
    "tool": "open_app",
    "app": "chrome"
  }
]
"""


def create_plan(command):

    prompt = f"""
You are an AI planner.

User command:
{command}

{TOOLS}

Generate action plan.
Only return JSON.
"""

    response = ollama.chat(
        model='tinyllama',
        messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ]
    )

    text = response['message']['content']

    try:

        start = text.find("[")

        end = text.rfind("]") + 1

        json_text = text[start:end]

        actions = json.loads(
            json_text
        )

        return actions

    except:

        return []