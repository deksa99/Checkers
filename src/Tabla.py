# tabla (matrica figura)
from src.Figura import *


class Tabla(object):
    def __init__(self):
        self._matrica = []
        self._broj_figura_komp = 0
        self._broj_figura_igrac = 0
        for i in range(8):
            self._matrica.append([])
            for j in range(8):
                self._matrica[i].append(None)

    def get_broj_figura_komp(self):
        return self._broj_figura_komp

    def get_broj_figura_igrac(self):
        return self._broj_figura_igrac

    def stampaj_tablu(self):
        for i in range(8):
            print(self._matrica[i])
        print()

    def validno_polje(self, x, y):
        if 8 > int(x) >= 0 and 8 > int(y) >= 0:
            return True
        return False

    def postoji_figura(self, x, y):
        if self.validno_polje(x, y):
            if self._matrica[int(x)][int(y)] is not None:
                return True
        return False

    def dodaj_figuru(self, tip, vlasnik, x, y):
        figura = Figura(tip, vlasnik)
        if not self.postoji_figura(x, y):
            if figura.get_vlasnik() == "komp":
                self._matrica[int(x)][int(y)] = figura
                self._broj_figura_komp += 1
                return True
            elif figura.get_vlasnik() == "igrac":
                self._matrica[int(x)][int(y)] = figura
                self._broj_figura_igrac += 1
                return True
        else:
            return False

    def figura_na_polju(self, x, y):
        if self.postoji_figura(x, y):
            return self._matrica[int(x)][int(y)]

    def ukloni_figuru(self, x, y):
        if self.postoji_figura(x, y):
            figura = self.figura_na_polju(x, y)
            self._matrica[int(x)][int(y)] = None
            if figura.get_vlasnik() == "komp":
                self._broj_figura_komp -= 1
            if figura.get_vlasnik() == "igrac":
                self._broj_figura_igrac -= 1
            return figura

    def pomeri_figuru(self, x, y, x1, y1):
        figura = self.ukloni_figuru(x, y)
        if figura:
            self.dodaj_figuru(figura.get_tip(), figura.get_vlasnik(), x1, y1)
            return True
        else:
            return False
