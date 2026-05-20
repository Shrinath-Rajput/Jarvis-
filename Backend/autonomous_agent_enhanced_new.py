# -*- coding: utf-8 -*-
"""
AUTONOMOUS AI AGENT - TRULY INTELLIGENT
NO HARDCODED LOGIC

Implements full OBSERVE → THINK → ACT → VERIFY cycle
"""

import asyncio
import logging
import json
from typing import Dict, List, Optional

try:
    from planner_ai import plan_task, improve_plan, get_planner
    PLANNER_AVAILABLE = True
except:
    PLANNER_AVAILABLE = False

try:
    from executor_universal import execute_plan, get_executor
    EXECUTOR_AVAILABLE = True
except:
    EXECUTOR_AVAILABLE = False

try:
    from screen_understanding_enhanced import get_screen_reader
    SCREEN_READER_AVAILABLE = True
except:
    SCREEN_READER_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ======================================
# AUTONOMOUS AGENT
# ======================================

class AutonomousAgent:
    """
    TRULY autonomous AI agent.
    No hardcoding. Pure LLM-driven reasoning.
    Implements OTAV: Observe → Think → Act → Verify
    """
    
    def __init__(self):
        self.planner = get_planner() if PLANNER_AVAILABLE else None
        self.executor = get_executor() if EXECUTOR_AVAILABLE else None
        self.screen_reader = get_screen_reader() if SCREEN_READER_AVAILABLE else None
        
        self.current_task = None
        self.execution_history = []
        self.max_retries = 3
        
        logger.info("🤖 Autonomous Agent initialized")
        
        if not PLANNER_AVAILABLE:
            logger.error("❌ Planner not available")
        if not EXECUTOR_AVAILABLE:
            logger.error("❌ Executor not available")
    
    async def execute_task(self, task_description: str) -> Dict:
        """
        Execute ANY user task dynamically
        OBSERVE → THINK → ACT → VERIFY
        """
        
        self.current_task = task_description
        logger.info(f"🎯 Task: {task_description}")
        
        try:
            # PHASE 1: OBSERVE (Take screenshot for context)
            logger.info("👁️ PHASE 1: OBSERVE")
            observation = self._observe()
            
            # PHASE 2: THINK (Generate plan using LLM)
            logger.info("🧠 PHASE 2: THINK")
            plan = self._think(task_description, observation)
            
            if not plan:
                return {
                    "status": "failed",
                    "task": task_description,
                    "reason": "Could not generate plan",
                    "phases": {
                        "observe": observation,
                        "think": {"plan": None}
                    }
                }
            
            # PHASE 3: ACT (Execute plan)
            logger.info("⚡ PHASE 3: ACT")
            execution_result = self._act(plan)
            
            # PHASE 4: VERIFY (Check if task succeeded)
            logger.info("✔️ PHASE 4: VERIFY")
            verification = self._verify(execution_result, task_description)
            
            # Store in history
            self.execution_history.append({
                "task": task_description,
                "observation": observation,
                "plan": plan,
                "execution": execution_result,
                "verification": verification
            })
            
            return {
                "status": "completed",
                "task": task_description,
                "successful_actions": execution_result.get("successful", 0),
                "total_actions": execution_result.get("total_actions", 0),
                "verified": verification.get("success", False),
                "phases": {
                    "observe": observation,
                    "think": {"actions": len(plan)},
                    "act": execution_result,
                    "verify": verification
                }
            }
        
        except Exception as e:
            logger.error(f"❌ Task failed: {e}")
            return {
                "status": "error",
                "task": task_description,
                "error": str(e)
            }
    
    def _observe(self) -> Dict:
        """OBSERVE: Analyze current screen state"""
        
        try:
            if not self.screen_reader:
                logger.warning("Screen reader not available")
                return {"observation": "Screen reader unavailable"}
            
            # Take screenshot
            screenshot_path = self.screen_reader.take_screenshot()
            
            # Analyze screen
            screen_state = self.screen_reader.analyze_screen()
            
            observation = {
                "screenshot": screenshot_path,
                "window_title": screen_state.window_title if screen_state else None,
                "visible_text": screen_state.raw_text[:500] if screen_state else "",
                "text_elements": len(screen_state.text_elements) if screen_state else 0
            }
            
            logger.info(f"✅ Observed: {observation['text_elements']} text elements")
            return observation
        
        except Exception as e:
            logger.error(f"Observation error: {e}")
            return {"error": str(e)}
    
    def _think(self, task: str, observation: Dict) -> List[Dict]:
        """THINK: Generate action plan using LLM"""
        
        try:
            if not self.planner:
                logger.error("Planner not available")
                return []
            
            # Add context from previous actions
            context = None
            if self.execution_history:
                context = [h["task"] for h in self.execution_history[-5:]]
            
            # Generate plan
            plan = self.planner.plan_task(task, context)
            
            if plan:
                logger.info(f"✅ Generated plan: {len(plan)} actions")
                return plan
            else:
                logger.error("Plan generation failed")
                return []
        
        except Exception as e:
            logger.error(f"Think error: {e}")
            return []
    
    def _act(self, plan: List[Dict]) -> Dict:
        """ACT: Execute action plan"""
        
        try:
            if not self.executor:
                logger.error("Executor not available")
                return {"status": "failed", "error": "Executor unavailable"}
            
            # Execute plan
            result = self.executor.execute_plan(plan, max_retries=self.max_retries)
            
            logger.info(f"✅ Executed: {result.get('successful', 0)}/{result.get('total_actions', 0)} actions")
            return result
        
        except Exception as e:
            logger.error(f"Act error: {e}")
            return {"status": "failed", "error": str(e)}
    
    def _verify(self, execution_result: Dict, task: str) -> Dict:
        """VERIFY: Check if task succeeded"""
        
        try:
            successful = execution_result.get("successful", 0)
            total = execution_result.get("total_actions", 0)
            
            # Consider successful if most actions succeeded
            if total == 0:
                success = False
                reason = "No actions executed"
            elif successful >= (total * 0.8):  # 80% threshold
                success = True
                reason = f"Task completed successfully"
            else:
                success = False
                reason = f"Only {successful}/{total} actions succeeded"
            
            verification = {
                "success": success,
                "reason": reason,
                "percentage": (successful / total * 100) if total > 0 else 0
            }
            
            logger.info(f"✅ Verification: {verification['reason']}")
            return verification
        
        except Exception as e:
            logger.error(f"Verification error: {e}")
            return {"success": False, "reason": str(e)}
    
    def retry_task(self, feedback: str) -> Dict:
        """Retry current task with feedback"""
        
        if not self.current_task:
            return {"status": "failed", "error": "No task to retry"}
        
        try:
            logger.info(f"🔄 Retrying with feedback: {feedback}")
            
            # Get last plan
            if self.execution_history:
                last_plan = self.execution_history[-1]["plan"]
            else:
                last_plan = []
            
            # Improve plan based on feedback
            improved_plan = self.planner.improve_plan(
                self.current_task,
                last_plan,
                feedback
            )
            
            if improved_plan:
                # Execute improved plan
                execution_result = self._act(improved_plan)
                verification = self._verify(execution_result, self.current_task)
                
                return {
                    "status": "retry_completed",
                    "improved_plan_actions": len(improved_plan),
                    "execution": execution_result,
                    "verification": verification
                }
            else:
                return {"status": "failed", "error": "Could not improve plan"}
        
        except Exception as e:
            logger.error(f"Retry error: {e}")
            return {"status": "failed", "error": str(e)}
    
    def get_history(self, limit: int = 10) -> List[Dict]:
        """Get execution history"""
        return self.execution_history[-limit:]


# ======================================
# GLOBAL AGENT INSTANCE
# ======================================

_agent = None

def get_agent() -> AutonomousAgent:
    """Get agent singleton"""
    global _agent
    if _agent is None:
        _agent = AutonomousAgent()
    return _agent

async def execute_task(task: str) -> Dict:
    """Execute task using autonomous agent"""
    agent = get_agent()
    return await agent.execute_task(task)

def execute_task_sync(task: str) -> Dict:
    """Synchronous wrapper for task execution"""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # Already in async context
            return asyncio.create_task(execute_task(task))
        else:
            return asyncio.run(execute_task(task))
    except RuntimeError:
        # Create new loop
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        try:
            return new_loop.run_until_complete(execute_task(task))
        finally:
            new_loop.close()

def retry_task(feedback: str) -> Dict:
    """Retry with feedback"""
    agent = get_agent()
    return agent.retry_task(feedback)

def get_execution_history() -> List[Dict]:
    """Get execution history"""
    agent = get_agent()
    return agent.get_history()
