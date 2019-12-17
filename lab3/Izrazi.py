import config
import PomocneFunkcije
import NaredbenaStruktura
import Deklaracija_I_Funkcije
from CvorStabla import CvorStabla
from CvorTablice import CvorTablice

#Nisam sig za ove postavi_tipove i to, provjeriti
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
    cvor = cvor_stabla.lista_djece[0]

    if cvor.podaci.startswith('<primarni_izraz>'):
        
        primarni_izraz(cvor)
        if config.error:
            return

        ..

    return


def lista_argumenata(cvor_stabla):
    if len(cvor_stabla.lista_djece) == 1:
        izraz_pridruzivanja(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.postavi_tip(cvor_stabla.lista_tipova[0].vrati_tip(config.doseg))
    else:
        Deklaracija_I_Funkcije.lista_argumenata(cvor_stabla.lista_djece[0])
        if config.error:
            return
        izraz_pridruzivanja(cvor_stabla.lista_djece[2])
        if config.error:
                return

        cvor_stabla.lista_tipova = cvor_stabla.lista_djece[0].vrati_tipove(config.doseg)
        cvor_stabla.tip = cvor_stabla.listadjece[2].vrati_tip(config.doseg)
    return


def unarni_izraz(cvor_stabla):
    if cvor_stabla.lista_djece.len() == 1:
        postfiks_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.tip = cvor_stabla.lista_djece[0].vrati_tip(config.doseg)
        cvor_stabla.lista_tipova = cvor_stabla.lista_djece[0].vrati_tipove(config.doseg)
        cvor_stabla.ime = cvor_stabla.lista_djece[0].vrati_ime()
        cvor_stabla.je_l_vrijednost = cvor_stabla.lista_djece[0].vrati_l_vrijednost(config.doseg)
    elif cvor_stabla.lista_djece[1] == "<unarni_izraz>":
        unarni_izraz(cvor_stabla.lista_djece[1])
        if config.error:
            return
        if not cvor_stabla.lista_djece[1].vrati_l_vrijednost(config.doseg) or not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[1].vrati_tip(config.doseg), "int"):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        cvor_stabla.tip = "int"
        cvor_stabla.je_l_vrijednost = False
    else:
        cast_izraz(cvor_stabla.lista_djece[1])
        if config.error:
            return
        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[1].vrati_tip(config.doseg), "int"):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        cvor_stabla.tip = "int"
        cvor_stabla.je_l_vrijednost = False
    return


def cast_izraz(cvor_stabla):
    if cvor_stabla.lista_djece.len() == 1:
        unarni_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.tip = cvor_stabla.lista_djece[0].vrati_ime(config.doseg)
        cvor_stabla.tipovi = cvor_stabla.lista_djece[0].vrati_tipove(config.doseg)
        cvor_stabla.ime = cvor_stabla.lista_djece[0].vrati_ime
        cvor_stabla.je_l_vrijednost = cvor_stabla.lista_djece[0].vrati_l_vrijednost(config.doseg)
    else:
        ime_tipa(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cast_izraz(cvor_stabla.lista_djece[3])
        if config.error:
            return
        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[3].vrati_tip(config.doseg), cvor_stabla.lista_djece[1].vrati_tip(config.scope)) and not cvor_stabla.lista_djece[3].vrati_tip(config.doseg) == "int" and cvor_stabla.lista_djece[1].vrati_tip(config.doseg) == "char" or cvor_stabla.lista_djece[3].isFunction() or cvor_stabla.lista_djece[1].je_funkcija():
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        cvor_stabla.tip = cvor_stabla.lista_djece[1].vrati_tip(config.doseg)
        cvor_stabla.je_l_vrijednost = False
    return


def ime_tipa(cvor_stabla):
    if len(cvor_stabla.lista_djece) == 1:
        specifikator_tipa(cvor_stabla.lista_djece[0])
        cvor_stabla.tip = cvor_stabla.lista_djece[0].vrati_tip(config.doseg)
    else:
        specifikator_tipa(cvor_stabla.lista_djece[1])
        if (cvor_stabla.lista_djece[1]).vrati_tip(config.doseg) == "void":
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        cvor_stabla.tip = cvor_stabla.lista_djece[1].vrati_tip(config.doseg)
        cvor_stabla.je_konstanta = True
    return

def specifikator_tipa(cvor_stabla):
    cvor = cvor_stabla.lista_djece[0]
    if cvor.podaci.startswith("KR VOID"):
        cvor_stabla.tip = "void"
    if cvor.podaci.startswith("KR CHAR"):
        cvor_stabla.tip = "char"
    if cvor.podaci.startswith("KR INT"):
        cvor_stabla.tip = "int"
    return


def multiplikativni_izraz(cvor_stabla):
    if cvor_stabla.lista_djece.len() == 1:
        cast_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.tip = cvor_stabla.lista_djece[0].vrati_tip(config.doseg)
        cvor_stabla.je_l_vrijednost(cvor_stabla.lista_djece[0].vrati_l_vrijednost(config.doseg))
    else:
        multiplikativni_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[0].vrati_tip(config.doseg), "int"):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        cast_izraz(cvor_stabla.lista_djece[2]);
        if config.doseg:
            return
        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[2].vrati_tip(config.doseg), "int"):
            PomocneFunkcije.ispisi_error_poruku()
            return
        cvor_stabla.tip = "int"
        cvor_stabla.je_l_vrijednost = False
    return


def aditivni_izraz(cvor_stabla):
    if cvor_stabla.lista_djece.len() == 1:
        multiplikativni_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.tip = cvor_stabla.lista_djece[0].vrati_tip(config.doseg)
        cvor_stabla.je_l_vrijednost(cvor_stabla.lista_djece[0].vrati_l_vrijednost(config.doseg))
    else:
        aditivni_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[0].vrati_tip(config.doseg), "int"):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        multiplikativni_izraz(cvor_stabla.lista_djece[2]);
        if config.doseg:
            return
        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[2].vrati_tip(config.doseg), "int"):
            PomocneFunkcije.ispisi_error_poruku()
            return
        cvor_stabla.tip = "int"
        cvor_stabla.je_l_vrijednost = False
    return


def odnosni_izraz(cvor_stabla):
    if cvor_stabla.lista_djece.len() == 1:
        aditivni_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.tip = cvor_stabla.lista_djece[0].vrati_tip(config.doseg)
        cvor_stabla.je_l_vrijednost(cvor_stabla.lista_djece[0].vrati_l_vrijednost(config.doseg))
    else:
        odnosni_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[0].vrati_tip(config.doseg), "int"):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        aditivni_izraz(cvor_stabla.lista_djece[2]);
        if config.doseg:
            return
        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[2].vrati_tip(config.doseg), "int"):
            PomocneFunkcije.ispisi_error_poruku()
            return
        cvor_stabla.tip = "int"
        cvor_stabla.je_l_vrijednost = False
    return


def jednakosni_izraz(cvor_stabla):
    if cvor_stabla.lista_djece.len() == 1:
        odnosni_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.tip = cvor_stabla.lista_djece[0].vrati_tip(config.doseg)
        cvor_stabla.je_l_vrijednost(cvor_stabla.lista_djece[0].vrati_l_vrijednost(config.doseg))
    else:
        jednakosni_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[0].vrati_tip(config.doseg), "int"):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        odnosni_izraz(cvor_stabla.lista_djece[2]);
        if config.doseg:
            return
        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[2].vrati_tip(config.doseg), "int"):
            PomocneFunkcije.ispisi_error_poruku()
            return
        cvor_stabla.tip = "int"
        cvor_stabla.je_l_vrijednost = False
    return


def bin_i_izraz(cvor_stabla):
    if cvor_stabla.lista_djece.len() == 1:
        jednakosni_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.tip = cvor_stabla.lista_djece[0].vrati_tip(config.doseg)
        cvor_stabla.je_l_vrijednost(cvor_stabla.lista_djece[0].vrati_l_vrijednost(config.doseg))
    else:
        bin_i_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[0].vrati_tip(config.doseg), "int"):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        jednakosni_izraz(cvor_stabla.lista_djece[2]);
        if config.doseg:
            return
        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[2].vrati_tip(config.doseg), "int"):
            PomocneFunkcije.ispisi_error_poruku()
            return
        cvor_stabla.tip = "int"
        cvor_stabla.je_l_vrijednost = False
    return


def bin_xili_izraz(cvor_stabla):
    if cvor_stabla.lista_djece.len() == 1:
        bin_i_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.tip = cvor_stabla.lista_djece[0].vrati_tip(config.doseg)
        cvor_stabla.je_l_vrijednost(cvor_stabla.lista_djece[0].vrati_l_vrijednost(config.doseg))
    else:
        bin_xili_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[0].vrati_tip(config.doseg), "int"):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        bin_i_izraz(cvor_stabla.lista_djece[2]);
        if config.doseg:
            return
        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[2].vrati_tip(config.doseg), "int"):
            PomocneFunkcije.ispisi_error_poruku()
            return
        cvor_stabla.tip = "int"
        cvor_stabla.je_l_vrijednost = False
    return


def bin_ili_izraz(cvor_stabla):
    if cvor_stabla.lista_djece.len() == 1:
        bin_xili_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.tip = cvor_stabla.lista_djece[0].vrati_tip(config.doseg)
        cvor_stabla.je_l_vrijednost(cvor_stabla.lista_djece[0].vrati_l_vrijednost(config.doseg))
    else:
        bin_ili_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[0].vrati_tip(config.doseg), "int"):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        bin_xili_izraz(cvor_stabla.lista_djece[2]);
        if config.doseg:
            return
        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[2].vrati_tip(config.doseg), "int"):
            PomocneFunkcije.ispisi_error_poruku()
            return
        cvor_stabla.tip = "int"
        cvor_stabla.je_l_vrijednost = False
    return


def log_i_izraz(cvor_stabla):
    if cvor_stabla.lista_djece.len() == 1:
        bin_ili_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.tip = cvor_stabla.lista_djece[0].vrati_tip(config.doseg)
        cvor_stabla.je_l_vrijednost(cvor_stabla.lista_djece[0].vrati_l_vrijednost(config.doseg))
    else:
        log_i_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[0].vrati_tip(config.doseg), "int"):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        bin_ili_izraz(cvor_stabla.lista_djece[2]);
        if config.doseg:
            return
        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[2].vrati_tip(config.doseg), "int"):
            PomocneFunkcije.ispisi_error_poruku()
            return
        cvor_stabla.tip = "int"
        cvor_stabla.je_l_vrijednost = False
    return


def log_ili_izraz(cvor_stabla):
    if cvor_stabla.lista_djece.len() == 1:
        log_i_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.tip = cvor_stabla.lista_djece[0].vrati_tip(config.doseg)
        cvor_stabla.je_l_vrijednost(cvor_stabla.lista_djece[0].vrati_l_vrijednost(config.doseg))
    else:
        log_ili_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[0].vrati_tip(config.doseg), "int"):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        log_i_izraz(cvor_stabla.lista_djece[2]);
        if config.doseg:
            return
        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[2].vrati_tip(config.doseg), "int"):
            PomocneFunkcije.ispisi_error_poruku()
            return
        cvor_stabla.tip = "int"
        cvor_stabla.je_l_vrijednost = False
    return


def izraz_pridruzivanja(cvor_stabla):
    if cvor_stabla.lista_djece.len() == 1:
        log_ili_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.tip = cvor_stabla.lista_djece[0].vrati_tip(config.doseg)
        cvor_stabla.je_l_vrijednost(cvor_stabla.lista_djece[0].vrati_l_vrijednost(config.doseg))
    else:
        postfiks_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        if not cvor_stabla.lista_djece[0].vrati_l_vrijednost(config.doseg):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        izraz_pridruzivanja(cvor_stabla.lista_djece[2]);
        if config.doseg:
            return
        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[2].vrati_tip(config.doseg), cvor_stabla.lista_djece[0].vrati_tip(config.doseg)):
            PomocneFunkcije.ispisi_error_poruku()
            return
        cvor_stabla.tip = cvor_stabla.lista_djece[0].vrati_tip(config.doseg)
        cvor_stabla.je_l_vrijednost = False
    return


def izraz(cvor_stabla):
    cvor = cvor_stabla.lista_djece[0]

    if cvor.podaci.startswith('<izraz_pridruzivanja>'):
        
        izraz_pridruzivanja(cvor)
        if config.error:
            return
        
        cvor_stabla.postavi_tip(cvor.vrati_tip(config.doseg))
        cvor_stabla.je_l_vrijednost = cvor.je_l_vrijednost

    if cvor.podaci.startswith('<izraz>'):

        izraz(cvor)
        if config.error:
            return

        izraz_pridruzivanja(cvor_stabla.lista_djece[2])
        if config.error:
            return
        
        cvor_stabla.postavi_tip(cvor_stabla.lista_djece[2].vrati_tip(config.doseg))
        cvor_stabla.je_l_vrijednost = False

    return