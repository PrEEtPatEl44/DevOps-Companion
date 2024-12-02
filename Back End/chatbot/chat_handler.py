from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from chatbot.chatbot_functions import (
    send_email_outlook,
    fetch_emails_outlook,
    book_meeting_outlook,
    get_all_work_items_devops,
    get_all_risk_items_devops,
    get_all_users_devops,
    get_total_priority_by_user_devops,
)
from helper.chatgpt import send_chat_with_functions
from chatbot.chat_data_struc import ChatData


class ChatHandler:
    def __init__(self):
        self.chat_data = ChatData()
        self.chat_data.add_system_message(
            content="You are an intelligent assistant designed to support a project manager who utilizes Azure DevOps and Outlook. "
                    "You have access to tools that allow you to send emails, retrieve emails, schedule meetings, fetch work items, "
                    "retrieve risk items, list users, and calculate priority scores. Use these capabilities to provide comprehensive assistance "
                    "and streamline the project management process."
        )

        # Define tools as required by the new format
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "send_email",
                    "description": "Send an email using the Outlook API.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "subject": {"type": "string", "description": "The subject of the email."},
                            "body": {"type": "string", "description": "The content of the email."},
                            "to_recipients": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "A list of recipient email addresses."
                            },
                            "attachments": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Optional file paths for attachments."
                            },
                        },
                        "required": ["subject", "body", "to_recipients"],
                        "additionalProperties": False,
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "fetch_emails",
                    "description": "Retrieve emails from the user's inbox.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": [],
                        "additionalProperties": False,
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "book_meeting",
                    "description": "Book a meeting using the Outlook API.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "subject": {"type": "string", "description": "The meeting subject."},
                            "start_time": {"type": "string", "description": "Start time in ISO 8601 format."},
                            "end_time": {"type": "string", "description": "End time in ISO 8601 format."},
                            "attendees": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "A list of attendee email addresses."
                            },
                            "location": {"type": "string", "description": "The meeting location (optional)."},
                            "body": {"type": "string", "description": "The meeting agenda or details (optional)."},
                        },
                        "required": ["subject", "start_time", "end_time", "attendees"],
                        "additionalProperties": False,
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_work_items",
                    "description": "Retrieve all work items from Azure DevOps.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": [],
                        "additionalProperties": False,
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_risk_items",
                    "description": "Retrieve all risk items from Azure DevOps.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": [],
                        "additionalProperties": False,
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_users",
                    "description": "Retrieve all users from Azure DevOps.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": [],
                        "additionalProperties": False,
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_priority_scores",
                    "description": "Retrieve the total priority score for each user based on their assigned work items.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": [],
                        "additionalProperties": False,
                    },
                },
            },
        ]

        # Map function names to their implementations
        self.function_mapping = {
            "send_email": send_email_outlook,
            "fetch_emails": fetch_emails_outlook,
            "book_meeting": book_meeting_outlook,
            "get_work_items": get_all_work_items_devops,
            "get_risk_items": get_all_risk_items_devops,
            "get_users": get_all_users_devops,
            "get_priority_scores": get_total_priority_by_user_devops,
        }

    def handle_message(self, user_message, model="gpt-4o-2024-08-06"):
        """Handle user input, call tools if needed, and return a response."""
        self.chat_data.add_user_message(user_message)

        # Send chat with tools
        messages = self.chat_data.get_messages()
        response = send_chat_with_functions(messages, model=model, functions=self.tools)

        # Process tool calls
        if "tool_calls" in response:
            return self._handle_tool_calls(response["tool_calls"])

        # Handle regular assistant responses
        assistant_message = response["content"]
        self.chat_data.add_assistant_message(content=assistant_message)
        return {"messages": self.chat_data.get_messages()}

    def _handle_tool_calls(self, tool_calls):
        """Handle multiple tool calls in parallel and return the results."""
        results = []

        # Process tool calls in parallel
        with ThreadPoolExecutor() as executor:
            future_to_tool_call = {
                executor.submit(
                    self._execute_tool_call,
                    tool_call
                ): tool_call for tool_call in tool_calls
            }

            for future in as_completed(future_to_tool_call):
                tool_call = future_to_tool_call[future]
                try:
                    result = future.result()
                    results.append({
                        "tool_call_id": tool_call["id"],
                        "response": result,
                    })
                except Exception as e:
                    results.append({
                        "tool_call_id": tool_call["id"],
                        "error": str(e),
                    })

        # Submit tool call results back to the model
        for result in results:
            tool_response_message = {
                "role": "tool",
                "content": json.dumps(result.get("response", {})),
                "tool_call_id": result["tool_call_id"]
            }
            self.chat_data.add_tool_response(tool_response_message)

        # Send the updated conversation history back to the model for continuation
        messages = self.chat_data.get_messages()
        response = send_chat_with_functions(messages, model="gpt-4o-2024-08-06", functions=self.tools)
        return {"messages": response["messages"]}

    def _execute_tool_call(self, tool_call):
        """Execute a tool call and return the result."""
        function_name = tool_call["function"]["name"]
        arguments = json.loads(tool_call["function"]["arguments"])

        if function_name in self.function_mapping:
            return self.function_mapping[function_name](**arguments)
        else:
            raise ValueError(f"Function {function_name} is not implemented.")

    def get_chat_history(self):
        """Return the current chat history."""
        return self.chat_data.get_messages()