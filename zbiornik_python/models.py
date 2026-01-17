class Zbiornik:
    def __init__(self, nazwa, x, y, pojemnosc, kolor):
        self.nazwa = nazwa
        self.x = x
        self.y = y
        self.max = pojemnosc
        self.poziom = 0.0
        self.kolor = kolor
        self.stan_tekst = "IDLE"
        self.temperatura = 20.0
        self.mieszadlo_on = False
        self.kat_mieszadla = 0