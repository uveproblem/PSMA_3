from numpy.ma.core import append

class Wynajmujacy:
    def __init__(self, imie, nazwisko, nr_dowodu):
        self.imie = imie
        self.nazwisko = nazwisko
        self.nr_dowodu = nr_dowodu

class Samochod:
    def __init__(self, marka, model, rok_produkcji, nr_vin, nr_rejestracyjny, przebieg, cena_wynajmu_doba, czy_wypozyczony):
        self.marka = str(marka)
        self.model = str(model)
        self.rok_produkcji = int(rok_produkcji)
        self.nr_vin = str(nr_vin)
        self.nr_rejestracyjny = str(nr_rejestracyjny)
        self.przebieg = int(przebieg)
        self.cena_wynajmu_doba = float(cena_wynajmu_doba)
        self.czy_wypozyczony = bool(czy_wypozyczony)

class Wypozyczalnia:
    def __init__(self):
        self.pojazdy = {}
        self.historia_transakcji = []

    def dodaj_samochod(self, samochod):
        if samochod.nr_rejestracyjny in self.pojazdy:
            print("Już istnieje pojazd z takim numerem rejestracyjnym")
        else:
            duplikat_vin = False
            for auto in self.pojazdy.values():
                if auto.nr_vin == samochod.nr_vin:
                    duplikat_vin = True
                    print("Istnieje już samochód z podanym numerem VIN")
            break
            if duplikat_vin == False:
            self.pojazdy[samochod] = append(nr.rejestracyjny)

    def wypozycz_samochod(self, nr_rejestracyjny, wynajmujacy):

    def zwroc_samochod(self, nr_rejestracyjny, aktualny_przebieg, liczba_dni):