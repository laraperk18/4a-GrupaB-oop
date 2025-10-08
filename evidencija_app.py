import tkinter as tk
#0671B7
#67A3D9
#C8E7F5
#F6D2E0
#F8B7CD

class ucenik:
    def __init__(self, ime, prezime, razred):
        self.ime=ime
        self.prezime=prezime
        self.razred=razred

    def __str__(self):
        return f" {self.ime} {self.prezime} ({self.razred})"
class EvidencijaApp:
    def __init__(self, root):
        self.root=root
        self.ucenici=[]
        self.odabrani_ucenik_index=None

        
        self.root.title("Evidencija učenika")
        self.root.geometry("500x300")
        self.root.configure(bg="#F8B7CD")

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        unos_frame = tk.Frame(self.root, padx=10, pady=10,bg="#F8B7CD")
        unos_frame.grid(row=0, column=0, sticky="NS") 
        prikaz_frame = tk.Frame(self.root, padx=10, pady=10)
        prikaz_frame.grid(row=1, column=0, sticky="NSEW") 
        prikaz_frame.columnconfigure(0, weight=1)
        prikaz_frame.rowconfigure(0, weight=1)
# Ime
        tk.Label(unos_frame, text="Ime:",fg="#0671B7",bg="#F8B7CD").grid(row=0, column=0, padx=5, pady=5, sticky="W")
        self.ime_entry = tk.Entry(unos_frame)
        self.ime_entry.grid(row=0, column=1, padx=5, pady=5, sticky="EW")
# Prezime
        tk.Label(unos_frame, text="Prezime:",fg="#0671B7",bg="#F8B7CD").grid(row=1, column=0, padx=5, pady=5, sticky="W")
        self.prezime_entry = tk.Entry(unos_frame)
        self.prezime_entry.grid(row=1, column=1, padx=5, pady=5, sticky="EW")
# Razred
        tk.Label(unos_frame, text="Razred:",fg="#0671B7",bg="#F8B7CD").grid(row=2, column=0, padx=5, pady=5, sticky="W")
        self.razred_entry = tk.Entry(unos_frame)
        self.razred_entry.grid(row=2, column=1, padx=5, pady=5, sticky="EW")



        self.dodaj_gumb = tk.Button(unos_frame, text="Dodaj učenika",bg="#67A3D9",fg="white",command=self.dodaj_ucenika)
        self.dodaj_gumb.grid(row=3, column=0, padx=5, pady=10)
        self.spremi_gumb = tk.Button(unos_frame, text="Spremi izmjene",bg="#67A3D9",fg="white",command=self.spremi_izmjene)
        self.spremi_gumb.grid(row=3, column=1, padx=5, pady=10, sticky="W")

##dodatni zadatak
        self.dodaj_gumb = tk.Button(unos_frame, text="Spremi CSV",bg="#67A3D9",fg="white",command=self.dodaj_ucenika)
        self.dodaj_gumb.grid(row=4, column=0, padx=3, pady=10)
        self.dodaj_gumb = tk.Button(unos_frame, text="Učitaj CSV",bg="#67A3D9",fg="white",command=self.dodaj_ucenika)
        self.dodaj_gumb.grid(row=4, column=1, padx=1, pady=10)


        self.listbox = tk.Listbox(prikaz_frame)
        self.listbox.grid(row=0, column=0, sticky="NSEW")
        scrollbar = tk.Scrollbar(prikaz_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="NS")
        self.listbox.config(yscrollcommand=scrollbar.set)
        self.listbox.bind("<<ListboxSelect>>", self.odaberi_ucenika)##

    def dodaj_ucenika(self):
        if len(self.ime_entry.get())==0:
            print("nema ime")
        elif len(self.prezime_entry.get())==0:
            print("nema prezime")
        elif len(self.razred_entry.get())==0:
            print("nema razred")
        else:
            ucenikx=ucenik(self.ime_entry.get(),self.prezime_entry.get(),self.razred_entry.get())
            self.ucenici.append(ucenikx)
            self.osvjezi_prikaz()
            self.ime_entry.delete(0, tk.END)
            self.prezime_entry.delete(0, tk.END)
            self.razred_entry.delete(0, tk.END)
    def osvjezi_prikaz(self):
        self.listbox.delete(0, tk.END)
        for i in range(len(self.ucenici)):
            self.listbox.insert(tk.END, str(self.ucenici[i]))
    def odaberi_ucenika(self,event):###
        odabrani_indeksi = self.listbox.curselection()#
        if not odabrani_indeksi:
            return
        index=odabrani_indeksi[0]#
        self.odabrani_ucenik_index = index#
        ucenix = self.ucenici[index] #

        self.ime_entry.delete(0, tk.END)
        self.ime_entry.insert(0, ucenix.ime)

        self.prezime_entry.delete(0, tk.END)
        self.prezime_entry.insert(0, ucenix.prezime)

        self.razred_entry.delete(0, tk.END)
        self.razred_entry.insert(0, ucenix.razred)
        
    def spremi_izmjene(self):
        if self.odabrani_ucenik_index!=None:
            if len(self.ime_entry.get())==0:
                print("nema ime")
            elif len(self.prezime_entry.get())==0:
                print("nema prezime")
            elif len(self.razred_entry.get())==0:
                print("nema razred")
            else:
                ucenix=self.ucenici[self.odabrani_ucenik_index]
                ucenix.ime=self.ime_entry.get()
                ucenix.prezime=self.prezime_entry.get()
                ucenix.razred=self.razred_entry.get()
            
                self.osvjezi_prikaz()
            
                self.ime_entry.delete(0, tk.END)
                self.prezime_entry.delete(0, tk.END)
                self.razred_entry.delete(0, tk.END)
                self.odabrani_ucenik_index = None

root=tk.Tk()
app = EvidencijaApp(root)
