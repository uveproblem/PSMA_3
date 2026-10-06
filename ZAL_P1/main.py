from Samochod import Samochod
from Wypozyczalnia import Wypozyczalnia, VehicleAlreadyExists

def main():
    wypozyczalnia = Wypozyczalnia()
    auto1 = Samochod("Toyota", "Corolla", 2021, "WA12345", "VIN11111111111", 50000, 150.0)
    auto2 = Samochod("Skoda", "Octavia", 2022, "KR98765", "VIN22222222222", 30000, 180.0)

    auto3_dubel_rej = Samochod("BMW", "Seria 3", 2020, "WA12345", "VIN33333333333", 70000, 250.0)

    auto4_dubel_vin = Samochod("Audi", "A4", 2023, "GD55555", "VIN11111111111", 15000, 220.0)

    auta_do_dodania = [
        auto1,
        auto2,
        auto3_dubel_rej,
        auto4_dubel_vin,
    ]

    for auto in auta_do_dodania:
        try:
            wypozyczalnia.dodaj_samochod(auto)
            print(f"[SUKCES] Dodano: {auto.marka} {auto.model} (Rejestracja: {auto.nr_rejestracyjny}, VIN: {auto.nr_vin})")
        except VehicleAlreadyExists as e:
            print(f"Nie dodano {auto.marka} {auto.model} ({auto.nr_rejestracyjny}): {e}")

    print("\n--- AKTUALNA FLOTA W WYPOŻYCZALNI ---")
    for rej, auto in wypozyczalnia.pojazdy.items():
        print(f"- {rej}: {auto.marka} {auto.model} | VIN: {auto.nr_vin} | Cena: {auto.cena_wynajmu} zł/doba")

if __name__ == "__main__":
    main()
