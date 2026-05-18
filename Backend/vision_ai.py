import mss
import cv2
import numpy as np
import easyocr
import os
import pyautogui
import time


# =========================
# OCR READER
# =========================

reader = easyocr.Reader(
    ['en']
)


# =========================
# CAPTURE SCREEN
# =========================

def capture_screen():

    with mss.mss() as sct:

        monitor = sct.monitors[1]

        screenshot = sct.grab(
            monitor
        )

        img = np.array(
            screenshot
        )

        return img


# =========================
# SAVE SCREENSHOT
# =========================

def save_screenshot():

    img = capture_screen()

    path = os.path.join(
        os.path.expanduser("~"),
        "Desktop",
        "jarvis_screen.png"
    )

    cv2.imwrite(
        path,
        img
    )

    return path


# =========================
# READ SCREEN TEXT
# =========================

def read_screen_text():

    img = capture_screen()

    results = reader.readtext(
        img
    )

    texts = []

    for result in results:

        text = result[1]

        texts.append(text)

    return texts


# =========================
# FIND TEXT POSITION
# =========================

def find_text(target_text):

    img = capture_screen()

    results = reader.readtext(
        img
    )

    clean_target = (
        target_text
        .lower()
        .strip()
    )

    for result in results:

        bbox = result[0]

        text = result[1]

        print(
            "FOUND:",
            text
        )

        clean_text = (
            text
            .lower()
            .strip()
        )

        if clean_target in clean_text:

            x = int(
                (
                    bbox[0][0]
                    +
                    bbox[2][0]
                ) / 2
            )

            y = int(
                (
                    bbox[0][1]
                    +
                    bbox[2][1]
                ) / 2
            )

            return (
                x,
                y,
                text
            )

    return None


# =========================
# CLICK TEXT
# =========================

def click_text(target_text):

    found = find_text(
        target_text
    )

    if found:

        x, y, text = found

        pyautogui.moveTo(
            x,
            y,
            duration=1
        )

        time.sleep(0.5)

        pyautogui.click()

        return (
            f"Clicked on {text}"
        )

    return (
        f"{target_text} not found"
    )


# =========================
# DOUBLE CLICK TEXT
# =========================

def double_click_text(target_text):

    found = find_text(
        target_text
    )

    if found:

        x, y, text = found

        pyautogui.moveTo(
            x,
            y,
            duration=1
        )

        time.sleep(0.5)

        pyautogui.doubleClick()

        return (
            f"Double clicked on {text}"
        )

    return (
        f"{target_text} not found"
    )


# =========================
# RIGHT CLICK TEXT
# =========================

def right_click_text(target_text):

    found = find_text(
        target_text
    )

    if found:

        x, y, text = found

        pyautogui.moveTo(
            x,
            y,
            duration=1
        )

        time.sleep(0.5)

        pyautogui.rightClick()

        return (
            f"Right clicked on {text}"
        )

    return (
        f"{target_text} not found"
    )


# =========================
# TYPE TEXT
# =========================

def type_text(text):

    pyautogui.write(
        text,
        interval=0.03
    )

    return (
        f"Typed: {text}"
    )


# =========================
# PRESS KEY
# =========================

def press_key(key):

    pyautogui.press(
        key
    )

    return (
        f"Pressed {key}"
    )


# =========================
# HOTKEY
# =========================

def hotkey(*keys):

    pyautogui.hotkey(
        *keys
    )

    return (
        f"Hotkey {' + '.join(keys)}"
    )


# =========================
# MOVE MOUSE
# =========================

def move_mouse(x, y):

    pyautogui.moveTo(
        x,
        y,
        duration=1
    )

    return (
        f"Mouse moved to {x}, {y}"
    )


# =========================
# SCROLL
# =========================

def scroll_up():

    pyautogui.scroll(
        1000
    )

    return (
        "Scrolled up"
    )


def scroll_down():

    pyautogui.scroll(
        -1000
    )

    return (
        "Scrolled down"
    )


# =========================
# SCREEN SIZE
# =========================

def screen_size():

    width, height = (
        pyautogui.size()
    )

    return (
        width,
        height
    )