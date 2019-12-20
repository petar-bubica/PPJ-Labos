import config

def izracunaj_duljinu_znakova(cvor_stabla):
    while len(cvor_stabla.lista_djece) > 0:
        cvor_stabla = cvor_stabla.lista_djece[0]

    return (len(cvor_stabla.podaci.split(" ")) -2)


def ide_u_niz_znakova(cvor_stabla):
    while len(cvor_stabla.lista_djece) > 0:
        if len(cvor_stabla.lista_djece) != 1:
            return False
        cvor_stabla = cvor_stabla.lista_djece[0]
    return cvor_stabla.podaci.startswith("NIZ_ZNAKOVA")


def provjeri_tipove(cvor_stabla_1, cvor_stabla_2):
    if len(cvor_stabla_1.vrati_tipove(config.doseg))!=len(cvor_stabla_2.vrati_tipove(config.doseg)):
        return False
    for i in range(len(cvor_stabla_1.vrati_tipove(config.doseg))):
        if cvor_stabla_1.lista_tipova[i] == cvor_stabla_2.lista_tipova[i]:
            return False
    return True


def vrati_lokalnu_deklaraciju(ime):
    for deklaracija in config.doseg.lista_deklaracija:
        if deklaracija.vrati_ime() == ime:
            return deklaracija
    return None


def je_deklarirano_lokalno(ime):
    if config.doseg.lista_deklaracija is None: #Ona ima null
        return False
    for deklaracija in config.doseg.lista_deklaracija:
        if deklaracija.vrati_ime() == ime:
            return True
    return False


def je_vec_deklarirano(ime):
    cvor_tablice = config.doseg
    while cvor_tablice != None:
        for deklaracija in cvor_tablice.lista_deklaracija:
            if deklaracija.vrati_ime() == ime:
                return True
        cvor_tablice = cvor_tablice.roditelj
    return False


def funkcija_vec_postoji(cvor_tablice, ime_funkcije):
    while cvor_tablice is not None:
        for deklaracija in cvor_tablice.lista_deklaracija:
            if deklaracija.je_funkcija() and deklaracija.vrati_ime() == ime_funkcije and deklaracija.je_definiran:
                return True
        cvor_tablice = cvor_tablice.roditelj
    return False


def konfliktna_deklaracija(cvor_tablice, ime_funkcije, tip_funkcije):
    while cvor_tablice.roditelj != None:
        cvor_tablice = cvor_tablice.roditelj
    for deklaracija in cvor_tablice.lista_deklaracija:
        if deklaracija.je_funkcija() and deklaracija.vrati_ime() == ime_funkcije and deklaracija.vrati_tip(config.doseg) != tip_funkcije:
            return True
    return False


def je_castable(tip_1, tip_2):
    return tip_1 == tip_2 or (tip_1 == "char" and tip_2 == "int")


def ispisi_error_poruku(cvor_stabla):
    print(cvor_stabla.podaci + " ::= " + str(cvor_stabla))
    config.error = True
    return


def je_integer(x):
    broj = int(x)
    return -2147483648 <= broj <= 2147483647


def je_char(x):
    return len(x) == 3 or (x[1] == '\\' and x[2] in "tn0'\"\\")


def je_string(x):
    for i in range(1, len(x) - 1):
        if x[i] == '\\':
            s = "'"
            s += x[i] + x[i+1]
            s += "'"
            if not je_char(s):
                return False
    return x[-2] != '\\'


def vrati_tip_trenutne_funkcije():
    cvor = config.doseg
    prazan_string = ""
    while cvor is not None:
        if cvor.lista_deklaracija:
            reverzna_lista_deklaracija = list(reversed(cvor.lista_deklaracija))
            for deklaracija in reverzna_lista_deklaracija:
                if deklaracija.je_funkcija() and deklaracija.je_definiran:
                    return deklaracija.vrati_tip(cvor)
        cvor = cvor.roditelj
    return prazan_string
