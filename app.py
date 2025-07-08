import streamlit as st
import random
from googlesearch import search

st.set_page_config(page_title="Cat CPT", layout="wide")

st.markdown("""
    <style>
        .message-box {
            background-color: #2c2c2c;
            color: black;
            padding: 1rem;
            border-radius: 12px;
            margin: 0.5rem 0;
            max-width: 70%;
        }
        .user { align-self: flex-end; background-color: #3a3a3a; }
        .bot { align-self: flex-start; background-color: #2c2c2c; }
        .chat-container {
            display: flex;
            flex-direction: column;
            height: 70vh;
            overflow-y: auto;
            padding: 1rem;
        }
        .input-area {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            padding: 1rem;
            background-color: #1e1e1e;
            display: flex;
            gap: 0.5rem;
        }
        input[type="file"] {
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 style="color:white;">Cat CPT</h1>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

def generate_bot_reply(message):
    if "merhaba" in message.lower():
        return "Merhaba! Size nasıl yardımcı olabilirim?"
    elif "teşekkür" in message.lower():
        return "Rica ederim! Her zaman buradayım."
    elif "mutluluk" in message.lower() and "zengin" in message.lower():
        return "Bence zenginlikle mutluluk garanti edilmez. Manevi tatmin daha önemlidir."
    elif "nedir" in message.lower() or "kimdir" in message.lower():
        try:
            result = next(search(message, num_results=1))
            return f"Bu konuda bulduğum kaynak: {result}"
        except:
            return "Araştırma yaparken bir sorun oluştu."
    else:
        return "Bu konuda kendi fikrimle yardımcı olayım: Hayata farklı açılardan bakmak iyidir. 🤔"

# Gösterilen Sohbet
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for i, (user_msg, bot_msg) in enumerate(st.session_state.messages, 1):
    st.markdown(f'<div class="message-box user"><strong>User:</strong> {user_msg}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="message-box bot"><strong>Cat CPT:</strong> {bot_msg}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Giriş alanı ve dosya/fotoğraf yükleme
st.markdown('<div class="input-area">', unsafe_allow_html=True)
user_input = st.text_input("Mesajınızı yazın", "", key="input")
col1, col2, col3 = st.columns([5, 1, 1])
with col2:
    st.file_uploader("Fotoğraf", type=["png", "jpg", "jpeg"], label_visibility="collapsed", key="photo")
with col3:
    st.file_uploader("Dosya", label_visibility="collapsed", key="file")
st.markdown('</div>', unsafe_allow_html=True)

# Mesaj gönderildiğinde
if user_input:
    response = generate_bot_reply(user_input)
    st.session_state.messages.append((user_input, response))
    st.experimental_rerun()
