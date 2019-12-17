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
        if not PomocneFunkcije.je_vec_deklarirano(cvor.vrati_ime()):
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
    if len(cvor_stabla.lista_djece) == 1:
        
        primarni_izraz(cvor_stabla)
        if config.error:
            return

        cvor_stabla.postavi_tip(cvor_stabla.vrati_tip(config.doseg))
        cvor_stabla.lista_tipova = cvor_stabla.vrati_tipove(config.doseg)
        cvor_stabla.ime = cvor_stabla.vrati_ime()
        cvor_stabla.je_l_vrijednost = cvor_stabla.vrati_l_vrijednost(config.doseg)

    if cvor_stabla.lista_djece[1].podaci.startswith('L_UGL_ZAGRADA'):

        postfiks_izraz(cvor_stabla.lista_djece[1])
        if config.error:
            return

        if not cvor_stabla.lista_djece[0].vrati_tip(config.doseg).startswith('niz'):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)

        X = cvor_stabla.lista_djece[0].vrati_tip(config.doseg)[:3]
        je_konstanta = cvor_stabla.lista_djece[0].je_konstanta
        izraz(cvor_stabla.lista_djece[2])

        if config.error:
            return

        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[2].vrati_tip(config.doseg), 'int'):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return

        cvor_stabla.postavi_tip(X)
        cvor_stabla.je_l_vrijednost = not je_konstanta

    if len(cvor_stabla.lista_djece) == 3:

        postfiks_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return

        if not cvor_stabla.lista_djece[0].je_funkcija() or not cvor_stabla.lista_djece[0].lista_tipova[0] == 'void':
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return

        cvor_stabla.postavi_tip(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
        cvor_stabla.ime = cvor_stabla.lista_djece[0].vrati_ime()
        cvor_stabla.je_l_vrijednost = False

    if len(cvor_stabla.lista_djece) == 4:

        postfiks_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return

        lista_argumenata(cvor_stabla.lista_djece[2])
        if config.error:
            return

        p_izraz = cvor_stabla.lista_djece[0]
        lista_arg = cvor_stabla.lista_djece[2]
        if not (len(p_izraz.vrati_tipove(config.doseg)) == len(lista_arg.vrati_tipove(config.doseg))):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return

        for i in range(len(p_izraz.vrati_tipove(config.doseg))):
            if not PomocneFunkcije.je_castable(lista_arg.lista_tipova[i], p_izraz.lista_tipova[i]):
                PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
                return

        cvor_stabla.postavi_tip(p_izraz.vrati_tip(config.doseg))
        cvor_stabla.je_l_vrijednost = False

    if len(cvor_stabla.lista_djece) == 2:

        postfiks_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return

        p_izraz = cvor_stabla.lista_djece[0]
        if not p_izraz.vrati_l_vrijednost(config.doseg) or not PomocneFunkcije.je_castable(p_izraz.vrati_tip(config.doseg), 'int'):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return

        cvor_stabla.postavi_tip('int')
        cvor_stabla.je_l_vrijednost = False

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
    return


def unarni_operator(cvor_stabla):
    return


def cast_izraz(cvor_stabla):
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