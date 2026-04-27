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
    [data-testid="stFileUploader"] {
        border: 3px dashed #e67e22;
        border-radius: 16px;
        padding: 30px;
        background: #fff8f0;
        min-height: 120px;
    }
    [data-testid="stFileUploader"]:hover {
        background: #ffeedd;
        border-color: #d35400;
    }
    div[data-testid="stCheckbox"] label {
        font-size: 13px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

st.title("✂️ PDF Ayır")
st.markdown("PDF'i yükle, sayfaları önizle, tık ile seç ve indir.")

if "secili_sayfalar" not in st.session_state:
    st.session_state.secili_sayfalar = set()
if "pdf_bytes" not in st.session_state:
    st.session_state.pdf_bytes = None
if "pdf_isim" not in st.session_state:
    st.session_state.pdf_isim = ""

# Upload alanı
yuklenen = st.file_uploader(
    "📂 PDF dosyasını buraya sürükle veya tıkla",
    type="pdf",
    help="Tek PDF yükle"
)

if yuklenen:
    if yuklenen.name != st.session_state.pdf_isim:
        st.session_state.pdf_bytes = yuklenen.read()
        st.session_state.pdf_isim = yuklenen.name
        st.session_state.secili_sayfalar = set()
        st.rerun()

if st.session_state.pdf_bytes:
    doc = fitz.open(stream=st.session_state.pdf_bytes, filetype="pdf")
    toplam = len(doc.pages)

    st.success(f"✅ **{st.session_state.pdf_isim}** — Toplam **{toplam}** sayfa")

    # Hızlı seçim
    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        if st.button("✅ Tümünü Seç", use_container_width=True):
            st.session_state.secili_sayfalar = set(range(1, toplam + 1))
            st.rerun()
    with c2:
        if st.button("❌ Temizle", use_container_width=True):
            st.session_state.secili_sayfalar = set()
            st.rerun()
    with c3:
        if st.session_state.secili_sayfalar:
            secili_siralı = sorted(st.session_state.secili_sayfalar)
            st.info(f"**{len(secili_siralı)} sayfa seçili:** {', '.join(str(s) for s in secili_siralı)}")

    st.markdown("---")
    st.markdown("### 📄 Sayfaları önizle ve seç")

    cols_per_row = 5
    degisti = False
    yeni_secim = set(st.session_state.secili_sayfalar)

    for row_start in range(0, toplam, cols_per_row):
        cols = st.columns(cols_per_row)
        for col_idx in range(cols_per_row):
            sayfa_no = row_start + col_idx + 1
            if sayfa_no > toplam:
                break
            with cols[col_idx]:
                secili = sayfa_no in st.session_state.secili_sayfalar

                # Seçili ise yeşil çerçeve
                border_color = "#27ae60" if secili else "#ddd"
                bg_color = "#f0fff4" if secili else "white"
                st.markdown(
                    f'<div style="border:3px solid {border_color}; border-radius:10px; '
                    f'background:{bg_color}; padding:4px; margin-bottom:4px;">',
                    unsafe_allow_html=True
                )

                # Sayfa görseli — büyük
                pix = doc.load_page(sayfa_no - 1).get_pixmap(matrix=fitz.Matrix(1.2, 1.2))
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                st.image(img, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

                # Checkbox
                checked = st.checkbox(
                    f"{'✅ ' if secili else ''}Sayfa {sayfa_no}",
                    value=secili,
                    key=f"s_{sayfa_no}"
                )
                if checked != secili:
                    if checked:
                        yeni_secim.add(sayfa_no)
                    else:
                        yeni_secim.discard(sayfa_no)
                    degisti = True

    doc.close()

    if degisti:
        st.session_state.secili_sayfalar = yeni_secim
        st.rerun()

    # İndir butonu
    if st.session_state.secili_sayfalar:
        st.markdown("---")
        secili_siralı = sorted(st.session_state.secili_sayfalar)
        if st.button("✅ Seçili Sayfaları Ayır ve İndir", type="primary", use_container_width=True):
            with st.spinner("Ayırılıyor..."):
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
            st.download_button(
                f"⬇️ İndir: {cikti}",
                buf, cikti, "application/pdf",
                use_container_width=True
            )
            st.success("✅ Ayırma tamamlandı!")
    else:
        st.warning("Henüz sayfa seçilmedi.")

st.caption("Tüm işlemler tarayıcıda yapılır, dosyaların sunucuya kaydedilmez.")
