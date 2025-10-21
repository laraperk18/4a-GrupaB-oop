import tkinter as tk
import csv
class Kontakt:
    def __init__(self, ime, email, broj_telefona):
        self.ime=ime
        self.email=email
        self.broj=broj_telefona
    def __str__(self):
        return f"{self.ime} - {self.email} - {self.broj}"
class ImenikApp:
    def __init__(self,root):
        self.root=root
        self.kontakti=[]
        self.odabrani_kontakt_index=None
        
        self.root.title("Kontakti")
        self.root.geometry("500x300")
        self.root.configure(bg="#F8B7CD")

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        unos_frame = tk.Frame(self.root, padx=10, pady=10,bg="#F8B7CD")
        unos_frame.grid(row=0, column=0, sticky="EW") 
        prikaz_frame = tk.Frame(self.root, padx=10, pady=10, bg="#F8B7CD")
        prikaz_frame.grid(row=1, column=0, sticky="NSEW")
        prikaz_frame.columnconfigure(0, weight=1)
        prikaz_frame.rowconfigure(1, weight=1)

        #unso

        tk.Label(unos_frame, text="Ime:",fg="#0671B7",bg="#F8B7CD").grid(row=0, column=0, padx=5, pady=5, sticky="W")
        self.ime_entry = tk.Entry(unos_frame)
        self.ime_entry.grid(row=0, column=1, padx=5, pady=5, sticky="EW")

        tk.Label(unos_frame, text="Email:",fg="#0671B7",bg="#F8B7CD").grid(row=1, column=0, padx=5, pady=5, sticky="W")
        self.email_entry = tk.Entry(unos_frame)
        self.email_entry.grid(row=1, column=1, padx=5, pady=5, sticky="EW")

        tk.Label(unos_frame, text="Broj telefona:",fg="#0671B7",bg="#F8B7CD").grid(row=2, column=0, padx=5, pady=5, sticky="W")
        self.broj_entry = tk.Entry(unos_frame)
        self.broj_entry.grid(row=2, column=1, padx=5, pady=5, sticky="EW")

        #listbox
        self.listbox = tk.Listbox(prikaz_frame)
        self.listbox.grid(row=1, column=0, sticky="NSEW")
        scrollbar = tk.Scrollbar(prikaz_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.grid(row=1, column=1, sticky="NS")
        self.listbox.config(yscrollcommand=scrollbar.set)
        ##self.listbox.bind("<<ListboxSelect>>", self.odaberi_ucenika)
        #gumb
        self.dodaj_gumb = tk.Button(prikaz_frame, text="Dodaj kontakt", bg="#67A3D9", fg="white",command=self.dodavanje_kontakta)
        self.dodaj_gumb.grid(row=0, column=0, padx=5, pady=10, sticky="W")
        self.obrisi_gumb = tk.Button(prikaz_frame, text="Obriši kontakt", bg="#F6D2E0", fg="white", command=self.obrisi_kontakt)
        self.obrisi_gumb.grid(row=0, column=1, padx=5, pady=5, sticky="E")

        
        self.spremi_gumb = tk.Button(prikaz_frame, text="Spremi kontakte", bg="#67A3D9", fg="white",command=self.spremi_u_csv)
        self.spremi_gumb.grid(row=2, column=0, padx=5, pady=10, sticky="W")
        self.ucitaj_gumb = tk.Button(prikaz_frame, text="Učitaj kontakte", bg="#67A3D9", fg="white",command=self.ucitaj_iz_csv)
        self.ucitaj_gumb.grid(row=2, column=1, padx=5, pady=10, sticky="E")


##funkcija
        self.ucitaj_iz_csv()
        
        
    def dodavanje_kontakta(self):
            if len(self.ime_entry.get())==0:
                print("nema ime")
            elif len(self.ime_entry.get()) < 3:
                print("ime mora imati najmanje 3 slova")
            elif len(self.email_entry.get())==0:
                print("nema emaila")
            elif not (self.email_entry.get().endswith("@gmail.com") or email.endswith("@skole.hr") or email.endswith("@hotmail.com")):
                print("Email mora biti na @gmail.com, @skole.hr ili @hotmail.com")
            elif len(self.broj_entry.get())==0:
                print("nema broja")
            else:
                kontaktA=Kontakt(self.ime_entry.get(),self.email_entry.get(),self.broj_entry.get())
                self.kontakti.append(kontaktA)
                self.osvjezi_prikaz()
                self.ime_entry.delete(0, tk.END)
                self.email_entry.delete(0, tk.END)
                self.broj_entry.delete(0, tk.END)
    def osvjezi_prikaz(self):
            self.listbox.delete(0, tk.END)
            for i in range(len(self.kontakti)):
                self.listbox.insert(tk.END, str(self.kontakti[i]))
    def spremi_u_csv(self):
            if len(self.kontakti)==0:
                return
            with open("kontakti.csv",mode="w",newline="",encoding="utf-8")as datoteka:
                polja = ['ime', 'email', 'broj']
                writer = csv.DictWriter(datoteka, fieldnames=polja)
                writer.writeheader()
                for i in range (len(self.kontakti)):
                    k=self.kontakti[i]
                    writer.writerow({'ime': k.ime, 'email': k.email, 'broj': k.broj})
            print(f"Spremljeno u kontakti.csv")

    def ucitaj_iz_csv(self):
        try:
            with open("kontakti.csv", mode="r", encoding="utf-8") as datoteka:
                reader = csv.DictReader(datoteka)
                self.kontakti = []
                self.kontakti = [Kontakt(r['ime'], r['email'], r['broj']) for r in reader]
            self.osvjezi_prikaz()
            print("Podaci su uspjesno ucitani")
        except FileNotFoundError:
            print("Datoteka kontakti.csv ne postoji učitavanje preskočeno.")

    def obrisi_kontakt(self):
        odabir = self.listbox.curselection()
        if odabir:
            index = odabir[0]
            self.kontakti.pop(index)
            self.osvjezi_prikaz()
            print("Kontakt obrisan")
        else:
            print("Nema odabranog kontakta za brisanje")
    
      
root=tk.Tk()
app = ImenikApp(root)    
    
