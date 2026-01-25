import os
import google.generativeai as genai
from config.config import GEMINI_API_KEY, DEBUG

MODEL_NAME = "gemini-2.0-flash"
_configured = False


def _configure_once():
    """
    Configure Gemini SDK only once per process.
    """
    global _configured
    if _configured:
        return True

    api_key = GEMINI_API_KEY or os.getenv("GEMINI_API_KEY")
    if not api_key:
        if DEBUG:
            print("[GEMINI] API key missing. Set GEMINI_API_KEY.")
        return False

    try:
        genai.configure(api_key=api_key)
        _configured = True
        if DEBUG:
            print("[GEMINI] Configured successfully.")
        return True
    except Exception as e:
        if DEBUG:
            print("[GEMINI] Configuration failed:", e)
        return False


def online_generate(text: str, recall: dict) -> str | None:
    """
    Generate a response using Gemini.
    Returns None if Gemini is unavailable.
    """
    if not _configure_once():
        return None

    system_prompt = "You are VED, a helpful AI assistant."
    if "user_name" in recall:
        system_prompt += f" The user's name is {recall['user_name']}."

    try:
        model = genai.GenerativeModel(
            model_name=MODEL_NAME,
            system_instruction=system_prompt,
        )

        response = model.generate_content(text)

        if DEBUG:
            print("[GEMINI] Response received.")

        return response.text.strip() if response and response.text else None

    except Exception as e:
        if DEBUG:
            print("[GEMINI] Generation error:", e)
        return None
