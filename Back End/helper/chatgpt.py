import os
from openai import OpenAI
import json
from flask import Flask, jsonify, request

# Initialize OpenAI client
# Load API key from a text file
with open('apikeys.txt', 'r') as file:
    api_key = file.read().strip()

client = OpenAI(
    api_key='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'
)

# Function to send a chat with given prompt and context
def send_chat(prompt, context, model="gpt-4o-mini", schema=""):
    """
    Sends a chat message to OpenAI GPT-4 model.
    :param prompt: The user's message.
    :param context: Additional context for the conversation.
    :param model: The model to use for chat completion (default is "gpt-4o-mini").
    :param schema: Optional schema for the response format.
    :return: GPT response as a string or a JSON object, based on the schema.
    """
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ]
    if context:
        messages.insert(1, {"role": "system", "content": context})
    
    # Define response format based on whether a schema is provided
    if not schema:
        response_format = {"type": "text"}
    else:
        response_format = {"type": "json_schema", "json_schema": schema}

    try:
        chat_completion = client.chat.completions.create(
            messages=messages,
            model=model,
            response_format=response_format
        )
    except Exception as e:
        raise RuntimeError(f"Error during chat completion: {str(e)}")

    if response_format["type"] == "object":
        return chat_completion
    else:
        # Access the message content safely
        content = chat_completion.choices[0].message.content
        return content




# Function to generate an email using GPT
def generate_gpt_email(to, to_name, from_, from_name, context):
    """
    Generates an email using GPT-4.
    :param to: The recipient of the email.
    :param from_: The sender of the email.
    :param context: Context or key details for the email content.
    :return: Generated email as a string.
    """
    prompt = f"Generate a professional email to {to_name} from {from_name}. Context: {context}. DO NOT INCLUDE ANYTHING BUT EMAIL BODY. DO NOT INCLUDE THE SUBJECT INSIDE THIS EMAIL BODY."
    return send_chat(prompt, None)

# Function to generate a subject line from a body
def generate_subject_line(body):
    """
    Generates a subject line for an email based on its body content.
    :param body: The content of the email body.
    :return: Generated subject line as a string.
    """
    prompt = f"Create a concise and professional subject line for this email body: {body}. DO NOT INCLUDE THE 'SUBJECT:' TOPIC IN THE SUBJECT LINE."
    return send_chat(prompt, None)




