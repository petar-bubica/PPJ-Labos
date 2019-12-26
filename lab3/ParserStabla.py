import sys
import config
from CvorStabla import CvorStabla


def parsiraj():
    #print("U parsiraj metodi")
    ulaz = sys.stdin.read().splitlines()

    korijen_stabla = CvorStabla(ulaz[0], 0)
    cvor_roditelj = korijen_stabla

    lista_cvorova = list()
    lista_cvorova.append(cvor_roditelj)

    brojac_redova = 0

    for linija in ulaz:
        if linija.startswith(" "):

            brojac_praznina = 0
            brojac_redova += 1

            for znak in linija:
                if znak == ' ':
                    brojac_praznina += 1
                else:
                    break

            cvor = CvorStabla(ulaz[brojac_redova], brojac_praznina)
            lista_cvorova.append(cvor)

            cvor_roditelj = nadji_roditelja(cvor, lista_cvorova)
            cvor_roditelj.dodaj_dijete(cvor)

    config.korijen = korijen_stabla
    korijen_stabla.ispisi_podstablo(korijen_stabla)


def nadji_roditelja(cvor, lista_cvorova):
    #print("U nadi roditelje metodi")
    zapamti = None

    for cvor_roditelj in lista_cvorova:
        if cvor_roditelj.dubina == (cvor.dubina - 1):
            zapamti = cvor_roditelj

    return zapamti
