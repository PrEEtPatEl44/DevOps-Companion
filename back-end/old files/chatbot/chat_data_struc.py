import json
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

    def add_assistant_tool_call(self, toolscall):
        """Add a function call to the assistant's response."""
        if toolscall and isinstance(toolscall, list):
            tool_call = toolscall[0]
            function_call = {
                "id": tool_call.id,
                "function": {
                    "name": tool_call.function.name,
                    "arguments": tool_call.function.arguments
                },
                "type": tool_call.type,
            }
            self.messages.append({
                "role": "assistant",
                "tool_calls": [function_call]
            })

    def add_tool_message(self, tool_call_id, content):
        """Add a function message with its name and result."""
        # Serialize the content as JSON string
        serialized_content = json.dumps(content) if isinstance(content, dict) else content
        self.messages.append({
            "role": "tool",
            "tool_call_id": tool_call_id,
            "content": serialized_content  # Use serialized content
        })



    def get_messages(self):
        """Retrieve the current conversation history."""
        return self.messages

    def reset(self):
        """Keep the first message and delete everything else."""
        if self.messages:
            self.messages = [self.messages[0]]
        else:
            self.messages = []