"""
Advanced Planning Engine using Gemini AI
Breaks down user requests into executable action plans
"""
import json
import logging
from ai_brain import get_ai
from config import DEBUG

logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO)
logger = logging.getLogger(__name__)

# ========================
# PLANNING PROMPTS
# ========================

PLANNING_SYSTEM_PROMPT = """
You are an expert task planner and coordinator.

Your job:
1. Understand the user's request completely
2. Break it down into logical steps
3. Return a JSON action plan

Available browser actions:
- navigate_to: Navigate to a website
- wait_for: Wait for element to appear
- click: Click an element by text or XPath
- type: Type text into a field
- submit_form: Submit a form
- extract_data: Extract data from page
- wait_seconds: Wait for N seconds
- screenshot: Take screenshot
- go_back: Go to previous page

Available system actions:
- open_app: Open application
- open_website: Open website
- search_google: Search Google
- search_youtube: Search YouTube
- create_folder: Create folder
- write_file: Write to file
- execute_command: Run system command

Available data actions:
- parse_text: Parse text from screenshot
- extract_emails: Extract emails
- format_data: Format/transform data
- summarize: Summarize content

Important Rules:
1. Return ONLY valid JSON (no markdown, no explanations)
2. Return array of action objects
3. Each action must have "tool" and "params" keys
4. Include "wait" actions between rapid operations
5. Think about realistic timings
6. Consider what user actually wants, not literal words
7. Use common sense - "open youtube and play songs" means multiple steps
8. Order actions logically

Example valid response:
[
  {"tool": "open_website", "params": {"site": "youtube"}},
  {"tool": "wait_seconds", "params": {"seconds": 3}},
  {"tool": "type", "params": {"text": "Arijit Singh"}},
  {"tool": "click", "params": {"text": "Search"}}
]

Return ONLY the JSON array, nothing else.
"""

# ========================
# PLAN CREATION
# ========================

class PlannerAI:
    """
    Advanced planning engine for breaking down user requests
    """

    def __init__(self):
        self.ai = get_ai()
        self.plan_history = []
        logger.info("Initialized PlannerAI")

    def create_plan(self, user_request, context=""):
        """
        Create an action plan from user request

        Args:
            user_request: What the user wants to do
            context: Additional context (previous actions, etc.)

        Returns:
            List of actions to execute
        """
        try:
            # Create prompt with context
            full_prompt = f"""
{context}

USER REQUEST: {user_request}

Create a detailed action plan for this request. 
Think step-by-step about what needs to happen.
Return ONLY a valid JSON array of actions.
"""

            logger.info(f"Planning: {user_request[:100]}...")

            # Get plan from AI
            response = self.ai.chat(full_prompt, "You are a planning expert.")

            # Extract JSON from response
            plan = self._extract_json(response)

            if not plan:
                logger.warning("Could not extract plan from response")
                return []

            # Validate plan
            validated_plan = self._validate_plan(plan)

            logger.info(f"Created plan with {len(validated_plan)} actions")
            logger.debug(f"Plan: {validated_plan}")

            # Store in history
            self.plan_history.append({
                'request': user_request,
                'plan': validated_plan
            })

            return validated_plan

        except Exception as e:
            logger.error(f"Plan creation error: {str(e)}")
            return []

    def _extract_json(self, text):
        """Extract JSON array from text response"""
        try:
            # Find JSON array
            start = text.find('[')
            end = text.rfind(']') + 1

            if start == -1 or end == 0:
                logger.warning("No JSON array found in response")
                return None

            json_text = text[start:end]
            plan = json.loads(json_text)

            return plan if isinstance(plan, list) else None

        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}")
            return None

    def _validate_plan(self, plan):
        """Validate and sanitize action plan"""
        if not isinstance(plan, list):
            return []

        valid_actions = []

        for action in plan:
            if not isinstance(action, dict):
                continue

            tool = action.get('tool', '')
            params = action.get('params', {})

            # Validate tool exists
            if not tool:
                logger.warning(f"Action missing tool: {action}")
                continue

            # Validate params is dict
            if not isinstance(params, dict):
                params = {}

            valid_actions.append({
                'tool': tool,
                'params': params
            })

        return valid_actions

    def refine_plan(self, plan, feedback):
        """Refine a plan based on feedback"""
        try:
            prompt = f"""
Current plan:
{json.dumps(plan, indent=2)}

Feedback/Issue:
{feedback}

Create a refined plan that addresses the feedback.
Return ONLY a valid JSON array of actions.
"""
            response = self.ai.chat(prompt)
            refined_plan = self._extract_json(response)
            return self._validate_plan(refined_plan) if refined_plan else plan

        except Exception as e:
            logger.error(f"Plan refinement error: {str(e)}")
            return plan

    def explain_plan(self, plan):
        """Explain what a plan will do"""
        try:
            prompt = f"""
Explain this action plan in simple terms for a user:
{json.dumps(plan, indent=2)}

Be concise and clear about what will happen.
"""
            return self.ai.chat(prompt)
        except Exception as e:
            logger.error(f"Explanation error: {str(e)}")
            return "Could not explain plan"


# ========================
# GLOBAL INSTANCE
# ========================

_planner = None

def get_planner():
    """Get global planner instance"""
    global _planner
    if _planner is None:
        _planner = PlannerAI()
    return _planner

def create_plan(command, context=""):
    """Quick function to create a plan"""
    return get_planner().create_plan(command, context)

# ========================
# TESTING
# ========================

if __name__ == "__main__":
    print("Testing Planner AI...")
    planner = get_planner()
    
    test_request = "Open YouTube and search for Arijit Singh songs"
    plan = planner.create_plan(test_request)
    
    print(f"\nRequest: {test_request}")
    print(f"\nGenerated Plan:")
    print(json.dumps(plan, indent=2))
    
    if plan:
        explanation = planner.explain_plan(plan)
        print(f"\nExplanation:\n{explanation}")
    
    print("\n✅ Planner test complete")