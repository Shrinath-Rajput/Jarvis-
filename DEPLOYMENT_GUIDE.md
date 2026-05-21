# DEPLOYMENT & QUICK START GUIDE

## Quick Start (5 Minutes)

### Step 1: Activate Virtual Environment
```bash
cd "d:\e drive\Only_Project\jarvis1.0\Backend"
.\.venv\Scripts\Activate.ps1
```

### Step 2: Start Ollama (in separate terminal)
```bash
ollama serve
# In another terminal window:
ollama run llama3
```

### Step 3: Start Backend
```bash
# In Backend directory
python app.py
# Backend: http://127.0.0.1:5000
```

### Step 4: Start Frontend (in another terminal)
```bash
cd "d:\e drive\Only_Project\jarvis1.0"
npm run dev
# Frontend: http://127.0.0.1:5173
```

### Step 5: Test
Open browser: http://127.0.0.1:5173

---

## Testing Tools

### Test All Tools
```bash
cd Backend
python test_all_tools.py
```

### Test via API
```bash
curl -X POST http://127.0.0.1:5000/api/autonomous/execute \
  -H "Content-Type: application/json" \
  -d '{"task": "Set volume to 50%"}'
```

### Test Individual Tool
```python
from executor import executor
result = executor.tool_set_volume(level=75)
print(result)
```

---

## Example Commands

### File Operations
- "Copy file from Downloads to Documents"
- "Organize my desktop"
- "Search for all PDF files in Documents"
- "Delete old files from Downloads"
- "Create a backup zip of my projects"

### Browser
- "Search Google for machine learning"
- "Open YouTube and search for tutorials"
- "Download PDF from website"
- "Open Gmail"
- "Search Amazon for laptop"

### System
- "Set volume to 75%"
- "Set brightness to 50%"
- "Take screenshot"
- "Enable dark mode"
- "Check battery status"
- "Lock screen"

### Productivity
- "Add task: Call John"
- "Set reminder in 10 minutes"
- "Create budget tracker with categories"
- "Send email to john@example.com"

### Development
- "Open terminal"
- "Clone my repository"
- "Create React component named Button"
- "Start localhost server on port 3000"

### Media
- "Play music from file"
- "Convert video to MP4"
- "Create slideshow from images"
- "Edit image: resize to 800x600"

---

## Configuration Files

### .env (Backend)
```
OLLAMA_MODEL=llama3
OLLAMA_BASE_URL=http://127.0.0.1:11434
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
```

### config.py (Backend)
Modify settings like:
- FLASK_HOST
- FLASK_PORT
- MAX_EXECUTION_TIME
- DEBUG mode

---

## Directory Structure

```
jarvis1.0/
├── Backend/
│   ├── app.py                    (Flask server)
│   ├── planner_ai.py            (AI planner)
│   ├── executor.py              (Main executor)
│   ├── config.py                (Configuration)
│   ├── requirements.txt          (Dependencies)
│   ├── file_manager.py
│   ├── browser_tools.py
│   ├── system_control.py
│   ├── email_tools.py
│   ├── document_tools.py
│   ├── app_launcher.py
│   ├── whatsapp_tools.py
│   ├── excel_tools.py
│   ├── media_tools.py
│   ├── developer_tools.py
│   ├── productivity_tools.py
│   └── test_all_tools.py
├── src/
│   ├── JarvisHUD.jsx           (Main UI)
│   ├── VoiceEngine.js
│   ├── BackendExecutor.js
│   └── components/
├── public/
├── package.json
├── vite.config.js
├── JARVIS_SETUP_EXTENDED.md     (Setup guide)
└── TOOLS_REFERENCE.md            (Tools documentation)
```

---

## Troubleshooting

### Backend won't start
```
Error: ModuleNotFoundError: No module named 'ollama'

Solution:
pip install -r requirements.txt
```

### Ollama connection failed
```
Error: Failed to connect to Ollama

Solution:
1. Ensure Ollama is running: ollama serve
2. Check URL in config.py
3. Verify OLLAMA_BASE_URL=http://127.0.0.1:11434
```

### Tool not found error
```
Error: Tool not found: my_tool

Solution:
1. Check tool name spelling
2. Verify tool exists in executor.py
3. Ensure helper module is imported
```

### pyautogui issues
```
Error: pyautogui cannot find display

Solution:
Already handled with pyautogui.FAILSAFE = False
This is a known issue on some systems
```

### File permission denied
```
Error: Permission denied

Solution:
1. Run terminal as Administrator
2. Check file permissions
3. Use expanded paths (~/Documents)
```

---

## Performance Optimization

### For Faster Response
1. Use simpler tool requests
2. Batch operations together
3. Reduce wait times between steps
4. Use smaller file operations

### For Stability
1. Add wait times between operations
2. Use error handling
3. Test individual tools first
4. Monitor system resources

---

## Security Best Practices

1. **Never hardcode credentials**
   - Use .env file
   - Use environment variables
   - Use app-specific passwords for email

2. **Validate input**
   - Check task content
   - Sanitize file paths
   - Verify URLs

3. **Limit access**
   - Run on localhost (127.0.0.1)
   - Use firewall rules
   - Monitor logs

4. **Keep updated**
   - Update dependencies regularly
   - Keep Ollama updated
   - Monitor security advisories

---

## Monitoring & Logs

### View Backend Logs
```bash
# Logs appear in terminal where you ran: python app.py
# Format: [TIMESTAMP] [STATUS] [MESSAGE]
```

### Enable Debug Mode
In Backend/config.py:
```python
DEBUG = True  # More verbose logging
```

### Monitor Tool Execution
All tool calls are logged with:
- Timestamp
- Success/Failure status
- Parameters used
- Results returned
- Errors encountered

---

## Extending JARVIS

### Add New Tool

1. **Create helper module** (e.g., my_tools.py):
```python
class MyTools:
    @staticmethod
    def my_operation(param1, param2):
        # Your implementation
        return {"success": True, "result": "..."}
```

2. **Import in executor.py**:
```python
from my_tools import my_tools
```

3. **Add tool method**:
```python
def tool_my_operation(self, param1, param2):
    return my_tools.my_operation(param1, param2)
```

4. **Update planner_ai.py** SYSTEM_PROMPT:
```
- my_operation: Description. Params: {param1, param2}
```

5. **Test**:
```json
{
  "task": "Use my operation with value1 and value2"
}
```

---

## Advanced Usage

### Multi-Step Workflows
```python
plan = [
    {"tool": "open_app", "params": {"name": "excel"}},
    {"tool": "wait", "params": {"seconds": 3}},
    {"tool": "create_spreadsheet", "params": {"data": {...}}},
    {"tool": "add_chart", "params": {"excel_path": "..."}}
]

results = executor.execute_plan(plan)
```

### Error Handling
```python
for result in results:
    if not result['success']:
        print(f"Tool {result['tool']} failed: {result['error']}")
```

### Chaining Operations
Use tool outputs as inputs for next steps:
```python
result1 = executor.tool_screenshot()
save_path = result1['message']  # Extract path
result2 = executor.tool_send_email(
    ...,
    attachment_path=save_path
)
```

---

## Performance Metrics

### Expected Response Times
- Simple tool: < 1 second
- App launch: 2-5 seconds
- File operations: 1-10 seconds
- Email send: 2-5 seconds
- API calls: 1-3 seconds

### System Requirements
- CPU: 2+ cores recommended
- RAM: 4GB+ for smooth operation
- Disk: 5GB+ for dependencies
- Network: Stable connection for API calls

---

## Backup & Recovery

### Backup Configuration
```bash
# Backup .env file
copy Backend\.env Backend\.env.backup

# Backup custom tools
xcopy Backend\*.py backup\ /Y
```

### Recovery
```bash
# Restore from backup
copy Backend\.env.backup Backend\.env

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

---

## Support & Resources

### Documentation
- [JARVIS_SETUP_EXTENDED.md](./JARVIS_SETUP_EXTENDED.md) - Detailed setup
- [TOOLS_REFERENCE.md](./TOOLS_REFERENCE.md) - All tools documentation

### Testing
```bash
# Run test suite
python Backend/test_all_tools.py

# Run specific test
python -m pytest Backend/test_all_tools.py::test_imports
```

### Debugging
1. Enable DEBUG mode in config.py
2. Check terminal output for detailed logs
3. Use test_all_tools.py to diagnose issues
4. Review TOOLS_REFERENCE.md for tool usage

---

## Version Information

- **JARVIS Version**: 1.0 Extended
- **Python Version**: 3.8+
- **Ollama Model**: llama3 (recommended)
- **Frontend**: React 19 + Vite
- **Backend**: Flask 3.0

---

## Updates & Changelog

### May 2024
- Extended with 100+ tools
- Added 11 helper modules
- Comprehensive documentation
- Full test suite
- Production-ready

---

**For questions or issues, refer to the documentation or review logs for error messages.**
