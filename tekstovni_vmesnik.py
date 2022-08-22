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

def vpis():
    print("vpis")

def registracija():
    print("registracija")

def izhod():
    print("Nasvidenje!")
    exit()

zacetne_moznosti = [(vpis, "vpis"), (registracija, "registracija"), (izhod, "izhod")]
def zacetni_pozdrav():
    print("Pozdravljeni!")

def ponudi_moznosti(seznam_moznosti):
    for i, (funkcija, moznost) in enumerate(seznam_moznosti):
        print(f"{i+1}) {moznost}")
        
    while True:
        try:
            vhod = int(input(">"))
            if vhod <= 0:
                print(f"Vnesiti morate število med 1 in {len(seznam_moznosti)}.")
                continue
            (funkcija, ime_funkcija) = seznam_moznosti[vhod - 1]
            return funkcija
        except (ValueError, IndexError) as e:
            print(f"Vnesiti morate celo število med 1 in {len(seznam_moznosti)}.")
              
def izberi_predmet(stanje):
    vsi_predmeti = []
    for predmet in stanje.seznam_predmetov:
        vsi_predmeti.append(predmet.ime_predmeta)
        
        ponudi_moznosti(vsi_predmeti)

def tekstovni_vmesnik():
    zacetni_pozdrav()
    ponudi_moznosti(zacetne_moznosti)()
    
    
tekstovni_vmesnik()

    