import sys
from CvorStabla import CvorStabla


def parsiraj():
    ulaz = sys.stdin.read().splitlines()

    cvor_roditelj = CvorStabla(ulaz[0], 0)

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


def nadji_roditelja(cvor, lista_cvorova):
    zapamti = None

    for cvor_roditelj in lista_cvorova:
        if cvor_roditelj.dubina == (cvor.dubina - 1):
            zapamti = cvor_roditelj

    return zapamti


parsiraj()
