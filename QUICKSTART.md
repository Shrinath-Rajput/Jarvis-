# 🚀 JARVIS 1.0 - QUICK START (5 Minutes)

## ⚡ TL;DR - Get It Running Now

### Option A: Everything at Once (Easiest)
```
Double-click: START_ALL.bat
```

### Option B: Two Separate Terminals
```
Terminal 1: Double-click START_BACKEND.bat
Terminal 2: Double-click START_FRONTEND.bat
```

---

## 🎯 Step-by-Step Setup (First Time Only)

### STEP 1: Install Backend Dependencies
```powershell
# Open PowerShell in project folder
cd "D:\e drive\Only_Project\jarvis1.0"

# Activate environment
.\.venv\Scripts\Activate.ps1

# Install packages
pip install -r Backend/requirements.txt
```

**Expected Output**: `Successfully installed flask flask-cors pyautogui`

### STEP 2: Start Backend
```powershell
# From the same PowerShell:
cd Backend
python app.py
```

**Expected Output**:
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### STEP 3: Open New Terminal for Frontend
```powershell
# New PowerShell window, navigate to project:
cd "D:\e drive\Only_Project\jarvis1.0"

# Start frontend
npm run dev
```

**Expected Output**:
```
VITE v5.x.x  ready in xxx ms
➜  Local:   http://localhost:5173/
```

### STEP 4: Open Browser
- Go to: http://localhost:5173
- Should see Jarvis HUD interface
- Check browser console (F12):
  - Should see: `[BackendExecutor] Backend healthy`
  - Should NOT see: `Health failed`

---

## 🎤 Try Your First Voice Command

1. **Click the microphone button** (or press Spacebar)
2. **Say**: "Open Notepad"
3. **Expected**: Notepad opens on your screen
4. **Backend Terminal**: Should show detailed logs

---

## ✅ Verify It's Working

### Check 1: Backend Running
```powershell
# In a new PowerShell window:
curl http://127.0.0.1:5000/health
```
Should show: `{"success":true}`

### Check 2: Backend Status
```powershell
curl http://127.0.0.1:5000/status
```
Should show: Backend info and endpoints

### Check 3: Frontend Connected
- Open browser Developer Tools (F12)
- Go to Console tab
- Look for: `[BackendExecutor] Backend healthy`

---

## 🎙️ Working Voice Commands

```
✅ "Open Notepad"
✅ "Open VS Code"
✅ "Open Calculator"
✅ "Create a folder named Test on Desktop"
✅ "Create a folder named MyFolder on D drive"
✅ "Search Google for Python"
✅ "Open YouTube"
✅ "Go to Gemini"
```

---

## 🐛 Quick Troubleshooting

### "Backend offline" Error?
**Problem**: Backend not running  
**Solution**: 
```powershell
# Check if running
netstat -ano | findstr :5000

# If not, start it:
cd "D:\e drive\Only_Project\jarvis1.0\Backend"
python app.py
```

### "Already listening" Error?
**Problem**: Voice recognition overlap  
**Solution**: Fixed in latest update - should work now  
**If persists**: Refresh browser page (Ctrl+R)

### App Won't Open?
**Problem**: Notepad/VS Code not opening  
**Solution**: Check backend logs for errors
```
Look for: ❌ FAILED [tool_open_app]
See what error is shown
```

### Folder Not Created?
**Problem**: create_folder command not working  
**Solution**: Check folder path
- Desktop works: "Create folder on Desktop"
- D drive: "Create folder on D drive"  
- Custom paths: Might need full path

---

## 📊 System Checks

### Pre-Flight Checklist
- [ ] Python 3.8+ installed
- [ ] Node.js 16+ installed
- [ ] Virtual environment (.venv) exists
- [ ] pip packages installed (`pip list | findstr flask`)
- [ ] Port 5000 available (`netstat -ano | findstr :5000` shows nothing)
- [ ] Microphone connected and permissions granted
- [ ] Only ONE browser tab open with Jarvis

### During Use
- [ ] Both terminals running (Backend + Frontend)
- [ ] Browser console shows "Backend healthy"
- [ ] Voice recognition working (micr
ophone active)
- [ ] Backend logs show task execution details

---

## 📁 File Locations

```
D:\e drive\Only_Project\jarvis1.0\
├── START_BACKEND.bat       ← Click to start backend
├── START_FRONTEND.bat      ← Click to start frontend
├── START_ALL.bat           ← Click for both
├── Backend/
│   ├── app.py              (Main server)
│   ├── executor.py         (Task execution)
│   └── planner_ai.py       (Task planning)
└── src/
    └── services/
        └── VoiceEngine.js  (Voice recognition)
```

---

## 🔄 Daily Workflow

Every time you want to use Jarvis:

1. **Start Backend**: Double-click `START_BACKEND.bat`
   - Wait for: `Running on http://127.0.0.1:5000`

2. **Start Frontend**: Double-click `START_FRONTEND.bat`
   - Wait for: `Local: http://localhost:5173`

3. **Open Browser**: Go to `http://localhost:5173`
   - Check console: `[BackendExecutor] Backend healthy`

4. **Use Voice**: Click mic, speak commands

---

## 🎯 Example Session

```
User: "Open Notepad"
→ VoiceEngine captures: "open notepad"
→ Backend receives: {"task": "open notepad"}
→ Planner creates: [{"tool": "open_app", "params": {"app_name": "notepad"}}]
→ Executor runs: subprocess.Popen("notepad.exe")
→ Result: Notepad opens ✅
→ Console: "[BackendExecutor] Task success"
```

---

## 🆘 Emergency Reset

If everything breaks:

```powershell
# Kill all related processes
taskkill /F /IM python.exe /T
taskkill /F /IM node.exe /T

# Clear port 5000
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000') do taskkill /PID %%a /F

# Start fresh
cd "D:\e drive\Only_Project\jarvis1.0"
.\.venv\Scripts\Activate.ps1
cd Backend
python app.py
```

---

## 📞 Getting Help

If something doesn't work:

1. **Check Backend Terminal** for error messages
2. **Check Browser Console** (F12) for frontend errors
3. **Check Windows Event Viewer** for system errors
4. **Try restart**: Close everything, start `START_ALL.bat`
5. **Check logs in**: `FIXES_APPLIED.md` and `TROUBLESHOOTING.md`

---

## ✨ What's Fixed

- ✅ Voice recognition double-start error
- ✅ App opening improvements (Notepad, VS Code, etc.)
- ✅ Folder creation with flexible paths
- ✅ Better error handling and logging
- ✅ Enhanced task planning

---

## 📚 Documentation

- **LOCAL_SETUP_GUIDE.md** - Detailed setup instructions
- **TROUBLESHOOTING.md** - Problem-solving guide
- **FIXES_APPLIED.md** - What was fixed and how
- **test_fixes.py** - Test script to verify all fixes

---

## 🎓 Understanding the Flow

```
Browser (Frontend)
    ↓
[Click Mic] → VoiceEngine.js (speech recognition)
    ↓
[Transcript] → JarvisHUD.jsx (displays & sends)
    ↓
[HTTP POST] → BackendExecutor.js (API call)
    ↓
Backend Server (app.py)
    ↓
[Planner] → Plans the task (planner_ai.py)
    ↓
[Executor] → Executes the plan (executor.py)
    ↓
[Result] → Returns to frontend
    ↓
[Show Result] → JarvisHUD displays outcome
```

---

## 💾 Tips & Tricks

### Faster Startup
- Leave backend running all day
- Only restart frontend if needed
- Refresh browser instead of restarting

### Better Performance
- Close other apps to free RAM
- Use simple commands first
- Wait for "Task complete" before next command

### Debug Mode
- Keep backend terminal in view
- Watch for step-by-step execution logs
- Check console at each stage

---

## 🚀 What Should Happen

### ✅ When Working
```
[BackendExecutor] Backend healthy ✅
[BackendExecutor] Executing: open notepad ✅
[BackendExecutor] Result: {...} ✅
[BackendExecutor] Task success ✅
→ Notepad opens ✅
```

### ❌ When NOT Working
```
[BackendExecutor] Health failed ❌
→ Backend not running
```

---

**Last Updated**: May 21, 2026  
**Status**: Ready to use  
**Support**: See TROUBLESHOOTING.md for issues
