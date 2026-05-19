from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio

from autonomous_agent_enhanced import (
    execute_autonomous_task
)

app = Flask(__name__)

CORS(app)

# =====================================================
# HEALTH
# =====================================================

@app.route("/health", methods=["GET"])
def health():

    return jsonify({

        "success": True,

        "status": "healthy"
    })

# =====================================================
# AUTONOMOUS EXECUTION
# =====================================================

@app.route(
    "/api/autonomous/execute",
    methods=["POST"]
)
def autonomous_execute():

    try:

        data = request.json

        task = data.get("task", "")

        print(f"🔥 TASK: {task}")

        # RUN ASYNC
        result = asyncio.run(
            execute_autonomous_task(task)
        )

        print("✅ RESULT:", result)

        # ALWAYS RETURN VALID FORMAT
        return jsonify({

            "success":
                result.get(
                    "success",
                    True
                ),

            "response":
                result.get(
                    "response",
                    "Task completed"
                ),

            "result": result
        })

    except Exception as e:

        print("❌ ERROR:", str(e))

        return jsonify({

            "success": False,

            "response": str(e)
        })

# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    print("🔥 JARVIS BACKEND STARTED")

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True
    )