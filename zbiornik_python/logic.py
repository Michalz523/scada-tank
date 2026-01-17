import settings

class Symulator:
    def __init__(self, zbiorniki):
        self.zbiorniki = {z.nazwa: z for z in zbiorniki}
        self.stan = "IDLE"
        self.tryb_auto = True
        
        
        self.st_srutownik = "IDLE"
        self.st_zacierna = "IDLE"
        self.st_filtracja = "IDLE"
        self.st_warzelnia = "IDLE"
        self.st_odpady = "IDLE" 
        
        self.licznik_mielenia = 0.0
        self.licznik_chmielu = 0.0
        self.temp_wejscie = 0.0
        self.temp_wyjscie = 0.0
        self.chlodzenie_active = False
        self.cisnienie_co2 = 0.0
        self.chmiel_flow = False
        self.licznik_butelek = 0
        self.progres_butelki = 0.0
        self.butelka_obecna = False
        
      
        self.total_malt = 0.0
        self.total_water = 0.0
        self.total_hops = 0.0
        self.total_waste = 0.0
        
        self.flows = {k: 0.0 for k in ["slod", "woda", "zacier", "brzeczka", "osad", "chmiel", "chlodzenie", "rozlew"]}

    def reset_flows(self):
        for k in self.flows: self.flows[k] = 0.0

    def aktualizuj(self):
        if self.stan == "IDLE":
            self.reset_flows()
            return

        srut = self.zbiorniki["Srutownik"]
        kadz = self.zbiorniki["Kadz Zacierna"]
        filt = self.zbiorniki["Kadz Filtracyjna"]
        warz = self.zbiorniki["Warzelnia"]
        odpad = self.zbiorniki["Zbiornik na Odpady"]
        ferm = self.zbiorniki["Fermentor"]
        self.reset_flows()

        #AUTOMATYCZNE OPRÓŻNIANIE ODPADÓW
        if odpad.poziom >= odpad.max and self.st_odpady == "IDLE":
            self.st_odpady = "OPROZNIANIE"

        if self.st_odpady == "OPROZNIANIE":
            odpad.stan_tekst = "WYWÓZ ODPADÓW"
            if odpad.poziom > 0:
                odpad.poziom -= 2.0 
                if odpad.poziom < 0: odpad.poziom = 0
            else:
                self.st_odpady = "IDLE"
        else:
            odpad.stan_tekst = "GOTOWY"

        #ŚRUTOWNIK
        if self.st_srutownik == "IDLE" and srut.poziom == 0:
            self.st_srutownik = "NAPELNIANIE"

        if self.st_srutownik == "NAPELNIANIE":
            srut.stan_tekst = "POBIERANIE"
            if srut.poziom < srut.max:
                srut.poziom += 1.0; self.total_malt += 1.0; self.flows["slod"] = 5.5
            else:
                self.st_srutownik = "MIELENIE"; self.licznik_mielenia = 0.0
        
        elif self.st_srutownik == "MIELENIE":
            srut.stan_tekst = "MIELENIE..."; srut.mieszadlo_on = True
            self.licznik_mielenia += 0.05
            srut.kat_mieszadla = (srut.kat_mieszadla + 40) % 360
            if self.licznik_mielenia >= 4.0:
                srut.mieszadlo_on = False; srut.stan_tekst = "ZMIELONE"
                self.st_srutownik = "GOTOWY_ZSYP"

        #KADŹ ZACIERNA
        if self.st_zacierna == "IDLE" and kadz.poziom == 0 and self.st_srutownik == "GOTOWY_ZSYP":
            self.st_zacierna = "POBIERANIE"

        if self.st_zacierna == "POBIERANIE":
            kadz.stan_tekst = "NAPEŁNIANIE"
            if srut.poziom > 0:
                srut.poziom -= 1.0; kadz.poziom += 1.0
                self.flows["slod"] = 8.0; self.flows["woda"] = 12.0; self.total_water += 1.0
            else:
                self.st_srutownik = "IDLE" 
                self.st_zacierna = "ZACIERANIE"

        elif self.st_zacierna == "ZACIERANIE":
            kadz.stan_tekst = "GOTOWANIE"; kadz.mieszadlo_on = True
            kadz.kat_mieszadla = (kadz.kat_mieszadla + 30) % 360
            if kadz.temperatura < 65: kadz.temperatura += 0.5
            else: self.st_zacierna = "GOTOWY_TRANSFER"

        #KADŹ FILTRACYJNA
        if self.st_filtracja == "IDLE" and filt.poziom == 0 and self.st_zacierna == "GOTOWY_TRANSFER":
            self.st_filtracja = "TRANSFER_IN"

        if self.st_filtracja == "TRANSFER_IN":
            kadz.stan_tekst = "WYDAWANIE"
            if kadz.poziom > 0:
                kadz.poziom -= 2.0; filt.poziom += 2.0; self.flows["zacier"] = 15.0
            else:
                kadz.temperatura = 20.0
                self.st_zacierna = "IDLE" 
                self.st_filtracja = "FILTRACJA"

        elif self.st_filtracja == "FILTRACJA":
            filt.stan_tekst = "FILTRACJA"
            if self.st_warzelnia == "IDLE" and warz.poziom <= 0 and self.st_odpady != "OPROZNIANIE":
                self.st_filtracja = "TRANSFER_OUT"

        elif self.st_filtracja == "TRANSFER_OUT":
            filt.stan_tekst = "WYDAWANIE"
            if filt.poziom > 0:
                t = min(2.0, filt.poziom)
                filt.poziom -= t
                warz.poziom += t * 0.7
                if odpad.poziom < odpad.max:
                    odpad.poziom += t * 0.3
                    self.total_waste += t * 0.3
                self.flows["brzeczka"] = 10.5; self.flows["osad"] = 4.2
            else:
                self.st_filtracja = "IDLE" 
                self.st_warzelnia = "WARZENIE"

        #WARZELNIA
        if self.st_warzelnia == "WARZENIE":
            warz.stan_tekst = "WARZENIE"
            if warz.temperatura < 100: warz.temperatura += 0.5
            else:
                if self.licznik_chmielu < 3.0:
                    self.chmiel_flow = True; self.flows["chmiel"] = 2.5
                    self.licznik_chmielu += 0.05; self.total_hops += 0.02
                else:
                    self.chmiel_flow = False; self.licznik_chmielu = 0.0
                    self.st_warzelnia = "CHLODZENIE"

        elif self.st_warzelnia == "CHLODZENIE":
            warz.stan_tekst = "CHLODZENIE"
            if warz.poziom > 0 and ferm.poziom < ferm.max:
                self.chlodzenie_active = True; self.flows["chlodzenie"] = 12.0
                warz.poziom -= 2.0; ferm.poziom += 2.0
                self.temp_wejscie = 100.0; self.temp_wyjscie = 20.0
            elif warz.poziom <= 0:
                warz.temperatura = 20.0; self.chlodzenie_active = False
                self.st_warzelnia = "IDLE" 

        #ROZLEW POTRÓJNY
        if ferm.poziom >= 1.5:
            ferm.stan_tekst = "WYDAWANIE X3"
            self.butelka_obecna = True; self.flows["rozlew"] = 6.0; self.progres_butelki += 25.0
            self.cisnienie_co2 = min(2.5, self.cisnienie_co2 + 0.01)
            if self.progres_butelki >= 100.0:
                self.progres_butelki = 0; self.licznik_butelek += 3; ferm.poziom -= 1.5
        else:
            ferm.stan_tekst = "IDLE"; self.butelka_obecna = False; self.cisnienie_co2 = 0.0