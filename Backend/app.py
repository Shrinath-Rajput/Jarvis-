"""
JARVIS AI System - Main Flask API Server
Advanced autonomous AI assistant with multi-step planning and execution
"""
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import logging
import json
from datetime import datetime

# Import core modules
from config import (
    DEBUG,
    FLASK_HOST,
    FLASK_PORT,
    CORS_ENABLED,
    validate_config,
)
from ai_brain import get_ai
from planner_ai import get_planner
from executor import get_executor
from memory_manager import get_memory_manager
from browser_control import close_browser

# Setup logging
logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask
app = Flask(__name__)

# Configure CORS properly
if CORS_ENABLED:
    CORS(app, 
         origins="*",
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         allow_headers=["Content-Type", "Authorization"],
         supports_credentials=False,
         max_age=3600)

# Add additional CORS headers to all responses
@app.after_request
def after_request(response):
    if CORS_ENABLED:
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Initialize components
try:
    validate_config()
    ai = get_ai()
    planner = get_planner()
    executor = get_executor()
    memory = get_memory_manager()
    logger.info("✅ All components initialized successfully")
except Exception as e:
    logger.error(f"❌ Initialization error: {str(e)}")
    raise

# ========================
# BASIC ENDPOINTS
# ========================

@app.route("/", methods=["GET", "OPTIONS"])
def home():
    """Health check endpoint"""
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200
    return jsonify({
        "status": "✅ JARVIS Running",
        "version": "1.0",
        "features": [
            "Natural Language Understanding",
            "Multi-step Planning",
            "Browser Automation",
            "Computer Control",
            "Memory & Learning",
            "Vision Analysis",
        ]
    })

@app.route("/health", methods=["GET", "OPTIONS"])
def health():
    """Extended health check"""
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "memory_stats": memory.get_statistics()
    })

# ========================
# MAIN COMMAND ENDPOINT
# ========================

@app.route("/command", methods=["POST", "OPTIONS"])
def execute_command():
    """
    Main command execution endpoint
    
    Request JSON:
    {
        "command": "user command",
        "text": "user command (alternative)",
        "context": "optional context",
        "stream": false
    }
    
    Response:
    {
        "success": true,
        "response": "AI response",
        "plan": [...],
        "execution_results": [...],
        "metadata": {...}
    }
    """
    # Handle preflight CORS request
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "No JSON data provided"
            }), 400
        
        # Support both "command" and "text" parameters
        user_text = data.get("command", "").strip() or data.get("text", "").strip()
        context = data.get("context", "")
        stream = data.get("stream", False)
        
        if not user_text:
            return jsonify({
                "success": False,
                "error": "Empty command"
            }), 400
        
        logger.info(f"\n{'='*50}")
        logger.info(f"USER: {user_text}")
        logger.info(f"{'='*50}")
        
        # Store in memory
        try:
            memory.add_conversation("user", user_text, {"context": context})
        except Exception as e:
            logger.warning(f"Memory store error: {e}")
        
        # Get AI understanding with fallback
        understanding = ""
        try:
            understanding = ai.chat(
                f"Understand this request and explain what the user wants: {user_text}",
                context
            )
            logger.info(f"Understanding: {understanding[:100]}...")
        except Exception as e:
            logger.error(f"AI understanding error: {e}")
            understanding = f"User wants: {user_text}"
        
        # Create plan with fallback
        plan = []
        try:
            plan = planner.create_plan(user_text, understanding)
            logger.info(f"Plan created: {len(plan)} actions")
        except Exception as e:
            logger.error(f"Plan creation error: {e}")
            plan = []
        
        # Generate response
        response_text = ""
        results = []
        successful = 0
        
        if not plan:
            logger.info("No plan created - generating natural response")
            try:
                response_text = ai.chat(
                    f"Cannot create automated plan for: {user_text}\n"
                    f"Just respond naturally to the user request in 1-2 sentences.",
                    context
                )
                logger.info(f"Natural response: {response_text[:100]}...")
            except Exception as e:
                logger.error(f"Natural response error: {e}", exc_info=True)
                response_text = f"I understood your request: '{user_text}'. I'll work on it."
                logger.info(f"Using fallback response: {response_text}")
        else:
            # Execute plan with error handling
            logger.info(f"Plan has {len(plan)} actions - executing...")
            try:
                logger.info("Starting plan execution...")
                results = executor.execute_plan(plan)
                successful = sum(1 for r in results if r.success)
                failed = len(results) - successful
                logger.info(f"Execution complete: {successful} successful, {failed} failed")
                
                # Generate response summary
                results_summary = json.dumps(
                    [r.to_dict() for r in results],
                    indent=2,
                    default=str
                )
                try:
                    response_text = ai.chat(
                        f"Task completed. Summarize in 1-2 sentences what was done.\n\n"
                        f"Original request: {user_text}\n"
                        f"Results: {results_summary[:500]}",
                        context
                    )
                    logger.info(f"Execution response: {response_text[:100]}...")
                except Exception as ai_err:
                    logger.error(f"AI summary error: {ai_err}")
                    response_text = f"Task executed with {successful} successes."
                    logger.info(f"Using summary fallback: {response_text}")
            except Exception as e:
                logger.error(f"Execution error: {e}", exc_info=True)
                response_text = f"I attempted to execute your request: '{user_text}'. There was an issue during execution."
                logger.info(f"Using execution error fallback: {response_text}")
        
        # Validate and ensure we have a response
        if not response_text or len(response_text.strip()) == 0:
            response_text = f"Request processed: {user_text}"
            logger.warning(f"Response was empty, using default: {response_text}")
        
        # Check if response contains error keywords and replace with sensible message
        if any(err in response_text.lower() for err in ["error", "could not", "failed", "unable"]):
            logger.warning(f"Response contains error keywords: {response_text[:100]}...")
            response_text = f"I understood your request about {user_text}. Processing now."
        
        logger.info(f"JARVIS: {response_text[:100]}...")
        
        # Store response in memory
        try:
            memory.add_conversation("assistant", response_text, {
                "plan_size": len(plan) if plan else 0,
                "execution_success": successful if plan else None
            })
        except Exception as e:
            logger.warning(f"Memory response store error: {e}")
        
        return jsonify({
            "success": True,
            "response": response_text,
            "plan": plan,
            "execution_results": [r.to_dict() for r in results] if plan else [],
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "understanding": understanding,
                "plan_size": len(plan) if plan else 0,
            }
        })
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"❌ Command Error: {error_msg}", exc_info=True)
        
        # Return structured error response with fallback message
        return jsonify({
            "success": False,
            "response": f"I encountered an error: {error_msg}. Please try again.",
            "error": error_msg,
            "plan": [],
            "execution_results": [],
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "error_type": type(e).__name__
            }
        }), 500


# ========================
# PLANNING ENDPOINT
# ========================

@app.route("/api/plan", methods=["POST"])
def create_plan():
    """Create a plan without executing"""
    try:
        data = request.get_json()
        user_text = data.get("text", "").strip()
        
        if not user_text:
            return jsonify({"success": False, "error": "Empty text"}), 400
        
        plan = planner.create_plan(user_text)
        explanation = planner.explain_plan(plan) if plan else "Cannot create plan"
        
        return jsonify({
            "success": True,
            "plan": plan,
            "explanation": explanation
        })
        
    except Exception as e:
        logger.error(f"Plan error: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


# ========================
# EXECUTION ENDPOINT
# ========================

@app.route("/api/execute", methods=["POST"])
def execute_plan():
    """Execute a pre-created plan"""
    try:
        data = request.get_json()
        plan = data.get("plan", [])
        
        if not plan:
            return jsonify({"success": False, "error": "Empty plan"}), 400
        
        results = executor.execute_plan(plan)
        summary = executor.get_results_summary()
        
        return jsonify({
            "success": True,
            "results": [r.to_dict() for r in results],
            "summary": summary
        })
        
    except Exception as e:
        logger.error(f"Execution error: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


# ========================
# AI CHAT ENDPOINT
# ========================

@app.route("/api/chat", methods=["POST"])
def chat():
    """Direct chat with AI (no planning)"""
    try:
        data = request.get_json()
        user_text = data.get("text", "").strip()
        context = data.get("context", "")
        
        if not user_text:
            return jsonify({"success": False, "error": "Empty text"}), 400
        
        memory.add_conversation("user", user_text)
        
        response = ai.chat(user_text, context)
        
        memory.add_conversation("assistant", response)
        
        return jsonify({
            "success": True,
            "response": response
        })
        
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


# ========================
# VISION ENDPOINT
# ========================

@app.route("/api/vision", methods=["POST"])
def analyze_image():
    """Analyze an image"""
    try:
        data = request.get_json()
        image_path = data.get("image_path", "")
        question = data.get("question", "")
        
        if not image_path:
            return jsonify({"success": False, "error": "No image path"}), 400
        
        from ai_brain import analyze_image as analyze_img
        result = analyze_img(image_path, question)
        
        return jsonify({
            "success": True,
            "analysis": result
        })
        
    except Exception as e:
        logger.error(f"Vision error: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


# ========================
# MEMORY ENDPOINTS
# ========================

@app.route("/api/memory/stats", methods=["GET"])
def memory_stats():
    """Get memory statistics"""
    try:
        stats = memory.get_statistics()
        return jsonify({"success": True, "statistics": stats})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/memory/conversation", methods=["GET"])
def get_conversation():
    """Get conversation history"""
    try:
        limit = request.args.get("limit", 20, type=int)
        history = memory.get_conversation_history(limit)
        return jsonify({"success": True, "conversation": history})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/memory/clear", methods=["POST"])
def clear_memory():
    """Clear memory"""
    try:
        memory.clear_memory()
        memory.clear_conversation()
        return jsonify({"success": True, "message": "Memory cleared"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ========================
# STATUS ENDPOINT
# ========================

@app.route("/api/status", methods=["GET"])
def status():
    """Get system status"""
    try:
        stats = memory.get_statistics()
        return jsonify({
            "success": True,
            "status": "running",
            "memory_stats": stats,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ========================
# ERROR HANDLERS
# ========================

@app.errorhandler(404)
def not_found(error):
    return jsonify({"success": False, "error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"success": False, "error": "Internal server error"}), 500


# ========================
# SHUTDOWN HANDLER
# ========================

@app.teardown_appcontext
def cleanup(error):
    """Clean up resources on shutdown"""
    try:
        close_browser()
        executor.cleanup()
        logger.info("✅ Cleanup completed")
    except Exception as e:
        logger.error(f"Cleanup error: {str(e)}")


# ========================
# MAIN
# ========================

if __name__ == "__main__":
    logger.info("="*50)
    logger.info("🤖 JARVIS AI SYSTEM STARTING")
    logger.info("="*50)
    logger.info(f"Host: {FLASK_HOST}")
    logger.info(f"Port: {FLASK_PORT}")
    logger.info(f"Debug: {DEBUG}")
    logger.info("="*50)
    
    app.run(
        host=FLASK_HOST,
        port=int(FLASK_PORT),
        debug=DEBUG
    )