# Importing the required libraries
import chainlit as cl  
from litellm import acompletion  
from my_secrets import Secrets  
import os
import asyncio
import traceback
import json  

# Loads the API key and model name from secrets file
secrets = Secrets()
gemini_api_key = secrets.gemini_api_key
gemini_model = secrets.gemini_model

# This function runs when a new chat session starts
@cl.on_chat_start
async def start():
    cl.user_session.set("chat_history", [])  # Start with an empty chat history
    await cl.Message(content="Welcome to panaversity!").send()  # Greet the user

# This function runs every time the user sends a message
@cl.on_message
async def main(message: cl.Message):
    # Show a temporary "Thinking..." message while the AI prepares a response
    msg = await cl.Message(content="Thinking...").send()

    # Get the current chat history
    history = cl.user_session.get("chat_history") or []
    history.append({"role": "user", "content": message.content})  # Add the user's message to the history

    try:
        # Ask the AI model to respond using streaming (one piece at a time)
        response = await acompletion(
            model=gemini_model,
            api_key=gemini_api_key,
            messages=history,
            stream=True,
        )

        # As the AI sends chunks of its reply, show them in real time
        async for chunk in response:
            content = chunk['choices'][0]['delta'].get('content', '')
            if content:
                await msg.stream_token(content)  # Display each part as it arrives

        # Add the AI's response to the chat history
        history.append({"role": "assistant", "content": msg.content})
        cl.user_session.set("chat_history", history)  # Save updated history

    except Exception as e:
        # If something goes wrong, show an error message
        print(f"Error occurred: {e}")
        await cl.Message(content="Sorry, an error occurred.").send()

# This function runs when the chat session ends
@cl.on_chat_end
async def on_chat_end():
    # Get the full chat history
    history = cl.user_session.get("chat_history") or []
    # Save the history to a file so we can look at it later
    with open("chat_history.json", "w") as f:
        json.dump(history, f, indent=2)
        print("chat saved")  # Confirm that the history was saved