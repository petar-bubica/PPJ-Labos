from .downloads import GStablo
from .downloads import GSA
from .downloads import LeksickaJedinka
from .downloads import Stog
import sys

indeks = 0
akcije = {}
novaStanja = {}
sinkro_znakovi_set = set(sinkronizacijski_zavrsni_znakovi)
korijen = GStablo(None)
stogZnakovi = Stog()
stogStanja = Stog()

input = sys.stdin.read().splitlines()
listaLeksickihJedinki = input
#PRENIJETI AKCIJE, NOVASTANJA I ZAVRSNE, NEZAVRSNE I SINKRO ZNAKOVE
#METODE ZA AKCIJE, KLASA AKCIJA
#: JE REGEX U PRODUKCIJAMA

def analiza():

    global indeks
    global listaLeksickihJedinki
    global akcije
    global novaStanja
    global korijen
    global stogZnakovi
    global stogStanja
    global sinkro_znakovi_set

    stogStanja.push(0)
    stogZnakovi.push(GStablo("$"))

    while True:
        stanje = stogStanja.peek()

        if indeks < len(listaLeksickihJedinki):
            leksickaJedinka = listaLeksickihJedinki[indeks]
        else:
            leksickaJedinka = LeksickaJedinka("$ $ $")
        akcija = akcije.get(stanje).get(leksickaJedinka.uniformniZnak)
        if akcija.Prihvati():
            break
        if akcija.Nepostojeca():
            sys.stderr.write("Oporavljanje u greske u redu ", leksickaJedinka.brojRetka)

            sys.stderr.write("Ne bi izazvali pogrešku:")

            setAkcija = set(akcije[stanje])
            for i in setAkcija:
                if akcije[stanje][i].Nepostojeca() == False:
                    sys.stderr.write(i + " ") # treba li u istom redu?

            sys.stderr.write("Izazvao pogresku: ", leksickaJedinka.uniformniZnak)
            naden = False
            for i in range(indeks,len(listaLeksickihJedinki)):
                if listaLeksickihJedinki[i].uniformniZnak in sinkro_znakovi_set:
                    naden = True
                    break
                indeks += 1
            if naden == False:
                sys.stderr.write("Ne može se oporaviti od pogreške")
                break
            leksickaJedinka = listaLeksickihJedinki[indeks]

            while stogStanja.velicina() > 0:
                privremenaAkcija = akcije[stogStanja.peek()][leksickaJedinka.uniformniZnak]
                if privremenaAkcija.Nepostojeca() == False:
                    korijen = stogZnakovi.peek()
                    break

                stogStanja.pop()
                stogZnakovi.pop()

            if velicina(stogStanja)==0:
                #error
                break
        if akcija.Pomakni():
            stogStanja.push(akcija.pomakni)
            novi = GStablo(leksickaJedinka.ispis())
            stogZnakovi.push(novi)
            indeks += 1
            continue
        if akcija.Reduciraj():
            produkcija = akcija.reduciraj
            lijeva = produkcija.split(":")[0] #OVAKO PRODUKCIJE
            desna = produkcija.split(":")[1]
            novoStablo = GStablo(lijeva)
            if len(desna) == 0:
                novoStablo.dodajDijete(GStablo("$"))
            else:
                for i in range(0,len(desna)):
                    stogStanja.pop()
                    novoStablo.dodajDijete(stogZnakovi.peek())
                    stogZnakovi.pop()
            stogZnakovi.push(novoStablo)
            stogZnakovi.push(novaStanja[stogStanja.peek()][lijeva])
            korijen = novoStablo















