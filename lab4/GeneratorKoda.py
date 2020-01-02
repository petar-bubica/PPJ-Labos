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
file = open("a.frisc", "w")

file.write("\t`BASE D\n")
file.write("\tMOVE 40000, R7\n")
main = "\tCALL MAIN\n\tHALT\n\n"

listaLabela = config.tabela
nijeTab = True

for kod in config.korijen.kod.split("\n"):
    if not kod.startswith("\t") and nijeTab:
        file.write(main)
        nijeTab = False
    file.write(kod + "\n")
for labela in listaLabela:
    if not labela.je_fja:
        file.write(labela.labela)
        if labela.je_prazno:
            file.write("\tDW %D 0\n")
            continue
        file.write(labela.vrati_bitove())

file.close()



#NEZ JEL OVO TREBA -nek stoji sad, mislim da ne jer je ja msm pisalo u uputama da nece do ovakvih slucaja doc
#if not config.error:
    #if config.nema_main:
        #print('main')
    #else:
        #if funkcijski_error:
            #print('funkcija')