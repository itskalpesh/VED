import os
from openai import OpenAI
from config.config import DEBUG

_client = None

def _get_client():
    global _client
    if _client:
        return _client

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        if DEBUG:
            print("[OPENAI] API key missing.")
        return None

    try:
        _client = OpenAI(api_key=api_key)
        if DEBUG:
            print("[OPENAI] Client initialized.")
        return _client
    except Exception as e:
        if DEBUG:
            print("[OPENAI] Init failed:", e)
        return None


def online_generate(text: str, recall: dict) -> str | None:
    client = _get_client()
    if not client:
        return None

    system_prompt = "You are VED, a helpful AI assistant."
    if "user_name" in recall:
        system_prompt += f" The user's name is {recall['user_name']}."

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text},
            ],
            temperature=0.7,
            max_tokens=300,
        )

        if DEBUG:
            print("[OPENAI] Response received.")

        return response.choices[0].message.content.strip()

    except Exception as e:
        if DEBUG:
            print("[OPENAI] Generation error:", e)
        return None
