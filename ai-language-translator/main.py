import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai


# ✅ FIRST Streamlit command
st.set_page_config(page_title="🌐 AI Translator", layout="centered")

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Check if API key is loaded
if not api_key:
    st.error("❌ API key not found. Please check your .env file.")
    st.stop()

# Set Gemini key
# genai.configure(api_key=api_key)
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# Supported Languages
languages = [
    "Urdu", "French", "Spanish", "German", "Chinese", "Japanese", "Korean", "Arabic",
    "Portuguese", "Russian", "Hindi", "Bengali", "Turkish", "Italian", "Dutch", "Greek",
    "Polish", "Swedish", "Thai", "Vietnamese", "Hebrew", "Malay", "Czech", "Romanian", "Finnish"
]

# Custom CSS for a cleaner UI
st.markdown("""
    <style>
        body {
            background-color: #f4f6f9;
        }
        .main {
            background-color: #ffffff;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.05);
        }
        .stTextArea textarea {
            background-color: #f9f9f9;
        }
        .translated-text {
            padding: 1rem;
            background-color: #e8f5e9;
            border-radius: 10px;
            border: 1px solid #c8e6c9;
            margin-top: 1rem;
        }
    </style>
""", unsafe_allow_html=True)



st.markdown("<h1 style='text-align: center;'>🌍Welcome to AI Language Translator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Created by <strong>Siddiqa Badar</strong> — Instantly translate your English text to multiple global languages using Gemini AI.</p>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

with st.container():
    text = st.text_area("✏️ Enter English text to translate:", height=150)
    lang = st.selectbox("🌐 Choose target language:", languages)
    btn = st.button("🔁 Translate")

    if btn and text:
        try:
            model = genai.GenerativeModel("models/gemini-1.5-flash")
            prompt = f"Translate the following English text into {lang}:\n\n{text}"
            response = model.generate_content(prompt)

            if hasattr(response, 'text') and response.text:
                st.markdown(f"<div class='translated-text'><strong>✅ Translated to {lang}:</strong><br><br>{response.text.strip()}</div>", unsafe_allow_html=True)
            else:
                st.warning("⚠️ No translation received. Try again with different text.")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    elif btn and not text:
        st.warning("⚠️ Please enter some English text to translate.")
