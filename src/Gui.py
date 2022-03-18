import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from src.Dama import *

sep = os.sep


class Slika(QWidget):
    def __init__(self, putanja):
        QWidget.__init__(self)
        self.picture = QPixmap(putanja)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.picture)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        screen_resolution = QApplication.desktop().screenGeometry()
        width, height = screen_resolution.width(), screen_resolution.height()
        self.setWindowTitle("Dame")
        self.width = 800
        self.height = 600
        self.left = (width - self.width) // 2
        self.top = (height - self.height) // 2
        self.setFixedSize(self.width, self.height)
        self.u_toku = False
        self.prvi_potez = 0  # ako igrac zapocinje onda se postavlja na 1, u suprotnom je -1
        self.brojac_poteza = 1
        self._kraj_igre = True
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None
        self.x_dalje = None
        self.y_dalje = None
        self.skoci_ponovo = False
        self.partija = None
        self.znak = "-"  # da li je igrac pojeo ili ne "-" ili "x"
        self.pasivna_igra = 0

        # putanje do slika
        self.prvi = ".." + sep + "Checkers" + sep + "images" + sep + "crni.png"
        self.prvi_dama = ".." + sep + "Checkers" + sep + "images" + sep + "crni_dama.png"
        self.prvi_oznaceni = ".." + sep + "Checkers" + sep + "images" + sep + "crni_oznaceni.png"
        self.prvi_dama_oznaceni = ".." + sep + "Checkers" + sep + "images" + sep + "crni_dama_oznaceni.png"
        self.drugi = ".." + sep + "Checkers" + sep + "images" + sep + "crveni.png"
        self.drugi_dama = ".." + sep + "Checkers" + sep + "images" + sep + "crveni_dama.png"
        self.drugi_dama_oznaceni = ".." + sep + "Checkers" + sep + "images" + sep + "crveni_dama_oznaceni.png"
        self.drugi_oznaceni = ".." + sep + "Checkers" + sep + "images" + sep + "crveni_oznaceni.png"
        self.crno_polje = ".." + sep + "Checkers" + sep + "images" + sep + "crno_polje.png"
        self.belo_polje = ".." + sep + "Checkers" + sep + "images" + sep + "belo_polje.png"
        self.crno_polje_oznaceno = ".." + sep + "Checkers" + sep + "images" + sep + "crno_polje_oznaceno.png"

        nova_igra_btn = QPushButton("Nova igra", self)
        nova_igra_btn.setFixedSize(100, 50)
        nova_igra_btn.move(90, 510)

        predaj_btn = QPushButton("Predaj", self)
        predaj_btn.setFixedSize(100, 50)
        predaj_btn.move(310, 510)

        self.vreme_label = QLabel("Vreme")
        self.vreme_label.setFont(QFont("Times New Roman", 12))
        self.vreme_label_vrednost = QLabel("0 : 0 : 0")
        self.vreme = QTime().currentTime()

        self.vreme_label_vrednost.setFont(QFont("Times New Roman", 12))
        self.poruka_label = QLabel("")
        self.poruka_label.setFont(QFont("Times New Roman", 12))

        self.tabla = QTableWidget(8, 8, self)
        self.tabla.verticalHeader().setDefaultSectionSize(60)
        self.tabla.horizontalHeader().setDefaultSectionSize(60)
        self.tabla.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tabla.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tabla.setFixedSize(482, 482)
        self.tabla.verticalHeader().hide()
        self.tabla.horizontalHeader().hide()
        self.tabla.cellClicked.connect(self.klik_tabla)

        self.dock_widget = QDockWidget()
        self.dock_widget.setAllowedAreas(Qt.RightDockWidgetArea)
        self.dock_widget.setFloating(False)
        self.dock_widget.setFixedWidth(self.width * 0.3)
        self.dock_widget.setFixedHeight(self.height * 0.6)
        self.dock_widget.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.dock_widget.setWindowTitle("Lista poteza")
        self.lista_poteza = QListWidget()
        self.dock_widget.setWidget(self.lista_poteza)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_widget)

        self.centralni = QWidget()
        layout_btns = QHBoxLayout()
        layout_btns.addWidget(nova_igra_btn)
        layout_btns.addWidget(predaj_btn)
        layout = QVBoxLayout()
        layout.addWidget(self.tabla)
        layout.addLayout(layout_btns)
        layout_pomocni = QVBoxLayout()
        layout_pomocni.addSpacing(10)
        layout_pomocni.addWidget(self.vreme_label, alignment=Qt.AlignCenter)
        layout_pomocni.addWidget(self.vreme_label_vrednost, alignment=Qt.AlignCenter)
        layout_pomocni.addSpacing(40)
        layout_pomocni.addWidget(self.dock_widget)
        layout_pomocni.setSpacing(20)
        layout_pomocni.addWidget(self.poruka_label, alignment=Qt.AlignCenter)
        layout_pomocni.addSpacing(40)
        layout_final = QHBoxLayout()
        layout_final.addLayout(layout)
        layout_final.addLayout(layout_pomocni)
        self.centralni.setLayout(layout_final)
        self.setCentralWidget(self.centralni)

        nova_igra_btn.clicked.connect(self.nova_igra_upit)
        predaj_btn.clicked.connect(self.predaj)

        self.postavi_tablu()
        self.tabla.setEnabled(False)

        self.show()

    def predaj(self):
        if self.u_toku:
            predajBox = QMessageBox.question(self, 'Predaj?', 'Da li ste sigurni?',
                                             QMessageBox.Yes, QMessageBox.No)
            if predajBox == QMessageBox.Yes:
                self._kraj_igre = True
                self.osvezi()
                self.tajmer.stop()
                self.u_toku = False

    def postavi_tablu(self):
        for y in range(8):
            for x in range(8):
                if (x + y) % 2 == 1:
                    self.tabla.setCellWidget(y, x, Slika(self.crno_polje))
                else:
                    self.tabla.setCellWidget(y, x, Slika(self.belo_polje))

    def nova_igra_upit(self):
        if self.u_toku:
            predajBox = QMessageBox.question(self, 'Nova partija', 'Partija je u toku. Započeti novu?',
                                             QMessageBox.Yes, QMessageBox.No)
            if predajBox == QMessageBox.Yes:
                self._kraj_igre = True
            else:
                return

        self.nova_opcije = QDialog()
        self.nova_opcije.setWindowTitle("Nova igra")

        self.btn_crni = QCheckBox()
        self.btn_crni.setFixedSize(85, 30)
        self.btn_crni.setChecked(True)
        self.btn_crni.setText("Igraj prvi")
        self.btn_crni.clicked.connect(self.ugasi_crveni)

        self.btn_crveni = QCheckBox()
        self.btn_crveni.setFixedSize(85, 30)
        self.btn_crveni.setChecked(False)
        self.btn_crveni.setText("Igraj drugi")
        self.btn_crveni.clicked.connect(self.ugasi_crni)

        self.btn_potvrdi = QPushButton()
        self.btn_potvrdi.setFixedSize(80, 40)
        self.btn_potvrdi.setText("Potvrdi")
        self.btn_potvrdi.clicked.connect(self.potvrda_nove_igre)

        self.o_skok = QCheckBox()
        self.o_skok.setText("Obavezan skok")
        self.o_skok.setChecked(True)

        layout = QVBoxLayout()
        layout.addWidget(self.btn_crni)
        layout.addWidget(self.btn_crveni)
        layout1 = QHBoxLayout()
        layout1.addLayout(layout)
        layout1.addSpacing(50)
        layout1.addWidget(self.o_skok, alignment=Qt.AlignCenter)
        layout_final = QVBoxLayout()
        layout_final.addLayout(layout1)
        layout_final.addWidget(self.btn_potvrdi, alignment=Qt.AlignCenter)
        self.nova_opcije.setLayout(layout_final)
        self.nova_opcije.show()

    def ugasi_crveni(self):
        self.btn_crveni.setChecked(False)
        self.btn_crni.setChecked(True)

    def ugasi_crni(self):
        self.btn_crveni.setChecked(True)
        self.btn_crni.setChecked(False)

    def potvrda_nove_igre(self):
        self.partija = Dama()

        self._kraj_igre = False
        self.lista_poteza.clear()
        if self.btn_crveni.isChecked():  # komp je prvi
            self.partija.set_potez(-1)
            self.prvi_potez = -1
            self.swap()
            self.komp_na_potezu()
        else:  # igrac je prvi
            self.partija.set_potez(1)
            self.prvi_potez = 1
        self.partija.set_obavezan(self.o_skok.isChecked())
        self.nova_opcije.hide()
        self.pasivna_igra = 0
        self.nova_igra()

    def swap(self):
        self.prvi, self.drugi = self.drugi, self.prvi
        self.prvi_dama, self.drugi_dama = self.drugi_dama, self.prvi_dama
        self.prvi_oznaceni, self.drugi_oznaceni = self.drugi_oznaceni, self.prvi_oznaceni
        self.prvi_dama_oznaceni, self.drugi_dama_oznaceni = self.drugi_dama_oznaceni, self.prvi_dama_oznaceni

    def nova_igra(self):
        self.tajmer = QTimer()
        self.tajmer.timeout.connect(self.osvezi_vreme)
        self.tajmer.setInterval(200)
        self.tajmer.start()
        self.vreme = QTime()
        self.vreme.start()

        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None

        self.tabla.setEnabled(True)
        self.u_toku = True
        self.osvezi()

    def osvezi_vreme(self):
        ukupno = self.vreme.elapsed() // 1000
        if ukupno > 3600:
            self.u_toku = False
        sekunde = ukupno % 60
        minuti = (ukupno // 60) % 60
        sati = (ukupno // 3600) % 24
        self.vreme_label_vrednost.setText(str(sati) + " : " + str(minuti) + " : " + str(sekunde))

    def osvezi(self):
        self.postavi_tablu()  # sklanjamo sve figure pa onda stavljamo nove
        for y in range(8):
            for x in range(8):
                figura = self.partija.tabla.figura_na_polju(x, y)
                if figura:
                    if figura.get_vlasnik() == "komp":
                        if figura.get_tip() == 1:
                            self.tabla.setCellWidget(x, y, Slika(self.drugi_dama))
                        else:
                            self.tabla.setCellWidget(x, y, Slika(self.drugi))

                    elif figura.get_vlasnik() == "igrac":
                        if figura.get_tip() == 1:
                            self.tabla.setCellWidget(x, y, Slika(self.prvi_dama))
                        else:
                            self.tabla.setCellWidget(x, y, Slika(self.prvi))

        if self.partija.get_potez() == -1:
            self.poruka_label.setText("Protivnik razmislja")
        else:
            self.poruka_label.setText("Vi ste na potezu")
        self.kraj_partije()
        if self._kraj_igre:
            self.u_toku = False

    def komp_na_potezu(self):
        if self.partija.get_potez() == -1 and not self._kraj_igre:
            komp_potez = self.partija.komp_potez()
            self.osvezi()
            if komp_potez:
                self.dodaj_u_listu_komp(komp_potez[0], komp_potez[1], komp_potez[2], komp_potez[3], komp_potez[4])
                self.oznaci_polje(komp_potez[0], komp_potez[1])
                self.oznaci_polje(komp_potez[2], komp_potez[3])
                self.x1 = None
                self.y1 = None

    def odredi_poteze(self):
        potezi = []
        if self.x1 is not None:
            if self.partija.get_obavezan():
                potezi = self.partija.skokovi_lista("igrac")
                if len(potezi) == 0:
                    potezi = self.partija.kretanje(self.x1, self.y1)
            else:
                potezi = self.partija.kretanje(self.x1, self.y1) + self.partija.skokovi(self.x1, self.y1)
        return potezi

    def igrac_na_potezu(self, x, y):
        if self.skoci_ponovo is True:
            potezi = self.partija.skokovi(self.x1, self.y1)
        else:
            potezi = self.odredi_poteze()

        if self.x1 is None or (self.x1, self.y1, x, y) not in potezi:
            self.klik(x, y)
        else:  # kada smo prethodno kliknuli na figuru, onda novi klik postaje odrediste
            self.x2 = x
            self.y2 = y
            self.x_dalje = x
            self.y_dalje = y

            if abs(self.x1 - self.x2) == 2:  # "pojeo sam"
                self.znak = "x"
                self.pasivna_igra = 0

            novi_skokovi = []
            if self.partija.get_potez() == 1:  # ako smo mi na potezu
                self.partija.odigraj(self.x1, self.y1, self.x2, self.y2)
                self.osvezi()
                novi_skokovi = self.partija.skokovi(self.x_dalje, self.y_dalje)

            if self.partija.get_potez() == 1 and not self._kraj_igre:
                if len(novi_skokovi) == 0 or abs(self.x_dalje - self.x1) == 1:
                    self.skoci_ponovo = False
                    self.dodaj_u_listu_igrac(self.x1, self.y1, self.x2, self.y2)
                    self.partija.kraj_poteza()
                    self.x1 = None
                    self.y1 = None
                    self.osvezi()
                    self.komp_na_potezu()
                else:
                    self.skoci_ponovo = True
            else:
                self.komp_na_potezu()

    def klik_tabla(self, x, y):
        if not self._kraj_igre:
            self.znak = "-"
            self.igrac_na_potezu(x, y)
            self.znak = "-"
            self.x2 = None
            self.y2 = None

    def klik(self, x, y):
        if self.partija.tabla.postoji_figura(x, y):
            if self.partija.tabla.figura_na_polju(x, y).get_vlasnik() == "igrac":
                self.x1 = x
                self.y1 = y
                self.oznaci_dosupne(self.x1, self.y1, self.partija.svi_potezi("igrac"))

    def oznaci_polje(self, x, y):
        figura = self.partija.tabla.figura_na_polju(x, y)
        if figura:
            if figura.get_vlasnik() == "komp":
                if figura.get_tip() == 1:
                    self.tabla.setCellWidget(x, y, Slika(self.drugi_dama_oznaceni))
                else:
                    self.tabla.setCellWidget(x, y, Slika(self.drugi_oznaceni))
            else:
                if figura.get_tip() == 1:
                    self.tabla.setCellWidget(x, y, Slika(self.prvi_dama_oznaceni))
                else:
                    self.tabla.setCellWidget(x, y, Slika(self.prvi_oznaceni))
        elif (x + y) % 2 == 1:
            self.tabla.setCellWidget(x, y, Slika(self.crno_polje_oznaceno))

    def oznaci_dosupne(self, x, y, lista_poteza):
        self.ukloni_oznake()
        self.oznaci_polje(x, y)
        for potez in lista_poteza:
            if x == int(potez[0]) and y == int(potez[1]):  # nepotrebno ali za svaki slucaj
                x_oznaceno = potez[2]
                y_oznaceno = potez[3]
                self.oznaci_polje(x_oznaceno, y_oznaceno)

    def ukloni_oznake(self):
        for i in range(8):
            for j in range(8):
                figura = self.partija.tabla.figura_na_polju(i, j)
                if figura:
                    if figura.get_vlasnik() == "igrac":
                        if figura.get_tip() == 1:
                            self.tabla.setCellWidget(i, j, Slika(self.prvi_dama))
                        else:
                            self.tabla.setCellWidget(i, j, Slika(self.prvi))
                elif (i + j) % 2 == 1:
                    self.tabla.setCellWidget(i, j, Slika(self.crno_polje))

    def dodaj_u_listu_komp(self, x, y, x1, x2, znak):
        item = QListWidgetItem()
        if znak == "x":
            self.pasivna_igra = 0
        if self.prvi_potez == -1:
            item.setText(str(self.brojac_poteza) + ":  " + str(x) + str(y) + str(znak) + str(x1) + str(x2))
        else:
            item.setText(" " * (len(str(self.brojac_poteza)) + 4) + str(x) + str(y) + str(znak) + str(x1) + str(x2))
        self.lista_poteza.addItem(item)
        self.brojac_poteza += 1
        self.pasivna_igra += 1

    def dodaj_u_listu_igrac(self, x, y, x1, x2):
        item = QListWidgetItem()
        if self.prvi_potez == 1:
            item.setText(str(self.brojac_poteza) + ":  " + str(x) + str(y) + str(self.znak) + str(x1) + str(x2))
        else:
            item.setText(" " * (len(str(self.brojac_poteza)) + 4) + str(x) + str(y) + str(self.znak) + str(x1) + str(x2))
        self.lista_poteza.addItem(item)

    def kraj_partije(self):
        kraj = self.partija.pobeda()
        if kraj == "komp":
            self.poruka_label.setText("Pobedio je računar!")
        elif kraj == "igrac":
            self.poruka_label.setText("Vi ste pobedili!")
        if self.pasivna_igra >= 20:
            procena = self.ocena_table_kraj()
            if procena == "komp":
                self.poruka_label.setText("Pasivna igra\nPobedio je računar!")
            elif procena == "igrac":
                self.poruka_label.setText("Pasivna igra\nVi ste pobedili!")
            self._kraj_igre = True
        if kraj:
            self._kraj_igre = True
        if self._kraj_igre:
            self.tajmer.stop()
            self.brojac_poteza = 0

    def ocena_table_kraj(self):
        if self.partija.oceni_tablu() > 0:
            return "komp"
        else:
            return "igrac"

    def closeEvent(self, event):
        zatvori = QMessageBox.question(self, 'Izlaz', 'Da li ste sigurni da zelite da izadjete?', QMessageBox.No,
                                       QMessageBox.Yes)
        if zatvori == QMessageBox.Yes:
            self.u_toku = False
            event.accept()
        else:
            event.ignore()
