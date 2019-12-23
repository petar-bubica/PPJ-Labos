import config
import PomocneFunkcije
import Izrazi
import Deklaracije_I_Definicije
from CvorStabla import CvorStabla
from CvorTablice import CvorTablice


def slozena_naredba(cvor_stabla):
    print("U slozena naredba metodi")

    kopija_dosega = CvorTablice(config.doseg.roditelj)
    kopija_dosega.lista_deklaracija = config.doseg.lista_deklaracija

    if config.doseg.je_u_petlji:
        kopija_dosega.je_u_petlji = True

    novi_doseg = CvorTablice(kopija_dosega)
    if cvor_stabla.je_u_petlji or config.doseg.je_u_petlji:
        novi_doseg.je_u_petlji = True
    config.doseg = novi_doseg

    if cvor_stabla.je_u_petlji:
        config.doseg.je_u_petlji = True

    for i in range(len(cvor_stabla.vrati_tipove(config.doseg))):

        novi_cvor = CvorStabla(-1, '<' + cvor_stabla.lista_imena[i])
        novi_cvor.postavi_tip(cvor_stabla.vrati_tipove(config.doseg)[i])

        if cvor_stabla.je_u_petlji:
            novi_cvor.je_u_petlji = True

        novi_cvor.ime = cvor_stabla.lista_imena[i]
        config.doseg.lista_deklaracija.append(novi_cvor)

    if len(cvor_stabla.lista_djece) == 3:
        lista_naredbi(cvor_stabla.lista_djece[1])
        if config.error:
            return
    else:
        if cvor_stabla.je_u_petlji:
            cvor_stabla.lista_djece[1].je_u_petlji = True

        Deklaracije_I_Definicije.lista_deklaracija(cvor_stabla.lista_djece[1])
        if config.error:
            return

        lista_naredbi(cvor_stabla.lista_djece[2])
        if config.error:
            return

    config.doseg = config.doseg.roditelj
    return


def lista_naredbi(cvor_stabla):
    print("U lista naredbi metodi")
    if len(cvor_stabla.lista_djece) == 1:
       naredba(cvor_stabla.lista_djece[0])
       if config.error:
           return
    elif len(cvor_stabla.lista_djece) > 1:
        lista_naredbi(cvor_stabla.lista_djece[0])
        if config.error:
            return
        naredba((cvor_stabla.lista_djece[1]))
        if config.error:
            return
    return


def naredba(cvor_stabla):
    print("U naredba metodi")

    desna_strana = cvor_stabla.lista_djece[0]
    if cvor_stabla.je_u_petlji:
        desna_strana.je_u_petlji = True

    podaci_desne_strane = desna_strana.podaci

    if podaci_desne_strane == '<slozena_naredba>':
        slozena_naredba(desna_strana)
    if podaci_desne_strane == '<izraz_naredba>':
        izraz_naredba(desna_strana)
    if podaci_desne_strane == '<naredba_grananja>':
        naredba_grananja(desna_strana)
    if podaci_desne_strane == '<naredba_petlje>':
        naredba_petlje(desna_strana)
    if podaci_desne_strane == '<naredba_skoka>':
        naredba_skoka(desna_strana)

    if config.error:
        return

    return


def izraz_naredba(cvor_stabla):
    print("U izraz naredba metodi")
    if len(cvor_stabla.lista_djece) == 1:
        cvor_stabla.postavi_tip("int")
    else:
        Izrazi.izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.postavi_tip(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
        cvor_stabla.lista_tipova = cvor_stabla.lista_djece[0].vrati_tipove(config.doseg)
        cvor_stabla.ime = cvor_stabla.lista_djece[0].vrati_ime()

    return


def naredba_grananja(cvor_stabla):
    print("U naredba grananja metodi")

    Izrazi.izraz(cvor_stabla.lista_djece[2])
    if config.error:
        return

    if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[2].vrati_tip(config.doseg), 'int') or len(cvor_stabla.lista_djece[2].lista_tipova) != 0:
        PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
        return

    naredba(cvor_stabla.lista_djece[4])
    if config.error:
        return

    if len(cvor_stabla.lista_djece) > 5:
        naredba(cvor_stabla.lista_djece[6])
        if config.error:
            return

    return


def naredba_petlje(cvor_stabla):
    print("U naredba petlje metodi")

    if len(cvor_stabla.lista_djece) == 5:

        Izrazi.izraz(cvor_stabla.lista_djece[2])
        if config.error:
            return

        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[2].vrati_tip(config.doseg), 'int') or len(cvor_stabla.lista_djece[2].lista_tipova) != 0:
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return

        cvor_stabla.lista_djece[4].je_u_petlji = True

        naredba(cvor_stabla.lista_djece[4])
        if config.error:
            return

    if len(cvor_stabla.lista_djece) == 6:

        izraz_naredba(cvor_stabla.lista_djece[2])
        if config.error:
            return

        izraz_naredba(cvor_stabla.lista_djece[3])
        if config.error:
            return

        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[3].vrati_tip(config.doseg), 'int') or len(cvor_stabla.lista_djece[3].lista_tipova) != 0:
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return

        cvor_stabla.lista_djece[5].je_u_petlji = True

        naredba(cvor_stabla.lista_djece[5])
        if config.error:
            return

    if len(cvor_stabla.lista_djece) == 7:

        izraz_naredba(cvor_stabla.lista_djece[2])
        if config.error:
            return

        izraz_naredba(cvor_stabla.lista_djece[3])
        if config.error:
            return

        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[3].vrati_tip(config.doseg), 'int') or len(cvor_stabla.lista_djece[3].lista_tipova) != 0:
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return

        Izrazi.izraz(cvor_stabla.lista_djece[4])
        if config.error:
            return

        cvor_stabla.lista_djece[6].je_u_petlji = True

        naredba(cvor_stabla.lista_djece[6])
        if config.error:
            return

    return


def naredba_skoka(cvor_stabla):
    print("U naredba skoka metodi")

    if len(cvor_stabla.lista_djece) == 3:

        Izrazi.izraz(cvor_stabla.lista_djece[1])
        if config.error:
            return

        tip = PomocneFunkcije.vrati_tip_trenutne_funkcije()

        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[1].vrati_tip(config.doseg), tip) or len(cvor_stabla.lista_djece[1].lista_tipova) != 0:
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return

    else:
        if cvor_stabla.lista_djece[0].podaci.startswith('KR_RETURN'):
            if PomocneFunkcije.vrati_tip_trenutne_funkcije() != 'void':
                PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
                return
        else:
            if not config.doseg.je_u_petlji:
                PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
                return

    return


def prijevodna_jedinica(cvor_stabla):
    print("U prijevodna jedinica metodi")
    if len(cvor_stabla.lista_djece) == 1:
        vanjska_deklaracija(cvor_stabla.lista_djece[0])
        if config.error:
            return
    elif len(cvor_stabla.lista_djece) > 1:
        prijevodna_jedinica(cvor_stabla.lista_djece[0])
        if config.error:
            return
        vanjska_deklaracija(cvor_stabla.lista_djece[1])
        if config.error:
            return
    return


def vanjska_deklaracija(cvor_stabla):
    print("U vanjska deklaracija metodi")
    if cvor_stabla.lista_djece[0].podaci == '<definicija_funkcije>':
        Deklaracije_I_Definicije.definicija_funkcije(cvor_stabla.lista_djece[0])
        if config.error:
            return
    else:
        Deklaracije_I_Definicije.deklaracija(cvor_stabla.lista_djece[0])
        if config.error:
            return
    return
