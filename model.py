class Stanje:
    def __init__(self, seznam_predmetov):
        self.seznam_predmetov = seznam_predmetov
        
    def dodaj_predmet(self, predmet):
        self.seznam_predmetov.append(predmet)     

class Predmet:
    def __init__(self, ime_predmeta, seznam_poglavij):
        self.ime_predmeta = ime_predmeta
        self.seznam_poglavij = seznam_poglavij
        
    def dodaj_poglavje(self, poglavje):
        self.seznam_poglavij.append(poglavje)

class Poglavje:
    def __init__(self, ime_poglavja, seznam_alinej):
        self.ime_poglavja = ime_poglavja
        self.seznam_alinej = seznam_alinej
        
    def dodaj_alinejo(self, alineja):
        self.seznam_alinej.append(alineja)

class Alineja:
    def __init__(self, vprasanje, odgovor, opravljeno):
        self.vprasanje = vprasanje
        self.odgovor = odgovor
        self.opravljeno = opravljeno
        
    def opravi(self):
        self.opravljeno = True
        
        

