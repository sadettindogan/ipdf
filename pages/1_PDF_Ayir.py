import streamlit as st
import fitz
from PIL import Image
import io
import pikepdf

st.set_page_config(page_title="PDF Ayır", page_icon="✂️", layout="wide")

st.markdown("""
<style>
    [data-testid="stSidebar"] {display: none;}
    [data-testid="collapsedControl"] {display: none;}
    .sayfa-secili {
        border: 3px solid #27ae60 !important;
        border-radius: 10px;
    }
    .sayfa-normal {
        border: 2px solid #e0e0e0;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.title("✂️ PDF Ayır")
st.markdown("PDF'i yükle, sayfaları seç ve indir.")

if "secili_sayfalar" not in st.session_state:
    st.session_state.secili_sayfalar = set()
if "pdf_bytes" not in st.session_state:
    st.session_state.pdf_bytes = None
if "pdf_isim" not in st.session_state:
    st.session_state.pdf_isim = ""

yuklenen = st.file_uploader("PDF dosyasını seç", type="pdf")

if yuklenen:
    if yuklenen.name != st.session_state.pdf_isim:
        st.session_state.pdf_bytes = yuklenen.read()
        st.session_state.pdf_isim = yuklenen.name
        st.session_state.secili_sayfalar = set()

if st.session_state.pdf_bytes:
    doc = fitz.open(stream=st.session_state.pdf_bytes, filetype="pdf")
    toplam = len(doc.pages)

    st.success(f"✅ **{st.session_state.pdf_isim}** — Toplam **{toplam}** sayfa")

    # Hızlı seçim butonları
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("✅ Tümünü Seç"):
            st.session_state.secili_sayfalar = set(range(1, toplam + 1))
            st.rerun()
    with c2:
        if st.button("❌ Seçimi Temizle"):
            st.session_state.secili_sayfalar = set()
            st.rerun()
    with c3:
        st.markdown(f"**Seçili: {len(st.session_state.secili_sayfalar)} sayfa**")

    st.markdown("---")
    st.markdown("### 📄 Sayfalara tıklayarak seç")

    # Sayfa önizlemeleri — 5 sütun
    cols_per_row = 5
    for row_start in range(0, toplam, cols_per_row):
        cols = st.columns(cols_per_row)
        for col_idx in range(cols_per_row):
            sayfa_no = row_start + col_idx + 1
            if sayfa_no > toplam:
                break
            with cols[col_idx]:
                # Sayfa görselini render et
                pix = doc.load_page(sayfa_no - 1).get_pixmap(matrix=fitz.Matrix(1.0, 1.0))
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

                secili = sayfa_no in st.session_state.secili_sayfalar

                # Seçili ise yeşil border efekti
                if secili:
                    st.markdown(f'<div style="border:3px solid #27ae60; border-radius:8px; padding:3px;">', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div style="border:2px solid #e0e0e0; border-radius:8px; padding:3px;">', unsafe_allow_html=True)

                st.image(img, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

                # Checkbox ile seçim
                checked = st.checkbox(
                    f"Sayfa {sayfa_no}" + (" ✅" if secili else ""),
                    value=secili,
                    key=f"sayfa_{sayfa_no}"
                )
                if checked and sayfa_no not in st.session_state.secili_sayfalar:
                    st.session_state.secili_sayfalar.add(sayfa_no)
                    st.rerun()
                elif not checked and sayfa_no in st.session_state.secili_sayfalar:
                    st.session_state.secili_sayfalar.discard(sayfa_no)
                    st.rerun()

    doc.close()

    st.markdown("---")
    if st.session_state.secili_sayfalar:
        secili_siralı = sorted(st.session_state.secili_sayfalar)
        st.info(f"Seçili sayfalar: {', '.join(str(s) for s in secili_siralı)}")

        if st.button("✅ Seçili Sayfaları Ayır ve İndir", type="primary", use_container_width=True):
            pdf_in = pikepdf.open(io.BytesIO(st.session_state.pdf_bytes))
            yeni = pikepdf.Pdf.new()
            for no in secili_siralı:
                yeni.pages.append(pdf_in.pages[no - 1])
            pdf_in.close()
            buf = io.BytesIO()
            yeni.save(buf)
            yeni.close()
            buf.seek(0)
            cikti = f"ayrilan_{st.session_state.pdf_isim}"
            st.download_button("⬇️ İndir: " + cikti, buf, cikti, "application/pdf", use_container_width=True)
            st.success("Ayırma tamamlandı!")
    else:
        st.warning("Henüz sayfa seçilmedi.")

st.caption("Tüm işlemler tarayıcıda yapılır, dosyaların sunucuya kaydedilmez.")
