# tools/file_tool.py

import os

SAFE_DIR = "VED_DATA"

INTENTS = [
    "open file",
    "read file",
    "find file",
    "search file",
    "show file",
    "list files"
]


def can_handle(text: str) -> bool:
    text = text.lower()
    return any(intent in text for intent in INTENTS)


def run(text: str) -> str:
    text = text.lower()

    if not os.path.exists(SAFE_DIR):
        return "Safe data directory not found."

    # List files
    if "list" in text:
        files = os.listdir(SAFE_DIR)
        if not files:
            return "The data folder is empty."
        return "Files:\n" + "\n".join(files)

    # Try to find a file name in text
    files = os.listdir(SAFE_DIR)
    for file in files:
        if file.lower() in text:
            path = os.path.join(SAFE_DIR, file)
            if os.path.isfile(path):
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read(1000)
                    return f"Contents of {file}:\n{content}"
                except Exception:
                    return f"I couldn’t read {file}."

    return "I couldn’t find that file in the safe folder."
