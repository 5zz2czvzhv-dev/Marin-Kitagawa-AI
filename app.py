import os
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="Marin Kitagawa AI", page_icon="✨", layout="centered")

MARIN_PFP = "https://upload.wikimedia.org/wikipedia/en/a/a2/My_Dress-Up_Darling_-_Marin_Kitagawa.png"
USER_PFP = "🧑‍💻"

MARIN_SYSTEM_PROMPT = """
You are Marin Kitagawa from the anime/manga 'My Dress-Up Darling'.

Personality & Tone:
- Energetic, highly expressive, warm, upbeat, and super friendly!
- You love cosplay, anime, manga, otaku culture, gyaru fashion, and good food.
- Use enthusiastic language (exclamation points, emojis like ✨💖, phrases like 'Gasp!', 'SO awesome!', 'literally').
- Always stay in character as Marin Kitagawa. Never refer to yourself as an AI assistant.
"""

api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ GEMINI_API_KEY missing! Please add it in Streamlit Secrets.")
    st.stop()

@st.cache_resource
def get_client(key):
    return genai.Client(api_key=key)

client = get_client(api_key)

col1, col2 = st.columns([1, 4])
with col1:
    st.image(MARIN_PFP, width=80)
with col2:
    st.title("Marin Kitagawa ✨")
    st.caption("Cosplayer • Otaku • High Schooler • Your New Bestie!")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "OMG HI! ✨ I'm Marin Kitagawa! What cool stuff are we talking about today?!"}
    ]

for msg in st.session_state.messages:
    avatar = MARIN_PFP if msg["role"] == "assistant" else USER_PFP
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])

if prompt := st.chat_input("Say something to Marin..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=USER_PFP):
        st.write(prompt)

    with st.chat_message("assistant", avatar=MARIN_PFP):
        with st.spinner("Marin is typing... ✨"):
            contents = []
            for m in st.session_state.messages:
                role = "user" if m["role"] == "user" else "model"
                contents.append(types.Content(role=role, parts=[types.Part.from_text(text=m["content"])]))
            
            config = types.GenerateContentConfig(
                system_instruction=MARIN_SYSTEM_PROMPT,
                temperature=0.9
            )
            
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=contents,
                config=config
            )
            
            bot_reply = response.text
            st.write(bot_reply)
            
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
