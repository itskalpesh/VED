# ================================
# VED JARVIS UI (GUI MODE)
# ================================

import sys
from pathlib import Path

# -------------------------------------------------
# FIX: Ensure project root is in PYTHONPATH
# -------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# -------------------------------------------------
# Normal imports (now WORK correctly)
# -------------------------------------------------
import customtkinter as ctk
import threading

from kernel.ved import VED
from voice.tts import speak

print("JARVIS UI FILE LOADED")

# -------------------------------------------------
# Init VED
# -------------------------------------------------
ved = VED()
voice_enabled = True

# -------------------------------------------------
# UI Setup
# -------------------------------------------------
ctk.set_appearance_mode("dark")

app = ctk.CTk()
app.title("VED AI - JARVIS MODE")
app.geometry("900x600")

chat = ctk.CTkTextbox(app, width=860, height=450, wrap="word")
chat.pack(pady=10)

# Code block style
chat.tag_config(
    "code",
    foreground="#dcdcdc",
    background="#1e1e1e"
)

entry = ctk.CTkEntry(app, width=700, placeholder_text="Ask VED...")
entry.pack(pady=10)

# -------------------------------------------------
# Voice handling
# -------------------------------------------------
def speak_later(text):
    if not voice_enabled:
        return

    def _speak():
        speak(text)

    app.after(
        100,
        lambda: threading.Thread(target=_speak, daemon=True).start()
    )

# -------------------------------------------------
# Chat rendering
# -------------------------------------------------
def insert_response(text):
    lines = text.split("\n")
    in_code = False

    for line in lines:
        if line.strip().startswith("```"):
            in_code = not in_code
            continue

        if in_code:
            chat.insert("end", line + "\n", "code")
        else:
            chat.insert("end", line + "\n")

    chat.insert("end", "\n")

# -------------------------------------------------
# Send message
# -------------------------------------------------
def send():
    user_text = entry.get().strip()
    if not user_text:
        return

    entry.delete(0, "end")

    chat.insert("end", f"You: {user_text}\n")
    chat.see("end")
    app.update_idletasks()

    def process_and_reply():
        response = ved.process(user_text)

        def update_ui():
            chat.insert("end", "VED:\n")
            insert_response(response)
            chat.see("end")
            speak_later(response)

        app.after(0, update_ui)

    threading.Thread(target=process_and_reply, daemon=True).start()

# -------------------------------------------------
# Voice toggle
# -------------------------------------------------
def toggle_voice():
    global voice_enabled
    voice_enabled = not voice_enabled
    voice_btn.configure(
        text="Voice: ON" if voice_enabled else "Voice: OFF"
    )

# -------------------------------------------------
# Buttons
# -------------------------------------------------
send_btn = ctk.CTkButton(app, text="Send", command=send)
send_btn.pack(pady=10)

voice_btn = ctk.CTkButton(app, text="Voice: ON", command=toggle_voice)
voice_btn.pack(pady=5)

entry.bind("<Return>", lambda e: send())

print("STARTING TKINTER LOOP")
app.mainloop()
