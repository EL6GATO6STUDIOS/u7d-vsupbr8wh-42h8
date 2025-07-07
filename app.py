
import streamlit as st
import wikipedia
from PyPDF2 import PdfReader
from PIL import Image

wikipedia.set_lang("tr")
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
    elif "teşekkür" in text or "sağ ol" in text or "eyvallah" in text:
        return "Ne demek, her zaman yardıma hazırım! 😺"
    elif "günaydın" in text:
        return "Günaydın! Güne enerjiyle başla 😸"
    elif "iyi akşamlar" in text:
        return "İyi akşamlar! Umarım günün güzel geçmiştir."
    elif "iyi geceler" in text:
        return "İyi geceler! Tatlı rüyalar 😴"
    elif "naber" in text or "nasılsın" in text:
        return "İyiyim, sen nasılsın? Sohbet etmek harika!"
    elif "selam" in text or "merhaba" in text:
        return "Selam! Hoş geldin 😺"
    elif "görüşürüz" in text or "hoşça kal" in text:
        return "Görüşürüz! Kendine dikkat et 🐾"
    else:
        return "😺"

def search_wikipedia(query):
    try:
        results = wikipedia.search(query)
        if not results:
            return "Wikipedia'da bu konuyla ilgili bir şey bulamadım."
        summary = wikipedia.summary(results[0], sentences=2)
        return summary
    except Exception:
        return "Wikipedia'dan bilgi alırken bir hata oluştu."

def generate_analysis(text):
    return f"Bu konu tartışmalı. Benim düşünceme göre: '{text}' farklı görüşlere sahip olabilir. Avantajları ve riskleri var."

user_message = st.chat_input("Mesajınızı yazın...")

if user_message:
    st.session_state.chat_history.append(("Sen", user_message))

    if is_casual_greeting(user_message):
        bot_response = respond_to_greeting(user_message)
    elif is_question(user_message):
        if is_analytic_question(user_message):
            bot_response = generate_analysis(user_message)
        else:
            bot_response = f"📚 Wikipedia'dan buldum:\n\n{search_wikipedia(user_message)}"
    else:
        bot_response = "Bu bir soru gibi görünmüyor. Sohbet etmek istersen buradayım 😺"

    st.session_state.chat_history.append(("Cat CPT", bot_response))

for sender, message in st.session_state.chat_history:
    with st.chat_message(sender.lower()):
        st.markdown(message)
