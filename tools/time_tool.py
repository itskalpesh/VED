# tools/time_tool.py

from datetime import datetime

INTENTS = [
    "time",
    "current time",
    "what time",
    "date",
    "today",
    "day",
    "current date"
]

def can_handle(text: str) -> bool:
    text = text.lower()
    return any(intent in text for intent in INTENTS)

def run(text: str) -> str:
    now = datetime.now()

    if "time" in text:
        return now.strftime("The current time is %I:%M %p.")

    if "date" in text or "day" in text:
        return now.strftime("Today is %A, %d %B %Y.")

    return "I couldn’t determine what time information you need."
