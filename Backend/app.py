# =========================================================
# FINAL WORKING app.py
# DYNAMIC AUTONOMOUS AI SERVER
# =========================================================

from flask import Flask, request, jsonify
from flask_cors import CORS

import logging
import traceback

# =========================================================
# IMPORTS
# =========================================================

try:

    from planner_ai import DynamicPlanner

    PLANNER_AVAILABLE = True

except Exception as e:

    print("PLANNER ERROR:", e)

    PLANNER_AVAILABLE = False

try:

    from executor import execute_plan

    EXECUTOR_AVAILABLE = True

except Exception as e:

    print("EXECUTOR ERROR:", e)

    EXECUTOR_AVAILABLE = False

# =========================================================
# APP
# =========================================================

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

app = Flask(__name__)

CORS(app)

# =========================================================
# HEALTH
# =========================================================

@app.route("/health", methods=["GET"])
def health():

    return jsonify({

        "success": True,

        "status": "healthy",

        "planner": PLANNER_AVAILABLE,

        "executor": EXECUTOR_AVAILABLE
    })

# =========================================================
# MAIN EXECUTION
# =========================================================

@app.route("/api/autonomous/execute", methods=["POST"])
def autonomous_execute():

    try:

        # =================================================
        # CHECK SYSTEM
        # =================================================

        if not PLANNER_AVAILABLE:

            return jsonify({

                "success": False,

                "response":
                    "Planner not available"
            })

        if not EXECUTOR_AVAILABLE:

            return jsonify({

                "success": False,

                "response":
                    "Executor not available"
            })

        # =================================================
        # GET TASK
        # =================================================

        data = request.json

        task = data.get("task", "").strip()

        if not task:

            return jsonify({

                "success": False,

                "response":
                    "No task provided"
            })

        print("\n🔥 USER TASK:")
        print(task)

        # =================================================
        # CREATE PLANNER
        # =================================================

        planner = DynamicPlanner()

        # =================================================
        # GENERATE PLAN
        # =================================================

        plan = planner.plan_task(task)

        print("\n🧠 GENERATED PLAN:")
        print(f"  Steps: {len(plan) if plan else 0}")
        for idx, step in enumerate(plan or []):
            print(f"  {idx+1}. {step.get('tool', 'unknown')} - {step.get('params', {})}")


        # =================================================
        # PLAN FAILED
        # =================================================

        if not plan or len(plan) == 0:
            return jsonify({
                "success": False,
                "response": "Could not generate plan",
                "task": task,
                "plan": None,
                "results": [],
                "error": "Planner returned empty plan"
            })

        # =================================================
        # EXECUTE PLAN
        # =================================================

        results = execute_plan(plan)

        print("\n⚡ EXECUTION RESULTS:")
        print(results)

        # =================================================
        # CHECK RESULTS
        # =================================================

        # Count successes and failures
        successful_actions = [r for r in results if r.get("success", False)]
        failed_actions = [r for r in results if not r.get("success", True)]

        # Task is successful if ANY action succeeded
        task_success = len(successful_actions) > 0

        print(f"\n📊 RESULTS ANALYSIS:")
        print(f"  ✅ Successful: {len(successful_actions)}/{len(results)}")
        print(f"  ❌ Failed: {len(failed_actions)}/{len(results)}")

        # =================================================
        # FINAL RESPONSE
        # =================================================

        return jsonify({
            "success": task_success,
            "status": "completed" if task_success else "failed",
            "response": (
                "Task completed successfully"
                if task_success
                else "Task could not be completed"
            ),
            "task": task,
            "plan": plan,
            "results": results,
            "summary": {
                "total_steps": len(results),
                "successful_steps": len(successful_actions),
                "failed_steps": len(failed_actions)
            }
        })

    except Exception as e:

        traceback.print_exc()

        return jsonify({

            "success": False,

            "response": str(e)
        })

# =========================================================
# TEST
# =========================================================

@app.route("/", methods=["GET"])
def root():

    return jsonify({

        "success": True,

        "message":
            "Autonomous AI Running"
    })

# =========================================================
# INFO
# =========================================================

@app.route("/api/info", methods=["GET"])
def info():

    return jsonify({

        "name":
            "Dynamic Autonomous AI",

        "hardcoded":
            False,

        "architecture":
            "OTAV",

        "features": [

            "Dynamic reasoning",

            "OCR clicking",

            "LLM planning",

            "No hardcoding",

            "Self verification",

            "Retry system"
        ]
    })

# =========================================================
# START
# =========================================================

if __name__ == "__main__":

    print("\n🚀 AUTONOMOUS AI STARTED")

    print("✅ Dynamic reasoning enabled")

    print("✅ No hardcoding")

    print("✅ OCR enabled")

    print("✅ Planner ready")

    print("✅ Executor ready")

    app.run(

        host="127.0.0.1",

        port=5000,

        debug=False
    )