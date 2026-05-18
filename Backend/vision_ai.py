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

reader = easyocr.Reader(['en'])


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
 