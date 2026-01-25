from kernel.safety import safe
from ai.hybrid_llm import think
from config.config import DEBUG

def route(text, recall):
    """
    Main entry point for decision making.
    """
    # 1. Check Safety First
    if not safe(text):
        if DEBUG: print(f"[ROUTER] Blocked unsafe input: {text}")
        return "I'm sorry, but I cannot process that request for safety reasons."

    # 2. Process through Thinking Engine
    try:
        return think(text, recall)
    except Exception as e:
        if DEBUG: print(f"[ROUTER ERROR] {e}")
        return "I encountered an internal error while processing your request."