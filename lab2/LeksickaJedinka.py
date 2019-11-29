class LeksickaJedinka:

    def __init__(self,input):
        uniformniZnakoviLista = input.split(" ")
        self.uniformniZnak = uniformniZnakoviLista[0]
        self.brojRetka = uniformniZnakoviLista[1]
        self.leksickaJedinka = uniformniZnakoviLista[2]

    def ispis(self):
        return (self.uniformniZnak + " " + self.brojRetka + " " + self.leksickaJedinka)





