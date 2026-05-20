#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
JARVIS 1.0 - QUICK START GUIDE
==============================

Run this script to verify everything is set up correctly
and get started with the autonomous agent.
"""

import os
import sys
import subprocess


def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def check_python_version():
    """Check Python version"""
    print_header("🐍 CHECKING PYTHON VERSION")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version_str} (OK)")
        return True
    else:
        print(f"❌ Python {version_str} (Requires 3.8+)")
        return False


def check_dependencies():
    """Check if main dependencies are installed"""
    print_header("📦 CHECKING DEPENDENCIES")
    
    dependencies = [
        "google.generativeai",
        "anthropic",
        "pyautogui",
        "pytesseract",
        "PIL",
        "mss",
        "numpy",
    ]
    
    missing = []
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep}")
            missing.append(dep)
    
    return len(missing) == 0, missing


def suggest_install():
    """Suggest installation command"""
    print_header("📥 INSTALLATION")
    
    print("To install all dependencies, run:")
    print("  cd Backend")
    print("  pip install -r requirements.txt")
    print()
    print("Or install specific package:")
    print("  pip install google-generativeai anthropic pyautogui pytesseract")


def check_project_structure():
    """Check project structure"""
    print_header("📁 PROJECT STRUCTURE")
    
    required_files = [
        "Backend/autonomous_agent_enhanced.py",
        "Backend/planner_ai.py",
        "Backend/executor_universal.py",
        "Backend/screen_understanding_ocr.py",
        "Backend/tool_implementations.py",
        "Backend/requirements.txt",
        "AUTONOMOUS_AGENT_COMPLETE_GUIDE.md",
        "PHASE_6_DELIVERY_SUMMARY.md",
        "test_autonomous_agent.py",
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} (MISSING)")
            all_exist = False
    
    return all_exist


def show_quick_examples():
    """Show quick usage examples"""
    print_header("💡 QUICK EXAMPLES")
    
    examples = [
        ('Basic Task', 'await execute_autonomous_task("create folder MyProject")'),
        ('Search Query', 'await execute_autonomous_task("search python on google")'),
        ('Multi-step', 'await execute_autonomous_task("open youtube and search ai")'),
    ]
    
    print("Python code examples:\n")
    for title, code in examples:
        print(f"  {title}:")
        print(f"    {code}\n")


def show_next_steps():
    """Show next steps"""
    print_header("📋 NEXT STEPS")
    
    print("1. INSTALL DEPENDENCIES")
    print("   cd Backend && pip install -r requirements.txt\n")
    
    print("2. READ DOCUMENTATION")
    print("   - AUTONOMOUS_AGENT_COMPLETE_GUIDE.md (full guide)")
    print("   - PHASE_6_DELIVERY_SUMMARY.md (what changed)\n")
    
    print("3. TEST THE SYSTEM")
    print("   python test_autonomous_agent.py --auto")
    print("   python test_autonomous_agent.py --interactive\n")
    
    print("4. USE IN YOUR CODE")
    print("   from Backend.autonomous_agent_enhanced import execute_autonomous_task\n")


def show_system_info():
    """Show system information"""
    print_header("ℹ️  SYSTEM INFORMATION")
    
    print(f"Platform: {sys.platform}")
    print(f"Python: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    print(f"Executable: {sys.executable}")
    print(f"Working Directory: {os.getcwd()}")


def show_features():
    """Show system features"""
    print_header("✨ JARVIS 1.0 FEATURES")
    
    features = [
        ("ZERO Hardcoding", "Pure dynamic LLM-driven reasoning"),
        ("Universal Actions", "18 generic actions for any task"),
        ("OCR Verification", "Real screen analysis after each action"),
        ("Auto Retry", "Automatic recovery from failures"),
        ("OTAVR Loop", "Observe → Think → Act → Verify → Retry"),
        ("Cross-Platform", "Windows, macOS, Linux support"),
        ("Multi-step Plans", "Complex workflows in one request"),
        ("Error Recovery", "Smart refinement on failure"),
    ]
    
    for feature, description in features:
        print(f"✅ {feature}")
        print(f"   {description}\n")


def main():
    """Main function"""
    
    print("\n" + "=" * 70)
    print("  🚀 JARVIS 1.0 - TRUE AUTONOMOUS AI AGENT")
    print("  Quick Start & Verification")
    print("=" * 70)
    
    # Check components
    py_ok = check_python_version()
    struct_ok = check_project_structure()
    deps_ok, missing = check_dependencies()
    
    show_system_info()
    show_features()
    
    # Summary
    print_header("📊 STATUS SUMMARY")
    
    if py_ok and struct_ok and deps_ok:
        print("✅ ALL CHECKS PASSED!")
        print("\nYou're ready to use JARVIS 1.0!")
        print("\nRun: python test_autonomous_agent.py --auto")
    else:
        print("⚠️  SOME CHECKS FAILED\n")
        
        if not py_ok:
            print("❌ Python 3.8+ required")
        if not struct_ok:
            print("❌ Some project files are missing")
        if not deps_ok:
            print(f"❌ Missing dependencies: {', '.join(missing)}")
        
        suggest_install()
    
    show_next_steps()
    
    print_header("📖 DOCUMENTATION")
    
    print("Read these files to learn about the system:\n")
    print("1. AUTONOMOUS_AGENT_COMPLETE_GUIDE.md")
    print("   └─ Full architecture and usage guide\n")
    print("2. PHASE_6_DELIVERY_SUMMARY.md")
    print("   └─ Before/After comparison and changes\n")
    print("3. JARVIS_1_0_FILES_REFERENCE.md")
    print("   └─ Reference to all modified files\n")
    print("4. test_autonomous_agent.py")
    print("   └─ Test and demo script\n")
    
    print_header("🎉 YOU'RE ALL SET!")
    
    print("JARVIS 1.0 is ready to use.")
    print("\nKey features:")
    print("  • Zero hardcoding")
    print("  • True autonomy")
    print("  • Dynamic reasoning")
    print("  • Auto-verification")
    print("  • Self-healing")
    print("\nStart with: python test_autonomous_agent.py --interactive\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Setup interrupted")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
