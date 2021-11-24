import os
import csv

POSSIBLE_CAR_TYPES = ('car', 'truck', 'spec_machine')
POSSIBLE_PHOTO_F_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif')


class CarBase:
    def __init__(self, brand, photo_file_name, carrying):
        self.car_type = None
        self.photo_file_name = photo_file_name
        self.brand = brand
        self.carrying = carrying

    def get_photo_file_ext(self):
        # ['filename', '.extension']
        return os.path.splitext(self.photo_file_name)[1]


class Car(CarBase):
    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = 'car'
        self.passenger_seats_count = int(passenger_seats_count)

    def __repr__(self):
        return self.car_type


class Truck(CarBase):
    def __init__(self, brand, photo_file_name, carrying, body_lwh):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = 'Truck'
        self.body_length = 0.0
        self.body_width = 0.0
        self.body_height = 0.0
        self.body_volume = 0.0
        self.set_truck_body_volume(body_lwh)

    def __repr__(self):
        return self.car_type

    def get_body_volume(self):
        return self.body_volume

    def set_truck_body_volume(self, body_lwh):
        try:
            l, w, h = map(float, body_lwh.split('x'))
        except ValueError:
            l, w, h = 0.0, 0.0, 0.0

        self.body_length = l
        self.body_width = w
        self.body_height = h
        self.body_volume = l * w * h


class SpecMachine(CarBase):
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = 'spec_machine'
        self.extra = extra

    def __repr__(self):
        return self.car_type


def get_car_list(csv_filename):
    car_list = []

    with open(csv_filename) as csv_file:
        reader = csv.DictReader(csv_file, delimiter=';')
        valid_csv_len = len(reader.fieldnames)
        for row in reader:
            car = get_car_from_csv_row(row, valid_csv_len)
            if car:
                car_list.append(car)
            else:
                print('Invalid row: ', row)

        return car_list


def get_car_from_csv_row(row, valid_csv_len):
    car_type, brand, passenger_sc, photo_f_ext, body_whl, carrying, extra = row.values()

    if len(row) != valid_csv_len or car_type not in POSSIBLE_CAR_TYPES:
        return None

    if car_type not in POSSIBLE_CAR_TYPES:
        return None
    if not (brand and photo_f_ext and carrying):
        return None
    if os.path.splitext(photo_f_ext)[1] not in POSSIBLE_PHOTO_F_EXTENSIONS:
        return None

    try:
        carrying = float(carrying)
    except ValueError:
        return None

    if car_type == Car.__name__.lower():
        try:
            passenger_sc = int(passenger_sc)
        except ValueError:
            return None
        return Car(brand, photo_f_ext, carrying, passenger_sc)

    if car_type == Truck.__name__.lower():
        return Truck(brand, photo_f_ext, carrying, body_whl)

    if car_type == SpecMachine.__name__.lower():
        if not extra:
            return None
        return SpecMachine(brand, photo_f_ext, carrying, extra)


# truck_1 = Truck('Komatsu-D355', 'd355.jpg', '93', '3x2x10')
# print(truck_1.get_photo_file_ext())

# test_car_list = get_car_list('cars.csv')
