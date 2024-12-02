class ChatData:
    def __init__(self):
        self.messages = []  # Stores the conversation history

    def add_system_message(self, content):
        """Add a system message."""
        self.messages.append({"role": "system", "content": content})

    def add_user_message(self, content):
        """Add a user message."""
        self.messages.append({"role": "user", "content": content})

    def add_assistant_message(self, content, function_call=None):
        """Add an assistant message. Optionally include a function call."""
        message = {"role": "assistant", "content": content}
        if function_call:
            message.pop("content")  # Remove 'content' if there's a function call
            message["function_call"] = function_call
        self.messages.append(message)

    def add_function_message(self, name, content):
        """Add a function message with its name and result."""
        self.messages.append({"role": "function", "name": name, "content": content})

    def get_messages(self):
        """Retrieve the current conversation history."""
        return self.messages

    def reset(self):
        """Clear the conversation history."""
        self.messages = []