import streamlit as st
from PyPDF2 import PdfReader
from PIL import Image
from urllib.parse import quote_plus

st.set_page_config(page_title="Cat CPT", page_icon="😺")

st.title("😺 Cat CPT")
st.write("Soru sor, sohbet et, dosya ya da fotoğraf gönder!")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

uploaded_file = st.file_uploader("📎 Dosya veya görsel yükle (.txt, .pdf, .jpg, .png):", 
                                 type=["txt", "pdf", "jpg", "jpeg", "png"])

def analyze_text_file(file):
    text = file.read().decode("utf-8")
    return f"📄 Dosya içeriği özetle:\n\n{text[:500]}..."

def analyze_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages[:2]:
        text += page.extract_text()
    return f"📄 PDF Özeti:\n\n{text[:500]}..."

def analyze_image(file):
    image = Image.open(file)
    st.image(image, caption="Yüklenen Görsel", use_column_width=True)
    return "🖼️ Görsel analizim: Resimde ilginç bir şey var gibi görünüyor! Daha iyi analiz için gelişmiş modele ihtiyaç var 😺"

if uploaded_file:
    st.session_state.chat_history.append(("Sen", f"{uploaded_file.name} dosyasını yükledi."))

    if uploaded_file.type == "text/plain":
        result = analyze_text_file(uploaded_file)
    elif uploaded_file.type == "application/pdf":
        result = analyze_pdf(uploaded_file)
    elif uploaded_file.type.startswith("image/"):
        result = analyze_image(uploaded_file)
    else:
        result = "Bu dosya türünü analiz edemiyorum."

    st.session_state.chat_history.append(("Cat CPT", result))

def is_question(text):
    return "?" in text or text.strip().lower().startswith(("kim", "ne", "hangi", "neden", "nasıl", "kaç", "nerede"))

def is_analytic_question(text):
    keywords = [
        "etkiler", "mantıklı mı", "doğru mu", "yanlış mı", "gerekiyor mu",
        "zararlı mı", "iyi mi", "kötü mü", "gerekli mi", "faydalı mı", "tehlikeli mi",
        "ne düşünüyorsun", "sence", "olur mu", "doğru olur mu", "düşüncen nedir"
    ]
    text_lower = text.lower()
    return any(kw in text_lower for kw in keywords) or text_lower.startswith(("sence", "sana göre"))

def is_casual_greeting(text):
    greetings = [
        "selam", "merhaba", "naber", "nasılsın", "günaydın", "iyi akşamlar", "iyi geceler",
        "teşekkür", "teşekkür ederim", "sağ ol", "eyvallah", "hoşça kal", "görüşürüz",
        "napıyon", "ne yapıyorsun", "adın ne", "ismin ne", "seni kim yaptı", "geliştiricin kim"
    ]
    return any(greet in text.lower() for greet in greetings)

def respond_to_greeting(text):
    text = text.lower()
    if "napıyon" in text or "ne yapıyorsun" in text:
        return "Seninle sohbet ediyorum 😸"
    elif "adın ne" in text or "ismin ne" in text:
        return "Benim adım Cat CPT! Yapay zekâyım 😺"
    elif "seni kim yaptı" in text or "geliştiricin kim" in text:
        return "Beni Melih yaptı! Harika biri 😎"
    elif "teşekkür" in text
