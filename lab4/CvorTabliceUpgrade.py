
class CvorTabliceUpgrade:
    def __init__(self, labela, cvor_stabla):
        self.labela = labela
        self.cvor_stabla = cvor_stabla
        self.je_fja = False
        self.je_prazno = False

    def vrati_bitove(self):
        if self.cvor_stabla.vrati_ime().startswith("'"):
            broj = int(self.cvor_stabla.vrati_ime()[1])
        else:
            broj = int(self.cvor_stabla.vrati_ime())
        maska = (1 << 8) - 1
        i = 0
        var = "\t`DW "
        while i < 4:
            var += "%D " + str(broj & maska) + ", "
            broj >>= 8
            i += 1
        #duljina = len(var) - 2
        #print('vrati bitove: ', var + "\n")
        return var[:-2] + "\n"
