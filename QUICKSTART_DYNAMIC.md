# QUICK START - Autonomous AI Agent v3

**⚡ Get running in 10 minutes!**

## Prerequisites
- Python 3.10+
- Gemini API key: https://aistudio.google.com

## Step 1: Setup (5 minutes)

```bash
# Navigate to project
cd "d:\e drive\Only_Project\jarvis1.0"

# Activate environment (Windows)
.venv\Scripts\Activate.ps1

# Or create if needed:
python -m venv .venv
.venv\Scripts\Activate.ps1

# Go to backend
cd Backend

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Add API Key (1 minute)

**Windows PowerShell:**
```powershell
$env:GEMINI_API_KEY = "your-gemini-key-from-https://aistudio.google.com"
```

**Verify:**
```powershell
echo $env:GEMINI_API_KEY  # Should print your key
```

## Step 3: Start Backend (1 minute)

```bash
python app.py

# You should see:
# 🚀 Starting Autonomous AI Server v3...
# ✅ Architecture: OTAV
# WARNING in app.run Running on http://127.0.0.1:5000
```

## Step 4: Test Backend (1 minute)

**In a NEW terminal:**

```bash
# Test if server is running
curl http://localhost:5000/health

# Should show: {"success": true, "status": "healthy", ...}
```

## Step 5: Start Frontend (1 minute)

**In a NEW terminal:**

```bash
cd "d:\e drive\Only_Project\jarvis1.0"
npm install  # Only first time
npm run dev

# You should see:
# ➜  Local:   http://localhost:5173/
```

## Step 6: Use the Agent! (0 minutes)

1. Open browser: http://localhost:5173
2. Click text input
3. Say anything:
   - "search cat videos on youtube"
   - "create folder my-project on desktop"
   - "open google"
   - "take a screenshot"
4. Press Enter or click Execute
5. Watch it work! 🚀

---

## Quick Test Examples

### Via Terminal (cURL)

```bash
# Example 1: Take screenshot
curl -X POST http://localhost:5000/api/autonomous/execute \
  -H "Content-Type: application/json" \
  -d '{"task":"take a screenshot"}'

# Example 2: Open website
curl -X POST http://localhost:5000/api/autonomous/execute \
  -H "Content-Type: application/json" \
  -d '{"task":"open google"}'

# Example 3: Search
curl -X POST http://localhost:5000/api/autonomous/execute \
  -H "Content-Type: application/json" \
  -d '{"task":"search python on google"}'

# Example 4: Create folder
curl -X POST http://localhost:5000/api/autonomous/execute \
  -H "Content-Type: application/json" \
  -d '{"task":"create folder test-project on desktop"}'
```

### Via JavaScript

```javascript
// Paste in browser console at http://localhost:5173

const executeTask = async (task) => {
  const response = await fetch('http://localhost:5000/api/autonomous/execute', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ task })
  });
  const result = await response.json();
  console.log('Result:', result);
  return result;
};

// Use it:
executeTask("search machine learning on youtube");
executeTask("take a screenshot");
executeTask("create folder my-app on desktop");
```

---

## What It Does

When you execute a task, the agent:

1. **OBSERVES** 👁️
   - Takes screenshot
   - Reads visible text using OCR
   - Detects current window

2. **THINKS** 🧠
   - Sends task to Gemini AI
   - Generates action plan
   - Returns JSON actions

3. **ACTS** ⚡
   - Executes each action
   - Retries if failed
   - Takes screenshots between actions

4. **VERIFIES** ✅
   - Checks if task succeeded
   - Compares before/after
   - Returns status

---

## Common Issues

### Issue: "No GEMINI_API_KEY"

```powershell
$env:GEMINI_API_KEY = "paste-your-key-here"
```

### Issue: "Backend not responding"

Make sure Flask is running:
```bash
python app.py  # In Backend folder
```

### Issue: "Frontend not loading"

Make sure you have npm installed:
```bash
npm install
npm run dev
```

### Issue: "Text not found"

The OCR didn't detect the text. Try:
- Clicking coordinates instead
- Adding wait time before click
- Check if text is visible on screen

---

## Next Steps

1. ✅ Get it running (you're here!)
2. 📚 Read [ARCHITECTURE_DYNAMIC.md](ARCHITECTURE_DYNAMIC.md) for deep dive
3. 📖 Check [API_REFERENCE_DYNAMIC.md](API_REFERENCE_DYNAMIC.md) for all endpoints
4. 🔧 Read [SETUP_GUIDE_DYNAMIC.md](SETUP_GUIDE_DYNAMIC.md) for advanced config

---

## Task Ideas to Try

```
"open youtube and search for kubernetes"
"create 3 folders on desktop: src, public, build"
"search tensorflow on github"
"open gmail and check inbox"
"create folder my-web-project on desktop"
"search javascript tutorials on google"
"open twitter and search for ai news"
"take a screenshot"
```

---

## Key Files

| File | Purpose |
|------|---------|
| `planner_ai.py` | LLM-based planning |
| `executor_universal.py` | Universal action executor |
| `screen_understanding_enhanced.py` | OCR engine |
| `autonomous_agent_enhanced_new.py` | OTAV orchestrator |
| `app.py` | Flask API |

---

## Architecture (1-minute summary)

```
User Input
    ↓
Planner: "Think about what to do"
    ↓
Executor: "Do it"
    ↓
Screen Reader: "Check if it worked"
    ↓
Result
```

**NO IF STATEMENTS. NO HARDCODING. Pure AI reasoning.**

---

## Troubleshooting Checklist

- [ ] Python 3.10+ installed? `python --version`
- [ ] Virtual env activated? `echo $env:PYTHON_PATH`
- [ ] Dependencies installed? `pip list | grep flask`
- [ ] Gemini key set? `echo $env:GEMINI_API_KEY`
- [ ] Backend running? `curl http://localhost:5000/health`
- [ ] Frontend running? Open http://localhost:5173

---

## Performance

- **Simple tasks**: 2-5 seconds
- **Website searches**: 8-15 seconds
- **Complex workflows**: 30-60 seconds

---

## Support

- **Setup issues?** → [SETUP_GUIDE_DYNAMIC.md](SETUP_GUIDE_DYNAMIC.md)
- **API questions?** → [API_REFERENCE_DYNAMIC.md](API_REFERENCE_DYNAMIC.md)
- **How it works?** → [ARCHITECTURE_DYNAMIC.md](ARCHITECTURE_DYNAMIC.md)

---

**Ready? Start with Step 1 above! 🚀**
