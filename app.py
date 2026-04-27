import streamlit as st

st.set_page_config(
    page_title="iPDF",
    page_icon="📄",
    layout="centered"
)

# Sidebar'ı gizle
st.markdown("""
    <style>
        [data-testid="stSidebar"] {display: none;}
        [data-testid="collapsedControl"] {display: none;}
        
        .card {
            display: block;
            padding: 16px 20px;
            border-radius: 10px;
            border: 1px solid #e0e0e0;
            background-color: #f8f9fa;
            text-decoration: none;
            color: inherit;
            margin-bottom: 12px;
            transition: background-color 0.2s;
        }
        .card:hover {
            background-color: #e8f0fe;
            border-color: #4a90e2;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📄 iPDF")
st.markdown("### PDF araçları, tek yerde.")

st.markdown("""
    <a class="card" href="/PDF_Ayir">
        🔧 <strong>PDF Ayır</strong> — Büyük PDF'i sayfa sayfa böl
    </a>
    <a class="card" href="/PDF_Birlestir">
        🔗 <strong>PDF Birleştir</strong> — Birden fazla PDF'i tek dosyada topla
    </a>
""", unsafe_allow_html=True)

st.caption("Tüm işlemler tarayıcıda yapılır, dosyaların sunucuya kaydedilmez.")
