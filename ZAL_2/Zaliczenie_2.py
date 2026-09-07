from datetime import datetime
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QTabWidget

import matplotlib.pyplot as plt
import json
import numpy as np

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

class Wynajmujacy:
    def __init__(self, imie, nazwisko, nr_dowodu):
        self.imie = imie
        self.nazwisko = nazwisko
        self.nr_dowodu = nr_dowodu

    def to_dict(self):
        return {
            "imie": self.imie,
            "nazwisko": self.nazwisko,
            "nr_dowodu": self.nr_dowodu
        }
    @classmethod
    def from_dict(cls, dane):
        return cls(dane["imie"], dane["nazwisko"], dane["nr_dowodu"])

class Samochod:
    def __init__(self, marka, model, rok_produkcji, nr_vin, nr_rejestracyjny, przebieg, cena_wynajmu_doba):
        self.marka = str(marka)
        self.model = str(model)
        self.rok_produkcji = int(rok_produkcji)
        self.nr_vin = str(nr_vin)
        self.nr_rejestracyjny = str(nr_rejestracyjny)
        self.przebieg = int(przebieg)
        self.cena_wynajmu_doba = float(cena_wynajmu_doba)
        self.czy_wypozyczony = False

    def to_dict(self):
        return {
            "marka": self.marka,
            "model": self.model,
            "rok_produkcji": self.rok_produkcji,
            "nr_vin": self.nr_vin,
            "nr_rejestracyjny": self.nr_rejestracyjny,
            "przebieg": self.przebieg,
            "cena_wynajmu_doba": self.cena_wynajmu_doba,
            "czy_wypozyczony": self.czy_wypozyczony
        }
    @classmethod
    def from_dict(cls, dane):
        auto = cls(
            dane["marka"],
            dane["model"],
            dane["rok_produkcji"],
            dane["nr_vin"],
            dane["nr_rejestracyjny"],
            dane["przebieg"],
            dane["cena_wynajmu_doba"],
        )
        auto.czy_wypozyczony = dane.get("czy_wypozyczony", False)
        return auto

class Wypozyczalnia:
    def __init__(self):
        self.pojazdy = {}
        self.historia_transakcji = []

    def dodaj_samochod(self, samochod):
        if samochod.nr_rejestracyjny in self.pojazdy:
            raise VehicleAlreadyExists("Istnieje już pojazd z tą rejestracją")
        for auto in self.pojazdy.values():
            if auto.nr_vin == samochod.nr_vin:
                raise VehicleAlreadyExists("Istnieje już pojazd z takim numerem VIN")
        self.pojazdy[samochod.nr_rejestracyjny] = samochod

    def wypozycz_samochod(self, nr_rejestracyjny, wynajmujacy):
        teraz = datetime.now()
        if nr_rejestracyjny not in self.pojazdy:
            raise VehicleDoNotExist("Nie istnieje pojazd o takim numerze rejestracyjnym")
        auto = self.pojazdy[nr_rejestracyjny]
        if auto.czy_wypozyczony:
            raise VehicleNotAvailable("Pojazd jest już wypożyczony")
        else:
            auto.czy_wypozyczony = True
        transakcja = {
            "samochod": auto,
            "wynajmujacy": wynajmujacy,
            "data_wypozyczenia": teraz
        }
        self.historia_transakcji.append(transakcja)

    def zwroc_samochod(self, nr_rejestracyjny, aktualny_przebieg, liczba_dni):
        if nr_rejestracyjny not in self.pojazdy:
            raise VehicleDoNotExist("Nie istnieje pojazd o takim numerze rejestracyjnym")
        auto = self.pojazdy[nr_rejestracyjny]
        if not auto.czy_wypozyczony:
            raise VehicleNotAvailable("Pojazd nie był wypożyczony")
        if aktualny_przebieg < auto.przebieg:
            raise InvalidMilage("Nowy przebieg jest niższy niż poprzedni")
        else:
            auto.przebieg = aktualny_przebieg
        auto.czy_wypozyczony = False
        if liczba_dni <= 0:
            raise InvalidPeriod
        koszt = liczba_dni * auto.cena_wynajmu_doba
        return koszt

    def wykres(self):
        popularnosc = {}
        for auto in self.pojazdy.values():
            etykieta = f"{auto.marka} {auto.model}({auto.nr_rejestracyjny})"
            popularnosc[etykieta] = 0

        for t in self.historia_transakcji:
            auto = t["samochod"]
            etykieta = f"{auto.marka} {auto.model}({auto.nr_rejestracyjny})"
            popularnosc[etykieta] += 1

        samochody = list(popularnosc.keys())
        ilosci = list(popularnosc.values())
        plt.figure(figsize=(10, 5))
        plt.bar(samochody, ilosci, color="skyblue")
        plt.xlabel("Pojazd")
        plt.ylabel("Ilość najmów")
        plt.title("Popularnosc aut")
        plt.xticks(rotation=60)
        plt.tight_layout()
        plt.show()


    def zapisz_do_pliku(self, plik="baza.json"):
        dane = {
            "pojazdy": [auto.to_dict() for auto in self.pojazdy.values()],
            "historia": [
                {
                    "samochod_rejestracja": t["samochod"].nr_rejestracyjny,
                    "wynajmujacy": t["wynajmujacy"].to_dict(),
                    "data_wypozyczenia": t["data_wypozyczenia"].isoformat(),
                }
                for t in self.historia_transakcji
            ]
        }
        with open(plik, "w", encoding="utf-8") as f:
            json.dump(dane, f, indent=4)

    def wczytaj_z_pliku(self, plik="baza.json"):
        try:
            with open(plik, "r", encoding="utf-8") as f:
                dane = json.load(f)
        except FileNotFoundError:
            return None

        self.pojazdy = {}
        self.historia_transakcji = []

        for auto_slownik in dane.get("pojazdy", []):
            auto = Samochod.from_dict(auto_slownik)
            self.pojazdy[auto.nr_rejestracyjny] = auto

        for h in dane.get("historia", []):
            klient = Wynajmujacy.from_dict(h["wynajmujacy"])
            auto = self.pojazdy[h["samochod_rejestracja"]]
            data = datetime.fromisoformat(h["data_wypozyczenia"])
            self.historia_transakcji.append({
                "samochod": auto,
                "wynajmujacy": klient,
                "data_wypozyczenia": data
            })

class WypozyczalniaGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("System Zarządzania Wypożyczalnią")
        self.resize(1200, 900)

        self.wypozyczalnia = Wypozyczalnia()
        self.wypozyczalnia.wczytaj_z_pliku()

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.tab_flota = QWidget()
        self.tab_operacje = QWidget()

        self.tabs.addTab(self.tab_flota, "Zarządzanie flotą")
        self.tabs.addTab(self.tab_operacje, "Wypożyczenia i zwroty")

        self.init_tab_flota()
        self.init_tab_operacja()

    def init_tab_flota(self):
        layout = QVBoxLayout()
        self.tabela_samochodow = QTableWidget()
        self.tabela_samochodow.setColumnCount(8)
        self.tabela_samochodow.setHorizontalHeaderLabels(["Marka", "Model", "Rok", "VIN", "Rejestracja", "Przebieg", "Cena", "Status"])
        layout.addWidget(self.tabela_samochodow)

        form_layout = QHBoxLayout()
        self.input_marka = QLineEdit()
        self.input_marka.setPlaceholderText("Marka")
        self.input_model = QLineEdit()
        self.input_model.setPlaceholderText("Model")
        self.input_rok = QLineEdit()
        self.input_rok.setPlaceholderText("Rok")
        self.input_vin = QLineEdit()
        self.input_vin.setPlaceholderText("VIN")
        self.input_rejestracja = QLineEdit()
        self.input_rejestracja.setPlaceholderText("Rejestracja")
        self.input_przebieg = QLineEdit()
        self.input_przebieg.setPlaceholderText("Przebieg")
        self.input_cena = QLineEdit()
        self.input_cena.setPlaceholderText("Cena")

        for inp in [
            self.input_marka,
            self.input_model,
            self.input_rok,
            self.input_vin,
            self.input_rejestracja,
            self.input_przebieg,
            self.input_cena,
        ]:
            form_layout.addWidget(inp)
        layout.addLayout(form_layout)

        btn_layout = QHBoxLayout()
        self.btn_dodaj_auto = QPushButton("➕ Dodaj samochód")
        self.btn_dodaj_auto.clicked.connect(self.obsluz_dodawanie_samochodu)

        self.btn_wykres = QPushButton("📊 Pokaż wykres popularności")
        self.btn_wykres.clicked.connect(self.wypozyczalnia.wykres)

        btn_layout.addWidget(self.btn_dodaj_auto)
        btn_layout.addWidget(self.btn_wykres)
        layout.addLayout(btn_layout)

        self.tab_flota.setLayout(layout)

        self.odswiez_tabele()
    def odswiez_tabele(self):
        self.tabela_samochodow.setRowCount(0)
        for row_idx, auto in enumerate(self.wypozyczalnia.pojazdy.values()):
            self.tabela_samochodow.insertRow(row_idx)
            status = "Wypożyczony" if auto.czy_wypozyczony else "Dostępny"

            dane_wiersza = [
                auto.marka, auto.model, str(auto.rok_produkcji), auto.nr_vin, auto.nr_rejestracyjny, str(auto.przebieg), str(auto.cena_wynajmu_doba), status
            ]
            for col_idx, wartosc in enumerate(dane_wiersza):
                self.tabela_samochodow.setItem(row_idx, col_idx, QTableWidgetItem(wartosc))

    def obsluz_dodawanie_samochodu(self):
        try:
            marka = self.input_marka.text().strip()
            model = self.input_model.text().strip()
            rok = int(self.input_rok.text().strip())
            vin = self.input_vin.text().strip()
            rej = self.input_rejestracja.text().strip()
            przebieg = int(self.input_przebieg.text().strip())
            cena = float(self.input_cena.text().strip())

            if not (marka and model and vin and rej):
                raise ValueError("Wszystkie pola muszą być wypełnione!")

            nowy_samochod = Samochod(marka, model, rok, vin, rej, przebieg, cena)
            self.wypozyczalnia.dodaj_samochod(nowy_samochod)

            self.odswiez_tabele()
            QMessageBox.information(self, "Sukces", "Pojazd został dodany do bazy!")

            for inp in [self.input_marka, self.input_model, self.input_rok, self.input_vin,
                        self.input_rejestracja, self.input_przebieg, self.input_cena]:
                inp.clear()

        except ValueError as e:
            QMessageBox.warning(self, "Błąd danych", f"Niepoprawne dane: {e}")
        except VehicleAlreadyExists as e:
            QMessageBox.critical(self, "Błąd pojazdu", str(e))

    def init_tab_operacja(self):
        pass


    def closeEvent(self, event):
        self.wypozyczalnia.zapisz_do_pliku()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    okno = WypozyczalniaGUI()
    okno.show()
    sys.exit(app.exec())