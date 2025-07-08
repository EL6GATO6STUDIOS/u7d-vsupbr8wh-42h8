import streamlit as st
from googlesearch import search
from bs4 import BeautifulSoup
import requests
import random
from PIL import Image
from PyPDF2 import PdfReader

st.set_page_config(page_title="Cat CPT 😺", layout="centered")
st.markdown("<h1 style='text-align: center;'>Cat CPT 😺</h1>", unsafe_allow_html=True)

# Geçmişi sakla
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Stil ayarları
def style_user(text):
    return f"""<div style="background-color:#DCF8C6; padding:10px; border-radius:10px; margin:10px 0;"><b>Sen:</b><br>{text}</div>"""

def style_bot(text):
    return f"""<div style="background-color:#E6E6EA; padding:10px; border-radius:10px; margin:10px 0;"><b>Cat CPT:</b><br>{text}</div>"""

# Fikir üretici
def generate_opinion_response(text):
    fikirler = [
        f"Bence {text} oldukça önemli bir konu. Kişiden kişiye değişebilir.",
        f"{text} bana kalırsa dikkatle değerlendirilmesi gereken bir durum.",
        f"Açıkçası {text} hakkında net bir fikrim var: oldukça karmaşık.",
        f"{text} konusunda herkes aynı fikirde olmayabilir, ama bence ilginç bir mesele."
    ]
    return random.choice(fikirler)

# Soru analizi
def is_gundelik(text):
    return any(x in text.lower() for x in ["selam", "merhaba", "naber", "nasılsın", "teşekkür"])

def is_analiz(text):
    return any(x in text.lower() for x in ["sence", "yorumla", "analiz", "düşünüyorsun", "bakış açın", "karakter"])

# Google araştırması
def google_arastir(query):
    try:
        results = list(search(query, num_results=1))
        if results:
            url = results[0]
            res = requests.get(url, timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")
            for p in soup.find_all("p"):
                if len(p.text.strip()) > 60:
                    return p.text.strip()
        return "Uygun bir bilgi bulunamadı."
    except Exception as e:
        return f"Araştırma hatası: {str(e)}"

# Girdi alanı
text = st.text_input("Mesajınızı yazın...")

# Yükleme alanı
uploaded = st.file_uploader("Dosya yükleyin (.pdf, .txt, .jpg, .png)", type=["pdf", "txt", "jpg", "jpeg", "png"])
if uploaded:
    st.subheader("Yüklenen Dosya:")
    if "pdf" in uploaded.type:
        reader = PdfReader(uploaded)
        content = "".join([p.extract_text() for p in reader.pages if p.extract_text()])
        st.text_area("PDF İçeriği", content)
    elif "text" in uploaded.type:
        content = uploaded.read().decode("utf-8")
        st.text_area("Metin Dosyası", content)
    elif "image" in uploaded.type:
        img = Image.open(uploaded)
        st.image(img, caption="Görsel", use_column_width=True)

# Girdi varsa yanıt üret
if text:
    if is_gundelik(text):
        if "selam" in text.lower() or "merhaba" in text.lower():
            response = "Merhaba! 😊 Size nasıl yardımcı olabilirim?"
        elif "naber" in text.lower() or "nasılsın" in text.lower():
            response = "İyiyim, sen nasılsın?"
        elif "teşekkür" in text.lower():
            response = "Rica ederim! Her zaman buradayım."
        else:
            response = "Anlayabildiğim bir gündelik ifade algıladım."
    elif is_analiz(text):
        response = generate_opinion_response(text)
    else:
        response = google_arastir(text)

    # Sohbet geçmişine ekle
    st.session_state.chat_history.append((text, response))

# Geçmişi sırayla göster (ChatGPT benzeri)
if st.session_state.chat_history:
    for q, a in st.session_state.chat_history:
        st.markdown(style_user(q), unsafe_allow_html=True)
        st.markdown(style_bot(a), unsafe_allow_html=True)
