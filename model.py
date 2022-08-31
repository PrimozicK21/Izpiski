from dataclasses import dataclass
from os import remove
import json


# Ucilnica_______________________________________________________________
@dataclass
class Ucilnica:
    def __init__(self, ime, seznam): #seznam_predmetov
        self.ime = ime
        self.seznam = seznam
        
    def dodaj(self, predmet):
        self.seznam.append(predmet)    
        
    def izbrisi(self, predmet):
        self.seznam.remove(predmet)
    
    def preimenuj(self, novo_ime):
        self.ime = novo_ime
        
    def v_slovar(self):     
        return{
            "ime": self.ime,
            "seznam": [predmet.v_slovar() for predmet in self.seznam]
        }
        
    @staticmethod                           #to je funkcija
    def iz_slovarja(slovar):
        ucilnica = Ucilnica(
            slovar["ime"],
            [
                Predmet.iz_slovarja(slovar_predmetov)
                for slovar_predmetov in slovar["seznam"]
            ]
        )
        return ucilnica

    
    def shrani_v_datoteko(self, ime_datoteke):
        with open(ime_datoteke, "w", encoding="utf-8") as dat:
            slovar = self.v_slovar()
            json.dump(slovar, dat, indent=4, ensure_ascii=False)  #da je model lepo oblikovan (zavihki, šumniki)
            
    @staticmethod
    def preberi_iz_datoteke(ime_datoteke):
        with open(ime_datoteke, encoding="utf-8") as dat:
            slovar = json.load(dat)
            return Ucilnica.iz_slovarja(slovar)
        
# Predmet_______________________________________________________________
class Predmet:
    def __init__(self, ime, seznam): #ime_predmeta #seznam_poglavij
        self.ime = ime
        self.seznam = seznam
        
    def dodaj(self, poglavje):
        self.seznam.append(poglavje)
        
    def izbrisi(self, poglavje):
        self.seznam.remove(poglavje)
        
    def preimenuj(self, novo_ime):
        self.ime = novo_ime
        
        
    def v_slovar(self):
        return{
            "ime": self.ime,
            "seznam": [poglavje.v_slovar() for poglavje in self.seznam]
        }    

    @staticmethod
    def iz_slovarja(slovar):
        predmeti = Predmet(
            slovar["ime"],
            [
                Poglavje.iz_slovarja(slovar_poglavij)
                for slovar_poglavij in slovar["seznam"]
            ]
            )
        return predmeti
# Poglavje_______________________________________________________________
class Poglavje:
    def __init__(self, ime, seznam): #ime_poglavja #seznam_alinej
        self.ime = ime
        self.seznam = seznam
        
    def dodaj(self, alineja):
        self.seznam.append(alineja)
        
    def izbrisi(self, alineja):
        self.seznam.remove(alineja)
        
    def preimenuj(self, novo_ime):
        self.ime = novo_ime

    def v_slovar(self):
        return{
            "ime": self.ime,
            "seznam": [alineja.v_slovar() for alineja in self.seznam]
        }

    @staticmethod
    def iz_slovarja(slovar):
        poglavja = Poglavje(
            slovar["ime"],
            [
                Alineja.iz_slovarja(slovar_alinej)
                for slovar_alinej in slovar["seznam"]
            ]
        )
        return poglavja
# Alineja_______________________________________________________________    
class Alineja:
    def __init__(self, ime, odgovor): #ime_alineje = vprašanje
        self.ime = ime
        self.odgovor = odgovor
    
    def spremeni_stanje_opravljenega(self, opravljeno):
        if opravljeno == False:
            self.ime = self.ime.replace("✅", "❌")
        if opravljeno == True:
            self.ime = self.ime.replace("❌", "✅")
        
    def opravi(self):
        self.opravljeno = True
        
        
    def v_slovar(self):
        return{
            "ime": self.ime.replace("❌", "_krizec_").replace("✅", "_kljukica_"),
            "odgovor": self.odgovor
        }  
        
    @staticmethod
    def iz_slovarja(slovar):
        alineje = Alineja(
            slovar["ime"].replace("_krizec_", "❌").replace("_kljukica_", "✅"),
            slovar["odgovor"]
        )
        return alineje

