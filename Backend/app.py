from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
import logging

from autonomous_agent_enhanced import (
    EnhancedAutonomousAgent
)

# ======================================================
# LOGGING
# ======================================================

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

# ======================================================
# FLASK
# ======================================================

app = Flask(__name__)

CORS(app)

# ======================================================
# AGENT
# ======================================================

print("STARTING JARVIS...")

autonomous_agent = EnhancedAutonomousAgent()

print("JARVIS READY")

# ======================================================
# HEALTH
# ======================================================

@app.route("/health", methods=["GET"])
def health():

    return jsonify({

        "success": True,

        "status": "healthy",

        "message": "Jarvis backend running"
    })

# ======================================================
# COMMAND API
# ======================================================

@app.route(

    "/api/autonomous/execute",

    methods=["POST"]
)
def execute_autonomous():

    try:

        data = request.json

        task = data.get("task", "")

        if not task:

            return jsonify({

                "success": False,

                "error": "No task provided"
            })

        logger.info("=" * 60)
        logger.info(f"TASK: {task}")
        logger.info("=" * 60)

        # ==============================================
        # RUN AGENT
        # ==============================================

        result = asyncio.run(

            autonomous_agent.execute_autonomous_task(
                task
            )
        )

        logger.info(f"RESULT: {result}")

        return jsonify(result)

    except Exception as e:

        logger.error(str(e))

        return jsonify({

            "success": False,

            "status": "failed",

            "error": str(e)
        })

# ======================================================
# OLD COMMAND ROUTE
# ======================================================

@app.route("/command", methods=["POST"])
def command():

    try:

        data = request.json

        task = data.get("command", "")

        result = asyncio.run(

            autonomous_agent.execute_autonomous_task(
                task
            )
        )

        return jsonify(result)

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)
        })

# ======================================================
# MAIN
# ======================================================

if __name__ == "__main__":

    print("\n========================")
    print("JARVIS BACKEND STARTED")
    print("========================\n")

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True
    )