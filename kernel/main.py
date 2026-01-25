from kernel.ved import VED
import warnings
warnings.filterwarnings("ignore")  # <--- Add this at the very top

from kernel.ved import VED
# ... rest of your code ...
def main():
    ved = VED()
    print("VED CLI MODE")
    print("Type 'exit' to quit.\n")

    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit"]:
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
