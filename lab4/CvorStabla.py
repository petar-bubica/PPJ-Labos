from lab4.CvorTablice import CvorTablice
from lab4 import config


class CvorStabla:

    def __init__(self, podaci, dubina):
        self.lista_djece = list()
        self.lista_tipova = list()
        self.lista_imena = list()
        self.podaci = str(podaci).strip()
        self.dubina = dubina
        self.velicina_niza = -1
        self.je_l_vrijednost = False
        self.je_konstanta = False
        self.je_definiran = False
        self.je_u_petlji = False
        self.ime = ''
        self.tip = ''

    def __repr__(self):
        #print("U repr metodi")
        ispis = str(self.dubina) + ' ' + str(self.podaci)
        return ispis

    def __str__(self):
        #print("U str metodi")
        result = ""
        for cvor_dijete in self.lista_djece:
            if cvor_dijete.podaci[0] != '<':
                niz = cvor_dijete.podaci.split(' ')
                result += niz[0] + '(' + niz[1] + ',' + niz[2] + ')' + " "
            else:
                result += cvor_dijete.podaci + " "
        return result

    def dodaj_dijete(self, cvor):
        #print("U dodaj dijete metodi")
        if cvor is None:
            return
        cvor.dubina = self.dubina + 1
        self.lista_djece.append(cvor)

    def dodaj_ime(self,ime):
        #print("U dodaj ime metodi")
        self.lista_imena.append(ime)

    def ispisi_podstablo(self, cvor):
        #print("U ispisi podstablo metodi")
        print(cvor.podaci, cvor.lista_djece)

        if len(cvor.lista_djece) == 0:
            return

        for dijete in cvor.lista_djece:
            self.ispisi_podstablo(dijete)

    def vrati_ime(self):
        #print("U vrati ime metodi")
        # print(self.podaci)
        if self.podaci[0] != '<':
            return self.podaci.split(' ')[2]
        return self.ime

    def vrati_tipove(self, doseg):
        #print(" U vrati tipove metodi")

        if self.podaci.startswith('IDN'):

            # cvor_tablice = CvorTablice(config.doseg.roditelj)
            # cvor_tablice.lista_deklaracija = config.doseg.lista_deklaracija

            cvor_tablice = doseg

            while cvor_tablice is not None:
                for deklaracija in cvor_tablice.lista_deklaracija:
                    if deklaracija.vrati_ime() == self.vrati_ime():   #promjena
                        return deklaracija.vrati_tipove(None)
                cvor_tablice = cvor_tablice.roditelj
        
        return self.lista_tipova

    def vrati_tip(self, doseg):
        #print("U vrati tip metodi")

        if self.podaci.startswith('IDN'):

            #cvor_tablice = CvorTablice(config.doseg.roditelj)
            #cvor_tablice.lista_deklaracija = config.doseg.lista_deklaracija

            cvor_tablice = doseg
            
            while cvor_tablice is not None:
                for deklaracija in cvor_tablice.lista_deklaracija:
                    #print('dekl:', deklaracija.podaci)
                    if deklaracija.vrati_ime() == self.vrati_ime():   #promjena
                        return deklaracija.vrati_tip(None)
                cvor_tablice = cvor_tablice.roditelj
        
        return self.tip

    def postavi_tip(self, tip):
        #print("U postavi tip metodi")
        if self.tip == 'niz':
            self.tip += tip
        else:
            self.tip = tip

    def vrati_l_vrijednost(self, doseg):
        #print("U vrati_l_ vrijednost metodi")
        
        if self.podaci.startswith('IDN'):

            # cvor_tablice = CvorTablice(config.doseg.roditelj)
            # cvor_tablice.lista_deklaracija = config.doseg.lista_deklaracija

            cvor_tablice = doseg

            while cvor_tablice is not None:
                for deklaracija in cvor_tablice.lista_deklaracija:
                    if deklaracija.vrati_ime() == self.vrati_ime():
                        return (deklaracija.vrati_tip(doseg) == 'int' or deklaracija.vrati_tip(doseg) == 'char') and not deklaracija.je_funkcija()
                cvor_tablice = doseg.roditelj
        return self.je_l_vrijednost

    def je_funkcija(self):
        #print("U je_funkcija metodi")
        if self.lista_tipova:
            return True
        return False

    def dohvati_vrijednost_broja(self):
        #print("U dohvati vrijednost broja metodi")
        niz = self.podaci.split(' ')
        if len(niz) > 4:
            return 1000000000
        return int(niz[2])

    def prikazi_djecu(self):
        #print("U prikazi djecu metodi")
        for dijete in self.lista_djece:
            print(dijete.podaci, end=" ")
        return

    def prikazi_tipove(self):
        #print("U prikazi tipove metodi")
        for tip in self.lista_tipova:
            print(tip, end=" ")
        return
