from model import Stanje, Predmet, Poglavje, Alineja
stanje = Stanje([
    Predmet(
        "Matematika",[
            Poglavje("Odvodi", [
                Alineja("vpr", "odgovor", False),
                Alineja("vpr2", "odg2", False)]),
            Poglavje("Integrali", [
                Alineja("vpr3", "odg3", False)])]),
    Predmet(
        "Slovenščina", [
            Poglavje("Renesansa", [
                Alineja("vpr4", "odg4", False)])]
        )]
)


#_______________________________________________________________________________________________________
def vpis():
    print("vpis")
    print("Živjo, izberi predmet:")
    izberi_predmet(stanje)
    

def registracija():
    print("registracija")

def izhod():
    print("Nasvidenje!")
    exit()
#_______________________________________________________________________________________________________
zacetne_moznosti = [(vpis, "vpis"), (registracija, "registracija"), (izhod, "izhod")]
def zacetni_pozdrav():
    print("Pozdravljeni!")

def ponudi_moznosti_za_seznam_zacetnih_moznosti(seznam_moznosti):
    for i, (funkcija, moznost) in enumerate(seznam_moznosti):
        print(f"{i+1}) {moznost}")
        
    while True:
        try:
            vhod = int(input(">"))
            if vhod <= 0:
                print(f"Vnesiti morate število med 1 in {len(seznam_moznosti)}.")
                continue
            (funkcija, moznost) = seznam_moznosti[vhod - 1]
            return funkcija
        except (ValueError, IndexError) as e:
            print(f"Vnesiti morate celo število med 1 in {len(seznam_moznosti)}.")
            
def ponudi_moznosti_za_normalen_seznam(seznam_moznosti):
    for i, ime in enumerate(seznam_moznosti):
        print(f"{i+1}) {ime}")
        
    while True:
        try:
            vhod = int(input(">"))
            if vhod <= 0:
                print(f"Vnesiti morate število med 1 in {len(seznam_moznosti)}.")
                continue
            return seznam_moznosti[vhod - 1]
        except (ValueError, IndexError) as e:
            print(f"Vnesiti morate celo število med 1 in {len(seznam_moznosti)}.")
#izbira_predmeta______________________________________________________________________________________________________             
def izberi_predmet(stanje):
    vsi_predmeti = []
    for predmet in stanje.seznam_predmetov:
        vsi_predmeti.append(predmet.ime_predmeta)
    
    izbran_predmet = ponudi_moznosti_za_normalen_seznam(vsi_predmeti)
    
    for predmet in stanje.seznam_predmetov:
        if predmet.ime_predmeta == izbran_predmet:
            seznam_poglavij_izbranega_predmeta = predmet.seznam_poglavij
            
    izberi_poglvje(seznam_poglavij_izbranega_predmeta)
#_____________________________________________________________________________________________________________________        

#izbira_poglavij______________________________________________________________________________________________________
def izberi_poglvje(seznam_poglavij):
    ponudi_moznosti_za_normalen_seznam(seznam_poglavij)
______________________________________________________________________________________________________________________
#tekstovni vmesnik____________________________________________________________________________________________________
def tekstovni_vmesnik():
    zacetni_pozdrav()
    ponudi_moznosti_za_seznam_zacetnih_moznosti(zacetne_moznosti)()

        
                
tekstovni_vmesnik()

    