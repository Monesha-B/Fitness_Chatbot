import os
import openai
from dotenv import load_dotenv

import os
os.system("pip install openai")
import openai


# Load environment variables from .env file (useful for local dev)
load_dotenv()

# Get your OpenAI API key from environment
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OpenAI API key not found. Set it in .env or Streamlit secrets.")

# Set the API key for OpenAI
openai.api_key = api_key

def chat_with_gpt(prompt, chat_history):
    messages = [{"role": "system", "content": "You are a helpful fitness assistant."}]
    messages.extend(chat_history)
    messages.append({"role": "user", "content": prompt})

    response = openai.ChatCompletion.create(
        model="gpt-4",  # You can change this to "gpt-3.5-turbo" if needed
        messages=messages,
        temperature=0.7
    )

    reply = response.choices[0].message["content"]
    chat_history.append({"role": "user", "content": prompt})
    chat_history.append({"role": "assistant", "content": reply})

    return reply, chat_history

# === Main loop (for command-line testing only) ===
if __name__ == "__main__":
    chat_history = []
    print("🤖 Welcome to your Fitness Chatbot! Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("🤖 Chatbot: Goodbye! Stay healthy 💪")
            break

        reply, chat_history = chat_with_gpt(user_input, chat_history)
        print(f"🤖 Chatbot: {reply}\n")
