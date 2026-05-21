# app.py

import json
from datetime import datetime
from flask import (
    Flask,
    request,
    jsonify
)

from flask_cors import CORS

from config import validate_config
from planner_ai import DynamicPlanner
from executor import execute_plan

validate_config()

app = Flask(__name__)

CORS(app)

planner = DynamicPlanner()

# ===================================
# LOGGING
# ===================================

def log_event(event_type, message, data=None):
    """Log events with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{event_type}] {message}")
    if data:
        print(f"  → {json.dumps(data, indent=2)}")


@app.route("/")
def root():

    log_event("INFO", "Root endpoint accessed")

    return jsonify({

        "success": True,

        "message": "Jarvis AI Backend Running"
    })


@app.route("/health")
def health():

    log_event("INFO", "Health check")

    return jsonify({
        "success": True
    })


@app.route("/status")
def status():
    """Get detailed backend status"""
    
    import platform
    import sys
    
    log_event("STATUS", "Status check requested")
    
    status_data = {
        "backend": "running",
        "version": "1.0",
        "python": platform.python_version(),
        "platform": platform.system(),
        "endpoints": {
            "health": "http://127.0.0.1:5000/health",
            "execute": "http://127.0.0.1:5000/api/autonomous/execute",
            "status": "http://127.0.0.1:5000/status"
        },
        "timestamp": datetime.now().isoformat()
    }
    
    return jsonify(status_data)


@app.route(
    "/api/autonomous/execute",
    methods=["POST"]
)
def execute():

    try:

        data = request.json

        task = data.get("task")

        log_event("TASK", f"Received task: {task}")

        if not task:

            log_event("ERROR", "Task is missing from request")

            return jsonify({

                "success": False,

                "error": "Task missing"
            }), 400

        # Plan the task
        log_event("PLANNING", f"Planning task: {task}")
        
        plan = planner.plan_task(task)
        
        log_event("PLAN", f"Generated plan with {len(plan)} steps", plan)

        # Execute the plan
        log_event("EXECUTING", f"Executing plan...")
        
        results = execute_plan(plan)
        
        log_event("EXECUTION_RESULTS", f"Execution complete", results)

        # Check if any step succeeded
        success = any(
            r.get("success", False)
            for r in results
        )

        response = {

            "success": success,

            "task": task,

            "plan": plan,

            "results": results,
            
            "message": "Task completed" if success else "Task failed",
            
            "timestamp": datetime.now().isoformat()
        }
        
        log_event("SUCCESS" if success else "FAILURE", 
                 f"Task response: success={success}")

        return jsonify(response)

    except Exception as e:

        log_event("ERROR", f"Execution error: {str(e)}")

        return jsonify({

            "success": False,

            "error": str(e),
            
            "timestamp": datetime.now().isoformat()
        }), 500


if __name__ == "__main__":

    log_event("STARTUP", "Starting Jarvis Backend Server")
    
    print("\n" + "="*60)
    print("  🤖 JARVIS AI BACKEND")
    print("  Running on http://127.0.0.1:5000")
    print("  Press Ctrl+C to stop")
    print("="*60 + "\n")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )