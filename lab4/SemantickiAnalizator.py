# LAB3 EDITION
# [najseksi PPJ ekipa + Petar Bubica]

import sys
from lab4 import config
from lab4 import ParserStabla
from lab4 import NaredbenaStruktura
#from Parser import Parser


def analiziraj():
    #print("U analiziraj metodi")
    NaredbenaStruktura.prijevodna_jedinica(config.korijen)


def funkcijski_error():
    #print("U funkcijski error metodi")
    set_definicija = set(config.definirane_funkcije)
    set_deklaracija = set(config.deklarirane_funkcije)
    
    if set_definicija == set_deklaracija:
        return False
    return True


#print("Pocetak programa")
#ulaz = sys.stdin.read().splitlines()
#parser = Parser(ulaz)
#config.korijen = parser.vrati_korijen()
#print(korijen.ispisi_podstablo(korijen))
ParserStabla.parsiraj()
analiziraj()

if not config.error:
    if config.nema_main:
        print('main')
    else:
        if funkcijski_error:
            print('funkcija')