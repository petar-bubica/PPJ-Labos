class CvorStabla:

    def __init__(self, podaci, dubina):
        self.lista_djece = list()
        self.lista_tipova = list()
        self.podaci = podaci
        self.dubina = dubina

    def __repr__(self):
        #samo za ispis vrijednosti i dubine
        stringToString = "Dubina ovog čvora: " + str(self.dubina) + " " + "Podaci ovog čvora: " + str(self.podaci) + "\n"
        return stringToString

    def dodaj_dijete(self, cvor):
        if cvor is None:
            return
        cvor.dubina = self.dubina + 1
        self.lista_djece.append(cvor)

    def prikaziDjecu(self):
        for dijete in self.lista_djece:
            print(dijete, end=" ")
        return

    def prikaziTipove(self):
        for tip in self.lista_tipova:
            print(tip, end=" ")
        return
    #def ispis_podstabla(self):
