# SETUP & DEPLOYMENT GUIDE - Autonomous AI Agent v3

## Prerequisites

- **Python 3.10+** (tested on 3.11)
- **Windows 10/11** (macOS and Linux support coming)
- **8GB+ RAM** (for OCR engines)
- **Active Internet** (for LLM APIs)
- **Administrative Access** (for some app launches)

## Step 1: Setup Python Environment

```bash
# Navigate to project
cd "d:\e drive\Only_Project\jarvis1.0"

# Create virtual environment
python -m venv .venv

# Activate it (Windows)
.venv\Scripts\Activate.ps1

# Activate it (macOS/Linux)
source .venv/bin/activate

# Verify activation
python --version  # Should be 3.10+
```

## Step 2: Install Dependencies

```bash
cd Backend

# Install all packages
pip install -r requirements.txt

# This will install:
# - Flask (web framework)
# - Google Generative AI (Gemini)
# - Anthropic (Claude fallback)
# - EasyOCR (screen reading)
# - PyAutoGUI (computer control)
# - OpenCV (image processing)
# - Playwright (browser automation)
# - And many more...

# Installation may take 5-10 minutes
```

### If Installation Fails

```bash
# For Tesseract on Windows (optional but recommended):
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
# Install to: C:\Program Files\Tesseract-OCR

# For EasyOCR issues:
pip install --upgrade easyocr

# For PyAutoGUI issues:
pip install --upgrade pyautogui
```

## Step 3: Setup API Keys

### Get Gemini API Key

1. Go to https://aistudio.google.com
2. Click "Get API key"
3. Create new API key
4. Copy the key

### Get Claude API Key (Optional)

1. Go to https://console.anthropic.com
2. Get API key
3. Copy the key

### Set Environment Variables

**Windows PowerShell:**
```powershell
$env:GEMINI_API_KEY = "your-gemini-key-here"
$env:ANTHROPIC_API_KEY = "your-claude-key-here"  # Optional
```

**Windows CMD:**
```cmd
setx GEMINI_API_KEY "your-gemini-key-here"
setx ANTHROPIC_API_KEY "your-claude-key-here"
```

**macOS/Linux:**
```bash
export GEMINI_API_KEY="your-gemini-key-here"
export ANTHROPIC_API_KEY="your-claude-key-here"
```

**Or create .env file:**
```
GEMINI_API_KEY=your-key-here
ANTHROPIC_API_KEY=your-key-here
```

## Step 4: Test Installation

```bash
cd Backend

# Test imports
python -c "import google.generativeai; print('✅ Gemini OK')"
python -c "import easyocr; print('✅ EasyOCR OK')"
python -c "import pyautogui; print('✅ PyAutoGUI OK')"

# Should see ✅ for each
```

## Step 5: Start the Backend Server

```bash
cd Backend

# Run Flask app
python app.py

# You should see:
# 🚀 Starting Autonomous AI Server v3...
# ✅ Architecture: OTAV (Observe → Think → Act → Verify)
# ✅ Mode: Full Dynamic Reasoning - NO Hardcoding
# WARNING in app.run Running on http://127.0.0.1:5000
```

## Step 6: Start the Frontend

**In a NEW terminal:**

```bash
# From project root
cd "d:\e drive\Only_Project\jarvis1.0"

# Install frontend dependencies (if not done yet)
npm install

# Start frontend dev server
npm run dev

# Should see:
# ➜  Local:   http://localhost:5173/
# ➜  press h to show help
```

## Step 7: Verify Full Stack

1. **Backend Running**: http://localhost:5000/health
   - Should return: `{"status": "healthy", ...}`

2. **Frontend Running**: http://localhost:5173
   - Should see Jarvis UI

3. **Test Connection**:
   ```bash
   curl -X POST http://localhost:5000/api/autonomous/execute \
     -H "Content-Type: application/json" \
     -d '{"task":"take a screenshot"}'
   ```

## Testing the System

### Test 1: Basic Task

**API Call:**
```bash
curl -X POST http://localhost:5000/api/autonomous/execute \
  -H "Content-Type: application/json" \
  -d '{"task":"take a screenshot"}'
```

**Expected Response:**
```json
{
  "success": true,
  "status": "completed",
  "task": "take a screenshot",
  "result": {
    "status": "completed",
    "phases": {
      "observe": {...},
      "think": {"actions": 1},
      "act": {...},
      "verify": {"success": true}
    }
  }
}
```

### Test 2: Website Search

**API Call:**
```bash
curl -X POST http://localhost:5000/api/autonomous/execute \
  -H "Content-Type: application/json" \
  -d '{"task":"open google and search for python tutorial"}'
```

**Expected Behavior:**
1. Opens Google
2. Finds search box (using OCR)
3. Clicks search box
4. Types "python tutorial"
5. Presses Enter
6. Returns success

### Test 3: Folder Creation

**API Call:**
```bash
curl -X POST http://localhost:5000/api/autonomous/execute \
  -H "Content-Type: application/json" \
  -d '{"task":"create folder MyAwesomeProject on desktop"}'
```

**Expected Result:**
- Folder created at: `C:\Users\<username>\Desktop\MyAwesomeProject`

### Test 4: Plan Generation Only

**API Call:**
```bash
curl -X POST http://localhost:5000/api/plan \
  -H "Content-Type: application/json" \
  -d '{"task":"search machine learning on youtube"}'
```

**Expected Response:**
```json
{
  "success": true,
  "task": "search machine learning on youtube",
  "plan": [
    {"tool": "open_website", "params": {"url": "https://youtube.com"}},
    {"tool": "wait", "params": {"seconds": 3}},
    {"tool": "click_text", "params": {"text": "search"}},
    ...
  ],
  "action_count": 5
}
```

### Test 5: From Frontend UI

1. Open http://localhost:5173
2. Click on text input
3. Say (or type): "open youtube"
4. Click "Execute" or press Enter
5. Watch the agent execute:
   - Takes screenshot
   - Plans action
   - Opens YouTube
   - Verifies success

## Performance Testing

### Basic Operations

```python
import requests
import time

endpoint = "http://localhost:5000/api/autonomous/execute"

# Test 1: Screenshot (fastest)
start = time.time()
requests.post(endpoint, json={"task": "take a screenshot"})
print(f"Screenshot: {time.time() - start:.2f}s")

# Test 2: Simple click (medium)
start = time.time()
requests.post(endpoint, json={"task": "click on the center of screen"})
print(f"Click: {time.time() - start:.2f}s")

# Test 3: Website search (slower)
start = time.time()
requests.post(endpoint, json={"task": "search hello on google"})
print(f"Website search: {time.time() - start:.2f}s")
```

### Expected Performance

| Task | Time | Notes |
|------|------|-------|
| Screenshot | 1-2s | Fastest |
| Click | 2-3s | Fast |
| Type | 3-4s | Depends on text length |
| Website load | 5-8s | Depends on site |
| Search | 8-15s | Multiple steps |
| Complex workflow | 30-60s | Many actions |

## Troubleshooting

### Issue: "No GEMINI_API_KEY"

**Solution:**
```bash
# Check if key is set
echo $env:GEMINI_API_KEY  # PowerShell
echo $GEMINI_API_KEY      # Linux/Mac

# If empty, set it:
$env:GEMINI_API_KEY = "paste-your-key-here"
```

### Issue: "Screen reader unavailable"

**Solution:**
```bash
# EasyOCR needs to download model (first run only)
python -c "import easyocr; reader = easyocr.Reader(['en'])"

# If fails, manually install:
pip install --upgrade easyocr

# For Tesseract on Windows:
# Download: https://github.com/UB-Mannheim/tesseract/wiki
# Install to: C:\Program Files\Tesseract-OCR
```

### Issue: "click_text not finding text"

**Solution:**
1. Check if text is visible
2. Try using coordinates instead: `{"tool": "click", "params": {"x": 100, "y": 100}}`
3. Add more wait time before click

### Issue: "Backend not responding"

**Solution:**
```bash
# Check if Flask is running
netstat -ano | findstr :5000  # Windows

# Kill port if stuck
Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess | Stop-Process -Force

# Restart Flask
python app.py
```

### Issue: "High latency / Slow performance"

**Solution:**
1. Use local LLM (Ollama) instead of Gemini
2. Reduce screenshot resolution
3. Disable OCR verification for speed
4. Use faster internet connection

## Configuration Tuning

### For Better Accuracy

In `executor_universal.py`:
```python
MAX_RETRIES = 5  # Retry more times
# Add screenshots between each action
```

In `planner_ai.py`:
```python
temperature = 0.3  # Lower = more consistent plans
```

### For Faster Speed

In `executor_universal.py`:
```python
MAX_RETRIES = 1  # Retry less
pyautogui.PAUSE = 0.2  # Faster actions
```

### For Local LLM (Ollama)

```bash
# Download Ollama: https://ollama.ai
# Run Ollama: ollama run mistral

# Update planner_ai.py to use local model
# (Implementation coming soon)
```

## Common Use Cases

### Use Case 1: Search YouTube

```json
{
  "task": "search cat videos on youtube"
}
```

### Use Case 2: Create Project Folder

```json
{
  "task": "create folder my-web-project on desktop"
}
```

### Use Case 3: Open Multiple Apps

```json
{
  "task": "open vs code, create new folder called src inside"
}
```

### Use Case 4: Email Check

```json
{
  "task": "open gmail and check unread emails"
}
```

### Use Case 5: Social Media

```json
{
  "task": "open twitter and search for javascript news"
}
```

## Production Deployment

### For Production:

1. **Use Gunicorn instead of Flask dev server:**
   ```bash
   pip install gunicorn
   gunicorn -w 4 app:app -b 127.0.0.1:5000
   ```

2. **Setup HTTPS:**
   ```bash
   # Use Let's Encrypt
   pip install python-certbot
   ```

3. **Rate Limiting:**
   ```python
   from flask_limiter import Limiter
   # Implement rate limiting
   ```

4. **Monitoring:**
   ```bash
   # Setup logging to file
   # Monitor agent performance
   ```

## Uninstall

```bash
# Remove virtual environment
deactivate
rm -r .venv  # Or delete folder manually

# Clean pip cache
pip cache purge
```

---

## Next Steps

1. ✅ **Installation** - Follow steps above
2. ✅ **Testing** - Run test cases
3. ✅ **Usage** - Use from frontend or API
4. ⏭️ **Customization** - Add your own actions
5. ⏭️ **Deployment** - Deploy to cloud

## Support

- **Issue with setup?** Check [TROUBLESHOOTING section](#troubleshooting)
- **Error logs?** Check `Backend/logs/` folder
- **API questions?** Check `API_REFERENCE.md`
- **Architecture?** Check `ARCHITECTURE_DYNAMIC.md`

---

**Happy autonomous agent testing! 🚀**
