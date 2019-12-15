import config
import PomocneFunkcije
import NaredbenaStruktura
import Deklaracija_I_Funkcije
from CvorStabla import CvorStabla
from CvorTablice import CvorTablice


def primarni_izraz(cvor_stabla):
    cvor = cvor_stabla.lista_djece[0]
    
    if cvor.podaci.startswith('IDN'):
        if PomocneFunkcije.je_vec_deklarirano(cvor.vrati_ime()):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return

        cvor_stabla.tip = cvor.vrati_tip(config.doseg)
        cvor_stabla.lista_tipova = cvor.vrati_tipove(config.doseg)
        cvor_stabla.ime = cvor.vrati_ime()
        cvor_stabla.je_l_vrijednost = cvor.vrati_l_vrijednost(config.doseg)

    if cvor.podaci.startswith('BROJ'):
        if not PomocneFunkcije.je_integer(cvor.vrati_ime()):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        
        cvor_stabla.postavi_tip('int')
        cvor_stabla.je_l_vrijednost = False

    if cvor.podaci.startswith('ZNAK'):
        if not PomocneFunkcije.je_char(cvor.vrati_ime()):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        
        cvor_stabla.postavi_tip('char')
        cvor_stabla.je_l_vrijednost = False

    if cvor.podaci.startswith('NIZ_ZNAKOVA'):
        if not PomocneFunkcije.je_string(cvor.vrati_ime()):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        
        cvor_stabla.postavi_tip('nizchar')
        cvor_stabla.je_konstanta = True
        cvor_stabla.je_l_vrijednost = False

    if cvor.podaci.startswith('L_ZAGRADA'):
        
        izraz(cvor_stabla.lista_djece[1])
        if config.error:
            return

        cvor_stabla.postavi_tip(cvor_stabla.lista_djece[1].vrati_tip(config.doseg))
        cvor_stabla.je_l_vrijednost = cvor_stabla.lista_djece[1].vrati_l_vrijednost(config.doseg)

    return


def postfiks_izraz(cvor_stabla):
    return


def lista_argumenata(cvor_stabla):
    return


def unarni_izraz(cvor_stabla):
    return


def unarni_operator(cvor_stabla):
    return


def cast_izraz(cvor_stabla):
    return


def ime_tipa(cvor_stabla):
    return


def specifikator_tipa(cvor_stabla):
    return


def multiplikativni_izraz(cvor_stabla):
    return


def aditivni_izraz(cvor_stabla):
    return


def odnosni_izraz(cvor_stabla):
    return


def jednakosni_izraz(cvor_stabla):
    return


def bin_i_izraz(cvor_stabla):
    return


def bin_xili_izraz(cvor_stabla):
    return


def bin_ili_izraz(cvor_stabla):
    return


def log_i_izraz(cvor_stabla):
    return


def log_ili_izraz(cvor_stabla):
    return


def izraz_pridruzivanja(cvor_stabla):
    return


def izraz(cvor_stabla):
    return