class Gramatika:

    def __init__(self, pravila):
        self.rjecnik_gramatike = pravila
        self.pravila = self.parsiraj(pravila)

    def parsiraj(self, pravila):
        parsirana_pravila = list()
        for nezavrsni_znak in pravila:
            for izraz in pravila[nezavrsni_znak]:
                pravilo = (nezavrsni_znak, izraz)
                parsirana_pravila.append(pravilo)
        return parsirana_pravila

    def get_skup_ZAPOCNI(self):
        skup_ZAPOCNI = {n_znak: set() for n_znak in self.nezavrsni_znakovi}
        skup_ZAPOCNI.update((z_znak, {z_znak}) for z_znak in self.zavrsni_znakovi)
        epsilon = set()

        while True:
            bilo_je_promjena = False

            for (nezavrsni_znak, izraz) in self.pravila:
                for znak in izraz:
                    if znak == '$':
                        break
                    #print((nezavrsni_znak, izraz), znak)
                    #print('DICT:', skup_ZAPOCNI)
                    bilo_je_promjena |= self.unija(skup_ZAPOCNI[nezavrsni_znak], skup_ZAPOCNI[znak])
                    if znak not in epsilon:
                        break
                    else:
                        bilo_je_promjena |= self.unija(epsilon, {nezavrsni_znak})

            if not bilo_je_promjena:
                return skup_ZAPOCNI

    def unija(self, prvi_skup, drugi_skup):
        duljina_prvog_skupa = len(prvi_skup)
        prvi_skup |= drugi_skup
        if len(prvi_skup) != duljina_prvog_skupa:
            return True
        return False

    def dohvati_iduci_nezavrsni_znak(self, produkcija):
        nezavrsni_znak, izraz = produkcija
        try:
            indeks_tockice = izraz.index('.')
            return izraz[indeks_tockice + 2]  # +1 za iduci te +1 jer je zadnji znak iz SLIJEDI
        except IndexError:
            return '$'

    @staticmethod
    def je_nezavrsni_znak(simbol):
        simbol_je_slovo = simbol.isalpha()
        simbol_je_veliko_slovo = simbol.isupper()
        if simbol_je_slovo and simbol_je_veliko_slovo:
            return True
        return False

    @property
    def nezavrsni_znakovi(self):
        skup_nezavrsnih_znakova = set()
        for (znak, _) in self.pravila:
            skup_nezavrsnih_znakova.add(znak)
        return skup_nezavrsnih_znakova

    @property
    def zavrsni_znakovi(self):
        skup_zavrsnih_znakova = set()
        for (_, izraz) in self.pravila:
            for znak in izraz:
                znak_je_malo_slovo = znak.islower()
                if znak_je_malo_slovo:
                    skup_zavrsnih_znakova.add(znak)
        return skup_zavrsnih_znakova

    @staticmethod
    def vrati_znak_iza_tocke(produkcija):
        try:
            nezavrsni_znak = produkcija[0]
            izraz = produkcija[1]
           # print(izraz)
            indeks_tockice = izraz.index('.')
            return izraz[indeks_tockice + 1]
        except ValueError:
            return '$'

    def nadji_produkcije_za_stanja(self, produkcije_u_stanjima):
        nije_gotovo = True
        while nije_gotovo:
            nije_gotovo = False
            for produkcije_stanja in produkcije_u_stanjima:
                produkcija = produkcije_stanja[0]
                nezavrsni_znak = self.vrati_znak_iza_tocke(produkcija)
                pronadjene_produkcije = self.nadji_produkcije(nezavrsni_znak)
                if pronadjene_produkcije == 1:
                    pass
                else:
                    for pronadjena_produkcija in pronadjene_produkcije:
                        iduci_znak = self.dohvati_iduci_nezavrsni_znak(produkcija)
                        skup_ZAPOCNI = self.get_skup_ZAPOCNI()
                        for znak in skup_ZAPOCNI:
                            #nova_produkcija = [nezavrsni_znak + '::=.' + self.pronadjena_produkcija + '' + znak]
                            nova_produkcija = (nezavrsni_znak, ['.'] + pronadjena_produkcija + [znak])
                            #print(nova_produkcija)
                            if nova_produkcija not in produkcije_stanja:
                                produkcije_stanja.append(nova_produkcija)
                                nije_gotovo = True
            return produkcije_stanja

    def provjeri_valjanost(self, produkcije_stanja):
        zadnji_znak_produkcije = produkcije_stanja[0][-1]
        if zadnji_znak_produkcije == '.':
            return False
        return True

    def razdvoji_slijedi(self, produkcije_u_stanjima):
        stanja_bez_slijedi = []
        for produkcije_stanja in produkcije_u_stanjima:
            if self.provjeri_valjanost(produkcije_stanja):
                stanja_bez_slijedi.append(produkcije_stanja)
                #stanja_bez_slijedi.append(''.join(produkcije_stanja).replace(' ', ''))
        if len(stanja_bez_slijedi) != 0:
            return stanja_bez_slijedi

    def pomakni_tocku(self, produkcija):
        print(1)
        print(produkcija)
        nezavrsni_znak, izraz = produkcija
        indeks_tockice = izraz.index('.')
        if len(izraz[indeks_tockice:]) != 1:
            novi_izraz = []

            if len(izraz[:indeks_tockice]) == 1:
                novi_izraz += list(izraz[:indeks_tockice])
            else:
                novi_izraz += izraz[:indeks_tockice]

            novi_izraz += list(izraz[indeks_tockice + 1])

            novi_izraz += ['.']

            if len(izraz[indeks_tockice + 2:]) == 1:
                novi_izraz += list(izraz[indeks_tockice + 2:])
            else:
                novi_izraz += izraz[indeks_tockice + 2:]

            return nezavrsni_znak, novi_izraz
        print(2)
        print(produkcija)
        return produkcija

    def provjeri_prijelaz(self, produkcija, znak):
        #print('PRODUKCIJAAA:', produkcija)
        try:
            nezavrsni_znak = produkcija[0]
            izraz = produkcija[1]
            indeks_tockice = izraz.index('.')
            if znak == izraz[indeks_tockice + 1]:
                return True
            if ' ' == izraz[indeks_tockice + 1]:
                return False
        except:
            return False

    def vrati_prijelaze(self, produkcije, znak):
        novi_prijelazi = []
        for produkcija in produkcije:
            if self.provjeri_prijelaz(produkcija, znak):
                novi_prijelaz = self.pomakni_tocku(produkcija)
                novi_prijelazi.append(novi_prijelaz)
        if len(novi_prijelazi) == 0:
            return []
        return self.nadji_produkcije_za_stanja([novi_prijelazi])

    def vrati_sve_znakove_gramatike(self):
        znakovi_gramatike = []
        for produkcije in self.pravila:
            for produkcija in produkcije:
                for znak in produkcija:
                    znak_je_slovo = znak.isalpha()
                    if znak_je_slovo:
                        znakovi_gramatike.append(znak)
        return set(znakovi_gramatike)

    def nadji_produkcije(self, nezavrsni_znak):
        #print('GRESKA', nezavrsni_znak)
        if nezavrsni_znak == '$':
            return 1
        if nezavrsni_znak not in self.rjecnik_gramatike.keys():
            return 1
        return self.rjecnik_gramatike[nezavrsni_znak]