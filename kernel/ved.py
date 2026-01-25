from kernel.router import route
from memory.memory import Memory

class VED:
    def __init__(self):
        self.memory = Memory()

    def process(self, text):
        # 1️⃣ Learn from input (e.g., "My name is...")
        learned = self.memory.learn_from_text(text)
        if learned:
            return learned

        # 2️⃣ Load recall (Facts & History)
        recall = self.memory.load()

        # 3️⃣ Route + Think (Safety -> Planner -> LLM)
        response = route(text, recall)

        # 4️⃣ Save conversation to store.json
        self.memory.save_conversation(text, response)

        return response