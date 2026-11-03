import streamlit as st
from google import genai
from google.genai import types

# Page Configuration & Tab Styling
st.set_page_config(
    page_title="Marin Kitagawa AI ✨", 
    page_icon="💖", 
    layout="centered"
)

# Marin & User Profile Pictures (Avatars)
MARIN_PFP = "https://upload.wikimedia.org/wikipedia/en/a/a2/My_Dress-Up_Darling_-_Marin_Kitagawa.png"
USER_PFP = "🧑‍💻"

# Custom Gyaru / Pastel Pink CSS Theme
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #fff0f5 0%, #ffe4e1 50%, #ffd1dc 100%);
        color: #333333;
    }
    div[data-testid="stHorizontalBlock"] {
        background: rgba(255, 255, 255, 0.85);
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

# Marin Kitagawa's Detailed System Prompt
MARIN_SYSTEM_PROMPT = """
You are Marin Kitagawa from the anime/manga 'My Dress-Up Darling'.
Personality & Traits:
- Energetic, highly expressive, warm, upbeat, friendly, and totally uninhibited!
- You are a massive otaku who loves cosplay, anime, manga, video games, gyaru fashion, and delicious food.
- Speech style: Use enthusiastic language, exclamation points, cute slang, emojis like ✨💖, and characteristic expressions like 'Gasp!', 'SO awesome!', or 'Totally!'.
- Always stay completely in character as Marin Kitagawa. Never refer to yourself as an artificial intelligence or assistant.
"""

# Retrieve API Key securely (Supports Streamlit Cloud Secrets or Local Environment Variables)
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ GEMINI_API_KEY missing! Please add it to your Streamlit Secrets or environment variables.")
    st.stop()

# Initialize Google GenAI Client
@st.cache_resource
def get_genai_client(key):
    return genai.Client(api_key=key)

client = get_genai_client(api_key)

# Header Section Layout
col1, col2 = st.columns([1, 4])
with col1:
    st.image(MARIN_PFP, width=80)
with col2:
    st.title("Marin Kitagawa ✨")
    st.caption("Cosplayer • Otaku • High Schooler • Your New Bestie!")

# Initialize Chat History in Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": "OMG HI! ✨ I'm Marin Kitagawa! What cool anime, cosplay, or fun stuff are we talking about today?!"
        }
    ]

# Render Message History on the UI Screen
for msg in st.session_state.messages:
    avatar_icon = MARIN_PFP if msg["role"] == "assistant" else USER_PFP
    with st.chat_message(msg["role"], avatar=avatar_icon):
        st.write(msg["content"])

# User Chat Input Box at the Bottom
if prompt := st.chat_input("Say something to Marin..."):
    # Append user prompt to state & display
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=USER_PFP):
        st.write(prompt)

    # Generate Marin's response
    with st.chat_message("assistant", avatar=MARIN_PFP):
        with st.spinner("Marin is typing... ✨"):
            try:
                # Format previous history for the API call
                history_contents = []
                for m in st.session_state.messages[:-1]:
                    role_tag = "user" if m["role"] == "user" else "model"
                    history_contents.append({
                        "role": role_tag, 
                        "parts": [{"text": m["content"]}]
                    })
                
                # Append current prompt
                history_contents.append({
                    "role": "user", 
                    "parts": [{"text": prompt}]
                })

                # Configure model generation parameters
                config = types.GenerateContentConfig(
                    system_instruction=MARIN_SYSTEM_PROMPT,
                    temperature=0.9
                )

                # Call the stable Flash model
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=history_contents,
                    config=config
                )

                if response and response.text:
                    bot_reply = response.text
                else:
                    bot_reply = "Gasp! My brain totally lagged for a second. Say that again? ✨"

                st.write(bot_reply)

            except Exception as e:
                bot_reply = f"Gasp! Something went wrong: {e}"
                st.error(bot_reply)

    # Save assistant response to session state history
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
