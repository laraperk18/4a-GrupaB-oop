import tkinter as tk 
from tkinter import messagebox, filedialog
import os 
from datetime import datetime

class vozilo:
    def __init__ (self,naziv,boja):
        self.naziv=naziv
        self.boja=boja
        
    def __str__(self):
        return f"Osnovno vozilo: {self.naziv}, Boja: {self.boja}"
    
class automobil(vozilo):
    def __init__ (self,naziv,boja,broj,broj_vrata):
        super().__init__(naziv,boja)
        self.broj_vrata= int(broj_vrata)
        
    def __str__(self):
        return f"Automobil: {self.naziv}, Boja: {self.boja}, Broj vrata: {self.broj_vrata}"
    
    def za_spremanje(self):
        return f"Automobil;{self.naziv};{self.boja};{self.broj_vrata}\n"
    
    
class bicikl(vozilo):
    def __init__ (self,naziv,boja):
        super().__init__(naziv,boja,ima_zvono):
        self.ima_zvono= ima_zvono
        
    def __str__(self):
        status = "ima" if self.ima_zvono else "nema"
        return f"Bicikl: {self.naziv}, Boja: {self.boja}, Ima zvono: {self.ima_zvono}"
    
    
class vozniParkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vozni Park evidencija 1.0")
        self.root.config(bg="pink")
        self.root.geometry("550x550")
        
        self.vozilo = []
        
        self,tip_vozila = tk.StringVar(value="Automobil")
        