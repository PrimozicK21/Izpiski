import hashlib
import bottle
from model import Ucilnica, Predmet, Poglavje, Alineja
import os
import json
import time


SKRIVNOST = "sifrirani kljuc"
ucilnica = Ucilnica("Učilnica", [])
skrivna_datoteka = os.path.join("uporabniki", "gesla_in_uporabniki.json")

def ime_uporabnikove_datoteke(uporabnisko_ime):
    return f"uporabniki/{uporabnisko_ime}.json"

def ucilnica_trenutnega_uporabnika():
    uporabnisko_ime = bottle.request.get_cookie("uporabnisko_ime", secret = SKRIVNOST)
    if uporabnisko_ime == None:
        bottle.redirect("/prijava/")
    else:
        uporabnisko_ime = uporabnisko_ime
        ime_datoteke = ime_uporabnikove_datoteke(uporabnisko_ime)
    try:
        ucilnica = Ucilnica.preberi_iz_datoteke(ime_datoteke)
    except:
        bottle.redirect("/registracija/")
    return ucilnica


def zasifriraj_geslo(geslo, sol):
    sifrirano_geslo= ""
    for i in range(len(str(geslo))):
        sifrirano_geslo += str(geslo)[i] + str(geslo)[-i] + str(19872349)
    geslo = sifrirano_geslo
    
    return str(hashlib.pbkdf2_hmac(
        'sha256', # The hash digest algorithm for HMAC
        str(geslo).encode('utf-8'), # Convert the password to bytes
        sol, # Provide the salt
        100000 # It is recommended to use at least 100,000 iterations of SHA-256 
        ))



@bottle.get("/registracija/")
def stran_registracije():
    return bottle.template("registracija.html")

@bottle.post("/registracija/")
def gumb_registracija():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    geslo_v_cistopisu_1 = bottle.request.forms.getunicode("geslo1")
    geslo_v_cistopisu_2 = bottle.request.forms.getunicode("geslo2")
    
    cas = time.time()
    
    if geslo_v_cistopisu_1 != geslo_v_cistopisu_2:
        return bottle.template("registracija_obvestilo.html", obvestilo = "Gesli se ne ujemata")
    with open(skrivna_datoteka, encoding="utf-8") as dat:
        slovar = json.load(dat)
    if uporabnisko_ime in slovar:
        return bottle.template("registracija_obvestilo.html", obvestilo = "To ime je že uporabljeno. Poizkusite drugo!")
    else:
        slovar[uporabnisko_ime] = (zasifriraj_geslo(geslo_v_cistopisu_1, str(cas).encode("utf-8")), cas)
        # print(slovar)
        # print(skrivna_datoteka)
        with open(skrivna_datoteka, "w", encoding="utf-8") as dat:
            json.dump(slovar, dat, indent=4, ensure_ascii=False)
    bottle.response.set_cookie("uporabnisko_ime", uporabnisko_ime, path="/", secret=SKRIVNOST)
    ime_datoteke = ime_uporabnikove_datoteke(uporabnisko_ime)
    ucilnica = Ucilnica("Učilnica", [])
    ucilnica.shrani_v_datoteko(ime_datoteke)
    bottle.redirect("/ucilnica/")
    
@bottle.get("/prijava/")
def prijava_get():
    return bottle.template("prijava.html")


@bottle.post("/prijava/")
def prijava_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    geslo_v_cistopisu = bottle.request.forms.getunicode("geslo")
    with open(skrivna_datoteka, encoding="utf-8") as dat:
        slovar = json.load(dat)
        if uporabnisko_ime not in slovar:
            return bottle.template("prijava_obvestilo.html")
    print(f"{slovar[uporabnisko_ime]}")
    zasifrirano_geslo, cas = slovar[uporabnisko_ime]
    if zasifriraj_geslo(geslo_v_cistopisu, str(cas).encode("utf-8")) == zasifrirano_geslo:
        bottle.response.set_cookie("uporabnisko_ime", uporabnisko_ime, path="/", secret=SKRIVNOST)
        bottle.redirect("/ucilnica/")
    else:
        return bottle.template("prijava_obvestilo.html")
        
    
@bottle.get("/odjava/")
def odjava_post():
    print("sem tukaj1")
    bottle.response.delete_cookie("uporabnisko_ime", path="/")
    print("sem tukaj2")
    bottle.redirect("/")
    

# IME_DATOTEKE = "stanje.json"
# try:
#     ucilnica = Ucilnica.preberi_iz_datoteke(IME_DATOTEKE)
# except FileNotFoundError:
#     with open(IME_DATOTEKE, "w") as dat:
#         ucilnica = Ucilnica("Učilnica", [])
#         ucilnica.shrani_v_datoteko(IME_DATOTEKE)
#         ucilnica = Ucilnica.preberi_iz_datoteke(IME_DATOTEKE)
    
# @bottle.get("/<ime>/")
# def pozdravi(ime):
#     return f"<h1>Živjo, {ime}!</h1>
@bottle.get("/")
def ucilnica():
    uporabnisko_ime = bottle.request.get_cookie("uporabnisko_ime", secret = SKRIVNOST)
    if uporabnisko_ime == None:
        bottle.redirect("/prijava/")
    else:
        bottle.redirect("/ucilnica/")
        
@bottle.get("/ucilnica/")
def stran_ucilnice():
    ucilnica = ucilnica_trenutnega_uporabnika()
    try:
        return bottle.template("ucilnica.html", ucilnica=ucilnica)
    except AttributeError:
        uporabnisko_ime = bottle.request.get_cookie("uporabnisko_ime", secret=SKRIVNOST)
        ime_datoteke = ime_uporabnikove_datoteke(uporabnisko_ime)
        return ucilnica.preberi_iz_datoteke(ime_datoteke)

@bottle.get("/<id_predmeta:int>/")
def stran_predmeta(id_predmeta):
    ucilnica = ucilnica_trenutnega_uporabnika()
    return bottle.template("stran_predmeta.html",ucilnica=ucilnica, predmet = ucilnica.seznam[id_predmeta], id_predmeta=id_predmeta)
        
@bottle.get("/<id_predmeta:int>/<id_poglavja:int>/")
def stran_poglavja(id_predmeta, id_poglavja):
    ucilnica = ucilnica_trenutnega_uporabnika()
    return bottle.template("stran_poglavja.html", ucilnica=ucilnica, predmet = ucilnica.seznam[id_predmeta], poglavje = ucilnica.seznam[id_predmeta].seznam[id_poglavja]) 
                
@bottle.get("/<id_predmeta:int>/<id_poglavja:int>/<id_alineje:int>/")
def pokazi_odgovor(id_predmeta, id_poglavja, id_alineje):
    ucilnica = ucilnica_trenutnega_uporabnika()
    return bottle.template("alineje.html", ucilnica=ucilnica, predmet = ucilnica.seznam[id_predmeta], poglavje = ucilnica.seznam[id_predmeta].seznam[id_poglavja], prikazana_alineja = ucilnica.seznam[id_predmeta].seznam[id_poglavja].seznam[id_alineje])
                        
@bottle.get("/<id_predmeta:int>/<id_poglavja:int>/<id_alineje:int>/znam/")
def znam(id_predmeta, id_poglavja, id_alineje):
    uporabnisko_ime = bottle.request.get_cookie("uporabnisko_ime", secret = SKRIVNOST)
    ime_datoteke = ime_uporabnikove_datoteke(uporabnisko_ime)
    ucilnica = ucilnica_trenutnega_uporabnika()
    ucilnica.seznam[id_predmeta].seznam[id_poglavja].seznam[id_alineje].spremeni_stanje_opravljenega(True)
    ucilnica.shrani_v_datoteko(ime_datoteke)
    path="/"+str(id_predmeta)+"/"+str(id_poglavja)+"/"
    bottle.redirect(path)
    
@bottle.get("/<id_predmeta:int>/<id_poglavja:int>/<id_alineje:int>/ne_znam/")
def ne_znam(id_predmeta, id_poglavja, id_alineje):
    uporabnisko_ime = bottle.request.get_cookie("uporabnisko_ime", secret = SKRIVNOST)
    ime_datoteke = ime_uporabnikove_datoteke(uporabnisko_ime)
    ucilnica = ucilnica_trenutnega_uporabnika()
    ucilnica.seznam[id_predmeta].seznam[id_poglavja].seznam[id_alineje].spremeni_stanje_opravljenega(False)
    ucilnica.shrani_v_datoteko(ime_datoteke)
    path="/"+str(id_predmeta)+"/"+str(id_poglavja)+"/"
    bottle.redirect(path)
    
@bottle.get("/<id_predmeta:int>/<id_poglavja:int>/<id_alineje:int>/izbrisi_alinejo/")
def izbrisi_alinejo(id_predmeta, id_poglavja, id_alineje):
    uporabnisko_ime = bottle.request.get_cookie("uporabnisko_ime", secret = SKRIVNOST)
    ime_datoteke = ime_uporabnikove_datoteke(uporabnisko_ime)
    ucilnica = ucilnica_trenutnega_uporabnika()
    ucilnica.seznam[id_predmeta].seznam[id_poglavja].seznam.remove(ucilnica.seznam[id_predmeta].seznam[id_poglavja].seznam[id_alineje])
    ucilnica.shrani_v_datoteko(ime_datoteke)
    path= "/"+str(id_predmeta)+"/"+str(id_poglavja)+"/"
    bottle.redirect(path)
    
@bottle.get("/<id_predmeta:int>/<id_poglavja:int>/izbrisi_poglavje/")
def izbrisi_poglavje(id_predmeta, id_poglavja):
    uporabnisko_ime = bottle.request.get_cookie("uporabnisko_ime", secret = SKRIVNOST)
    ime_datoteke = ime_uporabnikove_datoteke(uporabnisko_ime)
    ucilnica = ucilnica_trenutnega_uporabnika()
    ucilnica.seznam[id_predmeta].seznam.remove(ucilnica.seznam[id_predmeta].seznam[id_poglavja])
    ucilnica.shrani_v_datoteko(ime_datoteke)
    path= "/"+str(id_predmeta)+"/"
    bottle.redirect(path)
    
@bottle.get("/<id_predmeta:int>/izbrisi_predmet/")
def izbrisi_predmet(id_predmeta):
    uporabnisko_ime = bottle.request.get_cookie("uporabnisko_ime", secret = SKRIVNOST)
    ime_datoteke = ime_uporabnikove_datoteke(uporabnisko_ime)
    ucilnica = ucilnica_trenutnega_uporabnika()
    ucilnica.seznam.remove(ucilnica.seznam[id_predmeta])
    ucilnica.shrani_v_datoteko(ime_datoteke)
    path= "/"
    bottle.redirect(path)
                        
@bottle.post("/<id_predmeta:int>/<id_poglavja:int>/dodaj_alinejo/")
def dodaj_alinejo(id_predmeta, id_poglavja):
    uporabnisko_ime = bottle.request.get_cookie("uporabnisko_ime", secret = SKRIVNOST)
    ime_datoteke = ime_uporabnikove_datoteke(uporabnisko_ime)
    ucilnica = ucilnica_trenutnega_uporabnika()
    ime = bottle.request.forms.getunicode("ime")
    odgovor = bottle.request.forms.getunicode("odgovor")
    if ime !="" or odgovor !="":
        ime = "❌" + ime
        ucilnica.seznam[id_predmeta].seznam[id_poglavja].dodaj(Alineja(ime, odgovor))
        ucilnica.shrani_v_datoteko(ime_datoteke)
    path= "/"+str(id_predmeta)+"/"+str(id_poglavja)+"/"
    bottle.redirect(path)

@bottle.post("/<id_predmeta:int>/dodaj_poglavje/")
def dodaj_poglavje(id_predmeta):
    uporabnisko_ime = bottle.request.get_cookie("uporabnisko_ime", secret = SKRIVNOST)
    ime_datoteke = ime_uporabnikove_datoteke(uporabnisko_ime)
    ucilnica = ucilnica_trenutnega_uporabnika()
    ime = bottle.request.forms.getunicode("ime")

    if ime !="":
        ucilnica.seznam[id_predmeta].dodaj(Poglavje(ime, []))
        ucilnica.shrani_v_datoteko(ime_datoteke)
    path= "/"+str(id_predmeta)+"/"
    bottle.redirect(path)
 
@bottle.post("/dodaj_predmet/")
def dodaj_predmet():
    uporabnisko_ime = bottle.request.get_cookie("uporabnisko_ime", secret = SKRIVNOST)
    ime_datoteke = ime_uporabnikove_datoteke(uporabnisko_ime)
    ucilnica = ucilnica_trenutnega_uporabnika()
    ime = bottle.request.forms.getunicode("ime")
    if ime !="":
        ucilnica.dodaj(Predmet(ime, []))
        ucilnica.shrani_v_datoteko(ime_datoteke)
    path= "/"
    bottle.redirect(path)
    
@bottle.post("/<id_predmeta:int>/<id_poglavja:int>/preimenuj/")
def spremeni_ime_poglavja(id_predmeta, id_poglavja):
    uporabnisko_ime = bottle.request.get_cookie("uporabnisko_ime", secret = SKRIVNOST)
    ime_datoteke = ime_uporabnikove_datoteke(uporabnisko_ime)
    ucilnica = ucilnica_trenutnega_uporabnika()
    novo_ime = bottle.request.forms.getunicode("novo_ime")
    if novo_ime !="":
        ucilnica.seznam[id_predmeta].seznam[id_poglavja].preimenuj(novo_ime)
        ucilnica.shrani_v_datoteko(ime_datoteke)
    path= "/"+str(id_predmeta)+"/"+str(id_poglavja)+"/"
    bottle.redirect(path)

@bottle.post("/<id_predmeta:int>/preimenuj/")
def spremeni_ime_predmeta(id_predmeta):
    uporabnisko_ime = bottle.request.get_cookie("uporabnisko_ime", secret = SKRIVNOST)
    ime_datoteke = ime_uporabnikove_datoteke(uporabnisko_ime)
    ucilnica = ucilnica_trenutnega_uporabnika()
    novo_ime = bottle.request.forms.getunicode("novo_ime")
    if novo_ime !="":
        ucilnica.seznam[id_predmeta].preimenuj(novo_ime)
        ucilnica.shrani_v_datoteko(ime_datoteke)
    path= "/"+str(id_predmeta)+"/"
    bottle.redirect(path)
    
@bottle.post("/<id_predmeta:int>/preimenuj/")
def spremeni_ime_ucilnice():
    uporabnisko_ime = bottle.request.get_cookie("uporabnisko_ime", secret = SKRIVNOST)
    ime_datoteke = ime_uporabnikove_datoteke(uporabnisko_ime)
    ucilnica = ucilnica_trenutnega_uporabnika()
    novo_ime = bottle.request.forms.getunicode("novo_ime")
    if novo_ime !="":
        ucilnica.preimenuj(novo_ime)
        ucilnica.shrani_v_datoteko(ime_datoteke)
    path= "/"
    bottle.redirect(path)
    


@bottle.get("/style.css")
def slog():
    return bottle.static_file("style.css", root="views")

@bottle.get("/normalize.css")
def slog():
    return bottle.static_file("normalize.css", root="views")




    
bottle.run(debug=True, reloader=True) #če daš na javno spletno stran, potem debug izklopiš

