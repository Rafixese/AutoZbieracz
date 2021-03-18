# AutoZbieracz
Skrypt do automatycznego zbierania surowców w grze przeglądarkowej Plemiona

# Instalacja

## Google Chrome

https://www.google.com/chrome/

## Python 3.8.8

https://www.python.org/downloads/release/python-388/

## Requirements

Wejdź do katalogu głównego AutoZbieracz przez terminal. Wykonaj polecenie.
```pip install -r requirements.txt```
dla python 2 lub Windows lub
```pip3 install -r requirements.txt```
dla python 3

# Konfiguracja
## config.yaml

- browser - Czy pokazać okno przeglądarki - ```True``` lub ```False```
- credentials:
  - login - nasz login do gry. ```"JanKowalski```
  - password: - nasze hasło do gry ```"hasełko"```
- webdriver:
  - chrome:
    - version - wpisujemy w pole adresowe w przeglądarce ```chrome://settings/help```. Pojawi nam się przykładowo ```Wersja 89.0.4389.90 (Oficjalna wersja) (64-bitowa)```. Wpisujemy więc numer ```89```
    - platform - wybieramy opcję pasującą do naszego systemu:
      - ```'chromedriver_linux64'```
      - ```'chromedriver_mac64'```
      - ```'chromedriver_mac64_m1'```
      - ```chromedriver_win32'```
- game:
  - world - świat, na którym gramy. np. ```164```
  - villages - numery naszych wiosek. Muszą być podane w formacie ```['1234', '4321']```

## pliki skryptów (.js)

Świeżo pobrana wersja AutoZbieracza w folderze ```config/``` zawiera plik ```template.js```. Tworzymy kopię tego pliku i nazywamy go numerem naszej wioski, który podaliśmy w tablicy w pliku ```config.yaml```. Wynikowa nazwa pliku powinna wyglądać mniej więcej tak: ```1234.js``` i znajdować się w tym samymy folderze co ```template.js```.

Co do samej konfiguracji pliku odsyłam do dokumentacji twórcy:
```
// max_ressources - max amount of resources to gather from one level (rounding may cause some reduction)
// archers - is the world with archers (1 - yes, 0 - no)
// skip_level_1 - do you want to skip 1 level (the least efficient one) when others are unlocked?
//
// untouchable - troops "invisible" for this script, to be completely ignored
// max_unit_number - at most this number of troops of a kind will be send in total
// conditional_safeguard - troops to leave in village if possible in total, but if not, they will be send
```

# Włączenie skryptu
Uruchamiamy plik ```start.bat``` dla Windows lub ```start.sh``` dla pozostałych systemów.

# Czynności niezalecane
Przede wszystkim nie zaleca się logowania do plemion z innej przeglądarki w czasie działania bota. Może to przyczynić się do crasha programu.
