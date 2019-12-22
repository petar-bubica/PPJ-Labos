import config
import PomocneFunkcije
import Izrazi
import NaredbenaStruktura
from CvorStabla import CvorStabla
from CvorTablice import CvorTablice


def definicija_funkcije(cvor_stabla):
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
        config.doseg.lista_deklaracija.append(cvor_stabla)
        config.definirane_funkcije.append(cvor_stabla.vrati_ime())
        NaredbenaStruktura.slozena_naredba(cvor_stabla.lista_djece[5])
        if config.error:
            return
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
        config.definirane_funkcije.append(cvor_stabla.vrati_ime())
        config.doseg.lista_deklaracija.append(cvor_stabla)
        NaredbenaStruktura.slozena_naredba(cvor_stabla.lista_djece[5])
        if config.error:
            return
    return


def deklaracija_parametara(cvor_stabla):
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
    if len(cvor_stabla.lista_djece) == 1:
        if cvor_stabla.je_u_petlji:
            cvor_stabla.lista_djece[0].je_u_petlji = True
        deklaracija(cvor_stabla.lista_djece[0])
    elif len(cvor_stabla.lista_djece) > 1:
        if cvor_stabla.je_u_petlji:
            cvor_stabla.lista_djece[0].je_u_petlji = True
            cvor_stabla.lista_djece[1].je_u_petlji = False
        lista_deklaracija(cvor_stabla.lista_djece[0])
        deklaracija(cvor_stabla.lista_djece[1])
    return


def deklaracija(cvor_stabla):
    Izrazi.ime_tipa(cvor_stabla.lista_djece[0])
    if config.error:
        return
    cvor_stabla.lista_djece[1].postavi_tip(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
    if cvor_stabla.lista_djece[0].je_konstanta:
        cvor_stabla.lista_djece[1].je_konstanta = True
    if cvor_stabla.je_u_petlji:
        cvor_stabla.lista_djece[1].je_u_petlji = True
    lista_init_deklaratora(cvor_stabla.lista_djece[1])
    return


def lista_init_deklaratora(cvor_stabla):
    if len(cvor_stabla.lista_djece) == 1:
        cvor_stabla.lista_djece[0].postavi_tip(cvor_stabla.vrati_tip(config.doseg))
        if cvor_stabla.je_konstanta:
            cvor_stabla.lista_djece[0].je_konstanta = True
        if cvor_stabla.je_u_petlji:
            cvor_stabla.lista_djece[0].je_u_petlji = True
        init_deklarator(cvor_stabla.lista_djece[0])
        if config.error:
            return
    elif len(cvor_stabla.lista_djece) > 1:
        cvor_stabla.lista_djece[0].postavi_tip(cvor_stabla.vrati_tip(config.doseg))
        if cvor_stabla.je_konstanta:
            cvor_stabla.lista_djece[0].je_konstanta = True
        if cvor_stabla.je_u_petlji:
            cvor_stabla.lista_djece[0].je_u_petlji = True
        lista_init_deklaratora(cvor_stabla.lista_djece[0])
        if config.error:
            return

        cvor_stabla.lista_djece[2].postavi_tip(cvor_stabla.vrati_tip(config.doseg))
        if cvor_stabla.je_konstanta:
            cvor_stabla.lista_djece[2].je_konstanta = True
        if cvor_stabla.je_u_petlji:
            cvor_stabla.lista_djece[2].je_u_petlji = True
        init_deklarator(cvor_stabla.lista_djece[2])
        if config.error:
            return
    return


def init_deklarator(cvor_stabla):
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
    elif len(cvor_stabla.lista_djece) > 1:
        inicijalizator(cvor_stabla.lista_djece[2])
        if config.error:
            return
        if cvor_stabla.lista_djece[0].tip.startswith("niz"):
            if cvor_stabla.lista_djece[0].velicina_niza <= cvor_stabla.lista_djece[2].velicina_niza:
                config.error = True
            for tip in cvor_stabla.lista_djece[2].vrati_tipove(config.doseg):
                if not PomocneFunkcije.je_castable(tip, cvor_stabla.lista_djece[0].vrati_tip(config.doseg)[:3]):
                    config.error = True
            if config.error:
                PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
                return
        else:
            if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[2].vrati_tip(config.doseg), cvor_stabla.lista_djece[0].vrati_tip(config.doseg)) or cvor_stabla.lista_djece[2].je_funkcija():
                PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
                return
    return


def izravni_deklarator(cvor_stabla):
    if len(cvor_stabla.lista_djece) == 1:
        if cvor_stabla.vrati_tip(config.doseg) == "void" or PomocneFunkcije.je_deklarirano_lokalno(cvor_stabla.lista_djece[0].vrati_ime()):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        cvor_stabla.je_definiran = True
        cvor_stabla.ime = cvor_stabla.lista_djece[0].vrati_ime()
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
        config.doseg.lista_deklaracija.append(cvor_stabla)
    elif cvor_stabla.lista_djece[2].podaci.startswith("KR_VOID"):
        lokalna_deklaracija = PomocneFunkcije.vrati_lokalnu_deklaraciju(cvor_stabla.lista_djece[0].vrati_ime())
        if lokalna_deklaracija is None:
            cvor_stabla.lista_tipova.append("void")
            cvor_stabla.ime = cvor_stabla.lista_djece[0].vrati_ime()
            config.doseg.lista_deklaracija.append(cvor_stabla)
            config.deklarirane_funkcije.append(cvor_stabla.vrati_ime())
        else:
             if len(lokalna_deklaracija.vrati_tipove(config.doseg)) != 1 or not (lokalna_deklaracija.lista_tipova[0] == "void"):
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
            config.doseg.lista_deklaracija.append(cvor_stabla)
    return


def inicijalizator(cvor_stabla):
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
    elif len(cvor_stabla.lista_djece) > 1:
        lista_izraza_pridruzivanja(cvor_stabla.lista_djece[1])
        if config.error:
            return
        cvor_stabla.velicina_niza = cvor_stabla.lista_djece[1].velicina_niza
        cvor_stabla.lista_tipova = cvor_stabla.lista_djece[1].vrati_tipove(config.doseg)
        cvor_stabla.ime = cvor_stabla.lista_djece[1].vrati_ime()
    return


def lista_izraza_pridruzivanja(cvor_stabla):
    if len(cvor_stabla.lista_djece) == 1:
        Izrazi.izraz_pridruzivanja(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.lista_tipova.append(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
        cvor_stabla.velicina_niza = 1
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
    return
