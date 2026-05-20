# API REFERENCE - Autonomous AI Agent v3

## Base URL

```
http://localhost:5000
```

## Authentication

Currently no authentication required. For production, add API keys.

---

## Endpoints

### 1. Health Check

**Endpoint:** `GET /health`

**Purpose:** Verify server is running

**Request:**
```bash
curl http://localhost:5000/health
```

**Response:**
```json
{
  "success": true,
  "status": "healthy",
  "agent": "autonomous-ai-true",
  "version": "3.0-dynamic",
  "components": {
    "agent": true,
    "planner": true,
    "executor": true
  }
}
```

---

### 2. Autonomous Execution (MAIN ENDPOINT)

**Endpoint:** `POST /api/autonomous/execute`

**Purpose:** Execute ANY task using full OTAV cycle

**Request Body:**
```json
{
  "task": "search machine learning on youtube"
}
```

**Response:**
```json
{
  "success": true,
  "status": "completed",
  "task": "search machine learning on youtube",
  "result": {
    "status": "completed",
    "total_actions": 5,
    "successful_actions": 5,
    "verified": true,
    "phases": {
      "observe": {
        "screenshot": "screenshots/screenshot_1705678900.png",
        "window_title": "Google Chrome",
        "visible_text": "Search the web...",
        "text_elements": 15
      },
      "think": {
        "actions": 5
      },
      "act": {
        "status": "completed",
        "total_actions": 5,
        "successful": 5,
        "failed": 0,
        "results": [
          {
            "tool": "open_website",
            "success": true,
            "output": "Opened: https://youtube.com"
          },
          ...
        ]
      },
      "verify": {
        "success": true,
        "reason": "Task completed successfully",
        "percentage": 100
      }
    }
  }
}
```

**Query Parameters:** None

**Error Responses:**

| Status | Response |
|--------|----------|
| 400 | `{"success": false, "error": "No task provided"}` |
| 500 | `{"success": false, "error": "error message"}` |

**Examples:**

```bash
# Example 1: Website search
curl -X POST http://localhost:5000/api/autonomous/execute \
  -H "Content-Type: application/json" \
  -d '{"task":"search python tutorial on google"}'

# Example 2: Folder creation
curl -X POST http://localhost:5000/api/autonomous/execute \
  -H "Content-Type: application/json" \
  -d '{"task":"create folder my-project on desktop"}'

# Example 3: App launch
curl -X POST http://localhost:5000/api/autonomous/execute \
  -H "Content-Type: application/json" \
  -d '{"task":"open vs code"}'

# Example 4: Complex task
curl -X POST http://localhost:5000/api/autonomous/execute \
  -H "Content-Type: application/json" \
  -d '{"task":"open github, search for react tutorials, click first result"}'
```

---

### 3. Plan Generation

**Endpoint:** `POST /api/plan`

**Purpose:** Generate action plan without executing

**Request Body:**
```json
{
  "task": "search kubernetes on youtube",
  "context": []
}
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| task | string | ✅ | Task description |
| context | array | ❌ | Previous task history for context |

**Response:**
```json
{
  "success": true,
  "task": "search kubernetes on youtube",
  "plan": [
    {
      "tool": "open_website",
      "params": {"url": "https://youtube.com"},
      "critical": true
    },
    {
      "tool": "wait",
      "params": {"seconds": 3},
      "critical": false
    },
    {
      "tool": "click_text",
      "params": {"text": "search"},
      "critical": true
    },
    {
      "tool": "type",
      "params": {"text": "kubernetes"},
      "critical": true
    },
    {
      "tool": "press_key",
      "params": {"key": "Return"},
      "critical": true
    }
  ],
  "action_count": 5,
  "actions": [
    {"tool": "open_website", "critical": true},
    {"tool": "wait", "critical": false},
    ...
  ]
}
```

**Examples:**

```bash
# Simple plan
curl -X POST http://localhost:5000/api/plan \
  -H "Content-Type: application/json" \
  -d '{"task":"take a screenshot"}'

# Plan with context
curl -X POST http://localhost:5000/api/plan \
  -H "Content-Type: application/json" \
  -d '{
    "task":"then search for neural networks",
    "context":["previously opened youtube"]
  }'
```

---

### 4. Execute Plan

**Endpoint:** `POST /api/execute-plan`

**Purpose:** Execute a pre-generated plan

**Request Body:**
```json
{
  "plan": [
    {"tool": "open_website", "params": {"url": "google.com"}},
    {"tool": "wait", "params": {"seconds": 2}},
    {"tool": "type", "params": {"text": "hello"}}
  ],
  "max_retries": 3
}
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| plan | array | ✅ | Array of action objects |
| max_retries | integer | 3 | Max retry attempts |

**Response:**
```json
{
  "success": true,
  "status": "completed",
  "total_actions": 3,
  "successful_actions": 3,
  "failed_actions": 0,
  "results": [
    {
      "tool": "open_website",
      "params": {"url": "google.com"},
      "success": true,
      "output": "Opened: https://google.com",
      "retry_count": 0,
      "timestamp": "2024-01-10T15:30:00.000Z"
    },
    ...
  ]
}
```

**Examples:**

```bash
# Execute a plan
curl -X POST http://localhost:5000/api/execute-plan \
  -H "Content-Type: application/json" \
  -d '{
    "plan": [
      {"tool": "open_website", "params": {"url": "google.com"}},
      {"tool": "wait", "params": {"seconds": 2}},
      {"tool": "click_text", "params": {"text": "Search"}}
    ]
  }'
```

---

### 5. Retry with Feedback

**Endpoint:** `POST /api/retry`

**Purpose:** Retry last task with failure feedback

**Request Body:**
```json
{
  "feedback": "Text was not found, try scrolling first"
}
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| feedback | string | ✅ | What failed and how to improve |

**Response:**
```json
{
  "success": true,
  "status": "retry_completed",
  "result": {
    "improved_plan_actions": 6,
    "execution": {
      "status": "completed",
      "successful": 6,
      "total_actions": 6
    },
    "verification": {
      "success": true,
      "reason": "Task completed successfully"
    }
  }
}
```

**Examples:**

```bash
# Retry with feedback
curl -X POST http://localhost:5000/api/retry \
  -H "Content-Type: application/json" \
  -d '{"feedback":"Button not found, use scroll down first"}'
```

---

### 6. Execution History

**Endpoint:** `GET /api/history`

**Purpose:** Get past execution history

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| limit | integer | 10 | Number of records |

**Response:**
```json
{
  "success": true,
  "count": 3,
  "history": [
    {
      "task": "open youtube",
      "successful": 5,
      "total": 5,
      "verified": true
    },
    {
      "task": "search machine learning",
      "successful": 4,
      "total": 5,
      "verified": true
    },
    {
      "task": "create folder test",
      "successful": 1,
      "total": 1,
      "verified": true
    }
  ]
}
```

**Examples:**

```bash
# Get last 10 executions
curl http://localhost:5000/api/history

# Get last 5 executions
curl "http://localhost:5000/api/history?limit=5"

# Get last 100 executions
curl "http://localhost:5000/api/history?limit=100"
```

---

### 7. System Information

**Endpoint:** `GET /api/info`

**Purpose:** Get system and capability information

**Response:**
```json
{
  "name": "Autonomous AI Agent v3",
  "type": "Dynamic Computer-Use Agent",
  "architecture": "OTAV (Observe → Think → Act → Verify)",
  "features": [
    "No hardcoded commands",
    "No hardcoded apps",
    "No hardcoded websites",
    "Dynamic reasoning with LLM",
    "Automatic retry with improvement",
    "OCR-based element detection",
    "Screen understanding",
    "Memory and context awareness",
    "Execution verification"
  ],
  "universal_actions": [
    "open_website",
    "open_app",
    "open_folder",
    "screenshot",
    "click_text",
    "click",
    "type",
    "press_key",
    "hotkey",
    "scroll",
    "wait",
    "create_folder",
    "verify_text",
    "search",
    "select_all",
    "copy",
    "paste",
    "clear_field"
  ]
}
```

---

## Universal Actions Reference

### Action Format

Every action has this structure:

```json
{
  "tool": "action_name",
  "params": {
    "param1": "value1",
    "param2": "value2"
  },
  "critical": true
}
```

### Available Actions

#### 1. open_website

Open any website

```json
{
  "tool": "open_website",
  "params": {"url": "https://youtube.com"},
  "critical": true
}
```

| Parameter | Type | Required | Example |
|-----------|------|----------|---------|
| url | string | ✅ | `"youtube.com"` or `"https://youtube.com"` |

**Notes:**
- Auto-adds `https://` if missing
- Accepts domain names without protocol

---

#### 2. open_app

Open any application

```json
{
  "tool": "open_app",
  "params": {"name": "VS Code"},
  "critical": true
}
```

| Parameter | Type | Required | Example |
|-----------|------|----------|---------|
| name | string | ✅ | `"VS Code"`, `"Chrome"`, `"Notepad"` |

**Notes:**
- Searches in system PATH
- Tries multiple executable formats
- Works on Windows, macOS, Linux

---

#### 3. open_folder

Open or create folder

```json
{
  "tool": "open_folder",
  "params": {"path": "~/Desktop/MyFolder"},
  "critical": true
}
```

| Parameter | Type | Required | Example |
|-----------|------|----------|---------|
| path | string | ✅ | `"~/Desktop"`, `"C:/Users/...`, `"Desktop/Folder"` |

**Notes:**
- Auto-expands `~` to home directory
- Auto-creates if doesn't exist
- Works with relative and absolute paths

---

#### 4. screenshot

Take screenshot

```json
{
  "tool": "screenshot",
  "params": {},
  "critical": false
}
```

**Notes:**
- Saves to `screenshots/` folder
- No parameters needed
- Returns screenshot path

---

#### 5. click_text

Click visible text (OCR-based)

```json
{
  "tool": "click_text",
  "params": {"text": "Search"},
  "critical": true
}
```

| Parameter | Type | Required | Example |
|-----------|------|----------|---------|
| text | string | ✅ | `"Search"`, `"Submit"` |

**Notes:**
- Case-insensitive
- Supports partial matching
- Uses OCR to find text

---

#### 6. click

Click coordinates

```json
{
  "tool": "click",
  "params": {"x": 450, "y": 120, "button": "left"},
  "critical": true
}
```

| Parameter | Type | Required | Default | Example |
|-----------|------|----------|---------|---------|
| x | integer | ✅ | - | `450` |
| y | integer | ✅ | - | `120` |
| button | string | ❌ | `"left"` | `"left"`, `"right"`, `"middle"` |

---

#### 7. type

Type text

```json
{
  "tool": "type",
  "params": {"text": "hello world", "interval": 0.05},
  "critical": true
}
```

| Parameter | Type | Required | Default | Example |
|-----------|------|----------|---------|---------|
| text | string | ✅ | - | `"hello"` |
| interval | float | ❌ | `0.05` | `0.1` |

**Notes:**
- Handles special characters
- `interval` = delay between keys (seconds)

---

#### 8. press_key

Press single key

```json
{
  "tool": "press_key",
  "params": {"key": "Return"},
  "critical": true
}
```

| Parameter | Type | Required | Example |
|-----------|------|----------|---------|
| key | string | ✅ | `"Return"`, `"Tab"`, `"Escape"`, `"Delete"` |

**Supported Keys:**
- Letters: `"a"`, `"b"`, etc.
- Numbers: `"0"` - `"9"`
- Special: `"Return"`, `"Tab"`, `"Space"`, `"Backspace"`, `"Delete"`, `"Escape"`
- Navigation: `"Up"`, `"Down"`, `"Left"`, `"Right"`, `"Home"`, `"End"`
- Function: `"f1"` - `"f12"`

---

#### 9. hotkey

Key combination (Ctrl+C, Alt+Tab, etc)

```json
{
  "tool": "hotkey",
  "params": {"keys": ["ctrl", "c"]},
  "critical": true
}
```

| Parameter | Type | Required | Example |
|-----------|------|----------|---------|
| keys | array | ✅ | `["ctrl", "c"]`, `["alt", "tab"]` |

**Common Combinations:**
- Copy: `["ctrl", "c"]`
- Paste: `["ctrl", "v"]`
- Undo: `["ctrl", "z"]`
- Select All: `["ctrl", "a"]`
- Tab: `["alt", "tab"]`

---

#### 10. scroll

Scroll mouse wheel

```json
{
  "tool": "scroll",
  "params": {"pixels": 5, "x": 450, "y": 300},
  "critical": false
}
```

| Parameter | Type | Required | Default | Example |
|-----------|------|----------|---------|---------|
| pixels | integer | ✅ | - | `5`, `-5` (negative = up) |
| x | integer | ❌ | center | `450` |
| y | integer | ❌ | center | `300` |

---

#### 11. wait

Wait for seconds

```json
{
  "tool": "wait",
  "params": {"seconds": 2},
  "critical": false
}
```

| Parameter | Type | Required | Example |
|-----------|------|----------|---------|
| seconds | float | ✅ | `1`, `2.5` |

---

#### 12. create_folder

Create folder

```json
{
  "tool": "create_folder",
  "params": {"path": "~/Desktop/MyProject"},
  "critical": true
}
```

| Parameter | Type | Required | Example |
|-----------|------|----------|---------|
| path | string | ✅ | `"~/Desktop/Folder"`, `"./src"` |

---

#### 13. verify_text

Verify text appeared

```json
{
  "tool": "verify_text",
  "params": {"text": "Success", "timeout": 5},
  "critical": false
}
```

| Parameter | Type | Required | Default | Example |
|-----------|------|----------|---------|---------|
| text | string | ✅ | - | `"Success"` |
| timeout | integer | ❌ | `5` | `10` |

---

#### 14. search

Search on current website

```json
{
  "tool": "search",
  "params": {"query": "machine learning"},
  "critical": true
}
```

| Parameter | Type | Required | Example |
|-----------|------|----------|---------|
| query | string | ✅ | `"python tutorial"` |

---

#### 15. select_all

Select all (Ctrl+A)

```json
{
  "tool": "select_all",
  "params": {},
  "critical": false
}
```

---

#### 16. copy

Copy (Ctrl+C)

```json
{
  "tool": "copy",
  "params": {},
  "critical": false
}
```

---

#### 17. paste

Paste (Ctrl+V)

```json
{
  "tool": "paste",
  "params": {},
  "critical": false
}
```

---

#### 18. clear_field

Clear text field

```json
{
  "tool": "clear_field",
  "params": {},
  "critical": true
}
```

---

## Error Handling

### HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad request (missing parameters) |
| 404 | Not found |
| 500 | Server error |

### Error Response Format

```json
{
  "success": false,
  "error": "Description of what went wrong"
}
```

### Common Errors

| Error | Solution |
|-------|----------|
| "No task provided" | Add `"task"` to request body |
| "No plan provided" | Add `"plan"` to request body |
| "Planner not available" | Check Gemini API key |
| "Executor not available" | Check Python imports |
| "Agent not available" | Restart Flask server |

---

## Rate Limiting

Currently no rate limiting. For production, implement:

```bash
# Frontend should limit to:
- 1 request per 5 seconds
- Max 10 concurrent tasks
- Max 100 requests per hour per user
```

---

## Examples

### JavaScript (Fetch API)

```javascript
// Execute task
const response = await fetch('http://localhost:5000/api/autonomous/execute', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ task: 'search python on google' })
});

const result = await response.json();
console.log(result);
```

### Python (Requests)

```python
import requests

response = requests.post(
    'http://localhost:5000/api/autonomous/execute',
    json={'task': 'open youtube'}
)

print(response.json())
```

### cURL

```bash
curl -X POST http://localhost:5000/api/autonomous/execute \
  -H "Content-Type: application/json" \
  -d '{"task":"take a screenshot"}'
```

---

## Rate Limit Headers

Current implementation: No headers

Recommended for production:

```
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 9
X-RateLimit-Reset: 1705678900
```

---

**API Version:** 3.0-dynamic
**Last Updated:** 2024
**Status:** Active ✅
