from flask import Flask, request, jsonify
from flask_cors import CORS

from commands import execute_command

app = Flask(__name__)

# FULL CORS FIX
CORS(
    app,
    resources={
        r"/*": {
            "origins": "*"
        }
    }
)

# HOME
@app.route("/")

def home():

    return jsonify({

        "message":
        "Jarvis API is running",

        "endpoints": {

            "POST /command":
            "Execute a command"

        }
    })

# COMMAND API
@app.route(
    "/command",
    methods=["POST"]
)

def command():

    try:

        data = request.get_json()

        user_command = data.get(
            "command",
            ""
        )

        print(
            "USER COMMAND:",
            user_command
        )

        response = execute_command(
            user_command
        )

        return jsonify({

            "success": True,

            "response": response

        })

    except Exception as e:

        print("ERROR:", e)

        return jsonify({

            "success": False,

            "response": str(e)

        }), 500

# START SERVER
if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )