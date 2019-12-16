import config
import PomocneFunkcije
import Izrazi
import Deklaracija_I_Funkcije
from CvorStabla import CvorStabla
from CvorTablice import CvorTablice
#Nisam sig za ove postavi_tipove i to, provjeriti

def slozena_naredba(cvor_stabla):
    return


def lista_naredbi(cvor_stabla):
    if len(cvor_stabla.lista_djece) == 1:
       if naredba(cvor_stabla.lista_djece[0]) == None:
           return
    if lista_naredbi(cvor_stabla.lista_djece[0]) == None:
        return
    if naredba((cvor_stabla.lista_djece[1])) == None:
        return

    return


def naredba(cvor_stabla):
    return


def izraz_naredba(cvor_stabla):
    if len(cvor_stabla.lista_djece) == 1:
        cvor_stabla.tip = "int"
    else:
        if Izrazi.izraz(cvor_stabla.lista_djece[0]) == None:
            return
        cvor_stabla.tip = cvor_stabla.lista_djece[0].vrati_tip(config.doseg)
        cvor_stabla.lista_tipova = cvor_stabla.lista_djece[0].vrati_tipove(config.doseg)
        cvor_stabla.ime = cvor_stabla.lista_djece[0].vrati_ime()

    return


def naredba_grananja(cvor_stabla):
    return


def naredba_petlje(cvor_stabla):
    return


def naredba_skoka(cvor_stabla):
    return


def prijevodna_jedinica(cvor_stabla):
    if len(cvor_stabla.lista_djece) == 1:
        vanjska_deklaracija(cvor_stabla.lista_djece[0])
        if config.error:
            return
    else:
        prijevodna_jedinica(cvor_stabla.lista_djece[0])
        if config.error:
            return
        vanjska_deklaracija(cvor_stabla.lista_djece[1])
        if config.error:
            return
    return


def vanjska_deklaracija(cvor_stabla):
    if cvor_stabla.lista_djece[0].podaci == '<definicija_funkcije>':
        Deklaracija_I_Funkcije.definicija_funkcije(cvor_stabla.lista_djece[0])
        if config.error:
            return
    else:
        Deklaracija_I_Funkcije.deklaracija(cvor_stabla.lista_djece[0])
        if config.error:
            return
    return
