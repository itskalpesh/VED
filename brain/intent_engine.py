"""
VED Intent Engine — classify user input.
Detects: OS commands, file actions, voice commands, normal queries.
No execution here; only classification for the router.
"""

import re
from typing import Literal

IntentType = Literal["os_command", "file_action", "voice_command", "normal_query"]

# OS control intents (map to ved_os after permission check)
OS_OPEN = ["open", "launch", "start", "run"]
OS_CLOSE = ["close", "quit", "exit", "kill", "stop"]
OS_APPS = ["running apps", "what's open", "list apps", "running programs"]
OS_FIND = ["find file", "search for file", "find files"]
OS_OPEN_FILE = ["open file", "open the file"]
OS_OPEN_FOLDER = ["open folder", "open directory", "show folder", "explore"]
OS_SHUTDOWN = ["shutdown", "shut down", "turn off computer"]
OS_RESTART = ["restart", "reboot", "restart computer"]
OS_SLEEP = ["sleep", "suspend", "put to sleep"]
OS_LOCK = ["lock", "lock screen", "lock computer"]

# File actions (read/write — handled by tools or with permission)
FILE_INTENTS = ["read file", "write file", "create file", "delete file", "edit file"]

# Voice is usually inferred by input source (GUI/CLI sends text); keep for future wake-word flow
VOICE_INTENTS = ["hey ved", "okay ved"]  # optional wake word


def classify(text: str) -> tuple[IntentType, str | None]:
    """
    Returns (intent_type, detail).
    detail: for os_command, a slug like "open_software", "close_software", etc.; else None.
    """
    t = text.strip().lower()
    if not t:
        return "normal_query", None

    # --- OS commands (will need ved_os + permission) ---
    if any(w in t for w in OS_SHUTDOWN):
        return "os_command", "request_shutdown"
    if any(w in t for w in OS_RESTART):
        return "os_command", "request_restart"
    if any(w in t for w in OS_SLEEP):
        return "os_command", "request_sleep"
    if any(w in t for w in OS_LOCK):
        return "os_command", "lock_workstation"
    if any(w in t for w in OS_APPS):
        return "os_command", "get_running_apps"
    if any(w in t for w in OS_FIND):
        return "os_command", "find_files"
    if any(w in t for w in OS_OPEN_FOLDER):
        return "os_command", "open_folder"
    if any(w in t for w in OS_OPEN_FILE):
        return "os_command", "open_file"
    if any(w in t for w in OS_CLOSE):
        return "os_command", "close_software"
    if any(w in t for w in OS_OPEN):
        return "os_command", "open_software"

    # --- File actions (tools or permission) ---
    if any(w in t for w in FILE_INTENTS):
        return "file_action", None

    # --- Voice (optional) ---
    if any(w in t for w in VOICE_INTENTS):
        return "voice_command", None

    return "normal_query", None
