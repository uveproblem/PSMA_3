from datetime import datetime
import json
from matplotlib import pyplot as plt
from Samochod import Samochod
from Wynajmujący import Wynajmujacy


class VehicleNotAvailable(Exception):
    pass
class VehicleAlreadyExists(Exception):
    pass
class VehicleDoNotExist(Exception):
    pass
class InvalidMilage(Exception):
    pass
class InvalidPeriod(Exception):
    pass

class Wypozyczalnia:
    def __init__(self):
        self.pojazdy = {}
        self.historia_transakcji = []

    def dodaj_samochod(self, samochod):
        if samochod.nr_rejestracyjny in self.pojazdy:
            raise VehicleAlreadyExists("Istnieje już pojazd o takim numerze rejestracyjnym")
        for auto in self.pojazdy.values():
            if auto.nr_vin == samochod.nr_vin:
                raise VehicleAlreadyExists("Istnieje pojazd z takim numerem VIN")
        self.pojazdy[samochod.nr_rejestracyjny] = samochod

    def wypozycz_samochod(self, nr_rejestracyjny, wynajmujacy):
        teraz = datetime.now()
        if nr_rejestracyjny not in self.pojazdy:
            raise VehicleDoNotExist("Nie istnieje pojazd o podanym numerze rejestracyjnym")
        auto = self.pojazdy[nr_rejestracyjny]
        if auto.czy_wypozyczony:
            raise VehicleNotAvailable("Pojazd nie jest dostępny")
        else:
            auto.czy_wypozyczony = True
            transakcje = {
                "Data": teraz,
                "Wynajmujący": wynajmujacy,
                "Samochód": auto
            }
        self.historia_transakcji.append(transakcje)

    def zwroc_samochod(self, nr_rejestracyjny, aktualny_przebieg, liczba_dni):
        if nr_rejestracyjny not in self.pojazdy:
            raise VehicleDoNotExist("Nie istnieje taki pojazd")
        auto = self.pojazdy[nr_rejestracyjny]
        if not auto.czy_wypozyczony:
            raise VehicleDoNotExist("Pojazd nie był wypożyczony")
        if aktualny_przebieg < auto.przebieg:
            raise InvalidMilage("Nieprawidłowy przebieg")
        if liczba_dni <= 0:
            raise InvalidPeriod("Liczba dni musi być większa od zera")

        auto.przebieg = aktualny_przebieg
        auto.czy_wypozyczony = False
        return liczba_dni * auto.cena_wynajmu

    def wykres(self):
        popularnosc = {}
        for auto in self.pojazdy.values():
            etykieta = f"{auto.marka} {auto.model}({auto.nr_rejestracyjny})"
            popularnosc[etykieta] = 0

        for t in self.historia_transakcji:
            auto = t["Samochód"]
            etykieta = f"{auto.marka} {auto.model}({auto.nr_rejestracyjny})"
            popularnosc[etykieta] += 1

        samochody = list(popularnosc.keys())
        ilosci = list(popularnosc.values())
        plt.bar(samochody, ilosci)
        plt.xlabel("Modele")
        plt.ylabel("Popularność")
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()

    def zapisz_do_pliku(self, nazwa_pliku="baza.json"):
        dane_do_zapisu = {
            "pojazdy": [auto.to_dict() for auto in self.pojazdy.values()],
            "historia": [
                {
                    "nr_rejestracyjny": t["Samochód"].nr_rejestracyjny,
                    "wynajmujący": t["Wynajmujący"].to_dict(),
                    "data": t["Data"].isoformat()
                }
                for t in self.historia_transakcji
            ]
        }
        with open(nazwa_pliku, "w", encoding="utf-8") as plik:
            json.dump(dane_do_zapisu, plik, indent=4)

    def wczytaj_z_pliku(self, nazwa_pliku="baza.json"):
        try:
            with open(nazwa_pliku, "r", encoding="utf-8") as plik:
                dane = json.load(plik)
        except FileNotFoundError:
            return

        self.pojazdy = {}
        self.historia_transakcji = []

        for auto_dane in dane.get("pojazdy", []):
            auto = Samochod(
                auto_dane["marka"],
                auto_dane["model"],
                auto_dane["rok_produkcji"],
                auto_dane["nr_rejestracyjny"],
                auto_dane["nr_vin"],
                auto_dane["przebieg"],
                auto_dane["cena_wynajmu"]
            )
            auto.czy_wypozyczony = auto_dane.get("czy_wypozyczony", False)
            self.pojazdy[auto.nr_rejestracyjny] = auto

        for t in dane.get("historia", []):
            klient_dane = t["wynajmujący"]
            klient = Wynajmujacy(klient_dane["imie"], klient_dane["nazwisko"], klient_dane["nr_dowodu"])
            auto = self.pojazdy[t["nr_rejestracyjny"]]
            data = datetime.fromisoformat(t["data"])

            self.historia_transakcji.append({
                "Data": data,
                "Wynajmujący": klient,
                "Samochód": auto
            })
