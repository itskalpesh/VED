from memory.memory import Memory

# Single brain: brain.router (intent → permission → ved_os or planner/LLM)
try:
    from brain.router import route
except ImportError:
    from kernel.router import route  # fallback if brain not used

class VED:
    def __init__(self):
        self.memory = Memory()

    def process(self, text, confirmed_danger=False):
        # 1️⃣ Learn from input (e.g., "My name is...")
        learned = self.memory.learn_from_text(text)
        if learned:
            return learned

        # 2️⃣ Load recall (Facts & History)
        recall = self.memory.load()

        # 3️⃣ Route + Think (Safety → Intent → Permission → ved_os or Planner/LLM)
        response = route(text, recall, confirmed_danger=confirmed_danger)

        # 4️⃣ Save conversation to store.json
        self.memory.save_conversation(text, response)

        return response