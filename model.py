class Ucilnica:
    def __init__(self, seznam): #seznam_predmetov
        self.seznam = seznam
        
    def dodaj_predmet(self, predmet):
        self.seznam.append(predmet)     

class Predmet:
    def __init__(self, ime, seznam): #ime_predmeta #seznam_poglavij
        self.ime = ime
        self.seznam = seznam
        
    def dodaj_poglavje(self, poglavje):
        self.seznam.append(poglavje)

class Poglavje:
    def __init__(self, ime, seznam): #ime_poglavja #seznam_alinej
        self.ime = ime
        self.seznam = seznam
        
    def dodaj_alinejo(self, alineja):
        self.seznam.append(alineja)

class Alineja:
    def __init__(self, vprasanje, odgovor, opravljeno):
        self.vprasanje = vprasanje
        self.odgovor = odgovor
        self.opravljeno = opravljeno
        
    def opravi(self):
        self.opravljeno = True
        
        

