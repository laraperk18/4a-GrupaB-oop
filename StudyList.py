import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import os
# -----------------
# KLASE
class AktivnostUcenja:
    def __init__(self, predmet, datum, trajanje):
        self.predmet = predmet
        try:
            self.datum = datetime.strptime(datum, "%d.%m.%Y")
        except:
            raise ValueError("Datum mora biti u formatu dd.mm.gggg")
        try:
            self.trajanje = int(trajanje)
            if self.trajanje <= 0:
                raise ValueError
        except:
            raise ValueError("Trajanje mora biti pozitivan, cijeli broj.")
    def prikazi_detalje(self):
        return f"[{self.datum.strftime('%d.%m.%Y')}] {self.predmet} ({self.trajanje} min)"

    def datum_obj(self):
        return self.datum

class TeorijskaSesija(AktivnostUcenja):
    def __init__(self, predmet,datum,trajanje,teme):
        super().__init__(predmet,datum,trajanje)
        self.teme = teme

    def prikazi_detalje(self):
        return f"[{self.datum.date()}] Teorijska Sesija: {self.predmet} - {self.teme} ({self.trajanje} min)"

class Vjezba(AktivnostUcenja):
    def __init__(self, predmet, datum, trajanje, broj_zadataka, poteskoca):
        super().__init__(predmet, datum, trajanje)
        try:
            self.brojzad = int(broj_zadataka)
            if self.brojzad <= 0:
                raise ValueError
        except:
            raise ValueError("Broj zadataka mora biti pozitivan broj.")
        self.poteskoca = poteskoca

    def prikazi_detalje(self):
        return f"[{self.datum.date()}] Vježba: {self.predmet} - {self.brojzad} zadataka ({self.trajanje} min, poteškoća: {self.poteskoca})"


# ----------------------------------------------------
# APP -------------
class PlanerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("StudyList")
        self.root.geometry("900x600")
        self.root.configure(bg="#cad2c5")
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)

        # --- MENI
        self.kreiraj_menu()
        self.statusna_traka()

        # --- LISTE
        self.subjects = ["Matematika", "Fizika", "Kemija", "Engleski","Hrvatski", "Filozofija","Informatika"]
        self.subject_var = tk.StringVar()
        self.aktivnosti = []

        # ------------------- FRAMES
        self.frame_unos= tk.Frame(self.root, padx=10, pady=10, bg="#84a98c")
        self.frame_unos.grid(row=0, column=0, sticky="EW")
        self.frame_unos.columnconfigure(1, weight=1)

        self.prikaz_frame=tk.Frame(self.root, padx=10, pady=10, bg="#52796f")
        self.prikaz_frame.grid(row=1, column=0, sticky="NSEW")
        self.prikaz_frame.columnconfigure(0, weight=1)
        self.prikaz_frame.rowconfigure(0, weight=1)

        self.frame_donji=tk.Frame(self.root, padx=10, pady=10, bg="#84a98c")
        self.frame_donji.grid(row=2, column=0, sticky="EW")

        self.napravi_unos()

        #----------------- REDINA - LISTBOX I BRISANNJE
        self.listbox=tk.Listbox(self.prikaz_frame, height=15, font=("Courier New", 11),
                                  bg="#354f52", fg="#cad2c5", selectbackground="#84a98c")
        self.listbox.grid(row=0, column=0, sticky="NSEW")
        scrollbar=tk.Scrollbar(self.prikaz_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="NS")
        self.listbox.config(yscrollcommand=scrollbar.set)

        self.gumb_obrisi = ttk.Button(self.prikaz_frame, text="Obriši selektirano", command=self.obrisi_aktivnost)
        self.gumb_obrisi.grid(row=1, column=0, sticky="ew", pady=5)

        #----------------- DOLE - FILTER
        ttk.Label(self.frame_donji, text="Filtriraj po predmetu:", background="#84a98c",
                  font=("Helvetica", 12, "bold")).grid(row=0, column=0, sticky="w")
        self.filter_predmet = ttk.Combobox(self.frame_donji, values=["Svi"] + self.subjects, state="readonly",
                                          font=("Helvetica", 11))
        self.filter_predmet.current(0)
        self.filter_predmet.grid(row=0, column=1, padx=5)

        ttk.Label(self.frame_donji, text="Tip aktivnosti:", background="#84a98c",
                  font=("Helvetica", 12, "bold")).grid(row=0, column=2, sticky="w", padx=5)
        self.filter_tip = ttk.Combobox(self.frame_donji, values=["Svi", "Teorijska sesija", "Vježba"], state="readonly",
                                       font=("Helvetica", 11))
        self.filter_tip.current(0)
        self.filter_tip.grid(row=0, column=3, padx=5)

        tk.Button(self.frame_donji, text="FILTRIRAJ", command=self.primijeni_filter,
          bg="#52796f", fg="white", activebackground="#354f52", activeforeground="white",
          font=("Helvetica", 11, "bold")).grid(row=0, column=4, padx=10)

    #-----------------
    # UNOS
    def napravi_unos(self):
        tk.Label(self.frame_unos, text="Tip aktivnosti:", background="#84a98c",
                  font=("Helvetica", 12, "bold")).grid(row=0, column=0, sticky="w")
        self.tip_var = tk.StringVar()
        self.combo_tip = ttk.Combobox(self.frame_unos, textvariable=self.tip_var, state="readonly",
                                      font=("Helvetica", 11))
        self.combo_tip['values']=("Teorijska sesija", "Vježba")
        self.combo_tip.grid(row=0, column=1, sticky="ew", padx=5)
        self.combo_tip.current(0)

        ttk.Label(self.frame_unos, text="Predmet:", background="#84a98c",
                  font=("Helvetica",12,"bold")).grid(row=1, column=0, sticky="w")
        self.combo_predmet = ttk.Combobox(self.frame_unos, textvariable=self.subject_var, values=self.subjects, state="normal",
                                         font=("Helvetica", 11))
        self.combo_predmet.grid(row=1, column=1, sticky="ew", padx=5)
        self.combo_predmet.set(self.subjects[0])
        self.gumb_predmet = tk.Button(self.frame_unos, text="Dodaj predmet",
                              command=self.dodaj_predmet,
                              bg="#52796f", fg="white", font=("Helvetica", 11, "bold"),
                              activebackground="#354f52", activeforeground="white")
        self.gumb_predmet.grid(row=1, column=2, padx=5)

        ttk.Label(self.frame_unos, text="Datum (dd.mm.gggg):", background="#84a98c",
                  font=("Helvetica", 12, "bold")).grid(row=2, column=0, sticky="w")
        self.entry_datum = ttk.Entry(self.frame_unos, font=("Helvetica", 11))
        self.entry_datum.insert(0, "dd.mm.gggg")
        self.entry_datum.grid(row=2, column=1, sticky="ew", padx=5)

        ttk.Label(self.frame_unos, text="Trajanje (min):", background="#84a98c",
                  font=("Helvetica", 12, "bold")).grid(row=3, column=0, sticky="w")
        self.entry_trajanje = ttk.Entry(self.frame_unos, font=("Helvetica", 11))
        self.entry_trajanje.grid(row=3, column=1, sticky="ew", padx=5)
    #-----------------
    # Dinamička polja
        self.label_teme=ttk.Label(self.frame_unos, text="Obrađene teme:", background="#84a98c", font=("Helvetica", 12, "bold"))
        self.entry_teme= ttk.Entry(self.frame_unos, font=("Helvetica", 11))
        self.label_zad=ttk.Label(self.frame_unos, text="Broj zadataka:", background="#84a98c", font=("Helvetica", 12, "bold"))
        self.entry_zad=ttk.Entry(self.frame_unos, font=("Helvetica", 11))
        self.label_pot=ttk.Label(self.frame_unos, text="Poteškoća:", background="#84a98c", font=("Helvetica", 12, "bold"))
        self.entry_pot=ttk.Entry(self.frame_unos, font=("Helvetica", 11))

        self.gumb_dodaj= tk.Button(self.frame_unos, text="UNESI",
                            command=self.dodaj_aktivnost,
                            bg="#52796f", fg="white", font=("Helvetica", 11, "bold"),
                            activebackground="#354f52", activeforeground="white")
        self.gumb_dodaj.grid(row=6, column=1, sticky="ew", pady=15)

        self.combo_tip.bind("<<ComboboxSelected>>", self.prikazi_polja)
        self.prikazi_polja()

    
    def prikazi_polja(self, *args):
        for widget in (self.label_teme, self.entry_teme, self.label_zad, self.entry_zad, self.label_pot, self.entry_pot):
            widget.grid_remove()
        if self.tip_var.get() == "Teorijska sesija":
            self.label_teme.grid(row=4, column=0, sticky="w")
            self.entry_teme.grid(row=4, column=1, sticky="ew", padx=5)
        else:
            self.label_zad.grid(row=4, column=0, sticky="w")
            self.entry_zad.grid(row=4, column=1, sticky="ew", padx=5)
            self.label_pot.grid(row=5, column=0, sticky="w")
            self.entry_pot.grid(row=5, column=1, sticky="ew", padx=5)

    #-----------------
    # UNOS
    def dodaj_predmet(self):
        novo=self.subject_var.get().strip()
        if novo=="":
            messagebox.showwarning("Prazan unos", "Potrebno je unijeti ime predmeta.")
            return
        if any(novo.lower()==s.lower() for s in self.subjects):
            messagebox.showinfo("Predmet postoji", f"Predmet '{novo}' je već na popisu.")
            return
        self.subjects.append(novo)
        self.combo_predmet['values'] = self.subjects
        self.combo_predmet.set(novo)
        self.filter_predmet['values'] = ["Svi"] + self.subjects
        messagebox.showinfo("Dodano", f"Predmet '{novo}' je dodan na popis.")

    def dodaj_aktivnost(self):
        predmet=self.subject_var.get()
        datum=self.entry_datum.get()
        trajanje=self.entry_trajanje.get()

        if predmet =="" or datum =="" or trajanje =="":
            messagebox.showerror("Greška", "Unesite sve podatke!")
            return

        tip = self.tip_var.get()

        try:
            if tip=="Teorijska sesija":
                teme=self.entry_teme.get()
                aktivnost=TeorijskaSesija(predmet, datum, trajanje, teme)
            else:
                broj_zadataka=self.entry_zad.get()
                poteskoca=self.entry_pot.get()
                aktivnost=Vjezba(predmet,datum, trajanje, broj_zadataka,poteskoca)
        except ValueError as e:
            messagebox.showerror("Greska", str(e))
            return
        self.aktivnosti.append(aktivnost)
        self.listbox.insert(tk.END, aktivnost.prikazi_detalje())
        self.status_var.set("Aktivnost dodana!")
        

    def primijeni_filter(self):
        predmet_f=self.filter_predmet.get()
        tip_f=self.filter_tip.get()
        self.listbox.delete(0, tk.END)
        for a in self.aktivnosti:
            if (predmet_f=="Svi" or a.predmet==predmet_f) and \
               (tip_f=="Svi" or (tip_f=="Teorijska sesija" and isinstance(a, TeorijskaSesija)) or
                (tip_f=="Vježba" and isinstance(a, Vjezba))):
                self.listbox.insert(tk.END, a.prikazi_detalje())

    #-----------------
    # BRISANJE
    def obrisi_aktivnost(self):
        selekcija= self.listbox.curselection()
        if not selekcija:
            messagebox.showwarning("Upozorenje", "Odaberite aktivnost za brisanje.")
            return
    
        index=selekcija[0]
        a=self.aktivnosti[index]
        potvrda=messagebox.askyesno("Brisanje", f"Jeste li sigurni da želite obrisati:\n{a.prikazi_detalje()}?")
        for index in reversed(selekcija):
            del self.aktivnosti[index]
            self.listbox.delete(index)
        self.status_var.set("Aktivnost obrisana.")

    #-----------------
    #SPREMANJE
    def spremi_xml(self):
        try:
            path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML datoteke", "*.xml")])
            if not path:
                return
            root = ET.Element("Planer")
            for a in self.aktivnosti:
                tip = "TeorijskaSesija" if isinstance(a, TeorijskaSesija) else "Vjezba"
                elem = ET.SubElement(root, tip)
                elem.set("predmet", a.predmet)
                elem.set("datum", a.datum.strftime("%d.%m.%Y"))
                elem.set("trajanje", str(a.trajanje))
                if isinstance(a, TeorijskaSesija):
                    elem.set("teme", a.teme)
                else:
                    elem.set("broj_zadataka", str(a.brojzad))
                    elem.set("poteskoca", a.poteskoca)
            tree = ET.ElementTree(root)
            tree.write(path, encoding="utf-8", xml_declaration=True)
            messagebox.showinfo("Uspjeh", f"Podaci su spremljeni u {path}")
            self.status_var.set(f"Datoteka {path} spremljena.")
        except Exception as e:
            messagebox.showerror("Greška", f"Došlo je do greške pri spremanju: {e}")

    def ucitaj_xml(self):
        try:
            path=filedialog.askopenfilename(filetypes=[("XML datoteke", "*.xml")])
            if not path:
                return
            if not os.path.exists(path):
                messagebox.showwarning("Upozorenje", f"Datoteka {path} ne postoji.")
                return
            tree=ET.parse(path)
            root=tree.getroot()
            self.aktivnosti.clear()
            self.listbox.delete(0, tk.END)
            for elem in root:
                if elem.tag == "TeorijskaSesija":
                    a=TeorijskaSesija(elem.get("predmet"),elem.get("datum"),elem.get("trajanje"),elem.get("teme"))
                else:
                    a=Vjezba(elem.get("predmet"), elem.get("datum"), elem.get("trajanje"), elem.get("broj_zadataka"), elem.get("poteskoca"))
                self.aktivnosti.append(a)
                self.listbox.insert(tk.END, a.prikazi_detalje())
            messagebox.showinfo("Učitano", f"Podaci su učitani iz {path}")
            self.status_var.set(f"Datoteka {path} učitana.")
        except Exception as e:
            messagebox.showerror("Greska",f"Doslo je do greške pri učitavanju: {e}")

    #-----------------
    # VRIJEME
    def izracun_ukupno(self, tjedan_samo=False, predmet_filter=None):
        if not self.aktivnosti:
            messagebox.showinfo("Info","Nema unesenih aktivnosti.")
            return
        ukupno = 0
        trajanje_po_predmetu = {}
        danas = datetime.today()
        tjedan_pocetak = danas - timedelta(days=danas.weekday())
        tjedan_kraj = tjedan_pocetak + timedelta(days=6)
        for a in self.aktivnosti:
            datum_obj = a.datum_obj()
            if tjedan_samo and not (tjedan_pocetak <= datum_obj <= tjedan_kraj):
                continue
            if predmet_filter and a.predmet != predmet_filter:
                continue
            trajanje_po_predmetu[a.predmet] = trajanje_po_predmetu.get(a.predmet, 0) + a.trajanje
            ukupno += a.trajanje
        if not trajanje_po_predmetu:
            messagebox.showinfo("Info", "Nema aktivnosti za odabrani kriterij.")
            return
        tekst = "\n".join(f"{p}: {t} min" for p, t in trajanje_po_predmetu.items())
        tekst += f"\n\nUkupno: {ukupno} minuta"
        messagebox.showinfo("Ukupno trajanje", tekst)

    #-----------------
    # MENU
    def kreiraj_menu(self):
        menubar=tk.Menu(self.root)
        file_menu=tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Spremi XML",command=self.spremi_xml)
        file_menu.add_command(label="Učitaj XML",command=self.ucitaj_xml)
        file_menu.add_separator()
        file_menu.add_command(label="Izlaz", command=self.root.quit)
        menubar.add_cascade(label="Datoteka", menu=file_menu)

        tools_menu=tk.Menu(menubar, tearoff=0)
        tools_menu.add_command(label="Izračunaj ukupno vrijeme", command=self.izracun_ukupno)
        tools_menu.add_command(label="Ukupno za ovaj tjedan", command=lambda: self.izracun_ukupno(tjedan_samo=True))
        menubar.add_cascade(label="Alati", menu=tools_menu)

        help_menu=tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="O aplikaciji",command=self.prikazi_o_aplikaciji)
        menubar.add_cascade(label="Pomoć", menu=help_menu)

        self.root.config(menu=menubar)

    def statusna_traka(self):
        self.status_var= tk.StringVar()
        self.status_var.set("Spremno")
        status_bar=ttk.Label(self.root, textvariable=self.status_var, relief="sunken", anchor="w",
                               background="#2f3e46",foreground="#cad2c5", font=("Helvetica", 11))
        status_bar.grid(row=99, column=0, sticky="ew")

    def prikazi_o_aplikaciji(self):
        about=tk.Toplevel(self.root)
        about.title("O aplikaciji")
        about.geometry("350x350")
        about.resizable(False, False)
        about.configure(bg="#cad2c5")
        
        logo=tk.PhotoImage(file="LOGO.png")
        logo_label=tk.Label(about, image=logo, bg="#cad2c5")
        logo_label.image=logo
        logo_label.pack(pady=10)
        
        tk.Label(about, text="StudyList",font=("Helvetica", 18, "bold"), bg="#cad2c5").pack()
        tk.Label(about, text="Verzija 1.0", bg="#cad2c5").pack(pady=2)
        tk.Label(about, text="Autor: Lara Perković",bg="#cad2c5").pack(pady=2)
        tk.Label(about, text="Aplikacija za planiranje i praćenje učenja!", bg="#cad2c5",
                 wraplength=300, justify="center").pack(pady=10)
        
        ttk.Button(about, text="Zatvori", command=about.destroy).pack(pady=10)
        
        about.iconphoto(False, tk.PhotoImage(file="LOGO.png"))

if __name__=="__main__":
    root=tk.Tk()
    root.iconphoto(False, tk.PhotoImage(file="LOGO.png"))
    PlanerApp(root)
    root.mainloop()
