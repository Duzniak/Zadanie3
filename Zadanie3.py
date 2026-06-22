from abc import ABC, abstractmethod
import uuid


class Bike(ABC):
    def __init__(self, brand: str, model: str, base_rate: float):
        self._bike_id = str(uuid.uuid4())[:6]
        self.brand = brand
        self.model = model
        self._base_rate = base_rate
        self.__is_rented = False

    @property
    def bike_id(self):
        return self._bike_id

    @property
    def base_rate(self):
        return self._base_rate

    @property
    def is_rented(self):
        return self.__is_rented

    def rent_bike(self):
        if not self.__is_rented:
            self.__is_rented = True
            return True
        return False

    def return_bike(self):
        self.__is_rented = False

    @abstractmethod
    def calculate_rental_cost(self, hours: int) -> float:
        pass

    @abstractmethod
    def __str__(self):
        pass


class CityBike(Bike):
    def __init__(self, brand: str, model: str, base_rate: float, has_basket: bool):
        super().__init__(brand, model, base_rate)
        self.has_basket = has_basket

    def calculate_rental_cost(self, hours: int) -> float:
        return self.base_rate * hours

    def __str__(self):
        basket_info = "z koszykiem" if self.has_basket else "bez koszyka"
        return f"[Miejski] {self.brand} {self.model} {basket_info} (ID: {self.bike_id}) - Stawka: {self.base_rate} zł/h"


class ElectricBike(Bike):
    def __init__(self, brand: str, model: str, base_rate: float, battery_level: int = 100):
        super().__init__(brand, model, base_rate)
        self.battery_level = battery_level

    def calculate_rental_cost(self, hours: int) -> float:
        return self.base_rate * hours + (self.battery_level * 0.1)

    def __str__(self):
        return f"[Elektryczny] {self.brand} {self.model} (ID: {self.bike_id}) - Stawka: {self.base_rate} zł/h, Pojemność baterii: {self.battery_level} %"


class MountainBike(Bike):
    def __init__(self, brand: str, model: str, base_rate: float, suspension_type: str):
        super().__init__(brand, model, base_rate)
        self.suspension_type = suspension_type

    def calculate_rental_cost(self, hours: int) -> float:
        return self.base_rate * hours + (10 if self.suspension_type == "full" else 5)

    def __str__(self):
        return f"[Górski] {self.brand} {self.model} (ID: {self.bike_id}) - Stawka: {self.base_rate} zł/h, Typ zawieszenia: {self.suspension_type}"


class Client:
    def __init__(self, name: str):
        self.name = name
        self.client_id = str(uuid.uuid4())[:6]
        self.rented_bikes = []

    def __str__(self):
        rented_info = ', '.join([f"{bike.brand} {bike.model}" for bike in self.rented_bikes])
        return f"Klient: {self.name} (ID: {self.client_id}) - Wypożyczone rowery: {rented_info}"


class RentalSystem:
    def __init__(self, title: str):
        self.name = title
        self.fleet = []
        self.clients = []

    def add_bike(self, bike: Bike):
        self.fleet.append(bike)

    def add_client(self, client: Client):
        self.clients.append(client)

    def process_rental(self, client: Client, bike: Bike, hours: int):
        if bike in self.fleet and not bike.is_rented:
            if bike.rent_bike():
                client.rented_bikes.append(bike)
                cost = bike.calculate_rental_cost(hours)
                print(f"Rower {bike.brand} {bike.model} został wypożyczony przez klienta {client.name}. Koszt: {cost} zł.")
            else:
                print(f"Rower {bike.brand} {bike.model} jest już wypożyczony.")
        else:
            print(f"Rower {bike.brand} {bike.model} nie jest dostępny do wypożyczenia.")

    def process_return(self, client: Client, bike: Bike):
        if bike in client.rented_bikes:
            bike.return_bike()
            client.rented_bikes.remove(bike)
            print(f"\nRower {bike.brand} {bike.model} został zwrócony przez klienta {client.name}.")
        else:
            print(f"\nRower {bike.brand} {bike.model} nie jest wypożyczony przez klienta {client.name}.")

    def show_status(self):
        print(f"\nSystem wypożyczalni: {self.name}")
        if not self.clients:
            print("Brak aktywnych klientów w systemie.")
        for client in self.clients:
            print(f"\n*{client}")
            if not client.rented_bikes:
                print("Brak wypożyczonych rowerów.")
            for bike in client.rented_bikes:
                print(f"Wypożyczono: {bike}")


if __name__ == "__main__":
    rental_system = RentalSystem("Wypożyczalnia Rowerów")

    city_bike1 = CityBike("Romet", "Gazela", 10, True)
    city_bike2 = CityBike("Romet", "Luiza", 12, False)
    electric_bike1 = ElectricBike("Giant", "Stance E+", 20, 80)
    electric_bike2 = ElectricBike("Focus", "Jam", 20, 80)
    mountain_bike1 = MountainBike("Mondrakrer", "Dune", 15, "full")
    mountain_bike2 = MountainBike("Dartmoor", "Primal", 15, "hardtail")
    mountain_bike3 = MountainBike("Trek", "Slash 8", 15, "full")

    rental_system.add_bike(city_bike1)
    rental_system.add_bike(city_bike2)
    rental_system.add_bike(electric_bike1)
    rental_system.add_bike(electric_bike2)
    rental_system.add_bike(mountain_bike1)
    rental_system.add_bike(mountain_bike2)
    rental_system.add_bike(mountain_bike3)

    client1 = Client("Jan Duźniak")
    client2 = Client("Anna Nowak")
    client3 = Client("Piotr Kowalski")

    rental_system.add_client(client1)
    rental_system.add_client(client2)
    rental_system.add_client(client3)

    rental_system.process_rental(client1, mountain_bike1, 3)
    rental_system.process_rental(client2, electric_bike2, 2)
    rental_system.process_rental(client3, mountain_bike3, 5)

    rental_system.show_status()

    rental_system.process_return(client2, electric_bike2)
    rental_system.process_return(client3, mountain_bike3)

    rental_system.show_status()
        