System SCADA: Automatyczna Linia Rozlewnicza 
1. Opis Projektu
   
Projekt stanowi drugi etap realizacji przedmiotu Informatyka II. Jest to aplikacja desktopowa w języku Python, która wizualizuje proces przemysłowy typu SCADA (Supervisory Control and Data Acquisition).
Symulacja przedstawia pracę automatycznej linii rozlewniczej w zakładzie produkcyjnym.

2. Scenariusz procesu:

  Napełnianie: Płyny z dwóch zbiorników surowców (Woda i Koncentrat) są transportowane rurami do Mieszalnika.
  
  Przetwarzanie: W Mieszalniku następuje proces łączenia składników oraz podgrzewanie cieczy za pomocą grzałki do zadanej temperatury.
  
  Transport końcowy: Gotowy produkt jest przepompowywany za pomocą pompy do zbiornika magazynowego.
  
  Monitoring: System automatycznie monitoruje poziomy cieczy oraz temperaturę, reagując na sytuacje alarmowe.

2. Funkcjonalności i Wymagania
   
  Wizualizacja graficzna: Ekran główny z 4 zbiornikami oraz systemem rur z zakrętami 90 stopni.
  
  Elementy dynamiczne: Animowana pompa, grzałka oraz przepływ cieczy w rurach.
  
  Automatyzacja: Proces przebiega w pełni automatycznie po zadaniu parametrów początkowych przez użytkownika.
  
  Architektura OOP: Program oparty na klasach reprezentujących elementy procesu, sygnały i ekrany.
  
  Wieluekranowość: Możliwość przełączania między widokiem instalacji a raportami i alarmami.

  3. Struktura Projektu (Klasy)
Zgodnie z zasadami projektowania obiektowego, kod został podzielony na moduły:

  ElementSystemu: Klasa bazowa dla obiektów fizycznych.

  Zbiornik: Zarządzanie poziomem i pojemnością.

  Urzadzenie: Logika pracy pomp i grzałek.

  Symulator: Główny silnik sterujący logiką procesu.

  Interfejs: Obsługa biblioteki graficznej i wyświetlanie stanów.
