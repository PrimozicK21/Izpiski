from model import Ucilnica, Predmet, Poglavje, Alineja

ucilnica = Ucilnica([
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


#zacetne funkcije_______________________________________________________________________________________________________
def vpis():
    print("vpis")
    #izberi_iz_razreda(ucilnica)
    
def je_vpisan():
    return True
    
def zacetni_pozdrav():
    print("Pozdravljeni!")

def registracija():
    print("registracija")

def izhod():
    print("Nasvidenje!")
    exit()
    

#ponudi_moznosti_______________________________________________________________________________________________________
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

#tip_razreda = ["predmet", "poglavje", "alineja"]
# izbire______________________________________________________________________________________________________             
def izberi_iz_razreda(razred, tip_razreda):
    if razred == None:
        seznam_moznosti = ["dodaj", "Nazaj"]
        izbran_element = ponudi_moznosti_za_normalen_seznam(seznam_iz_razreda)
        if izbran_element == "dodaj":
            if tip_razreda == "poglavje":
                poglavje = dodaj_poglavje(razred)
    #elementi_v_seznam-----------------------------------------------------------
    seznam_iz_razreda = []
    for element_seznama in razred.seznam:
        seznam_iz_razreda.append(element_seznama.ime)
    #dodaj = "dodaj" + tip_razreda
    seznam_iz_razreda.append("dodaj")
    seznam_iz_razreda.append("nazaj")
    
    izbran_element = ponudi_moznosti_za_normalen_seznam(seznam_iz_razreda)
    
    
    #nadaljuj_po_okenckih-------------------------------------------------
    for element_seznama in razred.seznam:
        if element_seznama.ime == izbran_element:
            if tip_razreda == "predmet":
                return izberi_iz_razreda(element_seznama, "poglavje")
            if tip_razreda == "poglavje":
                return izberi_iz_razreda(element_seznama, "alineja")
            if tip_razreda == "alineja":
                print(element_seznama.odgovor)
                return element_seznama.odgovor
    
    #posebne_izbire-----------------------------------------------------   
    if izbran_element == "dodaj":
        if tip_razreda == "predmet":
            predmet = dodaj_predmet()
            return izberi_iz_razreda(predmet, "poglavje")
        if tip_razreda == "poglavje":
            poglavje = dodaj_poglavje(razred)
            return izberi_iz_razreda(poglavje, "alineja")
        if tip_razreda == "alineja":
            print("Alineja dodana")
            return izberi_iz_razreda(element_seznama, "alineja")
    #nazaj--------------------------------------------------------------    
    elif izbran_element == "nazaj":
        if tip_razreda == "predmet":
            return exit()
        elif tip_razreda == "poglavje":
            return izberi_iz_razreda(ucilnica, "predmet")
        elif tip_razreda == "alineja":
            for predmet in ucilnica.seznam:
                if razred in predmet.seznam:                                #razred = poglavje
                    return izberi_iz_razreda(predmet, "poglavje")
        
    #ce_se_zgodi_prazen_razred------------------------------------------
    seznam_moznosti = ["dodaj", "nazaj"]
    drugi_izbran_element = ponudi_moznosti_za_normalen_seznam(seznam_iz_razreda)
    if izbran_element == "dodaj":
        if tip_razreda == "predmet":
            poglavje = dodaj_poglavje(izbran_element)
            izberi_iz_razreda(poglavje, "alineje")
                    
#dodaj_____________________________________________________________________________________________________________________        
def dodaj_predmet():
    ime_predmeta = input("Ime predmeta: ")
    predmet = Predmet(ime_predmeta, [])
    #dodaj_poglavje()
    ucilnica.dodaj(predmet)
    return predmet

def dodaj_poglavje(razred):
    ime_poglavja = input("Ime poglavja: ")
    poglavje = Poglavje(ime_poglavja, [])
    
    razred.dodaj(poglavje)
    return poglavje

def dodaj_alinejo(poglavje):
    vprasanje = input("Vprasanje: ")
    odgovor = input("Odgovor: ")
    alineja = Alineja(vprasanje, odgovor, False)
    poglavje.dodaj(alineja)
    return alineja

#nazaj_____________________________________________________________________________________________________________
def nazaj(razred):
    pass




#tekstovni vmesnik____________________________________________________________________________________________________
zacetne_moznosti = [(vpis, "vpis"), (registracija, "registracija"), (izhod, "izhod")]

def tekstovni_vmesnik():
    zacetni_pozdrav()
    #vpisan = False
    ponudi_moznosti_za_seznam_zacetnih_moznosti(zacetne_moznosti)()
    izberi_iz_razreda(ucilnica, "predmet")
    # poglavje = izberi_iz_razreda(predmet, "poglavje")
    # alineja = izberi_iz_razreda(poglavje, "alineja")
    # odg = alineja.odgovor
    # print(odg)  



                
tekstovni_vmesnik()

    