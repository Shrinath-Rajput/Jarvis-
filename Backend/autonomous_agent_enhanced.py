"""
Enhanced Autonomous Agent Loop
True autonomous AI agent with dynamic tool selection and vision-based state understanding
Removes hardcoded logic and implements pure LLM-driven decision making

Implements: Perceive → Analyze → Plan → Act → Learn → Repeat
"""
import logging
import json
import uuid
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

from ai_brain import get_ai
from screen_understanding import get_screen_understanding
from task_state import get_task_manager, TaskState, TaskStatus
from tool_registry import get_tool_registry, ToolRegistry
from tool_implementations import register_all_tools

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class VisionContext:
    """
    Holds current vision/screen context
    Used to make intelligent decisions based on what's on screen
    """
    
    def __init__(self):
        self.current_screen = None
        self.screen_description = ""
        self.visible_elements = []
        self.text_on_screen = ""
        self.last_action_success = None
        self.error_on_screen = None
        self.changed_regions = []
    
    def to_dict(self) -> Dict:
        return {
            "description": self.screen_description,
            "text": self.text_on_screen[:500],  # Truncate for context
            "visible_elements": len(self.visible_elements),
            "last_action": self.last_action_success,
            "error_detected": self.error_on_screen is not None,
            "changed": len(self.changed_regions) > 0
        }


class EnhancedAutonomousAgent:
    """
    Enhanced Autonomous AI Agent
    - Dynamic tool selection without hardcoded logic
    - Vision-based decision making
    - Continuous learning and adaptation
    - Proper error handling and recovery
    """
    
    def __init__(self, use_local_llm: bool = True):
        logger.info("🤖 Initializing Enhanced Autonomous Agent...")
        
        self.ai = get_ai()
        self.screen = get_screen_understanding()
        self.task_manager = get_task_manager()
        self.tool_registry: ToolRegistry = register_all_tools()
        
        # Configuration
        self.max_steps_per_task = 150
        self.max_retries_per_action = 3
        self.use_local_llm = use_local_llm
        self.vision_context = VisionContext()
        
        # Memory and state
        self.action_history: List[Dict] = []
        self.decision_history: List[Dict] = []
        
        logger.info("✅ Agent initialized with dynamic tool registry")
        logger.info(f"📦 {len(self.tool_registry.get_all_tools())} tools available")
    
    async def execute_autonomous_task(self, user_intent: str, 
                                     task_id: str = None,
                                     max_steps: int = None) -> Dict[str, Any]:
        """
        Execute a task fully autonomously using AI decision making
        
        Flow:
        1. PERCEIVE - Understand current state
        2. ANALYZE - Check for errors/completeness
        3. PLAN - Use LLM to decide next action with dynamic tool selection
        4. ACT - Execute the chosen tool
        5. LEARN - Update knowledge and memory
        6. REPEAT - Continue until done or max steps
        
        Args:
            user_intent: What the user wants done
            task_id: Optional task identifier
            max_steps: Override max steps for this task
        
        Returns:
            Execution summary with results
        """
        # Initialize
        if task_id is None:
            task_id = f"task_{uuid.uuid4().hex[:8]}"
        
        if max_steps:
            self.max_steps_per_task = max_steps
        
        task = self.task_manager.create_task(task_id, user_intent)
        task.start()
        
        logger.info("\n" + "="*70)
        logger.info(f"🚀 AUTONOMOUS TASK EXECUTION STARTED")
        logger.info("="*70)
        logger.info(f"Task ID: {task_id}")
        logger.info(f"Objective: {user_intent}")
        logger.info(f"Max steps: {self.max_steps_per_task}")
        logger.info("="*70 + "\n")
        
        try:
            # Main autonomous loop
            while not task.is_complete() and task.step_count < self.max_steps_per_task:
                step_num = task.step_count + 1
                
                logger.info(f"\n{'─'*70}")
                logger.info(f"STEP {step_num}/{self.max_steps_per_task}")
                logger.info(f"{'─'*70}")
                
                # STEP 1: PERCEIVE - Analyze screen
                if not await self._perceive(task):
                    logger.error("❌ Perception failed")
                    task.fail("Perception system error")
                    break
                
                # STEP 2: ANALYZE - Check completion and errors
                analysis = await self._analyze(task)
                if analysis['task_complete']:
                    logger.info("✅ Task completion detected!")
                    task.complete()
                    break
                
                if analysis['task_failed']:
                    logger.error(f"❌ Task failure detected: {analysis.get('reason')}")
                    task.fail(analysis.get('reason', 'Task analysis indicated failure'))
                    break
                
                # STEP 3: PLAN - Use LLM to decide next action
                action_plan = await self._plan(task, analysis)
                if not action_plan:
                    logger.warning("⚠️ No action planned, task may be complete")
                    task.complete()
                    break
                
                logger.info(f"📋 PLANNED ACTION:")
                logger.info(f"   Tool: {action_plan.get('tool')}")
                logger.info(f"   Reason: {action_plan.get('reasoning')}")
                
                # STEP 4: ACT - Execute the planned action
                action_result = await self._act(task, action_plan)
                if not action_result['success']:
                    logger.warning(f"⚠️ Action failed: {action_result.get('error')}")
                    task.execution_errors += 1
                    
                    if not task.should_retry():
                        logger.error("❌ Max retries exceeded")
                        task.fail(f"Action failed too many times: {action_result.get('error')}")
                        break
                    
                    logger.info("🔄 Will retry on next step")
                    continue
                
                logger.info(f"✅ Action succeeded")
                
                # STEP 5: LEARN - Update our knowledge
                await self._learn(task, action_plan, action_result)
                
                # Increment step counter
                task.increment_step()
            
            # Task completed
            summary = task.get_execution_summary()
            
            logger.info("\n" + "="*70)
            logger.info("🎉 TASK EXECUTION COMPLETED")
            logger.info("="*70)
            logger.info(f"Status: {task.status.value}")
            logger.info(f"Total steps: {task.step_count}")
            logger.info(f"Success rate: {summary['actions_successful']}/{summary['total_actions']}")
            logger.info(f"Errors: {task.execution_errors}")
            logger.info("="*70 + "\n")
            
            return summary
            
        except Exception as e:
            logger.error(f"❌ Agent loop exception: {str(e)}", exc_info=True)
            task.fail(f"Agent exception: {str(e)}")
            return task.get_execution_summary()
    
    async def _perceive(self, task: TaskState) -> bool:
        """
        PERCEIVE: Understand current screen state
        Updates vision context with current screen analysis
        
        Returns:
            True if perception successful, False otherwise
        """
        logger.info("📷 PERCEIVING: Analyzing screen state...")
        
        try:
            # Capture and analyze screen
            screen_state = self.screen.analyze_screen()
            
            if 'error' in screen_state:
                logger.error(f"Screen capture error: {screen_state['error']}")
                return False
            
            # Update vision context
            self.vision_context.current_screen = screen_state
            self.vision_context.screen_description = screen_state.get('description', '')
            self.vision_context.text_on_screen = screen_state.get('all_text', '')
            self.vision_context.visible_elements = screen_state.get('elements', [])
            
            # Log perception results
            resolution = screen_state.get('screenshot_size', {})
            logger.info(f"   Resolution: {resolution.get('width')}x{resolution.get('height')}")
            logger.info(f"   Elements visible: {len(self.vision_context.visible_elements)}")
            logger.info(f"   Text detected: {len(self.vision_context.text_on_screen)} chars")
            
            # Check for error dialogs or messages
            if self._detect_error_on_screen():
                logger.warning("   ⚠️ Error detected on screen")
                self.vision_context.error_on_screen = self._extract_error_message()
            
            return True
            
        except Exception as e:
            logger.error(f"   ❌ Perception error: {e}")
            return False
    
    async def _analyze(self, task: TaskState) -> Dict[str, Any]:
        """
        ANALYZE: Check if task is complete or failed
        Uses vision context and task history
        
        Returns:
            Analysis dict with completion and error info
        """
        logger.info("🔍 ANALYZING: Checking task progress...")
        
        analysis = {
            'task_complete': False,
            'task_failed': False,
            'reason': None,
            'vision_state': self.vision_context.to_dict()
        }
        
        try:
            # Check if screen indicates task completion
            text_on_screen = self.vision_context.text_on_screen.lower()
            
            # Common completion indicators
            completion_phrases = [
                'success', 'completed', 'done', 'finished',
                'thank you', 'operation complete', 'saved',
                'downloaded', 'created', 'uploaded'
            ]
            
            for phrase in completion_phrases:
                if phrase in text_on_screen:
                    logger.info(f"   ✅ Detected completion phrase: '{phrase}'")
                    analysis['task_complete'] = True
                    break
            
            # Check for failure indicators
            failure_phrases = [
                'error', 'failed', 'failed to', "couldn't", 'cannot',
                'not found', 'invalid', 'access denied', 'permission'
            ]
            
            for phrase in failure_phrases:
                if phrase in text_on_screen:
                    if self.vision_context.error_on_screen:
                        logger.warning(f"   ❌ Detected failure phrase: '{phrase}'")
                        analysis['task_failed'] = True
                        analysis['reason'] = self.vision_context.error_on_screen
                        break
            
            # Use LLM to analyze current state against task intent
            if not analysis['task_complete'] and not analysis['task_failed']:
                llm_analysis = await self._llm_analyze_state(task)
                if llm_analysis:
                    analysis.update(llm_analysis)
            
            logger.info(f"   Complete: {analysis['task_complete']}, Failed: {analysis['task_failed']}")
            return analysis
            
        except Exception as e:
            logger.error(f"   ❌ Analysis error: {e}")
            return analysis
    
    async def _plan(self, task: TaskState, analysis: Dict) -> Optional[Dict[str, Any]]:
        """
        PLAN: Use LLM to decide next action
        Uses dynamic tool selection - no hardcoded logic
        
        Returns:
            Action dict with tool and parameters, or None if done
        """
        logger.info("🧠 PLANNING: Determining next action...")
        
        try:
            # Build comprehensive context for LLM
            tools_available = self.tool_registry.get_tools_for_llm()
            
            context = f"""
You are an autonomous AI agent controlling a computer to complete tasks.

CURRENT TASK:
{task.user_intent}

PROGRESS: {task.step_count} steps taken

CURRENT SCREEN STATE:
{json.dumps(self.vision_context.to_dict(), indent=2)}

VISIBLE TEXT:
{self.vision_context.text_on_screen[:300]}

AVAILABLE TOOLS:
{tools_available}

PREVIOUS ACTIONS:
{json.dumps([a['tool'] for a in self.action_history[-3:]], indent=2)}

YOUR JOB:
Based on the current screen and task, decide the NEXT SINGLE ACTION to take.
Choose from the available tools above. Be specific and practical.

If the task appears to be complete, respond with: {{"tool": "complete", "reasoning": "reason"}}
If the task appears impossible, respond with: {{"tool": "failed", "reasoning": "reason"}}

Otherwise, respond with a JSON object containing:
{{
    "tool": "exact_tool_name",
    "parameters": {{"param1": value1, "param2": value2}},
    "reasoning": "why this action helps complete the task"
}}
"""
            
            # Get LLM decision
            response = await self._query_llm(context)
            
            if not response:
                logger.warning("   ⚠️ LLM returned no response")
                return None
            
            # Parse response
            try:
                action = json.loads(response)
            except json.JSONDecodeError:
                logger.warning(f"   ⚠️ Could not parse LLM response: {response[:100]}")
                # Try to extract JSON from response
                action = self._extract_json_from_text(response)
                if not action:
                    return None
            
            # Handle completion signals
            if action.get('tool') == 'complete':
                logger.info(f"   ✅ LLM decided task is complete: {action.get('reasoning')}")
                return None
            
            if action.get('tool') == 'failed':
                logger.warning(f"   ❌ LLM detected task failure: {action.get('reasoning')}")
                return None
            
            # Verify tool exists
            tool_name = action.get('tool')
            if not self.tool_registry.get_tool(tool_name):
                logger.warning(f"   ⚠️ Tool '{tool_name}' not found, using fallback")
                # Try to find similar tool
                similar = self.tool_registry.search_tools(tool_name)
                if similar:
                    action['tool'] = similar[0].name
                    logger.info(f"   📌 Using similar tool: {action['tool']}")
                else:
                    return None
            
            logger.info(f"   ✅ Planned action: {action['tool']}")
            return action
            
        except Exception as e:
            logger.error(f"   ❌ Planning error: {e}")
            return None
    
    async def _act(self, task: TaskState, action_plan: Dict) -> Dict[str, Any]:
        """
        ACT: Execute the planned action
        Uses tool registry for execution
        
        Returns:
            Execution result
        """
        logger.info("🎬 ACTING: Executing action...")
        
        try:
            tool_name = action_plan.get('tool')
            parameters = action_plan.get('parameters', {})
            
            logger.info(f"   Tool: {tool_name}")
            logger.info(f"   Params: {parameters}")
            
            # Execute tool
            result = await self.tool_registry.execute_tool(tool_name, **parameters)
            
            # Record in history
            self.action_history.append({
                'step': task.step_count,
                'tool': tool_name,
                'parameters': parameters,
                'success': result['success'],
                'timestamp': datetime.now().isoformat()
            })
            
            if result['success']:
                logger.info(f"   ✅ Action succeeded")
                self.vision_context.last_action_success = True
            else:
                logger.warning(f"   ❌ Action failed: {result.get('error')}")
                self.vision_context.last_action_success = False
            
            return result
            
        except Exception as e:
            logger.error(f"   ❌ Execution error: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def _learn(self, task: TaskState, action_plan: Dict, result: Dict) -> None:
        """
        LEARN: Update knowledge and improve future decisions
        Stores action outcomes for learning
        """
        try:
            self.decision_history.append({
                'step': task.step_count,
                'action': action_plan.get('tool'),
                'success': result['success'],
                'time': datetime.now().isoformat()
            })
            
            # Could implement reinforcement learning here
            # For now, just tracking for analysis
            
        except Exception as e:
            logger.error(f"Learning error: {e}")
    
    # ========================
    # HELPER METHODS
    # ========================
    
    async def _query_llm(self, context: str) -> Optional[str]:
        """Query the LLM for decision making"""
        try:
            # Use configured LLM
            response = await self.ai.generate_response(context)
            return response
        except Exception as e:
            logger.error(f"LLM query error: {e}")
            return None
    
    async def _llm_analyze_state(self, task: TaskState) -> Dict:
        """Use LLM to analyze if task is complete"""
        try:
            analysis_prompt = f"""
Given this task: {task.user_intent}
And current screen text: {self.vision_context.text_on_screen[:200]}

Has the task been completed? Respond with JSON:
{{"task_complete": true/false, "reasoning": "brief reason"}}
"""
            response = await self._query_llm(analysis_prompt)
            if response:
                return json.loads(response)
        except Exception as e:
            logger.error(f"State analysis error: {e}")
        
        return {}
    
    def _detect_error_on_screen(self) -> bool:
        """Check if error dialog is visible"""
        text = self.vision_context.text_on_screen.lower()
        error_keywords = ['error', 'failed', 'exception', 'alert', 'warning']
        return any(keyword in text for keyword in error_keywords)
    
    def _extract_error_message(self) -> str:
        """Extract error message from screen"""
        # Find lines containing error keywords
        lines = self.vision_context.text_on_screen.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['error', 'failed']):
                return line.strip()
        return "Unknown error"
    
    def _extract_json_from_text(self, text: str) -> Optional[Dict]:
        """Extract JSON object from text"""
        try:
            start = text.find('{')
            end = text.rfind('}') + 1
            if start >= 0 and end > start:
                return json.loads(text[start:end])
        except:
            pass
        return None


# Global instance
_agent: Optional[EnhancedAutonomousAgent] = None


def get_autonomous_agent() -> EnhancedAutonomousAgent:
    """Get or create the global autonomous agent"""
    global _agent
    if _agent is None:
        _agent = EnhancedAutonomousAgent()
    return _agent


# Quick test
if __name__ == "__main__":
    import asyncio
    
    async def test():
        agent = get_autonomous_agent()
        result = await agent.execute_autonomous_task(
            "Open Google and search for 'Python autonomous agents'"
        )
        print("\nExecution Result:")
        print(json.dumps(result, indent=2))
    
    asyncio.run(test())
