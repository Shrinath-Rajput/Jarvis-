def create_plan(command):

    command = command.lower()

    actions = []

    # =========================
    # CHROME / GOOGLE
    # =========================

    if (
        "chrome" in command
        or "google" in command
    ):

        actions.append({
            "tool": "open_app",
            "app": "chrome"
        })

        if "search" in command:

            query = (
                command
                .split("search")[-1]
                .replace("for", "")
                .strip()
            )

            actions.append({
                "tool": "search_google",
                "query": query
            })

    # =========================
    # YOUTUBE
    # =========================

    elif "youtube" in command:

        if "search" in command:

            query = (
                command
                .replace("youtube", "")
                .replace("search", "")
                .replace("for", "")
                .strip()
            )

            actions.append({
                "tool": "search_youtube",
                "query": query
            })

        else:

            actions.append({
                "tool": "open_app",
                "app": "youtube"
            })

    # =========================
    # VS CODE
    # =========================

    elif (
        "vs code" in command
        or "vscode" in command
    ):

        actions.append({
            "tool": "open_app",
            "app": "vscode"
        })

        # CREATE FOLDER
        if (
            "create" in command
            and "folder" in command
        ):

            import re

            folder_name = "project"

            match = re.search(
                r'folder (.*)',
                command
            )

            if match:

                folder_name = (
                    match.group(1)
                    .strip()
                    .replace(" ", "_")
                )

            actions.append({
                "tool": "create_folder",
                "name": folder_name
            })

        # WRITE CODE
        if (
            "hello world" in command
            or "python" in command
        ):

            actions.append({
                "tool": "write_text",
                "text": 'print("Hello World")'
            })

    # =========================
    # NOTEPAD
    # =========================

    elif "notepad" in command:

        actions.append({
            "tool": "open_app",
            "app": "notepad"
        })

        if "write" in command:

            text = (
                command
                .split("write")[-1]
                .strip()
            )

            if (
                "python" in text
                or "hello world" in text
            ):

                text = (
                    'print("Hello World")'
                )

            actions.append({
                "tool": "write_text",
                "text": text
            })

    # =========================
    # SCREENSHOT
    # =========================

    elif "screenshot" in command:

        actions.append({
            "tool": "take_screenshot"
        })

    return actions