"""
Test Suite for Autonomous Agent System
Demonstrates all capabilities and provides testing utilities
"""

import asyncio
import json
import logging
from typing import Dict, Any, List

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# =========================
# TEST SUITE
# =========================

class AutonomousAgentTestSuite:
    """Comprehensive test suite for autonomous agent"""
    
    def __init__(self):
        from tool_registry import get_tool_registry
        from autonomous_agent_enhanced import get_autonomous_agent
        
        self.registry = get_tool_registry()
        self.agent = get_autonomous_agent()
        self.test_results = []
    
    # ========================
    # TOOL REGISTRY TESTS
    # ========================
    
    async def test_tool_registry(self) -> Dict[str, Any]:
        """Test tool registry functionality"""
        logger.info("\n" + "="*60)
        logger.info("TEST: Tool Registry")
        logger.info("="*60)
        
        results = {
            "test_name": "Tool Registry",
            "passed": True,
            "details": {}
        }
        
        try:
            # Test 1: Get all tools
            tools = self.registry.get_all_tools()
            logger.info(f"✅ Found {len(tools)} tools")
            results["details"]["total_tools"] = len(tools)
            
            # Test 2: Get tools by category
            from tool_registry import ToolCategory
            for category in ToolCategory:
                cat_tools = self.registry.get_tools_by_category(category)
                logger.info(f"✅ Category '{category.value}': {len(cat_tools)} tools")
                results["details"][f"category_{category.value}"] = len(cat_tools)
            
            # Test 3: Search tools
            search_results = self.registry.search_tools("click")
            logger.info(f"✅ Search 'click': {len(search_results)} results")
            
            # Test 4: Get tool by name
            click_tool = self.registry.get_tool("click")
            if click_tool:
                logger.info(f"✅ Retrieved tool: {click_tool.name}")
                results["details"]["tool_retrieval"] = True
            
            # Test 5: Get statistics
            stats = self.registry.get_statistics()
            logger.info(f"✅ Statistics: {stats['total_executions']} total executions")
            results["details"]["statistics"] = stats
            
        except Exception as e:
            logger.error(f"❌ Test failed: {e}")
            results["passed"] = False
            results["error"] = str(e)
        
        return results
    
    # ========================
    # TOOL EXECUTION TESTS
    # ========================
    
    async def test_tool_execution(self) -> Dict[str, Any]:
        """Test executing individual tools"""
        logger.info("\n" + "="*60)
        logger.info("TEST: Tool Execution")
        logger.info("="*60)
        
        results = {
            "test_name": "Tool Execution",
            "passed": True,
            "tool_tests": []
        }
        
        try:
            # Test basic tools that don't modify system
            test_tools = [
                {
                    "name": "wait",
                    "params": {"seconds": 0.1},
                    "description": "Simple wait"
                },
                {
                    "name": "screenshot",
                    "params": {},
                    "description": "Take screenshot"
                },
            ]
            
            for tool_test in test_tools:
                try:
                    logger.info(f"Testing: {tool_test['description']}...")
                    
                    result = await self.registry.execute_tool(
                        tool_test["name"],
                        **tool_test["params"]
                    )
                    
                    if result["success"]:
                        logger.info(f"✅ {tool_test['name']} succeeded")
                        results["tool_tests"].append({
                            "tool": tool_test["name"],
                            "success": True
                        })
                    else:
                        logger.warning(f"⚠️ {tool_test['name']} failed: {result.get('error')}")
                        results["tool_tests"].append({
                            "tool": tool_test["name"],
                            "success": False,
                            "error": result.get("error")
                        })
                        results["passed"] = False
                
                except Exception as e:
                    logger.error(f"❌ Exception in {tool_test['name']}: {e}")
                    results["passed"] = False
        
        except Exception as e:
            logger.error(f"❌ Test failed: {e}")
            results["passed"] = False
            results["error"] = str(e)
        
        return results
    
    # ========================
    # AGENT LOOP TESTS
    # ========================
    
    async def test_simple_task(self) -> Dict[str, Any]:
        """Test agent with a simple task"""
        logger.info("\n" + "="*60)
        logger.info("TEST: Simple Task Execution")
        logger.info("="*60)
        
        results = {
            "test_name": "Simple Task",
            "passed": True,
            "task": "Take a screenshot"
        }
        
        try:
            # Simple non-destructive task
            task_result = await self.agent.execute_autonomous_task(
                "Take a screenshot and analyze it",
                max_steps=5
            )
            
            if task_result["success"]:
                logger.info(f"✅ Task completed in {task_result['step_count']} steps")
                results["result"] = task_result
            else:
                logger.warning(f"⚠️ Task did not complete: {task_result}")
                results["passed"] = False
        
        except Exception as e:
            logger.error(f"❌ Test failed: {e}")
            results["passed"] = False
            results["error"] = str(e)
        
        return results
    
    # ========================
    # VISION CONTEXT TESTS
    # ========================
    
    async def test_vision_system(self) -> Dict[str, Any]:
        """Test vision and screen understanding"""
        logger.info("\n" + "="*60)
        logger.info("TEST: Vision System")
        logger.info("="*60)
        
        results = {
            "test_name": "Vision System",
            "passed": True,
            "details": {}
        }
        
        try:
            # Test screen capture
            result = await self.registry.execute_tool("screenshot")
            
            if result["success"]:
                logger.info(f"✅ Screenshot captured: {result['result']['path']}")
                results["details"]["screenshot_path"] = result["result"]["path"]
            else:
                logger.error(f"❌ Screenshot failed: {result['error']}")
                results["passed"] = False
            
            # Test vision context
            vision = self.agent.vision_context.to_dict()
            logger.info(f"✅ Vision context: {json.dumps(vision, indent=2)}")
            results["details"]["vision_context"] = vision
        
        except Exception as e:
            logger.error(f"❌ Test failed: {e}")
            results["passed"] = False
            results["error"] = str(e)
        
        return results
    
    # ========================
    # ACTION HISTORY TESTS
    # ========================
    
    async def test_history_tracking(self) -> Dict[str, Any]:
        """Test action and decision history tracking"""
        logger.info("\n" + "="*60)
        logger.info("TEST: History Tracking")
        logger.info("="*60)
        
        results = {
            "test_name": "History Tracking",
            "passed": True,
            "details": {}
        }
        
        try:
            action_count = len(self.agent.action_history)
            decision_count = len(self.agent.decision_history)
            
            logger.info(f"✅ Total actions recorded: {action_count}")
            logger.info(f"✅ Total decisions recorded: {decision_count}")
            
            results["details"]["action_count"] = action_count
            results["details"]["decision_count"] = decision_count
            
            if action_count > 0:
                logger.info(f"Recent actions: {self.agent.action_history[-3:]}")
                results["details"]["recent_actions"] = self.agent.action_history[-3:]
        
        except Exception as e:
            logger.error(f"❌ Test failed: {e}")
            results["passed"] = False
            results["error"] = str(e)
        
        return results
    
    # ========================
    # MAIN TEST RUNNER
    # ========================
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all tests and generate report"""
        logger.info("\n" + "▶"*70)
        logger.info("AUTONOMOUS AGENT SYSTEM - TEST SUITE")
        logger.info("▶"*70)
        
        test_results = {
            "timestamp": __import__('datetime').datetime.now().isoformat(),
            "tests": [],
            "summary": {
                "total": 0,
                "passed": 0,
                "failed": 0
            }
        }
        
        # Run tests
        tests = [
            self.test_tool_registry,
            self.test_tool_execution,
            self.test_vision_system,
            self.test_history_tracking,
            self.test_simple_task,
        ]
        
        for test in tests:
            try:
                result = await test()
                test_results["tests"].append(result)
                
                test_results["summary"]["total"] += 1
                if result["passed"]:
                    test_results["summary"]["passed"] += 1
                else:
                    test_results["summary"]["failed"] += 1
            
            except Exception as e:
                logger.error(f"❌ Test runner error: {e}")
                test_results["summary"]["failed"] += 1
        
        # Print summary
        logger.info("\n" + "="*70)
        logger.info("TEST SUMMARY")
        logger.info("="*70)
        logger.info(f"Total Tests: {test_results['summary']['total']}")
        logger.info(f"Passed: {test_results['summary']['passed']}")
        logger.info(f"Failed: {test_results['summary']['failed']}")
        
        if test_results["summary"]["failed"] == 0:
            logger.info("\n✅ ALL TESTS PASSED!")
        else:
            logger.warning(f"\n⚠️ {test_results['summary']['failed']} tests failed")
        
        logger.info("="*70 + "\n")
        
        return test_results


# =========================
# QUICK TESTS
# =========================

async def test_tools():
    """Quick test of individual tools"""
    logger.info("Running quick tool tests...")
    
    from tool_registry import get_tool_registry
    
    registry = get_tool_registry()
    
    # Show available tools
    tools = registry.get_all_tools()
    logger.info(f"\n📦 Available tools: {len(tools)}")
    
    for tool in tools[:5]:
        logger.info(f"  • {tool.name}: {tool.description}")


async def test_agent():
    """Quick test of agent"""
    logger.info("Running quick agent test...")
    
    from autonomous_agent_enhanced import get_autonomous_agent
    
    agent = get_autonomous_agent()
    
    logger.info(f"Agent configured with {agent.max_steps_per_task} max steps")


async def main():
    """Main test execution"""
    import sys
    
    if len(sys.argv) > 1:
        test_name = sys.argv[1].lower()
        
        if test_name == "quick":
            await test_tools()
            await test_agent()
        
        elif test_name == "full":
            suite = AutonomousAgentTestSuite()
            results = await suite.run_all_tests()
            
            # Save results
            with open("test_results.json", "w") as f:
                json.dump(results, f, indent=2)
            logger.info("Results saved to test_results.json")
        
        else:
            logger.warning(f"Unknown test: {test_name}")
    
    else:
        # Run full test suite by default
        suite = AutonomousAgentTestSuite()
        results = await suite.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())
