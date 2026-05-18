# ⚡ JARVIS AUTONOMOUS AI - QUICK REFERENCE CARD

## 🎯 What You Have

A complete autonomous AI system with NO hardcoded logic, dynamic tool selection, and LLM-driven decisions.

---

## 🚀 30-Second Integration

```python
# In Backend/app.py, add:
from autonomous_api import register_autonomous_api
from tool_implementations import register_all_tools

# After Flask app creation:
register_all_tools()
register_autonomous_api(app)
```

**That's it! System is now ready.**

---

## 📝 Quick Usage

### Via API
```bash
curl -X POST http://localhost:5000/api/autonomous/execute \
  -H "Content-Type: application/json" \
  -d '{"task": "Open Google"}'
```

### Via Python
```python
import asyncio
from autonomous_agent_enhanced import get_autonomous_agent

asyncio.run(get_autonomous_agent().execute_autonomous_task("Open Google"))
```

### Via React
```javascript
fetch('/api/autonomous/execute', {
  method: 'POST',
  body: JSON.stringify({task: "Open Google"})
})
```

---

## 🔧 The 25 Tools

**Application:** launch_app, close_app
**Browser:** open_website, navigate_url, search_google, search_youtube
**Files:** create_folder, create_file, delete_file, write_file
**Keyboard:** type_text, press_key, press_hotkey
**Mouse:** move_mouse, click, scroll, drag
**System:** screenshot, wait

---

## 📊 Key API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | /api/autonomous/execute | Run a task |
| GET | /api/autonomous/tools/list | See all tools |
| GET | /api/autonomous/stats | View statistics |
| GET | /api/autonomous/history | Action history |

**Full list:** See autonomous_api.py

---

## 🎓 How It Works

```
1. PERCEIVE    → Screen screenshot + analysis
2. ANALYZE     → Check state, detect errors
3. PLAN        → LLM decides best tool
4. ACT         → Execute the tool
5. LEARN       → Record statistics
6. REPEAT      → Continue until done
```

**NO hardcoded if/elif chains. Pure AI decisions!**

---

## ➕ Add New Tools (30 seconds)

```python
# In tool_implementations.py
async def my_tool(param: str):
    # your code
    return {"success": True, "result": "..."}

# In register_all_tools()
registry.register(Tool(
    name="my_tool",
    category=ToolCategory.SYSTEM,
    function=my_tool,
    description="My tool"
))

# NOW: Tool works everywhere!
# ✅ LLM knows about it
# ✅ API exposes it
# ✅ Can be used immediately
```

---

## 🧪 Test Everything

```bash
# Run full test suite
python test_autonomous_agent.py full

# Check tool registry
curl http://localhost:5000/api/autonomous/tools/list

# Get statistics
curl http://localhost:5000/api/autonomous/stats

# Execute a tool directly
curl -X POST http://localhost:5000/api/autonomous/tools/execute \
  -H "Content-Type: application/json" \
  -d '{"tool": "screenshot"}'
```

---

## 📦 Files You Need

Copy to Backend/:
- ✅ tool_registry.py
- ✅ tool_implementations.py
- ✅ autonomous_agent_enhanced.py
- ✅ autonomous_api.py
- ✅ test_autonomous_agent.py

---

## 📖 Documentation

Read in order:
1. **PROJECT_SUMMARY.md** (quick overview)
2. **AUTONOMOUS_AGENT_GUIDE.md** (full guide)
3. **BEFORE_vs_AFTER.md** (why this works)
4. **ARCHITECTURE_DIAGRAMS.md** (visual)

---

## ⚙️ Configuration

```python
# In your agent
agent.max_steps_per_task = 150      # Max iterations
agent.max_retries_per_action = 3    # Retry count
agent.use_local_llm = True          # Use Ollama
```

Or via API:
```bash
curl -X PUT http://localhost:5000/api/autonomous/config \
  -H "Content-Type: application/json" \
  -d '{"max_steps_per_task": 200}'
```

---

## 🔍 Troubleshooting

| Problem | Solution |
|---------|----------|
| Tool not found | Check registration in register_all_tools() |
| LLM errors | Ensure Ollama/API is running |
| Screenshot fails | Check EasyOCR installed |
| Slow execution | Reduce max_steps, optimize tools |
| API errors | Check logs in Backend/logs/ |

---

## 📊 Monitoring

### Get Stats
```bash
curl http://localhost:5000/api/autonomous/stats
```

Returns: Tool count, executions, success rates

### View History
```bash
curl http://localhost:5000/api/autonomous/history
```

Returns: Last 20 actions executed

### View Decisions
```bash
curl http://localhost:5000/api/autonomous/decision-history
```

Returns: Decision reasoning

---

## 🎯 Common Tasks

### "Search Google"
```json
{
  "task": "Search Google for Python tutorials"
}
```
→ Agent will: PERCEIVE → PLAN → search_google() → done ✅

### "Create Files"
```json
{
  "task": "Create a folder called 'test' with a file inside"
}
```
→ Agent will: create_folder() → create_file() → done ✅

### "Open Applications"
```json
{
  "task": "Open Chrome and VS Code"
}
```
→ Agent will: launch_app("chrome") → launch_app("vscode") → done ✅

---

## 💡 Pro Tips

### Tip 1: Use Clear Task Descriptions
✅ "Search Google for AI tutorials"
❌ "Search stuff"

### Tip 2: Monitor Statistics
Check `/api/autonomous/stats` to see which tools work best

### Tip 3: Add Custom Tools
Your business logic → Just register as tool → Automatically available

### Tip 4: Track Everything
All actions logged → Use for debugging and learning

### Tip 5: Test Before Deploy
Use test suite → Check stats → Monitor history

---

## 🚀 Quick Start Timeline

| When | What | Time |
|------|------|------|
| Now | Copy files | 2 min |
| Now | Update app.py | 2 min |
| Now | Run tests | 5 min |
| Now | Try API | 5 min |
| Today | Test with voice | 15 min |
| This week | Custom tools | 1 hour |
| This week | React integration | 1 hour |
| Next week | Deploy | 1 hour |

**Total: ~3 hours to full production!**

---

## 📞 Emergency Reference

### Python Script to Test
```python
import asyncio
from autonomous_agent_enhanced import get_autonomous_agent
from tool_implementations import register_all_tools

async def test():
    register_all_tools()
    agent = get_autonomous_agent()
    result = await agent.execute_autonomous_task("Take a screenshot")
    print(result)

asyncio.run(test())
```

### Curl to Test API
```bash
curl -X POST http://localhost:5000/api/autonomous/execute \
  -H "Content-Type: application/json" \
  -d '{"task": "Take a screenshot"}'
```

### Check Everything Works
```bash
# 1. Check tools
curl http://localhost:5000/api/autonomous/tools/list

# 2. Check health
curl http://localhost:5000/api/autonomous/health

# 3. Execute simple tool
curl -X POST http://localhost:5000/api/autonomous/tools/execute \
  -H "Content-Type: application/json" \
  -d '{"tool": "wait", "parameters": {"seconds": 1}}'
```

---

## 🎉 That's It!

You have a complete autonomous AI system. The hardest part is done.

**Next: Integrate and deploy! 🚀**

---

## 📋 Bookmark These Docs

- Main: `README_AUTONOMOUS_SYSTEM.md`
- Guide: `AUTONOMOUS_AGENT_GUIDE.md`
- Integration: `IMPLEMENTATION_CHECKLIST.md`
- Diagrams: `ARCHITECTURE_DIAGRAMS.md`

**Welcome to true AI autonomy! 🤖**
