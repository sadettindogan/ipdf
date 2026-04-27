import streamlit as st
import fitz
from PIL import Image
import io

st.set_page_config(page_title="PDF Birleştir", page_icon="🔗", layout="wide")

st.markdown("""
<style>
    [data-testid="stSidebar"] {display: none;}
    [data-testid="collapsedControl"] {display: none;}
    .pdf-card {
        border: 2px solid #e0e0e0;
        border-radius: 12px;
        padding: 10px;
        text-align: center;
        background: #fafafa;
        margin-bottom: 10px;
    }
    .pdf-card:hover {border-color: #4a90e2;}
</style>
""", unsafe_allow_html=True)

st.title("🔗 PDF Birleştir")

if "pdf_listesi" not in st.session_state:
    st.session_state.pdf_listesi = []

yuklenenler = st.file_uploader("PDF dosyalarını seç", type="pdf", accept_multiple_files=True)

if yuklenenler:
    mevcut = [p["isim"] for p in st.session_state.pdf_listesi]
    for f in yuklenenler:
        if f.name not in mevcut:
            st.session_state.pdf_listesi.append({"isim": f.name, "bytes": f.read()})

if st.session_state.pdf_listesi:
    st.markdown("---")
    st.markdown(f"### 📋 Yüklenen PDFler — {len(st.session_state.pdf_listesi)} dosya")
    st.caption("Sırayı değiştirmek için ⬆️⬇️ butonlarını kullan.")

    cols = st.columns(4)
    for i, pdf in enumerate(st.session_state.pdf_listesi):
        with cols[i % 4]:
            try:
                doc = fitz.open(stream=pdf["bytes"], filetype="pdf")
                pix = doc.load_page(0).get_pixmap(matrix=fitz.Matrix(1.2, 1.2))
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                doc.close()
                st.image(img, use_container_width=True)
            except:
                st.write("📄")

            st.markdown(f"**{i+1}.** {pdf['isim'][:22]}")

            c1, c2, c3 = st.columns(3)
            with c1:
                if i > 0:
                    if st.button("⬆️", key=f"u{i}"):
                        st.session_state.pdf_listesi[i], st.session_state.pdf_listesi[i-1] = \
                            st.session_state.pdf_listesi[i-1], st.session_state.pdf_listesi[i]
                        st.rerun()
            with c2:
                if i < len(st.session_state.pdf_listesi) - 1:
                    if st.button("⬇️", key=f"d{i}"):
                        st.session_state.pdf_listesi[i], st.session_state.pdf_listesi[i+1] = \
                            st.session_state.pdf_listesi[i+1], st.session_state.pdf_listesi[i]
                        st.rerun()
            with c3:
                if st.button("🗑️", key=f"x{i}"):
                    st.session_state.pdf_listesi.pop(i)
                    st.rerun()

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Birleştir ve İndir", type="primary", use_container_width=True):
            out = fitz.open()
            for pdf in st.session_state.pdf_listesi:
                doc = fitz.open(stream=pdf["bytes"], filetype="pdf")
                out.insert_pdf(doc)
                doc.close()
            buf = io.BytesIO()
            out.save(buf)
            out.close()
            buf.seek(0)
            st.download_button("⬇️ İndir: birleşmişpdf.pdf", buf, "birleşmişpdf.pdf", "application/pdf", use_container_width=True)
            st.success("Birleştirme tamamlandı!")
    with col2:
        if st.button("🗑️ Listeyi Temizle", use_container_width=True):
            st.session_state.pdf_listesi = []
            st.rerun()
else:
    st.info("Henüz PDF yüklenmedi.")

st.caption("Tüm işlemler tarayıcıda yapılır, dosyaların sunucuya kaydedilmez.")
