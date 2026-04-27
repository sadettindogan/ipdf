import streamlit as st
import fitz
from PIL import Image
import io

st.set_page_config(page_title="PDF Birleştir", page_icon="🔗", layout="wide")

st.markdown("""
<style>
    [data-testid="stSidebar"] {display: none;}
    [data-testid="collapsedControl"] {display: none;}
    [data-testid="stFileUploader"] {
        border: 3px dashed #4a90e2;
        border-radius: 16px;
        padding: 30px;
        background: #f0f6ff;
        min-height: 120px;
    }
    [data-testid="stFileUploader"]:hover {
        background: #e0eeff;
        border-color: #2563eb;
    }
    .pdf-grid-card {
        border: 2px solid #e0e0e0;
        border-radius: 12px;
        overflow: hidden;
        background: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: box-shadow 0.2s;
        margin-bottom: 8px;
        padding: 8px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

st.title("🔗 PDF Birleştir")
st.markdown("PDF dosyalarını sürükle-bırak ile yükle, sırala ve birleştir.")

if "pdf_listesi" not in st.session_state:
    st.session_state.pdf_listesi = []

# Upload alanı — büyük, sürükle bırak
yuklenenler = st.file_uploader(
    "📂 PDF dosyalarını buraya sürükle veya tıkla",
    type="pdf",
    accept_multiple_files=True,
    help="Birden fazla PDF seçebilirsin"
)

if yuklenenler:
    mevcut = [p["isim"] for p in st.session_state.pdf_listesi]
    eklendi = 0
    for f in yuklenenler:
        if f.name not in mevcut:
            data = f.read()
            # İlk sayfa önizlemesi oluştur
            try:
                doc = fitz.open(stream=data, filetype="pdf")
                pix = doc.load_page(0).get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                onizleme = buf.getvalue()
                toplam_sayfa = len(doc.pages)
                doc.close()
            except:
                onizleme = None
                toplam_sayfa = "?"
            st.session_state.pdf_listesi.append({
                "isim": f.name,
                "bytes": data,
                "onizleme": onizleme,
                "sayfa": toplam_sayfa
            })
            eklendi += 1
    if eklendi:
        st.rerun()

# Önizleme grid
if st.session_state.pdf_listesi:
    st.markdown("---")
    st.markdown(f"### 📋 {len(st.session_state.pdf_listesi)} PDF yüklendi — Sırayı düzenle")

    cols_per_row = 4
    for row_start in range(0, len(st.session_state.pdf_listesi), cols_per_row):
        cols = st.columns(cols_per_row)
        for col_idx in range(cols_per_row):
            i = row_start + col_idx
            if i >= len(st.session_state.pdf_listesi):
                break
            pdf = st.session_state.pdf_listesi[i]
            with cols[col_idx]:
                st.markdown(f'<div class="pdf-grid-card">', unsafe_allow_html=True)
                if pdf["onizleme"]:
                    st.image(pdf["onizleme"], use_container_width=True)
                else:
                    st.markdown("📄")
                st.markdown(f"**{i+1}.** {pdf['isim'][:20]}")
                st.caption(f"{pdf['sayfa']} sayfa")
                st.markdown("</div>", unsafe_allow_html=True)

                c1, c2, c3 = st.columns(3)
                with c1:
                    if i > 0 and st.button("⬆️", key=f"u{i}"):
                        st.session_state.pdf_listesi[i], st.session_state.pdf_listesi[i-1] = \
                            st.session_state.pdf_listesi[i-1], st.session_state.pdf_listesi[i]
                        st.rerun()
                with c2:
                    if i < len(st.session_state.pdf_listesi)-1 and st.button("⬇️", key=f"d{i}"):
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
            with st.spinner("Birleştiriliyor..."):
                out = fitz.open()
                for pdf in st.session_state.pdf_listesi:
                    doc = fitz.open(stream=pdf["bytes"], filetype="pdf")
                    out.insert_pdf(doc)
                    doc.close()
                buf = io.BytesIO()
                out.save(buf)
                out.close()
                buf.seek(0)
            st.download_button(
                "⬇️ İndir: birleşmişpdf.pdf",
                buf, "birleşmişpdf.pdf", "application/pdf",
                use_container_width=True
            )
            st.success("✅ Birleştirme tamamlandı!")
    with col2:
        if st.button("🗑️ Listeyi Temizle", use_container_width=True):
            st.session_state.pdf_listesi = []
            st.rerun()

else:
    st.info("⬆️ Yukarıdaki alana PDF sürükle veya tıkla.")

st.caption("Tüm işlemler tarayıcıda yapılır, dosyaların sunucuya kaydedilmez.")
