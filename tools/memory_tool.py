# tools/memory_tool.py

INTENTS = [
    "what did i ask last time",
    "what was my last question",
    "what did you say last time",
    "what do you remember",
    "do you remember me"
]

def can_handle(text: str) -> bool:
    text = text.lower()
    return any(intent in text for intent in INTENTS)

def run(text: str, recall: dict) -> str:
    if "last_user" in recall:
        return f"Last time, you asked: \"{recall['last_user']}\""
    return "I don’t have any past conversation stored yet."
