# LAB3 EDITION
# [najseksi PPJ ekipa + Dora Franjic]

import config
import ParserStabla
import NaredbenaStruktura


def analiziraj():
    NaredbenaStruktura.prijevodna_jedinica(config.korijen)


def funkcijski_error():
    set_definicija = set(config.definirane_funkcije)
    set_deklaracija = set(config.deklarirane_funkcije)
    
    if set_definicija == set_deklaracija:
        return False
    return True


ParserStabla.parsiraj()
analiziraj()

if not config.error:
    if config.nema_main:
        print('main')
    else:
        if funkcijski_error:
            print('funkcija')