# JARVIS 1.0 PRODUCTION - QUICK START

## 🚀 IMMEDIATE USAGE

### Step 1: Replace Executor
```bash
# In Backend folder:
mv executor.py executor_old.py
mv executor_v3_production.py executor.py
```

### Step 2: Install Dependencies
```bash
pip install psutil pyautogui pygetwindow
```

### Step 3: Test Individual Tools

#### Test Opening Chrome
```python
from executor import executor

# Simple test
result = executor.tool_open_chrome()
print(result)
# Watch: Chrome will actually open and you'll see process verification
```

#### Test Creating Folder
```python
result = executor.tool_create_folder("TestJARVIS", "C:\\Users\\YourUsername\\Desktop")
print(result)
# Watch: Folder appears on Desktop, result shows verified: true
```

#### Test File Operations
```python
# Create file first
import os
test_file = "C:\\Users\\YourUsername\\Desktop\\test.txt"
open(test_file, 'w').write("Hello")

# Delete it
result = executor.tool_delete_file(test_file)
print(result)
# Watch: File is deleted and verified
```

#### Test Keyboard Input
```python
# Open Notepad first
executor.tool_open_notepad()
time.sleep(2)

# Type text
result = executor.tool_type("JARVIS is now REAL!")
print(result)
# Watch: Text appears in Notepad
```

### Step 4: Test Full Plans

```python
from executor import executor
import time

# Plan: Open Chrome and Google
plan = [
    {"tool": "open_chrome", "params": {"url": "https://www.google.com"}},
    {"tool": "wait", "params": {"seconds": 3}},
    {"tool": "screenshot", "params": {"save_path": "C:\\Users\\YourUsername\\Desktop\\test_ss.png"}}
]

results = executor.execute_plan(plan)
print("\n=== RESULTS ===")
for result in results:
    print(result)
# Watch: Chrome opens with Google, screenshot is saved and verified
```

## 📋 COMMON COMMANDS

### Browser Operations
```python
# Open website
executor.tool_open_chrome(url="https://www.youtube.com")

# Search
executor.tool_google_search(query="machine learning")
executor.tool_youtube_search(query="Python tutorial")
executor.tool_amazon_search(query="laptop")

# Incognito
executor.tool_open_chrome_incognito()
```

### Application Operations
```python
# Open apps
executor.tool_open_word()
executor.tool_open_excel()
executor.tool_open_vscode()
executor.tool_open_notepad()
executor.tool_open_spotify()

# Open by name
executor.tool_open_app(name="calculator")

# Close
executor.tool_close_app(name="notepad")
```

### File Operations
```python
# Create folder
executor.tool_create_folder("MyProject", "C:\\Users\\YourUsername\\Desktop")

# Open folder
executor.tool_open_folder("C:\\Users\\YourUsername\\Desktop")

# Delete file
executor.tool_delete_file("C:\\Users\\YourUsername\\Desktop\\oldfile.txt")

# Copy file
executor.tool_copy_file(
    "C:\\Users\\YourUsername\\Desktop\\source.txt",
    "C:\\Users\\YourUsername\\Desktop\\copy.txt"
)
```

### Keyboard & Mouse
```python
# Type text
executor.tool_type("Hello World")

# Press key
executor.tool_press_key("enter")
executor.tool_press_key("escape")
executor.tool_press_key("tab")

# Hotkey
executor.tool_hotkey("ctrl", "c")  # Copy
executor.tool_hotkey("ctrl", "v")  # Paste
executor.tool_hotkey("ctrl", "s")  # Save
executor.tool_hotkey("alt", "tab") # Switch window

# Click
executor.tool_click(x=500, y=300)  # Click at coordinates
executor.tool_click()  # Click at current mouse position
```

### System Control
```python
# Wait
executor.tool_wait(seconds=5)

# Screenshot
executor.tool_screenshot()
executor.tool_screenshot(save_path="C:\\Users\\YourUsername\\Desktop\\screenshot.png")

# Lock
executor.tool_lock_screen()

# Shutdown
executor.tool_shutdown(delay_minutes=0)  # Immediate

# Restart
executor.tool_restart(delay_minutes=0)  # Immediate
```

## 🔍 CHECKING LOGS

All operations log to: `Backend/executor_production.log`

```bash
# On Windows in PowerShell:
tail -f Backend/executor_production.log

# Or use:
Get-Content Backend/executor_production.log -Wait
```

Example log output:
```
2024-05-21 14:30:45 [INFO] 🚀 LAUNCHING APPLICATION: chrome
2024-05-21 14:30:45 [INFO] 📍 Found executable: C:\Program Files\Google\Chrome\Application\chrome.exe
2024-05-21 14:30:45 [INFO] ▶️  Launching executable: ...
2024-05-21 14:30:48 [INFO] ✅✅✅ VERIFIED: chrome.exe is running
```

## ⚡ INTEGRATION WITH VOICE SYSTEM

### In your VoiceEngine or AI module:

```python
from executor import executor
from planner_ai import create_plan

# User speaks: "Open Chrome and search Virat Kohli"
user_command = "Open Chrome and search Virat Kohli"

# Create plan from natural language
plan = create_plan(user_command)  # Returns JSON plan

# Execute the plan
results = executor.execute_plan(plan)

# Check results
if all(r['success'] for r in results):
    print("✅ All actions completed successfully")
else:
    failed = [r for r in results if not r['success']]
    print(f"❌ {len(failed)} actions failed")
    for fail in failed:
        print(f"   - {fail['error']}")
```

## 🧪 VERIFICATION EXAMPLES

### Verify Chrome Opens (with process check)
```python
result = executor.tool_open_chrome()
assert result['success'] == True
assert result['verified'] == True
assert result['process'] == 'chrome.exe'
print("✅ Chrome verified running")
```

### Verify Folder Created (with existence check)
```python
result = executor.tool_create_folder("TestFolder", "C:\\Users\\...\\Desktop")
assert result['success'] == True
assert result['exists'] == True
print("✅ Folder verified exists")
```

### Verify File Deleted (with non-existence check)
```python
result = executor.tool_delete_file("C:\\Users\\...\\Desktop\\file.txt")
assert result['success'] == True
assert result['verified'] == True
print("✅ File verified deleted")
```

### Verify Screenshot Saved (with file size check)
```python
result = executor.tool_screenshot()
assert result['success'] == True
assert result['verified'] == True
assert result['size'] > 1000  # Should be larger than 1KB
print(f"✅ Screenshot verified saved ({result['size']} bytes)")
```

## 🎯 IMPORTANT NOTES

### ✅ DO USE:
- `open_chrome(url)` for specific URLs
- `google_search(query)` for Google searches
- `youtube_search(query)` for YouTube
- `type(text)` for text input
- `hotkey()` for keyboard shortcuts
- `screenshot()` to verify screen state

### ❌ DON'T USE (Not Implemented):
- `send_email` - Not production ready
- `send_whatsapp_message` - Not production ready
- `create_spreadsheet` - Use open_excel instead
- `run_python_script` - Run directly, don't use executor
- Any tool not listed in executor.py

### ⚠️ IMPORTANT:
- Always add `wait` between app openings
- Use absolute paths for file operations
- Check logs for detailed debugging
- If action fails, check log file for why
- Return success ONLY after verification passes

## 🐛 TROUBLESHOOTING

### Chrome Not Opening?
```python
# Check log for exact error
result = executor.tool_open_chrome()
print(result['error'])

# Possible issues:
# 1. Chrome not installed
# 2. Path incorrect
# 3. Permission denied
```

### File Operation Failed?
```python
# Always use full paths
❌ WRONG: executor.tool_delete_file("myfile.txt")
✅ CORRECT: executor.tool_delete_file("C:\\Users\\YourName\\Desktop\\myfile.txt")
```

### Typing Not Working?
```python
# Must have window focused
executor.tool_open_notepad()
executor.tool_wait(seconds=2)  # Wait for window to open
executor.tool_type("Hello")  # Now it will type
```

### Screenshot Blank?
```python
# Verify no lock screen is active
executor.tool_screenshot()
# Check saved file location
# File should be > 1000 bytes
```

## 📞 SUPPORT

For issues:
1. Check `executor_production.log` for details
2. Verify all paths are absolute paths
3. Ensure dependencies installed: `pip install psutil pyautogui pygetwindow`
4. Check Windows Defender/Antivirus not blocking
5. Run with Administrator privileges if needed

---

**Status**: ✅ PRODUCTION READY
**Real Automation**: YES
**Verified Execution**: YES
**No Fake Success**: YES
