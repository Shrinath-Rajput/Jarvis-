from flask import Flask, request, jsonify
from flask_cors import CORS

from commands import execute_command
from ai_brain import ask_ai

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return jsonify({
        "status": "Jarvis Running"
    })


@app.route("/command", methods=["POST"])
def command():

    try:

        data = request.json

        user_command = data.get(
            "command",
            ""
        )

        print("\nUSER:", user_command)

        local_response = execute_command(
            user_command
        )

        if "not recognized" in local_response.lower():
            response = ask_ai(user_command)
        else:
            response = local_response

        print("JARVIS:", response)

        return jsonify({
            "response": response
        })

    except Exception as e:

        print("ERROR:", str(e))

        return jsonify({
            "response": str(e)
        })


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )