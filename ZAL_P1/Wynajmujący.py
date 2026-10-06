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
