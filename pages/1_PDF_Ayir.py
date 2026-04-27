import streamlit as st
import pikepdf
import io

st.set_page_config(page_title="PDF Ayır", page_icon="✂️", layout="centered")

# Sidebar gizle
st.markdown("""
<style>
    [data-testid="stSidebar"] {display: none;}
    [data-testid="collapsedControl"] {display: none;}
</style>
""", unsafe_allow_html=True)

st.title("✂️ PDF Ayır")
st.markdown("PDF dosyasından istediğin sayfaları ayır ve indir.")

yuklenen = st.file_uploader("PDF dosyasını seç", type="pdf")

if yuklenen:
    try:
        pdf_bytes = yuklenen.read()
        pdf = pikepdf.open(io.BytesIO(pdf_bytes))
        toplam_sayfa = len(pdf.pages)
        pdf.close()

        st.success(f"✅ **{yuklenen.name}** yüklendi — Toplam **{toplam_sayfa}** sayfa")

        st.markdown("### Hangi sayfaları ayırmak istiyorsun?")
        sayfa_input = st.text_input(
            "Sayfa numaralarını girin",
            placeholder="Örn: 1,3,5 veya 2"
        )
        st.caption(f"1 ile {toplam_sayfa} arasında sayfa numarası girin, virgülle ayırın.")

        if st.button("✅ Ayır ve İndir", type="primary", use_container_width=True):
            if not sayfa_input.strip():
                st.error("Lütfen sayfa numarası girin!")
            else:
                sayfalar = []
                hatali = []
                for s in sayfa_input.split(","):
                    s = s.strip()
                    if s.isdigit():
                        no = int(s)
                        if 1 <= no <= toplam_sayfa:
                            sayfalar.append(no)
                        else:
                            hatali.append(s)
                    else:
                        hatali.append(s)

                if hatali:
                    st.warning(f"Geçersiz sayfa numaraları atlandı: {', '.join(hatali)}")

                if sayfalar:
                    pdf_in = pikepdf.open(io.BytesIO(pdf_bytes))
                    yeni_pdf = pikepdf.Pdf.new()
                    for no in sayfalar:
                        yeni_pdf.pages.append(pdf_in.pages[no - 1])
                    pdf_in.close()

                    cikti = io.BytesIO()
                    yeni_pdf.save(cikti)
                    yeni_pdf.close()
                    cikti.seek(0)

                    cikti_adi = f"ayrilan_{yuklenen.name}"
                    st.download_button(
                        label=f"⬇️ İndir: {cikti_adi}",
                        data=cikti,
                        file_name=cikti_adi,
                        mime="application/pdf",
                        use_container_width=True
                    )
                    st.success(f"Seçilen sayfalar: {', '.join(str(s) for s in sayfalar)}")
                else:
                    st.error("Geçerli sayfa bulunamadı!")

    except Exception as e:
        st.error(f"Hata: {e}")

else:
    st.info("Henüz PDF yüklenmedi. Yukarıdan dosya seç.")

st.caption("Tüm işlemler tarayıcıda yapılır, dosyaların sunucuya kaydedilmez.")
