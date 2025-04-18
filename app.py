import streamlit as st
from Fitness_Chatbot_Main import chat_with_gpt

# Set page config
st.set_page_config(page_title="CoverFitness Chatbot", page_icon="💪")
st.title("💬 CoverFitness AI Chatbot")

# Set dark mode theme
def set_dark_theme():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #121212;
            color: #e0e0e0;
        }
        .css-1cpxqw2, .css-ffhzg2, .css-1d391kg {
            background-color: #1f1f1f !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
set_dark_theme()

# Set background image
def set_background_image():
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://images.unsplash.com/photo-1605296867304-46d5465a13f1?auto=format&fit=crop&w=1350&q=80");
            background-size: cover;
            background-attachment: fixed;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
set_background_image()

# Add FitBuddy logo
st.image("https://img.icons8.com/external-flat-juicy-fish/200/000000/exercise-flat-juicy-fish.png", width=100)

# Sidebar with fitness tips
with st.sidebar:
    st.markdown("### 💡 FitBuddy Tips")
    st.markdown("- Stay hydrated 🥤")
    st.markdown("- Consistency beats intensity 💯")
    st.markdown("- Don't skip rest days 💤")
    st.markdown("---")
    st.markdown("👤 Made by Monesha")

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input
user_input = st.text_input("Ask me anything about fitness:")

if user_input:
    reply, st.session_state.chat_history = chat_with_gpt(user_input, st.session_state.chat_history)
    st.write("🤖:", reply)

# Display chat history
if st.session_state.chat_history:
    st.markdown("### Chat History")
    for entry in st.session_state.chat_history:
        if entry["role"] == "user":
            st.markdown(f"**You:** {entry['content']}")
        elif entry["role"] == "assistant":
            st.markdown(f"**AI:** {entry['content']}")
