import sys


def indeks_novog_retka():
    global izvorni_kod
    global broj_retka
    brojac_novih_redaka = 1
    for indeks in range(len(izvorni_kod)):
        if izvorni_kod[indeks] == '\n':
            brojac_novih_redaka += 1
            if brojac_novih_redaka == broj_retka:
                return indeks + 1


def novi_redak():
    global broj_retka
    broj_retka += 1
    return indeks_novog_retka()


def udji_u_stanje(argument):
    global trenutno_stanje
    novo_stanje = argument.split(" ")[1]
    trenutno_stanje = novo_stanje
    return


def vrati_se(argument):
    global izvorni_kod
    return int(argument.split(" ")[1])


""" [Metoda koja vrši traženi ispis (redak po redak)] """

def ispis_retka_tablice(uniformni_znak, znak):
    print(uniformni_znak + " " + str(broj_retka) + " " + znak)  ##npr. KR_AKO 3 if


""" [Metoda koja učitava izvorni kod programa] """

def ucitaj_kod():
    global izvorni_kod
    izvorni_kod = " " + sys.stdin.read()
    #print(izvorni_kod)
    return


def epsilon_okruzenje(stanja):
    Y = [] + stanja
    stog = [] + stanja
    if -1 in Y:
        Y.remove(-1)
    while stog:
        stanje_t = stog.pop()
        if (stanje_t, '') not in tablica_prijelaza:
            continue
        #print(tablica_prijelaza[(stanje_t, '$')])
        for stanje_v in tablica_prijelaza[(stanje_t, '')]:
            if stanje_v not in Y:
                Y.append(stanje_v)
                stog.append(stanje_v)
    return Y


def citaj(kazaljka):
    if (kazaljka + 1) >= len(izvorni_kod):
        return
    return izvorni_kod[kazaljka + 1]


def prijelaz_iz_vise_stanja(Q, znak):
    lista_prijelaza = set()
    for stanje in Q:
        if (stanje, znak) in tablica_prijelaza:
            lista_prijelaza.update(tablica_prijelaza.get((stanje, znak)))
    return list(lista_prijelaza)

def redni_broj_automata_za_stanje(stanje):
    redni_broj = -1
    #print(tablica_prijelaza[(-1, '$')])
    #print(tablica_prijelaza)
    for pocetno_stanje_malog_automata in tablica_prijelaza[(-1, '')]:
        #print("bla", pocetno_stanje_malog_automata)
        if stanje >= pocetno_stanje_malog_automata:
            redni_broj += 1
        else:
            break
    return redni_broj

def printaj_indekse(pocetak, zavrsetak, posljednji):
    print()
    print("pocetak:", pocetak)
    print("zavrsetak:", zavrsetak)
    print("posljednji:", posljednji)
    print()

def simuliraj():
    global tablica_prijelaza
    global izvorni_kod
    global prihvatljiva_stanja
    global leksicka_pravila
    #R = epsilon_okruzenje([-1])
    R = tablica_prijelaza[(-1, '')]
    #print("pocetna stanja:", R)
    pocetak = 1
    zavrsetak = 0
    posljednji = 1
    a = ''
    izraz = -1
    #printaj_indekse(pocetak, zavrsetak, posljednji)
    while (zavrsetak + 1) < len(izvorni_kod):
        while R:
            #print("trenutni R:", R)
            #print("prihvatljiva stanja:", prihvatljiva_stanja)
            P = set(R).intersection(set(prihvatljiva_stanja))
            P = list(sorted(P))
            #print("P:", P)
            #izraz = -1
            if not P and R:
                a = citaj(zavrsetak)
                #print("ucitan znak (prvi slucaj):", a)
                zavrsetak += 1
                #printaj_indekse(pocetak, zavrsetak, posljednji)
                Q = R
                R = epsilon_okruzenje(prijelaz_iz_vise_stanja(epsilon_okruzenje(Q), a))
                #print("R:", R)
            elif P:
                for stanje_P in P:
                    redni_broj_automata = redni_broj_automata_za_stanje(stanje_P)
                    #print(stanje_P, leksicka_pravila[redni_broj_automata][0], trenutno_stanje)
                    #print(redni_broj_automata, leksicka_pravila[redni_broj_automata][1])
                    if leksicka_pravila[redni_broj_automata][0] == trenutno_stanje:
                        izraz = redni_broj_automata
                        """
                        print()
                        print("trenutni znak:", a)
                        print("automat:", izraz)
                        print("stanje_P:", stanje_P)
                        print("P:", P)
                        print("R:", R)
                        """
                        break
                #print("broj automata:", izraz)
                Q = R
                a = citaj(zavrsetak)
                #print("ucitan znak (drugi slucaj):", a)
                posljednji = zavrsetak
                zavrsetak += 1
                #printaj_indekse(pocetak, zavrsetak, posljednji)
                R = epsilon_okruzenje(prijelaz_iz_vise_stanja(epsilon_okruzenje(Q), a))

        if izraz == -1:
            #print("ne valja znak " + str(a))
            zavrsetak = pocetak
            pocetak += 1
            #printaj_indekse(pocetak, zavrsetak, posljednji)
            R = epsilon_okruzenje([-1])
        else:
            #print("niz znakova " + izvorni_kod[pocetak: posljednji+1] + " valja")
            argumenti = leksicka_pravila[izraz][1]
            #print(argumenti)
            #print(izraz)
            for indeks_akcije in range(1, len(argumenti)):
                if argumenti[indeks_akcije] == "NOVI_REDAK":
                    novi_redak()
                elif "UDJI_U_STANJE" in argumenti[indeks_akcije]:
                    udji_u_stanje(argumenti[indeks_akcije])
                elif "VRATI_SE" in argumenti[indeks_akcije]:
                    #pocetak = vrati_se(argumenti[indeks_akcije])
                    posljednji = pocetak + vrati_se(argumenti[indeks_akcije]) - 1

            if argumenti[0] != '-':
                #print(trenutno_stanje, end=' ')
                ispis_retka_tablice(argumenti[0], izvorni_kod[pocetak: posljednji+1])

            izraz = -1
            pocetak = posljednji + 1
            zavrsetak = posljednji
            posljednji = pocetak
            #printaj_indekse(pocetak, zavrsetak, posljednji)
            R = epsilon_okruzenje([-1])
    return


""" [Globalne varijable] """

trenutno_stanje = ""
broj_retka = 1
izvorni_kod = ""