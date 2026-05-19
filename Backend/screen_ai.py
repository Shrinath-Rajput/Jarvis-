import pyautogui
import easyocr
import cv2
import numpy as np

reader = easyocr.Reader(['en'])


def capture_screen():

    screenshot = pyautogui.screenshot()

    image = np.array(screenshot)

    return cv2.cvtColor(
        image,
        cv2.COLOR_RGB2BGR
    )


def detect_text():

    image = capture_screen()

    results = reader.readtext(image)

    detected = []

    for r in results:

        box = r[0]

        text = r[1]

        x = int(box[0][0])

        y = int(box[0][1])

        detected.append({

            "text": text,

            "x": x,

            "y": y
        })

    return detected


def click_text(target):

    texts = detect_text()

    for item in texts:

        if target.lower() in item["text"].lower():

            print("CLICK:", target)

            pyautogui.click(

                item["x"],

                item["y"]
            )

            return True

    return False