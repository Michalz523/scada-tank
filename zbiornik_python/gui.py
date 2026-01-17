from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPen, QColor, QBrush, QFont
from PyQt6.QtCore import Qt
import math
import time

class WidokInstalacji(QWidget):
    def __init__(self, zbiorniki, symulator):
        super().__init__()
        self.zbiorniki = zbiorniki
        self.sym = symulator
        self.flow_offset = 0

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        font_b = QFont("Arial", 10, QFont.Weight.Bold)
        font_n = QFont("Arial", 8)
        self.flow_offset = (int(time.time() * 40)) % 40

        # POZYCJE ZBIORNIKÓW
        k_x, k_y = 300, 250 
        f_x, f_y = 600, 250   
        w_x, w_y = 900, 250 
        o_x, o_y = 600, 500   
        ch_x = 1100 
        ferm_x, ferm_y = 1350, 250

        def draw_p(points, f_val, col=QColor(80,80,80)):
            painter.setPen(QPen(QColor(60,60,60), 14))
            for i in range(len(points)-1):
                painter.drawLine(points[i][0], points[i][1], points[i+1][0], points[i+1][1])
            
            if f_val > 0:
                painter.setPen(QPen(col, 10))
                for i in range(len(points)-1):
                    painter.drawLine(points[i][0], points[i][1], points[i+1][0], points[i+1][1])
                
                # Animacja przepływu
                pen = QPen(Qt.GlobalColor.white, 4, Qt.PenStyle.DotLine)
                pen.setDashOffset(self.flow_offset)
                painter.setPen(pen)
                for i in range(len(points)-1):
                    painter.drawLine(points[i][0], points[i][1], points[i+1][0], points[i+1][1])

        painter.setPen(Qt.GlobalColor.white); painter.setFont(font_b)
        painter.drawText(125, 30, "SŁÓD"); painter.drawText(k_x + 90, 30, "WODA"); painter.drawText(w_x + 65, 30, "CHMIEL")

        #RURY PROCESOWE
        draw_p([(100,0), (100,50)], self.sym.flows["slod"], QColor(210,180,140))
        draw_p([(100, 170), (100, 210), (k_x+30, 210), (k_x+30, k_y)], self.sym.flows["slod"], QColor(210,180,140))
        draw_p([(k_x+70,0), (k_x+70, k_y)], self.sym.flows["woda"], QColor(0,150,255))
        draw_p([(k_x+50, k_y+120), (k_x+50, k_y+200), (f_x+25, k_y+200), (f_x+25, k_y+120)], self.sym.flows["zacier"], QColor(218,165,32))
        draw_p([(f_x+75, k_y+120), (f_x+75, o_y)], self.sym.flows["osad"], QColor(101,67,33))
        draw_p([(f_x+100, k_y+60), (w_x, k_y+60)], self.sym.flows["brzeczka"], QColor(218,165,32))
        draw_p([(w_x+50, 0), (w_x+50, w_y)], self.sym.flows["chmiel"], QColor(0,200,0))
        draw_p([(w_x+100, k_y+60), (ch_x, k_y+60)], self.sym.flows["chlodzenie"], QColor(0,150,255))
        draw_p([(ch_x+100, k_y+60), (ferm_x, k_y+60)], self.sym.flows["chlodzenie"], QColor(0,150,255))

        # ROZLEWNIK
        t_y = ferm_y + 350
        f_r = self.sym.flows.get("rozlew", 0)
        p_color = QColor(218, 165, 32) # Piwo

        draw_p([(ferm_x + 50, ferm_y + 120), (ferm_x + 50, t_y - 120)], f_r, p_color)
        draw_p([(ferm_x + 10, t_y - 120), (ferm_x + 90, t_y - 120)], f_r, p_color)
        draw_p([(ferm_x + 10, t_y - 120), (ferm_x + 10, t_y - 70)], f_r, p_color) # Lewa
        draw_p([(ferm_x + 50, t_y - 120), (ferm_x + 50, t_y - 70)], f_r, p_color) # Środkowa
        draw_p([(ferm_x + 90, t_y - 120), (ferm_x + 90, t_y - 70)], f_r, p_color) # Prawa

        #CHŁODNICA
        painter.setBrush(QColor(50, 50, 150)); painter.setPen(QPen(Qt.GlobalColor.cyan, 2))
        painter.drawRect(ch_x, k_y + 45, 100, 30)
        painter.setPen(Qt.GlobalColor.white); painter.setFont(font_n)
        painter.drawText(ch_x+5, k_y+40, "CHŁODNICA")

        #OBNIŻONY TAŚMOCIĄG I 3 BUTELKI
        painter.setPen(QPen(QColor(80, 80, 80), 6))
        painter.drawLine(ferm_x - 50, t_y, ferm_x + 150, t_y) 
        
        if self.sym.butelka_obecna:
            for off in [10, 50, 90]:
                bx = ferm_x + off - 10
        
                painter.setBrush(QColor(100, 70, 40)); painter.setPen(QPen(Qt.GlobalColor.black, 1))
                painter.drawRect(bx, t_y - 45, 20, 45)
                
                hb = int(45 * (self.sym.progres_butelki / 100))
                painter.setBrush(p_color)
                painter.drawRect(bx, t_y - hb, 20, hb)

        #ZBIORNIKI
        for z in self.zbiorniki:
            painter.setPen(QPen(Qt.GlobalColor.white, 2))
            painter.setBrush(Qt.BrushStyle.NoBrush); painter.drawRect(z.x, z.y, 100, 120)
            painter.setBrush(QBrush(QColor(*z.kolor) if isinstance(z.kolor, tuple) else QColor(z.kolor)))
            h = int(120 * (max(0, z.poziom) / z.max)); painter.drawRect(z.x, z.y+120-h, 100, h)
            painter.setPen(Qt.GlobalColor.white); painter.setFont(font_b); painter.drawText(z.x, z.y-10, z.nazwa)
            painter.setFont(font_n); off_x = 115; painter.drawText(z.x+off_x, z.y+15, f"STAN: {z.stan_tekst}")
            if z.nazwa in ["Srutownik", "Zbiornik na Odpady"]:
                painter.drawText(z.x+off_x, z.y+30, f"V: {z.poziom:.1f} kg")
            elif z.nazwa == "Fermentor":
                painter.drawText(z.x+off_x, z.y+30, f"V: {z.poziom:.1f} L"); painter.drawText(z.x+off_x, z.y+45, f"CO2: {self.sym.cisnienie_co2:.2f} bar")
            else:
                painter.drawText(z.x+off_x, z.y+30, f"TEMP: {z.temperatura:.1f} C"); painter.drawText(z.x+off_x, z.y+45, f"V: {z.poziom:.1f} L")