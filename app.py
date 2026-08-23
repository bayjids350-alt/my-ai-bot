import streamlit as st
import google.generativeai as genai

# Streamlit Page Config
st.set_page_config(page_title="Multi-Purpose AI Bot", page_icon="🤖", layout="centered")

# API Key Check
if "GEMINI_API_KEY" not in st.secrets:
    st.error("GEMINI_API_KEY not found in Secrets! Please add your API key in Streamlit Settings.")
    st.stop()

# Configure Gemini API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Sidebar for Mode Selection
st.sidebar.title("⚙️ Select Mode")
bot_mode = st.sidebar.radio(
    "Choose your mode:",
    ("General Chatbot", "Content Engine")
)

# System Prompt Assignment Based on Selection
if bot_mode == "Content Engine":
    st.title("🎬 AI Content & Script Engine")
    st.caption("All-in-one assistant for YouTube scripts, captions, titles, and SEO tags.")
    system_instruction = """
    You are an expert AI Content Creator and Scriptwriter. 
    Write engaging YouTube/Shorts scripts, high-CTR titles, SEO tags, and catchy social media captions in English.
    Organize responses clearly with bold section titles and bullet points.
    """
else:
    st.title("🤖 General AI Assistant")
    st.caption("Your assistant for general questions, chats, and guidance.")
    system_instruction = "You are a helpful, polite, and friendly AI assistant. Always respond in English clearly."

# Initialize Chat Session
if "current_mode" not in st.session_state or st.session_state.current_mode != bot_mode:
    st.session_state.current_mode = bot_mode
    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=system_instruction
        )
        st.session_state.chat_session = model.start_chat(history=[])
    except Exception as e:
        st.error(f"Error initializing model: {e}")

# Display Chat History
if "chat_session" in st.session_state:
    for message in st.session_state.chat_session.history:
        role = "user" if message.role == "user" else "assistant"
        with st.chat_message(role):
            st.markdown(message.parts[0].text)

# User Input Box
if user_prompt := st.chat_input("Type your message here..."):
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        if "chat_session" in st.session_state:
            response = st.session_state.chat_session.send_message(user_prompt)
            st.markdown(response.text)
