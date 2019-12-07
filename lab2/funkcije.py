
def ide_u_epsilon(znak, gramatika, zavrsni_znakovi, nezavrsni_znakovi):
    """provjerava da li znak gramatike moze skupom produkcija otic u epsilon"""

    if znak in zavrsni_znakovi:
        return False

    if ['$'] in gramatika[znak]:
        return True

    else:
        treba_provjeriti = [znak]
        provjereno = []
        while treba_provjeriti != []:
            znak = treba_provjeriti[0]
            if znak in nezavrsni_znakovi:
                if ['$'] in gramatika[znak]:
                    return True

                for produkcija in gramatika[znak]:
                    if produkcija[0] in nezavrsni_znakovi:
                        if produkcija[0] not in provjereno and produkcija[0] != znak:
                            treba_provjeriti.append(produkcija[0])
                            provjereno.append(znak)

            del treba_provjeriti[0]

        return False


def niz_ide_u_epsilon(niz, gramatika, zavrsni_znakovi, nezavrsni_znakovi):
    "provjerava da li cijeli niz znakova moze skupom produkcija otici u epsilon"

    for znak in niz:
        if not ide_u_epsilon(znak, gramatika, zavrsni_znakovi, nezavrsni_znakovi):
            return False
    return True


def zapocinje(znak, gramatika, zavrsni_znakovi, nezavrsni_znakovi):
    """racuna skup ZAPOCINJE za jedan znak, vraca set()"""

    if znak in zavrsni_znakovi:
        return set([znak])

    else:
        vrati = set()
        for produkcija in gramatika[znak]:
            if produkcija[0] in zavrsni_znakovi:
                vrati.update([produkcija[0]])
            elif produkcija[0] in nezavrsni_znakovi:
                znak = produkcija[0]
                i = 0
                provjereno = []

                # provjeravamo ide li u epsilon prvi znak produkcije
                while ide_u_epsilon(znak, gramatika, zavrsni_znakovi, nezavrsni_znakovi):
                    treba_provjeriti = [znak]
                    while treba_provjeriti != []:
                        x = treba_provjeriti[0]
                        for prod in gramatika[x]:
                            if prod[0] in zavrsni_znakovi:
                                vrati.update([prod[0]])
                            elif prod[0] in nezavrsni_znakovi:

                                if prod[0] not in provjereno:
                                    if prod[0] not in treba_provjeriti and prod[0] != znak:
                                        treba_provjeriti.append(prod[0])

                                k = 0
                                # dodaj sve nezavrsne znakove iz jedne produkcije koji mogu otic u epsilon u listu treba_provjeriti
                                while ide_u_epsilon(prod[k], gramatika, zavrsni_znakovi, nezavrsni_znakovi):
                                    if k+ 1 < len(prod):
                                        if prod[k + 1] in zavrsni_znakovi:
                                            vrati.update([prod[k + 1]])
                                            break
                                        elif prod[k + 1] in nezavrsni_znakovi:
                                            if prod[k + 1] not in provjereno:
                                                if prod[k + 1] not in treba_provjeriti:
                                                    treba_provjeriti.append(prod[k + 1])
                                    k += 1
                                    if k == len(prod):
                                        break
                        if x not in provjereno:
                            provjereno.append(x)
                        del treba_provjeriti[0]

                    i += 1

                    # uvjeti zaustavljanja
                    if i == len(produkcija):
                        break

                    if produkcija[i] in zavrsni_znakovi:
                        vrati.update([produkcija[i]])
                        break

                    znak = produkcija[i]

                    if znak in provjereno:
                        break

                # ako prvi znak ne ide u epsilon, a nije vec provjeren
                if znak not in provjereno:
                    treba_provjeriti = [znak]
                    while treba_provjeriti != []:
                        x = treba_provjeriti[0]
                        for prod in gramatika[x]:
                            if prod[0] in zavrsni_znakovi:
                                vrati.update([prod[0]])
                            elif prod[0] in nezavrsni_znakovi:
                                if prod[0] not in provjereno:
                                    treba_provjeriti.append(prod[0])

                        if x not in provjereno:
                            provjereno.append(x)
                        del treba_provjeriti[0]

    return vrati


def zapocinje_niz(niz, gramatika, zavrsni_znakovi, nezavrsni_znakovi):
    """racuna skup ZAPOCINJE za niz znakova (lista) i vraca set()"""

    if not niz:  # radi potreba GSA
        return False

    if niz[0] in zavrsni_znakovi:
        return set([niz[0]])

    if not ide_u_epsilon(niz[0], gramatika, zavrsni_znakovi, nezavrsni_znakovi):
        return zapocinje(niz[0], gramatika, zavrsni_znakovi, nezavrsni_znakovi)

    vrati = set()
    for znak in niz:
        if znak in zavrsni_znakovi:
            vrati.update([znak])
            break

        if not ide_u_epsilon(znak, gramatika, zavrsni_znakovi, nezavrsni_znakovi):
            vrati.update(zapocinje(znak, gramatika, zavrsni_znakovi, nezavrsni_znakovi))
            break

        vrati.update(zapocinje(znak, gramatika, zavrsni_znakovi, nezavrsni_znakovi))

    return vrati
