# JARVIS 1.0 EXTENDED - QUICK REFERENCE CARD

## START SYSTEM (5 MINUTES)

### Terminal 1: Ollama
```bash
ollama serve
```

### Terminal 2: Backend
```bash
cd Backend
.\.venv\Scripts\Activate.ps1
python app.py
```
Backend: http://127.0.0.1:5000

### Terminal 3: Frontend
```bash
npm run dev
```
Frontend: http://127.0.0.1:5173

---

## TOOL CATEGORIES (100+ TOOLS)

### 🗂️ File Management (10)
copy_file | move_file | rename_file | delete_file | search_files | 
zip_files | organize_desktop | disk_space_check | delete_old_files | unzip_files

### 🌐 Browser (8)
google_search | youtube_search | open_gmail | amazon_search | 
incognito_mode | translate | download_pdf | clear_cookies

### 🖥️ System (20)
set_volume | mute | set_brightness | enable_wifi | disable_wifi |
screenshot | record_screen | shutdown | restart | sleep |
dark_mode_on | lock_screen | battery_status | enable_firewall

### 📧 Email (4)
send_email | send_email_with_attachment | reply_email | search_emails

### 📄 Documents (7)
create_resume | create_cover_letter | spell_check | summarize_pdf |
translate_text | generate_report | read_pdf

### 💬 Messaging (3)
send_whatsapp_message | send_whatsapp_image | send_group_message

### 📊 Excel (6)
create_spreadsheet | add_chart | import_csv | create_pivot_table |
create_budget_tracker | add_formula

### 🎵 Media (7)
play_music | pause_music | next_song | convert_video | 
edit_image | create_slideshow

### 👨‍💻 Developer (11)
open_terminal | run_python_script | npm_install | git_clone |
git_commit | git_push | start_localhost_server | create_react_component |
docker_start | analyze_error

### ✅ Productivity (9)
set_reminder | set_timer | add_todo | list_todos | mark_todo_done |
schedule_meeting | open_calendar | get_reminders | delete_todo

### ⚙️ Apps (25+)
word | excel | chrome | firefox | vs code | notepad | 
calculator | paint | teams | zoom | spotify | powerpoint

---

## COMMON TASKS

### Search & Information
```
"Search Google for machine learning"
"Search YouTube for tutorials"
"Translate this to Spanish"
```

### File Operations
```
"Copy file from Downloads to Documents"
"Organize my desktop"
"Search for all PDF files"
"Create zip backup"
```

### System Control
```
"Set volume to 75%"
"Take screenshot"
"Enable dark mode"
"Check battery status"
```

### Productivity
```
"Add task: Call John"
"Create budget tracker"
"Send email to john@example.com"
"Set reminder in 10 minutes"
```

### Development
```
"Open VS Code"
"Clone my repository"
"Create React component Button"
"Start localhost on port 3000"
```

### Office Tasks
```
"Create resume with my info"
"Generate report"
"Create Excel sheet with data"
"Add pie chart to file"
```

---

## API USAGE

### Simple Request
```bash
curl -X POST http://127.0.0.1:5000/api/autonomous/execute \
  -H "Content-Type: application/json" \
  -d '{"task": "Search Google for Python"}'
```

### Python Client
```python
import requests

response = requests.post(
    'http://127.0.0.1:5000/api/autonomous/execute',
    json={'task': 'your task here'}
)
print(response.json())
```

### JavaScript Client
```javascript
fetch('http://127.0.0.1:5000/api/autonomous/execute', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({task: 'your task'})
}).then(r => r.json()).then(console.log);
```

---

## TROUBLESHOOTING

| Issue | Solution |
|-------|----------|
| Backend won't start | Ensure .venv is activated, run `pip install -r requirements.txt` |
| Ollama connection failed | Run `ollama serve` in separate terminal |
| Tool not found | Check spelling, verify tool exists in TOOLS_REFERENCE.md |
| File permission denied | Run terminal as Administrator |
| Email not sending | Use app-specific password, check .env EMAIL_USER |

---

## CONFIGURATION

### .env File
```
OLLAMA_MODEL=llama3
OLLAMA_BASE_URL=http://127.0.0.1:11434
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
```

### Ports
- Backend: 127.0.0.1:5000
- Frontend: 127.0.0.1:5173
- Ollama: 127.0.0.1:11434

---

## FILE LOCATIONS

```
jarvis1.0/
├── Backend/
│   ├── app.py                (Start here)
│   ├── executor.py           (100+ tools)
│   ├── planner_ai.py         (AI planning)
│   └── helper modules...
├── src/
│   └── JarvisHUD.jsx         (UI)
├── TOOLS_REFERENCE.md        (Read this)
├── DEPLOYMENT_GUIDE.md       (Setup)
└── API_DOCUMENTATION.md      (Integration)
```

---

## KEYBOARD SHORTCUTS

| Shortcut | Action |
|----------|--------|
| Ctrl+C | Stop backend/frontend |
| Ctrl+S | Save file |
| Ctrl+Z | Undo |
| F12 | Developer tools |

---

## PERFORMANCE TIPS

1. **Batch operations** - Group similar tasks
2. **Add delays** - Use `wait` between app launches
3. **Use full paths** - Always expand `~` to home directory
4. **Check resources** - Monitor CPU/RAM usage
5. **Test individual tools** - Debug before complex workflows

---

## ENVIRONMENT VARIABLES

```bash
# Set in PowerShell
$env:OLLAMA_MODEL = "llama3"
$env:FLASK_ENV = "development"

# Or create .env file in Backend/
```

---

## USEFUL COMMANDS

```bash
# List all tools
python -c "from executor import executor; print([x for x in dir(executor) if x.startswith('tool_')])"

# Test a tool
python -c "from executor import executor; print(executor.tool_set_volume(50))"

# Run tests
python test_all_tools.py

# Check health
curl http://127.0.0.1:5000/health

# Get status
curl http://127.0.0.1:5000/status
```

---

## RESPONSE FORMAT

```json
{
  "success": true,
  "task": "Your task",
  "plan": [
    {"tool": "tool_name", "params": {...}}
  ],
  "results": [
    {
      "tool": "tool_name",
      "success": true,
      "result": {...}
    }
  ]
}
```

---

## DOCUMENTATION MAP

| Document | Purpose |
|----------|---------|
| DEPLOYMENT_GUIDE.md | Quick start & setup |
| TOOLS_REFERENCE.md | Complete tool documentation |
| API_DOCUMENTATION.md | REST API integration |
| JARVIS_SETUP_EXTENDED.md | Detailed configuration |
| IMPLEMENTATION_SUMMARY.md | Project overview |

---

## QUICK STATS

- **100+** Tools
- **11** Helper Modules
- **3,500+** Lines of Code
- **4** Documentation Files
- **25+** Supported Apps
- **10+** Languages

---

## SUPPORT

1. **Setup Issues**: See DEPLOYMENT_GUIDE.md
2. **Tool Usage**: Check TOOLS_REFERENCE.md
3. **Integration**: Read API_DOCUMENTATION.md
4. **Diagnosis**: Run `python test_all_tools.py`
5. **Logs**: Check terminal output

---

## NEXT STEPS

1. ✅ Start system (see above)
2. ✅ Open http://127.0.0.1:5173
3. ✅ Enter a task
4. ✅ Watch it execute
5. ✅ Read documentation
6. ✅ Build workflows

---

**Version**: 1.0 Extended | **Status**: Production Ready | **Date**: May 2024

---

## REMEMBER

- Use **natural language** for all tasks
- **Always wait** between app launches
- **Expand paths** with `~` or full path
- **Check logs** if something fails
- **Read TOOLS_REFERENCE.md** for details
- **Run tests** to verify setup

---

**Happy Automating! 🚀**
