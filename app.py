import streamlit as st
from PyPDF2 import PdfReader
from PIL import Image
import urllib.parse

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

# Gündelik konuşmaları tanıma ve işlem
if text:
    text = text.lower()

    if "selam" in text or "merhaba" in text:
        st.write("Selam! Size nasıl yardımcı olabilirim?")
    elif "naber" in text or "nasılsın" in text:
        st.write("İyiyim, sen nasılsın?")
    elif "teşekkür" in text:
        st.write("Rica ederim! 😊")
    else:
        # Soruysa Google ve Wikipedia linki oluştur
        st.write("Sorunuzu araştırıyorum...")

        query = urllib.parse.quote_plus(text)
        google_link = f"https://www.google.com/search?q={query}"
        wiki_link = f"https://tr.wikipedia.org/wiki/{query.replace('+', '_')}"

        st.markdown(f"🔍 [Google'da Ara]({google_link})")
        st.markdown(f"📚 [Vikipedi'de Bak]({wiki_link})")
