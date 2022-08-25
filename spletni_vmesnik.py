import bottle
from model import Alineja, Poglavje, Predmet, Ucilnica

IME_DATOTEKE = "stanje.json"
try:
    ucilnica = Ucilnica.preberi_iz_datoteke(IME_DATOTEKE)
except FileNotFoundError:
    with open(IME_DATOTEKE, "w") as dat:
        ucilnica = Ucilnica("Učilnica", [])
        ucilnica.shrani_v_datoteko(IME_DATOTEKE)
        ucilnica = Ucilnica.preberi_iz_datoteke(IME_DATOTEKE)

def vstavi_sumnike(ime):
     return ime.replace("Ä\x8d","č").replace("Å¡","š").replace("Å¾","ž").replace("Ä\x8c","Č").replace("Å\xa0","Š").replace("Å½","Ž")

@bottle.get("/")
def zacetna_stran():
    return bottle.template("zacetna_stran.html", ucilnica=ucilnica) #spremenljivko poveze s pojmom ucilnica

@bottle.get("ime>/")
def pozdravi(ime):
    return f"<h1>Živjo, {ime}!</h1>"

@bottle.get("/<id_predmeta:int>/")
def stran_predmeta(id_predmeta):
    return bottle.template("stran_predmeta.html",ucilnica=ucilnica, predmet = ucilnica.seznam[id_predmeta], id_predmeta=id_predmeta)
        
@bottle.get("/<id_predmeta:int>/<id_poglavja:int>/")
def stran_poglavja(id_predmeta, id_poglavja):
        return bottle.template("stran_poglavja.html", ucilnica=ucilnica, predmet = ucilnica.seznam[id_predmeta], poglavje = ucilnica.seznam[id_predmeta].seznam[id_poglavja]) 
                
@bottle.get("/<id_predmeta:int>/<id_poglavja:int>/<id_alineje:int>/")
def pokazi_odgovor(id_predmeta, id_poglavja, id_alineje):
    return bottle.template("alineje.html", ucilnica=ucilnica, predmet = ucilnica.seznam[id_predmeta], poglavje = ucilnica.seznam[id_predmeta].seznam[id_poglavja], prikazana_alineja = ucilnica.seznam[id_predmeta].seznam[id_poglavja].seznam[id_alineje])
                        
@bottle.get("/<id_predmeta:int>/<id_poglavja:int>/<id_alineje:int>/znam/")
def znam(id_predmeta, id_poglavja, id_alineje):
    ucilnica.seznam[id_predmeta].seznam[id_poglavja].seznam[id_alineje].spremeni_stanje_opravljenega(True)
    ucilnica.shrani_v_datoteko(IME_DATOTEKE)
    path="/"+str(id_predmeta)+"/"+str(id_poglavja)+"/"
    bottle.redirect(path)
    
@bottle.get("/<id_predmeta:int>/<id_poglavja:int>/<id_alineje:int>/ne_znam/")
def ne_znam(id_predmeta, id_poglavja, id_alineje):
    ucilnica.seznam[id_predmeta].seznam[id_poglavja].seznam[id_alineje].spremeni_stanje_opravljenega(False)
    ucilnica.shrani_v_datoteko(IME_DATOTEKE)
    path="/"+str(id_predmeta)+"/"+str(id_poglavja)+"/"
    bottle.redirect(path)
    
@bottle.get("/<id_predmeta:int>/<id_poglavja:int>/<id_alineje:int>/izbrisi_alinejo/")
def izbrisi(id_predmeta, id_poglavja, id_alineje):
    pass
                    
@bottle.post("/<id_predmeta:int>/<id_poglavja:int>/dodaj_alinejo/")
def dodaj_alinejo(id_predmeta, id_poglavja):
    ime = bottle.request.forms["ime"]
    odgovor = bottle.request.forms["odgovor"]
    if ime !="" or odgovor !="":
        ime += "❌"
        ime = vstavi_sumnike(ime)
        ucilnica.seznam[id_predmeta].seznam[id_poglavja].dodaj(Alineja(ime, odgovor))
        ucilnica.shrani_v_datoteko(IME_DATOTEKE)
    path= "/"+str(id_predmeta)+"/"+str(id_poglavja)+"/"
    bottle.redirect(path)

@bottle.post("/<id_predmeta:int>/dodaj_poglavje/")
def dodaj_poglavje(id_predmeta):
    ime = bottle.request.forms["ime"]
    ime = vstavi_sumnike(ime)
    if ime !="":
        ucilnica.seznam[id_predmeta].dodaj(Poglavje(ime, []))
        ucilnica.shrani_v_datoteko(IME_DATOTEKE)
    path= "/"+str(id_predmeta)+"/"
    bottle.redirect(path)
 
@bottle.post("/dodaj_predmet/")
def dodaj_predmet():
    ime = bottle.request.forms["ime"]
    ime = vstavi_sumnike(ime)
    if ime !="":
        ucilnica.dodaj(Predmet(ime, []))
        ucilnica.shrani_v_datoteko(IME_DATOTEKE)
    path= "/"
    bottle.redirect(path)
    
@bottle.post("/<id_predmeta:int>/<id_poglavja:int>/preimenuj/")
def spremeni_ime_poglavja(id_predmeta, id_poglavja):
    novo_ime = vstavi_sumnike(bottle.request.forms["novo_ime"])
    if novo_ime !="":
        ucilnica.seznam[id_predmeta].seznam[id_poglavja].preimenuj(novo_ime)
        ucilnica.shrani_v_datoteko(IME_DATOTEKE)
    path= "/"+str(id_predmeta)+"/"+str(id_poglavja)+"/"
    bottle.redirect(path)

@bottle.post("/<id_predmeta:int>/preimenuj/")
def spremeni_ime_predmeta(id_predmeta):
    novo_ime = vstavi_sumnike(bottle.request.forms["novo_ime"])
    if novo_ime !="":
        ucilnica.seznam[id_predmeta].preimenuj(novo_ime)
        ucilnica.shrani_v_datoteko(IME_DATOTEKE)
    path= "/"+str(id_predmeta)+"/"
    bottle.redirect(path)
    
@bottle.post("/<id_predmeta:int>/preimenuj/")
def spremeni_ime_ucilnice():
    novo_ime = vstavi_sumnike(bottle.request.forms["novo_ime"])
    if novo_ime !="":
        ucilnica.preimenuj(novo_ime)
        ucilnica.shrani_v_datoteko(IME_DATOTEKE)
    path= "/"
    bottle.redirect(path)
    
# @bottle.get("/predmet/<ime_predmeta>/<ime_poglavja>/pokazi_vse_odgovore")
# def pokazi_vse_odgovore(ime_predmeta, ime_poglavja):
#     for predmet in ucilnica.seznam:
#             if ime_predmeta == predmet.ime:
#                 for poglavje in predmet.seznam:
#                     if ime_poglavja == poglavje.ime:
#                         for alineja in poglavje.seznam:
#                             alineja.pokazi_odgovor()
#                             return bottle.template("stran_poglavja.html", poglavje=poglavje, predmet = predmet)

bottle.run(debug=True, reloader=True) #če daš na javno spletno stran, potem debug izklopiš
