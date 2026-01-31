"""
VED — single entry point (Tier-4 upgrade).
Usage: python ved_start.py [cli|gui]
Default: CLI. Use 'gui' for Jarvis UI.
"""

import sys
import warnings
warnings.filterwarnings("ignore")

def main():
    mode = (sys.argv[1] if len(sys.argv) > 1 else "cli").lower()

    if mode == "gui":
        try:
            # GUI runs on import (app.mainloop() in jarvis_ui.py)
            import ui.jarvis_ui  # noqa: F401
        except Exception as e:
            print("GUI not available:", e)
            sys.exit(1)
        return

    # CLI
    from kernel.ved import VED
    ved = VED()
    print("VED CLI MODE")
    print("Type 'exit' to quit.\n")
    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("exit", "quit"):
                print("VED: Shutting down.")
                break
            response = ved.process(user_input)
            print(f"VED: {response}")
        except KeyboardInterrupt:
            print("\nVED: Interrupted. Exiting.")
            break
        except Exception as e:
            print(f"VED ERROR: {e}")


if __name__ == "__main__":
    main()
