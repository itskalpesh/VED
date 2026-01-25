from planner.planner import plan_and_execute
from config.config import DEBUG, LLM_MODE
from models.model_manager import generate

def think(text, recall):
    text_l = text.lower()

    # 1️⃣ Greetings (FAST PATH)
    if text_l in ["hi", "hello", "hey"]:
        name = recall.get("user_name")
        return f"Hello {name}! How can I help you?" if name else "Hello! How can I help you?"

    # 2️⃣ Identity (FAST PATH)
    name_intents = ["what is my name", "who am i", "tell me my name", "my name"]
    if any(intent in text_l for intent in name_intents):
        name = recall.get("user_name")
        return f"Your name is {name}." if name else "I don’t know your name yet. You can tell me by saying: my name is ..."

    # 3️⃣ PLANNER (Try tools first)
    try:
        response = plan_and_execute(text, recall)
        # If the planner handled it (Math, Time, etc.), return that
        if response and response != "I’m not sure how to handle that yet.":
            return response
    except Exception as e:
        if DEBUG: print("[DEBUG] Planner failed:", e)

    # 4️⃣ LLM FALLBACK (General Intelligence)
    # If no tools matched, use the LLM to answer the question
    return generate(text, recall, prefer=LLM_MODE)