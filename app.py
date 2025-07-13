import streamlit as st
import time
from googlesearch import search
from PIL import Image
import pytesseract
import os

st.set_page_config(layout="wide", page_title="Cat CPT")

st.markdown(
    """
    <style>
    body {background-color: #000000;}
    .message-container {
        background-color: #111111;
        color: black;
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
        max-width: 80%;
    }
    .user { text-align: left; }
    .bot { text-align: right; background-color: #222222; }
    .input-area {
        position: fixed;
        bottom: 0;
        width: 100%;
        background-color: #000000;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🐱 CAT CPT = KEDİ YAPAY ZEKA")

if "history" not in st.session_state:
    st.session_state.history = []

def generate_bot_response(user_input, uploaded_file=None):
    user_input_lower = user_input.lower()
    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            text = pytesseract.image_to_string(image)
            return f"📄 Fotoğraftan okunan yazı:\n\n{text}"
        except:
            return "⚠️ Görsel işleme başarısız oldu."
    
    if "?" in user_input:
        if any(keyword in user_input_lower for keyword in ["neden", "nasıl", "ne", "kim", "nerede", "hangi"]):
            try:
                query = user_input
                results = list(search(query, num_results=1))
                return f"🔎 Araştırmaya göre en uygun sonuç:\n{results[0]}"
            except:
                return "🌐 İnternet araştırması yapılamadı."
        else:
            return f"🧠 Benim düşünceme göre: {user_input} ilginç bir ifade. Belki daha net sorarsan daha fazla yorum yapabilirim."
    elif any(greet in user_input_lower for greet in ["merhaba", "selam", "naber", "nasılsın"]):
        return "👋 Merhaba! Sana nasıl yardımcı olabilirim?"
    else:
        return f"🤔 Bunu araştırmak yerine kendi görüşümü sunayım: {user_input} hakkında düşündüğüm şey bu: oldukça dikkat çekici bir ifade."

# Konu seçme alanı
with st.sidebar:
    st.text_input("🔍 konu arama", key="konu_ara")
    st.markdown("## 💬 konular ↓")
    for i in range(1, 7):
        st.markdown(f"{i}.konu")

# Mesaj geçmişini
