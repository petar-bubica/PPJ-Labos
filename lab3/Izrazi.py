import config
import PomocneFunkcije
import NaredbenaStruktura
import Deklaracije_I_Definicije
from CvorStabla import CvorStabla
from CvorTablice import CvorTablice


def primarni_izraz(cvor_stabla):
    print("U primarni izraz metodi")

    cvor = cvor_stabla.lista_djece[0]
    
    if cvor.podaci.startswith('IDN'):
        if not PomocneFunkcije.je_vec_deklarirano(cvor.vrati_ime()):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return

        cvor_stabla.postavi_tip(cvor.vrati_tip(config.doseg))
        cvor_stabla.lista_tipova = cvor.vrati_tipove(config.doseg)
        cvor_stabla.ime = cvor.vrati_ime()
        cvor_stabla.je_l_vrijednost = cvor.vrati_l_vrijednost(config.doseg)

    elif cvor.podaci.startswith('BROJ'):

        if not PomocneFunkcije.je_integer(cvor.vrati_ime()):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        
        cvor_stabla.postavi_tip('int')
        cvor_stabla.je_l_vrijednost = False

    elif cvor.podaci.startswith('ZNAK'):
        if not PomocneFunkcije.je_char(cvor.vrati_ime()):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        
        cvor_stabla.postavi_tip('char')
        cvor_stabla.je_l_vrijednost = False

    elif cvor.podaci.startswith('NIZ_ZNAKOVA'):
        if not PomocneFunkcije.je_string(cvor.vrati_ime()):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        
        cvor_stabla.postavi_tip('nizchar')
        cvor_stabla.je_konstanta = True
        cvor_stabla.je_l_vrijednost = False

    elif cvor.podaci.startswith('L_ZAGRADA'):
        
        izraz(cvor_stabla.lista_djece[1])
        if config.error:
            return

        cvor_stabla.postavi_tip(cvor_stabla.lista_djece[1].vrati_tip(config.doseg))
        cvor_stabla.je_l_vrijednost = cvor_stabla.lista_djece[1].vrati_l_vrijednost(config.doseg)

    return


def postfiks_izraz(cvor_stabla):
    print("U postfix izraz metodi", cvor_stabla, cvor_stabla.lista_djece)

    if len(cvor_stabla.lista_djece) == 1:
        primarni_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return

        cvor_stabla.postavi_tip(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
        cvor_stabla.lista_tipova = cvor_stabla.lista_djece[0].vrati_tipove(config.doseg)
        cvor_stabla.ime = cvor_stabla.lista_djece[0].vrati_ime()
        cvor_stabla.je_l_vrijednost = cvor_stabla.lista_djece[0].vrati_l_vrijednost(config.doseg)

    elif cvor_stabla.lista_djece[1].podaci.startswith('L_UGL_ZAGRADA'):

        postfiks_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return

        if not cvor_stabla.lista_djece[0].vrati_tip(config.doseg).startswith('niz'):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return

        X = cvor_stabla.lista_djece[0].vrati_tip(config.doseg)[:3]
        je_konstanta = cvor_stabla.lista_djece[0].je_konstanta
        
        izraz(cvor_stabla.lista_djece[2])
        if config.error:
            return

        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[2].vrati_tip(config.doseg), 'int'):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return

        cvor_stabla.postavi_tip(X)
        cvor_stabla.je_l_vrijednost = not (je_konstanta)
        return

    elif len(cvor_stabla.lista_djece) == 3:

        postfiks_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return

        if not cvor_stabla.lista_djece[0].je_funkcija() or cvor_stabla.lista_djece[0].lista_tipova[0] != 'void':
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return

        cvor_stabla.postavi_tip(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
        cvor_stabla.ime = cvor_stabla.lista_djece[0].vrati_ime()
        cvor_stabla.je_l_vrijednost = False

    elif len(cvor_stabla.lista_djece) == 4:

        postfiks_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return

        lista_argumenata(cvor_stabla.lista_djece[2])
        if config.error:
            return

        if not cvor_stabla.lista_djece[0].je_funkcija():
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return

        p_izraz = cvor_stabla.lista_djece[0]
        lista_arg = cvor_stabla.lista_djece[2]
        if len(p_izraz.vrati_tipove(config.doseg)) != len(lista_arg.vrati_tipove(config.doseg)):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return

        for i in range(len(p_izraz.vrati_tipove(config.doseg))):
            if not PomocneFunkcije.je_castable(lista_arg.lista_tipova[i], p_izraz.lista_tipova[i]):
                PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
                return

        cvor_stabla.postavi_tip(p_izraz.vrati_tip(config.doseg))
        cvor_stabla.je_l_vrijednost = False

    elif len(cvor_stabla.lista_djece) == 2:

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
    print("U lista argumenata metodi")
    if len(cvor_stabla.lista_djece) == 1:
        izraz_pridruzivanja(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.lista_tipova.append(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
    elif len(cvor_stabla.lista_djece) > 1:
        lista_argumenata(cvor_stabla.lista_djece[0])
        if config.error:
            return
        izraz_pridruzivanja(cvor_stabla.lista_djece[2])
        if config.error:
            return

        cvor_stabla.lista_tipova = cvor_stabla.lista_djece[0].vrati_tipove(config.doseg)
        cvor_stabla.lista_tipova.append(cvor_stabla.lista_djece[2].vrati_tip(config.doseg))
    return


def unarni_izraz(cvor_stabla):
    print("U unarni izraz metodi")

    if len(cvor_stabla.lista_djece) == 1:
        postfiks_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.postavi_tip(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
        cvor_stabla.lista_tipova = cvor_stabla.lista_djece[0].vrati_tipove(config.doseg)
        cvor_stabla.ime = cvor_stabla.lista_djece[0].vrati_ime()
        cvor_stabla.je_l_vrijednost = cvor_stabla.lista_djece[0].vrati_l_vrijednost(config.doseg)
    elif cvor_stabla.lista_djece[1].podaci == "<unarni_izraz>":
        unarni_izraz(cvor_stabla.lista_djece[1])
        if config.error:
            return
        if not cvor_stabla.lista_djece[1].vrati_l_vrijednost(config.doseg) or not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[1].vrati_tip(config.doseg), "int"):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        cvor_stabla.postavi_tip("int")
        cvor_stabla.je_l_vrijednost = False
    else:
        cast_izraz(cvor_stabla.lista_djece[1])
        if config.error:
            return
        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[1].vrati_tip(config.doseg), "int"):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        cvor_stabla.postavi_tip("int")
        cvor_stabla.je_l_vrijednost = False
    return


def cast_izraz(cvor_stabla):
    print("U cast izraz metodi")
    if len(cvor_stabla.lista_djece) == 1:
        unarni_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.postavi_tip(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
        cvor_stabla.lista_tipova = cvor_stabla.lista_djece[0].vrati_tipove(config.doseg)
        cvor_stabla.ime = cvor_stabla.lista_djece[0].vrati_ime()
        cvor_stabla.je_l_vrijednost = cvor_stabla.lista_djece[0].vrati_l_vrijednost(config.doseg)
    else:
        ime_tipa(cvor_stabla.lista_djece[1])
        if config.error:
            return
        cast_izraz(cvor_stabla.lista_djece[3])
        if config.error:
            return
        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[3].vrati_tip(config.doseg), cvor_stabla.lista_djece[1].vrati_tip(config.doseg)) and not (cvor_stabla.lista_djece[3].vrati_tip(config.doseg) == "int" and cvor_stabla.lista_djece[1].vrati_tip(config.doseg) == "char") or cvor_stabla.lista_djece[3].je_funkcija() or cvor_stabla.lista_djece[1].je_funkcija():
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        cvor_stabla.postavi_tip(cvor_stabla.lista_djece[1].vrati_tip(config.doseg))
        cvor_stabla.je_l_vrijednost = False
    return


def ime_tipa(cvor_stabla):
    print("U ime tipa metodi")
    if len(cvor_stabla.lista_djece) == 1:
        specifikator_tipa(cvor_stabla.lista_djece[0])
        cvor_stabla.postavi_tip(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
    else:
        specifikator_tipa(cvor_stabla.lista_djece[1])
        if cvor_stabla.lista_djece[1].vrati_tip(config.doseg) == "void":
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
        if config.error:
            return
        cvor_stabla.postavi_tip(cvor_stabla.lista_djece[1].vrati_tip(config.doseg))
        cvor_stabla.je_konstanta = True
    return


def specifikator_tipa(cvor_stabla):
    print("U specifikator tipa metodi")
    cvor = cvor_stabla.lista_djece[0]
    if cvor.podaci.startswith("KR_VOID"):
        cvor_stabla.postavi_tip("void")
    elif cvor.podaci.startswith("KR_CHAR"):
        cvor_stabla.postavi_tip("char")
    elif cvor.podaci.startswith("KR_INT"):
        cvor_stabla.postavi_tip("int")
    return


def multiplikativni_izraz(cvor_stabla):
    print("U multiplikativni izraz metodi")
    if len(cvor_stabla.lista_djece) == 1:
        cast_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.postavi_tip(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
        cvor_stabla.lista_tipova = cvor_stabla.lista_djece[0].vrati_tipove(config.doseg)
        cvor_stabla.ime = cvor_stabla.lista_djece[0].vrati_ime()
        cvor_stabla.je_l_vrijednost = cvor_stabla.lista_djece[0].vrati_l_vrijednost(config.doseg)
    else:
        multiplikativni_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[0].vrati_tip(config.doseg), "int"):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        cast_izraz(cvor_stabla.lista_djece[2])
        if config.doseg:
            return
        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[2].vrati_tip(config.doseg), "int"):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        cvor_stabla.postavi_tip("int")
        cvor_stabla.je_l_vrijednost = False
    return


def aditivni_izraz(cvor_stabla):
    print("U aditivni izraz metodi")
    if len(cvor_stabla.lista_djece) == 1:
        multiplikativni_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.postavi_tip(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
        cvor_stabla.lista_tipova = cvor_stabla.lista_djece[0].vrati_tipove(config.doseg)
        cvor_stabla.ime = cvor_stabla.lista_djece[0].vrati_ime()
        cvor_stabla.je_l_vrijednost = cvor_stabla.lista_djece[0].vrati_l_vrijednost(config.doseg)
    else:
        aditivni_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[0].vrati_tip(config.doseg), "int"):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        multiplikativni_izraz(cvor_stabla.lista_djece[2])
        if config.error:
            return
        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[2].vrati_tip(config.doseg), "int"):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        cvor_stabla.postavi_tip("int")
        cvor_stabla.je_l_vrijednost = False
    return


def odnosni_izraz(cvor_stabla):
    print("U odnosni izraz metodi")
    if len(cvor_stabla.lista_djece) == 1:
        aditivni_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.postavi_tip(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
        cvor_stabla.lista_tipova = cvor_stabla.lista_djece[0].vrati_tipove(config.doseg)
        cvor_stabla.ime = cvor_stabla.lista_djece[0].vrati_ime()
        cvor_stabla.je_l_vrijednost = cvor_stabla.lista_djece[0].vrati_l_vrijednost(config.doseg)
    else:
        odnosni_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[0].vrati_tip(config.doseg), "int"):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        aditivni_izraz(cvor_stabla.lista_djece[2])
        if config.error:
            return
        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[2].vrati_tip(config.doseg), "int"):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        cvor_stabla.postavi_tip("int")
        cvor_stabla.je_l_vrijednost = False
    return


def jednakosni_izraz(cvor_stabla):
    print("U jednakosni izraz metodi")
    if len(cvor_stabla.lista_djece) == 1:
        odnosni_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.postavi_tip(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
        cvor_stabla.lista_tipova = cvor_stabla.lista_djece[0].vrati_tipove(config.doseg)
        cvor_stabla.ime = cvor_stabla.lista_djece[0].vrati_ime()
        cvor_stabla.je_l_vrijednost = cvor_stabla.lista_djece[0].vrati_l_vrijednost(config.doseg)
    else:
        jednakosni_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        if cvor_stabla.lista_djece[0].je_funkcija() or not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[0].vrati_tip(config.doseg), "int"):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        odnosni_izraz(cvor_stabla.lista_djece[2])
        if config.error:
            return
        if cvor_stabla.lista_djece[2].je_funkcija() or not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[2].vrati_tip(config.doseg), "int"):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        cvor_stabla.postavi_tip("int")
        cvor_stabla.je_l_vrijednost = False
    return


def bin_i_izraz(cvor_stabla):
    print("U bin i izraz metodi")
    if len(cvor_stabla.lista_djece) == 1:
        jednakosni_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.postavi_tip(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
        cvor_stabla.lista_tipova = cvor_stabla.lista_djece[0].vrati_tipove(config.doseg)
        cvor_stabla.ime = cvor_stabla.lista_djece[0].vrati_ime()
        cvor_stabla.je_l_vrijednost = cvor_stabla.lista_djece[0].vrati_l_vrijednost(config.doseg)
    else:
        bin_i_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[0].vrati_tip(config.doseg), "int"):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        jednakosni_izraz(cvor_stabla.lista_djece[2])
        if config.error:
            return
        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[2].vrati_tip(config.doseg), "int"):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        cvor_stabla.postavi_tip("int")
        cvor_stabla.je_l_vrijednost = False
    return


def bin_xili_izraz(cvor_stabla):
    print("U bin xili izraz metodi")
    if len(cvor_stabla.lista_djece) == 1:
        bin_i_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.postavi_tip(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
        cvor_stabla.lista_tipova = cvor_stabla.lista_djece[0].vrati_tipove(config.doseg)
        cvor_stabla.ime = cvor_stabla.lista_djece[0].vrati_ime()
        cvor_stabla.je_l_vrijednost = cvor_stabla.lista_djece[0].vrati_l_vrijednost(config.doseg)
    else:
        bin_xili_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[0].vrati_tip(config.doseg), "int"):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        bin_i_izraz(cvor_stabla.lista_djece[2])
        if config.error:
            return
        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[2].vrati_tip(config.doseg), "int"):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        cvor_stabla.postavi_tip("int")
        cvor_stabla.je_l_vrijednost = False
    return


def bin_ili_izraz(cvor_stabla):
    print("U bin ili izraz metodi")
    if len(cvor_stabla.lista_djece) == 1:
        bin_xili_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.postavi_tip(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
        cvor_stabla.lista_tipova = cvor_stabla.lista_djece[0].vrati_tipove(config.doseg)
        cvor_stabla.ime = cvor_stabla.lista_djece[0].vrati_ime()
        cvor_stabla.je_l_vrijednost = cvor_stabla.lista_djece[0].vrati_l_vrijednost(config.doseg)
    else:
        bin_ili_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[0].vrati_tip(config.doseg), "int"):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        bin_xili_izraz(cvor_stabla.lista_djece[2])
        if config.error:
            return
        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[2].vrati_tip(config.doseg), "int"):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        cvor_stabla.postavi_tip("int")
        cvor_stabla.je_l_vrijednost = False
    return


def log_i_izraz(cvor_stabla):
    print("U log i izraz metodi")
    if len(cvor_stabla.lista_djece) == 1:
        bin_ili_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.postavi_tip(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
        cvor_stabla.lista_tipova = cvor_stabla.lista_djece[0].vrati_tipove(config.doseg)
        cvor_stabla.ime = cvor_stabla.lista_djece[0].vrati_ime()
        cvor_stabla.je_l_vrijednost = cvor_stabla.lista_djece[0].vrati_l_vrijednost(config.doseg)
    else:
        log_i_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[0].vrati_tip(config.doseg), "int"):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        bin_ili_izraz(cvor_stabla.lista_djece[2])
        if config.error:
            return
        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[2].vrati_tip(config.doseg), "int"):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        cvor_stabla.postavi_tip("int")
        cvor_stabla.je_l_vrijednost = False
    return


def log_ili_izraz(cvor_stabla):
    print("U log ili izraz metodi")
    if len(cvor_stabla.lista_djece) == 1:
        log_i_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.postavi_tip(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
        cvor_stabla.lista_tipova = cvor_stabla.lista_djece[0].vrati_tipove(config.doseg)
        cvor_stabla.ime = cvor_stabla.lista_djece[0].vrati_ime()
        cvor_stabla.je_l_vrijednost = cvor_stabla.lista_djece[0].vrati_l_vrijednost(config.doseg)
    else:
        log_ili_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[0].vrati_tip(config.doseg), "int"):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        log_i_izraz(cvor_stabla.lista_djece[2])
        if config.error:
            return
        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[2].vrati_tip(config.doseg), "int"):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        cvor_stabla.postavi_tip("int")
        cvor_stabla.je_l_vrijednost = False
    return


def izraz_pridruzivanja(cvor_stabla):
    print("U izraz pridruzivanja metodi")
    if len(cvor_stabla.lista_djece) == 1:
        log_ili_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.postavi_tip(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
        cvor_stabla.lista_tipova = cvor_stabla.lista_djece[0].vrati_tipove(config.doseg)
        cvor_stabla.ime = cvor_stabla.lista_djece[0].vrati_ime()
        cvor_stabla.je_l_vrijednost = cvor_stabla.lista_djece[0].vrati_l_vrijednost(config.doseg)
    elif len(cvor_stabla.lista_djece) > 1:
        postfiks_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        if not cvor_stabla.lista_djece[0].vrati_l_vrijednost(config.doseg):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        izraz_pridruzivanja(cvor_stabla.lista_djece[2])
        if config.error:
            return
        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[2].vrati_tip(config.doseg), cvor_stabla.lista_djece[0].vrati_tip(config.doseg)):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        cvor_stabla.postavi_tip(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
        cvor_stabla.je_l_vrijednost = False
    return


def izraz(cvor_stabla):
    print("U izraz metodi")
    if len(cvor_stabla.lista_djece) == 1:
        izraz_pridruzivanja(cvor_stabla.lista_djece[0])
        if config.error:
            return
        
        cvor_stabla.postavi_tip(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
        cvor_stabla.lista_tipova = cvor_stabla.lista_djece[0].vrati_tipove(config.doseg)
        cvor_stabla.ime = cvor_stabla.lista_djece[0].vrati_ime()
        cvor_stabla.je_l_vrijednost = cvor_stabla.lista_djece[0].vrati_l_vrijednost(config.doseg)

    elif len(cvor_stabla.lista_djece) > 1:

        izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return

        izraz_pridruzivanja(cvor_stabla.lista_djece[2])
        if config.error:
            return
        
        cvor_stabla.postavi_tip(cvor_stabla.lista_djece[2].vrati_tip(config.doseg))
        cvor_stabla.je_l_vrijednost = False

    return
