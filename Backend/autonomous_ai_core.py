"""
======================================
AUTONOMOUS AI CORE - MAIN ORCHESTRATOR
======================================

This is the heart of the autonomous system.

Flow:
1. Accept user request
2. Reason dynamically using AI planner
3. Generate action plan (JSON)
4. Execute each action
5. Verify and retry if needed
6. Maintain memory and context

NO HARDCODING. PURE DYNAMIC REASONING.
"""

import logging
import json
import time
from typing import Dict, List, Optional
from datetime import datetime

from planner_ai import plan_task, improve_plan
from executor import execute_plan, execute_action
from screen_understanding import analyze_current_screen
from memory_manager import MemoryManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ======================================
# AUTONOMOUS AGENT
# ======================================

class AutonomousAIAgent:
    """
    Main autonomous AI agent.
    Implements OBSERVE → THINK → ACT → VERIFY loop.
    """
    
    def __init__(self):
        self.memory = MemoryManager()
        self.current_task = None
        self.execution_history = []
        self.max_retries = 3
        logger.info("✅ AutonomousAIAgent initialized")
    
    # ======================================
    # MAIN EXECUTION LOOP
    # ======================================
    
    async def execute_task(self, user_request: str) -> Dict:
        """
        Execute any user request end-to-end.
        
        Args:
            user_request: Natural language user request
            
        Returns:
            Execution result dictionary
        """
        
        logger.info(f"🚀 Task: {user_request}")
        
        self.current_task = user_request
        result = {
            "task": user_request,
            "status": "pending",
            "plan": [],
            "execution_results": [],
            "final_verification": False,
            "error": None,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            # =====================================
            # PHASE 1: OBSERVE
            # =====================================
            
            logger.info("📸 Phase 1: OBSERVE - Analyzing current screen")
            initial_screen = analyze_current_screen()
            
            if initial_screen:
                logger.info(f"Current window: {initial_screen.window_title}")
                logger.info(f"Visible elements: {len(initial_screen.text_elements)}")
            
            # =====================================
            # PHASE 2: THINK
            # =====================================
            
            logger.info("🧠 Phase 2: THINK - Planning with AI")
            plan = plan_task(user_request)
            
            if not plan:
                return {
                    **result,
                    "status": "failed",
                    "error": "AI planner returned empty plan"
                }
            
            result["plan"] = plan
            logger.info(f"📋 Generated plan with {len(plan)} actions")
            
            # Save to memory
            self.memory.add_item({
                "type": "task_plan",
                "task": user_request,
                "plan": plan,
                "timestamp": datetime.now().isoformat()
            })
            
            # =====================================
            # PHASE 3: ACT
            # =====================================
            
            logger.info("⚡ Phase 3: ACT - Executing plan")
            execution_results = execute_plan(plan)
            result["execution_results"] = execution_results
            
            success_count = sum(1 for r in execution_results if r.get("success", False))
            logger.info(f"✅ Executed: {success_count}/{len(execution_results)} actions succeeded")
            
            # =====================================
            # PHASE 4: VERIFY
            # =====================================
            
            logger.info("✓ Phase 4: VERIFY - Checking results")
            final_screen = analyze_current_screen()
            
            # Simple verification: check if screen changed
            if initial_screen and final_screen:
                screen_changed = initial_screen.raw_text != final_screen.raw_text
                result["final_verification"] = screen_changed
                logger.info(f"Screen verification: {'✅ Changed' if screen_changed else '⚠️ No change'}")
            
            # =====================================
            # PHASE 5: RETRY IF NEEDED
            # =====================================
            
            failed_count = len(execution_results) - success_count
            
            if failed_count > 0 and self.max_retries > 0:
                logger.warning(f"⚠️ {failed_count} actions failed, attempting retry...")
                
                # Generate feedback for planner
                feedback = f"Failed actions: {[r['action'] for r in execution_results if not r.get('success', False)]}"
                
                # Try improved plan
                improved_plan = improve_plan(user_request, plan, feedback)
                
                if improved_plan and improved_plan != plan:
                    logger.info("🔄 Retrying with improved plan...")
                    self.max_retries -= 1
                    
                    # Execute improved plan
                    retry_results = execute_plan(improved_plan)
                    result["execution_results"].extend(retry_results)
                    
                    retry_success = sum(1 for r in retry_results if r.get("success", False))
                    logger.info(f"Retry result: {retry_success}/{len(retry_results)} succeeded")
            
            # =====================================
            # COMPLETION
            # =====================================
            
            result["status"] = "completed"
            logger.info("✅ Task execution complete")
            
            # Save to memory
            self.memory.add_item({
                "type": "task_execution",
                "task": user_request,
                "result": result,
                "timestamp": datetime.now().isoformat()
            })
            
            return result
        
        except Exception as e:
            logger.error(f"❌ Task error: {e}")
            result["status"] = "error"
            result["error"] = str(e)
            return result
    
    # ======================================
    # MEMORY ACCESS
    # ======================================
    
    def get_task_history(self, limit: int = 10) -> List[Dict]:
        """Get recent task history"""
        history = self.memory.search({"type": "task_execution"}, limit=limit)
        return history
    
    def get_context(self) -> Dict:
        """Get current context for agent"""
        return {
            "current_task": self.current_task,
            "execution_count": len(self.execution_history),
            "recent_tasks": self.get_task_history(5)
        }


# ======================================
# SINGLETON
# ======================================

agent = AutonomousAIAgent()


# ======================================
# ASYNC WRAPPER FOR FLASK
# ======================================

async def execute_autonomous_task(task_description: str) -> Dict:
    """Execute task - async wrapper for Flask"""
    return await agent.execute_task(task_description)


def execute_task_sync(task_description: str) -> Dict:
    """Execute task - sync wrapper for Flask"""
    import asyncio
    
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If loop is running (async context), run in thread
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as pool:
                future = pool.submit(asyncio.run, agent.execute_task(task_description))
                return future.result()
        else:
            # Otherwise, run directly
            return asyncio.run(agent.execute_task(task_description))
    except RuntimeError:
        # No event loop, create one
        return asyncio.run(agent.execute_task(task_description))
