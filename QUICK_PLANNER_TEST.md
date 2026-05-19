# Planner Fix - Quick Start Testing Guide

## What Was Fixed

❌ **Problem:** Autonomous agent generated ZERO execution plans (empty actions)

✅ **Root Cause:** Missing `generate_response()` method in AI classes

✅ **Solution:** Added proper async LLM interface with comprehensive debug logging

---

## Quick Test (2 minutes)

### Step 1: Run Backend
```bash
cd Backend
python app.py
```

Wait for: `✅ Backend ready at http://127.0.0.1:5000`

### Step 2: Open Another Terminal
```bash
cd Backend
python test_planner_debug.py
```

### Step 3: Look for These Outputs

**Good Signs:**
```
✅ PLAN GENERATED:
   Tool: open_website
   Parameters: {"site_name": "youtube"}
   Reasoning: Opening youtube as requested
```

**Bad Sign:**
```
❌ NO PLAN GENERATED
```

### Step 4: Check Log Details
```bash
cat planner_debug.log | grep -A5 "RAW LLM RESPONSE"
```

Should show LLM response received.

---

## What Each Test Does

### Test 1: Fallback Planner Test
Tests if keywords are being recognized:
- "Open YouTube" → Should plan: `open_website` with `youtube`
- "Search Google" → Should plan: `search_google`

### Test 2: LLM Response Test
Tests if LLM is callable:
- Calls `generate_response()` directly
- Shows if Gemini/Ollama is working
- Shows response length and content

### Test 3: Full Planner Test
Tests complete planning pipeline:
- Handles 6 different commands
- Shows tool selection
- Shows parameter generation
- Shows reasoning

---

## Expected Log Output

```
======================================================================
AUTONOMOUS AGENT PLANNER DEBUG TEST
======================================================================

📦 Available Tools (25):
======================================================================
  ✓ close_app
  ✓ create_file
  ✓ create_folder
  ✓ delete_file
  ✓ launch_app
  ✓ open_website
  ✓ press_key
  ✓ search_google
  ✓ search_youtube
  ✓ type_text
  ... (15 more tools)
======================================================================

🧪 Testing Planner with Various Commands:
======================================================================

──────────────────────────────────────────────────────────────────
TEST 1: Open YouTube
──────────────────────────────────────────────────────────────────

✅ PLAN GENERATED:
   Tool: open_website
   Parameters: {"site_name": "youtube"}
   Reasoning: Opening youtube as requested

──────────────────────────────────────────────────────────────────
TEST 2: Open YouTube and search Virat Kohli
──────────────────────────────────────────────────────────────────

✅ PLAN GENERATED:
   Tool: open_website
   Parameters: {"site_name": "youtube"}
   Reasoning: Opening youtube as requested
```

---

## Before vs After

### BEFORE (Broken)
```
User: "Open YouTube"
↓
Planner: generate_response() not found ← ERROR!
↓
Planner returns: None
↓
Result: No actions taken, task fails
```

### AFTER (Fixed)
```
User: "Open YouTube"
↓
Planner: Calls generate_response() ← WORKS!
↓
LLM: Returns {"tool": "open_website", ...}
↓
Planner: Creates plan successfully
↓
Executor: Runs open_website tool
↓
Result: Task completed!
```

---

## Command Reference

| Command | Expected Tool | Parameters |
|---------|---------------|------------|
| Open YouTube | open_website | site_name: youtube |
| Search YouTube for X | search_youtube | query: X |
| Open Chrome | launch_app | app_name: chrome |
| Search Google for X | search_google | query: X |
| Open GitHub | open_website | site_name: github |

---

## Debugging If Test Fails

### If you see: "Response is EMPTY/NONE"

**Check:** Is LLM running?
```bash
# For Gemini: Check API key
cat Backend/config.py | grep GEMINI_API_KEY

# For Ollama: Check if running
curl http://localhost:11434/api/tags
```

### If you see: "Could not parse LLM response"

**Check:** LLM is returning invalid format
- Look in `planner_debug.log` for actual response
- Should be valid JSON
- If not, LLM prompt might be wrong

### If you see: "Tool 'xxx' not found"

**Check:** Tools aren't registered
- Run: `python -c "from tool_registry import get_tool_registry; from tool_implementations import register_all_tools; print(len(get_tool_registry().get_all_tools()))"`
- Should show ~25+ tools

---

## Full Test Details (Optional)

### Individual Component Tests

**1. Check Tool Registry:**
```python
from tool_registry import get_tool_registry
from tool_implementations import register_all_tools

registry = get_tool_registry()
tools = registry.get_all_tools()
print(f"Tools registered: {len(tools)}")
for tool in tools:
    print(f"  - {tool.name}")
```

**2. Check LLM Direct:**
```python
import asyncio
from ai_brain import get_ai

ai = get_ai()
response = asyncio.run(ai.generate_response("Say hello"))
print(response)
```

**3. Check Planner Direct:**
```python
import asyncio
from autonomous_agent_enhanced import get_autonomous_agent
from task_state import TaskState

agent = get_autonomous_agent()
task = TaskState("test", "Open YouTube")
plan = asyncio.run(agent._plan(task, {}))
print(plan)
```

---

## Monitoring Real Execution

### Watch Backend Logs While Frontend Sends Commands

**Terminal 1:** Backend
```bash
cd Backend
python app.py
```

**Terminal 2:** Frontend (or test via API)
```bash
# or start frontend:
cd ..
npm run dev
# Then give voice command
```

**What to Watch:**
- Look for `[PLAN]` section in logs
- Check if `generate_response()` called
- Monitor tool execution
- Count steps taken

---

## Success Criteria

✅ **Test Passes If:**
- [ ] Tools are registered (25+)
- [ ] LLM response received (200+ chars)
- [ ] Plans generated for all 6 test commands
- [ ] No "is not a function" errors
- [ ] Fallback planner works for all keywords
- [ ] Log file shows detailed traces
- [ ] Frontend receives actual execution results

---

## Recovery Steps

If something breaks:

**1. Check Backend Health**
```bash
curl http://127.0.0.1:5000/health
# Should return: {"status": "ok"}
```

**2. Verify Configuration**
```bash
cat Backend/config.py | head -20
# Check PRIMARY_LLM is set to "gemini" or "ollama"
```

**3. Clear Logs and Retry**
```bash
rm Backend/planner_debug.log
python test_planner_debug.py
```

**4. Check Dependencies**
```bash
pip list | grep -E "google|ollama|pyautogui"
# All should be installed
```

---

## Summary

| Check | Status | Issue |
|-------|--------|-------|
| `generate_response()` exists | ✅ Added | Was missing |
| Async support | ✅ Added | Now supports async/await |
| Debug logging | ✅ Added | Full visibility |
| Tool registration | ✅ Working | 25+ tools available |
| LLM interface | ✅ Fixed | Now returns response |
| Fallback planner | ✅ Enhanced | Better keyword matching |

---

## Next: Frontend Integration

Once planner is working:

1. Start backend with fixed planner
2. Start frontend: `npm run dev`
3. Click ON to boot
4. Click microphone
5. Say: "Open YouTube and search Virat Kohli"
6. Should execute both commands
7. Should return actual results

---

**Status: READY FOR TESTING** 🚀
