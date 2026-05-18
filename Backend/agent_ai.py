from planner_ai import create_plan

from tools import (
    open_app,
    search_google,
    search_youtube,
    create_folder,
    write_text,
    take_screenshot
)


def run_agent(command):

    print(
        "\nUSER:",
        command
    )

    actions = create_plan(
        command
    )

    print(
        "\nAI PLAN:",
        actions
    )

    if not actions:

        return (
            "AI could not create plan"
        )

    results = []

    for action in actions:

        tool = action.get(
            "tool"
        )

        try:

            # =========================
            # OPEN APP
            # =========================

            if tool == "open_app":

                result = open_app(
                    action.get("app")
                )

            # =========================
            # GOOGLE SEARCH
            # =========================

            elif tool == "search_google":

                result = search_google(
                    action.get("query")
                )

            # =========================
            # YOUTUBE SEARCH
            # =========================

            elif tool == "search_youtube":

                result = search_youtube(
                    action.get("query")
                )

            # =========================
            # CREATE FOLDER
            # =========================

            elif tool == "create_folder":

                result = create_folder(
                    action.get("name")
                )

            # =========================
            # WRITE TEXT
            # =========================

            elif tool == "write_text":

                result = write_text(
                    action.get("text")
                )

            # =========================
            # SCREENSHOT
            # =========================

            elif tool == "take_screenshot":

                result = take_screenshot()

            else:

                result = (
                    f"Unknown tool: {tool}"
                )

            results.append(result)

        except Exception as e:

            results.append(
                str(e)
            )

    return "\n".join(results)