import json
import pathlib
import re
from config.config import STORE_FILE

class Memory:
    def __init__(self):
        # Ensure the directory exists
        STORE_FILE.parent.mkdir(parents=True, exist_ok=True)
        if not STORE_FILE.exists():
            with open(STORE_FILE, "w") as f:
                json.dump({}, f)

    def load(self):
        try:
            if not STORE_FILE.exists():
                return {}
            with open(STORE_FILE, "r") as f:
                data = json.load(f)
            return data if isinstance(data, dict) else {}
        except (json.JSONDecodeError, Exception):
            return {}

    def save_fact(self, key, value):
        data = self.load()
        data[key] = value
        with open(STORE_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def save_conversation(self, user_text, ai_text):
        data = self.load()
        data["last_user"] = user_text
        data["last_ai"] = ai_text
        with open(STORE_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def learn_from_text(self, user_text):
        """
        Extract facts like user name automatically.
        """
        user_text_l = user_text.lower()
        
        # Expanded Name detection
        patterns = [
            r"my name is ([a-zA-Z ]+)",
            r"call me ([a-zA-Z ]+)",
            r"i am ([a-zA-Z ]+)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_text_l)
            if match:
                name = match.group(1).strip().title()
                # Filter out small words or AI names
                if len(name) > 1 and name.lower() != "ved":
                    self.save_fact("user_name", name)
                    return f"I've noted that down. Nice to meet you, {name}!"
        return None