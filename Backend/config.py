"""
Configuration and environment setup for Jarvis AI System
"""
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# ========================
# API KEYS & CREDENTIALS
# ========================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY", "")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# ========================
# PRIMARY LLM CONFIG
# ========================

PRIMARY_LLM = "gemini"  # Options: "gemini", "claude", "ollama"
FALLBACK_LLM = "ollama"

# LLM Models to use
GEMINI_MODEL = "gemini-1.5-pro"  # Best for reasoning & vision
CLAUDE_MODEL = "claude-3-5-sonnet-20241022"  # Excellent for analysis
OLLAMA_MODEL = "llama2"  # Local fallback

# ========================
# VOICE SETTINGS
# ========================

VOICE_ENABLED = os.getenv("VOICE_ENABLED", "False") == "True"
SPEECH_RECOGNITION_ENABLED = True
TEXT_TO_SPEECH_ENABLED = False  # User chose voice input only

# ========================
# SYSTEM SETTINGS
# ========================

DEBUG = os.getenv("DEBUG", "True") == "True"
MAX_EXECUTION_TIME = int(os.getenv("MAX_EXECUTION_TIME", "60"))
SCREENSHOT_INTERVAL = int(os.getenv("SCREENSHOT_INTERVAL", "5"))
MAX_RETRIES = 3
TIMEOUT_SECONDS = 30

# ========================
# FLASK SETTINGS
# ========================

FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
FLASK_PORT = int(os.getenv("FLASK_PORT", "5000"))
CORS_ENABLED = os.getenv("CORS_ENABLED", "True") == "True"

# ========================
# BROWSER SETTINGS
# ========================

HEADLESS_BROWSER = False  # Show browser during automation
BROWSER_TIMEOUT = 30000  # 30 seconds in milliseconds
WAIT_FOR_NAVIGATION = 30000

# ========================
# PATHS
# ========================

PROJECT_ROOT = Path(__file__).parent.parent
BACKEND_DIR = Path(__file__).parent
SCREENSHOTS_DIR = BACKEND_DIR / "screenshots"
LOGS_DIR = BACKEND_DIR / "logs"
MEMORY_DIR = BACKEND_DIR / "memory"

# Create directories if they don't exist
SCREENSHOTS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)
MEMORY_DIR.mkdir(exist_ok=True)

# ========================
# LOGGING SETTINGS
# ========================

LOG_LEVEL = "DEBUG" if DEBUG else "INFO"
LOG_FILE = LOGS_DIR / "jarvis.log"

# ========================
# MEMORY SETTINGS
# ========================

MAX_MEMORY_ITEMS = 1000
MEMORY_FILE = MEMORY_DIR / "memory.json"
CONVERSATION_HISTORY_FILE = MEMORY_DIR / "conversation.json"

# ========================
# TOOL SETTINGS
# ========================

ALLOWED_SYSTEM_COMMANDS = [
    "open",
    "start",
    "code",
    "python",
    "node",
]

BLOCKED_OPERATIONS = [
    "delete",
    "format",
    "remove",
    "uninstall",
]

# ========================
# Validate API Keys
# ========================

def validate_config():
    """Validate that required API keys are set"""
    if PRIMARY_LLM == "gemini" and not GEMINI_API_KEY:
        raise ValueError(
            "GEMINI_API_KEY not set. Please add it to .env file. "
            "Get it from: https://makersuite.google.com/app/apikeys"
        )
    if PRIMARY_LLM == "claude" and not CLAUDE_API_KEY:
        raise ValueError(
            "CLAUDE_API_KEY not set. Please add it to .env file. "
            "Get it from: https://console.anthropic.com/account/keys"
        )
    return True

# ========================
# LLM Selection Logic
# ========================

def get_llm_config():
    """Get the LLM configuration"""
    return {
        "primary": PRIMARY_LLM,
        "fallback": FALLBACK_LLM,
        "models": {
            "gemini": GEMINI_MODEL,
            "claude": CLAUDE_MODEL,
            "ollama": OLLAMA_MODEL,
        },
        "api_keys": {
            "gemini": GEMINI_API_KEY,
            "claude": CLAUDE_API_KEY,
        },
        "base_urls": {
            "ollama": OLLAMA_BASE_URL,
        }
    }

if __name__ == "__main__":
    try:
        validate_config()
        print("✅ Configuration validated successfully")
        print(f"Primary LLM: {PRIMARY_LLM}")
        print(f"Voice Input: {SPEECH_RECOGNITION_ENABLED}")
        print(f"Voice Output: {TEXT_TO_SPEECH_ENABLED}")
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
