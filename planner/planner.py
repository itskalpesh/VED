import re
from tools import TOOLS
from models.model_manager import generate
from config.config import (
    ENABLE_TOOLS,
    ENABLE_OFFLINE_LLM,
    ENABLE_ONLINE_LLM,
    DEBUG
)

def needs_online_llm(text: str) -> bool:
    keywords = [
        "compare", "detail", "explain", "advantages", "disadvantages",
        "difference", "vs", "architecture", "design", "pros and cons"
    ]
    return any(k in text.lower() for k in keywords)

def split_steps(text: str) -> list:
    # Splits text by "and then", "then", "also", "next"
    return re.split(r'\s+(?:and\s+then|then|also|next)\s+', text, flags=re.IGNORECASE)

def is_multi_step(text: str) -> bool:
    # Checks if the user is asking for multiple things
    return len(split_steps(text)) > 1

def handle_multi_step(text: str, recall: dict) -> str:
    steps = split_steps(text)
    results = []
    
    for step in steps:
        step = step.strip()
        if step:
            # Recursively call plan_and_execute for each part
            res = plan_and_execute(step, recall)
            if res:
                results.append(f"• {res}")
    
    return "\n".join(results)

def plan_and_execute(text: str, recall: dict) -> str:
    text_l = text.lower()

    # 1. HANDLE MULTIPLE TASKS
    if is_multi_step(text_l):
        if DEBUG: print(f"[PLANNER] Multi-step detected: {text}")
        return handle_multi_step(text, recall)

    # 2. CHECK TOOLS
    if ENABLE_TOOLS:
        for can_handle, run in TOOLS:
            if can_handle(text_l):
                try:
                    return run(text_l, recall)
                except TypeError:
                    return run(text_l)

    # 3. USE LLM (Online or Offline)
    prefer_mode = "online" if needs_online_llm(text) else "offline"
    return generate(text, recall, prefer=prefer_mode)