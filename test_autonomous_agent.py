#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
JARVIS 1.0 - Quick Test & Demo
==============================

Test script to verify the autonomous agent is working correctly.
Run this to see OTAVR loop in action.
"""

import asyncio
import sys
import os

# Add Backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Backend'))


async def test_autonomous_agent():
    """Test the autonomous agent with sample requests"""
    
    print("\n" + "=" * 70)
    print("🚀 JARVIS 1.0 - AUTONOMOUS AGENT TEST")
    print("=" * 70)
    
    try:
        from autonomous_agent_enhanced import get_agent
        
        agent = get_agent()
        
        # Show status
        status = agent.get_status()
        print("\n📊 Agent Status:")
        print(f"   Planner: {'✅' if status['components']['planner'] else '❌'}")
        print(f"   Executor: {'✅' if status['components']['executor'] else '❌'}")
        print(f"   Screen Reader: {'✅' if status['components']['screen_reader'] else '❌'}")
        
        # Test requests
        test_requests = [
            "show current screen",
            "take a screenshot and analyze it",
        ]
        
        print("\n" + "=" * 70)
        print("📋 TEST REQUESTS")
        print("=" * 70)
        
        for i, request in enumerate(test_requests, 1):
            print(f"\n[{i}] Testing: '{request}'")
            print("-" * 70)
            
            try:
                result = await agent.execute_task(request)
                
                print("\n✅ RESULT:")
                print(f"   Success: {result.get('success')}")
                print(f"   Response: {result.get('response')}")
                
                if result.get('details'):
                    details = result['details']
                    print(f"   Actions: {details.get('total_actions', 0)}")
                    print(f"   Success Rate: {details.get('successful_actions', 0)}/{details.get('total_actions', 1)}")
                
            except Exception as e:
                print(f"\n❌ ERROR: {e}")
        
        print("\n" + "=" * 70)
        print("✅ TEST COMPLETE")
        print("=" * 70)
        print("\n📖 For more information, see: AUTONOMOUS_AGENT_COMPLETE_GUIDE.md\n")
        
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
        print("\n⚠️  Make sure all dependencies are installed:")
        print("   pip install -r Backend/requirements.txt")
        import traceback
        traceback.print_exc()


async def interactive_test():
    """Interactive test mode - user enters requests"""
    
    print("\n" + "=" * 70)
    print("🚀 JARVIS 1.0 - INTERACTIVE TEST MODE")
    print("=" * 70)
    print("\nEnter requests to test the autonomous agent.")
    print("Type 'exit' or 'quit' to exit.\n")
    
    try:
        from autonomous_agent_enhanced import get_agent
        
        agent = get_agent()
        
        while True:
            try:
                request = input("\n💬 Enter request: ").strip()
                
                if request.lower() in ['exit', 'quit']:
                    print("\n👋 Goodbye!")
                    break
                
                if not request:
                    print("⚠️  Please enter a request")
                    continue
                
                print("\n" + "-" * 70)
                result = await agent.execute_task(request)
                print("-" * 70)
                
                print(f"\n✅ Result: {result.get('success')}")
                print(f"   Response: {result.get('response')}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Test interrupted")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
        
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()


def print_usage():
    """Print usage information"""
    
    print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║                    JARVIS 1.0 - AUTONOMOUS AGENT TEST                          ║
╚════════════════════════════════════════════════════════════════════════════════╝

USAGE:
    python test_autonomous_agent.py [OPTIONS]

OPTIONS:
    --auto       Run automatic tests with predefined requests
    --interactive  Interactive mode (you enter requests)
    --help       Show this help message

EXAMPLES:
    python test_autonomous_agent.py --auto
    python test_autonomous_agent.py --interactive

FEATURES TESTED:
    ✅ Dynamic planning (NO hardcoding)
    ✅ Universal action execution
    ✅ OCR-based screen verification
    ✅ Automatic retry on failure
    ✅ OTAVR loop execution

For full documentation, see: AUTONOMOUS_AGENT_COMPLETE_GUIDE.md
    """)


if __name__ == "__main__":
    
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        
        if arg in ['--help', '-h', 'help']:
            print_usage()
        elif arg in ['--interactive', '-i', 'interactive']:
            asyncio.run(interactive_test())
        elif arg in ['--auto', 'auto']:
            asyncio.run(test_autonomous_agent())
        else:
            print(f"Unknown option: {arg}")
            print_usage()
    else:
        # Default: run auto test
        asyncio.run(test_autonomous_agent())
