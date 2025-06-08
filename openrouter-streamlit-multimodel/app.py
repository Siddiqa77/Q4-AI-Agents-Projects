import streamlit as st
import requests
import os

# Load API key (first from Streamlit secrets, fallback to .env if local)
try:
    API_KEY = st.secrets["OPENROUTER_API_KEY"]
except:
    from dotenv import load_dotenv
    load_dotenv()
    API_KEY = os.getenv("OPENROUTER_API_KEY")

# Validate API key
if not API_KEY:
    st.error("🚨 Missing API Key. Please set OPENROUTER_API_KEY in your .env or Streamlit secrets.")
    st.stop()

# Model list
MODELS = {
    "LLaMA 3 (8B)": "meta-llama/llama-3-8b-instruct",
    "DeepSeek R1": "deepseek/deepseek-r1",
    "DeepSeek Chat V3": "deepseek/deepseek-chat-v3-0324",
    "Gemma 3 27B": "google/gemma-3-27b-it",
    "Mistral Small": "mistralai/devstral-small"
}

# Query OpenRouter API
def query_openrouter(model, messages):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "X-Title": "Multi-Model Chatbot"
    }
    data = {
        "model": model,
        "messages": messages,
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"❌ Error: {response.text}"

# App Config
st.set_page_config(page_title="ChatGPT-Style Chatbot", layout="centered")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    selected_model_name = st.selectbox("Choose a model:", list(MODELS.keys()))
    selected_model_id = MODELS[selected_model_name]
    dark_mode = st.checkbox("🌙 Dark Mode", value=False)
    st.markdown("---")
    st.caption("Powered by [OpenRouter](https://openrouter.ai)")

# Theme
bg_color = "#1e1e1e" if dark_mode else "#ffffff"
user_color = "#005c4b" if dark_mode else "#DCF8C6"
assistant_color = "#2c2c2c" if dark_mode else "#f1f1f1"
text_color = "white" if dark_mode else "black"

# CSS
st.markdown(f"""
    <style>
        .stChatMessage {{ color: {text_color}; }}
        body {{ background-color: {bg_color}; color: {text_color}; }}
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown(f"<h2 style='text-align: center; color:{text_color}'>🤖 Multi-Model Chatbot</h2>", unsafe_allow_html=True)

# Session
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display messages
for msg in st.session_state.chat_history:
    align = "left" if msg["role"] == "assistant" else "right"
    bubble_color = assistant_color if msg["role"] == "assistant" else user_color
    st.markdown(
        f"""
        <div style='text-align: {align}; margin: 10px 0;'>
            <div style='display: inline-block; background-color: {bubble_color}; padding: 10px 15px; border-radius: 10px; max-width: 80%; color: {text_color};'>
                {msg["content"]}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Chat Input
user_prompt = st.chat_input("Type your message here...")

if user_prompt:
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})
    with st.spinner("Thinking..."):
        reply = query_openrouter(selected_model_id, st.session_state.chat_history)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
    st.rerun()
