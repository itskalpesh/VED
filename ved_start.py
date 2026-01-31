"""
VED — Single Unified Entry Point
- Asks user: CLI / GUI / Exit
- After exit, returns to menu
- Works for Python run, BAT, EXE
"""

import sys
import warnings

warnings.filterwarnings("ignore")


def run_cli():
    from kernel.ved import VED

    ved = VED()
    print("\nVED CLI MODE")
    print("Type 'exit' to return to menu.\n")

    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue

            if user_input.lower() in ("exit", "quit"):
                print("VED: Returning to menu...\n")
                break

            response = ved.process(user_input)
            print(f"VED: {response}")

        except KeyboardInterrupt:
            print("\nVED: Interrupted. Returning to menu...\n")
            break

        except Exception as e:
            print(f"VED ERROR: {e}")


def run_gui():
    try:
        print("\nStarting VED GUI (Jarvis Mode)...")
        import ui.jarvis_ui  # GUI blocks here (mainloop inside)
        print("\nVED GUI closed. Returning to menu...\n")
    except Exception as e:
        print("\nGUI failed to start:")
        print(e)
        print("Returning to menu...\n")


def main_menu():
    while True:
        print("======================================")
        print("          VED AI SYSTEM")
        print("======================================")
        print("[1] CLI (Terminal Mode)")
        print("[2] GUI (Jarvis UI Mode)")
        print("[0] Exit")
        print()

        choice = input("Select option (1/2/0): ").strip()

        if choice == "1":
            run_cli()

        elif choice == "2":
            run_gui()

        elif choice == "0":
            print("\nVED: Shutting down. Goodbye 👋")
            sys.exit(0)

        else:
            print("\nInvalid option. Try again.\n")


if __name__ == "__main__":
    main_menu()
