# 🔥 JARVIS 1.0 - COMPLETE LOCAL SETUP GUIDE

## ✅ What's Working
- Frontend (React app)
- Voice recognition
- YouTube/Browser tasks
- API connections

## ❌ What's Not Working
- VS Code opening
- Folder creation
- Local task execution
- **Because BACKEND IS NOT RUNNING**

---

## 🚀 STEP 1: Install Dependencies (One-Time Only)

### Backend Dependencies
```powershell
cd "D:\e drive\Only_Project\jarvis1.0"

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install required packages
pip install -r Backend/requirements.txt

# Verify installation
pip list | findstr "flask pyautogui ollama"
```

### Required Packages
The backend needs these to work (should be in requirements.txt):
- `flask` - Web server
- `flask-cors` - Handle cross-origin requests
- `pyautogui` - Control mouse/keyboard
- `ollama` - Local AI model (optional, for advanced planning)
- `python-dotenv` - Environment variables

### Check Requirements
```powershell
# View what's needed
type Backend\requirements.txt
```

---

## 🚀 STEP 2: Start Ollama (If Using Local Models)

Ollama is needed for task planning. If you don't have it, install from: https://ollama.ai

```powershell
# Check if Ollama is running
curl http://127.0.0.1:11434/api/tags

# If not running, start it:
ollama serve

# Or pull a model:
ollama pull llama2
```

---

## 🚀 STEP 3: Start the Backend Server

### Method 1: Direct Python (Recommended)
```powershell
# Navigate to project root
cd "D:\e drive\Only_Project\jarvis1.0"

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Go to Backend folder
cd Backend

# Start the server
python app.py
```

**Expected Output:**
```
WARNING in app.run() when it is not in development mode
 * Serving Flask app 'app' (lazy loading)
 * Environment: production
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### Method 2: Using npm script (If configured)
```powershell
npm run backend
```

### Method 3: Start in Background (PowerShell)
```powershell
$env:FLASK_APP="Backend/app.py"
$env:FLASK_ENV="development"

Start-Process python -ArgumentList "Backend/app.py" -NoNewWindow
```

---

## 🔍 STEP 4: Verify Backend is Running

### Check 1: Port is Open
```powershell
netstat -ano | findstr :5000
```
**Should show**: `LISTENING`

### Check 2: Health Endpoint
```powershell
curl http://127.0.0.1:5000/health
```
**Should return**: `{"success":true}`

### Check 3: Root Endpoint
```powershell
curl http://127.0.0.1:5000/
```
**Should return**: `{"success":true,"message":"Jarvis AI Backend Running"}`

### Check 4: Browser Console
Open http://localhost:5173 and check console:
- Should see: `[BackendExecutor] Backend healthy`
- Should NOT see: `Health failed`

---

## 🎯 STEP 5: Test the Full System

### Test 1: Open Notepad via Voice
1. Open browser to http://localhost:5173
2. Click microphone button
3. Say: "Open Notepad"
4. **Expected**: Notepad opens

### Test 2: Create Folder via Voice
1. Click microphone
2. Say: "Create a folder named TestJarvis on Desktop"
3. **Expected**: Folder appears on Desktop

### Test 3: Open VS Code
1. Click microphone
2. Say: "Open VS Code"
3. **Expected**: VS Code opens

---

## 🔧 Troubleshooting Startup Issues

### Issue: "ModuleNotFoundError: No module named 'flask'"
**Solution**:
```powershell
pip install flask flask-cors
```

### Issue: "Ollama connection refused"
**Solution**: Ollama isn't running
```powershell
# Start Ollama
ollama serve

# Or install from: https://ollama.ai
```

### Issue: "Port 5000 already in use"
**Solution**: Kill the process on port 5000
```powershell
netstat -ano | findstr :5000
# Find PID in output, then:
taskkill /PID <PID> /F

# Or use our helper:
Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue | 
  ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }
```

### Issue: "CORS error in browser"
**Solution**: Backend CORS is configured, but check:
```powershell
# Make sure Flask-CORS is installed
pip install flask-cors

# Verify app.py has: CORS(app)
```

---

## 📋 Complete Startup Script

Create a file: `start_backend.ps1`

```powershell
# =========================================
# JARVIS BACKEND STARTUP SCRIPT
# =========================================

Write-Host "🚀 Starting Jarvis Backend..." -ForegroundColor Green

# Kill existing processes
Write-Host "Stopping old backend processes..." -ForegroundColor Yellow
Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue | 
  ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }

Start-Sleep -Seconds 1

# Navigate to project
$projectPath = "D:\e drive\Only_Project\jarvis1.0"
Set-Location $projectPath

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1

# Navigate to backend
Set-Location Backend

# Start the server
Write-Host "Starting Flask server on http://127.0.0.1:5000..." -ForegroundColor Green
python app.py
```

**To use this script:**
```powershell
# Set execution policy
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned

# Run the script
& "D:\e drive\Only_Project\jarvis1.0\start_backend.ps1"
```

---

## 📊 Startup Checklist

- [ ] Virtual environment activated (`.venv`)
- [ ] All pip packages installed
- [ ] Ollama running (if needed)
- [ ] Port 5000 not in use
- [ ] No firewall blocking port 5000
- [ ] Flask server started and shows "Running on http://127.0.0.1:5000"
- [ ] Browser can reach http://127.0.0.1:5000/health
- [ ] Frontend shows "Backend healthy" in console

---

## 🎯 Expected Behavior When Working

### Console Output (Backend)
```
WARNING in app.run() when it is not in development mode
 * Serving Flask app 'app' (lazy loading)
 * Environment: production
 * Debug mode: on
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### Console Output (Frontend)
```
[BackendExecutor] Backend healthy
[BackendExecutor] Executing: open notepad
[BackendExecutor] Result: {...}
[BackendExecutor] Task success
```

### Working Commands
- ✅ "Open Notepad"
- ✅ "Open VS Code"
- ✅ "Open Calculator"
- ✅ "Create a folder named Test on Desktop"
- ✅ "Create a folder named Jyoti on D drive"
- ✅ "Search Google for Python"

---

## 🔄 Daily Startup Process

Every time you want to use Jarvis locally:

1. **Start Backend** (in Terminal 1)
   ```powershell
   cd "D:\e drive\Only_Project\jarvis1.0"
   .\.venv\Scripts\Activate.ps1
   cd Backend
   python app.py
   ```

2. **Start Frontend** (in Terminal 2)
   ```powershell
   cd "D:\e drive\Only_Project\jarvis1.0"
   npm run dev
   ```

3. **Open Browser**
   - Go to http://localhost:5173
   - Check console for "Backend healthy"
   - Start using voice commands

---

## 🆘 Emergency Troubleshooting

### Nothing is working?

1. **Check Backend Running**
   ```powershell
   curl http://127.0.0.1:5000/health
   ```

2. **Check Port Open**
   ```powershell
   netstat -ano | findstr :5000
   ```

3. **Check Frontend Connected**
   - Open http://localhost:5173
   - Press F12 (Developer Tools)
   - Go to Console tab
   - Look for `[BackendExecutor]` messages

4. **Restart Everything**
   - Close both terminals
   - Kill port 5000: `taskkill /PID <PID> /F`
   - Start backend again
   - Start frontend again
   - Refresh browser

5. **Check Logs**
   - Backend logs: Terminal where app.py is running
   - Frontend logs: Browser Developer Tools → Console
   - System logs: Windows Event Viewer

---

## 📚 File Structure Reminder

```
jarvis1.0/
├── Backend/
│   ├── app.py              (Main Flask server)
│   ├── executor.py         (Execute commands)
│   ├── planner_ai.py       (Plan tasks)
│   ├── config.py           (Configuration)
│   └── requirements.txt     (Dependencies)
├── src/
│   ├── services/
│   │   ├── VoiceEngine.js  (Speech recognition)
│   │   └── BackendExecutor.js
│   └── components/
│       └── JarvisHUD.jsx   (Main UI)
└── .venv/                  (Virtual environment)
```

---

## 💾 System Requirements

- **Python 3.8+**
- **Node.js 16+**
- **Windows 10/11**
- **4GB RAM minimum**
- **Internet connection** (for browser tasks)
- **Microphone** (for voice commands)

---

## ✅ Verification Commands

```powershell
# Check Python
python --version

# Check Node
node --version

# Check pip packages
pip list | findstr "flask pyautogui"

# Check ports
netstat -ano | findstr :5000 :5173 :11434

# Check Ollama
curl http://127.0.0.1:11434/api/tags

# Check Backend Health
curl http://127.0.0.1:5000/health

# Check Frontend
curl http://localhost:5173
```

---

## 📞 If Still Not Working

1. **Screenshot errors** from both terminals
2. **Copy console logs** from browser (F12)
3. **Check file permissions**: `icacls "D:\e drive\Only_Project\jarvis1.0"`
4. **Try different ports** if 5000 is blocked
5. **Disable antivirus** temporarily (might block app opening)

---

**Last Updated**: May 21, 2026
**Status**: Ready for local use
