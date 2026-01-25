from config.config import ENABLE_ONLINE_LLM, ENABLE_OFFLINE_LLM, DEBUG
from models.offline.qwen_local import offline_generate
from models.online.openai_llm import online_generate as openai_generate
from utils.net_check import internet_available
import time

# Cooldown tracking (seconds)
OPENAI_COOLDOWN = 60
GEMINI_COOLDOWN = 60

_openai_disabled_until = 0
_gemini_disabled_until = 0

CURRENT_MODE = "UNKNOWN"

try:
    from models.online.gemini_llm import online_generate as gemini_generate
except Exception as e:
    if DEBUG:
        print(f"[MODEL_MANAGER] Could not import Gemini: {e}")
    gemini_generate = None


def generate(text, recall, prefer="offline"):
    """
    Handles model selection and fallbacks.

    Priority:
    1. OpenAI
    2. Gemini
    3. Offline Qwen (guaranteed)
    """
    global _openai_disabled_until, _gemini_disabled_until, CURRENT_MODE

    # 🔒 INTERNET CHECK
    if not internet_available():
        CURRENT_MODE = "OFFLINE"
        if DEBUG:
            print("[MODEL_MANAGER] MODE = OFFLINE (no internet)")
        return offline_generate(text, recall)

    # 1️⃣ ONLINE MODE (AUTO / ONLINE)
    if prefer in ["online", "auto"] and ENABLE_ONLINE_LLM:
        now = time.time()

        # 🔹 OpenAI FIRST (with cooldown)
        if openai_generate and now > _openai_disabled_until:
            try:
                response = openai_generate(text, recall)
                if response:
                    CURRENT_MODE = "OPENAI"
                    if DEBUG:
                        print("[MODEL_MANAGER] MODE = OPENAI")
                    return response
            except Exception as e:
                msg = str(e).lower()
                if "quota" in msg or "429" in msg:
                    _openai_disabled_until = now + OPENAI_COOLDOWN
                    if DEBUG:
                        print("[MODEL_MANAGER] OpenAI cooled down for 60s")
                elif DEBUG:
                    print(f"[MODEL_MANAGER] OpenAI failed: {e}")

        # 🔹 Gemini SECOND (with cooldown)
        if gemini_generate and now > _gemini_disabled_until:
            try:
                response = gemini_generate(text, recall)
                if response:
                    CURRENT_MODE = "GEMINI"
                    if DEBUG:
                        print("[MODEL_MANAGER] MODE = GEMINI")
                    return response
            except Exception as e:
                msg = str(e).lower()
                if "quota" in msg or "429" in msg:
                    _gemini_disabled_until = now + GEMINI_COOLDOWN
                    if DEBUG:
                        print("[MODEL_MANAGER] Gemini cooled down for 60s")
                elif DEBUG:
                    print(f"[MODEL_MANAGER] Gemini failed: {e}")

    # 2️⃣ OFFLINE FALLBACK (ALWAYS)
    if ENABLE_OFFLINE_LLM:
        CURRENT_MODE = "OFFLINE"
        if DEBUG:
            print("[MODEL_MANAGER] MODE = OFFLINE")
        return offline_generate(text, recall)

    CURRENT_MODE = "NONE"
    return "I'm sorry, no AI models are currently available. Check your configuration."


def get_current_mode():
    return CURRENT_MODE
