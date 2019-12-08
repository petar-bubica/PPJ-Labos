class CvorTablice:

    def __init__(self, roditelj=None):
        self.roditelj = roditelj
        self.je_u_petlji = None
        self.lista_deklaracija = list()

    def dodaj_dijete(self, dijete):
        self.lista_deklaracija.append(dijete)
