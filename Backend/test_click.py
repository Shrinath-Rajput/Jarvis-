from vision_ai import (
    save_screenshot,
    read_screen_text,
    click_text
)

print(
    save_screenshot()
)

print(
    "\nSCREEN TEXT:\n"
)

texts = read_screen_text()

for text in texts:

    print(text)

print(
    "\nCLICK TEST:\n"
)

print(
    click_text("Terminal")
)