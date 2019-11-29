import sys

nezavrsni_znakovi = []
zavrsni_znakovi = []
sinkronizacijski_zavrsni_znakovi = []
gramatika = dict()
key = ""

def ucitaj_podatke():
    global zavrsni_znakovi
    global nezavrsni_znakovi
    global sinkronizacijski_zavrsni_znakovi
    global gramatika
    ucitaj_nezavrsne_znakove()

def ucitaj_nezavrsne_znakove():
    global nezavrsni_znakovi
    linija_unosa = sys.stdin.readline()[:-1]
    if linija_unosa[:2] == "%V":
        nezavrsni_znakovi = linija_unosa[3:].split(" ")
        formiraj_dict_nezavrsni()
        ucitaj_zavrsne_znakove()

def formiraj_dict_nezavrsni():
    for zavrsni in nezavrsni_znakovi:
        gramatika[zavrsni]=""

def ucitaj_zavrsne_znakove():
    global zavrsni_znakovi
    linija_unosa = sys.stdin.readline()[:-1]
    if linija_unosa[:2] == "%T":
        zavrsni_znakovi = linija_unosa[3:].split(" ")
        ucitaj_sinkronizacijske_zavrsne_znakove()

def ucitaj_sinkronizacijske_zavrsne_znakove():
    global sinkronizacijski_zavrsni_znakovi
    linija_unosa = sys.stdin.readline()[:-1]
    if linija_unosa[:4] == "%Syn":
        sinkronizacijski_zavrsni_znakovi = linija_unosa[5:].split(" ")
        ucitaj_produkcije_gramatike()

def ucitaj_produkcije_gramatike():
    global key
    linija_unosa = sys.stdin.readline()[:-1]
    if linija_unosa == "":
        uljepsaj_gramatiku()
        return
    if linija_unosa[0] != " ":
        key = linija_unosa
    else:
        gramatika[key] += linija_unosa[1:] + "|"
    ucitaj_produkcije_gramatike()

def uljepsaj_gramatiku():
    for nezavrsni in gramatika:
        gramatika[nezavrsni] = gramatika[nezavrsni][:len(gramatika[nezavrsni])-1]

def main():
    ucitaj_podatke()
    print(nezavrsni_znakovi)
    print(zavrsni_znakovi)
    print(sinkronizacijski_zavrsni_znakovi)
    print(gramatika)

#Main
main()




