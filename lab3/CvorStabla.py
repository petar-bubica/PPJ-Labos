class CvorStabla:

    def __init__(self, podaci, dubina):
        self.lista_djece = list()
        self.lista_tipova = list()
        self.podaci = podaci
        self.dubina = dubina

    def dodaj_dijete(self, cvor):
        if cvor is None:
            return
        cvor.dubina = self.dubina + 1
        self.lista_djece.append(cvor)

    #def ispis_podstabla(self):
