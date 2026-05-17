import os
import webbrowser
import pyautogui
import google.generativeai as genai

# GEMINI API KEY
genai.configure(
    api_key="AIzaSyBmuBZCsR4hMJy1w5FOJ6BSMkhZyT6mWM0"
)

model = genai.GenerativeModel(
    "gemini-1.5-flash"
)

def execute_command(command):

    print("USER:", command)

    command = command.lower()

    # DIRECT FAST COMMANDS

    if "shutdown" in command:

        os.system("shutdown /s /t 5")

        return "Shutting down"

    if "restart" in command:

        os.system("shutdown /r /t 5")

        return "Restarting"

    if "screenshot" in command:

        img = pyautogui.screenshot()

        img.save("screenshot.png")

        return "Screenshot taken"

    # AI BRAIN

    prompt = f"""

You are an advanced AI desktop assistant.

Understand user intent.

User command:
{command}

Return ONLY one action from below:

OPEN_CHROME
OPEN_YOUTUBE
OPEN_GOOGLE
OPEN_VSCODE
OPEN_CALCULATOR
OPEN_NOTEPAD
SEARCH_GOOGLE:query
SEARCH_YOUTUBE:query
VOLUME_UP
VOLUME_DOWN
MUTE
UNKNOWN

Examples:

open chrome
-> OPEN_CHROME

go to youtube and search arijit songs
-> SEARCH_YOUTUBE:arijit songs

search iron man trailer
-> SEARCH_GOOGLE:iron man trailer

open vscode
-> OPEN_VSCODE
"""

    response = model.generate_content(
        prompt
    )

    ai_response = (
        response.text.strip()
    )

    print("AI:", ai_response)

    # ACTION ENGINE

    if ai_response == "OPEN_CHROME":

        os.system("start chrome")

        return "Opening Chrome"

    elif ai_response == "OPEN_YOUTUBE":

        webbrowser.open(
            "https://youtube.com"
        )

        return "Opening YouTube"

    elif ai_response == "OPEN_GOOGLE":

        webbrowser.open(
            "https://google.com"
        )

        return "Opening Google"

    elif ai_response == "OPEN_VSCODE":

        os.system("code")

        return "Opening VS Code"

    elif ai_response == "OPEN_CALCULATOR":

        os.system("calc")

        return "Opening Calculator"

    elif ai_response == "OPEN_NOTEPAD":

        os.system("notepad")

        return "Opening Notepad"

    elif (
        "SEARCH_GOOGLE:"
        in ai_response
    ):

        query = ai_response.replace(
            "SEARCH_GOOGLE:",
            ""
        )

        webbrowser.open(
            f"https://www.google.com/search?q={query}"
        )

        return f"Searching {query}"

    elif (
        "SEARCH_YOUTUBE:"
        in ai_response
    ):

        query = ai_response.replace(
            "SEARCH_YOUTUBE:",
            ""
        )

        webbrowser.open(
            f"https://www.youtube.com/results?search_query={query}"
        )

        return f"Searching YouTube for {query}"

    elif ai_response == "VOLUME_UP":

        pyautogui.press(
            "volumeup"
        )

        return "Volume increased"

    elif ai_response == "VOLUME_DOWN":

        pyautogui.press(
            "volumedown"
        )

        return "Volume decreased"

    elif ai_response == "MUTE":

        pyautogui.press(
            "volumemute"
        )

        return "Muted"

    else:

        return (
            "I understood but cannot execute yet"
        )