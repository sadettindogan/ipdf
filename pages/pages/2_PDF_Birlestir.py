import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
import os

st.set_page_config(page_title="PDF Birleştir", page_icon="🔗", layout="centered")

# Sidebar gizle
st.markdown("""
<style>
    [data-testid="stSidebar"] {display: none;}
    [data-testid="collapsedControl"] {display: none;}
</style>
""", unsafe_allow_html=True)

st.title("🔗 PDF Birleştir")
st.markdown("PDF dosyalarını yükle, sırala ve birleştir.")

# Session state başlat
if "pdf_listesi" not in st.session_state:
    st.session_state.pdf_listesi = []  # [{"isim": ..., "bytes": ...}]

# Dosya yükle
yuklenenler = st.file_uploader(
    "PDF dosyalarını seç (birden fazla seçebilirsin)",
    type="pdf",
    accept_multiple_files=True
)

if yuklenenler:
    mevcut_isimler = [p["isim"] for p in st.session_state.pdf_listesi]
    for f in yuklenenler:
        if f.name not in mevcut_isimler:
            st.session_state.pdf_listesi.append({"isim": f.name, "bytes": f.read()})

# PDF listesi varsa göster
if st.session_state.pdf_listesi:
    st.markdown("---")
    st.markdown("### 📋 Sıralama (Yukarı/Aşağı ile sırala)")

    for i, pdf in enumerate(st.session_state.pdf_listesi):
        col1, col2, col3, col4, col5 = st.columns([0.8, 2, 0.4, 0.4, 0.4])

        # Kapak görseli
        with col1:
            try:
                doc = fitz.open(stream=pdf["bytes"], filetype="pdf")
                pix = doc.load_page(0).get_pixmap(matrix=fitz.Matrix(0.4, 0.4))
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                doc.close()
                st.image(img, width=70)
            except:
                st.write("📄")

        with col2:
            st.markdown(f"**{i+1}.** {pdf['isim']}")

        with col3:
            if i > 0:
                if st.button("⬆️", key=f"yukari_{i}"):
                    st.session_state.pdf_listesi[i], st.session_state.pdf_listesi[i-1] = \
                        st.session_state.pdf_listesi[i-1], st.session_state.pdf_listesi[i]
                    st.rerun()

        with col4:
            if i < len(st.session_state.pdf_listesi) - 1:
                if st.button("⬇️", key=f"asagi_{i}"):
                    st.session_state.pdf_listesi[i], st.session_state.pdf_listesi[i+1] = \
                        st.session_state.pdf_listesi[i+1], st.session_state.pdf_listesi[i]
                    st.rerun()

        with col5:
            if st.button("🗑️", key=f"sil_{i}"):
                st.session_state.pdf_listesi.pop(i)
                st.rerun()

    st.markdown("---")

    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:
        if st.button("✅ Birleştir ve İndir", use_container_width=True, type="primary"):
            try:
                out = fitz.open()
                for pdf in st.session_state.pdf_listesi:
                    doc = fitz.open(stream=pdf["bytes"], filetype="pdf")
                    out.insert_pdf(doc)
                    doc.close()
                
                pdf_bytes = io.BytesIO()
                out.save(pdf_bytes)
                out.close()
                pdf_bytes.seek(0)

                st.download_button(
                    label="⬇️ İndir: birleşmişpdf.pdf",
                    data=pdf_bytes,
                    file_name="birleşmişpdf.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                st.success("Birleştirme tamamlandı!")
            except Exception as e:
                st.error(f"Hata: {e}")

    with col_btn2:
        if st.button("🗑️ Listeyi Temizle", use_container_width=True):
            st.session_state.pdf_listesi = []
            st.rerun()

else:
    st.info("Henüz PDF yüklenmedi. Yukarıdan dosya seç.")

st.caption("Tüm işlemler tarayıcıda yapılır, dosyaların sunucuya kaydedilmez.")
