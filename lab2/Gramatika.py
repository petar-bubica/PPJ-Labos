class Gramatika:
    
    def __init__(self, pravila):
        self.pravila = self.parsiraj(pravila)

    def parsiraj(self, pravila):
        parsirana_pravila = list()
        for (nezavrsni_znak, lista_produkcija) in pravila:
            for produkcija in lista_produkcija:
                parsirana_pravila.append((nezavrsni_znak, produkcija))
        return parsirana_pravila

    def get_skup_ZAPOCNI(self):
        skup_ZAPOCNI = dict()
        epsilon = set()

        while True:
            bilo_je_promjena = False
            
            for (nezavrsni_znak, izraz) in self.pravila:
                for znak in izraz:
                    bilo_je_promjena |= self.unija(skup_ZAPOCNI[nezavrsni_znak], skup_ZAPOCNI[znak])
                    if znak not in epsilon:
                        break
                    else:
                        bilo_je_promjena |= self.unija(epsilon, {nezavrsni_znak})
            
            if not bilo_je_promjena:
                return skup_ZAPOCNI
    
    def unija(self, prvi_skup, drugi_skup):
        duljina_prvog_seta = len(prvi_skup)
        prvi_skup |= drugi_skup
        if len(prvi_skup) != duljina_prvog_seta:
            return True
        return False

    def dohvati_iduci_nezavrsni_znak(self, produkcija):
        produkcija = produkcija.replace(' ', '')
        slova_produkcije = list(produkcija)
        try:
            pozicija_tockice_u_produkciji = slova_produkcije.index('.')
            return slova_produkcije[pozicija_tockice_u_produkciji + 2] # +1 za iduci te +1 jer je zadnji znak iz SLIJEDI
        except IndexError:
            return '$'
    
    @staticmethod
    def je_nezavrsni_znak(simbol):
        simbol_je_slovo = simbol.isalpha()
        simbol_je_veliko_slovo = simbol.isuppercase()
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
        for (_, niz_znakova) in self.pravila:
            for znak in niz_znakova:
                znak_je_malo_slovo = znak.islowercase()
                if znak_je_malo_slovo:
                    skup_zavrsnih_znakova.add(znak)
    
    def vrati_znak_iza_tocke(self, produkcija):
        produkcija = produkcija.replace(' ', '')
        znakovi_produkcije = list(produkcija)
        try:
            pozicija_tockice_u_produkciji = znakovi_produkcije.index('.')
            return znakovi_produkcije[pozicija_tockice_u_produkciji + 1]
        except IndexError:
            return '$'

    def nadji_produkcije_za_stanja(self, lista_stanja):

        return