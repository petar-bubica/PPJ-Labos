from lab4 import config
from lab4 import PomocneFunkcije
from lab4 import Izrazi
from lab4 import NaredbenaStruktura
from lab4.CvorStabla import CvorStabla
from lab4.CvorTablice import CvorTablice
from lab4.CvorTabliceUpgrade import CvorTabliceUpgrade


def definicija_funkcije(cvor_stabla):
    #print("U definicija funkcije metodi")
    Izrazi.ime_tipa(cvor_stabla.lista_djece[0])
    if cvor_stabla.lista_djece[0].je_konstanta:
        PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
        return
    if PomocneFunkcije.funkcija_vec_postoji(config.doseg, cvor_stabla.lista_djece[1].vrati_ime()):
        PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
        return
    if cvor_stabla.lista_djece[3].podaci.startswith("KR_VOID"):
        if PomocneFunkcije.konfliktna_deklaracija(config.doseg, cvor_stabla.lista_djece[0].vrati_ime(), cvor_stabla.lista_djece[0].vrati_tip(config.doseg)):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        cvor_stabla.je_definiran = True
        cvor_stabla.ime = cvor_stabla.lista_djece[1].vrati_ime()
        cvor_stabla.postavi_tip(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
        cvor_stabla.lista_tipova.append("void")
        if cvor_stabla.vrati_ime() == "main" and cvor_stabla.vrati_tip(config.doseg) == "int":
            config.nema_main = False
        #print('doseg.lista dekl:', config.doseg.lista_deklaracija)
        config.doseg.lista_deklaracija.append(cvor_stabla)
        config.definirane_funkcije.append(cvor_stabla.vrati_ime())
        NaredbenaStruktura.slozena_naredba(cvor_stabla.lista_djece[5])
        if config.error:
            return
        if cvor_stabla.lista_djece[1].vrati_ime() == "main":
            cvor_stabla.labela = "MAIN"
        else:
            cvor_stabla.labela = "F" + str(config.function_counter_label)
            config.function_counter_label += 1
        cvor_stabla.dodaj_kod(cvor_stabla.labela)
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[5].kod)
        novi = CvorTabliceUpgrade(cvor_stabla.labela, cvor_stabla)
        novi.je_fja = True
        config.tabela.append(novi)
    else:
        lista_parametara(cvor_stabla.lista_djece[3])
        if config.error:
            return
        if PomocneFunkcije.konfliktna_deklaracija(config.doseg, cvor_stabla.vrati_ime(), cvor_stabla.vrati_tip(config.doseg)):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        cvor_stabla.je_definiran = True
        cvor_stabla.postavi_tip(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
        cvor_stabla.ime = cvor_stabla.lista_djece[1].vrati_ime()
        cvor_stabla.lista_djece[5].lista_tipova = cvor_stabla.lista_djece[3].vrati_tipove(config.doseg)
        cvor_stabla.lista_tipova = cvor_stabla.lista_djece[3].vrati_tipove(config.doseg)
        cvor_stabla.lista_djece[5].lista_imena = cvor_stabla.lista_djece[3].lista_imena
        cvor_stabla.lista_imena = cvor_stabla.lista_djece[3].lista_imena
        if cvor_stabla.lista_djece[1].vrati_ime() == "main":
            cvor_stabla.labela = "MAIN"
        else:
            cvor_stabla.labela = "F" + str(config.function_counter_label)
            config.function_counter_label += 1
        cvor_stabla.dodaj_kod(cvor_stabla.labela)
        config.definirane_funkcije.append(cvor_stabla.vrati_ime())
        #print('doseg.lista dekl:', config.doseg.lista_deklaracija)
        config.doseg.lista_deklaracija.append(cvor_stabla)
        NaredbenaStruktura.slozena_naredba(cvor_stabla.lista_djece[5])
        if config.error:
            return
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[5].kod)
        if cvor_stabla.lista_djece[0].vrati_ime() == "void":
            cvor_stabla.dodaj_kod("\tRET\n")
        novi = CvorTabliceUpgrade(cvor_stabla.labela, cvor_stabla)
        novi.je_fja = True
        config.tabela.append(novi)
    return


def deklaracija_parametara(cvor_stabla):
    #print("U deklaracija parametara metodi")
    Izrazi.ime_tipa(cvor_stabla.lista_djece[0])
    if config.error:
        return
    if cvor_stabla.lista_djece[0].vrati_tip(config.doseg) == "void":
        PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
        return
    if len(cvor_stabla.lista_djece) == 2:
        cvor_stabla.postavi_tip(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
    else:
        cvor_stabla.postavi_tip("niz" + cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
    cvor_stabla.ime = cvor_stabla.lista_djece[1].vrati_ime()
    return


def lista_parametara(cvor_stabla):
    #print("U lista parametara metodi")
    if len(cvor_stabla.lista_djece) == 1:
        deklaracija_parametara(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.lista_tipova.append(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
        cvor_stabla.dodaj_ime(cvor_stabla.lista_djece[0].vrati_ime())
    elif len(cvor_stabla.lista_djece) > 1:
        lista_parametara(cvor_stabla.lista_djece[0])
        if config.error:
            return
        deklaracija_parametara(cvor_stabla.lista_djece[2])
        if config.error:
            return
        if cvor_stabla.lista_djece[2].vrati_ime() in cvor_stabla.lista_djece[0].lista_imena:
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        cvor_stabla.lista_tipova = cvor_stabla.lista_djece[0].vrati_tipove(config.doseg)
        cvor_stabla.lista_tipova.append(cvor_stabla.lista_djece[2].vrati_tip(config.doseg))
        cvor_stabla.lista_imena = cvor_stabla.lista_djece[0].lista_imena
        cvor_stabla.dodaj_ime(cvor_stabla.lista_djece[2].vrati_ime())
    return


def lista_deklaracija(cvor_stabla):
    #print("U lista deklaracija metodi")
    if len(cvor_stabla.lista_djece) == 1:
        if cvor_stabla.je_u_petlji:
            cvor_stabla.lista_djece[0].je_u_petlji = True
        deklaracija(cvor_stabla.lista_djece[0])
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[0].kod)
    elif len(cvor_stabla.lista_djece) > 1:
        if cvor_stabla.je_u_petlji:
            cvor_stabla.lista_djece[0].je_u_petlji = True
            cvor_stabla.lista_djece[1].je_u_petlji = False
        lista_deklaracija(cvor_stabla.lista_djece[0])
        deklaracija(cvor_stabla.lista_djece[1])
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[0].kod)
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[1].kod)
    return


def deklaracija(cvor_stabla):
    #print("U deklaracija metodi")
    Izrazi.ime_tipa(cvor_stabla.lista_djece[0])
    if config.error:
        return
    cvor_stabla.lista_djece[1].postavi_tip(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
    if cvor_stabla.lista_djece[0].je_konstanta:
        cvor_stabla.lista_djece[1].je_konstanta = True
    if cvor_stabla.je_u_petlji:
        cvor_stabla.lista_djece[1].je_u_petlji = True
    lista_init_deklaratora(cvor_stabla.lista_djece[1])
    cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[1].kod)
    return


def lista_init_deklaratora(cvor_stabla):
    #print("U lista init deklaratora metodi")
    if len(cvor_stabla.lista_djece) == 1:
        cvor_stabla.lista_djece[0].postavi_tip(cvor_stabla.vrati_tip(config.doseg))
        if cvor_stabla.je_konstanta:
            cvor_stabla.lista_djece[0].je_konstanta = True
        if cvor_stabla.je_u_petlji:
            cvor_stabla.lista_djece[0].je_u_petlji = True
        init_deklarator(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[0].kod)
    elif len(cvor_stabla.lista_djece) > 1:
        cvor_stabla.lista_djece[0].postavi_tip(cvor_stabla.vrati_tip(config.doseg))
        if cvor_stabla.je_konstanta:
            cvor_stabla.lista_djece[0].je_konstanta = True
        if cvor_stabla.je_u_petlji:
            cvor_stabla.lista_djece[0].je_u_petlji = True
        lista_init_deklaratora(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[0].kod)

        cvor_stabla.lista_djece[2].postavi_tip(cvor_stabla.vrati_tip(config.doseg))
        if cvor_stabla.je_konstanta:
            cvor_stabla.lista_djece[2].je_konstanta = True
        if cvor_stabla.je_u_petlji:
            cvor_stabla.lista_djece[2].je_u_petlji = True
        init_deklarator(cvor_stabla.lista_djece[2])
        if config.error:
            return
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[2].kod)
    return


def init_deklarator(cvor_stabla):
    #print("U init deklarator metodi")
    cvor_stabla.lista_djece[0].postavi_tip(cvor_stabla.vrati_tip(config.doseg))
    if cvor_stabla.je_konstanta:
        cvor_stabla.lista_djece[0].je_konstanta = True
    if cvor_stabla.je_u_petlji:
        cvor_stabla.lista_djece[0].je_u_petlji = True
    izravni_deklarator(cvor_stabla.lista_djece[0])
    if config.error:
        return
    if len(cvor_stabla.lista_djece) == 1:
        if cvor_stabla.lista_djece[0].je_konstanta:
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[0].kod)
        if cvor_stabla.lista_djece[0].tip.startswith("niz"):
            for i in range(cvor_stabla.lista_djece[0].velicina_niza):
                labela = "L" + str(config.brojac_labela)
                config.brojac_labela += 1
                if i == 0:
                    cvor_stabla.labela = labela
                novi = CvorTabliceUpgrade(labela, None)
                novi.je_prazno = True
                config.tabela.append(novi)
            config.doseg.lista_deklaracija[len(config.doseg.lista_deklaracija)-1].labela = cvor_stabla.labela
    elif len(cvor_stabla.lista_djece) > 1:
        inicijalizator(cvor_stabla.lista_djece[2])
        if config.error:
            return
        if cvor_stabla.lista_djece[0].tip.startswith("niz"):
            if cvor_stabla.lista_djece[0].velicina_niza <= cvor_stabla.lista_djece[2].velicina_niza:
                config.error = True
            for tip in cvor_stabla.lista_djece[2].vrati_tipove(config.doseg):
                if not PomocneFunkcije.je_castable(tip, cvor_stabla.lista_djece[0].vrati_tip(config.doseg)[3:]):
                    config.error = True
            if config.error:
                PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
                return
            cvor_stabla.labela = cvor_stabla.lista_djece[2].labela
            config.doseg.lista_deklaracija[len(config.doseg.lista_deklaracija) - 1].labela = cvor_stabla.labela
        else:
            if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[2].vrati_tip(config.doseg), cvor_stabla.lista_djece[0].vrati_tip(config.doseg)) or cvor_stabla.lista_djece[2].je_funkcija():
                PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
                return
            cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[2].kod)
            labela = cvor_stabla.lista_djece[0].labela
            cvor_stabla.dodaj_kod("\tLOAD R0, (R7)\n");
            cvor_stabla.dodaj_kod("\tSTORE R0, (" + labela + ")\n");
            cvor_stabla.dodaj_kod("\tADD R7, 4, R7\n");
            novi = CvorTabliceUpgrade(labela,cvor_stabla)
            novi.je_prazno = True
            config.tabela.append(novi)
            cvor_stabla.labela = labela
    return


def izravni_deklarator(cvor_stabla):
    #print("U izravni deklarator metodi")
    if len(cvor_stabla.lista_djece) == 1:
        if cvor_stabla.vrati_tip(config.doseg) == "void" or PomocneFunkcije.je_deklarirano_lokalno(cvor_stabla.lista_djece[0].vrati_ime()):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        cvor_stabla.je_definiran = False
        cvor_stabla.ime = cvor_stabla.lista_djece[0].vrati_ime()
        labela = "L" + str(config.brojac_labela)
        cvor_stabla.labela = labela
        #print('doseg.lista dekl:', config.doseg.lista_deklaracija)
        config.doseg.lista_deklaracija.append(cvor_stabla)
        return
    elif cvor_stabla.lista_djece[2].podaci.startswith("BROJ"):
        if cvor_stabla.vrati_tip(config.doseg) == "void" or PomocneFunkcije.je_deklarirano_lokalno(cvor_stabla.vrati_ime()):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        if cvor_stabla.lista_djece[2].dohvati_vrijednost_broja() <= 0 or cvor_stabla.lista_djece[2].dohvati_vrijednost_broja() > 1024:
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        cvor_stabla.postavi_tip("niz" + cvor_stabla.vrati_tip(config.doseg))
        cvor_stabla.velicina_niza = cvor_stabla.lista_djece[2].dohvati_vrijednost_broja()
        cvor_stabla.ime = cvor_stabla.lista_djece[0].vrati_ime()
        #print('doseg.lista dekl:', config.doseg.lista_deklaracija)
        config.doseg.lista_deklaracija.append(cvor_stabla)
    elif cvor_stabla.lista_djece[2].podaci.startswith("KR_VOID"):
        lokalna_deklaracija = PomocneFunkcije.vrati_lokalnu_deklaraciju(cvor_stabla.lista_djece[0].vrati_ime())
        if lokalna_deklaracija is None:
            cvor_stabla.lista_tipova.append("void")
            cvor_stabla.ime = cvor_stabla.lista_djece[0].vrati_ime()
            #print('doseg.lista dekl:', config.doseg.lista_deklaracija)
            config.doseg.lista_deklaracija.append(cvor_stabla)
            config.deklarirane_funkcije.append(cvor_stabla.vrati_ime())
        else:
             if len(lokalna_deklaracija.vrati_tipove(config.doseg)) != 1 or lokalna_deklaracija.lista_tipova[0] != "void":
                 PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
                 return
             cvor_stabla.ime = cvor_stabla.lista_djece[0].vrati_ime()
             cvor_stabla.lista_tipova.append("void")
    elif cvor_stabla.lista_djece[2].podaci == "<lista_parametara>":
        lista_parametara(cvor_stabla.lista_djece[2])
        if config.error:
            return
        lokalna_deklaracija = PomocneFunkcije.vrati_lokalnu_deklaraciju(cvor_stabla.lista_djece[0].vrati_ime())
        if lokalna_deklaracija is not None:
            if not PomocneFunkcije.provjeri_tipove(lokalna_deklaracija, cvor_stabla.lista_djece[2]):
                PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
                return
            cvor_stabla.lista_tipova = cvor_stabla.lista_djece[2].vrati_tipove(config.doseg)
            cvor_stabla.ime = cvor_stabla.lista_djece[0].vrati_ime()
        else:
            cvor_stabla.ime = cvor_stabla.lista_djece[0].vrati_ime()
            cvor_stabla.lista_tipova = cvor_stabla.lista_djece[2].vrati_tipove(config.doseg)
            config.deklarirane_funkcije.append(cvor_stabla.vrati_ime())
            #print('doseg.lista dekl:', config.doseg.lista_deklaracija)
            config.doseg.lista_deklaracija.append(cvor_stabla)
    return


def inicijalizator(cvor_stabla):
    #print("U inicijalizator metodi")
    if len(cvor_stabla.lista_djece) == 1:
        Izrazi.izraz_pridruzivanja(cvor_stabla.lista_djece[0])
        if config.error:
            return
        if PomocneFunkcije.ide_u_niz_znakova(cvor_stabla.lista_djece[0]):
            cvor_stabla.velicina_niza = PomocneFunkcije.izracunaj_duljinu_znakova(cvor_stabla)
            for i in range(cvor_stabla.velicina_niza):
                cvor_stabla.lista_tipova.append("char")
        else:
            cvor_stabla.postavi_tip(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
            cvor_stabla.lista_tipova = cvor_stabla.lista_djece[0].vrati_tipove(config.doseg)
        cvor_stabla.ime = cvor_stabla.lista_djece[0].vrati_ime()
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[0].kod)
        cvor_stabla.labela = cvor_stabla.lista_djece[0].labela
    elif len(cvor_stabla.lista_djece) > 1:
        lista_izraza_pridruzivanja(cvor_stabla.lista_djece[1])
        if config.error:
            return
        cvor_stabla.velicina_niza = cvor_stabla.lista_djece[1].velicina_niza
        cvor_stabla.lista_tipova = cvor_stabla.lista_djece[1].vrati_tipove(config.doseg)
        cvor_stabla.ime = cvor_stabla.lista_djece[1].vrati_ime()
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[1].kod)
        cvor_stabla.labela = cvor_stabla.lista_djece[1].labela
    return


def lista_izraza_pridruzivanja(cvor_stabla):
    #print("U lista izraza pridruzivanja metodi")
    if len(cvor_stabla.lista_djece) == 1:
        Izrazi.izraz_pridruzivanja(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.lista_tipova.append(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
        cvor_stabla.velicina_niza = 1
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[0].kod)
        cvor_stabla.labela = cvor_stabla.lista_djece[0].labela
    elif len(cvor_stabla.lista_djece) > 1:
        lista_izraza_pridruzivanja(cvor_stabla.lista_djece[0])
        if config.error:
            return
        Izrazi.izraz_pridruzivanja(cvor_stabla.lista_djece[2])
        if config.error:
            return
        cvor_stabla.lista_tipova = cvor_stabla.lista_djece[0].vrati_tipove(config.doseg)
        cvor_stabla.lista_tipova.append(cvor_stabla.lista_djece[2].vrati_tip(config.doseg))
        cvor_stabla.velicina_niza = cvor_stabla.lista_djece[0].velicina_niza + 1
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[0].kod)
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[2].kod)
        cvor_stabla.labela = cvor_stabla.lista_djece[0].labela
    return
