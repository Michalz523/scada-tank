import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, 
                             QWidget, QPushButton, QLabel, QFrame, QDialog, QSpinBox)
from PyQt6.QtCore import QTimer, Qt
from models import Zbiornik
from gui import WidokInstalacji
from logic import Symulator
import settings

class SetupDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Parametry Początkowe"); self.setFixedSize(300, 200)
        self.setStyleSheet("background-color: #2b2b2b; color: white;")
        l = QVBoxLayout(); l.addWidget(QLabel("<b>Zadaj cel produkcyjny (butelek):</b>"))
        self.s = QSpinBox(); self.s.setRange(0, 1000); self.s.setValue(40); l.addWidget(self.s)
        self.b = QPushButton("OTWÓRZ PANEL"); self.b.setMinimumHeight(40); self.b.clicked.connect(self.accept); l.addWidget(self.b)
        self.setLayout(l)

class MainWindow(QMainWindow):
    def __init__(self, cel):
        super().__init__()
        self.cel_produkcji = cel
        self.setWindowTitle("SCADA Browar - Pipeline Mode")
        self.setStyleSheet("background-color: #1e1e1e; color: white;")
        self.zbiorniki = [
            Zbiornik("Srutownik", 50, 50, 50, settings.COLOR_MALT),
            Zbiornik("Kadz Zacierna", 300, 250, 200, settings.COLOR_WORT_LIGHT),
            Zbiornik("Kadz Filtracyjna", 600, 250, 200, settings.COLOR_WORT_LIGHT),
            Zbiornik("Warzelnia", 900, 250, 200, settings.COLOR_WORT_DARK),
            Zbiornik("Zbiornik na Odpady", 600, 500, 100, settings.COLOR_WASTE),
            Zbiornik("Fermentor", 1350, 250, 200, (80, 120, 80))
        ]
        self.symulator = Symulator(self.zbiorniki)
        self.widok = WidokInstalacji(self.zbiorniki, self.symulator)

        mv = QVBoxLayout(); th = QHBoxLayout(); w = QWidget(); w.setLayout(mv); self.setCentralWidget(w)
        th.addWidget(self.widok, stretch=10)
        
        p = QVBoxLayout(); p.addWidget(QLabel("<b>STEROWANIE:</b>"))
        self.bs = QPushButton("START WARZENIA (PĘTLA)"); self.bs.setStyleSheet("background-color: green; font-weight: bold; min-height: 40px;")
        self.bs.clicked.connect(self.start_a); p.addWidget(self.bs)
        self.bt = QPushButton("STOP AWARYJNY"); self.bt.setStyleSheet("background-color: red; font-weight: bold; min-height: 40px;")
        self.bt.clicked.connect(self.stop_a); p.addWidget(self.bt)

        p.addWidget(QLabel("<b>ZUŻYCIE:</b>"))
        self.rm = QLabel("Słód: 0.0 kg"); p.addWidget(self.rm)
        self.rw = QLabel("Woda: 0.0 L"); p.addWidget(self.rw)
        self.rh = QLabel("Chmiel: 0.0 kg"); p.addWidget(self.rh)
        
        p.addWidget(QLabel(f"<b>CEL: {self.cel_produkcji} BUT.</b>"))
        self.lo = QLabel(""); self.lo.setStyleSheet("color: #4caf50; font-weight: bold;"); p.addWidget(self.lo)
        
        self.rb = QLabel("BUTELKI: 0"); p.addWidget(self.rb)
        self.rs = QLabel("SKRZYNKI: 0"); p.addWidget(self.rs)
        self.rp = QLabel("PALETY: 0.000"); p.addWidget(self.rp)
        
        p.addStretch(); th.addLayout(p, stretch=2); mv.addLayout(th)
        self.lt = QLabel("Czas pracy: 00:00:00"); mv.addWidget(self.lt)

        self.rt = 0.0; self.timer = QTimer(); self.timer.timeout.connect(self.odsw); self.timer.start(50)
        self.showMaximized()

    def start_a(self): self.symulator.stan = "RUN"
    def stop_a(self): self.symulator.stan = "IDLE"; self.symulator.reset_flows()

    def odsw(self):
        self.symulator.aktualizuj(); self.widok.update()
        if self.symulator.stan != "IDLE": self.rt += 0.05
        h, m, s = int(self.rt//3600), int((self.rt%3600)//60), int(self.rt%60)
        self.lt.setText(f"Czas pracy: {h:02d}:{m:02d}:{s:02d}")
        
        b = self.symulator.licznik_butelek
        self.rm.setText(f"Słód: {self.symulator.total_malt:.1f} kg")
        self.rw.setText(f"Woda: {self.symulator.total_water:.1f} L")
        self.rh.setText(f"Chmiel: {self.symulator.total_hops:.1f} kg")
        self.rb.setText(f"BUTELKI: {b}")
        self.rs.setText(f"SKRZYNKI: {b // 20}"); self.rp.setText(f"PALETY: {(b // 20) / 160:.3f}")
        if b >= self.cel_produkcji: self.lo.setText("✅ CEL OSIĄGNIĘTY")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    setup = SetupDialog()
    if setup.exec() == QDialog.DialogCode.Accepted:
        window = MainWindow(setup.s.value()); window.show(); sys.exit(app.exec())