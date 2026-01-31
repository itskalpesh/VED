"""
VED Doctor — health checks for OS control, Python–C++ bridge, LLM, memory, voice, GUI.
Run: python -m doctor.ved_doctor
"""

import sys
from pathlib import Path

# Project root
ROOT = Path(__file__).resolve().parent.parent


def check(name: str, ok: bool, detail: str = "") -> None:
    status = "OK" if ok else "FAIL"
    print(f"  [{status}] {name}" + (f" — {detail}" if detail else ""))


def main() -> int:
    print("VED Doctor — diagnostics\n")
    all_ok = True

    # 1. OS control (ved_os) — optional; project runs without it
    print("1. OS control (ved_os) [optional]")
    try:
        import ved_os
        check("ved_os module", True, "Python–C++ bridge loaded")
        try:
            apps = ved_os.get_running_apps()
            check("get_running_apps()", True, f"{len(apps)} windows")
        except Exception as e:
            check("get_running_apps()", False, str(e))
    except ImportError:
        check("ved_os module", False, "Build os_control and add to PYTHONPATH")
    print()

    # 2. Python version
    print("2. Python")
    v = sys.version_info
    check("Python 3.10+", v.major == 3 and v.minor >= 10, f"{v.major}.{v.minor}.{v.micro}")
    print()

    # 3. Brain
    print("3. Brain")
    try:
        from brain.intent_engine import classify
        intent, detail = classify("open notepad")
        check("intent_engine", intent == "os_command" and detail == "open_software")
    except ImportError as e:
        check("brain", False, str(e))
        all_ok = False
    print()

    # 4. LLM availability
    print("4. LLM")
    try:
        from config.config import ENABLE_OFFLINE_LLM, ENABLE_ONLINE_LLM
        check("ENABLE_OFFLINE_LLM", True, str(ENABLE_OFFLINE_LLM))
        check("ENABLE_ONLINE_LLM", True, str(ENABLE_ONLINE_LLM))
        try:
            from models.model_manager import get_current_mode
            check("model_manager", True, get_current_mode())
        except Exception as e:
            check("model_manager", False, str(e))
    except ImportError as e:
        check("config/models", False, str(e))
        all_ok = False
    print()

    # 5. Memory
    print("5. Memory")
    try:
        from memory.memory import Memory
        m = Memory()
        data = m.load()
        check("memory load", True, f"{len(data)} keys")
    except Exception as e:
        check("memory", False, str(e))
        all_ok = False
    print()

    # 6. Voice
    print("6. Voice")
    try:
        from voice.tts import speak
        check("TTS (pyttsx3)", True)
    except ImportError:
        check("TTS", False, "pyttsx3 not installed or failed")
        all_ok = False
    try:
        import speech_recognition as sr
        check("STT (speech_recognition)", True)
    except ImportError:
        check("STT", False, "speech_recognition not installed")
    print()

    # 7. GUI bridge (optional) — don't import jarvis_ui (it runs mainloop and blocks)
    print("7. GUI")
    try:
        import customtkinter
        gui_file = ROOT / "ui" / "jarvis_ui.py"
        check("GUI (customtkinter + ui/jarvis_ui.py)", gui_file.exists())
    except ImportError:
        check("GUI", False, "customtkinter not installed")
    except Exception as e:
        check("GUI", False, str(e))
    print()

    # Only fail on critical checks (brain, memory, config); ved_os is optional
    critical_ok = all_ok
    print("Done." if critical_ok else "Some checks failed.")
    return 0 if critical_ok else 1


if __name__ == "__main__":
    sys.exit(main())
