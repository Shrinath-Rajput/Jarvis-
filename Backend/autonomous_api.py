"""
Flask API Integration for Autonomous Agent
Connects the React frontend to the enhanced autonomous agent
Provides endpoints for task execution and monitoring
"""
import logging
import json
import asyncio
from typing import Dict, Any
from flask import Blueprint, request, jsonify
from datetime import datetime

from autonomous_agent_enhanced import get_autonomous_agent
from tool_registry import get_tool_registry

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create blueprint for autonomous endpoints
autonomous_bp = Blueprint('autonomous', __name__, url_prefix='/api/autonomous')


# =========================
# TASK EXECUTION ENDPOINTS
# =========================

@autonomous_bp.route("/execute", methods=["POST"])
def execute_task():
    """
    Execute a task autonomously
    
    Request body:
    {
        "task": "What you want the AI to do",
        "max_steps": 100,  # optional
        "task_id": "custom-id"  # optional
    }
    """
    try:
        data = request.json
        user_intent = data.get('task') or data.get('command')
        
        if not user_intent:
            return jsonify({
                "success": False,
                "error": "Missing 'task' or 'command' in request"
            }), 400
        
        task_id = data.get('task_id')
        max_steps = data.get('max_steps', 150)
        
        logger.info(f"📥 Received task: {user_intent}")
        
        # Execute task asynchronously
        agent = get_autonomous_agent()
        
        # Run async function in event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        result = loop.run_until_complete(
            agent.execute_autonomous_task(
                user_intent,
                task_id=task_id,
                max_steps=max_steps
            )
        )
        
        loop.close()
        
        return jsonify({
            "success": True,
            "result": result
        })
        
    except Exception as e:
        logger.error(f"❌ Task execution error: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@autonomous_bp.route("/execute-voice", methods=["POST"])
def execute_voice_command():
    """
    Execute a task from voice input
    
    Request body:
    {
        "voice_text": "transcribed voice text",
        "max_steps": 100  # optional
    }
    """
    try:
        data = request.json
        voice_text = data.get('voice_text') or data.get('transcript')
        
        if not voice_text:
            return jsonify({
                "success": False,
                "error": "Missing voice_text"
            }), 400
        
        logger.info(f"🎤 Executing voice command: {voice_text}")
        
        agent = get_autonomous_agent()
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        result = loop.run_until_complete(
            agent.execute_autonomous_task(voice_text)
        )
        
        loop.close()
        
        return jsonify({
            "success": True,
            "result": result
        })
        
    except Exception as e:
        logger.error(f"❌ Voice command error: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# =========================
# TOOL REGISTRY ENDPOINTS
# =========================

@autonomous_bp.route("/tools/list", methods=["GET"])
def list_tools():
    """Get list of all available tools"""
    try:
        registry = get_tool_registry()
        tools = [t.to_dict() for t in registry.get_all_tools()]
        
        return jsonify({
            "success": True,
            "total": len(tools),
            "tools": tools
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@autonomous_bp.route("/tools/categories", methods=["GET"])
def list_tool_categories():
    """Get tools organized by category"""
    try:
        registry = get_tool_registry()
        tools_by_category = {}
        
        for tool in registry.get_all_tools():
            cat = tool.category.value
            if cat not in tools_by_category:
                tools_by_category[cat] = []
            tools_by_category[cat].append({
                "name": tool.name,
                "description": tool.description
            })
        
        return jsonify({
            "success": True,
            "categories": tools_by_category
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@autonomous_bp.route("/tools/search", methods=["POST"])
def search_tools():
    """
    Search for tools
    
    Request body:
    {
        "query": "search term"
    }
    """
    try:
        data = request.json
        query = data.get('query', '')
        
        if not query:
            return jsonify({
                "success": False,
                "error": "Missing query"
            }), 400
        
        registry = get_tool_registry()
        results = registry.search_tools(query)
        
        return jsonify({
            "success": True,
            "results": [t.to_dict() for t in results]
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@autonomous_bp.route("/tools/execute", methods=["POST"])
def execute_tool_directly():
    """
    Execute a tool directly (for testing)
    
    Request body:
    {
        "tool": "tool_name",
        "parameters": {param1: value1, param2: value2}
    }
    """
    try:
        data = request.json
        tool_name = data.get('tool')
        parameters = data.get('parameters', {})
        
        if not tool_name:
            return jsonify({
                "success": False,
                "error": "Missing tool name"
            }), 400
        
        registry = get_tool_registry()
        
        # Execute tool asynchronously
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        result = loop.run_until_complete(
            registry.execute_tool(tool_name, **parameters)
        )
        
        loop.close()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# =========================
# STATISTICS & MONITORING
# =========================

@autonomous_bp.route("/stats", methods=["GET"])
def get_statistics():
    """Get agent and tool statistics"""
    try:
        registry = get_tool_registry()
        stats = registry.get_statistics()
        
        return jsonify({
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "statistics": stats
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@autonomous_bp.route("/health", methods=["GET"])
def health_check():
    """Health check for autonomous agent"""
    try:
        agent = get_autonomous_agent()
        
        return jsonify({
            "success": True,
            "status": "healthy",
            "components": {
                "agent": "ready",
                "tools": f"{len(get_tool_registry().get_all_tools())} available",
                "timestamp": datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "status": "unhealthy"
        }), 500


# =========================
# CONFIGURATION ENDPOINTS
# =========================

@autonomous_bp.route("/config", methods=["GET"])
def get_config():
    """Get agent configuration"""
    try:
        agent = get_autonomous_agent()
        
        return jsonify({
            "success": True,
            "config": {
                "max_steps_per_task": agent.max_steps_per_task,
                "max_retries_per_action": agent.max_retries_per_action,
                "use_local_llm": agent.use_local_llm
            }
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@autonomous_bp.route("/config", methods=["PUT"])
def update_config():
    """
    Update agent configuration
    
    Request body:
    {
        "max_steps_per_task": 200,
        "max_retries_per_action": 5
    }
    """
    try:
        data = request.json
        agent = get_autonomous_agent()
        
        if 'max_steps_per_task' in data:
            agent.max_steps_per_task = data['max_steps_per_task']
        
        if 'max_retries_per_action' in data:
            agent.max_retries_per_action = data['max_retries_per_action']
        
        logger.info("✅ Agent configuration updated")
        
        return jsonify({
            "success": True,
            "message": "Configuration updated",
            "config": {
                "max_steps_per_task": agent.max_steps_per_task,
                "max_retries_per_action": agent.max_retries_per_action
            }
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# =========================
# ACTION HISTORY & LOGGING
# =========================

@autonomous_bp.route("/history", methods=["GET"])
def get_action_history():
    """Get recent action history"""
    try:
        agent = get_autonomous_agent()
        limit = request.args.get('limit', 20, type=int)
        
        history = agent.action_history[-limit:]
        
        return jsonify({
            "success": True,
            "total_actions": len(agent.action_history),
            "recent_actions": history
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@autonomous_bp.route("/decision-history", methods=["GET"])
def get_decision_history():
    """Get decision history"""
    try:
        agent = get_autonomous_agent()
        limit = request.args.get('limit', 20, type=int)
        
        history = agent.decision_history[-limit:]
        
        return jsonify({
            "success": True,
            "total_decisions": len(agent.decision_history),
            "recent_decisions": history
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


def register_autonomous_api(app):
    """Register autonomous API blueprint with Flask app"""
    app.register_blueprint(autonomous_bp)
    logger.info("✅ Autonomous API endpoints registered")
