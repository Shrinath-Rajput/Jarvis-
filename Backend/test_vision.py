from vision_ai import (
    save_screenshot,
    read_screen_text
)

print(
    save_screenshot()
)

texts = read_screen_text()

print("\nSCREEN TEXT:\n")

for text in texts:

    print(text)