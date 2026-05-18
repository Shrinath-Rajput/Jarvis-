# 🤖 JARVIS 1.0 - Advanced AI Assistant System

Autonomous AI that understands natural language and controls your computer intelligently.

## ⚡ Quick Start (5 Minutes)

```bash
# 1. Get Gemini API Key
# https://makersuite.google.com/app/apikeys

# 2. Setup
cd Backend
cp .env.example .env
# Edit .env: add GEMINI_API_KEY

# 3. Run
pip install -r requirements.txt
python -m playwright install  
python app.py

# ✅ Visit http://localhost:5000
```

## ✨ Features

✅ **Browser Automation** - Navigate, fill forms, extract data
✅ **Computer Control** - Files, apps, keyboard, mouse
✅ **Intelligent Planning** - Multi-step task execution
✅ **Natural Language** - Understand any request
✅ **Memory System** - Remember and learn
✅ **Vision Analysis** - Understand images

## 📚 Complete Documentation

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design & roadmap
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Installation & all API endpoints
- **[IMPLEMENTATION_COMPLETE.md](IMPLEMENTATION_COMPLETE.md)** - What's been built

## 🎮 Example Commands

```
"Open YouTube and play Arijit Singh songs"
"Create a portfolio project with React structure"  
"Search Google for AI trends and summarize"
"Fill contact form with my details"
"Create 5 project documentation files"
```

## 🏗️ System Architecture

```
User Input → AI Understanding → Planning → Execution → Result
              (Gemini)         (Smart)    (Tools)
```

## 🚀 API Endpoints

```bash
POST /api/command              # Execute with automation
POST /api/plan                 # Create plan only
POST /api/chat                 # Direct chat
GET  /api/memory/stats         # System statistics
GET  /api/memory/conversation  # History
POST /api/execute              # Run pre-made plan
```

## 💻 Tech Stack

| Component | Technology |
|-----------|-----------|
| **LLM** | Google Gemini 1.5 Pro |
| **Backend** | Python Flask |
| **Browser** | Playwright |
| **Control** | PyAutoGUI |
| **Memory** | SQLite + JSON |
| **Frontend** | React + Vite |

## 📋 Core Components

✅ **AI Brain** (ai_brain.py) - Gemini integration with fallback
✅ **Planner** (planner_ai.py) - Intelligent action planning
✅ **Executor** (executor.py) - Multi-action execution engine
✅ **Browser** (browser_control.py) - Website automation
✅ **Computer** (computer_control.py) - System control
✅ **Memory** (memory_manager.py) - Learning system
✅ **API** (app.py) - REST endpoints

## 🎯 Capabilities Included

- Natural language understanding
- Multi-step task planning
- Browser automation (Playwright)
- File & folder operations
- Application launching
- Keyboard & mouse control
- Screenshot capture
- Form filling
- Data extraction
- Conversation memory
- Action history
- Success tracking

## 🔧 Configuration

Edit `Backend/.env`:
```ini
GEMINI_API_KEY=your_key_here
HEADLESS_BROWSER=False
DEBUG=True
FLASK_PORT=5000
```

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| API key error | Add GEMINI_API_KEY to .env |
| Port 5000 in use | Change FLASK_PORT in .env |
| Playwright issues | `python -m playwright install` |

See [SETUP_GUIDE.md](SETUP_GUIDE.md#troubleshooting) for detailed help.

## 📈 Project Phases

✅ **Phase 1**: LLM + Planning (DONE)
✅ **Phase 3**: Browser Automation (DONE)  
🔲 **Phase 2**: Vision/OCR (TODO)
🔲 **Phase 4**: Voice I/O (TODO)
🔲 **Phase 5**: Advanced Learning (TODO)

## 🚀 Next Steps

1. [Read Setup Guide](SETUP_GUIDE.md)
2. [Understand Architecture](ARCHITECTURE.md)
3. [Try API Examples](SETUP_GUIDE.md#usage-examples)
4. [Check Status](IMPLEMENTATION_COMPLETE.md)

## 📞 Support

- 📖 [SETUP_GUIDE.md](SETUP_GUIDE.md) - Installation & troubleshooting
- 🏗️ [ARCHITECTURE.md](ARCHITECTURE.md) - System design
- 📋 [IMPLEMENTATION_COMPLETE.md](IMPLEMENTATION_COMPLETE.md) - Current status
- 🔍 Logs: `Backend/logs/jarvis.log`

---

**Status: Production Ready ✅ | Version 1.0 | Made for AI Automation**

[Get Started →](SETUP_GUIDE.md)
