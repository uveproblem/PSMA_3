class Samochod:
    def __init__(self, marka, model, rok_produkcji,nr_rejestracyjny, nr_vin, przebieg, cena_wynajmu):
        self.marka = str(marka)
        self.model = str(model)
        self.rok_produkcji = int(rok_produkcji)
        self.nr_rejestracyjny = str(nr_rejestracyjny)
        self.nr_vin = str(nr_vin)
        self.przebieg = int(przebieg)
        self.cena_wynajmu = float(cena_wynajmu)
        self.czy_wypozyczony = False

    def to_dict(self):
        return {
            "marka": self.marka,
            "model": self.model,
            "rok_produkcji": self.rok_produkcji,
            "nr_rejestracyjny": self.nr_rejestracyjny,
            "nr_vin": self.nr_vin,
            "przebieg": self.przebieg,
            "cena_wynajmu": self.cena_wynajmu,
            "czy_wypozyczony": self.czy_wypozyczony,
        }