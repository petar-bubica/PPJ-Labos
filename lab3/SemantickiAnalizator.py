# LAB3 EDITION
# [najseksi PPJ ekipa + Petar Bubica]

import config
import ParserStabla
import NaredbenaStruktura


def analiziraj():
    print("U analiziraj metodi")
    NaredbenaStruktura.prijevodna_jedinica(config.korijen)


def funkcijski_error():
    print("U funkcijski error metodi")
    set_definicija = set(config.definirane_funkcije)
    set_deklaracija = set(config.deklarirane_funkcije)
    
    if set_definicija == set_deklaracija:
        return False
    return True

print("Pocetak programa")
ParserStabla.parsiraj()
analiziraj()

if not config.error:
    if config.nema_main:
        print('main')
    else:
        if funkcijski_error:
            print('funkcija')