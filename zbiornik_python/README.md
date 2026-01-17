# 🍺 SCADA Brewery Control System

Profesjonalny symulator systemu SCADA (Supervisory Control and Data Acquisition) do zarządzania procesem produkcji piwa w browarze rzemieślniczym. Aplikacja monitoruje parametry fizyczne, steruje przepływami i wizualizuje procesy w czasie rzeczywistym.



## 🚀 Główne Funkcje

* **Pipeline Processing (Przetwarzanie Potokowe):** System umożliwia równoległą pracę wielu urządzeń. Możesz mielić słód dla nowej warki, podczas gdy poprzednia jest już gotowana lub rozlewana.
* **Interaktywna Wizualizacja GUI:** * Dynamiczne animacje przepływu w rurach (ruchome kropki).
    * Realistyczny układ instalacji z rurą w kształcie litery U oraz symetrycznymi przyłączami.
    * **Potrójny Rozdzielacz (Trójząb):** System rozlewu napełniający 3 butelki jednocześnie z jednej rury głównej.
* **Automatyzacja Przemysłowa:**
    * Automatyczne sekwencje startowe i procesowe.
    * Inteligentny system opróżniania zbiornika na odpady (wywóz młóta).
    * Kontrola temperatury w kadziach i monitoring chłodnicy.
* **Raportowanie i Logistyka:**
    * Licznik produkcji (butelki, skrzynki, palety).
    * Raport zużycia surowców (słód, woda, chmiel) w czasie rzeczywistym.
    * Dynamiczny wskaźnik osiągnięcia celu produkcyjnego.

## 🛠 Technologie

* **Python 3.x** – Główny język programowania.
* **PyQt6** – Zaawansowany interfejs graficzny i silnik renderowania 2D.
* **Logic Pipeline Model** – Autorski model współbieżności procesów przemysłowych.

## 🏗 Struktura Projektu

* `main.py` – Punkt wejścia aplikacji, okno parametrów (Setup) i panel operatora.
* `gui.py` – Silnik graficzny rysujący instalację, animacje i trójząb rozlewniczy.
* `logic.py` – Logika biznesowa, automaty stanów (FSM) dla każdego zbiornika.
* `models.py` – Definicje obiektów fizycznych (Zbiornik, Srutownik itp.).
* `settings.py` – Konfiguracja kolorów, stałych procesowych i prędkości symulacji.

## 🚦 Jak uruchomić

1.  Upewnij się, że masz zainstalowanego Pythona 3.10+.
2.  Zainstaluj wymaganą bibliotekę PyQt6:
    ```bash
    pip install PyQt6
    ```
3.  Uruchom aplikację:
    ```bash
    python main.py
    ```
4.  W oknie początkowym zadaj cel produkcyjny (liczbę butelek) i kliknij "OTWÓRZ PANEL".

## 📸 Widok Systemu

System wizualizuje następujące etapy:
1.  **Śrutowanie:** Pobieranie i mielenie słodu.
2.  **Zacieranie:** Podgrzewanie i mieszanie w Kadzi Zaciernej.
3.  **Filtracja:** Oddzielanie brzeczki od młóta (odpadów).
4.  **Warzenie:** Gotowanie z automatycznym dawkowaniem chmielu.
5.  **Chłodzenie:** Przejście przez wymiennik ciepła do Fermentora.
6.  **Rozlew:** Trójfazowe napełnianie butelek na taśmociągu.

---
*Projekt stworzony na potrzeby edukacyjne jako demonstracja systemów sterowania procesami ciągłymi.*