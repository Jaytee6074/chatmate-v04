import streamlit as st
import random
import datetime

st.set_page_config(page_title="ChatMate v0.4", page_icon="🤖")

# --- Memory and State Initialization ---
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

# --- Utility Functions ---
def analyze_input(text):
    text = text.lower()
    if any(word in text for word in ["interview", "resume", "job"]):
        return "interview"
    elif any(word in text for word in ["lose weight", "diet", "exercise", "fat", "gym"]):
        return "health"
    elif any(word in text for word in ["happy", "excited", "great", "joy", "awesome"]):
        return "joy"
    elif any(word in text for word in ["sad", "depressed", "tired", "down", "cry"]):
        return "sadness"
    return "general"

def get_response(intent, user_name):
    responses = {
        "interview": [
            f"{user_name}, that's amazing news! 🎉 Want to go over a few interview tips together?",
            f"You've got this, {user_name}. Let’s prep you with confidence!"
        ],
        "health": [
            f"Losing weight starts with small steps. Want to talk exercise or nutrition, {user_name}?",
            f"Hydration, movement, sleep—let’s get you feeling good from the inside out. 💪"
        ],
        "joy": [
            f"YES! Keep that energy going, {user_name}. What’s making today so great?",
            f"That’s the spirit! 🙌 Got anything fun planned?"
        ],
        "sadness": [
            f"Sounds like it’s been a heavy day, {user_name}. I’m right here with you. 🫂",
            f"Let’s take a breath together, {user_name}. Want to talk more about what’s on your heart?"
        ],
        "general": [
            f"I’m here to listen, {user_name}. Tell me anything you like.",
            f"Thanks for sharing that, {user_name}. I’m always listening."
        ]
    }
    return random.choice(responses.get(intent, responses["general"]))

# --- UI Layout ---
st.title("🤖 ChatMate v0.4")

if not st.session_state.user_name:
    st.subheader("What’s your name?")
    name_input = st.text_input("Enter your name:")
    if name_input:
        st.session_state.user_name = name_input
        st.rerun()

else:
    st.success(f"Hey {st.session_state.user_name}, I’m your ChatMate. Let’s talk!")

    st.write("**How are you feeling today?**")
    user_input = st.text_input("Tell me something or ask a question:")

    if user_input:
        user_name = st.session_state.user_name
        intent = analyze_input(user_input)
        response = get_response(intent, user_name)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.chat_log.append((timestamp, user_input, response))

    if st.session_state.chat_log:
        st.subheader("📜 Conversation Log")
        for timestamp, user, bot in reversed(st.session_state.chat_log):
            st.markdown(f"**[{timestamp}] {st.session_state.user_name}:** {user}")
            st.markdown(f"**ChatMate:** {bot}")
