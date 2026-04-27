import streamlit as st

st.set_page_config(
    page_title="iPDF",
    page_icon="📄",
    layout="centered"
)

st.title("📄 iPDF")
st.markdown("### PDF araçları, tek yerde.")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.page_link("pages/1_PDF_Ayir.py", label="✂️ PDF Ayır", use_container_width=True)
    st.caption("Büyük PDF'i sayfa sayfa böl")

with col2:
    st.page_link("pages/2_PDF_Birlestir.py", label="🔗 PDF Birleştir", use_container_width=True)
    st.caption("Birden fazla PDF'i tek dosyada topla")

st.markdown("---")
st.caption("Tüm işlemler tarayıcında yapılır, dosyaların sunucuya kaydedilmez.")
