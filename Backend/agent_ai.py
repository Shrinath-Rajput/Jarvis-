import time

from planner_ai import create_plan

from tools import (

    open_app,
    open_website,

    search_google,
    search_youtube,

    create_folder,

    write_text,

    take_screenshot,

    click_text,
    press_key,
    type_text
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
            # OPEN WEBSITE
            # =========================

            elif tool == "open_website":

                result = open_website(
                    action.get("site")
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
            # CLICK TEXT
            # =========================

            elif tool == "click_text":

                result = click_text(
                    action.get("text")
                )

            # =========================
            # PRESS KEY
            # =========================

            elif tool == "press_key":

                result = press_key(
                    action.get("key")
                )

            # =========================
            # WAIT
            # =========================

            elif tool == "wait":

                time.sleep(
                    action.get("seconds")
                )

                result = (
                    f"Waited "
                    f"{action.get('seconds')} sec"
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

            print(
                "RESULT:",
                result
            )

            results.append(result)

        except Exception as e:

            results.append(
                str(e)
            )

    return "\n".join(results)