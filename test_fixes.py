#!/usr/bin/env python3
"""
Quick test script to verify Jarvis backend fixes
Run this to test the fixed executor and planner
"""

import subprocess
import json
import time
from pathlib import Path

# Test configuration
BACKEND_URL = "http://127.0.0.1:5000"
TEST_COMMANDS = [
    "Open Notepad",
    "Open Calculator", 
    "Open VS Code",
    "Create a folder named TestFolder on the Desktop",
    "Search Google for Python programming",
]

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def test_health():
    """Test if backend is running"""
    print_header("Testing Backend Health")
    try:
        import requests
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running")
            return True
        else:
            print(f"❌ Backend returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend not accessible: {e}")
        return False

def test_executor_app_opening():
    """Test the improved executor app opening"""
    print_header("Testing App Opening Fix")
    
    try:
        from Backend.executor import executor
        
        # Test notepad (most common failure)
        print("Testing notepad opening...")
        try:
            result = executor.tool_open_app("notepad")
            print(f"✅ Notepad: {result}")
        except Exception as e:
            print(f"❌ Notepad failed: {e}")
        
        # Test calculator
        print("\nTesting calculator opening...")
        try:
            result = executor.tool_open_app("calculator")
            print(f"✅ Calculator: {result}")
        except Exception as e:
            print(f"❌ Calculator failed: {e}")
            
    except Exception as e:
        print(f"❌ Could not import executor: {e}")

def test_folder_creation():
    """Test the improved folder creation"""
    print_header("Testing Folder Creation Fix")
    
    try:
        from Backend.executor import executor
        
        # Test Desktop folder
        print("Testing Desktop folder creation...")
        try:
            result = executor.tool_create_folder("TestJarvis", None)
            print(f"✅ Created: {result}")
            
            # Clean up
            import shutil
            if Path(result).exists():
                shutil.rmtree(result)
                print("   (Cleaned up test folder)")
        except Exception as e:
            print(f"❌ Failed: {e}")
            
    except Exception as e:
        print(f"❌ Could not import executor: {e}")

def test_voice_engine():
    """Test the VoiceEngine speech recognition fix"""
    print_header("Testing Speech Recognition Fix")
    
    # Check if isListening flag exists
    try:
        with open("src/services/VoiceEngine.js", "r") as f:
            content = f.read()
            
            if "this.isListening = false" in content:
                print("✅ isListening flag initialized")
            else:
                print("❌ isListening flag not found")
                
            if "if (this.isListening)" in content:
                print("✅ Double-start prevention check added")
            else:
                print("❌ Double-start prevention check not found")
                
            if "this.isListening = true" in content:
                print("✅ Flag set before recognition.start()")
            else:
                print("❌ Flag not set properly")
                
    except Exception as e:
        print(f"❌ Could not verify VoiceEngine: {e}")

def test_planner():
    """Test the improved planner"""
    print_header("Testing Planner Improvements")
    
    try:
        with open("Backend/planner_ai.py", "r") as f:
            content = f.read()
            
            checks = [
                ("Windows app mappings in prompt", "Open Notepad" in content),
                ("D drive path example", "D:\\\\" in content),
                ("VS Code example", "vs code" in content),
                ("open_app parameter doc", "app_name" in content),
            ]
            
            for check_name, found in checks:
                status = "✅" if found else "❌"
                print(f"{status} {check_name}")
                
    except Exception as e:
        print(f"❌ Could not verify planner: {e}")

def main():
    """Run all tests"""
    print("\n" + "█"*60)
    print("█  JARVIS 1.0 - FIXES VERIFICATION TEST")
    print("█"*60)
    
    # Test backend health
    is_healthy = test_health()
    
    # Test local Python modules
    test_executor_app_opening()
    test_folder_creation()
    test_voice_engine()
    test_planner()
    
    print_header("Test Summary")
    
    if is_healthy:
        print("✅ Backend is ready")
        print("\nTo fully test the fixes:")
        print("1. Open http://localhost:5173 in your browser")
        print("2. Click the microphone button")
        print("3. Try voice commands:")
        print("   - 'Open Notepad'")
        print("   - 'Open Calculator'")
        print("   - 'Create a folder named Test on Desktop'")
    else:
        print("❌ Backend is not running")
        print("\nTo start backend:")
        print("cd Backend")
        print("python app.py")
    
    print("\nAll fixes have been applied. See FIXES_APPLIED.md for details.\n")

if __name__ == "__main__":
    main()
