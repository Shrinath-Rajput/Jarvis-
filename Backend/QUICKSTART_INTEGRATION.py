"""
Quick Start: Autonomous Agent System
Copy this into your app.py to integrate the autonomous agent
"""

# Add these imports to your existing app.py
from autonomous_api import register_autonomous_api
from tool_implementations import register_all_tools

# In your Flask app initialization (after creating Flask app):

# ========================
# AUTONOMOUS AGENT SETUP
# ========================

# Initialize the autonomous agent system
try:
    logger.info("🤖 Initializing Autonomous Agent System...")
    
    # Register all available tools
    register_all_tools()
    logger.info("✅ Tool registry initialized")
    
    # Register API endpoints
    register_autonomous_api(app)
    logger.info("✅ Autonomous API endpoints registered")
    
    # Verify components
    from autonomous_agent_enhanced import get_autonomous_agent
    from tool_registry import get_tool_registry
    
    agent = get_autonomous_agent()
    registry = get_tool_registry()
    
    logger.info(f"✅ Agent ready with {len(registry.get_all_tools())} tools")
    
except Exception as e:
    logger.error(f"❌ Failed to initialize autonomous agent: {str(e)}")
    raise


# ========================
# EXISTING ENDPOINTS
# ========================

# Your existing endpoints continue to work as before
# The autonomous agent system is completely separate but integrated

@app.route("/command", methods=["POST"])
def command():
    """
    Existing endpoint - now uses autonomous agent
    
    You can keep this as-is or forward to /api/autonomous/execute
    """
    try:
        data = request.json
        command_text = data.get('command')
        
        # Option 1: Use old system (backward compatibility)
        # result = run_agent(command_text)
        
        # Option 2: Use new autonomous system (recommended)
        import asyncio
        agent = get_autonomous_agent()
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            agent.execute_autonomous_task(command_text)
        )
        loop.close()
        
        return jsonify({
            "success": True,
            "result": result
        })
        
    except Exception as e:
        logger.error(f"Command error: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ========================
# MAIN ENTRY POINT
# ========================

if __name__ == "__main__":
    logger.info("🚀 Starting JARVIS with Autonomous Agent System")
    logger.info(f"🌐 Server running on {FLASK_HOST}:{FLASK_PORT}")
    logger.info("📚 API Documentation at /api/autonomous/tools/list")
    
    app.run(
        host=FLASK_HOST,
        port=FLASK_PORT,
        debug=DEBUG,
        threaded=True
    )
