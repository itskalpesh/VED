"""
VED Speech-to-Text (STT).
Converts voice input to text for the same brain pipeline.
Voice input → STT → text → brain (router/planner/LLM).
"""

def listen(timeout_sec: float = 5.0) -> str | None:
    """
    Listen for speech and return transcribed text, or None on failure/timeout.
    """
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, timeout=timeout_sec, phrase_time_limit=timeout_sec)
        return r.recognize_google(audio)  # or recognize_sphinx for offline
    except Exception:
        return None
