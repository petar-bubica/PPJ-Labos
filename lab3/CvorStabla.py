class CvorStabla:

    def __init__(self, podaci, dubina):
        self.lista_djece = list()
        self.lista_tipova = list()
        self.podaci = podaci.strip()
        self.dubina = dubina
        self.je_l_vrijednost = False
        self.je_konstanta = False
        self.je_definiran = False
        self.je_u_petlji = False

    def __repr__(self):
        ispis = str(self.dubina) + ' ' + str(self.podaci)
        return ispis

    def dodaj_dijete(self, cvor):
        if cvor is None:
            return
        cvor.dubina = self.dubina + 1
        self.lista_djece.append(cvor)

    def ispisi_podstablo(self, cvor):
        print(cvor.podaci, cvor.lista_djece)

        if len(cvor.lista_djece) == 0:
            return

        for dijete in cvor.lista_djece:
            self.ispisi_podstablo(dijete)

    def ime(self):
        return self.podaci[1: -1]

    def prikazi_djecu(self):
        for dijete in self.lista_djece:
            print(dijete.podaci, end=" ")
        return

    def prikazi_tipove(self):
        for tip in self.lista_tipova:
            print(tip, end=" ")
        return
