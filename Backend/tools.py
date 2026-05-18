import os
import webbrowser
import pyautogui
import time

from vision_ai import (
    click_text,
    press_key,
    type_text
)


# =========================
# OPEN APP
# =========================

def open_app(app):

    app = app.lower()

    if "chrome" in app:

        os.system(
            "start chrome"
        )

    elif "vscode" in app:

        os.system(
            "code"
        )

    elif "notepad" in app:

        os.system(
            "notepad"
        )

    elif "calculator" in app:

        os.system(
            "calc"
        )

    return f"{app} opened"


# =========================
# OPEN WEBSITE
# =========================

def open_website(site):

    sites = {

        "youtube":
        "https://youtube.com",

        "google":
        "https://google.com",

        "chatgpt":
        "https://chat.openai.com",

        "gemini":
        "https://gemini.google.com",

        "claude":
        "https://claude.ai",

        "github":
        "https://github.com",

        "linkedin":
        "https://linkedin.com",

        "spotify":
        "https://spotify.com"
    }

    if site in sites:

        webbrowser.open(
            sites[site]
        )

        return (
            f"{site} opened"
        )

    return (
        "Website not found"
    )


# =========================
# SEARCH GOOGLE
# =========================

def search_google(query):

    webbrowser.open(
        f"https://www.google.com/search?q={query}"
    )

    return (
        f"Searching {query}"
    )


# =========================
# SEARCH YOUTUBE
# =========================

def search_youtube(query):

    webbrowser.open(
        f"https://www.youtube.com/results?"
        f"search_query={query}"
    )

    return (
        f"Searching YouTube for {query}"
    )


# =========================
# CREATE FOLDER
# =========================

def create_folder(name):

    desktop = os.path.join(

        os.path.expanduser("~"),

        "Desktop"
    )

    folder_path = os.path.join(

        desktop,

        name.replace(
            " ",
            "_"
        )
    )

    os.makedirs(

        folder_path,

        exist_ok=True
    )

    return (
        f"Folder {name} created"
    )


# =========================
# WRITE TEXT
# =========================

def write_text(text):

    time.sleep(2)

    pyautogui.write(

        text,

        interval=0.03
    )

    return (
        "Text written"
    )


# =========================
# SCREENSHOT
# =========================

def take_screenshot():

    img = pyautogui.screenshot()

    img.save(
        "screenshot.png"
    )

    return (
        "Screenshot taken"
    )


# =========================
# CLICK TEXT
# =========================

def click_button(text):

    return click_text(
        text
    )


# =========================
# PRESS ENTER
# =========================

def enter():

    return press_key(
        "enter"
    )


# =========================
# PRESS TAB
# =========================

def tab():

    return press_key(
        "tab"
    )


# =========================
# PRESS ESC
# =========================

def esc():

    return press_key(
        "esc"
    )


# =========================
# HOTKEYS
# =========================

def copy():

    pyautogui.hotkey(
        "ctrl",
        "c"
    )

    return "Copied"


def paste():

    pyautogui.hotkey(
        "ctrl",
        "v"
    )

    return "Pasted"


def select_all():

    pyautogui.hotkey(
        "ctrl",
        "a"
    )

    return "Selected all"


# =========================
# SCROLL
# =========================

def scroll_down():

    pyautogui.scroll(
        -1000
    )

    return (
        "Scrolled down"
    )


def scroll_up():

    pyautogui.scroll(
        1000
    )

    return (
        "Scrolled up"
    )