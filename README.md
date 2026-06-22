# System Wypożyczalni Rowerów (Bike Rental System)

## Krótki opis tematu aplikacji
Aplikacja to konsolowy system stworzony do obsługi wypożyczalni rowerów. Pozwala na łatwe zarządzanie dostępną flotą (od zwykłych rowerów miejskich, przez górskie, aż po elektryki) oraz bazą klientów. System procesuje same wypożyczenia i zwroty oraz automatycznie wylicza koszty dla klienta. Wykorzystuje do tego zasady polimorfizmu, dzięki czemu każdy typ roweru ma swoją własną, unikalną logikę naliczania opłat.

## Lista klas
1. **Bike (Klasa Abstrakcyjna)**
   * **Odpowiedzialność:** Definiuje wspólny kontrakt i bazowe właściwości dla wszystkich typów rowerów w systemie.
   * **Właściwości:** `brand`, `model`, chronione `_bike_id` oraz `_base_rate`, prywatne `__is_rented`.
   * **Metody:** Gettery właściwości (`bike_id`, `base_rate`, `is_rented`), metody mutujące stan (`rent_bike()`, `return_bike()`), abstrakcyjne metody wymuszające implementację: `calculate_rental_cost()` oraz `__str__()`.

2. **CityBike**
   * **Odpowiedzialność:** Reprezentuje rower miejski.
   * **Właściwości:** Dziedziczy po `Bike` + `has_basket`.
   * **Metody:** Implementuje standardowe obliczanie kosztów (`calculate_rental_cost`) i formatowanie tekstu.

3. **ElectricBike**
   * **Odpowiedzialność:** Reprezentuje rower elektryczny.
   * **Właściwości:** Dziedziczy po `Bike` + `battery_level`.
   * **Metody:** Implementuje `calculate_rental_cost` z doliczeniem opłaty zależnej od pojemności baterii.

4. **MountainBike**
   * **Odpowiedzialność:** Reprezentuje rower górski (MTB).
   * **Właściwości:** Dziedziczy po `Bike` + `suspension_type` (rodzaj amortyzacji).
   * **Metody:** Implementuje `calculate_rental_cost` z doliczeniem stałej kwoty uzależnionej od typu zawieszenia (full / hardtail).

5. **Client**
   * **Odpowiedzialność:** Reprezentuje klienta wypożyczalni, przechowując jego dane oraz przypisane do niego zasoby.
   * **Właściwości:** `name`, generowane `client_id`, lista `rented_bikes`.

6. **RentalSystem**
   * **Odpowiedzialność:** Centralny punkt (Controller) zarządzający logiką systemu wypożyczalni.
   * **Właściwości:** `name`, kolekcje `fleet` (dostępne rowery) oraz `clients` (zarejestrowani użytkownicy).
   * **Metody:** `add_bike()`, `add_client()`, `process_rental()`, `process_return()`, `show_status()`.

## Opis relacji między klasami
* **Dziedziczenie (is-a):** Klasy `CityBike`, `ElectricBike` oraz `MountainBike` dziedziczą atrybuty i metody po ogólnej klasie `Bike`.

* **Kolekcja obiektów (Agregacja/Kompozycja):** 
Klasa `RentalSystem` agreguje obiekty klas `Bike` w liście `fleet` oraz obiekty klas `Client` w liście `clients`. Dodatkowo obiekt `Client` posiada własną kolekcję przypisanych do niego obiektów `Bike` w liście `rented_bikes`.

* **Przekazanie obiektu jako parametr:** 
Metody biznesowe `process_rental` oraz `process_return` w klasie `RentalSystem` przyjmują jako argumenty gotowe instancje obiektów klas `Client` oraz `Bike`, aby wywołać na nich odpowiednie operacje.

## Wskazanie czterech zasad OOP

1. **Abstrakcja:** 
Wykorzystano moduł `abc` i dekorator `@abstractmethod`. Klasa `Bike` nie pozwala na utworzenie bezpośredniego obiektu - stanowi jedynie zarys (interfejs) tego, co każdy rower musi posiadać, ukrywając zbędne detale implementacyjne przed użytkownikiem systemu.

2. **Dziedziczenie:** 
Klasy pochodne (`CityBike`, `ElectricBike`, `MountainBike`) przejmują logikę klasy `Bike`. Dzięki użyciu `super().__init__()` uniknięto dublowania kodu nadającego numery ID, zapisującego markę, model i stawkę bazową.

3. **Enkapsulacja:** 
Wrażliwe dane zostały ukryte. Zmienna `__is_rented` jest w pełni prywatna, a dostęp do niej z zewnątrz odbywa się wyłącznie poprzez dekoratory `@property` (tylko do odczytu) oraz kontrolowane metody `rent_bike()` i `return_bike()`. Ukryto również stawkę bazową `_base_rate`.

4. **Polimorfizm:** 
Ta sama metoda `calculate_rental_cost(hours)` zachowuje się różnie w zależności od typu obiektu, na którym jest wywoływana. Oblicza stawkę standardowo dla roweru miejskiego, dolicza koszt za procenty baterii w rowerze elektrycznym, a dla roweru górskiego warunkuje cenę od rodzaju zawieszenia (doliczając 10 zł dla pełnego zawieszenia lub 5 zł w innych przypadkach).
