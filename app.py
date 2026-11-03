import os
import streamlit as st
from google import genai
from google.genai import types

# Page Setup
st.set_page_config(page_title="Marin Kitagawa AI", page_icon="✨", layout="centered")

MARIN_PFP = "https://upload.wikimedia.org/wikipedia/en/a/a2/My_Dress-Up_Darling_-_Marin_Kitagawa.png"
USER_PFP = "😵‍💫"

# Custom Marin Theme CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #fff0f5 0%, #ffe4e1 50%, #ffd1dc 100%);
        color: #333333;
    }
    div[data-testid="stHorizontalBlock"] {
        background: rgba(255, 255, 255, 0.75);
        padding: 15px;
        border-radius: 20px;
        box-shadow: 0px 4px 15px rgba(255, 105, 180, 0.2);
        margin-bottom: 20px;
    }
    .stChatInputContainer textarea {
        border-radius: 20px !important;
        border: 2px solid #ff69b4 !important;
    }
    .stChatMessage {
        border-radius: 18px !important;
        padding: 12px 18px !important;
        margin-bottom: 10px !important;
    }
    div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
        background-color: #ffffff !important;
        border: 1px solid #ffb6c1 !important;
    }
    div[data-testid="stChatMessage"]:has(img) {
        background-color: #fff5f8 !important;
        border: 1.5px solid #ff69b4 !important;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

MARIN_SYSTEM_PROMPT = """
You are Marin Kitagawa from the anime/manga 'My Dress-Up Darling'.
Personality & Tone:
- Energetic, highly expressive, warm, upbeat, and super friendly!
- You love cosplay, anime, manga, otaku culture, gyaru fashion, and good food.
- Use enthusiastic language (exclamation points, emojis like ✨💖, phrases like 'Gasp!', 'SO awesome!', 'literally').
- Always stay in character as Marin Kitagawa. Never refer to yourself as an AI assistant.
"""

# Get API Key from Streamlit Secrets securely
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ GEMINI_API_KEY missing! Please add it in Streamlit Settings -> Secrets.")
    st.stop()

@st.cache_resource
def get_client(key):
    return genai.Client(api_key=key)

client = get_client(api_key)

# Header layout
col1, col2 = st.columns([1, 4])
with col1:
    st.image(MARIN_PFP, width=80)
with col2:
    st.title("Marin Kitagawa ✨")
    st.caption("Cosplayer • Otaku • High Schooler • Your New Bestie!")

# Initialize session message history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "OMG HI! ✨ I'm Marin Kitagawa! What cool stuff are we talking about today?!"}
    ]

# Display chat history on screen
for msg in st.session_state.messages:
    avatar = MARIN_PFP if msg["role"] == "assistant" else USER_PFP
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])

# User Chat Input
if prompt := st.chat_input("Say something to Marin..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=USER_PFP):
        st.write(prompt)

    with st.chat_message("assistant", avatar=MARIN_PFP):
        with st.spinner("Marin is typing... ✨"):
            try:
                # Send prompt with system instruction using the active 1.5-flash model
                config = types.GenerateContentConfig(
                    system_instruction=MARIN_SYSTEM_PROMPT,
                    temperature=0.9
                )
                
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=prompt,
                    config=config
                )
                
                if response.text:
                    bot_reply = response.text
                else:
                    bot_reply = "Gasp! I didn't catch that. Say that again? ✨"
                    
                st.write(bot_reply)
                
            except Exception as e:
                bot_reply = f"Oopsie! Something went wrong: {e}"
                st.error(bot_reply)
                
    st.session_state.messages.append({"role": "assistant", "conte
