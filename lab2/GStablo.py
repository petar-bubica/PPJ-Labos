class GStablo:
    #indeks - broj razmaka
    def __init__(self,vrijednost):
        self.vrijednost = vrijednost
        self.djeca = []
    def vratiVrijednost(self):
        return self.vrijednost
    def vratiDjecu(self):
        return self.djeca
    def dodajDijete(self, dijete):
        djeca.append(dijete)
    def ispis(self,indeks):
        for i in range(0,indeks):
            print(" ")
    def ispisiPodstablo(self,indeks):
        self.ispis(indeks)
        print(self.vratiVrijednost())
        for i in range(len(djeca)-1,0,-1):
            djeca[i].ispisiPodstablo(indeks+1)
