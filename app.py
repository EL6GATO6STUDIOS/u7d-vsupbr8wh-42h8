import streamlit as st
from PyPDF2 import PdfReader
from PIL import Image
from googlesearch import search
import requests
from bs4 import BeautifulSoup
import random

# Sayfa başlığı ve ayarları
st.set_page_config(page_title="Cat CPT 😺", layout="wide")
st.title("Cat CPT 😺")

# Sohbet geçmişi
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Kullanıcıdan giriş al
text = st.text_input("Sorunuzu yazın:")

# Dosya yükleme alanı
uploaded_file = st.file_uploader("Bir dosya yükleyin (.pdf, .txt, .jpg, .png)", type=["pdf", "txt", "jpg", "jpeg", "png"])

# Yüklenen dosya gösterimi
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

# Yorumlama (analiz) cevabı üreten fonksiyon
def generate_opinion_response(user_input):
    fikir_sablonlari = [
        "Bence bu oldukça düşündürücü. {} konusu, insanların karakterine ve bakış açısına göre değişir.",
        "{} hakkında kendi fikrimi söylemem gerekirse: bu konuda oldukça net bir görüşüm var.",
        "Açıkçası ben {} konusuna pek sıcak bakmıyorum. Ama herkesin fikrine saygı duyarım.",
        "{} bana kalırsa günümüzde sıkça tartışılan bir mesele. Bence önemli olan kişinin yaklaşımıdır.",
        "{} konusunu düşündüğümde aklıma gelen ilk şey: insanları yargılamadan önce anlamaya çalışmak.",
        "Kendi bakış açıma göre, {} biraz abartılıyor olabilir. Ama yine de farklı düşünceler değerlidir.",
        "{} ile ilgili fikrim şu: bu durum tamamen bağlama göre değişebilir, ama genel olarak destekliyorum.",
    ]
    sablon = random.choice(fikir_sablonlari)
    return sablon.format(user_input.capitalize())

# Kullanıcının metnini işleme
if text:
    original_text = text
    lower_text = text.lower()

    # Gündelik konuşmalar
    if any(word in lower_text for word in ["selam", "merhaba"]):
        response = "Selam! Size nasıl yardımcı olabilirim?"
    elif any(word in lower_text for word in ["naber", "nasılsın"]):
        response = "İyiyim, sen nasılsın?"
    elif "teşekkür" in lower_text:
        response = "Rica ederim! 😊"

    # Analiz (yorumlama) isteyen ifadeler
    elif any(keyword in lower_text for keyword in ["sence", "yorumla", "analiz", "ne düşünüyorsun", "karakter", "tartış", "duygusal", "kişilik"]):
        response = generate_opinion_response(original_text)

    # Diğer tüm sorular için Google araştırması
    else:
        response = "Araştırılıyor..."
        try:
            results = list(search(original_text, num_results=1))
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
                    response = "Uygun bir bilgi bulunamadı."
            else:
                response = "Sonuç bulunamadı."
        except Exception as e:
            response = f"Araştırma sırasında bir hata oluştu: {str(e)}"

    # Sohbet geçmişine ekle
    st.session_state.chat_history.append((original_text, response))

# Geçmişi sırayla göster
if st.session_state.chat_history:
    st.subheader("🧠 Sohbet Geçmişi")
    for i, (q, a) in enumerate(st.session_state.chat_history, start=1):
        st.markdown(f"**{i}. Soru:** {q}")
        st.markdown(f"**{i}. Cevap:** {a}")
