import customtkinter as ctk
import threading
from kernel.ved import VED
from voice.tts import speak
print("JARVIS UI FILE LOADED")

ved = VED()
voice_enabled = True


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

def speak_later(text):
    if not voice_enabled:
        return

    def _speak():
        speak(text)

    app.after(100, lambda: threading.Thread(target=_speak, daemon=True).start())


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

def send():
    user_text = entry.get().strip()
    if not user_text:
        return

    entry.delete(0, "end")

    # Show user text immediately
    chat.insert("end", f"You: {user_text}\n")
    chat.see("end")
    app.update_idletasks()

    # Run LLM in BACKGROUND thread
    def process_and_reply():
        response = ved.process(user_text)

        # UI update must happen on main thread
        def update_ui():
            chat.insert("end", "VED:\n")
            insert_response(response)
            chat.see("end")
            speak_later(response)


        app.after(0, update_ui)

    threading.Thread(target=process_and_reply, daemon=True).start()

def toggle_voice():
    global voice_enabled
    voice_enabled = not voice_enabled
    voice_btn.configure(text="Voice: ON" if voice_enabled else "Voice: OFF")

# Send button
send_btn = ctk.CTkButton(app, text="Send", command=send)
send_btn.pack(pady=10)
voice_btn = ctk.CTkButton(app, text="Voice: ON", command=toggle_voice)
voice_btn.pack(pady=5)


# Press Enter to send
entry.bind("<Return>", lambda e: send())

print("STARTING TKINTER LOOP")
app.mainloop()

