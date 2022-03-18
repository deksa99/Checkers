# logika igre - provera mogucih poteza i nalazenje najboljeg

from src.Tabla import *
from copy import deepcopy
# from time import time


class Dama(object):
    def __init__(self):
        self.tabla = Tabla()
        self._potez = 1  # 1 - prvi je igrac, -1 - prvi je racunar
        self._najbolji_potez = None
        self.obavezan_skok = True
        self.kraj_igre = False
        self.odigran = (None, None)  # x i y (gde)
        self.odigran_igrac = (None, None)  # isto to samo kad je igrac na potezu

        for i in range(3):  # dodaj gornja tri reda (racunareve figure)
            for j in range(8):
                if (i + j) % 2 == 1:  # ako su crna polja
                    self.tabla.dodaj_figuru(0, "komp", i, j)

        for i in range(5, 8):
            for j in range(8):
                if (i + j) % 2 == 1:
                    self.tabla.dodaj_figuru(0, "igrac", i, j)

    def set_obavezan(self, val):
        self.obavezan_skok = val

    def get_obavezan(self):
        return self.obavezan_skok

    def get_potez(self):
        return self._potez

    def set_potez(self, ko):
        self._potez = ko

    def pobeda(self):
        if self.tabla.get_broj_figura_igrac() == 0 or len(self.svi_potezi("igrac")) == 0:
            self.kraj_igre = True
            return "komp"
        elif self.tabla.get_broj_figura_komp() == 0 or len(self.svi_potezi("komp")) == 0:
            self.kraj_igre = True
            return "igrac"

    def _postavi_tablu(self, kod):
        for i in range(len(kod)):
            x = i // 8
            y = i % 8
            self.tabla.ukloni_figuru(x, y)
            if kod[i] == "k":
                self.tabla.dodaj_figuru(0, "komp", x, y)
            if kod[i] == "K":
                self.tabla.dodaj_figuru(1, "komp", x, y)
            if kod[i] == "i":
                self.tabla.dodaj_figuru(0, "igrac", x, y)
            if kod[i] == "I":
                self.tabla.dodaj_figuru(1, "igrac", x, y)

    def _stampaj(self):
        for i in range(8):
            for j in range(8):
                if self.tabla.postoji_figura(i, j):
                    figura = self.tabla.figura_na_polju(i, j)
                    if figura.get_vlasnik() == "komp":
                        if figura.get_tip() == 1:
                            print("K", end=" ")
                        else:
                            print("k", end=" ")
                    else:
                        if figura.get_tip() == 1:
                            print("I", end=" ")
                        else:
                            print("i", end=" ")
                else:
                    print("-", end=" ")
            print()

    def kretanje(self, x, y):  # vraca listu polja gde figura moze da ode (ne skace, obican potez) [(x, y, x1, y1)...]
        lista_poteza = []
        smer = 0
        figura = self.tabla.figura_na_polju(x, y)
        if figura:
            if figura.get_tip() == 0:  # ako je obicna figura onda moze na gore ako je igrac, tj na dole ako je racunar
                if figura.get_vlasnik() == "komp":
                    smer = 1
                if figura.get_vlasnik() == "igrac":
                    smer = -1
                for j in [-1, 1]:
                    if self.tabla.validno_polje(x + smer, y + j) and not self.tabla.postoji_figura(x + smer, y + j):
                        lista_poteza.append((x, y, x + smer, y + j))
            if figura.get_tip() == 1:
                for i in [-1, 1]:
                    for j in [-1, 1]:
                        if self.tabla.validno_polje(x + i, y + j) and not self.tabla.postoji_figura(x + i, y + j):
                            lista_poteza.append((x, y, x + i, y + j))
        return lista_poteza

    def skokovi(self, x, y):
        lista_poteza = []
        smer = 0
        figura = self.tabla.figura_na_polju(x, y)
        if figura:
            if figura.get_tip() == 0:
                if figura.get_vlasnik() == "komp":
                    smer = 1
                if figura.get_vlasnik() == "igrac":
                    smer = -1
                for j in [-1, 1]:
                    if self.tabla.validno_polje(x + smer, y + j) and self.tabla.postoji_figura(x + smer, y + j):
                        if figura.get_vlasnik() != self.tabla.figura_na_polju(x + smer, y + j).get_vlasnik() and \
                                self.tabla.validno_polje(x + 2 * smer, y + 2 * j) and \
                                not self.tabla.postoji_figura(x + 2 * smer, y + 2 * j):
                            lista_poteza.append((x, y, x + 2 * smer, y + 2 * j))
            if figura.get_tip() == 1:
                for i in [-1, 1]:
                    for j in [-1, 1]:
                        if self.tabla.validno_polje(x + i, y + j) and self.tabla.postoji_figura(x + i, y + j):
                            if figura.get_vlasnik() != self.tabla.figura_na_polju(x + i, y + j).get_vlasnik() \
                                    and self.tabla.validno_polje(x + 2 * i, y + 2 * j) and not \
                                    self.tabla.postoji_figura(x + 2 * i, y + 2 * j):
                                lista_poteza.append((x, y, x + 2 * i, y + 2 * j))
        return lista_poteza

    def kretanje_lista(self, ko_igra):
        svi_potezi = []
        for i in range(8):
            for j in range(8):
                if self.tabla.postoji_figura(i, j) and self.tabla.figura_na_polju(i, j).get_vlasnik() == ko_igra:
                    svi_potezi += self.kretanje(i, j)
        return svi_potezi

    def skokovi_lista(self, ko_igra):
        svi_skokovi = []
        for i in range(8):
            for j in range(8):
                if self.tabla.postoji_figura(i, j) and self.tabla.figura_na_polju(i, j).get_vlasnik() == ko_igra:
                    svi_skokovi += self.skokovi(i, j)
        return svi_skokovi

    def svi_potezi(self, ciji_su):
        svi_potezi = self.skokovi_lista(ciji_su) + self.kretanje_lista(ciji_su)
        return svi_potezi

    def odigraj(self, x, y, x1, y1):
        if abs(int(x) - int(x1)) == 2:
            x2 = (x + x1) // 2
            y2 = (y + y1) // 2
            self.tabla.ukloni_figuru(x2, y2)
        self.tabla.pomeri_figuru(x, y, x1, y1)

        for i in range(8):  # provera da li je obicna figura postala dama
            pre = None
            posle = None
            pre2 = None
            posle2 = None
            figura = self.tabla.figura_na_polju(0, i)
            figura2 = self.tabla.figura_na_polju(7, i)
            if figura:
                pre = figura.get_tip()
                if figura.get_vlasnik() == "igrac":
                    figura.set_tip(1)
                posle = figura.get_tip()
            if figura2:
                pre2 = figura2.get_tip()
                if figura2.get_vlasnik() == "komp":
                    figura2.set_tip(1)
                posle2 = figura2.get_tip()
            if pre != posle or pre2 != posle2:  # ako jeste tu se potez zavrsava
                if self.tabla.figura_na_polju(x1, y1).get_tip() == 1:
                    self.odigran = (None, None)
                    return True
                elif self.tabla.figura_na_polju(x1, y1).get_tip() == 0:
                    self.odigran_igrac = (None, None)
                    return True

        if len(self.skokovi(x1, y1)) != 0 and abs(x1 - x) != 1:  # ukoliko postoje skokovi i prethodno je bio skok
            if self.tabla.figura_na_polju(x1, y1).get_vlasnik() == "komp":
                self.odigran = (x1, y1)
                return False
            elif self.tabla.figura_na_polju(x1, y1).get_vlasnik() == "igrac":
                self.odigran_igrac = (x1, y1)
                return False
        else:
            if self.tabla.figura_na_polju(x1, y1).get_vlasnik() == "komp":
                self.odigran = (None, None)
                return True
            elif self.tabla.figura_na_polju(x1, y1).get_vlasnik() == "igrac":
                self.odigran_igrac = (None, None)
                return True

    def komp_potez(self):
        znak = "-"
        # t = time()
        self.nadji_najbolji(self, "komp", 0, float("-inf"), float("inf"))
        # print(time() - t)
        x = self._najbolji_potez[0]
        y = self._najbolji_potez[1]
        x1 = self._najbolji_potez[2]
        y1 = self._najbolji_potez[3]
        self.odigraj(x, y, x1, y1)
        x_start = x  # pocetne koordinate
        y_start = y
        if abs(x1 - x) == 2:  # ako se desio skok u ispisu poteza ce stajati "x"
            znak = "x"
        while self.odigran != (None, None):
            self.nadji_najbolji(self, "komp", 0, float("-inf"), float("inf"))
            x = self._najbolji_potez[0]
            y = self._najbolji_potez[1]
            x1 = self._najbolji_potez[2]
            y1 = self._najbolji_potez[3]
            self.odigraj(x, y, x1, y1)
        x_kraj = x1  # krajnje koordinate
        y_kraj = y1
        self.kraj_poteza()
        return x_start, y_start, x_kraj, y_kraj, znak

    def oceni_tablu(self):
        # ukoliko je igraceva obicna figura na protivnikovom polju njena vrednost raste, u suprotonom je 5
        igrac = 0
        komp = 0
        for i in range(4):
            for j in range(8):
                figura = self.tabla.figura_na_polju(i, j)
                if figura:
                    if figura.get_tip() == 0:
                        if figura.get_vlasnik() == "igrac":
                            igrac += 9 - i
                        if figura.get_vlasnik() == "komp":
                            komp += 5
                    if figura.get_tip() == 1:
                        if figura.get_vlasnik() == "igrac":
                            igrac += 11
                        if figura.get_vlasnik() == "komp":
                            komp += 11
        for i in range(4, 8):
            for j in range(8):
                figura = self.tabla.figura_na_polju(i, j)
                if figura:
                    if figura.get_tip() == 0:
                        if figura.get_vlasnik() == "igrac":
                            igrac += 5
                        if figura.get_vlasnik() == "komp":
                            komp += 2 + i
                    if figura.get_tip() == 1:
                        if figura.get_vlasnik() == "igrac":
                            igrac += 11
                        if figura.get_vlasnik() == "komp":
                            komp += 11
        return komp - igrac

    def nadji_najbolji(self, igra, ko_igra, sloj, alpha, beta):
        # print(sloj, "----------------------------")
        dubina = 3
        igra.pobeda()
        if sloj >= dubina or igra.kraj_igre:
            score = igra.oceni_tablu()
            return score
        # max
        if ko_igra == "komp" and not sloj == dubina:
            if igra.odigran != (None, None):
                potezi = igra.skokovi(igra.odigran[0], igra.odigran[1])
                
            elif igra.obavezan_skok:
                potezi = igra.skokovi_lista(ko_igra)
                if len(potezi) == 0:
                    potezi = igra.kretanje_lista(ko_igra)
            else:
                potezi = igra.skokovi_lista(ko_igra) + igra.kretanje_lista(ko_igra)

            for potez in potezi:
                nova_igra = deepcopy(igra)

                x1 = int(potez[0])
                y1 = int(potez[1])
                x2 = int(potez[2])
                y2 = int(potez[3])

                kraj = nova_igra.odigraj(x1, y1, x2, y2)  # jedno dete (na prethodnu tablu se doda odigran potez)
                # print("komp")
                # nova_igra._stampaj()
                # print(nova_igra.oceni_tablu())

                if kraj:
                    ko_igra = "igrac"
                    score = self.nadji_najbolji(nova_igra, ko_igra, sloj + 1, alpha, beta)
                else:  # ukoliko postoji jos skokova sloj se ne povecava, sve je to jedan potez
                    score = self.nadji_najbolji(nova_igra, ko_igra, sloj, alpha, beta)

                if score > alpha:
                    if sloj == 0:
                        self._najbolji_potez = x1, y1, x2, y2
                    alpha = score

                if alpha >= beta:
                    # print("max")
                    break

            return alpha
        # min
        elif ko_igra == "igrac" and not sloj == dubina:
            if igra.odigran_igrac != (None, None):
                potezi = igra.skokovi(igra.odigran_igrac[0], igra.odigran_igrac[1])
            elif igra.obavezan_skok:
                potezi = igra.skokovi_lista(ko_igra)
                if len(potezi) == 0:
                    potezi = igra.kretanje_lista(ko_igra)
            else:
                potezi = igra.skokovi_lista(ko_igra) + igra.kretanje_lista(ko_igra)
            for potez in potezi:
                nova_igra = deepcopy(igra)

                x1 = int(potez[0])
                y1 = int(potez[1])
                x2 = int(potez[2])
                y2 = int(potez[3])

                kraj_poteza = nova_igra.odigraj(x1, y1, x2, y2)
                # print("igrac")
                # nova_igra._stampaj()
                # print(nova_igra.oceni_tablu())

                if kraj_poteza:
                    ko_igra = "komp"
                    score = self.nadji_najbolji(nova_igra, ko_igra, sloj + 1, alpha, beta)
                else:
                    score = self.nadji_najbolji(nova_igra, ko_igra, sloj, alpha, beta)
                if score < beta:
                    beta = score
                if alpha >= beta:
                    # print("min")
                    break
            return beta

    def kraj_poteza(self):
        self._potez *= -1
