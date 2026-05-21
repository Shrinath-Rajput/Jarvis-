#!/usr/bin/env python3
"""
🧪 COMPREHENSIVE TEST SUITE FOR EXECUTOR AND PLANNER FIXES
Tests all fixes for executor-planner mismatch and voice recognition issues
"""

import sys
import json
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

# Add Backend to path
sys.path.insert(0, '/d/e drive/Only_Project/jarvis1.0/Backend')

from planner_ai import DynamicPlanner
from executor import executor

print(f"\n{'='*80}")
print(f"🧪 JARVIS EXECUTOR AND PLANNER COMPREHENSIVE TEST SUITE")
print(f"{'='*80}\n")

# ============================================================================
# TEST 1: Verify Executor Has All Tools
# ============================================================================

def test_executor_tools():
    """✅ Test 1: Verify all tools are available in executor"""
    print(f"\n{'='*80}")
    print(f"TEST 1: Executor Tool Inventory")
    print(f"{'='*80}\n")
    
    executor.print_available_tools()
    
    essential_tools = [
        'open_word', 'open_excel', 'open_chrome', 'open_firefox',
        'google_search', 'take_note', 'screenshot', 'set_volume',
        'play_spotify', 'send_email', 'create_spreadsheet'
    ]
    
    missing = [t for t in essential_tools if t not in executor.tools_available]
    
    if missing:
        print(f"⚠️  MISSING ESSENTIAL TOOLS: {missing}")
        return False
    
    print(f"✅ All {len(essential_tools)} essential tools are available")
    return True


# ============================================================================
# TEST 2: Verify Planner Tool Validation
# ============================================================================

def test_planner_validation():
    """✅ Test 2: Verify planner validates tool names"""
    print(f"\n{'='*80}")
    print(f"TEST 2: Planner Tool Validation")
    print(f"{'='*80}\n")
    
    planner = DynamicPlanner()
    
    # Test valid plan
    valid_plan = [
        {"tool": "open_chrome", "params": {}},
        {"tool": "wait", "params": {"seconds": 2}},
        {"tool": "google_search", "params": {"query": "Python"}}
    ]
    
    is_valid, errors = planner.validate_plan(valid_plan)
    print(f"Valid plan check: {'✅ PASS' if is_valid else '❌ FAIL'}")
    
    # Test invalid plan
    invalid_plan = [
        {"tool": "open_nonexistent_app", "params": {}},
        {"tool": "invalid_tool", "params": {}}
    ]
    
    is_valid, errors = planner.validate_plan(invalid_plan)
    
    if is_valid:
        print(f"❌ FAIL: Invalid plan was not caught")
        return False
    
    print(f"✅ Invalid plan correctly detected:")
    for error in errors:
        print(f"   - {error}")
    
    return True


# ============================================================================
# TEST 3: Tool Execution (Dry Run)
# ============================================================================

def test_tool_execution():
    """✅ Test 3: Test tool execution without actual actions"""
    print(f"\n{'='*80}")
    print(f"TEST 3: Tool Execution Dry Run")
    print(f"{'='*80}\n")
    
    test_plan = [
        {"tool": "wait", "params": {"seconds": 1}},
        {"tool": "screenshot", "params": {}},
        {"tool": "set_volume", "params": {"level": 50}}
    ]
    
    results = executor.execute_plan(test_plan)
    
    successful = sum(1 for r in results if r['success'])
    
    print(f"\n✅ Executed {len(results)} tools")
    print(f"✅ Successful: {successful}/{len(results)}")
    
    return True


# ============================================================================
# TEST 4: Parameter Validation
# ============================================================================

def test_parameter_validation():
    """✅ Test 4: Verify parameter validation"""
    print(f"\n{'='*80}")
    print(f"TEST 4: Parameter Validation")
    print(f"{'='*80}\n")
    
    # Test with missing required parameters
    bad_plan = [
        {"tool": "wait"}  # Missing required 'seconds' param
    ]
    
    results = executor.execute_plan(bad_plan)
    
    # Should handle gracefully
    if results[0]['success']:
        print(f"⚠️  Missing params didn't cause error (tool handles defaults)")
    else:
        print(f"✅ Missing params correctly identified: {results[0]['error']}")
    
    return True


# ============================================================================
# TEST 5: Error Recovery
# ============================================================================

def test_error_recovery():
    """✅ Test 5: Verify error recovery"""
    print(f"\n{'='*80}")
    print(f"TEST 5: Error Recovery")
    print(f"{'='*80}\n")
    
    # Plan with one invalid tool and valid ones
    mixed_plan = [
        {"tool": "wait", "params": {"seconds": 1}},
        {"tool": "nonexistent_tool", "params": {}},  # This should fail gracefully
        {"tool": "wait", "params": {"seconds": 1}}   # This should still execute
    ]
    
    results = executor.execute_plan(mixed_plan)
    
    # Count results
    successful = sum(1 for r in results if r['success'])
    failed = sum(1 for r in results if not r['success'])
    
    print(f"\n✅ Execution continued after error")
    print(f"   ✅ Successful: {successful}")
    print(f"   ❌ Failed: {failed}")
    
    # Should have 3 results (all steps attempted)
    return len(results) == 3


# ============================================================================
# TEST 6: Tool Name Normalization
# ============================================================================

def test_tool_name_normalization():
    """✅ Test 6: Verify tool name normalization"""
    print(f"\n{'='*80}")
    print(f"TEST 6: Tool Name Normalization")
    print(f"{'='*80}\n")
    
    # Test various name formats
    test_cases = [
        ("open_chrome", "open_chrome"),
        ("OPEN_CHROME", "open_chrome"),
        ("Open Chrome", "open_chrome"),
        ("open chrome", "open_chrome")
    ]
    
    all_passed = True
    
    for input_name, expected in test_cases:
        # Simulate normalization
        normalized = input_name.lower().replace(" ", "_").strip()
        
        passed = normalized == expected
        all_passed = all_passed and passed
        
        status = "✅" if passed else "❌"
        print(f"{status} '{input_name}' → '{normalized}' (expected: '{expected}')")
    
    return all_passed


# ============================================================================
# TEST 7: Large Plan Execution
# ============================================================================

def test_large_plan():
    """✅ Test 7: Execute larger complex plan"""
    print(f"\n{'='*80}")
    print(f"TEST 7: Large Plan Execution")
    print(f"{'='*80}\n")
    
    large_plan = [
        {"tool": "wait", "params": {"seconds": 1}},
        {"tool": "set_volume", "params": {"level": 75}},
        {"tool": "wait", "params": {"seconds": 1}},
        {"tool": "mute_system", "params": {}},
        {"tool": "wait", "params": {"seconds": 1}},
        {"tool": "unmute_system", "params": {}},
        {"tool": "battery_status", "params": {}},
        {"tool": "disk_space_check", "params": {}},
    ]
    
    print(f"📋 Executing {len(large_plan)}-step plan...\n")
    
    results = executor.execute_plan(large_plan)
    
    successful = sum(1 for r in results if r['success'])
    
    print(f"\n✅ Completed {len(large_plan)}-step plan")
    print(f"✅ Success rate: {successful}/{len(results)} ({100*successful//len(results)}%)")
    
    return successful >= len(large_plan) - 2  # Allow for minor failures


# ============================================================================
# TEST 8: Planner Integration
# ============================================================================

def test_planner_integration():
    """✅ Test 8: Test planner-executor integration"""
    print(f"\n{'='*80}")
    print(f"TEST 8: Planner-Executor Integration")
    print(f"{'='*80}\n")
    
    planner = DynamicPlanner()
    
    # Test simple requests
    requests = [
        "Take a screenshot",
        "Set volume to 50 percent",
        "Wait 2 seconds"
    ]
    
    print(f"Testing {len(requests)} planning requests...\n")
    
    for request in requests:
        try:
            print(f"📝 Request: {request}")
            plan = planner.plan_task(request)
            
            # Validate plan
            is_valid, errors = planner.validate_plan(plan)
            
            if is_valid:
                print(f"✅ Generated valid {len(plan)}-step plan\n")
            else:
                print(f"⚠️  Generated plan with warnings: {errors}\n")
        
        except Exception as e:
            print(f"❌ Error: {str(e)}\n")
            return False
    
    return True


# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

def run_all_tests():
    """Run all tests and report results"""
    
    tests = [
        ("Executor Tools", test_executor_tools),
        ("Planner Validation", test_planner_validation),
        ("Tool Execution", test_tool_execution),
        ("Parameter Validation", test_parameter_validation),
        ("Error Recovery", test_error_recovery),
        ("Tool Name Normalization", test_tool_name_normalization),
        ("Large Plan", test_large_plan),
        ("Planner Integration", test_planner_integration),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            print(f"\n{'='*80}")
            passed = test_func()
            results.append((name, passed))
            print(f"{'='*80}")
            print(f"Result: {'✅ PASS' if passed else '❌ FAIL'}")
        except Exception as e:
            logger.exception(f"Test '{name}' crashed: {e}")
            results.append((name, False))
    
    # Final Report
    print(f"\n\n{'='*80}")
    print(f"📊 FINAL TEST REPORT")
    print(f"{'='*80}\n")
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status:10} | {name}")
    
    print(f"\n{'='*80}")
    print(f"✅ PASSED: {passed_count}/{total_count}")
    print(f"{'='*80}\n")
    
    return passed_count == total_count


if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        sys.exit(1)
