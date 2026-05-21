# JARVIS API DOCUMENTATION

## Overview
JARVIS exposes RESTful API endpoints for executing autonomous tasks using natural language processing.

## Base URL
```
http://127.0.0.1:5000
```

## Authentication
Currently no authentication required (runs on localhost). For production, implement API key authentication.

---

## Endpoints

### 1. Health Check
Check if backend is running.

**Endpoint**: `GET /health`

**Response**:
```json
{
  "success": true
}
```

---

### 2. Status
Get detailed backend information.

**Endpoint**: `GET /status`

**Response**:
```json
{
  "backend": "running",
  "version": "1.0",
  "python": "3.11.0",
  "platform": "Windows",
  "endpoints": {
    "health": "http://127.0.0.1:5000/health",
    "execute": "http://127.0.0.1:5000/api/autonomous/execute",
    "status": "http://127.0.0.1:5000/status"
  },
  "timestamp": "2024-05-21T10:30:45.123456"
}
```

---

### 3. Execute Task
Execute a natural language task.

**Endpoint**: `POST /api/autonomous/execute`

**Headers**:
```
Content-Type: application/json
```

**Request Body**:
```json
{
  "task": "natural language task description"
}
```

**Response (Success)**:
```json
{
  "success": true,
  "task": "Search Google for python tutorials",
  "plan": [
    {
      "tool": "google_search",
      "params": {
        "query": "python tutorials"
      }
    }
  ],
  "results": [
    {
      "tool": "google_search",
      "success": true,
      "result": {
        "success": true,
        "message": "Searched Google for: python tutorials"
      }
    }
  ],
  "message": "Task completed",
  "timestamp": "2024-05-21T10:30:45.123456"
}
```

**Response (Error)**:
```json
{
  "success": false,
  "error": "Task missing",
  "timestamp": "2024-05-21T10:30:45.123456"
}
```

---

## Request/Response Details

### Task Parameter
The task parameter should be natural language describing what the user wants to accomplish.

**Valid Examples**:
- "Search Google for Python tutorials"
- "Create an Excel budget tracker"
- "Send email to john@example.com with attachment"
- "Take screenshot and save to Pictures"
- "Clone repository and create React component"

**Invalid Examples**:
- "" (empty string)
- null
- undefined

### Plan Response
The plan is a JSON array of tools that will be executed sequentially.

**Structure**:
```json
{
  "tool": "tool_name",
  "params": {
    "param1": "value1",
    "param2": "value2"
  }
}
```

### Results Response
Contains execution details for each step in the plan.

**Structure**:
```json
{
  "tool": "tool_name",
  "success": true/false,
  "result": {
    "success": true/false,
    "message": "Operation result"
  },
  "error": "error message if failed"
}
```

---

## Example Requests

### Example 1: Simple Search
```bash
curl -X POST http://127.0.0.1:5000/api/autonomous/execute \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Search Google for machine learning"
  }'
```

### Example 2: File Operation
```bash
curl -X POST http://127.0.0.1:5000/api/autonomous/execute \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Create folder named MyProject on Desktop"
  }'
```

### Example 3: Email with Attachment
```bash
curl -X POST http://127.0.0.1:5000/api/autonomous/execute \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Send email to john@example.com with subject report and attachment at ~/Documents/report.pdf"
  }'
```

### Example 4: Multi-Step Workflow
```bash
curl -X POST http://127.0.0.1:5000/api/autonomous/execute \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Open Excel, create a budget tracker with food 5000 transport 2000 entertainment 1500, and add a pie chart"
  }'
```

---

## Client Libraries

### Python Client
```python
import requests
import json

class JarvisClient:
    def __init__(self, base_url="http://127.0.0.1:5000"):
        self.base_url = base_url
    
    def health(self):
        """Check health"""
        response = requests.get(f"{self.base_url}/health")
        return response.json()
    
    def status(self):
        """Get status"""
        response = requests.get(f"{self.base_url}/status")
        return response.json()
    
    def execute(self, task):
        """Execute task"""
        payload = {"task": task}
        response = requests.post(
            f"{self.base_url}/api/autonomous/execute",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        return response.json()

# Usage
client = JarvisClient()
result = client.execute("Search Google for Python")
print(result)
```

### JavaScript/Node.js Client
```javascript
class JarvisClient {
  constructor(baseUrl = "http://127.0.0.1:5000") {
    this.baseUrl = baseUrl;
  }
  
  async health() {
    const response = await fetch(`${this.baseUrl}/health`);
    return response.json();
  }
  
  async status() {
    const response = await fetch(`${this.baseUrl}/status`);
    return response.json();
  }
  
  async execute(task) {
    const response = await fetch(
      `${this.baseUrl}/api/autonomous/execute`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ task })
      }
    );
    return response.json();
  }
}

// Usage
const client = new JarvisClient();
client.execute("Search Google for Python").then(result => {
  console.log(result);
});
```

### cURL Examples
```bash
# Health check
curl http://127.0.0.1:5000/health

# Get status
curl http://127.0.0.1:5000/status

# Execute task
curl -X POST http://127.0.0.1:5000/api/autonomous/execute \
  -H "Content-Type: application/json" \
  -d '{"task": "your task here"}'
```

---

## Error Handling

### Common Errors

**400 Bad Request**
```json
{
  "success": false,
  "error": "Task missing",
  "timestamp": "2024-05-21T10:30:45.123456"
}
```
Cause: Task parameter is missing or empty.

**500 Internal Server Error**
```json
{
  "success": false,
  "error": "Tool execution failed",
  "timestamp": "2024-05-21T10:30:45.123456"
}
```
Cause: Backend error during execution. Check logs.

**Connection Refused**
```
Error: connect ECONNREFUSED 127.0.0.1:5000
```
Cause: Backend not running. Start with `python app.py`

### Error Handling Best Practices
```python
try:
    result = client.execute("task")
    
    if result['success']:
        print("Success:", result['results'])
    else:
        print("Failed:", result['error'])
        
except requests.exceptions.ConnectionError:
    print("Backend not reachable")
except Exception as e:
    print("Error:", str(e))
```

---

## Rate Limiting

Currently not implemented. For production:
- Implement per-IP rate limiting
- Use token buckets
- Return 429 Too Many Requests

---

## CORS

CORS is enabled for all origins. For production:
```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5173"],
        "methods": ["POST", "GET"]
    }
})
```

---

## Timeout & Performance

### Expected Response Times
- Simple tools: < 1 second
- Complex workflows: 5-30 seconds
- Long operations: May take minutes

### Timeout Configuration
Set in `config.py`:
```python
MAX_EXECUTION_TIME = 60  # seconds
```

### Async Execution
For long-running tasks, consider:
1. Implementing background jobs
2. Using message queues (Celery)
3. WebSocket for progress updates

---

## Logging

### Backend Logs
All API calls are logged with timestamps:
```
[2024-05-21 10:30:45] [TASK] Received task: Search Google for python
[2024-05-21 10:30:45] [PLANNING] Planning task: Search Google for python
[2024-05-21 10:30:46] [PLAN] Generated plan with 1 steps
[2024-05-21 10:30:46] [EXECUTING] Executing plan...
[2024-05-21 10:30:47] [SUCCESS] google_search
```

### Access Logs
```python
# Add to app.py for verbose logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## Security Considerations

### Input Validation
The AI planner validates tasks, but additional validation recommended:
```python
def validate_task(task):
    if not task or not isinstance(task, str):
        return False
    if len(task) > 1000:
        return False
    if any(dangerous in task for dangerous in ['rm -rf', 'DROP TABLE']):
        return False
    return True
```

### Output Sanitization
All results are JSON serialized, preventing injection attacks.

### File Operations
Always use expanded paths:
```python
path = os.path.expanduser(path)
path = os.path.abspath(path)
```

---

## Integration Examples

### Flask Integration
```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/task', methods=['POST'])
def create_task():
    data = request.json
    task = data.get('task')
    
    import requests
    response = requests.post(
        'http://127.0.0.1:5000/api/autonomous/execute',
        json={'task': task}
    )
    
    return response.json()
```

### React Integration
```javascript
import { useState } from 'react';

function TaskExecutor() {
  const [task, setTask] = useState('');
  const [result, setResult] = useState(null);
  
  const execute = async () => {
    const response = await fetch(
      'http://127.0.0.1:5000/api/autonomous/execute',
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ task })
      }
    );
    setResult(await response.json());
  };
  
  return (
    <div>
      <input value={task} onChange={e => setTask(e.target.value)} />
      <button onClick={execute}>Execute</button>
      {result && <pre>{JSON.stringify(result, null, 2)}</pre>}
    </div>
  );
}
```

---

## Versioning

Current API Version: **1.0**

Future versions will maintain backward compatibility with `/v1/` prefix:
```
/v1/api/autonomous/execute
/v2/api/autonomous/execute
```

---

## Webhooks (Future)

Planned feature for async task notifications:
```json
{
  "webhook_url": "https://yourserver.com/webhook",
  "events": ["task.completed", "task.failed"]
}
```

---

## Changelog

### v1.0 (May 2024)
- Initial release
- 100+ tools support
- Natural language planning
- Full REST API

---

## Support

- GitHub Issues: Report bugs
- Documentation: [TOOLS_REFERENCE.md](./TOOLS_REFERENCE.md)
- Setup Guide: [JARVIS_SETUP_EXTENDED.md](./JARVIS_SETUP_EXTENDED.md)

---

## License

MIT License - See LICENSE file

---

**API Documentation Version**: 1.0
**Last Updated**: May 2024
