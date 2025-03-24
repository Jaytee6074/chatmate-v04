import streamlit as st
import random
import datetime

st.set_page_config(page_title="ChatMate v0.5", page_icon="🤖")
# Sidebar toggle for calming background
use_bg = st.sidebar.selectbox(
    "🌄 Calming Background Image",
    ("None", "Galaxy Gradient", "Nature Blur", "Ocean Waves")
)

# Load Google Font (Quicksand)
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# Apply styles and optional background
background_css = """
    <style>
    body {
        background-color: #eae8f4;  /* base calm background */
        font-family: 'Quicksand', sans-serif;
    }
    .chat-message {
        padding: 10px 15px;
        margin: 8px;
        border-radius: 20px;
        max-width: 80%;
    }
    .user-message {
        background-color: #f0f0f0;
        color: #000;
        text-align: left;
    }
    .chatmate-message {
        background-color: #d9d9d9;
        color: #000;
        text-align: right;
        float: right;
    }
    .timestamp {
        text-align: center;
        color: #666;
        margin-top: 10px;
    }
    """

# Optional background image logic
if use_bg != "None":
    bg_urls = {
        "Galaxy Gradient": "https://images.unsplash.com/photo-1615751072473-6c3d53a6f8d3?blur=50",
        "Nature Blur": "https://images.unsplash.com/photo-1506748686214-e9df14d4d9d0?blur=50",
        "Ocean Waves": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?blur=50"
    }
    selected_url = bg_urls[use_bg]
    background_css += f"""
        body::before {{
            content: "";
            background: url('{selected_url}') no-repeat center center fixed;
            background-size: cover;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            opacity: 0.3;
            filter: blur(6px);
        }}
    """

background_css += "</style>"
st.markdown(background_css, unsafe_allow_html=True)

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
