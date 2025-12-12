import streamlit as st
from groq import Groq

# ----------------------------
# API KEY FROM STREAMLIT SECRETS
# ----------------------------
API_KEY = st.secrets["GROQ_API_KEY"]

client = Groq(api_key=API_KEY)
MODEL_NAME = "llama-3.1-8b-instant"

# ----------------------------
# STREAMLIT PAGE SETUP
# ----------------------------
st.set_page_config(page_title="Groq Chatbot", layout="centered")
st.title("🤖 Groq Chatbot (Streamlit Version)")

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

# ----------------------------
# CHAT FUNCTION
# ----------------------------
def get_response(user_message):
    messages = []
    for human, assistant in st.session_state.history:
        messages.append({"role": "user", "content": human})
        messages.append({"role": "assistant", "content": assistant})
    messages.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.7,
            max_tokens=512,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[ERROR contacting Groq] {e}"

# ----------------------------
# DISPLAY CHAT HISTORY
# ----------------------------
for human, assistant in st.session_state.history:
    with st.chat_message("user"):
        st.write(human)
    with st.chat_message("assistant"):
        st.write(assistant)

# ----------------------------
# USER INPUT
# ----------------------------
user_msg = st.chat_input("Type your message...")

if user_msg:
    reply = get_response(user_msg)
    st.session_state.history.append([user_msg, reply])
    st.experimental_rerun()

# ----------------------------
# CLEAR BUTTON
# ----------------------------
if st.button("🗑️ Clear Chat"):
    st.session_state.history = []
    st.experimental_rerun()
