"""
Autonomous AI Agent Loop
Core loop for autonomous computer control
Implements: Perceive → Plan → Act → Analyze → Repeat
"""
import logging
import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional

from ai_brain import get_ai
from planner_ai import get_planner
from executor import get_executor
from screen_understanding import get_screen_understanding
from task_state import (
    get_task_manager, TaskState, ActionRecord, ActionType, TaskStatus
)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# =========================
# AGENT LOOP
# =========================

class AutonomousAgent:
    """
    Autonomous AI Agent Loop
    Implements continuous perception, planning, and action
    """
    
    def __init__(self):
        self.ai = get_ai()
        self.planner = get_planner()
        self.executor = get_executor()
        self.screen = get_screen_understanding()
        self.task_manager = get_task_manager()
        
        # Configuration
        self.max_steps_per_task = 100
        self.debug_mode = True
        
        logger.info("AutonomousAgent initialized")
    
    def execute_autonomous_task(self, user_intent: str,
                               task_id: str = None,
                               context: str = "") -> Dict[str, Any]:
        """
        Execute a task autonomously
        
        Implements the main agent loop:
        1. Perceive - Analyze current screen
        2. Plan - Determine next action
        3. Act - Execute action
        4. Analyze - Check if complete
        5. Repeat
        
        Args:
            user_intent: What the user wants done
            task_id: Optional task ID (generated if None)
            context: Optional context about the task
            
        Returns:
            Dict with execution results
        """
        # Initialize task
        if task_id is None:
            task_id = f"task_{uuid.uuid4().hex[:8]}"
        
        task = self.task_manager.create_task(task_id, user_intent)
        task.start()
        
        logger.info(f"🤖 Starting autonomous task: {user_intent}")
        logger.info(f"Task ID: {task_id}")
        
        try:
            # Main agent loop
            while not task.is_complete():
                logger.info(f"\n{'='*60}")
                logger.info(f"Step {task.step_count + 1}/{self.max_steps_per_task}")
                logger.info(f"{'='*60}")
                
                # STEP 1: PERCEIVE - Analyze screen
                logger.info("📷 PERCEIVE: Analyzing current screen...")
                screen_state = self._perceive(task)
                
                if screen_state is None:
                    task.fail("Screen perception failed")
                    break
                
                # STEP 2: PLAN - Decide next action
                logger.info("🧠 PLAN: Determining next action...")
                next_action = self._plan(task, screen_state)
                
                if next_action is None:
                    logger.info("✅ Task appears complete or no action needed")
                    task.complete()
                    break
                
                logger.info(f"Action planned: {next_action['tool']} - {next_action.get('description', '')}")
                
                # STEP 3: ACT - Execute action
                logger.info("🎬 ACT: Executing action...")
                action_result = self._act(task, next_action, screen_state)
                
                if action_result['success']:
                    logger.info(f"✅ Action succeeded")
                else:
                    logger.warning(f"⚠️ Action failed: {action_result.get('error', 'Unknown error')}")
                    task.execution_errors += 1
                    
                    if not task.should_retry():
                        task.fail(f"Max retries exceeded: {action_result.get('error')}")
                        break
                
                # STEP 4: ANALYZE - Check result
                logger.info("🔍 ANALYZE: Analyzing action result...")
                analysis = self._analyze(task, action_result, screen_state)
                
                if analysis.get('task_complete'):
                    logger.info("✅ Task completed successfully!")
                    task.complete()
                    break
                
                if analysis.get('task_failed'):
                    task.fail(analysis.get('failure_reason', 'Task analysis indicated failure'))
                    break
                
                # Check step limit
                if task.step_count >= self.max_steps_per_task:
                    logger.warning("⚠️ Max steps reached, completing task")
                    task.complete()
                    break
            
            # Task finished
            result = task.get_execution_summary()
            logger.info(f"\n{'='*60}")
            logger.info(f"✅ Task finished: {task.status.value}")
            logger.info(f"Total steps: {task.step_count}")
            logger.info(f"Success rate: {result['actions_successful']}/{result['total_actions']}")
            logger.info(f"{'='*60}\n")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Agent loop error: {e}", exc_info=True)
            task.fail(f"Agent loop exception: {str(e)}")
            return task.get_execution_summary()
    
    def _perceive(self, task: TaskState) -> Optional[Dict[str, Any]]:
        """
        PERCEIVE: Analyze current screen state
        
        Returns:
            Screen state dict, or None on error
        """
        try:
            # Capture and analyze screen
            screen_state = self.screen.analyze_screen()
            
            if 'error' in screen_state:
                logger.error(f"Screen capture error: {screen_state['error']}")
                return None
            
            # Log what we see
            logger.info(f"Screen: {screen_state['screenshot_size']['width']}x{screen_state['screenshot_size']['height']}")
            logger.info(f"Elements visible: {screen_state['element_count']}")
            logger.info(f"Changed: {screen_state.get('changed', False)}")
            logger.info(f"Visible text: {screen_state['all_text'][:100]}...")
            
            return screen_state
            
        except Exception as e:
            logger.error(f"Perception error: {e}")
            return None
    
    def _plan(self, task: TaskState, screen_state: Dict) -> Optional[Dict[str, Any]]:
        """
        PLAN: Determine next action using LLM
        
        Returns:
            Action dict with tool and params, or None if done
        """
        try:
            # Build planning context
            context = f"""
Current Task: {task.user_intent}
Progress: {task.step_count} steps taken
Status: {task.status.value}

Current Screen:
{self.screen.describe_current_screen()}

Task Context:
{task.get_context_summary()}

What should happen next? Return a JSON action object with:
{{
    "tool": "click|type|navigate|wait|extract|open_app|command|scroll|drag",
    "params": {{}},
    "description": "what this action will do",
    "reasoning": "why we're doing this"
}}

If task is complete, return {{"action": "complete"}}
If task cannot continue, return {{"action": "failed", "reason": "..."}}
"""
            
            # Get AI planning decision
            response = self.ai.chat(context)
            
            # Parse response
            logger.debug(f"AI response: {response[:200]}...")
            
            # Try to extract JSON
            try:
                # Handle JSON in markdown code blocks
                if '```json' in response:
                    json_str = response.split('```json')[1].split('```')[0].strip()
                elif '```' in response:
                    json_str = response.split('```')[1].split('```')[0].strip()
                else:
                    json_str = response
                
                action = json.loads(json_str)
                
                # Check for completion
                if action.get('action') == 'complete':
                    logger.info("AI decided task is complete")
                    return None
                
                if action.get('action') == 'failed':
                    logger.warning(f"AI decided task failed: {action.get('reason')}")
                    return None
                
                return action
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse action JSON: {e}")
                logger.error(f"Response: {response}")
                return None
                
        except Exception as e:
            logger.error(f"Planning error: {e}")
            return None
    
    def _act(self, task: TaskState, action: Dict,
            screen_state: Dict) -> Dict[str, Any]:
        """
        ACT: Execute the planned action
        
        Returns:
            Action result dict
        """
        try:
            tool = action.get('tool', '').lower()
            params = action.get('params', {})
            description = action.get('description', f"Execute {tool}")
            
            logger.info(f"Executing: {tool} with params {params}")
            
            # Create action record
            action_record = ActionRecord(
                ActionType[tool.upper()] if tool.upper() in ActionType.__members__ else ActionType.COMMAND,
                description,
                params
            )
            action_record.screen_before = screen_state['all_text'][:500]
            
            # Execute based on tool type
            result = {'success': False, 'error': 'Unknown action'}
            
            if tool == 'click':
                result = self.executor.click(params.get('target', ''))
            elif tool == 'type':
                result = self.executor.type_text(params.get('text', ''))
            elif tool == 'navigate':
                result = self.executor.navigate(params.get('url', ''))
            elif tool == 'wait':
                result = self.executor.wait(params.get('seconds', 1))
            elif tool == 'screenshot':
                result = {'success': True, 'message': 'Screenshot captured'}
            elif tool == 'extract':
                result = {'success': True, 'data': screen_state.get('all_text', '')}
            elif tool == 'open_app':
                result = self.executor.open_application(params.get('app', ''))
            elif tool == 'scroll':
                result = self.executor.scroll(params.get('direction', 'down'), 
                                             params.get('amount', 3))
            elif tool == 'drag':
                result = self.executor.drag(params.get('from', {}), 
                                           params.get('to', {}))
            else:
                result = {'success': False, 'error': f'Unknown tool: {tool}'}
            
            # Update action record
            action_record.success = result.get('success', False)
            action_record.result = result
            action_record.error = result.get('error')
            
            # Record action
            task.record_action(action_record)
            
            return result
            
        except Exception as e:
            logger.error(f"Action execution error: {e}")
            return {'success': False, 'error': str(e)}
    
    def _analyze(self, task: TaskState, action_result: Dict,
                screen_state: Dict) -> Dict[str, Any]:
        """
        ANALYZE: Evaluate action result and decide next steps
        
        Returns:
            Analysis dict with completion status
        """
        try:
            # Get new screen state
            new_screen = self.screen.analyze_screen()
            
            if action_result.get('success'):
                task.add_screen_change(
                    screen_state['all_text'],
                    new_screen['all_text'],
                    'action_result'
                )
            
            # Build analysis context
            analysis_prompt = f"""
Task: {task.user_intent}
Action performed: {task.current_action.description if task.current_action else 'None'}
Action successful: {action_result.get('success', False)}

Screen changed: {new_screen.get('changed', False)}

Previous visible text:
{screen_state['all_text'][:200]}

Current visible text:
{new_screen['all_text'][:200]}

Did we make progress towards: {task.user_intent}?
Is the task complete?

Respond with JSON:
{{
    "task_complete": true/false,
    "task_failed": true/false,
    "failure_reason": "if failed",
    "progress": "description of progress",
    "confidence": 0-1
}}
"""
            
            response = self.ai.chat(analysis_prompt)
            
            # Parse analysis
            try:
                if '```json' in response:
                    json_str = response.split('```json')[1].split('```')[0].strip()
                elif '```' in response:
                    json_str = response.split('```')[1].split('```')[0].strip()
                else:
                    json_str = response
                
                analysis = json.loads(json_str)
                logger.info(f"Analysis: {analysis.get('progress', 'No progress info')}")
                
                return analysis
                
            except json.JSONDecodeError:
                logger.warning("Could not parse analysis JSON, assuming task continues")
                return {'task_complete': False, 'task_failed': False}
                
        except Exception as e:
            logger.error(f"Analysis error: {e}")
            return {'task_complete': False, 'task_failed': False}


# =========================
# SINGLETON INSTANCE
# =========================

_agent = None

def get_autonomous_agent() -> AutonomousAgent:
    """Get or create agent instance"""
    global _agent
    if _agent is None:
        _agent = AutonomousAgent()
    return _agent
