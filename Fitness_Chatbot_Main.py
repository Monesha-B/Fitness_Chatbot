from dotenv import load_dotenv
import os
import streamlit as st
import openai

# Load environment variables from .env file (for local dev)
load_dotenv()

# Set the API key for OpenAI from Streamlit secrets or .env
api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OpenAI API key not found. Set it in .env or Streamlit secrets.")
openai.api_key = api_key

# Optional: Filter to allow only fitness-related prompts
def is_fitness_related(text):
    fitness_keywords = [
        "fitness", "workout", "exercise", "training", "gym", "muscle",
        "cardio", "weight loss", "nutrition", "meal", "calories", "protein",
        "recovery", "stretch", "routine", "diet", "macros"
    ]
    return any(keyword in text.lower() for keyword in fitness_keywords)

# Chat logic with system instruction to focus only on fitness topics
def chat_with_gpt(prompt, chat_history):
    messages = [
        {"role": "system", "content": (
            "You are a helpful and expert fitness assistant. "
            "You only answer questions related to fitness, workouts, exercise routines, and nutrition that supports fitness goals. "
            "If a user asks about unrelated topics, politely let them know you're only here to help with fitness guidance."
        )}
    ]
    messages.extend(chat_history)
    messages.append({"role": "user", "content": prompt})

    response = openai.ChatCompletion.create(
        model="gpt-4",  # Use "gpt-3.5-turbo" if you don't have GPT-4 access
        messages=messages,
        temperature=0.7
    )

    reply = response.choices[0].message["content"]
    chat_history.append({"role": "user", "content": prompt})
    chat_history.append({"role": "assistant", "content": reply})

    return reply, chat_history

# === Command-line test (optional for local dev) ===
if __name__ == "__main__":
    chat_history = []
    print("🤖 Welcome to your Fitness Chatbot! Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("🤖 Chatbot: Goodbye! Stay healthy 💪")
            break

        if is_fitness_related(user_input):
            reply, chat_history = chat_with_gpt(user_input, chat_history)
            print(f"🤖 Chatbot: {reply}\n")
        else:
            print("🤖 Chatbot: I'm here to help only with fitness and nutrition topics. Try asking about workouts, diet plans, or exercise advice! 💪\n")
