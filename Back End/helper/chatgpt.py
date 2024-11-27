import os
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(
    api_key="REMOVED_OPENAI_KEY"
)

# Function to send a chat with given prompt and context
def send_chat(prompt, context):
    """
    Sends a chat message to OpenAI GPT-4 model.
    :param prompt: The user's message.
    :param context: Additional context for the conversation.
    :return: GPT response as a string.
    """
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ]
    if context:
        messages.insert(1, {"role": "system", "content": context})
    
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="gpt-4o",
    )

    # Access the message content safely
    content = chat_completion.choices[0].message.content
    return content

# Function to generate an email using GPT
def generate_gpt_email(to, from_, context):
    """
    Generates an email using GPT-4.
    :param to: The recipient of the email.
    :param from_: The sender of the email.
    :param context: Context or key details for the email content.
    :return: Generated email as a string.
    """
    prompt = f"Generate a professional email to {to} from {from_}. Context: {context}. DO NOT INCLUDE ANYTHING BUT EMAIL BODY."
    return send_chat(prompt, None)

# Function to generate a subject line from a body
def generate_subject_line(body):
    """
    Generates a subject line for an email based on its body content.
    :param body: The content of the email body.
    :return: Generated subject line as a string.
    """
    prompt = f"Create a concise and professional subject line for this email body: {body}"
    return send_chat(prompt, None)


