import streamlit as st
from PyPDF2 import PdfReader
from PIL import Image
from googlesearch import search
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Cat CPT 😺", layout="wide")
st.title("Cat CPT 😺")

# Soruları ve cevapları saklayacağımız liste
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Kullanıcıdan metin al
text = st.text_input("Sorunuzu yazın:")

# Dosya yükleme alanı
uploaded_file = st.file_uploader("Bir dosya yükleyin (.pdf, .txt, .jpg, .png)", type=["pdf", "txt", "jpg", "jpeg", "png"])

# Dosya analiz kısmı
if uploaded_file is not None:
    file_type = uploaded_file.type
    st.subheader("Yüklenen Dosya:")

    if "pdf" in file_type:
        reader = PdfReader(uploaded_file)
        all_text = ""
        for page in reader.pages:
            all_text += page.extract_text()
        st.text_area("PDF İçeriği", all_text)
    
    elif "text" in file_type:
        content = uploaded_file.read().decode("utf-8")
        st.text_area("Metin Dosyası İçeriği", content)

    elif "image" in file_type:
        img = Image.open(uploaded_file)
        st.image(img, caption="Yüklenen Görsel", use_column_width=True)

# Kullanıcının yazdığı metin varsa işle
if text:
    text = text.lower()

    # Gündelik konuşmalara özel cevap ver
    if "selam" in text or "merhaba" in text:
        response = "Selam! Size nasıl yardımcı olabilirim?"
    elif "naber" in text or "nasılsın" in text:
        response = "İyiyim, sen nasılsın?"
    elif "teşekkür" in text:
        response = "Rica ederim! 😊"
    else:
        response = "Araştırılıyor..."
        try:
            results = list(search(text, num_results=1))
            if results:
                url = results[0]
                res = requests.get(url, timeout=10)
                soup = BeautifulSoup(res.text, "html.parser")
                paragraphs = soup.find_all("p")
                found = False
                for p in paragraphs:
                    if len(p.text.strip()) > 50:
                        response = p.text.strip()
                        found = True
                        break
                if not found:
                    response = "Uygun bir cevap bulunamadı."
            else:
                response = "Hiç sonuç bulunamadı."
        except Exception as e:
            response = f"Araştırma sırasında bir hata oluştu: {str(e)}"

    # Soruyu ve cevabı geçmişe ekle
    st.session_state.chat_history.append((text, response))

# Önceki soru-cevapları sırayla göster
if st.session_state.chat_history:
    st.subheader("🧠 Sohbet Geçmişi")
    for i, (q, a) in enumerate(st.session_state.chat_history, start=1):
        st.markdown(f"**{i}. Soru:** {q}")
        st.markdown(f"**{i}. Cevap:** {a}")
