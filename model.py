from os import remove


class Ucilnica:
    def __init__(self, ime, seznam): #seznam_predmetov
        self.ime = ime
        self.seznam = seznam
        
    def dodaj(self, predmet):
        self.seznam.append(predmet)    
        
    def izbrisi(self, predmet):
        self.seznam.remove(predmet) 

class Predmet:
    def __init__(self, ime, seznam): #ime_predmeta #seznam_poglavij
        self.ime = ime
        self.seznam = seznam
        
    def dodaj(self, poglavje):
        self.seznam.append(poglavje)
        
    def izbrisi(self, poglavje):
        self.seznam.remove(poglavje)

class Poglavje:
    def __init__(self, ime, seznam): #ime_poglavja #seznam_alinej
        self.ime = ime
        self.seznam = seznam
        
    def dodaj(self, alineja):
        self.seznam.append(alineja)
        
    def izbrisi(self, alineja):
        self.seznam.remove(alineja)

class Alineja:
    def __init__(self, ime, odgovor): #ime_alineje
        self.ime = ime
        self.odgovor = odgovor
    
    def spremeni_stanje_opravljenega(self, opravljeno):
        if opravljeno == False:
            self.ime = self.ime.replace("✅", "❌")
        if opravljeno == True:
            self.ime = self.ime.replace("❌", "✅")
        
    def opravi(self):
        self.opravljeno = True
        
        

