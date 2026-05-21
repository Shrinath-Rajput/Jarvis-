# config.py

"""
Jarvis AI Configuration File
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# ==========================================
# LOAD ENV VARIABLES
# ==========================================

load_dotenv()

# ==========================================
# PROJECT PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

SCREENSHOTS_DIR = BASE_DIR / "screenshots"
LOGS_DIR = BASE_DIR / "logs"
MEMORY_DIR = BASE_DIR / "memory"

# Create folders automatically
SCREENSHOTS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)
MEMORY_DIR.mkdir(exist_ok=True)

# ==========================================
# OLLAMA SETTINGS
# ==========================================

PRIMARY_LLM = "ollama"

FALLBACK_LLM = "gemini"

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3"
)

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://127.0.0.1:11434"
)

# ==========================================
# OPTIONAL API KEYS
# ==========================================

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY",
    ""
)

CLAUDE_API_KEY = os.getenv(
    "CLAUDE_API_KEY",
    ""
)

# ==========================================
# GEMINI / CLAUDE MODELS
# ==========================================

GEMINI_MODEL = "gemini-2.0-flash"

CLAUDE_MODEL = "claude-3-5-sonnet-20241022"

# ==========================================
# VOICE SETTINGS
# ==========================================

VOICE_ENABLED = False

SPEECH_RECOGNITION_ENABLED = True

TEXT_TO_SPEECH_ENABLED = False

# ==========================================
# EXECUTION SETTINGS
# ==========================================

DEBUG = True

MAX_EXECUTION_TIME = 60

MAX_RETRIES = 3

TIMEOUT_SECONDS = 30

# ==========================================
# FLASK SETTINGS
# ==========================================

FLASK_HOST = "127.0.0.1"

FLASK_PORT = 5000

CORS_ENABLED = True

# ==========================================
# LOGGING SETTINGS
# ==========================================

LOG_LEVEL = "DEBUG"

LOG_FILE = LOGS_DIR / "jarvis.log"

# ==========================================
# MEMORY SETTINGS
# ==========================================

MAX_MEMORY_ITEMS = 1000

MEMORY_FILE = MEMORY_DIR / "memory.json"

CONVERSATION_HISTORY_FILE = (
    MEMORY_DIR / "conversation.json"
)

# ==========================================
# SECURITY SETTINGS
# ==========================================

ALLOWED_SYSTEM_COMMANDS = [

    "open",
    "start",
    "code",
    "python",
    "node",
]

BLOCKED_OPERATIONS = [

    "delete",
    "remove",
    "format",
    "uninstall",
]

# ==========================================
# VALIDATE CONFIG
# ==========================================

def validate_config():

    if PRIMARY_LLM == "gemini":

        if not GEMINI_API_KEY:

            raise ValueError(
                "GEMINI_API_KEY missing"
            )

    if PRIMARY_LLM == "claude":

        if not CLAUDE_API_KEY:

            raise ValueError(
                "CLAUDE_API_KEY missing"
            )

    return True

# ==========================================
# GET LLM CONFIG
# ==========================================

def get_llm_config():

    return {

        "primary": PRIMARY_LLM,

        "fallback": FALLBACK_LLM,

        "models": {

            "gemini": GEMINI_MODEL,

            "claude": CLAUDE_MODEL,

            "ollama": OLLAMA_MODEL,
        },

        "base_urls": {

            "ollama": OLLAMA_BASE_URL
        }
    }

# ==========================================
# TEST CONFIG
# ==========================================

if __name__ == "__main__":

    try:

        validate_config()

        print(
            "✅ Configuration Loaded"
        )

        print(
            f"Primary LLM: {PRIMARY_LLM}"
        )

        print(
            f"Ollama Model: {OLLAMA_MODEL}"
        )

        print(
            f"Ollama URL: {OLLAMA_BASE_URL}"
        )

    except Exception as e:

        print(
            f"❌ Config Error: {e}"
        )