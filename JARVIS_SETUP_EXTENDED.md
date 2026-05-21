# JARVIS 1.0 EXTENDED - INSTALLATION & SETUP GUIDE

## Overview
JARVIS is now extended with 100+ dynamic tools covering all aspects of desktop automation, from file management to AI-powered task planning.

## Prerequisites
- Python 3.8+
- Windows OS (for desktop automation)
- Ollama running locally (for AI planning)
- Node.js (for React frontend)

## Installation

### 1. Python Environment Setup

```bash
cd "d:\e drive\Only_Project\jarvis1.0\Backend"

# Create virtual environment
python -m venv .venv

# Activate virtual environment (Windows)
.\.venv\Scripts\Activate.ps1

# Or using bash
source .venv/Scripts/activate
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup Environment Variables

Create `.env` file in Backend directory:

```
OLLAMA_MODEL=llama3
OLLAMA_BASE_URL=http://127.0.0.1:11434

# Optional: For email functionality
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

# Optional: For API keys
GEMINI_API_KEY=your_key
CLAUDE_API_KEY=your_key
```

### 4. Start Ollama

```bash
# In separate terminal
ollama serve

# Then run: ollama run llama3
```

### 5. Start JARVIS Backend

```bash
cd Backend
python app.py
```

Backend runs on: `http://127.0.0.1:5000`

### 6. Start React Frontend (in another terminal)

```bash
npm run dev
```

Frontend runs on: `http://127.0.0.1:5173`

## Tool Categories

### 1. File Management (10 tools)
- copy_file
- move_file
- rename_file
- delete_file
- delete_old_files
- search_files
- zip_files
- unzip_files
- organize_desktop
- disk_space_check

### 2. Browser Operations (8 tools)
- google_search
- youtube_search
- open_gmail
- amazon_search
- incognito_mode
- translate
- download_pdf
- clear_cookies

### 3. System Control (20 tools)
- set_volume / mute / unmute
- set_brightness
- enable/disable_wifi
- enable/disable_bluetooth
- screenshot / record_screen
- shutdown / restart / sleep
- dark_mode_on / dark_mode_off
- battery_status
- lock_screen
- enable/disable_firewall
- disable/enable_webcam

### 4. Email (4 tools)
- send_email
- send_email_with_attachment
- reply_email
- search_emails

### 5. Documents (7 tools)
- create_resume
- create_cover_letter
- spell_check
- summarize_pdf
- translate_text
- generate_report
- read_pdf

### 6. Messaging (3 tools)
- send_whatsapp_message
- send_whatsapp_image
- send_group_message

### 7. Excel/Spreadsheets (6 tools)
- create_spreadsheet
- add_chart
- import_csv
- create_pivot_table
- create_budget_tracker
- add_formula

### 8. Media (7 tools)
- play_music
- pause_music / next_song / previous_song
- convert_video
- edit_image
- create_slideshow

### 9. Developer Tools (11 tools)
- open_terminal / open_powershell
- run_python_script
- npm_install
- git_clone / git_commit / git_push
- start_localhost_server
- create_react_component
- docker_start / docker_stop
- analyze_error

### 10. Productivity (9 tools)
- set_reminder
- set_timer
- add_todo / list_todos / mark_todo_done
- schedule_meeting
- open_calendar
- get_reminders
- delete_todo

### 11. Advanced (3 tools)
- research_and_summarize
- create_and_send_report
- complete_workflow

## Usage Examples

### Example 1: Search Google
```json
{
  "task": "Search Google for Python tutorials"
}
```

### Example 2: Create Budget Tracker
```json
{
  "task": "Create a budget tracker with categories food 5000, transport 2000, entertainment 1500"
}
```

### Example 3: Create and Send Report
```json
{
  "task": "Create a report about Q1 results and send to manager@example.com"
}
```

### Example 4: Developer Workflow
```json
{
  "task": "Clone my git repository, create a react button component, and start localhost server"
}
```

### Example 5: File Organization
```json
{
  "task": "Organize my desktop files and create a zip backup"
}
```

## API Endpoints

### Execute Task
```
POST /api/autonomous/execute
Content-Type: application/json

{
  "task": "your natural language task"
}
```

### Health Check
```
GET /health
```

### Status
```
GET /status
```

## Tool Architecture

### Core Components

1. **executor.py** - Main execution engine
   - Routes requests to appropriate tools
   - Handles error management
   - Logs all operations

2. **planner_ai.py** - AI task planner
   - Converts natural language to action plans
   - Uses Ollama llama3 model
   - Returns JSON action sequences

3. **Helper Modules**:
   - file_manager.py - File operations
   - browser_tools.py - Browser automation
   - system_control.py - System settings
   - email_tools.py - Email operations
   - document_tools.py - Document generation
   - app_launcher.py - Application management
   - whatsapp_tools.py - WhatsApp messaging
   - excel_tools.py - Spreadsheet operations
   - media_tools.py - Media operations
   - developer_tools.py - Development tasks
   - productivity_tools.py - Productivity features

### Execution Flow

```
User Input (Natural Language)
    ↓
Planner AI (Converts to Action Plan)
    ↓
Executor (Routes to Tools)
    ↓
Helper Modules (Execute Actions)
    ↓
Results (Logged & Returned)
```

## Advanced Configuration

### Custom Tool Creation

To add a new tool:

1. Create function in appropriate helper module
2. Add `tool_` prefixed method in executor.py
3. Update planner_ai.py SYSTEM_PROMPT
4. Test with sample request

Example:
```python
# In executor.py
def tool_my_custom_tool(self, param1, param2):
    result = my_helper_function(param1, param2)
    return result
```

### Multi-Step Workflows

Create complex workflows with:
```python
{
  "tool": "complete_workflow",
  "params": {
    "workflow_steps": [
      {"tool": "tool1", "params": {...}},
      {"tool": "tool2", "params": {...}}
    ]
  }
}
```

## Troubleshooting

### Issue: Tools not found
**Solution**: Ensure all helper modules are in Backend directory and executor imports them

### Issue: Ollama connection failed
**Solution**: Verify Ollama is running - `ollama serve`

### Issue: pyautogui errors
**Solution**: Disable failsafe - already done in executor.py

### Issue: File permission errors
**Solution**: Run terminal as Administrator

### Issue: Email not sending
**Solution**: Use app-specific password for Gmail, check environment variables

## Performance Tips

1. Batch operations together in workflows
2. Use timeouts for long operations
3. Leverage tool caching where possible
4. Monitor system resources
5. Use appropriate delays between GUI operations

## Security Considerations

1. Store credentials in .env, not in code
2. Sanitize user input in planner
3. Implement rate limiting
4. Use secure SMTP for emails
5. Validate all file paths
6. Be cautious with git credentials

## Monitoring & Logging

All operations are logged with timestamps and results:
```
[2024-05-21 10:30:45] [✅ SUCCESS] google_search
  Params: {"query": "python"}
  Result: {"success": true, "message": "Searched Google..."}
```

## Testing

### Test Individual Tools

```python
from executor import executor

# Test a tool directly
result = executor.tool_open_app(name="notepad")
print(result)
```

### Test Full Workflow

```bash
curl -X POST http://127.0.0.1:5000/api/autonomous/execute \
  -H "Content-Type: application/json" \
  -d '{"task": "Open Chrome and search for python"}'
```

## Updating & Maintenance

### Update Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Check System Requirements
```bash
python --version
ollama --version
node --version
npm --version
```

### Verify Tool Availability
```bash
# In Backend directory
python -c "from executor import executor; print(dir(executor))" | grep tool_
```

## FAQ

**Q: Can I run this on Linux/Mac?**
A: Most tools will need modification. pyautogui and system_control are Windows-specific.

**Q: How do I add custom apps?**
A: Edit app_launcher.py APP_PATHS dictionary

**Q: Can I use different AI models?**
A: Yes, change OLLAMA_MODEL in .env. Supports any Ollama model.

**Q: How do I implement multi-language support?**
A: Tools like translate_text and document translation already support multiple languages.

**Q: Is there a database?**
A: Currently uses in-memory storage. Can integrate with Redis/MongoDB.

## Support

For issues, check the logs in Backend/logs directory or terminal output.

---

**Version**: JARVIS 1.0 Extended
**Last Updated**: May 2024
**Status**: Production Ready
