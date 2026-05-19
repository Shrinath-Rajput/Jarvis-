"""
Autonomous Agent Planner Debug Script
Tests the planner's ability to generate action plans from user commands
"""
import asyncio
import json
import logging
from autonomous_agent_enhanced import get_autonomous_agent
from tool_registry import get_tool_registry
from tool_implementations import register_all_tools

# Setup logging to capture everything
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('planner_debug.log')
    ]
)
logger = logging.getLogger(__name__)

async def test_planner():
    """Test the planner with various commands"""
    
    print("\n" + "="*70)
    print("AUTONOMOUS AGENT PLANNER DEBUG TEST")
    print("="*70 + "\n")
    
    # Initialize
    logger.info("Initializing autonomous agent...")
    agent = get_autonomous_agent()
    
    # Show available tools
    registry = get_tool_registry()
    tools = registry.get_all_tools()
    tool_names = [t.name for t in tools]
    
    print(f"\n📦 Available Tools ({len(tool_names)}):")
    print("=" * 70)
    for name in sorted(tool_names):
        print(f"  ✓ {name}")
    print("=" * 70 + "\n")
    
    # Test cases
    test_commands = [
        "Open YouTube",
        "Open YouTube and search Virat Kohli",
        "Search Google for Python tutorials",
        "Open Chrome",
        "Launch Google Chrome",
        "Open GitHub",
    ]
    
    print("\n🧪 Testing Planner with Various Commands:")
    print("=" * 70 + "\n")
    
    for i, command in enumerate(test_commands, 1):
        print(f"\n{'─'*70}")
        print(f"TEST {i}: {command}")
        print(f"{'─'*70}")
        
        try:
            # Test the planning without full execution
            logger.info(f"\n[TEST {i}] Testing command: {command}")
            
            # Simulate what the autonomous agent does
            from task_state import TaskState, TaskStatus
            task = TaskState("test_task", command)
            
            # Get planner output
            logger.info("[PLANNER] Calling _plan method...")
            plan = await agent._plan(task, {'task_complete': False, 'task_failed': False})
            
            if plan:
                print(f"\n✅ PLAN GENERATED:")
                print(f"   Tool: {plan.get('tool')}")
                print(f"   Parameters: {json.dumps(plan.get('parameters', {}), indent=6)}")
                print(f"   Reasoning: {plan.get('reasoning')}")
            else:
                print(f"\n❌ NO PLAN GENERATED")
                print(f"   This means the planner returned None")
                
        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")
            logger.error(f"Test error: {e}", exc_info=True)
    
    print("\n" + "="*70)
    print("TEST COMPLETE")
    print("="*70)
    print("\n📋 Check planner_debug.log for detailed logging output")

async def test_fallback_planner():
    """Test just the fallback planner"""
    
    print("\n\n" + "="*70)
    print("FALLBACK PLANNER TEST")
    print("="*70 + "\n")
    
    agent = get_autonomous_agent()
    
    from task_state import TaskState
    
    test_commands = [
        "Open YouTube",
        "Search for Python tutorials",
        "Open Chrome and go to Google",
        "Launch Notepad",
    ]
    
    for command in test_commands:
        print(f"\n📋 Command: {command}")
        task = TaskState("test", command)
        plan = agent._create_fallback_plan(task)
        
        if plan:
            print(f"   ✅ Tool: {plan.get('tool')}")
            print(f"   Parameters: {plan.get('parameters')}")
        else:
            print(f"   ❌ No fallback plan generated")

async def test_llm_response():
    """Test the LLM response directly"""
    
    print("\n\n" + "="*70)
    print("LLM RESPONSE TEST")
    print("="*70 + "\n")
    
    from ai_brain import get_ai
    
    ai = get_ai()
    print(f"AI Instance: {type(ai).__name__}")
    
    test_prompt = """
You are an autonomous AI agent. 
I need you to open YouTube and search for "Virat Kohli".
Respond with ONLY valid JSON (no markdown):
{
    "tool": "tool_name",
    "parameters": {"param": "value"},
    "reasoning": "why this action"
}
"""
    
    logger.info("Testing LLM response generation...")
    response = await ai.generate_response(test_prompt)
    
    if response:
        print(f"\n✅ LLM Response Received:")
        print(f"   Length: {len(response)} chars")
        print(f"   Content:\n{response}")
    else:
        print(f"\n❌ LLM Response is empty/None")

async def main():
    """Run all tests"""
    
    # First test just the fallback planner
    await test_fallback_planner()
    
    # Test LLM response
    await test_llm_response()
    
    # Full planner test
    await test_planner()

if __name__ == "__main__":
    asyncio.run(main())
