import csv
import sys
import json
import pickle


class Plik:
    def __init__(self, nazwa):
        self.nazwa = nazwa
        self.rozszerzenie = nazwa.split(".")[-1]  # wyodrębnij rozszerzenie pliku

    def odczytaj(self):
        if self.rozszerzenie == "csv":
            plik = PlikCSV(self.nazwa)
            return plik.odczytaj()
        elif self.rozszerzenie == "json":
            plik = PlikJSON(self.nazwa)
            return plik.odczytaj()
        elif self.rozszerzenie == "txt":
            plik = PlikTXT(self.nazwa)
            return plik.odczytaj()
        elif self.rozszerzenie == "pickle":
            plik = PlikPICKLE(self.nazwa)
            return plik.odczytaj()

        else:
            raise ValueError("Nieobsługiwane rozszerzenie pliku")

    def zapisz(self, dane):
        if self.rozszerzenie == "csv":
            plik = PlikCSV(self.nazwa)
            plik.zapisz(dane)
        elif self.rozszerzenie == "json":
            plik = PlikJSON(self.nazwa)
            plik.zapisz(dane)
        elif self.rozszerzenie == "txt":
            plik = PlikTXT(self.nazwa)
            plik.zapisz(dane)
        elif self.rozszerzenie == "pickle":
            plik = PlikPICKLE(self.nazwa)
            plik.zapisz(dane)
        else:
            raise ValueError("Nieobsługiwane rozszerzenie pliku")


class Zmieniacz(Plik):
    def zmien_wartosci(self, dane, zmiany):
        for zmiana in zmiany:
            z = zmiana.split(",")
            if len(z) != 3:
                print("Blad!!!!!!")
                quit()
            x, y, wartosc = z
            x = int(x) - 1
            y = int(y) - 1
            if x < 0 or y < 0:
                print("Blad, x i y musza byc wieksze od 0.")
                quit()
            dane[x][y] = wartosc
        return dane


class PlikCSV(Zmieniacz):
    def odczytaj(self):
        dane = []
        with open(self.nazwa, "r") as PlikCSV:
            czytnik = csv.reader(PlikCSV)
            for wiersz in czytnik:
                dane.append(wiersz)
        return dane

    def zapisz(self, dane):
        with open(self.nazwa, "w", newline="") as PlikCSV:
            zapis = csv.writer(PlikCSV)
            for wiersz in dane:
                zapis.writerow(wiersz)


class PlikJSON(Zmieniacz):
    def odczytaj(self):
        print(self.nazwa)
        with open(self.nazwa, "r") as plikjson:
            dane = json.load(plikjson)
        return dane

    def zapisz(self, dane):
        with open(self.nazwa, "w") as plikjson:
            json.dump(dane, plikjson)


class PlikTXT(Zmieniacz):
    def odczytaj(self):
        with open(self.nazwa, "r") as pliktxt:
            dane = pliktxt.read()
        return dane

    def zapisz(self, dane):
        with open(self.nazwa, "w") as pliktxt:
            dane_str = "\n".join(str(element) for element in dane)
            pliktxt.write(dane_str)


# Funkcje do odczytu i zapisu pliku PICKLE
class PlikPICKLE(Zmieniacz):
    def odczytaj(self):
        with open(self.nazwa, "rb") as plikpickle:
            dane = pickle.load(plikpickle)
        return dane

    def zapisz(self, dane):
        with open(self.nazwa, "wb") as plikpickle:
            pickle.dump(dane, plikpickle)


def stworz_klase_obslugi_pliku(plik_wejsciowy):
    if plik_wejsciowy.endswith(".csv"):
        plik = PlikCSV(plik_wejsciowy)
    elif plik_wejsciowy.endswith(".json"):
        plik = PlikJSON(plik_wejsciowy)
    elif plik_wejsciowy.endswith(".txt"):
        plik = PlikTXT(plik_wejsciowy)
    elif plik_wejsciowy.endswith(".pickle"):
        plik = PlikPICKLE(plik_wejsciowy)
    else:
        print("Nieobsługiwany format pliku!")
        sys.exit(1)
    return plik


# Główna funkcja programu
if __name__ == "__main__":
    # Sprawdzenie poprawności argumentów wywołania programu
    if len(sys.argv) < 3:
        print(
            "Sposób użycia: python reader.py <plik_wejsciowy> <plik_wyjsciowy> <zmiana_1> <zmiana_2> ... <zmiana_n>"
        )
        print(
            '<zmiana_x> - Zmiana w postaci "x,y,wartosc" - x (kolumna) oraz y (wiersz) są współrzędnymi liczonymi od 0, natomiast "wartosc" to zmiana, która ma trafić na podane miejsce.'
        )
        sys.exit(1)

    # Odczytanie nazw plików oraz zmian z argumentów wywołania programu
    plik_wejsciowy = sys.argv[1]
    plik_wyjsciowy = sys.argv[2]
    zmiany = sys.argv[3:]

    # # Odczytanie danych z pliku wejściowego
    # dane = odczytaj_csv(plik_wejsciowy)
    # Odczytanie danych z pliku wejściowego

    plik = stworz_klase_obslugi_pliku(plik_wejsciowy)
    plik_zapis = stworz_klase_obslugi_pliku(plik_wyjsciowy)

    dane = plik.odczytaj()

    # Przetworzenie zmian
    dane = plik.zmien_wartosci(dane, zmiany)

    # Wyświetlenie danych w terminalu
    for wiersz in dane:
        print(",".join(wiersz))

    # # Zapisanie danych do pliku wyjściowego
    # zapisz_csv(plik_wyjsciowy, dane)
    # Zapisanie danych do pliku wyjściowego
    plik_zapis.zapisz(dane)
