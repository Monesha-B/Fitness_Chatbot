import streamlit as st
from Fitness_Chatbot_Test import chat_with_gpt

st.set_page_config(page_title="CoverFitness Chatbot", page_icon="💪")
st.title("💬 CoverFitness AI Chatbot")

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
