import pikepdf
import os
import sys

def pdf_islem_garanti():
    try:
        # --- DÜZELTME BURADA BAŞLIYOR ---
        # Eğer program EXE olarak çalışıyorsa sys.executable yolunu kullanır
        if getattr(sys, 'frozen', False):
            mevcut_dizin = os.path.dirname(sys.executable)
        else:
            mevcut_dizin = os.path.dirname(os.path.abspath(__file__))
        
        os.chdir(mevcut_dizin)
        # --- DÜZELTME BURADA BİTTİ ---
        
        print("-" * 35)
        print(f"Klasör: {mevcut_dizin}")
        print("-" * 35)

        pdf_dosyalari = [f for f in os.listdir() if f.lower().endswith('.pdf')]
        
        if not pdf_dosyalari:
            print("Hata: Klasörde PDF dosyası bulunamadı!")
            return

        for i, dosya in enumerate(pdf_dosyalari, 1):
            print(f"{i}- {dosya}")
        
        secim_input = input("\nDosya numarası seçin: ")
        if not secim_input.isdigit():
            print("Hata: Geçersiz seçim!")
            return
            
        secim = int(secim_input)
        secilen_dosya = pdf_dosyalari[secim - 1]
        
        sayfa_input = input("Hangi sayfayı/sayfaları ayırmak istiyorsunuz? (Örn: 54 veya 1,2,5): ")
        alinacak_sayfalar = [int(s.strip()) for s in sayfa_input.split(',') if s.strip().isdigit()]

        if not alinacak_sayfalar:
            print("Hata: Sayfa numarası girmediniz!")
            return

        with pikepdf.open(secilen_dosya) as pdf:
            yeni_pdf = pikepdf.Pdf.new()
            
            for s_no in alinacak_sayfalar:
                if 1 <= s_no <= len(pdf.pages):
                    yeni_pdf.pages.append(pdf.pages[s_no - 1])
                else:
                    print(f"Uyarı: {s_no}. sayfa belgede mevcut değil.")

            if len(yeni_pdf.pages) > 0:
                cikti_adi = f"ayrilan_{secilen_dosya}"
                yeni_pdf.save(cikti_adi)
                print(f"\nBaşarılı! Dosya kaydedildi: {cikti_adi}")
            else:
                print("\nHata: Kaydedilecek geçerli sayfa bulunamadı.")

    except Exception as e:
        print(f"\n!!! HATA OLUŞTU !!!\nDetay: {e}")

if __name__ == "__main__":
    pdf_islem_garanti()
    print("\n" + "="*35)
    input("Kapatmak için Enter'a basın...")
