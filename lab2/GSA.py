import sys
import pickle

nezavrsni_znakovi = []
zavrsni_znakovi = []
sinkronizacijski_zavrsni_znakovi = []
pocetni_nezavrsni_znak = ''
gramaticka_pravila = dict()
trenutni_nezavrsni_znak = ''
gramatika = None

def ucitaj_podatke():
    global zavrsni_znakovi
    global nezavrsni_znakovi
    global sinkronizacijski_zavrsni_znakovi
    global gramatika
    ucitaj_nezavrsne_znakove()

def ucitaj_nezavrsne_znakove():
    global nezavrsni_znakovi
    global pocetni_nezavrsni_znak
    linija_unosa = sys.stdin.readline()[:-1]
    if linija_unosa[:2] == '%V':
        nezavrsni_znakovi = linija_unosa[3:].split(' ')
        pocetni_nezavrsni_znak = nezavrsni_znakovi[0]
        formiraj_dict_nezavrsni()
        ucitaj_zavrsne_znakove()

def formiraj_dict_nezavrsni():
    for nezavrsni in nezavrsni_znakovi:
        gramaticka_pravila[nezavrsni] = []

def ucitaj_zavrsne_znakove():
    global zavrsni_znakovi
    linija_unosa = sys.stdin.readline()[:-1]
    if linija_unosa[:2] == '%T':
        zavrsni_znakovi = linija_unosa[3:].split(' ')
        ucitaj_sinkronizacijske_zavrsne_znakove()

def ucitaj_sinkronizacijske_zavrsne_znakove():
    global sinkronizacijski_zavrsni_znakovi
    linija_unosa = sys.stdin.readline()[:-1]
    if linija_unosa[:4] == '%Syn':
        sinkronizacijski_zavrsni_znakovi = linija_unosa[5:].split(' ')
        ucitaj_produkcije_gramatike()

def ucitaj_produkcije_gramatike():
    global trenutni_nezavrsni_znak
    #linija_unosa = sys.stdin.readline()[:-1]
    linija_unosa = sys.stdin.readline()
    if linija_unosa == '':
        return
    if linija_unosa[0] != ' ':
        trenutni_nezavrsni_znak = linija_unosa[:-1]
    else:
        if linija_unosa[-1] == '\n':
            linija_unosa = linija_unosa[:-1]
            produkcija = linija_unosa[1:]
        else:
            produkcija = linija_unosa[1:]
        gramaticka_pravila[trenutni_nezavrsni_znak].append(produkcija.split(' '))
    ucitaj_produkcije_gramatike()


def ispis_svega():
    print('NEZAVRSNI ZNAKOVI:', nezavrsni_znakovi)
    print('POC. NEZAVRSNI ZNAK:', pocetni_nezavrsni_znak)
    print('ZAVRSNI ZNAKOVI:', zavrsni_znakovi)
    print('SYNCHRO ZNAKOVI:', sinkronizacijski_zavrsni_znakovi)
    print('GRAMATICKA PRAVILA:', gramaticka_pravila)


def main():
    global gramatika
    ucitaj_podatke()
    #ispis_svega()


#Main
main()