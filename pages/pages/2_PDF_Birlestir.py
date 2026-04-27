import fitz  # PyMuPDF
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

class PDFBirlestirici:
    def __init__(self, root):
        self.root = root
        self.root.title("Görsel PDF Düzenleyici - Sadettin Doğan")
        self.klasor_yolu = os.path.dirname(os.path.abspath(__file__))
        
        self.pdf_kartlari = []
        self.suruklenen_indeks = None
        self.hayalet_label = None

        self.root.geometry("1100x850")
        self.root.configure(bg="#f0f0f0")

        # Üst Buton
        self.btn = tk.Button(root, text="SIRALAMAYI ONAYLA VE OTOMATİK KAYDET", 
                             command=self.birlestir, bg="#27ae60", fg="white", 
                             font=('Arial', 12, 'bold'), pady=10)
        self.btn.pack(fill="x", padx=20, pady=10)

        # Kaydırılabilir Alan
        self.canvas = tk.Canvas(root, bg="#ffffff")
        self.scroll_y = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.container = tk.Frame(self.canvas, bg="#ffffff")

        self.canvas.create_window((0, 0), window=self.container, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll_y.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll_y.pack(side="right", fill="y")

        self.pdf_yukle()

    def pdf_yukle(self):
        # Klasördeki PDF'leri bul (daha önce birleşen dosyayı listeye ekleme)
        dosyalar = [f for f in os.listdir(self.klasor_yolu) 
                    if f.lower().endswith(".pdf") and not f.startswith("birleşmişpdf")]
        
        for f in dosyalar:
            yol = os.path.join(self.klasor_yolu, f)
            try:
                doc = fitz.open(yol)
                pix = doc.load_page(0).get_pixmap(matrix=fitz.Matrix(0.3, 0.3))
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                photo = ImageTk.PhotoImage(img)
                doc.close()

                kart = tk.Frame(self.container, bd=1, relief="solid", bg="white")
                kart.yol = yol
                
                lbl_img = tk.Label(kart, image=photo, bg="white")
                lbl_img.image = photo
                lbl_img.pack(padx=5, pady=5)

                tk.Label(kart, text=f[:20], bg="white", font=("Arial", 8)).pack()

                for w in (kart, lbl_img):
                    w.bind("<Button-1>", self.basla)
                    w.bind("<B1-Motion>", self.surukle)
                    w.bind("<ButtonRelease-1>", self.bitir)

                self.pdf_kartlari.append(kart)
            except:
                continue
        self.ciz()

    def ciz(self):
        for i, k in enumerate(self.pdf_kartlari):
            k.grid(row=i // 4, column=i % 4, padx=15, pady=15)
        self.container.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def basla(self, event):
        w = event.widget
        target = w.master if isinstance(w, tk.Label) else w
        if target in self.pdf_kartlari:
            self.suruklenen_indeks = self.pdf_kartlari.index(target)
            self.hayalet_label = tk.Label(self.root, image=target.winfo_children()[0].image, bd=1, relief="solid")
            self.hayalet_label.place(x=event.x_root - self.root.winfo_rootx(), y=event.y_root - self.root.winfo_rooty())

    def surukle(self, event):
        if self.hayalet_label:
            self.hayalet_label.place(x=event.x_root - self.root.winfo_rootx() - 30, 
                                     y=event.y_root - self.root.winfo_rooty() - 30)

    def bitir(self, event):
        if self.suruklenen_indeks is not None:
            x = self.root.winfo_pointerx() - self.container.winfo_rootx()
            y = self.root.winfo_pointery() - self.container.winfo_rooty()
            
            hedef = None
            for i, k in enumerate(self.pdf_kartlari):
                if k.winfo_x() < x < k.winfo_x()+k.winfo_width() and k.winfo_y() < y < k.winfo_y()+k.winfo_height():
                    hedef = i
                    break
            
            if hedef is not None:
                self.pdf_kartlari.insert(hedef, self.pdf_kartlari.pop(self.suruklenen_indeks))
                self.ciz()
                
            if self.hayalet_label:
                self.hayalet_label.destroy()
            self.suruklenen_indeks = None

    def birlestir(self):
        if not self.pdf_kartlari:
            return

        out = fitz.open()
        for k in self.pdf_kartlari:
            doc = fitz.open(k.yol)
            out.insert_pdf(doc)
            doc.close()
        
        # Otomatik Dosya Adı Belirleme
        dosya_adi = "birleşmişpdf.pdf"
        hedef_yol = os.path.join(self.klasor_yolu, dosya_adi)
        
        # Eğer dosya varsa numaralandır (V1, V2 gibi)
        sayac = 1
        while os.path.exists(hedef_yol):
            hedef_yol = os.path.join(self.klasor_yolu, f"birleşmişpdf({sayac}).pdf")
            sayac += 1
            
        try:
            out.save(hedef_yol)
            out.close()
            messagebox.showinfo("Başarılı", f"Dosya kaydedildi:\n{os.path.basename(hedef_yol)}")
            self.root.destroy()
        except Exception as e:
            messagebox.showerror("Hata", f"Kaydedilemedi: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFBirlestirici(root)
    root.mainloop()
