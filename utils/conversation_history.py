import datetime
import json

class ConversationHistory:
    def __init__(self):
        self.history = []

    def add_conversation(self, user_input, response_text):
        conversation = {
            "timestamp": datetime.datetime.now().isoformat(),
            "user_input": user_input,
            "response_text": response_text
        }
        self.history.append(conversation)

    def save_history(self, filename):
        with open(filename, "w") as f:
            json.dump(self.history, f)

    def load_history(self, filename):
        try:
            with open(filename, "r") as f:
                self.history = json.load(f)
        except FileNotFoundError:
            pass

    def get_history(self):
        return self.history

    def add_to_history(self, user_input, response_text):
        self.history.append({"timestamp": datetime.datetime.now().isoformat(), "user_input": user_input, "response_text": response_text})