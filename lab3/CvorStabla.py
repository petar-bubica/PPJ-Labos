from CvorTablice import CvorTablice


class CvorStabla:

    def __init__(self, podaci, dubina):
        self.lista_djece = list()
        self.lista_tipova = list()
        self.lista_imena = list()
        self.podaci = podaci.strip()
        self.dubina = dubina
        self.velicina_niza = -1
        self.je_l_vrijednost = False
        self.je_konstanta = False
        self.je_definiran = False
        self.je_u_petlji = False
        self.ime = None
        self.tip = None

    def __repr__(self):
        ispis = str(self.dubina) + ' ' + str(self.podaci)
        return ispis

    def __str__(self):
        result = ""
        for cvor_dijete in self.lista_djece:
            if cvor_dijete.podaci[0] != '<':
                niz = cvor_dijete.podaci.split(' ')
                result += niz[0] + '(' + niz[1] + ',' + niz[2] + ')' + " "
            else:
                result += cvor_dijete.podaci + " "
        return result

    def dodaj_dijete(self, cvor):
        if cvor is None:
            return
        cvor.dubina = self.dubina + 1
        self.lista_djece.append(cvor)

    def dodaj_ime(self,ime):
        self.lista_imena.append(ime)

    def ispisi_podstablo(self, cvor):
        print(cvor.podaci, cvor.lista_djece)

        if len(cvor.lista_djece) == 0:
            return

        for dijete in cvor.lista_djece:
            self.ispisi_podstablo(dijete)

    def vrati_ime(self):
        return self.podaci[1: -1]

    def vrati_tipove(self, doseg):

        if self.podaci.startswith('IDN'):
            
            cvor_tablice = doseg.copy()
            
            while cvor_tablice is not None:
                for deklaracija in cvor_tablice.lista_deklaracija:
                    if deklaracija.ime == self.vrati_ime():
                        return deklaracija.vrati_tipove(None)
                cvor_tablice = cvor_tablice.roditelj
        
        return self.lista_tipova

    def vrati_tip(self, doseg):

        if self.podaci.startswith('IDN'):

            cvor_tablice = doseg.copy()
            
            while cvor_tablice is not None:
                for deklaracija in cvor_tablice.lista_deklaracija:
                    if deklaracija.ime == self.ime:
                        return deklaracija.vrati_tip(None)
                cvor_tablice = cvor_tablice.roditelj
        
        return self.tip

    def postavi_tip(self, tip):
        if self.tip == 'niz':
            self.tip += tip
        else:
            self.tip = tip

    def vrati_l_vrijednost(self, doseg):
        
        if self.podaci.startswith('IDN'):
            
            cvor_tablice = doseg.copy()

            while cvor_tablice is not None:
                for deklaracija in cvor_tablice.lista_deklaracija:
                    if deklaracija.vrati_ime() == self.ime:
                        return deklaracija.vrati_tip(doseg) == 'int' or deklaracija.vrati_tip(doseg) == 'char' and not deklaracija.je_funkcija()

    def je_funkcija(self):
        if self.lista_tipova:
            return True
        return False

    def dohvati_vrijednost_broja(self):
        niz = self.podaci.split(' ')
        if len(niz) > 4:
            return 1000000000
        return int(niz[2])

    def prikazi_djecu(self):
        for dijete in self.lista_djece:
            print(dijete.podaci, end=" ")
        return

    def prikazi_tipove(self):
        for tip in self.lista_tipova:
            print(tip, end=" ")
        return
