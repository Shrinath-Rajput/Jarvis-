def plan_task(command):

    cmd = command.lower()

    actions = []

    # OPEN CHROME
    if "chrome" in cmd:

        actions.append({

            "tool": "open_app",

            "app": "chrome"

        })

    # OPEN VSCODE
    if (
        "vs code" in cmd
        or "vscode" in cmd
    ):

        actions.append({

            "tool": "open_app",

            "app": "vscode"

        })

    # OPEN NOTEPAD
    if "notepad" in cmd:

        actions.append({

            "tool": "open_app",

            "app": "notepad"

        })

    # YOUTUBE SEARCH
    if (
        "youtube" in cmd
        and "search" in cmd
    ):

        query = (
            cmd
            .replace("youtube", "")
            .replace("search", "")
        )

        actions.append({

            "tool": "search_youtube",

            "query": query

        })

    # GOOGLE SEARCH
    elif "search" in cmd:

        query = cmd.replace(
            "search",
            ""
        )

        actions.append({

            "tool": "search_google",

            "query": query

        })

    # CREATE FOLDER
    if (
        "create" in cmd
        and "folder" in cmd
    ):

        words = cmd.split()

        folder_name = "NewFolder"

        try:

            index = words.index(
                "create"
            )

            folder_name = words[
                index + 1
            ]

        except:
            pass

        actions.append({

            "tool": "create_folder",

            "name": folder_name

        })

    # WRITE TEXT
    if "write" in cmd:

        text = cmd.split(
            "write"
        )[-1]

        actions.append({

            "tool": "write_text",

            "text": text

        })

    return actions