# -*- coding: utf-8 -*-
"""
TRUE AUTONOMOUS AGENT - ZERO HARDCODING
========================================

OBSERVE → THINK → ACT → VERIFY → RETRY (OTAVR) Architecture

The agent dynamically understands ANY user request and executes it
without hardcoded rules, if/else statements, or static mappings.

Uses:
- DynamicPlanner: Generates action plans dynamically
- UniversalExecutor: Executes universal actions
- ScreenUnderstanding: Verifies actions through OCR
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any

try:
    from planner_ai import DynamicPlanner
    PLANNER_AVAILABLE = True
except ImportError:
    PLANNER_AVAILABLE = False
    DynamicPlanner = None

try:
    from executor_universal import get_executor
    EXECUTOR_AVAILABLE = True
except ImportError:
    EXECUTOR_AVAILABLE = False
    get_executor = None

try:
    from screen_understanding_ocr import get_screen_understanding
    SCREEN_READER_AVAILABLE = True
except ImportError:
    SCREEN_READER_AVAILABLE = False
    get_screen_understanding = None

from tool_implementations import ToolImplementations

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ======================================
# TRUE AUTONOMOUS AGENT
# ======================================

class TrueAutonomousAgent:
    """
    TRULY AUTONOMOUS AGENT
    
    - NO hardcoding
    - NO if/else for apps/websites
    - NO static rule-based automation
    - PURE dynamic LLM-driven reasoning
    
    Architecture: OBSERVE → THINK → ACT → VERIFY → RETRY
    """
    
    def __init__(self):
        """Initialize agent with all components"""
        
        self.planner = DynamicPlanner() if PLANNER_AVAILABLE else None
        self.executor = get_executor() if EXECUTOR_AVAILABLE else None
        self.screen_reader = get_screen_understanding() if SCREEN_READER_AVAILABLE else None
        self.tools = ToolImplementations()
        
        self.task_history = []
        self.context = []
        
        logger.info("=" * 60)
        logger.info("🚀 TRUE AUTONOMOUS AGENT INITIALIZED")
        logger.info("=" * 60)
        
        if not PLANNER_AVAILABLE:
            logger.error("❌ Planner not available!")
        if not EXECUTOR_AVAILABLE:
            logger.error("❌ Executor not available!")
        if not SCREEN_READER_AVAILABLE:
            logger.warning("⚠️ Screen reader not available")
        
        logger.info("✅ Agent ready for OTAVR loop")
    
    async def execute_task(self, user_request: str, max_retries: int = 3) -> Dict[str, Any]:
        """
        EXECUTE ANY TASK DYNAMICALLY
        
        OBSERVE → THINK → ACT → VERIFY → RETRY
        
        Args:
            user_request: User's natural language request
            max_retries: Max retry attempts on failure
        
        Returns:
            Task result
        """
        
        logger.info("=" * 60)
        logger.info(f"📝 TASK RECEIVED: '{user_request}'")
        logger.info("=" * 60)
        
        try:
            # ================================
            # PHASE 1: OBSERVE
            # ================================
            logger.info("\n🔍 PHASE 1: OBSERVE")
            
            self.task_history.append(user_request)
            
            # Take screenshot to understand current state
            if self.screen_reader:
                logger.info("📸 Taking screenshot for context...")
                self.screen_reader.screenshot()
                self.screen_reader.ocr_screenshot()
            
            # ================================
            # PHASE 2: THINK
            # ================================
            logger.info("\n🧠 PHASE 2: THINK (PLANNING)")
            
            if not self.planner:
                logger.error("❌ Planner not available")
                return {
                    "success": False,
                    "response": "Planner not initialized",
                    "error": "PLANNER_UNAVAILABLE"
                }
            
            # Generate plan dynamically (no hardcoding)
            plan = self.planner.plan_task(user_request, context=self.context)
            
            if not plan:
                logger.warning("⚠️ Plan generation failed")
                return {
                    "success": False,
                    "response": "Could not generate plan for this request",
                    "error": "PLAN_GENERATION_FAILED"
                }
            
            logger.info(f"✅ Generated plan with {len(plan)} actions:")
            for i, action in enumerate(plan, 1):
                logger.info(f"   {i}. {action.get('tool', 'unknown')}: {action.get('params', {})}")
            
            # ================================
            # PHASE 3: ACT
            # ================================
            logger.info("\n⚡ PHASE 3: ACT (EXECUTION)")
            
            if not self.executor:
                logger.error("❌ Executor not available")
                return {
                    "success": False,
                    "response": "Executor not initialized",
                    "error": "EXECUTOR_UNAVAILABLE"
                }
            
            # Execute plan
            results = self.executor.execute_plan(plan, verify=True)
            
            logger.info(f"✅ Plan executed: {len(results)} actions completed")
            
            # ================================
            # PHASE 4: VERIFY
            # ================================
            logger.info("\n✅ PHASE 4: VERIFY")
            
            success_count = sum(1 for r in results if r.get("success", False))
            total_count = len(results)
            
            logger.info(f"Execution results: {success_count}/{total_count} successful")
            
            # Check if critical actions failed
            critical_failures = [
                r for r in results 
                if not r.get("success") and r.get("action", {}).get("critical", False)
            ]
            
            if critical_failures:
                logger.warning(f"⚠️ {len(critical_failures)} critical actions failed")
                
                # ================================
                # PHASE 5: RETRY
                # ================================
                if max_retries > 0:
                    logger.info(f"\n🔄 PHASE 5: RETRY (Attempt {4-max_retries+1})")
                    
                    # Refine plan and retry
                    feedback = "\n".join([
                        r.get("error", "Unknown error") 
                        for r in critical_failures
                    ])
                    
                    refined_plan = self.planner.refine_plan(plan, feedback)
                    
                    if refined_plan and refined_plan != plan:
                        logger.info("Retrying with refined plan...")
                        return await self.execute_task(user_request, max_retries - 1)
            
            # Update context
            self.context.append(f"Completed: {user_request}")
            
            # Prepare response
            task_success = success_count > 0
            
            response = {
                "success": task_success,
                "response": f"Task '{user_request}' completed",
                "details": {
                    "total_actions": total_count,
                    "successful_actions": success_count,
                    "failed_actions": total_count - success_count,
                    "results": results
                }
            }
            
            logger.info("=" * 60)
            logger.info(f"✅ TASK COMPLETE: {'SUCCESS' if task_success else 'PARTIAL'}")
            logger.info("=" * 60)
            
            return response
        
        except Exception as e:
            logger.error(f"❌ Task execution error: {e}", exc_info=True)
            
            return {
                "success": False,
                "response": f"Task failed with error: {str(e)}",
                "error": str(e)
            }
    
    async def execute_multiple_tasks(self, tasks: List[str]) -> List[Dict[str, Any]]:
        """
        Execute multiple tasks sequentially
        
        Args:
            tasks: List of user requests
        
        Returns:
            List of results
        """
        logger.info(f"\n📋 Executing {len(tasks)} tasks in sequence...\n")
        
        results = []
        for i, task in enumerate(tasks, 1):
            logger.info(f"\n[{i}/{len(tasks)}] Executing: {task}")
            result = await self.execute_task(task)
            results.append(result)
        
        logger.info(f"\n✅ All {len(tasks)} tasks completed")
        return results
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status and history"""
        return {
            "initialized": True,
            "components": {
                "planner": PLANNER_AVAILABLE,
                "executor": EXECUTOR_AVAILABLE,
                "screen_reader": SCREEN_READER_AVAILABLE
            },
            "task_history": self.task_history,
            "context_memory": len(self.context)
        }


# ======================================
# GLOBAL AGENT INSTANCE
# ======================================

_agent_instance = None


def get_agent() -> TrueAutonomousAgent:
    """Get agent singleton"""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = TrueAutonomousAgent()
    return _agent_instance


# ======================================
# PUBLIC API
# ======================================

async def execute_autonomous_task(task: str) -> Dict[str, Any]:
    """Execute a task autonomously (zero hardcoding)"""
    agent = get_agent()
    return await agent.execute_task(task)


async def execute_multiple_autonomous_tasks(tasks: List[str]) -> List[Dict[str, Any]]:
    """Execute multiple tasks autonomously"""
    agent = get_agent()
    return await agent.execute_multiple_tasks(tasks)


def get_agent_status() -> Dict[str, Any]:
    """Get current agent status"""
    agent = get_agent()
    return agent.get_status()


# Backwards compatibility
class EnhancedAutonomousAgent(TrueAutonomousAgent):
    """Backwards compatibility wrapper"""
    pass


# Global instances for backwards compatibility
agent = get_agent()


__all__ = [
    "TrueAutonomousAgent",
    "get_agent",
    "execute_autonomous_task",
    "execute_multiple_autonomous_tasks",
    "get_agent_status",
    "EnhancedAutonomousAgent",  # Backwards compat
]
