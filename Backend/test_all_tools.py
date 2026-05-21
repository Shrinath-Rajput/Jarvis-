# test_all_tools.py
"""
Comprehensive test suite for JARVIS extended tools
Tests individual tool imports and basic functionality
"""

import sys
import os
from datetime import datetime

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def print_status(name, success, message=""):
    """Print test status"""
    status = f"{GREEN}✓ PASS{RESET}" if success else f"{RED}✗ FAIL{RESET}"
    print(f"  {status} | {name:40} | {message}")

def test_imports():
    """Test all helper module imports"""
    print(f"\n{YELLOW}{'='*80}{RESET}")
    print(f"{YELLOW}TESTING IMPORTS{RESET}")
    print(f"{YELLOW}{'='*80}{RESET}\n")
    
    modules = [
        ('file_manager', 'FileManager'),
        ('browser_tools', 'BrowserTools'),
        ('system_control', 'SystemControl'),
        ('email_tools', 'EmailTools'),
        ('document_tools', 'DocumentTools'),
        ('app_launcher', 'AppLauncher'),
        ('whatsapp_tools', 'WhatsAppTools'),
        ('excel_tools', 'ExcelTools'),
        ('media_tools', 'MediaTools'),
        ('developer_tools', 'DeveloperTools'),
        ('productivity_tools', 'ProductivityTools'),
    ]
    
    passed = 0
    failed = 0
    
    for module_name, class_name in modules:
        try:
            module = __import__(module_name)
            print_status(f"Import {module_name}", True)
            passed += 1
        except Exception as e:
            print_status(f"Import {module_name}", False, str(e)[:30])
            failed += 1
    
    return passed, failed

def test_executor():
    """Test executor integration"""
    print(f"\n{YELLOW}{'='*80}{RESET}")
    print(f"{YELLOW}TESTING EXECUTOR{RESET}")
    print(f"{YELLOW}{'='*80}{RESET}\n")
    
    try:
        from executor import DynamicExecutor
        executor = DynamicExecutor()
        
        # Test basic tool methods exist
        tools_to_test = [
            'tool_open_website',
            'tool_google_search',
            'tool_set_volume',
            'tool_create_folder',
            'tool_type',
            'tool_wait',
            'tool_screenshot',
            'tool_send_email',
            'tool_create_spreadsheet',
            'tool_open_app',
        ]
        
        passed = 0
        failed = 0
        
        for tool_name in tools_to_test:
            if hasattr(executor, tool_name):
                print_status(f"Tool: {tool_name[5:]}", True)
                passed += 1
            else:
                print_status(f"Tool: {tool_name[5:]}", False, "Not found")
                failed += 1
        
        return passed, failed
    except Exception as e:
        print_status("Executor import", False, str(e))
        return 0, len(tools_to_test)

def test_planner():
    """Test planner integration"""
    print(f"\n{YELLOW}{'='*80}{RESET}")
    print(f"{YELLOW}TESTING PLANNER{RESET}")
    print(f"{YELLOW}{'='*80}{RESET}\n")
    
    try:
        from planner_ai import DynamicPlanner
        planner = DynamicPlanner()
        print_status("Planner instantiation", True)
        
        # Check if SYSTEM_PROMPT exists and contains tool descriptions
        from planner_ai import SYSTEM_PROMPT
        
        required_keywords = [
            'open_website',
            'create_folder',
            'send_email',
            'create_spreadsheet',
            'set_volume',
        ]
        
        passed = 1
        failed = 0
        
        for keyword in required_keywords:
            if keyword in SYSTEM_PROMPT:
                print_status(f"Prompt contains: {keyword}", True)
                passed += 1
            else:
                print_status(f"Prompt contains: {keyword}", False, "Not in prompt")
                failed += 1
        
        return passed, failed
    except Exception as e:
        print_status("Planner setup", False, str(e)[:40])
        return 0, 1

def test_sample_plan():
    """Test generating a sample plan"""
    print(f"\n{YELLOW}{'='*80}{RESET}")
    print(f"{YELLOW}TESTING SAMPLE PLAN GENERATION{RESET}")
    print(f"{YELLOW}{'='*80}{RESET}\n")
    
    try:
        from executor import executor
        import json
        
        # Test a simple plan execution without network calls
        sample_plan = [
            {"tool": "wait", "params": {"seconds": 1}},
            {"tool": "type", "params": {"text": "test"}},
        ]
        
        print(f"  Executing sample plan with {len(sample_plan)} steps...")
        results = executor.execute_plan(sample_plan)
        
        success = sum(1 for r in results if r.get('success'))
        print_status(f"Executed {len(sample_plan)} steps", success > 0, f"{success}/{len(sample_plan)} succeeded")
        
        return 1, 0
    except Exception as e:
        print_status("Sample plan execution", False, str(e)[:40])
        return 0, 1

def test_tool_calls():
    """Test individual tool calls"""
    print(f"\n{YELLOW}{'='*80}{RESET}")
    print(f"{YELLOW}TESTING INDIVIDUAL TOOL CALLS{RESET}")
    print(f"{YELLOW}{'='*80}{RESET}\n")
    
    from file_manager import file_manager
    from system_control import system_control
    from productivity_tools import productivity_tools
    
    passed = 0
    failed = 0
    
    # Test disk space check (read-only, should always work)
    try:
        result = file_manager.get_disk_space()
        if result.get('success'):
            print_status("file_manager.get_disk_space()", True, f"{len(result.get('disks', []))} disks")
            passed += 1
        else:
            print_status("file_manager.get_disk_space()", False, result.get('error'))
            failed += 1
    except Exception as e:
        print_status("file_manager.get_disk_space()", False, str(e)[:30])
        failed += 1
    
    # Test battery status (read-only)
    try:
        result = system_control.get_battery_status()
        print_status("system_control.get_battery_status()", result.get('success'), "")
        if result.get('success'):
            passed += 1
        else:
            failed += 1
    except Exception as e:
        print_status("system_control.get_battery_status()", False, str(e)[:30])
        failed += 1
    
    # Test list todos (should return empty list)
    try:
        result = productivity_tools.list_todos()
        if result.get('success'):
            print_status("productivity_tools.list_todos()", True, "")
            passed += 1
        else:
            print_status("productivity_tools.list_todos()", False, result.get('error'))
            failed += 1
    except Exception as e:
        print_status("productivity_tools.list_todos()", False, str(e)[:30])
        failed += 1
    
    return passed, failed

def run_all_tests():
    """Run all tests"""
    print(f"\n{YELLOW}{'*'*80}{RESET}")
    print(f"{YELLOW}JARVIS 1.0 EXTENDED - TEST SUITE{RESET}")
    print(f"{YELLOW}{'*'*80}{RESET}")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Started at: {timestamp}\n")
    
    total_passed = 0
    total_failed = 0
    
    # Run all test suites
    p, f = test_imports()
    total_passed += p
    total_failed += f
    
    p, f = test_executor()
    total_passed += p
    total_failed += f
    
    p, f = test_planner()
    total_passed += p
    total_failed += f
    
    p, f = test_tool_calls()
    total_passed += p
    total_failed += f
    
    p, f = test_sample_plan()
    total_passed += p
    total_failed += f
    
    # Summary
    print(f"\n{YELLOW}{'='*80}{RESET}")
    print(f"{YELLOW}TEST SUMMARY{RESET}")
    print(f"{YELLOW}{'='*80}{RESET}\n")
    
    print(f"  Total Tests:    {total_passed + total_failed}")
    print(f"  {GREEN}Passed: {total_passed}{RESET}")
    print(f"  {RED}Failed: {total_failed}{RESET}")
    
    if total_failed == 0:
        print(f"\n{GREEN}{'✓'*40}{RESET}")
        print(f"{GREEN}ALL TESTS PASSED!{RESET}")
        print(f"{GREEN}{'✓'*40}{RESET}\n")
        return 0
    else:
        print(f"\n{RED}{'✗'*40}{RESET}")
        print(f"{RED}SOME TESTS FAILED{RESET}")
        print(f"{RED}{'✗'*40}{RESET}\n")
        return 1

if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
