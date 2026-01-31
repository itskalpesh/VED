"""
VED Voice Loop — continuous listen → brain → speak.
Voice ON/OFF toggle; voice confirmation for dangerous OS actions (shutdown/restart).
"""

from voice.stt import listen
from voice.tts import speak

# Voice confirmation for dangerous actions: ask user to say "yes" before executing
def ask_voice_confirm(prompt: str, timeout_sec: float = 10.0) -> bool:
    """Speak prompt, listen for yes/confirm; return True if confirmed."""
    speak(prompt)
    text = listen(timeout_sec=timeout_sec)
    if not text:
        return False
    t = text.strip().lower()
    return t in ("yes", "yeah", "confirm", "ok", "okay", "do it")


def run_voice_loop(ved_process_fn, voice_enabled: bool = True):
    """
    Optional: run a loop that listens → process → speaks.
    ved_process_fn(text, confirmed_danger) returns response string.
    """
    if not voice_enabled:
        return
    while True:
        text = listen(timeout_sec=5.0)
        if not text:
            continue
        # Dangerous intents: ask for confirmation
        confirmed = False
        if any(w in text.lower() for w in ["shutdown", "restart", "reboot"]):
            confirmed = ask_voice_confirm("Say yes to confirm shutdown or restart.")
        response = ved_process_fn(text, confirmed_danger=confirmed)
        if response:
            speak(response)
