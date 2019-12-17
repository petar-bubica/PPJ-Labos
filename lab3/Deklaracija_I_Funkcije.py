import config
import PomocneFunkcije
import Izrazi
import NaredbenaStruktura
from CvorStabla import CvorStabla
from CvorTablice import CvorTablice

#Nisam sig za ove postavi_tipove i to, provjeriti

def definicija_funkcije(cvor_stabla):
    return

def deklaracija_parametara(cvor_stabla):
    return

def lista_parametara(cvor_stabla):
    if len(cvor_stabla.lista_djece) == 1:
        if deklaracija_parametara(cvor_stabla.lista_djece[0]) == None:
            return
        cvor_stabla.postavi_tip(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
        cvor_stabla.dodaj_ime(cvor_stabla.lista_djece[0].vrati_ime()) #ili funkcija??
    if lista_parametara(cvor_stabla.lista_djece[0]) == None:
        return
    if deklaracija_parametara(cvor_stabla.lista_djece[2]) == None:
        return
    if cvor_stabla.lista_djece[2].ime in cvor_stabla.lista_djece[0].lista_imena:
        PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
        return
    cvor_stabla.lista_tipova = cvor_stabla.lista_djece[0].vrati_tipove(config.doseg)
    cvor_stabla.postavi_tip(cvor_stabla.lista_djece[2].vrati_tip(config.doseg))
    cvor_stabla.lista_imena = cvor_stabla.lista_djece[0].vrati_imena()
    cvor_stabla.dodaj_ime(cvor_stabla.lista_djece[2].vrati_ime())
    return


def lista_deklaracija(cvor_stabla):
    return


def deklaracija(cvor_stabla):
    return


def lista_init_deklaratora(cvor_stabla):
    return


def init_deklarator(cvor_stabla):
    return


def izravni_deklarator(cvor_stabla):
    return


def inicijalizator(cvor_stabla):
    return


def lista_izraza_pridruzivanja(cvor_stabla):
    return
