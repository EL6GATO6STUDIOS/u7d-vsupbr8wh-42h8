import streamlit as st
from PyPDF2 import PdfReader
from PIL import Image
from googlesearch import search
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Cat CPT 😺", layout="wide")
st.title("Cat CPT 😺")

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

# Gündelik konuşmaları tanıma ve araştırma
if text:
    text = text.lower()

    if "selam" in text or "merhaba" in text:
        st.write("Selam! Size nasıl yardımcı olabilirim?")
    elif "naber" in text or "nasılsın" in text:
        st.write("İyiyim, sen nasılsın?")
    elif "teşekkür" in text:
        st.write("Rica ederim! 😊")
    else:
        st.write("Sorunuzu araştırıyorum...")

        try:
            # Google'da arama yap
            results = list(search(text, num_results=1))
            if results:
                url = results[0]
                response = requests.get(url, timeout=10)
                soup = BeautifulSoup(response.text, "html.parser")
                paragraphs = soup.find_all("p")
                answer = ""
                for p in paragraphs:
                    if len(p.text.strip()) > 50:
                        answer = p.text.strip()
                        break
                if answer:
                    st.write("🔎 **Cevap:**", answer)
                else:
                    st.write("Uygun bir cevap bulunamadı.")
            else:
                st.write("Hiç sonuç bulunamadı.")
        except Exception as e:
            st.write("Araştırma sırasında bir hata oluştu:", str(e))
