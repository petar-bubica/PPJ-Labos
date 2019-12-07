import sys
from automat import *
from funkcije import *
import pickle

# ulaz = sys.stdin.readlines()

f = open("./testovi/ppjC1.txt", "r")
ulaz = f.readlines()

nezavrsni_znakovi = ulaz[0][3:-1].split(' ')
pocetni_nezavrsni_znak = nezavrsni_znakovi[0]
zavrsni_znakovi = ulaz[1][3:-1].split(' ')
sinkronizacijski_znakovi = ulaz[2][5:-1].split(' ')
gramatika = {}
stari_prijelazi = []
prijelazi = []
stanje = ''
ima = False
lista_produkcija = []  # produkcije onim redom kako su zadane u datoteci

for red in ulaz[3:]:
    if red[0] == '<':
        stanje = red[:-1]
        ima = False
        prijelazi = []
        if stanje in gramatika:
            ima = True
            stari_prijelazi = gramatika[stanje]
    if red[0] == ' ':
        prijelazi.append((red[1:].rstrip()).split(' '))
        gramatika[stanje] = prijelazi
        for prijelaz in prijelazi:
            spremi = str(stanje) + '->' + ','.join(prijelaz)
            if spremi not in lista_produkcija:
                lista_produkcija.append(spremi)

    if ima == True:
        gramatika[stanje] = stari_prijelazi + prijelazi
        for prijelaz in prijelazi:
            spremi = str(stanje) + '->' + ','.join(prijelaz)
            if spremi not in lista_produkcija:
                lista_produkcija.append(spremi)

    else:
        gramatika[stanje] = prijelazi
        for prijelaz in prijelazi:
            spremi = str(stanje) + '->' + ','.join(prijelaz)
            if spremi not in lista_produkcija:
                lista_produkcija.append(spremi)

gramatika['<novop>'] = [[pocetni_nezavrsni_znak]]  # dodaj novi pocetni znak u gramatiku

eNKA = automat()
eNKA.dodaj_pocetno('<novop>' + '->' + "*" + "," + ','.join(gramatika['<novop>'][0]) + ",{#}")
eNKA.dodaj_prihvatljivo('<novop>' + "->" + pocetni_nezavrsni_znak + "," + "*" + "," + "{#}")
# racunanje prijelaza i odmah ljepljenje skupa T na stanje

treba_provjeriti = []
provjereno = []
treba_provjeriti = [eNKA.pocetno]

while treba_provjeriti != []:
    lista_trenutnog = treba_provjeriti[0].split('->')[1]
    lista_trenutnog = lista_trenutnog.split(',')

    index_tocke = lista_trenutnog.index('*')

    if lista_trenutnog[index_tocke + 1] in nezavrsni_znakovi or lista_trenutnog[index_tocke + 1] in zavrsni_znakovi:
        # uzimanje za zapocinje
        index_skupa = treba_provjeriti[0].index('{')
        cuvaj_skup = treba_provjeriti[0][index_skupa + 1:-1].split(',')
        prvi_dio = treba_provjeriti[0][:index_skupa - 1].split("->")
        desna_strana = prvi_dio[1]
        desna_strana = desna_strana.split(',')
        index_tocke = desna_strana.index('*')
        ZAPOCINJE = desna_strana[index_tocke + 2:]
        novi_skup = zapocinje_niz(ZAPOCINJE, gramatika, zavrsni_znakovi, nezavrsni_znakovi)

        # pravimo prijelaz bilo za zavrsni, bilo za nezavrsni znak
        lijeva_strana = prvi_dio[0]
        if desna_strana[:index_tocke]:
            nov_stanje = lijeva_strana + "->" + ",".join(desna_strana[:index_tocke]) + "," + desna_strana[
                index_tocke + 1] + "," + "*" + "," + ",".join(desna_strana[index_tocke + 2:])
        else:
            nov_stanje = lijeva_strana + "->" + desna_strana[
                index_tocke + 1] + "," + "*" + "," + ",".join(desna_strana[index_tocke + 2:])

        # moguce da ce trebat dodat jos zarez nakon svega prije skupa T
        if desna_strana[index_tocke + 2:]:
            nov_stanje = nov_stanje + ","
        nov_stanje = nov_stanje + treba_provjeriti[0][index_skupa:]
        eNKA.dodaj_prijelaz(treba_provjeriti[0], nov_stanje, desna_strana[index_tocke + 1])

        if nov_stanje not in provjereno:
            if nov_stanje not in treba_provjeriti:
                treba_provjeriti.append(nov_stanje)

        if lista_trenutnog[index_tocke + 1] in nezavrsni_znakovi:
            nez_znak = lista_trenutnog[index_tocke + 1]
            for produkcija in gramatika[nez_znak]:
                if produkcija == ['$']:
                    nov_stanje = nez_znak + "->" + "*"

                else:
                    nov_stanje = nez_znak + "->" + "*" + "," + ",".join(produkcija)

                # ako je prazan zapocinje ()
                if not novi_skup:
                    nov_stanje = nov_stanje + ",{"
                    for znak_T in cuvaj_skup:
                        if znak_T == cuvaj_skup[0]:
                            nov_stanje = nov_stanje + znak_T
                            continue
                        nov_stanje = nov_stanje + "," + znak_T
                    nov_stanje = nov_stanje + "}"
                    eNKA.dodaj_prijelaz(treba_provjeriti[0], nov_stanje, '$')

                else:
                    # ako nije prazan zapocinje () + ide u epsilon
                    if niz_ide_u_epsilon(desna_strana[index_tocke + 2:], gramatika, zavrsni_znakovi, nezavrsni_znakovi):
                        novi_skup = novi_skup | set(cuvaj_skup)
                    nov_stanje = nov_stanje + ",{"
                    # moguce pretvorit novi skup u listu, list()
                    for znak_T in list(novi_skup):
                        if znak_T == list(novi_skup)[0]:
                            nov_stanje = nov_stanje + znak_T
                            continue
                        nov_stanje = nov_stanje + "," + znak_T

                    nov_stanje = nov_stanje + "}"
                    # nov_stanje = nez_znak + "->" + "*" + "," + ",".join(produkcija)
                    eNKA.dodaj_prijelaz(treba_provjeriti[0], nov_stanje, '$')

                if nov_stanje not in provjereno:
                    if nov_stanje not in treba_provjeriti:
                        treba_provjeriti.append(nov_stanje)

        if treba_provjeriti[0] not in provjereno:
            provjereno.append(treba_provjeriti[0])
        del treba_provjeriti[0]

    else:
        if treba_provjeriti[0] not in provjereno:
            provjereno.append(treba_provjeriti[0])
        del treba_provjeriti[0]

eNKA.pretvori_u_DKA()

###izrada tablice NOVO STANJE###

novo_stanje = {}

# prijelazi kao u automatu
for nezavrsni_znak in nezavrsni_znakovi:
    for stanje in eNKA.Stanja():

        # stanje nakon kojeg nema prijelaza
        if stanje not in eNKA.prijelazi.keys():
            continue

        # znak nakon kojeg nema prijelaza
        if nezavrsni_znak not in eNKA.prijelazi[stanje].keys():
            continue

        if stanje not in novo_stanje.keys():
            novo_stanje[stanje] = {}

        novo_stanje[stanje][nezavrsni_znak] = eNKA.prijelazi[stanje][nezavrsni_znak]

###izrada tablice AKCIJA###

akcija = {}
prihvatljivo = list(eNKA.Prihvatljiva())[0]
akcija[prihvatljivo] = {}
akcija[prihvatljivo]['#'] = ["PRIHVATI"]

zavrsni_znakovi.append('#')

# izrada akcija Pomakni
for zavrsni_znak in zavrsni_znakovi:
    for stanje in eNKA.Stanja():

        # stanje nakon kojeg nema prijelaza
        if stanje not in eNKA.prijelazi.keys():
            continue

        # znak nakon kojeg nema prijelaza
        if zavrsni_znak not in eNKA.prijelazi[stanje].keys():
            continue

        if stanje not in akcija.keys():
            akcija[stanje] = {}
        if zavrsni_znak not in akcija[stanje].keys():
            akcija[stanje][zavrsni_znak] = ["POMAKNI"]

        akcija[stanje][zavrsni_znak].append(eNKA.prijelazi[stanje][zavrsni_znak])

# izrada akcija Reduciraj
for stanje in eNKA.Stanja():
    reducirat_cu = False
    lista_stanja = stanje.split(';')
    nova_lista = []
    for stavka in lista_stanja:
        nova_lista += [stavka.split('->')]
    for element in nova_lista:
        element[1] = element[1].split(',{')
        element[1][0] = element[1][0].split(',')
        element[1][1] = element[1][1][:-1].split(',')

    za_znakove = []

    min_index = len(lista_produkcija)
    for element in nova_lista:
        index_tocke = element[1][0].index('*')
        if index_tocke == len(element[1][0]) - 1:
            if element[1][0][0] == '*':
                produkcija = element[0] + '->' + '$'

            else:
                novi_element = element[1][0][:]
                novi_element.remove('*')
                produkcija = element[0] + '->' + ','.join(novi_element)
                if produkcija[:7] == '<novop>':
                    continue

            index = lista_produkcija.index(produkcija)

            # reduciraj za produkciju koja je prva zadana u Ulaznoj Datoteci
            if index < min_index:
                min_index = index
                za_znakove = element[1][1]
                reducirat_cu = True

            # dvije produkcije s istim indexom, reduciraj za uniju njihovih skupova T
            if index == min_index:
                za_znakove.extend(element[1][1])

    if reducirat_cu:
        for zavrsni_znak in za_znakove:
            if stanje in akcija.keys():

                # ne dodaj akcije ako je vec Pomakni ili Prihvati na tom mjestu
                if zavrsni_znak in akcija[stanje].keys():
                    if akcija[stanje][zavrsni_znak][0] == "POMAKNI" or akcija[stanje][zavrsni_znak][0] == "PRIHVATI":
                        continue

            if stanje not in akcija.keys():
                akcija[stanje] = {}
            if zavrsni_znak not in akcija[stanje].keys():
                akcija[stanje][zavrsni_znak] = ["REDUCIRAJ"]

            if len(akcija[stanje][zavrsni_znak]) == 1:
                akcija[stanje][zavrsni_znak].append(lista_produkcija[min_index])
            else:
                akcija[stanje][zavrsni_znak][1] = lista_produkcija[min_index]

# posalji tablice Akcija i NovoStanje analizatoru

"""
outputFile = open("./analizator/data.p", "wb")

pickle.dump(eNKA.pocetno, outputFile)
pickle.dump(sinkronizacijski_znakovi, outputFile)
pickle.dump(akcija, outputFile)
pickle.dump(novo_stanje, outputFile)

outputFile.close()

print
'kraaaaaaj'
"""

#print(akcija)
#print(novo_stanje)