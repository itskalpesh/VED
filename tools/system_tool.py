# tools/system_tool.py

import platform
import os

INTENTS = [
    "system info",
    "os",
    "operating system",
    "cpu",
    "architecture",
    "machine"
]

def can_handle(text: str) -> bool:
    text = text.lower()
    return any(intent in text for intent in INTENTS)

def run(text: str) -> str:
    return (
        f"OS: {platform.system()} {platform.release()}\n"
        f"Architecture: {platform.machine()}\n"
        f"Processor: {platform.processor()}\n"
        f"Python Version: {platform.python_version()}"
    )

