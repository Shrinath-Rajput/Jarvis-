from Backend.planner_ai import plan_task

from tools import (
    open_app,
    search_google,
    search_youtube,
    create_folder,
    write_text,
    take_screenshot
)


# ------------------------
# EXECUTE ACTIONS
# ------------------------

def run_agent(command):

    print(
        "USER COMMAND:",
        command
    )

    actions = plan_task(command)

    print(
        "PLANNED ACTIONS:",
        actions
    )

    results = []

    for action in actions:

        tool = action["tool"]

        try:

            # OPEN APP
            if tool == "open_app":

                result = open_app(
                    action["app"]
                )

            # SEARCH GOOGLE
            elif tool == "search_google":

                result = search_google(
                    action["query"]
                )

            # SEARCH YOUTUBE
            elif tool == "search_youtube":

                result = search_youtube(
                    action["query"]
                )

            # CREATE FOLDER
            elif tool == "create_folder":

                result = create_folder(
                    action["name"]
                )

            # WRITE TEXT
            elif tool == "write_text":

                result = write_text(
                    action["text"]
                )

            # SCREENSHOT
            elif tool == "take_screenshot":

                result = take_screenshot()

            else:

                result = (
                    f"Unknown tool {tool}"
                )

            results.append(result)

        except Exception as e:

            results.append(str(e))

    if not results:

        return (
            "No actions planned"
        )

    return "\n".join(results)