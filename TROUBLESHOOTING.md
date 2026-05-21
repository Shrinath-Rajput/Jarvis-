# 🔧 Jarvis 1.0 - Troubleshooting Guide

## Problem: Speech Recognition Still Shows "Already Started" Error

### Diagnosis
```javascript
// Error: InvalidStateError: Failed to execute 'start' on 'SpeechRecognition': 
// recognition has already started
```

### Causes & Solutions

**Cause 1**: Browser cache issue
- **Solution**: Clear browser cache and reload the page
- **How**: Ctrl+Shift+Delete → Select "All time" → Clear data

**Cause 2**: Multiple page tabs open
- **Solution**: Close other Jarvis tabs and keep only one active
- **How**: Only one browser tab with Jarvis should be open

**Cause 3**: Rapid voice clicks
- **Solution**: Wait for previous command to complete before clicking mic again
- **How**: Listen for "Speech ended" in console before next command

**Cause 4**: Browser microphone locked
- **Solution**: Check browser microphone permissions
- **How**: Click lock icon in address bar → Allow microphone access

---

## Problem: Notepad/VS Code Not Opening

### Diagnosis
```
[BackendExecutor] Task failed
Error: Failed to open app
```

### Causes & Solutions

**Cause 1**: Backend not running
- **Solution**: Start the backend server
- **How**:
  ```powershell
  cd Backend
  python app.py
  ```

**Cause 2**: Wrong app name format
- **Solution**: Use standard app names
- **Correct Names**:
  - ✅ "Notepad" or "notepad"
  - ✅ "VS Code" or "vs code"
  - ✅ "Calculator"
  - ❌ "text editor"
  - ❌ "code editor"

**Cause 3**: Application not installed
- **Solution**: Install the application
- **Check**: 
  ```powershell
  # For Notepad (Windows built-in, should exist)
  where.exe notepad.exe
  
  # For VS Code
  where.exe code
  ```

**Cause 4**: Path issues on specific drives
- **Solution**: Ensure drive letters are correct
- **Test Command**: "Create a folder named Test on C drive"

---

## Problem: Folder Not Created

### Diagnosis
```
[BackendExecutor] Task success (but folder not found)
or
[BackendExecutor] Task failed
```

### Causes & Solutions

**Cause 1**: Folder created on wrong location
- **Solution**: Check Desktop or specified path
- **How**:
  ```powershell
  # Check Desktop
  Get-ChildItem "$env:USERPROFILE\Desktop" | Where-Object {$_.Name -like "*Jyoti*"}
  
  # Check D drive
  Get-ChildItem "D:\" | Where-Object {$_.Name -like "*Jyoti*"}
  ```

**Cause 2**: Permission denied
- **Solution**: Run application as Administrator
- **How**: Right-click PowerShell → Run as Administrator

**Cause 3**: Drive doesn't exist
- **Solution**: Use valid drive letters
- **Check**:
  ```powershell
  Get-Volume  # List all drives
  ```

**Cause 4**: Special characters in folder name
- **Solution**: Avoid special characters
- **Good Names**: "Jyoti", "TestFolder", "MyProject"
- **Bad Names**: "Test<>", "Folder|Name", "File*"

---

## Problem: Multiple Consecutive Commands Fail

### Diagnosis
```
First command works, subsequent commands fail
```

### Causes & Solutions

**Cause 1**: Voice recognition not properly stopped
- **Solution**: Fixed in this update (isListening flag)
- **Check**: See console for "Speech ended" message

**Cause 2**: Backend rate limiting
- **Solution**: Add small delay between commands
- **How**: In JarvisHUD.jsx, ensure proper error handling

**Cause 3**: Memory leak in voice engine
- **Solution**: Clear old event listeners
- **What Fixed**: Updated listen() method now properly cleans up

---

## Problem: Backend Returns 500 Error

### Diagnosis
```
BackendExecutor] Failed: HTTP 500
```

### Causes & Solutions

**Cause 1**: Planner model not found
- **Check**: Ensure Ollama is running with correct model
- **Fix**:
  ```powershell
  # Check Ollama
  curl http://127.0.0.1:11434/api/tags
  
  # Start Ollama if needed
  ollama serve
  ```

**Cause 2**: Executor error
- **Check**: Look at backend console for detailed error
- **Debug**: Run executor test:
  ```python
  python -c "from Backend.executor import executor; print(executor.tool_open_app('notepad'))"
  ```

**Cause 3**: Task parsing error
- **Check**: Verify task format in logs
- **Debug**: Check planner_ai.py system prompt

---

## Verification Steps

### 1. Check Backend Running
```powershell
# Check port 5000
netstat -ano | findstr :5000

# Test health
curl http://127.0.0.1:5000/health
```

### 2. Check Ollama Running (for local models)
```powershell
# Check port 11434
netstat -ano | findstr :11434

# Test Ollama
curl http://127.0.0.1:11434/api/tags
```

### 3. Check Frontend Connected
Open browser console (F12) and look for:
- ✅ "[BackendExecutor] Backend healthy"
- ❌ "[BackendExecutor] Health failed:"

### 4. Test Voice Recognition
```javascript
// In browser console
navigator.mediaDevices.getUserMedia({audio: true})
  .then(() => console.log("✅ Microphone access granted"))
  .catch(e => console.log("❌ Microphone denied:", e))
```

---

## Debug Mode

### Enable Detailed Logging

**In Backend (app.py)**:
```python
DEBUG = True  # Already set in config.py
```

**In Frontend (VoiceEngine.js)**:
```javascript
// Already has console.log statements
// Check browser console for detailed messages
```

### Run Test Script
```powershell
cd "D:\e drive\Only_Project\jarvis1.0"
python test_fixes.py
```

---

## Quick Fixes Checklist

- [ ] Backend running on port 5000
- [ ] Frontend can connect to backend  
- [ ] Ollama running on port 11434 (if using local models)
- [ ] Browser has microphone permission
- [ ] Only one Jarvis tab open
- [ ] Browser cache cleared
- [ ] Using correct app names
- [ ] Target paths exist and are writable
- [ ] No special characters in folder names

---

## Performance Optimization

### If Commands Are Slow

1. **Check Backend Logs**: Look for timeout messages
2. **Optimize Planner**: Reduce max_steps in BackendExecutor.js (currently 50)
3. **Use Faster Model**: If using Ollama, use a faster model
4. **Monitor Resources**: Check CPU/RAM usage

### If Speech Recognition Lags

1. **Reduce Interim Updates**: Modify VoiceEngine.js
2. **Disable Wake Word**: In JarvisHUD component
3. **Close Other Apps**: Free up system resources

---

## Getting Help

### Information to Provide When Asking for Help

1. **Error Message**: Copy exact error from console
2. **Console Logs**: F12 → Console → Screenshot of errors
3. **Backend Logs**: Terminal output from `python app.py`
4. **Steps to Reproduce**: Exactly what you did before error
5. **System Info**:
   ```powershell
   python --version
   node --version
   Get-Volume
   ```

---

## Files Modified & Where to Check

| File | Purpose | Check |
|------|---------|-------|
| `src/services/VoiceEngine.js` | Speech recognition | Look for `isListening` flag |
| `Backend/executor.py` | App opening & folder creation | App name mappings |
| `Backend/planner_ai.py` | Task planning | System prompt examples |
| `Backend/config.py` | Configuration | GEMINI_MODEL, OLLAMA_* |

---

## Common Voice Commands That Should Work

```
✅ "Open Notepad"
✅ "Open VS Code"  
✅ "Open Calculator"
✅ "Create a folder named MyFolder on Desktop"
✅ "Create a folder named Jyoti on the D drive"
✅ "Search Google for Python"
✅ "Open YouTube"
✅ "Open Gemini and search for code"

❌ "Open text editor" (be specific: "Open Notepad")
❌ "Make a folder" (say: "Create a folder")
❌ "Go to D drive" (say: "Create folder on D drive")
```

---

## Latest Fixes (May 21, 2026)

- ✅ Speech recognition double-start error fixed
- ✅ App opening improved with Windows mappings
- ✅ Folder creation with flexible paths
- ✅ Better error handling and fallbacks
- ✅ Enhanced task planning prompts

See `FIXES_APPLIED.md` for complete details.

---

**Last Updated**: May 21, 2026
**Version**: 1.0
