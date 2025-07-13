import streamlit as st import time from googlesearch import search from PIL import Image import pytesseract import os

def get_ai_response(text): text_lower = text.lower()

if any(word in text_lower for word in ["selam", "merhaba", "naber"]):
    return "Merhaba! Sana nasıl yardımcı olabilirim?"
elif "teşekkür" in text_lower:
    return "Rica ederim! Başka bir sorunuz varsa yardımcı olmaktan memnuniyet duyarım."

elif "neden", "sence", "nasıl olur", "yorumla" in text_lower or text_lower.endswith("?"):
    return f"Bu konuda kendi düşünceme göre şöyle diyebilirim: {text} hakkında birçok farklı görüş olabilir."

else:
    try:
        query = text
        results = list(search(query, num_results=1))
        if results:
            return f"İnternetten bulduğum bilgiye göre: {results[0]}"
        else:
            return "Bu konuda bir bilgi bulamadım."
    except Exception as e:
        return f"Araştırma sırasında bir hata oluştu: {str(e)}"

def analyze_file(uploaded_file): if uploaded_file.type.startswith("image"): image = Image.open(uploaded_file) text = pytesseract.image_to_string(image) return f"Görselde okunan metin: {text.strip()}" elif uploaded_file.type == "text/plain": content = uploaded_file.read().decode("utf-8") return f"Dosya içeriği: {content.strip()}" else: return "Yalnızca metin ve görsel dosyaları analiz edebilirim."

Sayfa başlığı ve yapı

st.markdown(""" <style> .main-container { display: flex; flex-direction: row; } .sidebar { width: 200px; background-color: #111; color: white; padding: 20px; } .chat-area { flex: 1; background-color: black; padding: 20px; color: white; } .chat-bubble { background-color: #222; border-radius: 10px; padding: 10px; margin-bottom: 10px; } .message-input { position: fixed; bottom: 0; left: 200px; right: 0; background-color: #111; padding: 10px; } </style> """, unsafe_allow_html=True)

st.markdown(""" <div class="main-container"> <div class="sidebar"> <input type="text" placeholder="konu arama" style="width:100%; margin-bottom:10px"> <p>🗨 konular ↓</p> <p>1.konu</p> <p>2.konu</p> <p>3.konu</p> <p>4.konu</p> <p>5.konu</p> <p>6.konu</p> </div> <div class="chat-area"> <h3>🐱CAT CPT=KEDİ YAPAY ZEKA</h3> """, unsafe_allow_html=True)

if "chat_history" not in st.session_state: st.session_state.chat_history = []

for i, (q, a) in enumerate(st.session_state.chat_history): st.markdown(f"<div class='chat-bubble'> {i+1}.soru: {q} </div>", unsafe_allow_html=True) st.markdown(f"<div class='chat-bubble'> {i+1}.cevap: {a} </div>", unsafe_allow_html=True)

st.markdown(""" </div> </div> """, unsafe_allow_html=True)

with st.container(): st.markdown("<div class='message-input'>", unsafe_allow_html=True) col1, col2, col3 = st.columns([7, 1, 1]) with col1: user_input = st.text_input("", placeholder="Herhangi bir şey sor", label_visibility="collapsed") with col2: uploaded_file = st.file_uploader("", type=["png", "jpg", "jpeg", "txt"], label_visibility="collapsed") with col3: send = st.button("Gönder") st.markdown("</div>", unsafe_allow_html=True)

if send: if uploaded_file: result = analyze_file(uploaded_file) st.session_state.chat_history.append((f"[Dosya: {uploaded_file.name}]", result)) elif user_input: response = get_ai_response(user_input) st.session_state.chat_history.append((user_input, response))

