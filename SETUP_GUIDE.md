# JARVIS AI System - Setup & Usage Guide

## 🚀 Quick Start (5 minutes)

### 1. Get API Keys

**Google Gemini API** (Primary - Required)
- Go to: https://makersuite.google.com/app/apikeys
- Click "Create API Key"
- Copy your API key

### 2. Setup Environment

```bash
# Navigate to Backend folder
cd Backend

# Create .env file from template
cp .env.example .env

# Edit .env and add your GEMINI_API_KEY
# (Use your favorite editor)
```

### 3. Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt

# Install Playwright browsers
python -m playwright install
```

### 4. Run the System

```bash
# Start the backend server
python app.py

# Should show:
# 🤖 JARVIS AI SYSTEM STARTING
# Host: 0.0.0.0
# Port: 5000
```

### 5. Test in Another Terminal

```bash
# Test basic command
curl -X POST http://localhost:5000/api/command \
  -H "Content-Type: application/json" \
  -d '{"text": "Navigate to YouTube and take a screenshot"}'
```

---

## 📚 API Endpoints

### Main Command Endpoint
**POST** `/api/command`

Execute a complete command with planning and execution.

**Request:**
```json
{
  "text": "Open YouTube and search for Arijit Singh",
  "context": "optional previous context",
  "stream": false
}
```

**Response:**
```json
{
  "success": true,
  "response": "I've opened YouTube and searched for Arijit Singh...",
  "plan": [
    {"tool": "navigate", "params": {"url": "https://youtube.com"}},
    {"tool": "wait", "params": {"seconds": 2}},
    {"tool": "type", "params": {"selector": "input[name='search']", "text": "Arijit Singh"}}
  ],
  "execution_results": [...],
  "metadata": {...}
}
```

---

### Planning Endpoint
**POST** `/api/plan`

Just create a plan without executing.

**Request:**
```json
{"text": "Create a new folder named 'Portfolio'"}
```

**Response:**
```json
{
  "success": true,
  "plan": [
    {"tool": "create_folder", "params": {"path": "Desktop/Portfolio"}}
  ],
  "explanation": "This will create a new folder called Portfolio on your Desktop"
}
```

---

### Execution Endpoint
**POST** `/api/execute`

Execute a pre-created plan.

**Request:**
```json
{
  "plan": [
    {"tool": "navigate", "params": {"url": "https://google.com"}},
    {"tool": "screenshot", "params": {"name": "google"}}
  ]
}
```

---

### Chat Endpoint
**POST** `/api/chat`

Direct chat with AI (no planning/execution).

**Request:**
```json
{"text": "What can you do for me?"}
```

---

### Vision Endpoint
**POST** `/api/vision`

Analyze images using Gemini's vision.

**Request:**
```json
{
  "image_path": "/path/to/image.png",
  "question": "What's in this image?"
}
```

---

### Memory Endpoints

**GET** `/api/memory/stats` - Memory statistics
**GET** `/api/memory/conversation` - Conversation history
**POST** `/api/memory/clear` - Clear all memory

---

## 🎯 Usage Examples

### Example 1: Open YouTube and Play Music
```json
{
  "text": "Open YouTube and play Arijit Singh songs"
}
```

**What happens:**
1. AI understands: Open YouTube → Search → Play
2. Creates action plan with 5-6 steps
3. Executes each step:
   - Navigate to YouTube
   - Wait for load
   - Find search box
   - Type query
   - Press Enter
   - Click first result

---

### Example 2: Create Project Files
```json
{
  "text": "Create a new portfolio project folder with index.html and style.css"
}
```

**What happens:**
1. AI plans: Create folder → Create files → Add content
2. Executes:
   - Creates folder on Desktop
   - Creates index.html with basic structure
   - Creates style.css with basic styling

---

### Example 3: Search and Analyze
```json
{
  "text": "Search Google for 'React best practices' and take a screenshot of results"
}
```

---

## 🔧 Configuration

Edit `Backend/.env` to customize:

```ini
# Use Gemini (recommended)
GEMINI_API_KEY=your_key_here

# Show browser during automation
HEADLESS_BROWSER=False

# Enable debug logging
DEBUG=True

# Voice input
VOICE_ENABLED=True
```

---

## 📊 System Architecture

### Components

1. **AI Brain** (`ai_brain.py`)
   - Gemini integration for reasoning
   - Fallback to Ollama

2. **Planner** (`planner_ai.py`)
   - Breaks down requests into action plans
   - Uses Gemini for intelligent planning

3. **Executor** (`executor.py`)
   - Executes planned actions
   - Monitors results
   - Error handling

4. **Browser Control** (`browser_control.py`)
   - Website navigation
   - Clicking elements
   - Form filling
   - Data extraction

5. **Computer Control** (`computer_control.py`)
   - Keyboard/mouse control
   - File operations
   - Application launching

6. **Memory** (`memory_manager.py`)
   - Conversation history
   - Action logs
   - Learning from past

---

## 🐛 Troubleshooting

### Issue: "GEMINI_API_KEY not set"
**Solution:** Make sure `.env` file exists with your API key:
```
GEMINI_API_KEY=your_actual_key_here
```

### Issue: Browser doesn't open
**Solution:** Install Playwright browsers:
```bash
python -m playwright install
```

### Issue: "Element not found"
**Solution:** Try increasing wait time or check selector:
```json
{
  "tool": "wait_for",
  "params": {
    "element": "button[type='submit']",
    "timeout": 15000
  }
}
```

### Issue: Connection refused on port 5000
**Solution:** Change port in `.env`:
```
FLASK_PORT=8000
```

---

## 📈 Performance Tips

1. **Use headless browser** (faster):
   ```
   HEADLESS_BROWSER=True
   ```

2. **Cache plans** for repeated tasks
3. **Use shorter waits** for fast sites:
   ```json
   {"tool": "wait", "params": {"seconds": 1}}
   ```

4. **Screenshot strategically** (uses disk space)

---

## 🔐 Security Notes

1. **Protect API keys** - Never commit `.env` to git
2. **Validate user input** - AI can be creative, sometimes dangerously
3. **Use HTTPS** in production
4. **Rate limit** the API
5. **Log all operations** for audit

---

## 📝 Common Tasks

### Open a Website
```json
{"text": "Open Google"}
```

### Search Something
```json
{"text": "Search Google for machine learning"}
```

### Create Files
```json
{"text": "Create a Python file named test.py with a hello world program"}
```

### Navigate a Website
```json
{"text": "Go to GitHub and search for React projects"}
```

### Fill a Form
```json
{"text": "Go to contact form and fill: name=John, email=john@example.com"}
```

---

## 🚀 Next Steps

1. **Phase 1 Complete**: Core LLM + Planning ✅
2. **Phase 3 In Progress**: Browser Automation ✅
3. **Next: Phase 2**: Vision + OCR
4. **Then: Phase 4**: Voice Integration
5. **Then: Phase 5**: Learning & Adaptation

---

## 📚 Learn More

- [Google Gemini API](https://ai.google.dev/)
- [Playwright Documentation](https://playwright.dev/)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

## 💡 Tips & Tricks

### Use Stream Mode for Long Tasks
```json
{
  "text": "Create 10 files for a project",
  "stream": true
}
```

### Get Execution Details
```bash
curl http://localhost:5000/api/memory/stats | jq '.statistics.success_rate'
```

### Clear Memory for Fresh Start
```bash
curl -X POST http://localhost:5000/api/memory/clear
```

### Check System Status
```bash
curl http://localhost:5000/api/status
```

---

## 🤝 Contributing

To extend Jarvis:

1. **Add new tools** in `executor.py`
2. **Add new AI features** in `ai_brain.py`
3. **Add endpoints** in `app.py`
4. **Test thoroughly** before merging

---

**Happy Automating! 🎉**
