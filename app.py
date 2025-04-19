import streamlit as st
import json
import os
from datetime import datetime
from Fitness_Chatbot_Main import chat_with_gpt

st.set_page_config(page_title="Interactive Fitness Dashboard", page_icon="💪")
st.title("💬 CoverFitness AI Chatbot + Planner")

# Collect basic user info
st.sidebar.header("👤 Your Info")
age = st.sidebar.number_input("Age", min_value=12, max_value=100, step=1)
height = st.sidebar.number_input("Height (cm)", min_value=100, max_value=250)
weight = st.sidebar.number_input("Weight (kg)", min_value=30, max_value=200)
gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])
goal = st.sidebar.selectbox("Fitness Goal", ["Lose Fat", "Build Muscle", "Maintain"])

# Load chat history if it exists
if "chat_history" not in st.session_state:
    if os.path.exists("chat_history.json"):
        with open("chat_history.json", "r") as f:
            st.session_state.chat_history = json.load(f)
    else:
        st.session_state.chat_history = []

# Generate plan
if all([age, height, weight]):
    if st.sidebar.button("Generate Fitness Plan"):
        user_profile = {
            "age": age, "height": height, "weight": weight,
            "gender": gender, "goal": goal
        }
        intro = f"User profile: {user_profile}. Suggest a weekly meal and workout plan."
        response, st.session_state.chat_history = chat_with_gpt(intro, [])
        st.session_state.generated_plan = response

# Show generated plan
if "generated_plan" in st.session_state:
    st.markdown("### 🧾 Suggested Plan")
    st.write(st.session_state.generated_plan)

# Meals Table
st.markdown("### 🍽️ Edit Your Meal Plan")
default_meals = {
    "Day": ["Monday", "Tuesday", "Wednesday"],
    "Breakfast": ["Smoothie", "Oats", "Tofu Scramble"],
    "Lunch": ["Quinoa Bowl", "Lentil Soup", "Chickpea Salad"],
    "Dinner": ["Zucchini Noodles", "Veggie Stir-fry", "Stuffed Peppers"]
}
meal_df = st.data_editor(default_meals, num_rows="dynamic", key="meals_editor")

# Workouts Table
st.markdown("### 🏋️ Edit Your Workout Plan")
default_workouts = {
    "Day": ["Monday", "Tuesday", "Wednesday"],
    "Workout 1": ["Swimming (30m)", "HIIT (20m)", "Jogging (30m)"],
    "Workout 2": ["Yoga (30m)", "Core (20m)", "Stretching (15m)"]
}
workout_df = st.data_editor(default_workouts, num_rows="dynamic", key="workout_editor")

# Save plans to file
if st.button("💾 Save Plans"):
    plans = {
        "user_info": {"age": age, "height": height, "weight": weight, "goal": goal},
        "meals": meal_df,
        "workouts": workout_df
    }
    with open("saved_plan.json", "w") as f:
        json.dump(plans, f, indent=2)
    st.success("Plans saved successfully!")

# Chatbot Section
st.markdown("## 🤖 Chat With FitBuddy")
user_input = st.text_input("Ask something about your fitness, meals, or workouts:")

if user_input:
    reply, st.session_state.chat_history = chat_with_gpt(user_input, st.session_state.chat_history)
    st.markdown(f"**🤖 FitBuddy:** {reply}")

# Display chat history
if st.session_state.chat_history:
    st.markdown("### 💭 Chat History")
    for entry in st.session_state.chat_history:
        role = "🧑 You" if entry["role"] == "user" else "🤖 FitBuddy"
        st.markdown(f"**{role}:** {entry['content']}")

# Save chat history button
if st.button("💾 Save Chat History"):
    with open("chat_history.json", "w") as f:
        json.dump(st.session_state.chat_history, f, indent=2)
    st.success("Chat history saved to chat_history.json!")
