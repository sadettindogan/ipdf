import streamlit as st

st.set_page_config(
    page_title="iPDF",
    page_icon="📄",
    layout="centered"
)

st.title("📄 iPDF")
st.markdown("### PDF araçları, tek yerde.")
st.markdown("Soldaki menüden bir araç seç:")

st.info("✂️ **PDF Ayır** — Büyük PDF'i sayfa sayfa böl")
st.info("🔗 **PDF Birleştir** — Birden fazla PDF'i tek dosyada topla")

st.caption("Tüm işlemler tarayıcında yapılır, dosyaların sunucuya kaydedilmez.")
