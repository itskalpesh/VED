import os
from pathlib import Path

# ===== DIRECTORIES =====
BASE_DIR = Path(__file__).parent.parent
MEMORY_DIR = BASE_DIR / "memory"
STORE_FILE = MEMORY_DIR / "store.json"

# ===== LLM MODE =====
# "auto" (Online first) | "offline" (Local only) | "online" (Cloud only)
LLM_MODE = "auto"

# ===== CORE SWITCHES =====
ENABLE_TOOLS = True
ENABLE_OFFLINE_LLM = True  # Set to True if you have the GGUF model
ENABLE_ONLINE_LLM = True

# ===== API KEYS =====
# Ensure this is set in your environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# ===== INTERFACES =====
ENABLE_VOICE = True
ENABLE_GUI = True
ENABLE_CLI = True

# ===== SAFETY & DEBUG =====
STRICT_SAFETY = True
DEBUG = False