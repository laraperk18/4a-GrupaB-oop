class Zaposlenik:  #glavna klasa
    def __init__(self, ime, prezime, placa):
        self.ime = ime
        self.prezime = prezime
        self.placa = placa

    def prikazi_info(self):
        print(f"Ime i prezime: {self.ime} {self.prezime}, Plaća: {self.placa} EUR")


class Programer(Zaposlenik): #izvedena klasa Programer
    def __init__(self, ime, prezime, placa, programski_jezici):
        super().__init__(ime, prezime, placa)
        self.programski_jezici = programski_jezici

    def prikazi_info(self): 
        super().prikazi_info()
        print("Programski jezici:", ", ".join(self.programski_jezici))


class Menadzer(Zaposlenik): #izvedena klasa Menadzer
    def __init__(self, ime, prezime, placa, tim):
        super().__init__(ime, prezime, placa)
        self.tim = tim

    def prikazi_info(self):
        super().prikazi_info()
        print("Tim:", ", ".join(self.tim))

#bonus
    def dodaj_clana_tima(self, novi_clan):
        self.tim.append(novi_clan)
        print(f"{novi_clan} je dodan u tim!")
#test
z1 = Zaposlenik("Lara", "Perković", 1200)
p1 = Programer("Karla", "Matković", 1800, ["Python", "JavaScript"])
m1 = Menadzer("Aleksej", "Kurbasi", 2500, ["Lara Perković", "Karla Matković"])

print("--- Podaci o zaposleniku ---")
z1.prikazi_info()
print("--- Podaci o programeru ---")
p1.prikazi_info()
print("--- Podaci o menadzeru ---")
m1.prikazi_info()
    
print("\n--- Dodavanje novog člana tima ---")
m1.dodaj_clana_tima("Borna Lakoseljac")
m1.prikazi_info()
