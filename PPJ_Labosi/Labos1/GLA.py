""" [PPJ Projekt - 1. labos - Generator leksičkog analizatora]
@autori: najseksi PPJ ekipa + Dora Franjić
"""
import sys


class LeksickoPravilo:
    def __init__(self):
        self.stanje = ""
        self.regex = ""
        self.argumenti = []

    def dodaj_argument(self, argument):
        self.argumenti.append(argument)

    def ispis(self):
        string = self.stanje + " " + self.regex + " "
        for argument in self.argumenti:
            string += argument + " "
        return string


class Automat:

    def __init__(self, broj_stanja):
        self.broj_stanja = broj_stanja
        self.prihvatljiva_stanja = []
        self.funkcije_prijelaza = dict()

    def nadji_epsilon_stanja(self, stanje):
        if (stanje, '$') in self.funkcije_prijelaza:
            return self.funkcije_prijelaza.get((stanje, '$'))
        else:
            return set()

    def dohvati_epsilon_stanja(self, stanje):
        if stanje == '#':
            return set('#')
        else:
            if (stanje, '$') in self.funkcije_prijelaza:
                ciljno_stanje = self.funkcije_prijelaza.get((stanje, '$'))
                iduca_stanja = set()
                iduca_stanja_prethodni = set()
                iduca_stanja.update(ciljno_stanje)
                while iduca_stanja != iduca_stanja_prethodni:
                    iduca_stanja_prethodni = set(iduca_stanja)
                    epsilon_stanja = set()
                    for iduce_stanje in iduca_stanja:
                        epsilon_stanja.update(self.nadji_epsilon_stanja(iduce_stanje))
                    iduca_stanja.update(epsilon_stanja)
                    del epsilon_stanja
                return iduca_stanja.difference(set('#'))
            else:
                return set()

    def dohvati_iduca_stanja(self, stanje, simbol):
        if stanje == '#':
            return set('#')
        elif (stanje, simbol) in self.funkcije_prijelaza:
            ciljno_stanje = self.funkcije_prijelaza.get((stanje, simbol))
            iduca_stanja = set()
            epsilon_stanja = set()
            iduca_stanja.update(ciljno_stanje)
            for iduce_stanje in iduca_stanja:
                epsilon_stanja.update(self.dohvati_epsilon_stanja(iduce_stanje))
            iduca_stanja.update(epsilon_stanja)
            del epsilon_stanja
            return iduca_stanja
        else:
            return set('#')


    def dodaj_epsilon_prijelaz(self, staro_stanje, novo_stanje):
        if (staro_stanje, '$') not in self.funkcije_prijelaza:
            self.funkcije_prijelaza[(staro_stanje, '$')] = []
        if novo_stanje not in self.funkcije_prijelaza[(staro_stanje, '$')]:
            self.funkcije_prijelaza[(staro_stanje, '$')].append(novo_stanje)
        return


    def dodaj_prijelaz(self, staro_stanje, novo_stanje, prijelazni_znak):
        if (staro_stanje, prijelazni_znak) not in self.funkcije_prijelaza:
            self.funkcije_prijelaza[(staro_stanje, prijelazni_znak)] = []
        if novo_stanje not in self.funkcije_prijelaza[(staro_stanje, prijelazni_znak)]:
            self.funkcije_prijelaza[(staro_stanje, prijelazni_znak)].append(novo_stanje)
        return

    def novo_stanje(self):
        self.broj_stanja += 1
        return self.broj_stanja - 1

    def je_operator(self, izraz, i):
        br = 0
        while i - 1 >= 0 and izraz[i - 1] == "\\":
            br += 1
            i -= 1
        return br % 2 == 0

    def nadji_odgovarajucu_zatvorenu_zagradu(self, izraz):
        for i in range(len(izraz)):
            if izraz[i] == ")" and self.je_operator(izraz, i):
                return i

    def pretvori(self, izraz):
        izbori = []
        br_zagrada = 0
        zadnji = 0
        for i in range(len(izraz)):
            if izraz[i] == "(" and self.je_operator(izraz, i):
                br_zagrada += 1
            elif izraz[i] == ")" and self.je_operator(izraz, i):
                br_zagrada -= 1
            elif br_zagrada == 0 and izraz[i] == "|" and self.je_operator(izraz, i):
                izbori += [izraz[zadnji: i]]
                zadnji = i + 1

        if izbori:
            izbori += [izraz[zadnji: len(izraz)]]

        lijevo_stanje = self.novo_stanje()
        desno_stanje = self.novo_stanje()
        if izbori:
            for i in range(len(izbori)):
                privremeno = self.pretvori(izbori[i])
                self.dodaj_epsilon_prijelaz(lijevo_stanje, privremeno[0])
                self.dodaj_epsilon_prijelaz(privremeno[1], desno_stanje)
        else:
            prefiksirano = False
            zadnje_stanje = lijevo_stanje
            for i in range(len(izraz)):
                if prefiksirano:
                    prefiksirano = False
                    if izraz[i] == "t":
                        prijelazni_znak = "\t"
                    elif izraz[i] == "n":
                        prijelazni_znak = "\n"
                    elif izraz[i] == "_":
                        prijelazni_znak = " "
                    else:
                        prijelazni_znak = izraz[i]
                    a = self.novo_stanje()
                    b = self.novo_stanje()
                    self.dodaj_prijelaz(a, b, prijelazni_znak)
                else:
                    if izraz[i] == "\\":
                        prefiksirano = True
                        continue
                    if izraz[i] != "(":
                        a = self.novo_stanje()
                        b = self.novo_stanje()
                        if izraz[i] == "$":
                            self.dodaj_prijelaz(a, b, '$')
                        else:
                            self.dodaj_prijelaz(a, b, izraz[i])
                    else:
                        j = self.nadji_odgovarajucu_zatvorenu_zagradu(izraz)
                        privremeno = self.pretvori(izraz[i + 1: j - 1])
                        a = privremeno[0]
                        b = privremeno[1]
                        i = j

                if i + 1 < len(izraz) and izraz[i + 1] == "*":
                    x = a
                    y = b
                    a = self.novo_stanje()
                    b = self.novo_stanje()
                    self.dodaj_epsilon_prijelaz(a, x)
                    self.dodaj_epsilon_prijelaz(y, b)
                    self.dodaj_epsilon_prijelaz(a, b)
                    self.dodaj_epsilon_prijelaz(y, x)
                    i += 1
                self.dodaj_epsilon_prijelaz(zadnje_stanje, a)
                zadnje_stanje = b
            self.dodaj_epsilon_prijelaz(zadnje_stanje, desno_stanje)
        return lijevo_stanje, desno_stanje

    def ispis(self):
        string = ""
        for prijelaz in self.funkcije_prijelaza:
            string += str(prijelaz[0]) + " " + str(prijelaz[1]) + " " + str(
                self.funkcije_prijelaza.get(prijelaz)) + "\n"
        return string


##################################################

""" [Globalne varijable] """
regularne_definicije = dict()
lista_stanja = list()
lista_uniformnih_znakova = list()
lista_leksickih_pravila = list()
glavni_automat = Automat(0)
lista_malih_automata = list()

""" [Metode za parsiranje ulaznih podataka]
    - ucitaj_regularne_definicije(): parsira prvi dio ulazne datoteke
    - ucitaj_stanja(): parsira drugi dio ulazne datoteke
    - ucitaj_uniformne_znakove(): parsira treći dio ulazne datoteke
    - ucitaj_leksicka_pravila(): parsira četvrti dio ulazne datoteke
"""


def ucitaj_podatke():
    global lista_leksickih_pravila
    ucitaj_regularne_definicije()
    lista_leksickih_pravila = set(lista_leksickih_pravila)
    lista_leksickih_pravila = list(lista_leksickih_pravila)


""" [Metoda koja učitava regularne definicije te pokreće učitavanje stanja] """


def ucitaj_regularne_definicije():
    global regularne_definicije
    linija_unosa = sys.stdin.readline()[:-1]
    if linija_unosa[:2] == "%X":
        ucitaj_stanja(linija_unosa)
        return
    regularna_definicija = linija_unosa.split(" ")
    ime_regularne_definicije = regularna_definicija[0]
    regularni_izraz = regularna_definicija[1]
    regularne_definicije[ime_regularne_definicije] = regularni_izraz
    ucitaj_regularne_definicije()


""" [Metoda koja učitava stanja te pokreće učitavanje uniformnih znakova] """


def ucitaj_stanja(linija_unosa):
    global lista_stanja
    lista_stanja = linija_unosa[3:].split(" ")
    ucitaj_uniformne_znakove()


""" [Metoda koja učitava uniformne znakove te pokreće učitavanje leksičkih pravila] """


def ucitaj_uniformne_znakove():
    global lista_uniformnih_znakova
    linija_unosa = sys.stdin.readline()[:-1]
    if linija_unosa[:2] == "%L":
        lista_uniformnih_znakova = linija_unosa[3:].split(" ")
    ucitaj_leksicka_pravila()


""" [Metoda koja učitava leksička pravila] """


def ucitaj_leksicka_pravila():
    """ [Format leksickih pravila]
        <stanje>regex
        {
        ...argumenti svaki u svom retku...
        }
    """
    global lista_leksickih_pravila
    linija_unosa = sys.stdin.readline()[:-1]
    if linija_unosa == "":
        return
    leksicko_pravilo = LeksickoPravilo()
    if linija_unosa[0] == "<":
        indeks = linija_unosa.index(">")
        leksicko_pravilo.stanje = linija_unosa[1: indeks]
        leksicko_pravilo.regex = linija_unosa[indeks + 1:]
        lista_leksickih_pravila.append(leksicko_pravilo)
        linija_unosa = sys.stdin.readline()[:-1]
        if linija_unosa[0] == "{":
            while linija_unosa[0] != "}":
                linija_unosa = sys.stdin.readline()[:-1]
                if linija_unosa[0] != "{" and linija_unosa[0] != "}":
                    leksicko_pravilo.dodaj_argument(linija_unosa)
    ucitaj_leksicka_pravila()


""" [Metoda koja unutar regex-a svih regularnih definicija, regularnu definiciju zamjenjuje
     sa pripadnim regex-om] """


def reformatiraj_regularne_definicije():
    for key in regularne_definicije:
        for regDef in regularne_definicije:
            if regDef in regularne_definicije.get(key):
                regularne_definicije[key] = regularne_definicije[key].replace(regDef,
                                                                              "(" + regularne_definicije[regDef] + ")")
    return


""" [Metoda koja unutar regex-a zamjenjuje regularne definicije sa pripradnim regex-om] """


def reformatiraj_pravila():
    for leksicko_pravilo in lista_leksickih_pravila:
        for key in regularne_definicije:
            if key in leksicko_pravilo.regex:
                leksicko_pravilo.regex = regularne_definicije[key]
    return


#todo
def izgradi_automat():
    global glavni_automat
    trenutni_broj_stanja_automata = 0
    for leksicko_pravilo in lista_leksickih_pravila:
        automat = Automat(trenutni_broj_stanja_automata)
        [pocetno_stanje, konacno_stanje] = automat.pretvori(leksicko_pravilo.regex)

        lista_malih_automata.append(automat)

        glavni_automat.funkcije_prijelaza.update(automat.funkcije_prijelaza)
        glavni_automat.prihvatljiva_stanja.append(konacno_stanje)

        glavni_automat.dodaj_prijelaz(-1, pocetno_stanje, '$')
        trenutni_broj_stanja_automata = automat.broj_stanja
    glavni_automat.broj_stanja = trenutni_broj_stanja_automata
    return


#todo
def generirajLA():
    datotekaLA = open("analizator/LA.py", "at")
    # datotekaLA.write(ispisKodaAutomata())
    # datotekaLA.write(ispis_koda_leksickih_pravila())
    # datotekaLA.write("lista_stanja = " + str(lista_stanja) + "\n")
    # nadodat dio za main()
    datotekaLA.close()
    return


""" [Metoda koja generira varijablu argumenata leksičkih pravila da se pošalje datoteci LA] """


def ispis_koda_leksickih_pravila():
    ispis = "leksicka_pravila = "
    rjecnik_leksickih_pravila = dict()
    for leksicko_pravilo in lista_leksickih_pravila:
        rjecnik_leksickih_pravila[(leksicko_pravilo.stanje, leksicko_pravilo.regex)] = leksicko_pravilo.argumenti
    ispis += str(rjecnik_leksickih_pravila)
    ispis += "\n"
    return ispis


def ispis_tablica_prijelaza_malih_automata():
    ispis = "tablice_prijelaza_malih_automata = ["
    for mali_automat in lista_malih_automata:
        ispis += str(mali_automat.funkcije_prijelaza) + ","
    ispis = ispis[:-1]
    ispis += "]"
    return ispis


""" [Main metoda programa] """
ucitaj_podatke()
reformatiraj_regularne_definicije()
reformatiraj_pravila()
izgradi_automat()
# generirajLA()

print("tablica_prijelaza = " + str(glavni_automat.funkcije_prijelaza))
print(ispis_tablica_prijelaza_malih_automata())
print(ispis_koda_leksickih_pravila())
print("lista_stanja = " + str(lista_stanja))
print("prihvatljiva_stanja = " + str(glavni_automat.prihvatljiva_stanja))
print("broj_stanja_u_automatu = " + str(glavni_automat.broj_stanja))
