"""
Advanced Execution Engine
Executes planned actions with error handling and monitoring
"""
import logging
import json
import traceback
from datetime import datetime
from typing import List, Dict, Any

from browser_control import get_browser, close_browser
from computer_control import ComputerControl
from config import DEBUG, MAX_RETRIES, TIMEOUT_SECONDS

logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO)
logger = logging.getLogger(__name__)

# ========================
# ACTION EXECUTION RESULTS
# ========================

class ExecutionResult:
    """Store execution result for an action"""
    
    def __init__(self, action, success, output, error=None):
        self.action = action
        self.success = success
        self.output = output
        self.error = error
        self.timestamp = datetime.now()
    
    def to_dict(self):
        return {
            'action': self.action,
            'success': self.success,
            'output': self.output,
            'error': self.error,
            'timestamp': self.timestamp.isoformat()
        }


# ========================
# EXECUTION ENGINE
# ========================

class ExecutionEngine:
    """
    Executes planned actions with monitoring and error handling
    """
    
    def __init__(self):
        self.browser = get_browser()
        self.computer = ComputerControl()
        self.results = []
        self.state = {
            'current_url': None,
            'page_title': None,
            'last_text_extracted': None,
        }
        logger.info("ExecutionEngine initialized")
    
    def execute_plan(self, plan: List[Dict]) -> List[ExecutionResult]:
        """
        Execute a complete action plan
        
        Args:
            plan: List of actions to execute
            
        Returns:
            List of execution results
        """
        self.results = []
        
        if not plan:
            logger.warning("Empty plan provided")
            return []
        
        logger.info(f"Starting execution of plan with {len(plan)} actions")
        
        for i, action in enumerate(plan):
            logger.info(f"\n--- Action {i+1}/{len(plan)} ---")
            logger.info(f"Action: {action}")
            
            result = self.execute_action(action)
            self.results.append(result)
            
            # Stop on critical errors
            if not result.success and 'critical' in result.error.lower():
                logger.error(f"Critical error, stopping execution: {result.error}")
                break
        
        logger.info(f"\nExecution complete. Results: {len(self.results)}")
        return self.results
    
    def execute_action(self, action: Dict) -> ExecutionResult:
        """
        Execute a single action with error handling
        
        Args:
            action: Action to execute
            
        Returns:
            ExecutionResult
        """
        try:
            tool = action.get('tool', '').lower()
            params = action.get('params', {})
            
            logger.debug(f"Executing: {tool} with params: {params}")
            
            # ========================
            # BROWSER NAVIGATION
            # ========================
            
            if tool == 'navigate_to' or tool == 'navigate':
                url = params.get('url') or params.get('site', '')
                if not self.browser.is_open:
                    self.browser.launch()
                
                success = self.browser.navigate(url)
                output = self.browser.get_current_url() if success else None
                self.state['current_url'] = output
                
                return ExecutionResult(
                    action,
                    success,
                    f"Navigated to {output}" if success else None,
                    "Failed to navigate" if not success else None
                )
            
            # ========================
            # WAIT ACTIONS
            # ========================
            
            elif tool == 'wait' or tool == 'wait_seconds':
                seconds = int(params.get('seconds', 1))
                self.browser.wait(seconds)
                return ExecutionResult(
                    action,
                    True,
                    f"Waited {seconds} seconds"
                )
            
            elif tool == 'wait_for':
                selector = params.get('selector') or params.get('element', '')
                timeout = int(params.get('timeout', 10000))
                success = self.browser.wait_for_element(selector, timeout)
                
                return ExecutionResult(
                    action,
                    success,
                    f"Element appeared: {selector}" if success else None,
                    f"Element not found: {selector}" if not success else None
                )
            
            elif tool == 'wait_for_text':
                text = params.get('text', '')
                timeout = int(params.get('timeout', 10000))
                success = self.browser.wait_for_text(text, timeout)
                
                return ExecutionResult(
                    action,
                    success,
                    f"Text appeared: {text}" if success else None,
                    f"Text not found: {text}" if not success else None
                )
            
            # ========================
            # CLICK ACTIONS
            # ========================
            
            elif tool == 'click':
                selector = params.get('selector') or params.get('element', '')
                success = self.browser.click(selector)
                
                return ExecutionResult(
                    action,
                    success,
                    f"Clicked: {selector}" if success else None,
                    f"Failed to click: {selector}" if not success else None
                )
            
            elif tool == 'click_text':
                text = params.get('text', '')
                success = self.browser.click_text(text)
                
                return ExecutionResult(
                    action,
                    success,
                    f"Clicked text: {text}" if success else None,
                    f"Failed to click text: {text}" if not success else None
                )
            
            # ========================
            # TYPE ACTIONS
            # ========================
            
            elif tool == 'type' or tool == 'type_text':
                selector = params.get('selector') or params.get('element', '')
                text = params.get('text', '')
                delay = int(params.get('delay', 0))
                
                success = self.browser.type_text(selector, text, delay)
                
                return ExecutionResult(
                    action,
                    success,
                    f"Typed into {selector}" if success else None,
                    f"Failed to type: {selector}" if not success else None
                )
            
            elif tool == 'fill_field':
                label = params.get('label', '')
                text = params.get('text', '')
                success = self.browser.find_and_type(label, text)
                
                return ExecutionResult(
                    action,
                    success,
                    f"Filled field: {label}" if success else None,
                    f"Failed to fill field: {label}" if not success else None
                )
            
            # ========================
            # FORM ACTIONS
            # ========================
            
            elif tool == 'submit_form':
                selector = params.get('selector', 'form')
                success = self.browser.submit_form(selector)
                
                return ExecutionResult(
                    action,
                    success,
                    "Form submitted" if success else None,
                    "Failed to submit form" if not success else None
                )
            
            elif tool == 'select_dropdown':
                selector = params.get('selector', '')
                value = params.get('value', '')
                success = self.browser.select_dropdown(selector, value)
                
                return ExecutionResult(
                    action,
                    success,
                    f"Selected {value}" if success else None,
                    f"Failed to select {value}" if not success else None
                )
            
            # ========================
            # DATA EXTRACTION
            # ========================
            
            elif tool == 'extract_text':
                selector = params.get('selector', '')
                text = self.browser.get_text(selector)
                
                return ExecutionResult(
                    action,
                    text is not None,
                    text if text else None,
                    "Failed to extract text" if text is None else None
                )
            
            elif tool == 'extract_links':
                links = self.browser.extract_links()
                
                return ExecutionResult(
                    action,
                    True,
                    f"Extracted {len(links)} links",
                    None
                )
            
            elif tool == 'screenshot':
                name = params.get('name', '')
                path = self.browser.screenshot(name)
                
                return ExecutionResult(
                    action,
                    path is not None,
                    f"Screenshot: {path}" if path else None,
                    "Failed to take screenshot" if path is None else None
                )
            
            # ========================
            # NAVIGATION
            # ========================
            
            elif tool == 'go_back':
                success = self.browser.go_back()
                return ExecutionResult(
                    action,
                    success,
                    "Went back" if success else None,
                    "Failed to go back" if not success else None
                )
            
            elif tool == 'refresh':
                success = self.browser.refresh()
                return ExecutionResult(
                    action,
                    success,
                    "Page refreshed" if success else None,
                    "Failed to refresh" if not success else None
                )
            
            # ========================
            # SYSTEM ACTIONS
            # ========================
            
            elif tool == 'open_app':
                app = params.get('app', '')
                success = self.computer.open_application(app)
                return ExecutionResult(
                    action,
                    success,
                    f"Opened {app}" if success else None,
                    f"Failed to open {app}" if not success else None
                )
            
            elif tool == 'open_website':
                site = params.get('site', '')
                if not self.browser.is_open:
                    self.browser.launch()
                success = self.browser.navigate(site)
                return ExecutionResult(
                    action,
                    success,
                    f"Opened {site}" if success else None,
                    f"Failed to open {site}" if not success else None
                )
            
            # ========================
            # UNKNOWN ACTION
            # ========================
            
            else:
                logger.warning(f"Unknown tool: {tool}")
                return ExecutionResult(
                    action,
                    False,
                    None,
                    f"Unknown tool: {tool}"
                )
        
        except Exception as e:
            logger.error(f"Execution error: {str(e)}")
            logger.error(traceback.format_exc())
            
            return ExecutionResult(
                action,
                False,
                None,
                f"Exception: {str(e)}"
            )
    
    def get_results_summary(self) -> Dict[str, Any]:
        """Get summary of execution results"""
        successful = sum(1 for r in self.results if r.success)
        failed = len(self.results) - successful
        
        return {
            'total_actions': len(self.results),
            'successful': successful,
            'failed': failed,
            'success_rate': (successful / len(self.results) * 100) if self.results else 0,
            'results': [r.to_dict() for r in self.results]
        }
    
    def cleanup(self):
        """Clean up resources"""
        try:
            close_browser()
            self.computer.cleanup()
            logger.info("Execution engine cleaned up")
        except Exception as e:
            logger.error(f"Cleanup error: {str(e)}")


# ========================
# GLOBAL INSTANCE
# ========================

_executor = None

def get_executor():
    """Get global executor"""
    global _executor
    if _executor is None:
        _executor = ExecutionEngine()
    return _executor

def execute_plan(plan):
    """Quick execute function"""
    return get_executor().execute_plan(plan)

if __name__ == "__main__":
    print("Testing Execution Engine...")
    
    test_plan = [
        {"tool": "navigate", "params": {"url": "https://google.com"}},
        {"tool": "wait", "params": {"seconds": 2}},
        {"tool": "screenshot", "params": {"name": "google"}},
    ]
    
    executor = get_executor()
    results = executor.execute_plan(test_plan)
    
    print("\nExecution Results:")
    print(json.dumps(executor.get_results_summary(), indent=2))
    
    executor.cleanup()
    print("\n✅ Executor test complete")
