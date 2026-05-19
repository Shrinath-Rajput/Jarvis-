"""
JARVIS AI SYSTEM - FINAL STABLE APP.PY
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback
import logging
from datetime import datetime

# =========================
# IMPORTS
# =========================

from ai_brain import get_ai
from planner_ai import get_planner
from executor import get_executor
from memory_manager import get_memory_manager
from autonomous_agent_enhanced import EnhancedAutonomousAgent

# =========================
# LOGGING
# =========================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# =========================
# FLASK
# =========================

app = Flask(__name__)

# =========================
# CORS FIX
# =========================

CORS(
    app,
    resources={
        r"/*": {
            "origins": [
                "http://localhost:5173",
                "http://127.0.0.1:5173"
            ]
        }
    }
)

# =========================
# INIT SYSTEMS
# =========================

print("STARTING JARVIS...")

ai = get_ai()
planner = get_planner()
executor = get_executor()
memory = get_memory_manager()

autonomous_agent = EnhancedAutonomousAgent(
    use_local_llm=True
)

print("JARVIS READY")

# =========================
# HOME
# =========================

@app.route("/")
def home():

    return jsonify({
        "success": True,
        "message": "JARVIS RUNNING"
    })

# =========================
# HEALTH
# =========================

@app.route("/health")
def health():

    return jsonify({
        "success": True,
        "status": "healthy",
        "time": datetime.now().isoformat()
    })

# =========================
# CHAT
# =========================

@app.route("/command", methods=["POST"])
def command():

    try:

        data = request.get_json()

        text = (
            data.get("command")
            or data.get("text")
            or ""
        ).strip()

        if not text:

            return jsonify({
                "success": False,
                "error": "Empty command"
            })

        print("\n====================")
        print("USER:", text)
        print("====================")

        # =====================
        # MEMORY
        # =====================

        try:
            memory.add_conversation(
                "user",
                text
            )
        except:
            pass

        # =====================
        # CREATE PLAN
        # =====================

        try:

            plan = planner.create_plan(text)

            print("PLAN:", plan)

        except Exception as e:

            print("PLAN ERROR:", e)

            plan = []

        # =====================
        # EXECUTE
        # =====================

        results = []

        if plan:

            try:

                results = executor.execute_plan(plan)

                print("EXECUTION COMPLETE")

            except Exception as e:

                print("EXECUTION ERROR")
                print(traceback.format_exc())

        # =====================
        # AI RESPONSE
        # =====================

        try:

            response = ai.chat(
                f"""
                User request:
                {text}

                Respond naturally in 1 sentence.
                """
            )

        except Exception as e:

            print("AI RESPONSE ERROR:", e)

            response = f"Processing request: {text}"

        # =====================
        # SAVE MEMORY
        # =====================

        try:

            memory.add_conversation(
                "assistant",
                response
            )

        except:
            pass

        return jsonify({

            "success": True,

            "response": response,

            "plan": plan,

            "results": [

                r.to_dict()
                if hasattr(r, "to_dict")
                else str(r)

                for r in results
            ]
        })

    except Exception as e:

        print(traceback.format_exc())

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# =========================
# AUTONOMOUS EXECUTION
# =========================

@app.route(
    "/api/autonomous/execute",
    methods=["POST"]
)
def autonomous_execute():

    try:

        data = request.get_json()

        task = data.get("task", "").strip()

        if not task:

            return jsonify({
                "success": False,
                "error": "Empty task"
            })

        print("\n==========================")
        print("AUTONOMOUS TASK:", task)
        print("==========================")

        import asyncio
        import time

        start = time.time()

        loop = asyncio.new_event_loop()

        asyncio.set_event_loop(loop)

        result = loop.run_until_complete(

            autonomous_agent.execute_autonomous_task(

                user_intent=task,

                max_steps=50
            )
        )

        loop.close()

        execution_time = time.time() - start

        print("AUTONOMOUS RESULT:")
        print(result)

        return jsonify({

            "success": True,

            "result": result,

            "execution_time": execution_time
        })

    except Exception as e:

        print("\nAUTONOMOUS ERROR")
        print(traceback.format_exc())

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500

# =========================
# STATUS
# =========================

@app.route("/api/status")
def status():

    return jsonify({

        "success": True,

        "status": "running",

        "time": datetime.now().isoformat()
    })

# =========================
# ERROR HANDLER
# =========================

@app.errorhandler(500)
def server_error(error):

    return jsonify({

        "success": False,

        "error": "Internal server error"

    }), 500

# =========================
# MAIN
# =========================

if __name__ == "__main__":

    print("\n========================")
    print("JARVIS BACKEND STARTED")
    print("========================\n")

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True,

        threaded=True,

        use_reloader=False
    )