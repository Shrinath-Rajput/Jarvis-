"""
Task State Management
Tracks autonomous task execution state and context
"""
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from enum import Enum

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# =========================
# TASK STATE ENUMS
# =========================

class TaskStatus(Enum):
    """Task execution status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"
    CANCELLED = "cancelled"


class ActionType(Enum):
    """Types of actions"""
    CLICK = "click"
    TYPE = "type"
    NAVIGATE = "navigate"
    SCREENSHOT = "screenshot"
    WAIT = "wait"
    EXTRACT = "extract"
    OPEN_APP = "open_app"
    COMMAND = "command"
    SCROLL = "scroll"
    DRAG = "drag"


# =========================
# ACTION EXECUTION RECORD
# =========================

class ActionRecord:
    """Record of a single action execution"""
    
    def __init__(self, action_type: ActionType, description: str,
                 params: Dict[str, Any]):
        self.action_type = action_type
        self.description = description
        self.params = params
        self.timestamp = datetime.now()
        self.duration = 0
        self.success = False
        self.result = None
        self.error = None
        self.screen_before = None
        self.screen_after = None
    
    def to_dict(self) -> Dict:
        return {
            'action_type': self.action_type.value,
            'description': self.description,
            'params': self.params,
            'timestamp': self.timestamp.isoformat(),
            'duration': self.duration,
            'success': self.success,
            'result': self.result,
            'error': self.error,
            'screen_before': self.screen_before,
            'screen_after': self.screen_after
        }


# =========================
# TASK STATE
# =========================

class TaskState:
    """Manages the state of a single autonomous task"""
    
    def __init__(self, task_id: str, user_intent: str):
        self.task_id = task_id
        self.user_intent = user_intent
        self.status = TaskStatus.PENDING
        self.created_at = datetime.now()
        self.started_at = None
        self.completed_at = None
        
        # Execution tracking
        self.action_history: List[ActionRecord] = []
        self.current_action: Optional[ActionRecord] = None
        self.max_steps = 100
        self.step_count = 0
        
        # Context tracking
        self.context_window: List[Dict] = []
        self.max_context = 20
        self.screen_changes: List[Dict] = []
        
        # Decision tracking
        self.planning_attempts = 0
        self.execution_errors = 0
        self.max_retries = 3
        
        # Memory
        self.short_term_memory: Dict[str, Any] = {}
        self.extracted_data: Dict[str, Any] = {}
        
        logger.info(f"TaskState created: {task_id} - {user_intent}")
    
    def start(self):
        """Mark task as started"""
        self.status = TaskStatus.IN_PROGRESS
        self.started_at = datetime.now()
        logger.info(f"Task started: {self.task_id}")
    
    def complete(self):
        """Mark task as completed"""
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now()
        duration = (self.completed_at - self.started_at).total_seconds()
        logger.info(f"Task completed: {self.task_id} in {duration:.1f}s")
    
    def fail(self, reason: str):
        """Mark task as failed"""
        self.status = TaskStatus.FAILED
        self.completed_at = datetime.now()
        logger.error(f"Task failed: {self.task_id} - {reason}")
    
    def record_action(self, action: ActionRecord):
        """
        Record an action in history
        
        Args:
            action: ActionRecord to record
        """
        self.action_history.append(action)
        self.current_action = action
        self.step_count += 1
        
        # Maintain context window
        context_entry = {
            'action': action.to_dict(),
            'timestamp': datetime.now().isoformat(),
            'status': self.status.value
        }
        self.context_window.append(context_entry)
        
        if len(self.context_window) > self.max_context:
            self.context_window.pop(0)
        
        logger.info(
            f"Action recorded: {action.action_type.value} - {action.description}"
        )
    
    def add_screen_change(self, before_text: str, after_text: str,
                         change_type: str):
        """
        Record a screen state change
        
        Args:
            before_text: Text before action
            after_text: Text after action
            change_type: Type of change detected
        """
        change = {
            'timestamp': datetime.now().isoformat(),
            'step': self.step_count,
            'before_text': before_text[:200],
            'after_text': after_text[:200],
            'type': change_type
        }
        self.screen_changes.append(change)
        logger.info(f"Screen change detected: {change_type}")
    
    def is_complete(self) -> bool:
        """Check if task should be considered complete"""
        # Task times out after max steps
        if self.step_count >= self.max_steps:
            return True
        # Task explicitly completed
        if self.status == TaskStatus.COMPLETED:
            return True
        return False
    
    def should_retry(self) -> bool:
        """Check if task should retry after error"""
        return self.execution_errors < self.max_retries
    
    def get_context_summary(self) -> str:
        """
        Get summary of task context for LLM
        
        Returns:
            str: Context summary
        """
        summary = f"""
Task: {self.user_intent}
Status: {self.status.value}
Steps completed: {self.step_count}/{self.max_steps}
Errors: {self.execution_errors}

Recent actions:
"""
        # Show last 5 actions
        for action in self.action_history[-5:]:
            summary += f"- {action.description} ({'✓' if action.success else '✗'})\n"
        
        if self.screen_changes:
            summary += "\nRecent screen changes:\n"
            for change in self.screen_changes[-3:]:
                summary += f"- {change['type']}\n"
        
        return summary
    
    def get_execution_summary(self) -> Dict:
        """Get complete execution summary"""
        duration = 0
        if self.started_at and self.completed_at:
            duration = (self.completed_at - self.started_at).total_seconds()
        elif self.started_at:
            duration = (datetime.now() - self.started_at).total_seconds()
        
        successful_actions = sum(
            1 for a in self.action_history if a.success
        )
        
        return {
            'task_id': self.task_id,
            'user_intent': self.user_intent,
            'status': self.status.value,
            'duration_seconds': duration,
            'steps_taken': self.step_count,
            'actions_successful': successful_actions,
            'total_actions': len(self.action_history),
            'errors': self.execution_errors,
            'extracted_data': self.extracted_data,
            'screen_changes': len(self.screen_changes),
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
    
    def to_dict(self) -> Dict:
        """Convert task state to dict"""
        return {
            'task_id': self.task_id,
            'user_intent': self.user_intent,
            'status': self.status.value,
            'step_count': self.step_count,
            'action_history': [a.to_dict() for a in self.action_history],
            'context_window': self.context_window,
            'short_term_memory': self.short_term_memory,
            'extracted_data': self.extracted_data,
            'screen_changes': self.screen_changes,
            'summary': self.get_execution_summary()
        }


# =========================
# TASK STATE MANAGER
# =========================

class TaskStateManager:
    """Manages multiple task states"""
    
    def __init__(self):
        self.tasks: Dict[str, TaskState] = {}
        self.current_task_id: Optional[str] = None
        logger.info("TaskStateManager initialized")
    
    def create_task(self, task_id: str, user_intent: str) -> TaskState:
        """Create a new task"""
        task = TaskState(task_id, user_intent)
        self.tasks[task_id] = task
        self.current_task_id = task_id
        return task
    
    def get_current_task(self) -> Optional[TaskState]:
        """Get currently active task"""
        if self.current_task_id:
            return self.tasks.get(self.current_task_id)
        return None
    
    def get_task(self, task_id: str) -> Optional[TaskState]:
        """Get task by ID"""
        return self.tasks.get(task_id)
    
    def list_tasks(self, status: TaskStatus = None) -> List[TaskState]:
        """List all tasks, optionally filtered by status"""
        tasks = list(self.tasks.values())
        if status:
            tasks = [t for t in tasks if t.status == status]
        return tasks


# =========================
# SINGLETON INSTANCE
# =========================

_task_manager = None

def get_task_manager() -> TaskStateManager:
    """Get or create task state manager"""
    global _task_manager
    if _task_manager is None:
        _task_manager = TaskStateManager()
    return _task_manager
