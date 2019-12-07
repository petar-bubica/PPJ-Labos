class automat:
    def __init__(self, pocetno=None):
        self.pocetno = pocetno
        self.stanja = set()
        self.prihvatljiva = set()
        self.prijelazi = {}
        self.ulazni_znakovi = set()

    def Stanja(self):
        return self.stanja

    def Prihvatljiva(self):
        return self.prihvatljiva

    def Prijelazi(self):
        return self.prijelazi

    def dodaj_pocetno(self, stanje):
        self.pocetno = stanje
        self.stanja.update([stanje])

    def dodaj_stanje(self, stanje):
        self.stanja.update([stanje])

    def dodaj_prihvatljivo(self, stanje):
        self.stanja.update([stanje])
        self.prihvatljiva.update([stanje])

    def izbrisi_stanje(self, stanje):
        self.stanja.remove(stanje)

    def dodaj_ulazni_znak(self, znak):
        self.ulazni_znakovi.update([znak])

    def izbrisi_ulazni_znak(self, znak):
        self.ulazni_znakovi.remove(znak)

    def dodaj_prijelaz(self, stanje_iz, stanje_u, prijelazni_znak):
        if stanje_iz not in self.prijelazi.keys():
            self.prijelazi[stanje_iz] = {}
        if prijelazni_znak not in self.prijelazi[stanje_iz].keys():
            self.prijelazi[stanje_iz][prijelazni_znak] = []
        self.prijelazi[stanje_iz][prijelazni_znak].append(stanje_u)

        self.stanja.update([stanje_iz, stanje_u])
        self.ulazni_znakovi.update([prijelazni_znak])

    def __str__(self):
        izlaz = ""
        for iz in self.prijelazi.keys():
            for znak in self.prijelazi[iz]:
                izlaz += str(iz) + str(' : ') + str(znak) + str(' -> ') + str(self.prijelazi[iz][znak]) + '\n'
        return izlaz

    def e_okruzenje(self, stanje):
        okruzenje = [stanje]
        i = 0
        while True:
            try:
                if '$' in self.prijelazi[okruzenje[i]].keys():
                    pom = self.prijelazi[okruzenje[i]]['$']
                    for prijelaz in pom:
                        if prijelaz not in okruzenje:
                            okruzenje.append(prijelaz)
            except KeyError:
                pass

            if okruzenje[i] == okruzenje[-1]:
                break
            i += 1
        return okruzenje

    def pretvori_u_NKA(self):
        pocetno_okruzenje = self.e_okruzenje(self.pocetno)
        for stanje in pocetno_okruzenje:
            if stanje in self.prihvatljiva:
                self.prihvatljiva.update([self.pocetno])
                break

        e_okruzenja = {}
        for stanje in self.stanja:
            e_okruzenja[stanje] = self.e_okruzenje(stanje)  # e-okruzenja svih stanja

        novi_prijelazi = {}

        if '$' in self.ulazni_znakovi:
            self.ulazni_znakovi.remove('$')

        for stanje_iz in self.prijelazi.keys():
            for prijelazni_znak in self.ulazni_znakovi:

                stanja_u = set()
                for stanje in e_okruzenja[stanje_iz]:
                    if stanje in self.prijelazi.keys():
                        if prijelazni_znak in self.prijelazi[stanje].keys():
                            stanja_u.update(
                                set(self.prijelazi[stanje][prijelazni_znak]))  # napravi uniju s novim stanjima

                for izbor in list(stanja_u):
                    stanja_u.update(set(e_okruzenja[izbor]))  # unija e_okruzenja svih stanja iz tog prijelaza

                if len(stanja_u) > 0:
                    if stanje_iz not in novi_prijelazi.keys():
                        novi_prijelazi[stanje_iz] = {}
                    if prijelazni_znak not in novi_prijelazi[stanje_iz].keys():
                        novi_prijelazi[stanje_iz][prijelazni_znak] = []
                    novi_prijelazi[stanje_iz][prijelazni_znak].extend(list(stanja_u))

        self.prijelazi = novi_prijelazi

    def pretvori_u_DKA(self):

        novo_pocetno = self.e_okruzenje(self.pocetno)
        novo_pocetno = ';'.join(novo_pocetno)

        self.pretvori_u_NKA()

        nova_stanja = set([self.pocetno])  # dodaj pocetno u stanja
        novi_prijelazi = {}
        treba_provjeriti = [self.pocetno]
        provjereno = []

        while len(treba_provjeriti) > 0:
            trenutno_stanje = treba_provjeriti[0]
            nova_stanja.update([trenutno_stanje])
            for ulazni_znak in self.ulazni_znakovi:
                if trenutno_stanje in self.prijelazi.keys():
                    if ulazni_znak in self.prijelazi[trenutno_stanje]:

                        prijelaz = sorted(self.prijelazi[trenutno_stanje][ulazni_znak])
                        novo_stanje = ';'.join(prijelaz)  # pretvori skup stanja u string ['q0','q1','q2]->'q0;q1;q2'

                        if novo_stanje not in provjereno:
                            treba_provjeriti.append(novo_stanje)

                        # dodavanje u prihvatljiva
                        if set(prijelaz).intersection(self.prihvatljiva) != set():
                            self.prihvatljiva.update([novo_stanje])

                        # dodavanje prijelaza
                        if trenutno_stanje not in novi_prijelazi.keys():
                            novi_prijelazi[trenutno_stanje] = {}
                        novi_prijelazi[trenutno_stanje][ulazni_znak] = novo_stanje

                else:
                    prijelaz = trenutno_stanje.split(';')
                    prijelaz = sorted(self.prijelaz_skup_stanja(prijelaz, ulazni_znak))

                    if prijelaz == []:  # ne postoji ni jedan prijelaz
                        continue

                    novo_stanje = ';'.join(prijelaz)

                    if novo_stanje not in provjereno:
                        treba_provjeriti.append(novo_stanje)

                    if trenutno_stanje not in novi_prijelazi.keys():
                        novi_prijelazi[trenutno_stanje] = {}
                    novi_prijelazi[trenutno_stanje][ulazni_znak] = novo_stanje

            provjereno.append(trenutno_stanje)
            treba_provjeriti.remove(trenutno_stanje)

        self.stanja = nova_stanja
        self.prijelazi = novi_prijelazi
        self.prihvatljiva.intersection_update(self.stanja)  # izbacuje nepostojeca stanja iz prihvatljivih

        pom = self.prijelazi[self.pocetno]
        del self.prijelazi[self.pocetno]
        self.prijelazi[novo_pocetno] = pom

        self.izbrisi_stanje(self.pocetno)
        self.dodaj_pocetno(novo_pocetno)

    def prijelaz_skup_stanja(self, stanja, prijelazni_znak):
        """Vraca skup svih stanja u koje jedan skup ide za jedan znak"""
        idu_u_stanja = set()
        for stanje in stanja:
            try:
                idu_u_stanja.update(self.prijelazi[stanje][prijelazni_znak])

            except KeyError:
                pass

        return idu_u_stanja
