System SCADA: Automatyczna Linia Rozlewnicza 
1. Opis Projektu
   
Projekt stanowi wizualizację i symulację zautomatyzowanego procesu przemysłowego typu SCADA (Supervisory Control and Data Acquisition). 
Aplikacja została stworzona w języku Python z wykorzystaniem biblioteki PyQt6 i modeluje pełny cykl produkcyjny browaru – od przygotowania surowców po rozlew gotowego produktu.

2. Funkcjonalności
   
Wizualizacja procesów: Dynamiczne poziomy cieczy, animowane mieszadła, przepływy w rurach oraz system napełniania butelek.

Siedem etapów produkcji: Śrutowanie (Pobieranie słodu i mielenie w śrutowniku), Zacieranie (Podgrzewanie zacieru w kadzi zaciernej z kontrolą temperatury), Filtracja (Oddzielanie brzeczki od młóta (odpadów)), Warzenie (Gotowanie brzeczki i automatyczne dozowanie chmielu), Chłodzenie (Przejście przez wymiennik ciepła (chłodnicę) z monitoringiem temperatury Wejściowej i Wyjciowej), Fermentacja (Kontrolowany proces w fermentorze z monitoringiem ciśnienia CO2), Rozlew (Automatyczna linia rozlewnicza napełniająca butelki na taśmociągu).

Raport Produkcyjny: Dynamiczne podsumowanie zużycia słodu, wody, chmielu oraz licznik wyprodukowanych butelek.


3. Wymagania Techniczne

Obiekty: 6 zbiorników, system rur z zakrętami 90 stopni, elementy dynamiczne (mieszadła, chłodnica, taśmociąg)

Logika: Proces przebiega automatycznie na podstawie zadanych parametrów

Architektura: Program oparty na programowaniu obiektowym (OOP) z podziałem na logikę (logic.py), interfejs (gui.py) i model danych (models.py)
