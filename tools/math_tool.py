# tools/math_tool.py

import re

INTENTS = [
    "calculate",
    "add",
    "subtract",
    "multiply",
    "divide",
    "what is",
    "solve"
]

def can_handle(text: str) -> bool:
    text = text.lower()
    return any(intent in text for intent in INTENTS) and any(
        char.isdigit() for char in text
    )

def run(text: str) -> str:
    # Extract the FULL math expression safely
    matches = re.findall(r"[0-9\.\+\-\*\/\(\)]+", text.replace(" ", ""))

    if not matches:
        return "I couldn't find a math expression."

    expr = matches[0]

    try:
        result = eval(expr, {"__builtins__": {}})
        return f"The answer is {result}."
    except Exception:
        return "I couldn't calculate that safely."
