def can_handle(text):
    return "disconnect internet" in text or "turn off internet" in text

def run(text, recall=None):
    return (
        "I can't control your internet connection directly.\n"
        "You can:\n"
        "• Turn off Wi-Fi from system tray\n"
        "• Disable network adapter\n"
        "• Unplug router\n"
    )
