# predstavlja jednu figuru koju karakterise cija je ona (racunar ili igrac) i kakva je ona (obicna ili dama)


class Figura(object):
    def __init__(self, tip, vlasnik):
        self._tip = tip  # 0 - obicna, 1 - dama
        self._vlasnik = vlasnik  # "igrac" ili "komp"

    def set_tip(self, val):
        self._tip = val

    def get_tip(self):
        return self._tip

    def get_vlasnik(self):
        return self._vlasnik

    def __str__(self):
        if self._tip == 0:
            tip = "Obicna figura"
        else:
            tip = "Dama"
        return "Vlasnik = " + str(self._vlasnik) + "\n" + "Tip = " + tip
