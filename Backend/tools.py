import os
import webbrowser
import pyautogui
import time


# ------------------------
# OPEN APP
# ------------------------

def open_app(app):

    app = app.lower()

    if "chrome" in app:

        os.system("start chrome")

    elif "vscode" in app:

        os.system("code")

    elif "notepad" in app:

        os.system("notepad")

    elif "calculator" in app:

        os.system("calc")

    return f"{app} opened"


# ------------------------
# SEARCH WEB
# ------------------------

def search_google(query):

    webbrowser.open(
        f"https://www.google.com/search?q={query}"
    )

    return f"Searching {query}"


# ------------------------
# SEARCH YOUTUBE
# ------------------------

def search_youtube(query):

    webbrowser.open(
        f"https://www.youtube.com/results?search_query={query}"
    )

    return (
        f"Searching YouTube for {query}"
    )


# ------------------------
# CREATE FOLDER
# ------------------------

def create_folder(name):

    desktop = os.path.join(
        os.path.expanduser("~"),
        "Desktop"
    )

    folder_path = os.path.join(
        desktop,
        name.replace(" ", "_")
    )

    os.makedirs(
        folder_path,
        exist_ok=True
    )

    return (
        f"Folder {name} created"
    )


# ------------------------
# WRITE TEXT
# ------------------------

def write_text(text):

    time.sleep(2)

    pyautogui.write(
        text,
        interval=0.03
    )

    return "Text written"


# ------------------------
# SCREENSHOT
# ------------------------

def take_screenshot():

    img = pyautogui.screenshot()

    img.save("screenshot.png")

    return "Screenshot taken"