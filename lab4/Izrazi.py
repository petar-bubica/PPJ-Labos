from lab4 import config
from lab4 import PomocneFunkcije
from lab4 import NaredbenaStruktura
from lab4 import Deklaracije_I_Definicije
from lab4.CvorStabla import CvorStabla
from lab4.CvorTablice import CvorTablice

from lab4.CvorTabliceUpgrade import CvorTabliceUpgrade

#PROVJERITI PRI KRAJU UVLAKE
def primarni_izraz(cvor_stabla):
    #print("U primarni izraz metodi")

    cvor = cvor_stabla.lista_djece[0]
    
    if cvor.podaci.startswith('IDN'):
        if not PomocneFunkcije.je_vec_deklarirano(cvor.vrati_ime()):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return

        cvor_stabla.postavi_tip(cvor.vrati_tip(config.doseg))
        cvor_stabla.lista_tipova = cvor.vrati_tipove(config.doseg)
        cvor_stabla.ime = cvor.vrati_ime()
        cvor_stabla.je_l_vrijednost = cvor.vrati_l_vrijednost(config.doseg)

        identifikator = dohvati_vec_deklarirano(cvor.vrati_ime())
        labela = identifikator.vrati_labelu()

        if cvor_stabla.je_funkcija:
            cvor_stabla.dodaj_kod("\tCALL" + labela + "\n")
            if len(cvor_stabla.vrati_tipove(config.doseg)) != 1 or (len(cvor_stabla.vrati_tipove(config.doseg)) == 1 and cvor_stabla.lista_tipova[0] == "void"):
                cvor_stabla.dodaj_kod("\tADD R7, %D " + str(len(cvor_stabla.vrati_tipove(config.doseg))*4) + ", R7\n")
            if cvor_stabla.vrati_tip(config.doseg) != "void":
                cvor_stabla.dodaj_kod("\tPUSH R7\n")
        else:
            if cvor_stabla.tip.startswith("niz"):
                cvor_stabla.dodaj_kod("\tMOVE " + labela + ", R0\n")
                cvor_stabla.dodaj_kod("\tPUSH R0\n")
            else:
                cvor_stabla.dodaj_kod("\tLOAD R0, ( " + labela + ")\n")
                cvor_stabla.dodaj_kod("\tPUSH R0\n")
        cvor_stabla.postavi_labelu(labela)


    elif cvor.podaci.startswith('BROJ'):

        if not PomocneFunkcije.je_integer(cvor.vrati_ime()):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        
        cvor_stabla.postavi_tip('int')
        cvor_stabla.je_l_vrijednost = False
        cvor.labela = ("L" + config.brojac_labela)
        config.brojac_labela += 1

        config.tabela.append(CvorTabliceUpgrade(cvor.labela,cvor))
        cvor_stabla.dodaj_kod("\tLOAD R0, ( " + cvor.labela + ")\n")
        cvor_stabla.dodaj_kod("\tPUSH R0\n")
        cvor_stabla.labela = cvor.labela

    elif cvor.podaci.startswith('ZNAK'):
        if not PomocneFunkcije.je_char(cvor.vrati_ime()):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        
        cvor_stabla.postavi_tip('char')
        cvor_stabla.je_l_vrijednost = False

        cvor.labela = ("L" + config.brojac_labela)
        config.brojac_labela += 1

        config.tabela.append(CvorTabliceUpgrade(cvor.labela, cvor))
        cvor_stabla.dodaj_kod("\tLOAD R0, ( " + cvor.labela + ")\n")
        cvor_stabla.dodaj_kod("\tPUSH R0\n")
        cvor_stabla.labela = cvor.labela

    elif cvor.podaci.startswith('NIZ_ZNAKOVA'):
        if not PomocneFunkcije.je_string(cvor.vrati_ime()):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        
        cvor_stabla.postavi_tip('nizchar')
        cvor_stabla.je_konstanta = True
        cvor_stabla.je_l_vrijednost = False

        #TODO

    elif cvor.podaci.startswith('L_ZAGRADA'):
        
        izraz(cvor_stabla.lista_djece[1])
        if config.error:
            return

        cvor_stabla.postavi_tip(cvor_stabla.lista_djece[1].vrati_tip(config.doseg))
        cvor_stabla.je_l_vrijednost = cvor_stabla.lista_djece[1].vrati_l_vrijednost(config.doseg)
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[1].kod)
    return


def postfiks_izraz(cvor_stabla):
    #print("U postfix izraz metodi", cvor_stabla, cvor_stabla.lista_djece)

    if len(cvor_stabla.lista_djece) == 1:
        primarni_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return

        cvor_stabla.postavi_tip(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
        cvor_stabla.lista_tipova = cvor_stabla.lista_djece[0].vrati_tipove(config.doseg)
        cvor_stabla.ime = cvor_stabla.lista_djece[0].vrati_ime()
        cvor_stabla.je_l_vrijednost = cvor_stabla.lista_djece[0].vrati_l_vrijednost(config.doseg)
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[0].kod)
        cvor_stabla.labela = cvor_stabla.lista_djece[0].labela

    elif cvor_stabla.lista_djece[1].podaci.startswith('L_UGL_ZAGRADA'):

        postfiks_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return

        if not cvor_stabla.lista_djece[0].vrati_tip(config.doseg).startswith('niz'):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return

        X = cvor_stabla.lista_djece[0].vrati_tip(config.doseg)[3:]
        je_konstanta = cvor_stabla.lista_djece[0].je_konstanta
        
        izraz(cvor_stabla.lista_djece[2])
        if config.error:
            return

        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[2].vrati_tip(config.doseg), 'int'):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return

        cvor_stabla.postavi_tip(X)
        cvor_stabla.je_l_vrijednost = not (je_konstanta)
        labela = dohvati_vec_deklarirano(cvor_stabla.lista_djece[0].vrati_ime()).labela
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[2].kod)
        cvor_stabla.dodaj_kod("\tPOP R0\n");
        cvor_stabla.dodaj_kod("\tSHL R0, %D 2, R0\n");
        cvor_stabla.dodaj_kod("\tMOVE " + labela + ", R1\n");
        cvor_stabla.dodaj_kod("\tADD R0, R1, R0\n");
        cvor_stabla.dodaj_kod("\tLOAD R0, (R0)\n\tPUSH R0\n");

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
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[0].kod)

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
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[2].kod)
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[0].kod)

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
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[0].kod)
        if cvor_stabla.lista_djece[0].vrati_ime() == "++":
            cvor_stabla.dodaj_kod("\tPOP R0\n");
            cvor_stabla.dodaj_kod("\tADD R0, 1, R0\n");
            cvor_stabla.dodaj_kod("\tPUSH R0\n");
        else:
            cvor_stabla.dodaj_kod("\tPOP R0\n");
            cvor_stabla.dodaj_kod("\tSUB R0, 1, R0\n");
            cvor_stabla.dodaj_kod("\tPUSH R0\n");

    return


def lista_argumenata(cvor_stabla):
    #print("U lista argumenata metodi")
    if len(cvor_stabla.lista_djece) == 1:
        izraz_pridruzivanja(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.lista_tipova.append(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[0].kod)

    elif len(cvor_stabla.lista_djece) > 1:
        lista_argumenata(cvor_stabla.lista_djece[0])
        if config.error:
            return
        izraz_pridruzivanja(cvor_stabla.lista_djece[2])
        if config.error:
            return

        cvor_stabla.lista_tipova = cvor_stabla.lista_djece[0].vrati_tipove(config.doseg)
        cvor_stabla.lista_tipova.append(cvor_stabla.lista_djece[2].vrati_tip(config.doseg))
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[0].kod)
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[2].kod)
    return


def unarni_izraz(cvor_stabla):
    #print("U unarni izraz metodi")

    if len(cvor_stabla.lista_djece) == 1:
        postfiks_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.postavi_tip(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
        cvor_stabla.lista_tipova = cvor_stabla.lista_djece[0].vrati_tipove(config.doseg)
        cvor_stabla.ime = cvor_stabla.lista_djece[0].vrati_ime()
        cvor_stabla.je_l_vrijednost = cvor_stabla.lista_djece[0].vrati_l_vrijednost(config.doseg)
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[0].kod)
        cvor_stabla.labela = cvor_stabla.lista_djece[0].labela
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
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[1].kod)
        cvor_stabla.dodaj_kod("\tPOP R0\n");
        if cvor_stabla.lista_djece[0].lista_djece[0].vrati_ime() == "-":
            cvor_stabla.dodaj_kod("\tXOR R0, -1, R0\n\tADD R0, 1, R0\n")
        if cvor_stabla.lista_djece[0].lista_djece[0].vrati_ime() == "~":
            cvor_stabla.dodaj_kod("\tXOR R0, %D -1, R0\n");
        cvor_stabla.dodaj_kod("\tPUSH R0\n")
    return


def cast_izraz(cvor_stabla):
    #print("U cast izraz metodi")
    if len(cvor_stabla.lista_djece) == 1:
        unarni_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.postavi_tip(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
        cvor_stabla.lista_tipova = cvor_stabla.lista_djece[0].vrati_tipove(config.doseg)
        cvor_stabla.ime = cvor_stabla.lista_djece[0].vrati_ime()
        cvor_stabla.je_l_vrijednost = cvor_stabla.lista_djece[0].vrati_l_vrijednost(config.doseg)
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[0].kod)
        cvor_stabla.labela = cvor_stabla.lista_djece[0].labela
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
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[3].kod)
        cvor_stabla.labela = cvor_stabla.lista_djece[3].labela
    return


def ime_tipa(cvor_stabla):
    #print("U ime tipa metodi")
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
    #print("U specifikator tipa metodi")
    cvor = cvor_stabla.lista_djece[0]
    if cvor.podaci.startswith("KR_VOID"):
        cvor_stabla.postavi_tip("void")
    elif cvor.podaci.startswith("KR_CHAR"):
        cvor_stabla.postavi_tip("char")
    elif cvor.podaci.startswith("KR_INT"):
        cvor_stabla.postavi_tip("int")
    return


def multiplikativni_izraz(cvor_stabla):
    #print("U multiplikativni izraz metodi")
    if len(cvor_stabla.lista_djece) == 1:
        cast_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.postavi_tip(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
        cvor_stabla.lista_tipova = cvor_stabla.lista_djece[0].vrati_tipove(config.doseg)
        cvor_stabla.ime = cvor_stabla.lista_djece[0].vrati_ime()
        cvor_stabla.je_l_vrijednost = cvor_stabla.lista_djece[0].vrati_l_vrijednost(config.doseg)
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[0].kod)
        cvor_stabla.labela = cvor_stabla.lista_djece[0].labela
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
    #print("U aditivni izraz metodi")
    if len(cvor_stabla.lista_djece) == 1:
        multiplikativni_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.postavi_tip(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
        cvor_stabla.lista_tipova = cvor_stabla.lista_djece[0].vrati_tipove(config.doseg)
        cvor_stabla.ime = cvor_stabla.lista_djece[0].vrati_ime()
        cvor_stabla.je_l_vrijednost = cvor_stabla.lista_djece[0].vrati_l_vrijednost(config.doseg)
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[0].kod)
        cvor_stabla.labela = cvor_stabla.lista_djece[0].labela
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
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[0].kod)
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[2].kod)

        cvor_stabla.dodaj_kod("\tPOP R0\n")
        cvor_stabla.dodaj_kod("\tPOP R1\n")

        if cvor_stabla.lista_djece[1].podaci.startswith("PLUS"):
            cvor_stabla.dodaj_kod("\tADD R0, R1, R0\n")
        else:
            cvor_stabla.dodaj_kod("\tSUB R1, R0, R0\n")
        cvor_stabla.dodaj_kod("\tPUSH R0\n")
    return


def odnosni_izraz(cvor_stabla):
    #print("U odnosni izraz metodi")
    if len(cvor_stabla.lista_djece) == 1:
        aditivni_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.postavi_tip(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
        cvor_stabla.lista_tipova = cvor_stabla.lista_djece[0].vrati_tipove(config.doseg)
        cvor_stabla.ime = cvor_stabla.lista_djece[0].vrati_ime()
        cvor_stabla.je_l_vrijednost = cvor_stabla.lista_djece[0].vrati_l_vrijednost(config.doseg)
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[0].kod)
        cvor_stabla.labela = cvor_stabla.lista_djece[0].labela
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
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[0].kod)
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[2].kod)
        cvor_stabla.dodaj_kod("\tPOP R1\n")
        cvor_stabla.dodaj_kod("\tPOP R0\n")
        cvor_stabla.dodaj_kod("\tCMP R0, R1\n")
        mapa = {}
        mapa["<"] = "SLT"
        mapa[">"] = "SGT"
        mapa["<="] = "SLE"
        mapa[">="] = "SGE"

        cvor_stabla.dodaj_kod("\tJP_" + mapa[cvor_stabla.lista_djece[1].vrati_ime()] + " " + "TRUE"+ str(config.if_counter_label) + "\n")
        cvor_stabla.dodaj_kod("FALSE" + str(config.if_counter_label) + "\n")
        cvor_stabla.dodaj_kod("\tMOVE 0, R2\n")
        cvor_stabla.dodaj_kod("\tJP " + "ENDIF" + str(config.if_counter_label) + "\n")
        config.if_counter_label += 1
        cvor_stabla.appendKod("TRUE" + str(config.if_counter_label) + "\n")
        cvor_stabla.appendKod("\tMOVE 1, R2\n")
        cvor_stabla.appendKod("ENDIF" + str(config.if_counter_label) + "\n")
        cvor_stabla.appendKod("\tPUSH R2\n")

    return


def jednakosni_izraz(cvor_stabla):
    #print("U jednakosni izraz metodi")
    if len(cvor_stabla.lista_djece) == 1:
        odnosni_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.postavi_tip(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
        cvor_stabla.lista_tipova = cvor_stabla.lista_djece[0].vrati_tipove(config.doseg)
        cvor_stabla.ime = cvor_stabla.lista_djece[0].vrati_ime()
        cvor_stabla.je_l_vrijednost = cvor_stabla.lista_djece[0].vrati_l_vrijednost(config.doseg)
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[0].kod)
        cvor_stabla.labela = cvor_stabla.lista_djece[0].labela
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
    #print("U bin i izraz metodi")
    if len(cvor_stabla.lista_djece) == 1:
        jednakosni_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.postavi_tip(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
        cvor_stabla.lista_tipova = cvor_stabla.lista_djece[0].vrati_tipove(config.doseg)
        cvor_stabla.ime = cvor_stabla.lista_djece[0].vrati_ime()
        cvor_stabla.je_l_vrijednost = cvor_stabla.lista_djece[0].vrati_l_vrijednost(config.doseg)
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[0].kod)
        cvor_stabla.labela = cvor_stabla.lista_djece[0].labela
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
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[0].kod)
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[2].kod)
        cvor_stabla.dodaj_kod("\tPOP R0\n\tPOP R1\n");
        cvor_stabla.dodaj_kod("\tAND R0, R1, R0\n");
        cvor_stabla.dodaj_kod("\tPUSH R0\n");

    return


def bin_xili_izraz(cvor_stabla):
    #print("U bin xili izraz metodi")
    if len(cvor_stabla.lista_djece) == 1:
        bin_i_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.postavi_tip(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
        cvor_stabla.lista_tipova = cvor_stabla.lista_djece[0].vrati_tipove(config.doseg)
        cvor_stabla.ime = cvor_stabla.lista_djece[0].vrati_ime()
        cvor_stabla.je_l_vrijednost = cvor_stabla.lista_djece[0].vrati_l_vrijednost(config.doseg)
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[0].kod)
        cvor_stabla.labela = cvor_stabla.lista_djece[0].labela
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
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[0].kod)
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[2].kod)
        cvor_stabla.dodaj_kod("\tPOP R0\n\tPOP R1\n");
        cvor_stabla.dodaj_kod("\tXOR R0, R1, R0\n");
        cvor_stabla.dodaj_kod("\tPUSH R0\n");
    return


def bin_ili_izraz(cvor_stabla):
    #print("U bin ili izraz metodi")
    if len(cvor_stabla.lista_djece) == 1:
        bin_xili_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.postavi_tip(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
        cvor_stabla.lista_tipova = cvor_stabla.lista_djece[0].vrati_tipove(config.doseg)
        cvor_stabla.ime = cvor_stabla.lista_djece[0].vrati_ime()
        cvor_stabla.je_l_vrijednost = cvor_stabla.lista_djece[0].vrati_l_vrijednost(config.doseg)
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[0].kod)
        cvor_stabla.labela = cvor_stabla.lista_djece[0].labela
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
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[0].kod)
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[2].kod)
        cvor_stabla.dodaj_kod("\tPOP R0\n\tPOP R1\n");
        cvor_stabla.dodaj_kod("\tOR R0, R1, R0\n");
        cvor_stabla.dodaj_kod("\tPUSH R0\n");
    return


def log_i_izraz(cvor_stabla):
    #print("U log i izraz metodi")
    if len(cvor_stabla.lista_djece) == 1:
        bin_ili_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.postavi_tip(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
        cvor_stabla.lista_tipova = cvor_stabla.lista_djece[0].vrati_tipove(config.doseg)
        cvor_stabla.ime = cvor_stabla.lista_djece[0].vrati_ime()
        cvor_stabla.je_l_vrijednost = cvor_stabla.lista_djece[0].vrati_l_vrijednost(config.doseg)
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[0].kod)
        cvor_stabla.labela = cvor_stabla.lista_djece[0].labela
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
    #print("U log ili izraz metodi")
    if len(cvor_stabla.lista_djece) == 1:
        log_i_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.postavi_tip(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
        cvor_stabla.lista_tipova = cvor_stabla.lista_djece[0].vrati_tipove(config.doseg)
        cvor_stabla.ime = cvor_stabla.lista_djece[0].vrati_ime()
        cvor_stabla.je_l_vrijednost = cvor_stabla.lista_djece[0].vrati_l_vrijednost(config.doseg)
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[0].kod)
        cvor_stabla.labela = cvor_stabla.lista_djece[0].labela
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
    #print("U izraz pridruzivanja metodi")
    if len(cvor_stabla.lista_djece) == 1:
        log_ili_izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.postavi_tip(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
        cvor_stabla.lista_tipova = cvor_stabla.lista_djece[0].vrati_tipove(config.doseg)
        cvor_stabla.ime = cvor_stabla.lista_djece[0].vrati_ime()
        cvor_stabla.je_l_vrijednost = cvor_stabla.lista_djece[0].vrati_l_vrijednost(config.doseg)
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[0].kod)
        cvor_stabla.labela = cvor_stabla.lista_djece[0].labela
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
        loop = 0
        while loop < (len(cvor_stabla.lista_djece[0].kod.split("\n")) - 2):
            loop +=1 #ILI POSLIJE
            cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[0].kod.split("\n")[loop] + "\n")
        cvor_stabla.dodaj_kod("\tPUSH R0\n")
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[2].kod)
        cvor_stabla.dodaj_kod("\tPOP R1\n")
        cvor_stabla.dodaj_kod("\tPOP R0\n")
        cvor_stabla.dodaj_kod("\tSTORE R1, (R0)\n")

    return


def izraz(cvor_stabla):
    #print("U izraz metodi")
    if len(cvor_stabla.lista_djece) == 1:
        izraz_pridruzivanja(cvor_stabla.lista_djece[0])
        if config.error:
            return
        
        cvor_stabla.postavi_tip(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
        cvor_stabla.lista_tipova = cvor_stabla.lista_djece[0].vrati_tipove(config.doseg)
        cvor_stabla.ime = cvor_stabla.lista_djece[0].vrati_ime()
        cvor_stabla.je_l_vrijednost = cvor_stabla.lista_djece[0].vrati_l_vrijednost(config.doseg)
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[0].kod)

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
